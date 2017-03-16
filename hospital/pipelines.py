# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from models import engine, Hospital
from sqlalchemy.orm import sessionmaker

class HospitalPipeline(object):
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def process_item(self, item, spider):
        record = Hospital(item['name'], item['province'], item['city'], item['district'],\
                    item['address'], item['phone'], item['category'], item['label'], item['groundpos'],\
                    item['marspos'], item['baidupos'], item['poiid'])

        self.session.add(record)
        self.session.commit()
