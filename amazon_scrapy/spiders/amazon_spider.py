import scrapy
import  json
from urllib.parse import urlencode

class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    
    def start_requests(self):
        keyword_list = ['ipad']  # Add more keywords if needed
        for keyword in keyword_list:
            search_url = f'https://www.amazon.com/s?{urlencode({"k": keyword})}&page=1'
            yield scrapy.Request(url=search_url, callback=self.parse, meta={'keyword': keyword, 'page': 1})

    def parse(self, response):
        keyword = response.meta['keyword']
        page_number = response.meta['page']

        products = response.css('div.s-result-item')
    
        for product in products:
            asin = product.css('div::attr(data-asin)').get()
            title = product.css('h2 span::text').get()
            link = product.css('h2 a::attr(href)').get()
            image_url = product.css('img.s-image::attr(src)').get()
            rating = product.css('span.a-icon-alt::text').get()
            num_reviews = product.css('span.a-size-base::text').re_first(r'\d+,\d+')
            price = product.css('span.a-price-whole::text').get()

            yield {
                'asin': asin,
                'title': title,
                'link': response.urljoin(link),
                'image_url': image_url,
                'rating': rating,
                'num_reviews': num_reviews,
                'price': price
            }

        # Pagination
        next_page = response.css('li.a-last a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
