import re
import random
from scrapy.exceptions import CloseSpider
from twisted.internet import reactor, defer
import requests
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
import scrapy
import json
from datetime import datetime
from scrapy_splash import SplashRequest
class MySpider(scrapy.Spider):
    name =  'spider'
    custom_settings = {
        'DOWNLOAD_DELAY': '2',
	"DOWNLOADER_MIDDLEWARES":  {  'scrapy_splash.SplashCookiesMiddleware': 723,
    	'scrapy_splash.SplashMiddleware': 725,
    	'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
					},
	'SPIDER_MIDDLEWARES' : {
    			'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
		},
	'DUPEFILTER_CLASS' :'scrapy_splash.SplashAwareDupeFilter',
	'SPLASH_URL' : 'http://0.0.0.0:8050/'
    	}
    def __init__(self, search_term):
        self.search_term = search_term
    def start_requests(self):
        yield SplashRequest('https://www.google.com/search?q={}&hl=EN&tbm=isch&source=hp'.format(self.search_term), self.parse, meta={
            'wait': 0.5,
            'splash': {
              'args': {
                  'html': 1,
                  'png': 1,
              }
          },
        }, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
    def parse(self, response):
        #print(response.text)
        c = response.text.split(",")
        imgs = [i for i in c if re.match('^\[(.+)jpg"$', i)]
        print(imgs)
        for i in imgs[:10]:
            filename = i.split('/')[-1]
            url = i.replace('["', '').replace('"', '')
            try:
                r = requests.get(url, timeout=10)
                open(filename, 'wb').write(r.content)
            except:
                pass





import time
configure_logging()
process = CrawlerRunner()
@defer.inlineCallbacks
def crawl():
    yield process.crawl(MySpider, search_term='Carrot')
    reactor.stop()
crawl()
reactor.run()
