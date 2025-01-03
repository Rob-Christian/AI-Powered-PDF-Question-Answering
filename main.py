# Import necessary libraries
import streamlit as st
import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI, VectorDBQA
from langchain.chains import RetrievalQAWithSourcesChain
import PyPDF2
import os

# Set API key
os.environ["OPENAI_API_KEY"] = st.secrets["key"]

# Function to extract text and sources from PDFs
def pdf_to_text(files):
    text_list = []
    source_list = []
    for file in files:
        pdf_reader = PyPDF2.PdfReader(file)
        for i in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[i]
            text = page.extract_text()
            page.clear()
            text_list.append(text)
            source_list.append(file.name + "_page_" + str(i))
    return [text_list, source_list]

# Streamlit page configuration
st.set_page_config(layout='centered', page_title="Retrieval-based Question Answering")
st.header("PDF Reviewer with Question Answering")
st.write("---")

# Initialize session state variables
if "mode" not in st.session_state:
    st.session_state["mode"] = None  # To track the selected mode (ask/generate)
if "model" not in st.session_state:
    st.session_state["model"] = None  # To store the QA model
if "texts" not in st.session_state:
    st.session_state["texts"] = []
if "sources" not in st.session_state:
    st.session_state["sources"] = []
if "questions" not in st.session_state:
    st.session_state["questions"] = []
if "answers" not in st.session_state:
    st.session_state["answers"] = []
if "reveal_states" not in st.session_state:
    st.session_state["reveal_states"] = []

# File uploader
upload_files = st.file_uploader(
    "Upload up to 3 PDF Documents", accept_multiple_files=True, type=['pdf']
)

# File upload status
if upload_files:
    if len(upload_files) > 3:
        st.warning("You can only upload up to 3 PDF Documents")
        upload_files = upload_files[:3]
    else:
        st.success(f"{len(upload_files)} document(s) ready for processing")

# Process files button
if st.button("Process Files"):
    if not upload_files:
        st.info("Please upload PDF Documents")
    else:
        with st.spinner("Processing Files..."):
            try:
                # Extract text and sources
                text_and_source = pdf_to_text(upload_files)
                text = text_and_source[0]
                source = text_and_source[1]

                st.session_state["texts"] = text
                st.session_state["sources"] = source

                # Extract embeddings
                embeddings = OpenAIEmbeddings()

                # Vector store with metadata
                vectordb = Chroma.from_texts(
                    text, embeddings, metadatas=[{"source": s} for s in source]
                )

                # Retrieval model
                llm = OpenAI(
                    model_name="gpt-3.5-turbo",
                    streaming=True,
                )
                retriever = vectordb.as_retriever(search_kwargs={"k": 2})
                model = RetrievalQAWithSourcesChain.from_chain_type(
                    llm=llm, chain_type="stuff", retriever=retriever
                )

                # Store the model in session state
                st.session_state["model"] = model
                st.success("Files processed successfully! You can now ask questions.")
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")

# Render options if the model exists
if st.session_state["model"]:
    st.header("What do you prefer to do?")
    col1, col2 = st.columns(2)

    # Buttons for selecting mode
    with col1:
        if st.button("Ask a Question"):
            st.session_state["mode"] = "ask"
    with col2:
        if st.button("Generate Questions"):
            st.session_state["mode"] = "generate"

    # Mode: Ask a Question
    if st.session_state["mode"] == "ask":
        st.subheader("Ask a Question")
        query = st.text_area("Enter your question here", key="query")

        if st.button("Get Answer"):
            try:
                with st.spinner("Model is working on it..."):
                    result = st.session_state["model"](
                        {"question": query}, return_only_outputs=True
                    )
                    st.subheader("Answer:")
                    st.write(result["answer"])
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Mode: Generate Questions
    elif st.session_state["mode"] == "generate":
        st.subheader("Generate Questions")
        num_questions = st.slider("How many questions do you want to generate?", 1, 5, 3)

        if st.button("Generate"):
            try:
                with st.spinner("Generating Questions..."):
                    all_texts = "".join(st.session_state.get("texts", []))

                    # Define prompt
                    prompt = f"Generate {num_questions} meaningful questions from the following texts: {all_texts}"

                    # Generate questions using the model
                    llm = OpenAI(model_name = "gpt-3.5-turbo", streaming = False)
                    response = llm(prompt)
                    questions = response.strip().split("\n")

                    # Prepare answers from the question
                    answers = []
                    for question in questions:
                        answer_prompt = llm(f"Provide a concise answer to the following question: {question}")
                        answers.append(answer_prompt)

                    st.session_state["questions"] = questions
                    st.session_state["answers"] = answers
                    st.session_state["reveal_states"] = [False]*len(questions)
           
            except Exception as e:
                st.error(f"An error occurred when generating questions: {e}")

        if st.session_state["questions"]:
            st.subheader("Generated Questions:")
            for i, question in enumerate(st.session_state["questions"]):
                st.write(f"{question}")
                if st.button(f"Reveal Answer {i + 1}", key=f"reveal_{i}"):
                    st.session_state["reveal_states"][i] = True
                if st.session_state["reveal_states"][i]:
                    st.write(f"Answer: {st.session_state['answers'][i]}")
                    
else:
    st.info("Please upload and process your PDF files first.")
