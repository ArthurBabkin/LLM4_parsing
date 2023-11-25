from bs4 import BeautifulSoup

#html_file - variable
with open('home.html', 'r', encoding='utf-8') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, "lxml")
    #print(soup.prettify())
    # courses_html_tags = soup.find_all('h1')
    # for course in courses_html_tags:
    #     print(course.text)

    # courses_html_tags1 = soup.find_all('div', class_="")
    # for course in courses_html_tags1:
    #     print(course.a)

    courses_html_tags1 = soup.find_all('div', class_="")
    courses_html_tags1 = soup.find_all('a')
    for course in courses_html_tags1:
        block_name = course.get('title')
        link_to_block = course.get('href')
        if link_to_block != None and block_name != None:
            print("russian: ", block_name.split('/')[0], "\n tatar: ", block_name.split('/')[-1], "\n link: ", link_to_block)