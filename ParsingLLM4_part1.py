from bs4 import BeautifulSoup
import requests

def get_pdf(url, article_counter):
    html = requests.get(url)
    pdf = open(f'C:/Users/Artur/Desktop/testLLM4/{article_counter}.pdf', 'wb')
    pdf.write(html.content)

def doIt(k, soup):
    if k == 0:
        options = soup.find_all('li', class_='arxiv-result')
        for option in options:
            resource_elem = option.find(class_='list-title is-inline-block')
            if resource_elem:
                resource = resource_elem.span.find('a')['href']
                print(resource)
            k += 1
            get_pdf(resource, k)
            print(k)
            if (k % 50 == 0 and k != 0):
                doIt(k, soup)
    else:
        if (k % 50 == 0 and k != 0):
            next_page_link_elem = soup.find('a', class_='pagination-next')
            if next_page_link_elem:
                url = 'https://arxiv.org/' + str(next_page_link_elem['href'])
                #print('f')
                print(url)
        response = requests.get(url)
        html_text = response.content
        soup = BeautifulSoup(html_text, 'lxml')
        options = soup.find_all('li', class_='arxiv-result')
        for i in range(len(options)):
            resource_elem = options[i].find(class_='list-title is-inline-block')
            if resource_elem:
                resource = resource_elem.span.find('a')['href']
                k += 1
                get_pdf(resource, k)
                print(resource)
                print(k)
                if (k % 50 == 0 and k != 0):
                    doIt(k, soup)
url_start = 'https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term=Data+Science&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date=2020-01-01&date-to_date=2023-11-24&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first&start=0'
response = requests.get(url_start)
html_text_start = response.content
soup_start = BeautifulSoup(html_text_start, 'lxml')
doIt(0, soup_start)