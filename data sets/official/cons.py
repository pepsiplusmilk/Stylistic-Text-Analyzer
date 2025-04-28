import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE_URL = 'https://www.consultant.ru'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

def get_article_links(main_url):
    try:
        response = requests.get(main_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при загрузке оглавления: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем блок с содержанием
    toc_block = soup.find('div', class_='document-page__toc')
    if not toc_block:
        print("Блок содержания не найден!")
        return []

    # Собираем все ссылки, начинающиеся с "Статья"
    articles = []
    for link in toc_block.find_all('a', href=True):
        link_text = link.get_text(strip=True)
        if link_text.startswith('Статья'):
            article_url = urljoin(BASE_URL, link['href'])
            articles.append({
                'title': link_text,
                'url': article_url
            })

    return articles

def parse_article_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка загрузки статьи: {url} - {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Извлекаем основной текст статьи
    content = soup.find('div', class_='document-page__content')
    if not content:
        print("x")
        return None

    # Очищаем от ненужных элементов
    for elem in content.find_all(['script', 'style', 'noscript', 'aside', 'footer', 'table']):
        elem.decompose()

    # Собираем текст статьи
    text_blocks = []
    for p in content.find_all(['p', 'div'], class_= False, id=False):
        text = ' '.join(p.get_text(strip=True).split())
        text = text.replace('\xa0', ' ').replace('\xad', '')
        text_blocks.append(text)

    #print(f'\n---------------------------\n{text_blocks}\n----------------------\n')
    return ' '.join(text_blocks)

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Название статьи', 'Текст'])
        for item in data:
            writer.writerow([item['title'], item['text']])

def main():
    start_url = 'https://www.consultant.ru/document/cons_doc_LAW_10699/'
    
    print("Сбор ссылок на статьи...")
    articles = get_article_links(start_url)
    
    if not articles:
        print("Не найдено статей для парсинга")
        return
    
    print(f"Найдено статей: {len(articles)}")
    
    result = []
    for idx, article in enumerate(articles, 1):
        print(article)
        print(f"Обработка [{idx}/{len(articles)}]: {article['title']}")
        
        article_text = parse_article_page(article['url'])
        if article_text:
            result.append({
                'title': article['title'],
                'text': article_text
            })
        
        time.sleep(0.12)  # Задержка для соблюдения правил сайта
    
    if result:
        save_to_csv(result, 'criminal_code.csv')
        print(f"Успешно сохранено {len(result)} статей")
    else:
        print("Нет данных для сохранения")

if __name__ == '__main__':
    main()
