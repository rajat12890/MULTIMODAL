import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import os

# from chains.image_caption import generate_image_caption
from chains.text_qa import get_text_qa_chain
from utils.extract_pdf_text import extract_text_from_pdf
from utils.extract_image_text import extract_text_from_image
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
def build_context_from_history(history, limit=6):
    ctx = ""
    for entry in history[-limit:]:
        if entry["role"] == "user":
            ctx += f"User: {entry['question']}\n"
        elif entry["role"] == "assistant":
            ctx += f"Bot: {entry['answer']}\n"
    return ctx

# Initialize LLM
llm = ChatGroq(groq_api_key=groq_key, model_name="Llama3-70b-8192")
if "history" not in st.session_state:
    st.session_state.history=[]
# Streamlit UI Config
st.set_page_config(page_title="🤖 Multimodal Chatbot", layout="wide")
st.title("🤖 Multimodal Chatbot (Text + Image + Document)")

# Input selector
input_type = st.radio("📌 Select Input Type", ["Text", "Image", "PDF"])

# ===== TEXT MODE =====
if input_type == "Text":
    query = st.text_area("💬 Ask your question")
    if st.button("Answer"):
        chain = get_text_qa_chain(llm)
        context = build_context_from_history(st.session_state.history)
        response = chain.run(context=context, question=query)
        st.session_state.history.append({"role":"user","question":query,"input_type":"Text"})
        st.session_state.history.append({"role":"assistant","answer":response})  
        st.subheader("📤 Response:")
        st.write(response)      

# ===== IMAGE MODE =====
elif input_type == "Image":
    img_file = st.file_uploader("📸 Upload an Image", type=["png", "jpg", "jpeg"])
    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="🖼️ Uploaded Image", use_column_width=True)

        # Extract: Caption + OCR
        with st.spinner("🧠 Extracting image understanding..."):
            # caption = generate_image_caption(image)
            caption=""
            ocr_text = extract_text_from_image(image)

        st.success(f"📝 Caption: {caption}")
        st.info(f"🧾 OCR Text: {ocr_text}")

        # Q&A on image
        question = st.text_input("💬 Ask a question about the image")
        if st.button("Ask Image Question"):
            chain = get_text_qa_chain(llm)
          
            context = f"{caption}\n{ocr_text}\n" + build_context_from_history(st.session_state.history)
            response=chain.run(context=context,question=question)
            st.session_state.history.append({"role": "user", "question": question, "input_type": "Image"})
            st.session_state.history.append({"role": "assistant", "answer": response})
            st.subheader("📤 Response:")
            st.write(response)

# ===== PDF MODE =====
elif input_type == "PDF":
    pdf_file = st.file_uploader("📄 Upload a PDF", type=["pdf"])

    # Load and store text only once
    if pdf_file and "pdf_text" not in st.session_state:
        with st.spinner("🔍 Extracting PDF text..."):
            st.session_state["pdf_text"] = extract_text_from_pdf(pdf_file)

    if "pdf_text" in st.session_state:
        question = st.text_input("💬 Ask a question about the document")

        if st.button("Ask PDF Question"):
            chain = get_text_qa_chain(llm)

            context = build_context_from_history(st.session_state.history)
            # PDF text acts as persistent base context, not repeated
            full_context = st.session_state["pdf_text"] + "\n" + context

            response = chain.run(context=full_context, question=question)

            st.session_state.history.append({"role": "user", "question": question, "input_type": "PDF"})
            st.session_state.history.append({"role": "assistant", "answer": response})

            st.subheader("📤 Response:")
            st.write(response)

st.markdown("---")
st.subheader("🕓 Chat History")

for entry in st.session_state.history:
    if entry["role"] == "user":
        st.markdown(f"🧑‍💻 **You** ({entry.get('input_type', '')}): {entry['question']}")
    elif entry["role"] == "assistant":
        st.markdown(f"🤖 **Bot**: {entry['answer']}")

if st.button("🗑️ Clear Chat History"):
    st.session_state.history = []
    st.success("Chat history cleared.")
