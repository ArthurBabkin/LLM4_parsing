from bs4 import BeautifulSoup
with open('DSAI-01_moodle.html', 'r', encoding='utf-8') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, "lxml")
    names = soup.find_all('a', class_="d-inline-block aabtn")
    for name in names:
        print(name.text[2:])
with open('DSAI-01-part2.html', 'r', encoding='utf-8') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, "lxml")
    names = soup.find_all('a', class_="d-inline-block aabtn")
    for name in names:
        print(name.text[2:])