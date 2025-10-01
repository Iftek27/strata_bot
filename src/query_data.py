import argparse
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.prompts import PromptTemplate
from rewriter import rewrite_query

DB_DIR = "db/chroma_db"

# Prompt for QA
PROMPT_TEMPLATE = """
You are an assistant that provides *general guidance* on the Unit Titles (Management) Act 2011 (ACT).
You must ONLY use the text provided in the Context below.

⚠️ RULES:
- If the law is in a Schedule, cite it as “Schedule X, clause Y”.
- If the law is in the main Act, cite it as “Section X”.
- Do NOT invent or guess section numbers.
- Do NOT say "The Act does not provide a clear answer" if a relevant section/clause is in Context.
- If the Act is silent, point to the rules of the owners corporation (s 107–108).
- Always include the most precise clause/section available.
- Clarify enforcement: owners corporations issue infringement notices, but penalties/fines require ACAT.
- Write in clear, professional plain English, aiming for 120–180 words.

📑 Format your answer as 2–3 flowing paragraphs without headings:
- Paragraph 1 – plain English explanation of the answer.  
- Paragraph 2 – cite the Act with exact section or schedule/clause and explain why it applies.  
- Paragraph 3 (optional) – add clarifications/limits if needed.  
Always end with:  
⚠ This is general guidance only and should not be treated as legal advice.

Context:
{context}

Question:
{question}

Answer:
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, nargs="?", default="Who fixes balcony leaks?",
                        help="Your legal question (default: 'Who fixes balcony leaks?')")
    args = parser.parse_args()

    # Rewrite query into legal style
    rewritten = rewrite_query(args.query)
    print("🔎 Original:", args.query)
    print("📝 Rewritten:", rewritten)

    # Load DB
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 6})

    # Prompt
    qa_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE,
    )

    # LLM
    llm = ChatOllama(model="llama3", temperature=0.1, num_ctx=4096)

    # Retrieve documents
    results = retriever.get_relevant_documents(rewritten)
    context = "\n\n".join([doc.page_content for doc in results])

    # Build final prompt
    final_prompt = qa_prompt.format(context=context, question=rewritten)
    answer = llm.predict(final_prompt)

    # Print results
    print("\n💡 Answer:\n")
    print(answer.strip())

    print("\n📚 Sources:")
    for doc in results:
        act = doc.metadata.get("source_file", "Unknown")
        section = doc.metadata.get("section", "Unknown")
        preview = doc.page_content[:200].replace("\n", " ")
        print(f"- {act} | {section}: {preview}...")


if __name__ == "__main__":
    main()
