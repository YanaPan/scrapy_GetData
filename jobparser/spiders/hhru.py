import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?clusters=true&area=1&no_magic=true&ored_clusters=true&items_on_page=20&enable_snippets=true&salary=&text=Python',
                  'https://hh.ru/search/vacancy?clusters=true&area=2&no_magic=true&ored_clusters=true&items_on_page=20&enable_snippets=true&salary=&text=Python']

    def parse(self, response: HtmlResponse):
        # next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
