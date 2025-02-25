import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
import time
import traceback
import json
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import groq

# Load environment variables
load_dotenv()

# Set page title and layout
st.set_page_config(page_title="Web Q&A Tool", page_icon="🤖", layout="centered")

# Sidebar section for web page ingestion
st.sidebar.title("🌐 Web Page Ingestion")
st.sidebar.markdown("Enter URLs to ingest webpage content.")

# Initialize Pinecone connection
def initialize_pinecone():
    """Initialize Pinecone index and return the index object."""
    try:
        api_key = os.environ.get("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY not set in environment variables.")
        
        pc = Pinecone(api_key=api_key)
        index_name = 'smart-data-catalog'
        
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1024,
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
        index = pc.Index(index_name)
        return index, pc
    except Exception as e:
        st.error(f"Error initializing Pinecone: {e}")
        raise

index, pc = initialize_pinecone()

# Maintain list of URLs in session state
if "urls" not in st.session_state:
    st.session_state.urls = [""]

# Display URL input fields
for i, url in enumerate(st.session_state.urls):
    col1, col2 = st.sidebar.columns([0.85, 0.15])
    st.session_state.urls[i] = col1.text_input(f"URL {i+1}", value=url, key=f"url_{i}")
    
    # Remove URL button
    if col2.button("❌", key=f"remove_{i}", help="Remove URL"):
        del st.session_state.urls[i]
        st.rerun()

# Add a new URL input field
if st.sidebar.button("➕ Add URL"):
    st.session_state.urls.append("")
    st.rerun()

def split_text_by_bytes(text, max_bytes=40960):
    """Splits text into smaller chunks to fit within Pinecone's 40KB metadata limit."""
    chunks = []
    current_chunk = ""
    
    for paragraph in text.split("\n"):
        paragraph_bytes = len(paragraph.encode('utf-8')) 
        
        if len(current_chunk.encode('utf-8')) + paragraph_bytes > max_bytes:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            current_chunk += "\n" + paragraph
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

# Submit URLs and ingest webpage content
if st.sidebar.button("Submit"):
    for url in st.session_state.urls:
        try:
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, "html.parser")
            text = ' '.join([p.get_text() for p in soup.find_all("p")])
            
            if text:
                text_chunks = split_text_by_bytes(text)
                
                for i, chunk in enumerate(text_chunks):
                    embedding = pc.inference.embed(
                        model="llama-text-embed-v2",
                        inputs=[chunk],
                        parameters={"input_type": "passage"}
                    )[0].values
                    
                    index.upsert(vectors=[{
                        "id": f"content_{time.time()}_{i}",
                        "values": embedding,
                        "metadata": {"text": chunk}
                    }])
                
                st.sidebar.success(f"✅ Chatbot is ready to answer queries")
            else:
                st.sidebar.warning(f"No content found in {url}")

        except Exception as e:
            st.sidebar.error(f"Failed to ingest {url}: {str(e)}")

# Chatbot UI
st.title("💬 Web Content Q&A Chatbot")

# Chat container
chat_container = st.container()

# Maintain chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous chat messages
for role, text in st.session_state.chat_history:
    with chat_container:
        st.chat_message(role).write(text)

# Capture user input
question = st.chat_input("Ask a question...")

def answer_question(question, index, pc):
    """Retrieves relevant content from Pinecone and generates an answer using Groq API."""
    try:
        with st.spinner("Thinking..."):
            # Generate question embedding
            question_embedding = pc.inference.embed(
                model="llama-text-embed-v2",
                inputs=[question],
                parameters={"input_type": "query"}
            )[0].values
            
            # Query Pinecone for relevant content
            results = index.query(
                vector=question_embedding,
                top_k=5,
                include_metadata=True
            )
            
            if not results["matches"]:
                return "No relevant content found."
            
            matched_texts = [match["metadata"]["text"] for match in results["matches"]]
            combined_context = "\n\n".join(matched_texts)
            
            # Limit context to 5000 characters to reduce token usage
            combined_context = combined_context[:5000]  

            # Initialize Groq API
            groq_api_key = os.getenv("GROQ_API_KEY")
            client = groq.Client(api_key=groq_api_key)
            prompt = f"""
            Instruction:
            1. Only answer from the given context. Do not answer anything outside the context.
            2. Summarize the answer concisely.
            3. Use bullet points or sections where necessary.
            4. Answer in full sentences.
            5. If the question is out of context, respond that the chatbot cannot answer.

            Context: {combined_context}\n\n
            User Query: {question}
            """

            # Generate response
            response = client.chat.completions.create(
                model="gemma2-9b-it",
                temperature=0,
                messages=[
                    {"role": "system", "content": "Answer based only on the provided content."},
                    {"role": "user", "content": prompt}
                ],
            )

            return response.choices[0].message.content
        
    except Exception as e:
        return f"Error answering question: {e}"

# **Fix: Show user question immediately**
if question:
    # Add user question to history first
    st.session_state.chat_history.append(("user", question))

    # Display user question immediately
    with chat_container:
        st.chat_message("user").write(question)

    # Generate and display the assistant's response
    answer = answer_question(question, index, pc)
    st.session_state.chat_history.append(("assistant", answer))

    # Show assistant response immediately
    with chat_container:
        st.chat_message("assistant").write(answer)
