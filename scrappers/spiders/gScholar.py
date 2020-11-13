import scrapy
import requests
import mimetypes

class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    abstract = scrapy.Field()

class QuotesSpider(scrapy.Spider):
    name = "gScholar"

    def start_requests(self):
        urls = ['https://scholar.google.com/scholar?start=20&hl=en&as_sdt=2005&sciodt=0,5&cites=9402209269334396424&scipsc=']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        titles = response.xpath('//h3[@class="gs_rt"]//text()').extract()
        abstracts = response.xpath('//div[@class="gs_rs"]')
        print("Articles: ", len(titles), " -- Abstract: ", len(abstracts))
        for index, abstract in enumerate(abstracts):
            abstract = "".join(abstract.xpath('text()').extract()), '\n'
            abstract = abstract[0].replace('\/xa0…','')

            item = ArticleItem()
            item['title'] = titles[index]
            item['abstract'] = abstract
            print(item)
            yield(item)
        # move to next page 
        url = response.xpath('//span[@class="gs_ico gs_ico_nav_next"]/../@href').extract()[0]
        url = response.urljoin(url)
        print(url)
        yield scrapy.Request(url=url, callback=self.parse)

