import scrapy
import logging
from sdcf.items import SdcfItem

logger = logging.getLogger()

class SDCFSpider(scrapy.Spider):
  name = "sdcf"
  allowed_domains = ["sundowncrossfit.com"]
  start_urls = ["https://www.sundowncrossfit.com"]

  def parse(self, response):
    for i in range(2, 170):
      URI = "https://sundowncrossfit.com/category/wod/page/" + str(i) + "/"
      yield scrapy.Request(URI, callback = self.get_info_url)

  def get_info_url(self, response):
    for sel in response.xpath('//article'):
      for l in sel.xpath('a/@href').extract():
        yield scrapy.Request(l, callback = self.save_wod)

  def save_wod(self, response):
    section_tag = '//div[@class="post-content section-inner thin clearfix"]'
    for content in response.xpath(section_tag).extract():
      item = SdcfItem()
      item['url'] = response.url
      item['content_html'] = content
      yield item
