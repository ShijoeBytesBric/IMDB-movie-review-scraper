import scrapy
import re

class Imdbspider(scrapy.Spider):
    name = "IMDbSpider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/title/tt0903747/reviews"]

    def __init__(self):
        self.target_name = None
        self.target_type = None

    def parse(self, response):

        if self.target_name is None or self.target_type is None:
            self.target_name = response.css('a.subnav_heading::text').get()
            self.target_type = response.css('div.subnav > span.nobr::text').get().strip()

        for review in response.css('div.lister-item-content'):
            yield {
                'name': self.target_name, 
                'type': self.target_type, 
                'user_name': review.css('span.display-name-link > a::text').get(), 
                'rating': review.css('span.rating-other-user-rating > span:nth-of-type(1)::text').get(), 
                'review_date': review.css('span.review-date::text').get(), 
                'reviews': review.css('div.show-more__control::text').get()
            }
        
        data_key = response.css('div.load-more-data::attr(data-key)').get()
        if data_key is not None:
            next_page_url = f"https://www.imdb.com/title/tt0068646/reviews/_ajax?ref_=undefined&paginationKey={data_key}"
            next_page = response.urljoin(next_page_url)
            yield scrapy.Request(next_page, callback=self.parse)
