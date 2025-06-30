from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def get_text_qa_chain(llm):
    """
    Creates an LLMChain for question-answering based on input context.

    Args:
        llm: A language model instance (e.g., ChatGroq, HuggingFaceHub).

    Returns:
        LLMChain: Configured chain to answer questions from provided context.
    """
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful and concise assistant. Answer the following question based only on the provided context.

If the answer is not present in the context, say: "I couldn't find the answer in the given context."

--- Context ---
{context}

--- Question ---
{question}

--- Answer ---
"""
    )

    return LLMChain(prompt=prompt, llm=llm)
