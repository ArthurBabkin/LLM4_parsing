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
