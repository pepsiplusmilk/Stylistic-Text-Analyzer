import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://nplus1.ru/material-print/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
MAX_RECORDS = 2200
START_NUMBER = 6000
DELAY = 0.1  # Задержка между запросами в секундах

def parse_page(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Извлекаем заголовок
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'Без заголовка'
        
        # Извлекаем основной текст (адаптируйте селекторы под реальную структуру страницы)
        content = soup.find_all('p', class_='text-8')  # Замените на актуальный класс
        if not content:
            return None
        #print(content)
        text = ' '.join([p.get_text(strip=True) for p in content])
        text = text.replace('\xa0', ' ').replace('\xad', '').replace('\n', ' ').replace('\r', '')
        return {'Заголовок': title, 'Текст': text}

    except Exception as e:
        print(f"Ошибка при обработке {url}: {str(e)}")
        return None

def main():
    current_number = START_NUMBER
    collected = 0

    with open('articles.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Заголовок', 'Текст'], delimiter=';')
        writer.writeheader()

        while collected < MAX_RECORDS:
            url = f"{BASE_URL}{current_number}"
            print(f"Обработка: {url}")

            page_data = parse_page(url)
            #print(page_data)
            if page_data:
                writer.writerow(page_data)
                collected += 1
                print(f"Найдено записей: {collected}/{MAX_RECORDS}")

            current_number += 1
            time.sleep(DELAY)

    print(f"Готово! Собрано {collected} записей.")

if __name__ == "__main__":
    main()
