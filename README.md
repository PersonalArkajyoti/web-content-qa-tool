🌐 Web Content Q&A Tool

📝 Overview

The Web Content Q&A Tool allows users to input URLs, ingest webpage content, and ask questions based on the extracted information. The tool utilizes Pinecone for vector storage and Groq API for answering queries based strictly on ingested content.

🚀 Features

Scrapes webpage content from user-provided URLs.

Uses Pinecone for efficient storage and retrieval.

Integrates Groq API to generate accurate answers from webpage content.

Provides an intuitive Streamlit UI for user interaction.

Stores chat history for a seamless conversation flow.

📥 Installation

Follow these steps to set up and run the project locally.

1️⃣ Clone the Repository

git clone https://github.com/your-username/web-content-qa-tool.git
cd web-content-qa-tool

2️⃣ Create and Activate Virtual Environment (Optional but Recommended)

On Windows (Command Prompt)

python -m venv venv
venv\Scripts\activate

On macOS/Linux (Terminal)

python3 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies

Make sure you have Python 3.8+ installed. Then, install the required modules:

pip install -r requirements.txt

🔑 Environment Variables Setup

Create a .env file in the project directory and add your API keys:

PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key

▶️ Running the Application

To launch the Streamlit app, run:

streamlit run app.py

This will open the web interface in your browser.

🛠️ How to Use

Enter webpage URLs in the input field.

Click the Submit button to ingest the webpage content.

Ask a question in the chat interface.

The chatbot will fetch relevant content and generate an answer using Groq API.

📝 Notes

The tool does not answer questions that are out of the provided webpage content.

If the ingested webpage has no meaningful content, it may not return an answer.

Pinecone is used for efficient content retrieval, ensuring accurate responses.

📜 License

This project is licensed under the MIT License.

🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

📞 Contact

For any queries or suggestions, feel free to reach out:

GitHub: your-username

Email: your-email@example.com

