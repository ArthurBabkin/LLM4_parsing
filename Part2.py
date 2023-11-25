from bs4 import BeautifulSoup
from selenium import webdriver


driver_path = 'C:\\Users\\Artur\Desktop\\chromedriver-win32\\chromedriver'
url = 'https://www.avito.ru/kazan/vakansii?cd=1&q=python'


driver = webdriver.Chrome()
driver.get(url)
html_text = driver.page_source
print(html_text)
soup = BeautifulSoup(html_text, 'lxml')
#print(html_text)

# job = soup.find_all(class_='iva-item-hideUrl-K81M7')
# salary = soup.find_all(class_='styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-size_l_dense-Wae_G styles-module-size_l-hruVE styles-module-size_dense-z56yO stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-paragraph-l-dense-TTLmp')
# print(salary)
# print(salary[0])
# print(salary[1])
# for j in range(1):
#     block = job[j].get('title')
#     sal = salary[j].find('p', {'data-marker': 'item-price'}).find('meta', {'itemprop': 'price'})['content']
#     print(block)
#     print(sal)








# print(job)
# print("fdasfd")

driver.quit()

# service = Service(executable_path=driver_path)
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service = service, options=options)
# browser = webdriver.Chrome(executable_path=driver_path)
#
#
# # Открываем страницу в браузере
# browser.get(url)
#
# # Получаем HTML-код страницы после выполнения JavaScript
# html_text = browser.page_source
#
# # Создаем объект BeautifulSoup
# soup = BeautifulSoup(html_text, 'lxml')
#
# # Ищем элементы, которые вам нужны
# job = soup.find_all ('div', class_="iva-item-content-rejJg")
# print(job)

# # Закрываем браузер
# browser.quit()
# driver.quit()


