# Placeholder for app/main.py
import os
import streamlit as st
from dotenv import load_dotenv
from app.crew_flow import Flow, meta_optimize
from app.ingest import Ingestor
from app.rag import RAG
from app.utils import list_files

load_dotenv(override=True)

st.set_page_config(
    page_title=os.getenv("APP_TITLE", "ARC RAG Demo"), layout="wide"
)

#st.title(os.getenv("APP_TITLE", "ARC RAG Demo"))
st.title("ARC RAG - Ask questions about Autism Resource Guide")

# 👇 Add a description right below the title
st.caption(
    "This chatbot uses Retrieval-Augmented Generation (RAG) over the Autism Resource "
    "Guide 2025. You can ask natural language questions, and it will retrieve relevant "
    "sections from the guide and generate answers with proper citations."
)

DATA_DIR = os.getenv("DATA_DIR", "./data")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./storage")

# Sidebar
with st.sidebar:
    st.header("Setup")
    llm_mode = os.getenv("LLM_MODE") #, "local")
    st.caption(f"LLM mode: **{llm_mode}**")

    # if st.button("Ingest / Refresh Index"):
    #     ing = Ingestor(DATA_DIR, CHROMA_DIR)
    #     files = list(list_files(DATA_DIR))
    #     with st.status("Embedding & indexing..."):
    #         result = ing.upsert_files(files)
    #     st.success(result)

    # base_url = st.text_input(
    #     "ARC base URL (optional crawler)", placeholder="https://example.org/"
    # )
    # if st.button("Crawl & Save") and base_url:
    #     from app.crawler import SimpleCrawler

    #     cr = SimpleCrawler(base_url, DATA_DIR)
    #     with st.status("Crawling website..."):
    #         saved = cr.crawl()
    #     st.success({"saved": len(saved)})

# Main QA
# Input field with a form to catch Enter key
with st.form("chat_form", clear_on_submit=True):
    question = st.text_input(
        "Your question",
        placeholder="What services are offered for adult autism support?"
    )
    submitted = st.form_submit_button("Answer")

if submitted and question:
    rag = RAG(DATA_DIR, CHROMA_DIR)
    with st.spinner("Retrieving..."):
        resp = rag.answer(question)

    st.markdown("### Answer")
    st.write(resp.get("answer", "(no answer)"))

    if resp.get("citations"):
        st.markdown("**Citations**")
        for c in resp["citations"]:
            st.code(c)
st.divider()
# st.subheader("Meta Prompt Optimizer (demo)")
# raw_task = st.text_area(
#     "Task description", "Download ARC docs and save to data folder"
# )
# if st.button("Optimize Task Prompt") and raw_task:
#     mp = meta_optimize(raw_task)
#     st.json(mp)
