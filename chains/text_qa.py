from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq  # or use HuggingFaceHub

def get_text_qa_chain(llm):
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful assistant. Based on the following context, answer the question.

Context:
{context}

Question:
{question}
"""
    )
    return LLMChain(prompt=prompt, llm=llm)
