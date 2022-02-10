import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4&geo%5Bt%5D%5B1%5D=14']

    def parse(self, response: HtmlResponse):
        # next_page = response.xpath("//a[@rel='next']/@href").get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

        links = response.xpath(
            "//div[@class='f-test-search-result-item']//a[contains(@href,'vakansii')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacansy_parser)

    def vacansy_parser(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").getall()
        salary = response.xpath("//h1/../span/span//text()").getall()
        url = response.url
        # _id = int(re.findall(r'vacancy/(.+?)from', str(link).replace('?', ''))[0])
        yield JobparserItem(name=name, salary=salary, url=url)
