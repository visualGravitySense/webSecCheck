import requests
from bs4 import BeautifulSoup
import re
import csv

def evaluate_website(website_url):
    try:
        response = requests.get(website_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        design_score = 5 if soup.find('div', class_='main-container') else 2
        functionality_score = 5 if soup.find('form', id='contact-form') else 3
        load_time = requests.get(website_url).elapsed.total_seconds()
        user_experience_score = 5 if load_time < 3 else 3
        meta_tags = soup.find_all('meta', {'name': re.compile(r'keywords|description', re.I)})
        seo_score = 5 if len(meta_tags) >= 2 else 3
        security_score = 5 if website_url.startswith('https://') else 2

        average_score = (design_score + functionality_score + user_experience_score + seo_score + security_score) / 5

        return {
            'website_url': website_url,
            'design_score': design_score,
            'functionality_score': functionality_score,
            'user_experience_score': user_experience_score,
            'seo_score': seo_score,
            'security_score': security_score,
            'average_score': average_score
        }
    except Exception as e:
        print(f"Ошибка при оценке сайта {website_url}: {e}")
        return None

def save_to_csv(results, output_file):
    try:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Design Score', 'Functionality Score', 'User Experience Score', 'SEO Score', 'Security Score', 'Average Score'])

            for result in results:
                writer.writerow([
                    result['website_url'],
                    result['design_score'],
                    result['functionality_score'],
                    result['user_experience_score'],
                    result['seo_score'],
                    result['security_score'],
                    result['average_score']
                ])
        print(f"Результаты сохранены в файл: {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении в файл {output_file}: {e}")

if __name__ == "__main__":
    csv_input_file = 'schoolsTest.csv'
    csv_output_file = 'website_evaluations.csv'
    results = []

    try:
        with open(csv_input_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header if exists

            for row in reader:
                website_url = row[0].strip()
                evaluation_result = evaluate_website(website_url)

                if evaluation_result:
                    results.append(evaluation_result)

        save_to_csv(results, csv_output_file)

    except FileNotFoundError:
        print(f"Файл {csv_input_file} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении CSV файла: {e}")
