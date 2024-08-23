# langchained

Ask questions about a folder of local text files.
It splits your files into small chunks, finds the chunks that match your question,
and sends them to a chat model to get an answer.
It works offline with no API key.

## What it does

- Reads all `.md` and `.txt` files in a folder and saves them as a simple JSON index.
- Scores chunks by counting how many of your query words appear in them.
- Sends the best chunks to a chat model and prints which source files were used.

## Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python -m langchained ingest samples
python -m langchained ask "how do I rotate the database credentials?"
```

Add `-k 5` to `ask` to use more chunks.

Without an `OPENAI_API_KEY`, the app prints the best matching chunk instead of calling
a model. Set the key to use `gpt-4o-mini` through `init_chat_model`.

Example output:

```text
$ python -m langchained ingest samples
Indexed 18 chunks from samples
  - database-rotation-runbook.md
  - incident-postmortem.md
  - oncall-escalation.md
  - product-faq.md

$ python -m langchained ask "when should I escalate to secondary on-call?"
(offline mode: no LLM used)
...

Sources:
  - oncall-escalation.md
```

## How it works

1. `ingest` reads each file and cuts it into overlapping chunks of about 500 characters.
   The chunks are saved to `.langchained/index.json`.
2. `ask` loads the chunks, splits your question into words, and counts how many of those
   words appear in each chunk. Chunks whose file name also matches get a small bonus.
3. The top `k` chunks are pasted into a `ChatPromptTemplate` and sent to the model
   with `prompt | llm | StrOutputParser`.
4. Finally the app prints the answer and the names of the files that were used.

## Tests

```bash
python -m pytest tests -q
```

## License

MIT
