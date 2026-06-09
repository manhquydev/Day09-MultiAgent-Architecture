from __future__ import annotations


def parse_policy_markdown(markdown_text: str) -> list[dict]:
    lines = markdown_text.splitlines()
    chunks = []
    
    current_h2 = None
    current_h3 = None
    current_content_lines = []
    
    def save_chunk():
        nonlocal current_h2, current_h3, current_content_lines
        if current_h2 and current_content_lines:
            content = "\n".join(current_content_lines).strip()
            if content:
                if current_h3:
                    rendered_text = f"## {current_h2}\n### {current_h3}\n{content}"
                    citation = f"{current_h2} > {current_h3}"
                else:
                    rendered_text = f"## {current_h2}\n{content}"
                    citation = f"{current_h2}"
                chunks.append({
                    "section_h2": current_h2,
                    "section_h3": current_h3 or "",
                    "citation": citation,
                    "rendered_text": rendered_text
                })
            current_content_lines = []

    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith("## "):
            save_chunk()
            current_h2 = line_stripped[3:].strip()
            current_h3 = None
        elif line_stripped.startswith("### "):
            save_chunk()
            current_h3 = line_stripped[4:].strip()
        else:
            if current_h2:
                current_content_lines.append(line)
                
    save_chunk()
    return chunks

