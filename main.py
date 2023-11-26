import requests
from bs4 import BeautifulSoup
import json
import os

offset = 0
limit = 500

articles_arXiv_ID = set()
articles_paper_ID = set()
articles_titles = set()
articles = []


def get_pdf(url: str, counter) -> None:
    html = requests.get(url)
    pdf = open(f'C:/Users/{os.getlogin()}/Desktop/LLM4/DataScience/Articles/{counter}.pdf', 'wb')
    pdf.write(html.content)

def forward_snowballing_first_wave(counter_forward:int, api_url:str, api_text: dict, offset: int, limit:int) -> None:
    if offset + limit < 5000:
        #print(offset + limit)
        if (counter_forward == 0):
            api_url = 'https://api.semanticscholar.org/graph/v1/paper/204e3073870fae3d05bcbc2f6a8e263d9b72e776/citations?fields=title,citationCount,externalIds&offset=0&limit=500'
            api_text = requests.get(api_url).json() #получили dict из API'шника(JSON-строка)
        # Извлеките нужные данные
        for item in api_text["data"]:
            counter_forward += 1
            citing_paper = item.get("citingPaper")
            if citing_paper:
                external_ids = citing_paper.get("externalIds")
                if external_ids:
                    arthive_id = external_ids.get("ArXiv", "N/A")
                    paper_id = citing_paper.get("paperId", "N/A")
                    citation_count = citing_paper.get("citationCount", 0)
                    title = citing_paper.get("title", "N/A")

            if citation_count > 10  and arthive_id != "N/A":
                articles_arXiv_ID.add(arthive_id)
                articles_titles.add(title)
                articles_paper_ID.add(paper_id)
                print(f"arXiv ID: {arthive_id}, Citation Count: {citation_count}")
                print(counter_forward)
                print(title)
            if (counter_forward % 500 == 0 and counter_forward != 0):
                if offset + limit < 9500:
                    if offset + 499 + limit < 10000:
                        offset += 499
                    else:
                        offset += 500
                    api_url = "https://api.semanticscholar.org/graph/v1/paper/204e3073870fae3d05bcbc2f6a8e263d9b72e776/citations?fields=title,citationCount,externalIds&offset=" + str(offset) + "&limit=500"
                    api_text = requests.get(api_url).json()
                    forward_snowballing_first_wave(counter_forward, api_url, api_text, offset, limit)
                else:
                    return



# Title, ArXiv, citationCount
def backwards_snowballing():
    url = ('https://api.semanticscholar.org/graph/v1/paper/204e3073870fae3d05bcbc2f6a8e263d9b72e776/references?fields'
           '=title,citationCount,externalIds')
    response = requests.get(url).json()

    # getting articles from api
    for item in response["data"]:
        external_ids = item["citedPaper"]["externalIds"]
        paper_id = "N/A"
        if external_ids:
            paper_id = external_ids.get("ArXiv", "N/A")

        citation_count = item["citedPaper"]["citationCount"]
        title = item["citedPaper"]["title"]
        if citation_count and citation_count >= 10:
            articles.append([title, paper_id, citation_count])



backwards_snowballing()


forward_snowballing_first_wave(0, "", None, 0, limit)

list_articles_titles = list(articles_titles)
list_articles_arXiv_ID = list(articles_arXiv_ID)

print(list_articles_titles[0])
for i in range(len(articles_arXiv_ID)):
    get_pdf("https://arxiv.org//pdf/" + str(list_articles_arXiv_ID[i]) + ".pdf", str(i))