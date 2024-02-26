import requests
from bs4 import BeautifulSoup

def scrape_references_summary(arxiv_id):
    url = f"https://arxiv.org/abs/1311.5636v1"
    response = requests.get(url)

    print(response.text)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        references_div = soup.find('div', {'class': 'bibtex-abstract'})
        if references_div:
            references_summary = references_div.text.strip()
            return references_summary
        else:
            return "References summary not found."
    else:
        return "Failed to fetch the arXiv paper."

if __name__ == "__main__":
    arxiv_id = input("Enter the arXiv ID (e.g., '2001.00001'): ")
    summary = scrape_references_summary(arxiv_id)
    print(summary)
