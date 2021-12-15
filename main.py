import bs4
import requests
from datetime import datetime


my_tags = {'python', 'хакатоны', 'игры и игровые консоли', 'искусственный интеллект'}

base_url = 'https://habr.com'
news_url = base_url + '/ru/news/'
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
}
response = requests.get(news_url, headers=headers)
response.raise_for_status()
text = response.text
soup = bs4.BeautifulSoup(text, features='html.parser')

articles = soup.findAll(class_='tm-articles-list__item')

for article in articles:

	# определение хабов статьи
	hubs = article.find_all('a', class_='tm-article-snippet__hubs-item-link')
	hubs = set(hub.find('span').text.lower() for hub in hubs)

	# определение даты статьи
	news_date_snippet = article.find(class_='tm-article-snippet__datetime-published')
	news_date = datetime.strptime(news_date_snippet.contents[0].attrs['title'], '%Y-%m-%d, %H:%M').date()

	# определение заголовка статьи
	title_snippet = article.find('a', class_='tm-article-snippet__title-link')
	news_title = title_snippet.text
	href = title_snippet['href']  # ссылка на статью

	url = base_url + href
	if hubs & my_tags:
		print(f'<{news_date}> - <{news_title}> - <{url}>')