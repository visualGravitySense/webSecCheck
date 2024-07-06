import requests
from bs4 import BeautifulSoup
import re

def evaluate_website(website_url):
    # Оценка дизайна (можно использовать CSS-селекторы для анализа)
    try:
        response = requests.get(website_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Пример оценки: проверяем наличие основного контейнера или изображений на главной странице
        design_score = 5 if soup.find('div', class_='main-container') else 2
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        design_score = 1  # Низкая оценка из-за ошибки

    # Оценка функциональности (можно проверить работу основных функций сайта)
    try:
        # Пример: проверка наличия формы обратной связи или корзины покупок
        functionality_score = 5 if soup.find('form', id='contact-form') else 3
    except Exception as e:
        print(f"Ошибка при оценке функциональности: {e}")
        functionality_score = 1

    # Оценка пользовательского опыта (можно анализировать скорость загрузки, адаптивность и т.д.)
    try:
        # Пример: анализ скорости загрузки страницы
        load_time = requests.get(website_url).elapsed.total_seconds()
        user_experience_score = 5 if load_time < 3 else 3
    except Exception as e:
        print(f"Ошибка при оценке пользовательского опыта: {e}")
        user_experience_score = 1

    # Оценка SEO-продвижения (можно анализировать мета-теги, заголовки и т.д.)
    try:
        # Пример: анализ наличия мета-тегов keywords и description
        meta_tags = soup.find_all('meta', {'name': re.compile(r'keywords|description', re.I)})
        seo_score = 5 if len(meta_tags) >= 2 else 3
    except Exception as e:
        print(f"Ошибка при оценке SEO: {e}")
        seo_score = 1

    # Оценка безопасности (можно анализировать SSL, обработку ввода данных и т.д.)
    try:
        # Пример: проверка наличия SSL-сертификата
        security_score = 5 if website_url.startswith('https://') else 2
    except Exception as e:
        print(f"Ошибка при оценке безопасности: {e}")
        security_score = 1

    # Средняя оценка по всем критериям
    average_score = (design_score + functionality_score + user_experience_score + seo_score + security_score) / 5

    return {
        'design_score': design_score,
        'functionality_score': functionality_score,
        'user_experience_score': user_experience_score,
        'seo_score': seo_score,
        'security_score': security_score,
        'average_score': average_score
    }

# Пример использования
if __name__ == "__main__":
    website_url = "http://autokool.alfapro.ee/"
    evaluation_result = evaluate_website(website_url)

    print(f"Оценка дизайна: {evaluation_result['design_score']}")
    print(f"Оценка функциональности: {evaluation_result['functionality_score']}")
    print(f"Оценка пользовательского опыта: {evaluation_result['user_experience_score']}")
    print(f"Оценка SEO: {evaluation_result['seo_score']}")
    print(f"Оценка безопасности: {evaluation_result['security_score']}")
    print(f"Средняя оценка: {evaluation_result['average_score']}")
