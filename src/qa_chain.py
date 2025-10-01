from langchain.chains import RetrievalQA
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate

from retriever import get_retriever
from rewriter import rewrite_query


# Strict legal prompt
prompt_template = """
You are an assistant that provides *general guidance* on the Unit Titles (Management) Act 2011 (ACT).
You must ONLY use the text provided in the Context below. Never invent section or clause numbers.

⚖️ RULES:
- If the law text explicitly says "Schedule X" or "Section X", you may cite it exactly as written.  
- If no section/schedule is explicitly visible in the context, explain without citing numbers.  
- Do NOT invent or guess section/clause numbers.  
- Use only the most precise citation available in the context/metadata.  
- If the Act is silent, say: "The Act does not provide a clear answer to this. Please seek advice from the owners corporation or a qualified legal professional."  
- Write in clear, professional plain English, aiming for 120–180 words.  

📄 Format your answer as flowing paragraphs (no headings):
- Paragraph 1: Plain English explanation of the answer.  
- Paragraph 2 must always cite the Act with the exact section or schedule/clause number from the context. 
- Paragraph 3 (optional): Add clarifications, context, or limits.  

Always end with:
⚠ This is general guidance only and should not be treated as legal advice.

Context:
{context}

Question:
{question}

Answer:
"""



def get_qa_chain():
    retriever = get_retriever()
    llm = ChatOllama(model="llama3", temperature=0.1, num_ctx=4096)

    qa_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": qa_prompt},
        return_source_documents=True,
    )
    return qa

if __name__ == "__main__":
    qa = get_qa_chain()

    query = "Who fixes balcony leaks?"
    rewritten = rewrite_query(query)

    print("🔎 Original:", query)
    print("📝 Rewritten:", rewritten)

    result = qa.invoke({"query": rewritten})

    print("\n💡 Answer:\n")
    print(result["result"])

    print("\n📚 Sources:")
    for doc in result["source_documents"]:
        act = doc.metadata.get("source_file", "Unknown")
        section = doc.metadata.get("section", "Unknown")
        preview = doc.page_content[:200].replace("\n", " ")
        print(f"- {act} | {section}: {preview}...")
