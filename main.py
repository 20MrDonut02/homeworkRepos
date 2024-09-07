import requests
from bs4 import BeautifulSoup

# Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# URL страницы для парсинга
URL = 'https://habr.com/ru/articles/'

# Получаем HTML-код страницы
response = requests.get(URL)
response.encoding = 'utf-8'  # Устанавливаем кодировку

# Проверяем статус ответа
if response.status_code != 200:
    print("Ошибка при запросе страницы:", response.status_code)
else:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все статьи на странице
    articles = soup.find_all('article')

    # Проверяем, нашли ли мы статьи
    if not articles:
        print("Статьи не найдены.")
    else:
        # Список для подходящих статей
        matching_articles = []

        # Обрабатываем каждую статью
        for article in articles:
            # Получаем заголовок, дату и ссылку
            title_tag = article.find('h2')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.find('a')['href']

                # Получаем дату публикации
                date_tag = article.find('time')
                date = date_tag['datetime'] if date_tag else 'Нет даты'

                # Проверяем наличие ключевых слов в заголовке или анонсе
                preview_text = article.get_text(strip=True)
                if any(keyword.lower() in preview_text.lower() for keyword in KEYWORDS):
                    matching_articles.append(f"{date} – {title} – {link}")

        # Выводим подходящие статьи
        if matching_articles:
            for article in matching_articles:
                print(article)
        else:
            print("Подходящие статьи не найдены.")

