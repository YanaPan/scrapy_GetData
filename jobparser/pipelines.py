# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo import errors
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies0902

    def process_item(self, item, spider):
        if spider.name == "hhru":
            dirty_salary = self.hhprocess_salary(item.get('salary'))
            _id = int(re.findall(r'vacancy/(.+?)from', item.get('url').replace('?', ''))[0])
        else:
            dirty_salary = self.sjprocess_salary(item.get('salary'))
            _id = int(re.findall(item.get('url'), r'-(.+?).html')[0])

        item['salary_min'], item['salary_max'], item['cur'] = dirty_salary
        collection = self.mongobase[spider.name]
        try:
            collection.insert_one(item)
        except errors.DuplicateKeyError:
            print(f'Вакансия {_id} уже есть в базе данных')


    def hhprocess_salary(self, dirty_salary):
        salary_min, salary_max, cur = None, None, 'руб'
        dirty_salary = list(filter(None, dirty_salary))
        if dirty_salary.index('от'):
            salary_min = dirty_salary[dirty_salary.index('от')+1].replace('\xa0', '')
            cur = dirty_salary[-2]
        elif dirty_salary.index('до'):
            salary_max = dirty_salary[dirty_salary.index('до')+1].replace('\xa0', '')
            cur = dirty_salary[-2]
        else:
            pass

        return salary_min, salary_max, cur

    def sjprocess_salary(self, dirty_salary):
        salary_min, salary_max, cur = None, None, 'руб'
        dirty_salary = list(filter(None, dirty_salary))
        if dirty_salary.index('руб'):
            if dirty_salary.index('от'):
                salary_min = dirty_salary[dirty_salary.index('от') + 1].replace('\xa0', '')
            elif dirty_salary.index('до'):
                salary_max = dirty_salary[dirty_salary.index('до') + 1].replace('\xa0', '')
            else:
                salary_min = dirty_salary[0].replace('\xa0', '')
                salary_max = dirty_salary[2].replace('\xa0', '')

        return salary_min, salary_max, cur
