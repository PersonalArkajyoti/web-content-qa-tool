# 🌐 Web Content Q&A Chatbot

  A simple web-based Q&A chatbot that allows users to input URLs, extract webpage content, and ask questions based on the ingested content. The chatbot retrieves relevant information using Pinecone and generates responses using the Groq API.

## 🚀 Features

  - Ingests webpage content from given URLs.
  - Stores extracted text embeddings in **Pinecone**.
  - Uses **Groq API** to generate answers based on relevant content.
  - Provides a clean and interactive **Streamlit** UI.
  - Stores chat history for better context.

## 🛠️ Installation

### 1️⃣ Clone the Repository

    git clone https://github.com/yourusername/web-content-qa-chatbot.git
    cd web-content-qa-chatbot

### 2️⃣ Create a Virtual Environment (Optional but Recommended)

    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate      # On Windows

### 3️⃣ Install Dependencies

    pip install -r requirements.txt

### 4️⃣ Set Up Environment Variables
  Create a .env file in the project root and add the following:
    PINECONE_API_KEY="your_pinecone_api_key"
    GROQ_API_KEY="your_groq_api_key"
  Replace your_pinecone_api_key and your_groq_api_key with actual API keys.


## ▶️ Running the Application
To start the Streamlit app, run:
  streamlit run app.py

## 🏗️ How It Works
  - The user inputs webpage URLs.
  - The tool extracts text content from the webpages.
  - Extracted text is stored as embeddings in Pinecone.
  - The user asks a question related to the ingested content.
  - The chatbot retrieves relevant text and generates an answer using Groq API.
  
## 📌 Example Usage
  1. Run the app using streamlit run app.py.
  2. Enter webpage URLs and submit.
  3. Ask questions related to the webpage content.
  4. Get AI-generated answers based on the extracted text.


## 🤖 Technologies Used
  - Python
  - Streamlit (UI)
  - BeautifulSoup (Web Scraping)
  - Pinecone (Vector Database)
  - Groq API (AI Model for Answering)



## 📜 License
  This project is licensed under the MIT License.

## 💡 Contributing
  Pull requests are welcome! If you have suggestions for improvements, feel free to submit an issue or open a PR.

## 📬 Contact
  For questions or feedback, reach out via
    Email: arkajyotichakraborty99@gmail.com
