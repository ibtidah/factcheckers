import scrapy

class QuotesSpider(scrapy.Spider):
    name = "AFPPaksitan"

    def start_requests(self):
        urls = ['https://factcheck.afp.com/afp-pakistan']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//div[@class="card"]//a/@href').extract()
        for url in urls:
            url = response.urljoin(url)
            #print(url)
            yield scrapy.Request(url=url, callback=self.parseArticle)

    def parseArticle(self, response):
        images = response.xpath('//div[@id="wysiwyg"]/img/@src').extract()
        for img in images:
            img = response.urljoin(img)
            print(img)
