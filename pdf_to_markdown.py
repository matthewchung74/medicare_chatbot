import pymupdf4llm
import pathlib
from datetime import datetime

def convert_pdf_to_markdown(input_pdf, output_md):
    # Get the markdown text
    print(f"Converting {input_pdf} to markdown...")
    md_text = pymupdf4llm.to_markdown(input_pdf)
    
    # Add a header with metadata
    header = f"""# Medicare and You Documentation
> Converted from PDF on {datetime.now().strftime('%Y-%m-%d')}
> Source: {input_pdf}

---

"""
    
    # Combine header and content
    final_content = header + md_text
    
    # Write to file
    print(f"Writing markdown to {output_md}...")
    pathlib.Path(output_md).write_bytes(final_content.encode())
    print("Conversion complete!")

if __name__ == "__main__":
    input_pdf = "10050-medicare-and-you.pdf"
    output_md = "medicare_and_you.md"
    convert_pdf_to_markdown(input_pdf, output_md)
