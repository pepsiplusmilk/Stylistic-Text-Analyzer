import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import chardet
import time
import re

BASE_URL = "https://lib.ru/RUFANT/"
OUTPUT_FILE = "authors_books.csv"
DELAY = 0.2
HEADERS = ['Заголовок', 'Текст']

def detect_encoding(content):
    return chardet.detect(content)['encoding'] or 'windows-1251'

def get_page(url):
    try:
        response = requests.get(url)
        response.encoding = detect_encoding(response.content)
        return response.text
    except Exception as e:
        print(f"Ошибка загрузки {url}: {e}")
        return None

def clean_text(text):
    return re.sub(r'[\x00-\x1F\x7F-\x9F]|\[.*?\]|\*{3,}', '', text)

def extract_links_after_author_header(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    
    # Ищем любой элемент с текстом "Авторы"
    author_header = soup.find(string=re.compile(r'^\s*Авторы\s*$', re.IGNORECASE))
    if not author_header:
        return []
    
    # Ищем родительский контейнер заголовка
    header_container = author_header.find_parent(['h2', 'b', 'strong', 'div', 'font'])
    
    # Собираем все последующие элементы до следующего заголовка
    current = header_container.next_element
    while current:
        if current.name in ['h1', 'h2', 'h3', 'h4']:
            break
            
        if current.name == 'li':
            link = current.find('a')
            if link and link.get('href'):
                links.append(urljoin(BASE_URL, link['href']))

        if len(links) > 5:
            break
        
        current = current.next_element
    
    return links

def extract_li_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    return [urljoin(base_url, li.a['href']) 
            for li in soup.find_all('li') 
            if li.a and li.a.get('href')]

def parse_book_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    header = soup.find(['h1', 'h2', 'h3']) or soup.find('title')
    title = header.get_text(strip=True) if header else 'Без названия'
    
    text_container = soup.find('pre') or soup.find('div', class_='text')
    text = text_container.get_text(' ', strip=True) if text_container else ''
    
    return title, clean_text(text)

def main():
    main_page = get_page(BASE_URL)
    if not main_page:
        return
    
    first_level_links = extract_links_after_author_header(main_page)
    print(first_level_links)
    second_level_links = []
    for link in first_level_links:
        time.sleep(DELAY)
        page = get_page(link)
        if page:
            second_level_links.extend(extract_li_links(page, link))
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADERS, delimiter=';')
        writer.writeheader()
        
        for i, book_url in enumerate(second_level_links, 1):
            time.sleep(DELAY)
            print(f"Обработка {i}/{len(second_level_links)}: {book_url}")
            
            page = get_page(book_url)
            if not page:
                continue
                
            title, text = parse_book_page(page)
            writer.writerow({
                'Заголовок': title,
                'Текст': text
            })

if __name__ == "__main__":
    main()
