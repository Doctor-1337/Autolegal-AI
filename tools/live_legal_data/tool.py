from langchain.tools import Tool
from datasets import load_dataset

# Load dataset once (you can cache this)
dataset = load_dataset("lex_glue", "ecthr_a", split="train[:500]")  # use a smaller subset for performance

def legal_dataset_search(query: str) -> str:
    from datasets import load_dataset

    dataset = load_dataset("lex_glue", "ecthr_a")
    results = []

    for item in dataset["train"]:
        text = item["text"]

        if isinstance(text, list):
            text = " ".join(text)
        if query.lower() in text.lower():
            results.append(text)

        if len(results) >= 3:
            break

    if results:
        return "\n\n---\n\n".join(results)
    return "No relevant legal data found."


LegalDatasetTool = Tool(
    name="LegalDatasetTool",
    func=legal_dataset_search,
    description="Useful for searching legal case data from the ECHR LexGLUE dataset using a natural language query."
)
