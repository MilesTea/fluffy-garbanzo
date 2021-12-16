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
	article_date_snippet = article.find(class_='tm-article-snippet__datetime-published')
	article_date = datetime.strptime(article_date_snippet.contents[0].attrs['title'], '%Y-%m-%d, %H:%M').date()

	# определение заголовка статьи
	article_title_snippet = article.find('a', class_='tm-article-snippet__title-link')
	article_title = article_title_snippet.text
	article_href = article_title_snippet['href']  # ссылка на статью
	article_url = base_url + article_href

	tag_found = False

	# опциональное задание (сильно замедляет работу программы)
	article_response = requests.get(article_url, headers=headers).text
	article_soup = bs4.BeautifulSoup(article_response, features='html.parser')
	content = article_soup.findAll(id="post-content-body")
	article_text = content[0].text
	for tag in my_tags:
		if (tag in article_text.lower()) or (tag in article_title.lower()):
			tag_found = True
	# опциональное задание

	if (hubs & my_tags) or tag_found:
		print(f'<{article_date}> - <{article_title}> - <{article_url}>')