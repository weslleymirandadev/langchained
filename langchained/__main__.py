"""Command line app: ingest files, then ask questions about them."""

import argparse
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from .index import build_index, load_index
from .search import search

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Answer the question using only the context below. Be brief."),
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])


def get_llm():
    if os.environ.get("OPENAI_API_KEY"):
        from langchain.chat_models import init_chat_model
        return init_chat_model("openai:gpt-4o-mini")
    return None


def answer_offline(question, chunks):
    best = max(chunks, key=lambda c: len(c["text"]))
    return "(offline mode: no LLM used)\n\n" + best["text"]


def ask(question, k=3):
    chunks = load_index()
    found = search(chunks, question, k)
    if not found:
        print("No matching text found.")
        return

    context = "\n\n".join(chunk["text"] for chunk in found)
    llm = get_llm()
    if llm is None:
        answer = answer_offline(question, found)
    else:
        chain = PROMPT | llm | StrOutputParser()
        answer = chain.invoke({"context": context, "question": question})

    print(answer)
    print("\nSources:")
    for name in sorted({chunk["source"] for chunk in found}):
        print(f"  - {name}")


def main():
    parser = argparse.ArgumentParser(prog="langchained")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="index a file or folder")
    ingest.add_argument("path")

    ask_cmd = sub.add_parser("ask", help="ask a question")
    ask_cmd.add_argument("question")
    ask_cmd.add_argument("-k", type=int, default=3, help="how many chunks to use")

    args = parser.parse_args()

    if args.command == "ingest":
        chunks = build_index(args.path)
        print(f"Indexed {len(chunks)} chunks from {args.path}")
        for name in sorted({chunk["source"] for chunk in chunks}):
            print(f"  - {name}")
    else:
        ask(args.question, args.k)


if __name__ == "__main__":
    main()
