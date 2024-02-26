import PyPDF2
import re
import json
def pdf_to_text(pdf_path, text_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        with open(text_path, 'w', encoding='utf-8') as text_file:
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_file.write(page.extract_text())



def extract_sections(text):
    sections = {}
    pattern = r'^(\d+(\.\d+)?)\s+(.+?)(?=\n\d+(\.\d+)?\s+|\Z)'
    matches = re.findall(pattern, text, re.DOTALL|re.MULTILINE)
    for match in matches:
        section_title = match[2].strip()
        section_content = match[0] + ' ' + section_title
        sections[section_content] = section_title
    return sections



    
if __name__ == "__main__":
    # pdf_to_text('dummy.pdf', 'dummy.txt')

    with open('dummy.txt', 'r') as file:
        paper_text = file.read()

    paper_sections = extract_sections(paper_text)
    with open('parsed.json', 'w') as f:
        json.dump(paper_sections, f, indent=4)
    # for section_title, section_content in paper_sections.items():
    #     print(f"{section_title}: {section_content}\n")
    #     break


