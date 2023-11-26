import requests
import json
import os

offset = 0
limit = 500

articles_arxiv_id = set()
articles_paper_id = set()


def get_pdf(url: str, counter) -> None:
    html = requests.get(url)
    pdf = open(f'C:/Users/{os.getlogin()}/Desktop/LLM4/DataScience/Articles/{counter}.pdf', 'wb')
    pdf.write(html.content)


def forward_snowballing_first_wave(counter_forward: int, api_url: str, api_text: dict, offset: int, limit: int) -> None:
    if offset + limit >= 10000:
        return
    if (counter_forward == 0):
        api_url = 'https://api.semanticscholar.org/graph/v1/paper/204e3073870fae3d05bcbc2f6a8e263d9b72e776/citations?fields=title,citationCount,externalIds&offset=0&limit=500'
        api_text = requests.get(api_url).json()  # получили dict из API'шника(JSON-строка)
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

        if citation_count > 10 and arthive_id != "N/A":
            articles_arxiv_id.add(arthive_id)
            articles_paper_id.add(paper_id)
            print(f"arXiv ID: {arthive_id}, Citation Count: {citation_count}")
            print(f"paper ID: {paper_id}")
            print(counter_forward)
        if (counter_forward % 500 == 0 and counter_forward != 0):
            if offset + limit < 9500:
                if offset + 499 + limit < 10000:
                    offset += 499
                else:
                    offset += 500
                api_url = "https://api.semanticscholar.org/graph/v1/paper/204e3073870fae3d05bcbc2f6a8e263d9b72e776/citations?fields=title,citationCount,externalIds&offset=" + str(
                    offset) + "&limit=500"
                api_text = requests.get(api_url).json()
                forward_snowballing_first_wave(counter_forward, api_url, api_text, offset, limit)
            else:
                return


def forward_snowballing_second_wave(counter_forward: int, api_url: str, api_text: dict, offset: int,
                                    limit: int) -> None:
    if offset + limit >= 10000:
        return
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

        if citation_count > 10 and arthive_id != "N/A":
            articles_arxiv_id.add(arthive_id)
            articles_paper_id.add(paper_id)
            print(f"arXiv ID: {arthive_id}, Citation Count: {citation_count}")
            print(f"paper ID: {paper_id}")
            print(counter_forward)
        if (counter_forward % 500 == 0 and counter_forward != 0):
            if offset + limit < 9500:
                if offset + 499 + limit < 10000:
                    offset += 499
                else:
                    offset += 500
                # Получаем часть строки до параметра offset
                url_before_offset = api_url[:api_url.find("&offset=") + 8]
                # Получаем часть строки после параметра offset
                url_after_offset = api_url[api_url.find("&offset=") + 9:]
                api_url = url_before_offset + str(offset) + url_after_offset
                api_text = requests.get(api_url).json()
                forward_snowballing_first_wave(counter_forward, api_url, api_text, offset, limit)
            else:
                return


def backward_snowballing_first_wave(counter_forward: int, api_url: str, api_text: dict, offset: int, limit: int):
    if offset + limit >= 10000:
        return
    if counter_forward == 0:
        api_url = 'https://api.semanticscholar.org/graph/v1/paper/204e3073870fae3d05bcbc2f6a8e263d9b72e776/references?fields=title,citationCount,externalIds&offset=0&limit=500'
        api_text = requests.get(api_url).json()  # получили dict из API'шника(JSON-строка)
    # Извлеките нужные данные
    for item in api_text["data"]:
        counter_forward += 1
        citing_paper = item.get("citedPaper")
        if citing_paper:
            external_ids = citing_paper.get("externalIds")
            if external_ids:
                arthive_id = external_ids.get("ArXiv", "N/A")
                paper_id = citing_paper.get("paperId", "N/A")
                citation_count = citing_paper.get("citationCount", 0)

        if citation_count > 10 and arthive_id != "N/A":
            articles_arxiv_id.add(arthive_id)
            articles_paper_id.add(paper_id)
            print(
                f"arXiv ID: {arthive_id}, Citation Count: {citation_count} Paper Id: {paper_id} Counter_forward: {counter_forward}")
        if counter_forward % 500 == 0 and counter_forward != 0:
            if offset + limit < 9500:
                if offset + 499 + limit < 10000:
                    offset += 499
                else:
                    offset += 500
                api_url = "https://api.semanticscholar.org/graph/v1/paper/204e3073870fae3d05bcbc2f6a8e263d9b72e776/references?fields=title,citationCount,externalIds&offset=" + str(
                    offset) + "&limit=500"
                api_text = requests.get(api_url).json()
                forward_snowballing_first_wave(counter_forward, api_url, api_text, offset, limit)
            else:
                return


def backward_snowballing_second_wave(counter_forward: int, api_url: str, api_text: dict, offset: int,
                                     limit: int) -> None:
    if offset + limit >= 10000:
        return
    # Извлеките нужные данные
    if "data" in api_text.keys():
        for item in api_text["data"]:
            counter_forward += 1
            citing_paper = item.get("citedPaper")
            if citing_paper:
                external_ids = citing_paper.get("externalIds")
                if external_ids:
                    arthive_id = external_ids.get("ArXiv", "N/A")
                    paper_id = citing_paper.get("paperId", "N/A")
                    citation_count = citing_paper.get("citationCount", 0)
            if citation_count > 10 and arthive_id != "N/A":
                articles_arxiv_id.add(arthive_id)
                articles_paper_id.add(paper_id)
                print(
                    f"arXiv ID: {arthive_id}, Citation Count: {citation_count} paper ID: {paper_id} Counter_forward: {counter_forward} SECOND")

            if (counter_forward % 500 == 0 and counter_forward != 0):
                if offset + limit < 9500:
                    if offset + 499 + limit < 10000:
                        offset += 499
                    else:
                        offset += 500
                    # Получаем часть строки до параметра offset
                    url_before_offset = api_url[:api_url.find("&offset=") + 8]
                    # Получаем часть строки после параметра offset
                    url_after_offset = api_url[api_url.find("&offset=") + 9:]
                    api_url = url_before_offset + str(offset) + url_after_offset
                    api_text = requests.get(api_url).json()
                    backward_snowballing_first_wave(counter_forward, api_url, api_text, offset, limit)
                else:
                    return

forward_snowballing_first_wave(0, "", None, 0, limit)



list_articles_arxiv_id = list(articles_arxiv_id)
list_articles_paper_id = list(articles_paper_id)

print(len(articles_arxiv_id))

# Athurs'
# Осуществляем вторую волну forward snowballing, проходимся по всем элементам articles_paper_ID составленным первой волной
for i in range(len(list_articles_paper_id)):
    api_url = "https://api.semanticscholar.org/graph/v1/paper/" + str(
        list_articles_paper_id[i]) + "/citations?fields=title,citationCount,externalIds&offset=0&limit=500"
    api_text = requests.get(api_url).json()  # получили dict из API'шника(JSON-строка)
    forward_snowballing_second_wave(0, api_url, api_text, 0, limit)

# Vlads'
# for i in range(len(list(list_articles_paper_id))):
#     api_url = "https://api.semanticscholar.org/graph/v1/paper/" + str(list_articles_paper_id[i]) + "/references?fields=title,citationCount,externalIds&offset=0&limit=500"
#     api_text = requests.get(api_url).json()  # получили dict из API'шника(JSON-строка)
#     print(api_url)
#     backward_snowballing_second_wave(0, api_url, api_text, 0, 500)


# for i in range(len(articles_arXiv_ID)):
#     get_pdf("https://arxiv.org//pdf/" + str(list_articles_arXiv_ID[i]) + ".pdf", str(i))
#     print(i, " comlete")
print(len(articles_arxiv_id))