from bs4 import BeautifulSoup
import requests

articles = []

def get_pdf(url, article_counter):
    html = requests.get(url)
    pdf = open(f'C:/Users/Artur/Desktop/testLLM4/{article_counter}.pdf', 'wb')
    pdf.write(html.content)


def find_articles_names(k, soup):
    if k == 1000:
        return
    if k == 0:
        url = 'https://dl.acm.org/action/doSearch?AllField=Data+Science&ContentItemType=research-article&startPage=0&pageSize=50'
        response = requests.get(url)
        html_text = response.content
        soup = BeautifulSoup(html_text, 'lxml')
        options = soup.find_all('h5', class_='issue-item__title')
        for option in options:
            articles.append(str(option.find('a').text))
            k += 1
            print(articles[-1])
            print(k)
            if (k % 50 == 0 and k != 0):
                find_articles_names(k, soup)
    else:
        if (k % 50 == 0 and k != 0):
            url = "https://dl.acm.org/action/doSearch?AllField=Data+Science&ContentItemType=research-article&startPage=" + str(k/50) + "&pageSize=50"
        response = requests.get(url)
        html_text = response.content
        soup = BeautifulSoup(html_text, 'lxml')
        options = soup.find_all('h5', class_='issue-item__title')
        for option in options:
            articles.append(str(option.find('a').text))
            k += 1
            print(articles[-1])
            print(k)
            if (k % 50 == 0 and k != 0):
                find_articles_names(k, soup)

def shcolar_parse(article_name: str):
    article_name.replace(' ', '+')
    url = f'https://scholar.google.com/scholar?q={article_name}'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    test = soup.find('div', class_='gs_r gs_or gs_scl')
    print(test)


find_articles_names(0, 0)
print(articles[0])
shcolar_parse(articles[0])

