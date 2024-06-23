import scrapy


class ImdbspiderSpider(scrapy.Spider):
    name = "IMDbSpider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/title/tt0068646/reviews"]

    def parse(self, response):
        for review in response.css('div.lister-item-content'):
            yield {
                'user_name': review.css('span.display-name-link > a::text').get(),
                'rating': review.css('span.rating-other-user-rating > span:nth-of-type(1)::text').get(),
                'reviews': review.css('div.show-more__control::text').get()
            }
        
        data_key = response.css('div.load-more-data::attr(data-key)').get()
        if data_key is not None:
            next_page_url = f"https://www.imdb.com/title/tt0068646/reviews/_ajax?ref_=undefined&paginationKey={data_key}"
            next_page = response.urljoin(next_page_url)
            yield scrapy.Request(next_page, callback=self.parse)
