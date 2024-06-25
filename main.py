from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from IMDbScraper.spiders.IMDbSpider import Imdbspider

def run_spider():

    settings = get_project_settings()

    output_file = f'breaking_bad_reviews.csv'
    settings.update({
        'FEEDS': {
            output_file: {
                'format': 'csv',
                'overwrite': True
            }
        }
    })

    process = CrawlerProcess(settings)
    process.crawl(Imdbspider)
    process.start()


if __name__ == "__main__":
    run_spider()
   