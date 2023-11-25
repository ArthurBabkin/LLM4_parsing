import requests
from bs4 import BeautifulSoup
import json
import os

offset = 0
limit = 500


def get_pdf(url, title):
    html = requests.get(url)
    pdf = open(f'C:/Users/{os.getlogin()}/Desktop/LLM4/{title}.pdf', 'wb')
    pdf.write(html.content)

def forward_snowballing():
    api_url = 'https://api.semanticscholar.org/graph/v1/paper/204e3073870fae3d05bcbc2f6a8e263d9b72e776/citations?fields=title,citationCount,externalIds&offset=0&limit=500'
    api_text = requests.get(api_url).json() #получили dict из API'шника(JSON-строка)
    #data = json.loads(api_text)
    # Извлеките нужные данные
    for item in api_text["data"]:
        external_ids = item["citingPaper"]["externalIds"]
        paper_id = external_ids.get("ArXiv", "N/A")  # Если "ArXiv" отсутствует, возвращает "N/A"
        citation_count = item["citingPaper"]["citationCount"]
        print(f"Paper ID: {paper_id}, Citation Count: {citation_count}")

forward_snowballing()