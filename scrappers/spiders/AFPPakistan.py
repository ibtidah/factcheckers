import scrapy
import requests
import mimetypes

class QuotesSpider(scrapy.Spider):
    name = "AFPPaksitan"

    def start_requests(self):
        urls = ['https://factcheck.afp.com/afp-pakistan?page=0']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//div[@class="card"]//a/@href').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parseArticle)
            # get new page url and extract images
        # scrap next url
        currentPage = int(response.url.split('=')[1])
        if currentPage == 24:
            print('DONEEEE DONEEE')
            return
        newUrl = response.url.split('=')[0]+"="+str(currentPage+1)
        yield scrapy.Request(url=newUrl, callback=self.parse)


    def parseArticle(self, response):
        images = response.xpath('//div[@id="wysiwyg"]/img/@src').extract()
        for img in images:
            imgUrl = response.urljoin(img)
            yield {'image_urls': [imgUrl]}
