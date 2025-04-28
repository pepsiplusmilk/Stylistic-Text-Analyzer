import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

# Настройки
BASE_URL = "http://lib.ru/"
SECTIONS = {
    "РУССКАЯ И ЗАРУБЕЖНАЯ ПОЭЗИЯ": "POEZIQ/",
    "РУССКАЯ ДОВОЕННАЯ ЛИТЕРАТУРА": "PROZA/DRSUHOW/",
    "РУССКАЯ КЛАССИКА": "LITRA/"
}
OUTPUT_FILE = "lib_ru_books.csv"
HEADERS = ['Раздел', 'Автор', 'Название', 'Ссылка']

def get_page(url):
    try:
        response = requests.get(url)
        response.encoding = 'windows-1251'
        return response.text
    except Exception as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        return None

def parse_author_page(author_url):
    works = []
    html = get_page(author_url)
    if not html:
        return works
    
    soup = BeautifulSoup(html, 'html.parser')
    pre_block = soup.find('pre')
    
    if pre_block:
        for link in pre_block.find_all('a'):
            title = link.text.strip()
            if not title:
                continue
                
            work_url = urljoin(author_url, link.get('href'))
            works.append((title, work_url))
    
    return works

def process_section(section_name, section_path, writer):
    section_url = urljoin(BASE_URL, section_path)
    print(f"Обрабатываем раздел: {section_name}")
    
    html = get_page(section_url)
    if not html:
        return
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Ищем авторов в разных возможных структурах
    authors = []
    for element in soup.find_all(['li', 'p']):
        link = element.find('a')
        if link and link.get('href'):
            author_name = link.text.strip()
            author_url = urljoin(section_url, link.get('href'))
            authors.append((author_name, author_url))
    
    for author_name, author_url in authors:
        print(f"Обрабатываем автора: {author_name}")
        works = parse_author_page(author_url)
        
        for title, work_url in works:
            writer.writerow({
                'Раздел': section_name,
                'Автор': author_name,
                'Название': title,
                'Ссылка': work_url
            })

def main():
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
        writer.writeheader()
        
        for section_name, section_path in SECTIONS.items():
            process_section(section_name, section_path, writer)
            time.sleep(1)

if __name__ == "__main__":
    main()
