import re

MERMAID_BLOCK_PATTERN = re.compile(
    r"```mermaid\s*(.*?)\s*```",
    re.DOTALL | re.IGNORECASE
)

def extract_mermaid(text: str) -> str | None:
    """
    Extracts the raw Mermaid diagram code from a fenced ```mermaid ... ```
    block and sanitizes syntax-breaking formatting artifacts.
    """
    if not text:
        return None

    match = MERMAID_BLOCK_PATTERN.search(text)
    if not match:
        return None

    raw_code = match.group(1)

    # 1. Replace illegal non-breaking spaces (\xa0) with standard web spaces
    sanitized_code = raw_code.replace("\xa0", " ")

    # 2. Strip trailing semicolons from lines to prevent engine parser hiccups
    lines = [line.rstrip().rstrip(";") for line in sanitized_code.splitlines()]
    
    return "\n".join(lines).strip()

def clean_markdown(text: str) -> str:
    """
    Strips stray code-fence markers and collapses excess blank lines from
    a model response, normalizing hidden spacing issues.
    """
    if not text:
        return ""

    # Clear out non-breaking spaces across the global text chunk
    cleaned = text.replace("\xa0", " ").strip()

    cleaned = re.sub(r"^```[a-zA-Z]*\s*\n", "", cleaned)
    cleaned = re.sub(r"\n```$", "", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()

DANGLING_ARROW_PATTERN = re.compile(r'(-->\s*(?:\|[^|\n]*\|)?)[ \t]*\n[ \t]*')

def normalize_mermaid(code: str) -> str:
    """
    Joins edges where the arrow (and optional |label|) is left dangling
    at the end of a line with its target node on the next line, e.g.
        A["X"] -->
            B["Y"]
    becomes
        A["X"] --> B["Y"]
    Mermaid's flowchart parser treats each line as a statement, so a
    split arrow/target breaks parsing even though it reads fine to a human.
    """
    if not code:
        return code
    return DANGLING_ARROW_PATTERN.sub(r'\1 ', code)