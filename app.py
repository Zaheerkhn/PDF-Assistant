import os
import streamlit as st
from dotenv import load_dotenv
from phi.agent import Agent
from phi.storage.agent.postgres import PgAgentStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.model.groq import Groq
from phi.embedder.google import GeminiEmbedder

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Database URL
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Initialize Streamlit app
st.title("📄 PDF AI Assistant")
st.write("Enter a PDF link and ask questions about its content.")

# User inputs PDF URL
pdf_url = st.text_input("Enter the PDF URL:", "")

# Check if user provided a PDF URL
if pdf_url:
    with st.spinner("Loading PDF..."):
        try:
            # Load knowledge base dynamically
            knowledge_base = PDFUrlKnowledgeBase(
                urls=[pdf_url],
                vector_db=PgVector2(
                    collection="user_uploaded_pdfs",
                    db_url=db_url,
                    embedder=GeminiEmbedder(model="models/embedding-001"),
                ),
            )
            knowledge_base.load()
            st.success("PDF Loaded Successfully! You can now ask questions.")

            # Postgres storage for chat history
            storage = PgAgentStorage(
                table_name="agent_sessions",
                db_url=db_url,
            )

            # Initialize session state for run_id
            if "run_id" not in st.session_state:
                st.session_state.run_id = None

            # User query
            user_query = st.chat_input("Enter your query:")

            if user_query:
                with st.spinner("Thinking..."):
                    assistant = Agent(
                        model=Groq(id="llama-3.3-70b-versatile", embedder=GeminiEmbedder(model="models/embedding-001")),
                        run_id=st.session_state.run_id,
                        user_id="user",
                        knowledge_base=knowledge_base,
                        storage=storage,
                        show_tool_calls=True,
                        search_knowledge=True,
                        read_chat_history=True,
                    )

                    # Run assistant with user query
                    response = assistant.run(user_query)

                    # Store run_id for session continuity
                    if st.session_state.run_id is None:
                        st.session_state.run_id = assistant.run_id

                    # Display response
                    clean_response = response.content if hasattr(response, "content") else str(response)
                
                st.markdown(clean_response)

        except Exception as e:
            st.error(f"Error loading PDF: {e}")

# import os
# from dotenv import load_dotenv
# import typer
# from typing import Optional, List
# from phi.agent import Agent
# from phi.storage.agent.postgres import PgAgentStorage
# from phi.knowledge.pdf import PDFUrlKnowledgeBase
# from phi.vectordb.pgvector import PgVector2

# from phi.model.groq import Groq
# from phi.embedder.google import GeminiEmbedder 

# # Load environment variables
# load_dotenv()
# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# knowledge_base = PDFUrlKnowledgeBase(
#     urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
#     vector_db=PgVector2(collection="recipes", db_url=db_url,embedder=GeminiEmbedder(model="models/embedding-001")),
# )
# knowledge_base.load()

# # Create a storage backend using the Postgres database
# storage = PgAgentStorage(
#     # store sessions in the ai.sessions table
#     table_name="agent_sessions",
#     # db_url: Postgres database URL
#     db_url=db_url,
# )


# def pdf_assistant(new: bool = False, user: str = "user"):
#     run_id: Optional[str] = None

#     assistant = Agent(
#         model=Groq(id="llama-3.3-70b-versatile",embedder=GeminiEmbedder(model="models/embedding-001")),
#         run_id=run_id,
#         user_id=user,
#         knowledge_base=knowledge_base,
#         storage=storage,
#         # Show tool calls in the response
#         show_tool_calls=True,
#         # Enable the assistant to search the knowledge base
#         search_knowledge=True,
#         # Enable the assistant to read the chat history
#         read_chat_history=True,
#     )
#     if run_id is None:
#         run_id = assistant.run_id
#         print(f"Started Run: {run_id}\n")
#     else:
#         print(f"Continuing Run: {run_id}\n")

#     assistant.cli_app(markdown=True)

# if __name__=="__main__":
#     typer.run(pdf_assistant)
