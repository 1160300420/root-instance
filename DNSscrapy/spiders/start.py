import scrapy
import time
import datetime
from pandas.tseries.offsets import Day
from DNSscrapy.spiders.instanceItem import instanceItem
from DNSscrapy.timestamp import gen_timestamp
class dnsSpider(scrapy.Spider):
    name ="dns"
    allowed_domains = ['https://atlas.ripe.net']
    ts = gen_timestamp()
    today = datetime.datetime.now()
    st = (today - 1 * Day()).strftime('%Y-%m-%d %H:%M:%S')  # 格式化
    print(st+"-----")
    #st = time.strftime('%Y-%m-%d %H:%M:%S',    time.localtime(time.time()))
    timestamp=str(int(ts.gen(st)))
    base_url = "https://atlas.ripe.net/api/v2/measurements/10301/timetravel/"
    static_part = "/?fields=responses.0.response_time,responses.0.abuf.answers.0.data_string,created&probe_ids="
    fix_url=base_url+timestamp+static_part+"1"
    print(fix_url)
    start_urls=[fix_url]
   # start_urls = [
   #    'https://atlas.ripe.net/api/v2/measurements/10301/timetravel/1562910180/?fields=responses.0.response_time,responses.0.abuf.answers.0.data_string,created&probe_ids=2']
    def parse(self, response):
        print("oparse")
        urls = response.xpath('body//p/text()').extract()
        print(len(urls))
        print(urls)
        if len(urls) == 0:
            print("none")
        else:
            items = instanceItem()
            list=urls[0].split(',')
            items['domain_name']=list[1]
            items['probe_num']=1
            items['probe_root']=1
            yield items
            print(list[1])
            print(dnsSpider.st)
        print(urls)
        for count in range(2,5):
            temp_url=self.base_url+self.timestamp+self.static_part+str(count)
            print(temp_url)
            req=scrapy.Request(temp_url,callback=self.parse_one,dont_filter=True)
            req.meta['probe'] = count
            yield req


    def parse_one(self,response):
        print("000")
        urls = response.xpath('body//p/text()').extract()
        print(len(urls))
        print(urls)
        if len(urls) == 0:
            print("none")
        else:
            items = instanceItem()
            list = urls[0].split(',')
            items['domain_name'] = list[1]
            items['probe_num'] = response.meta['probe']
            items['probe_root'] = 1
            yield items
            print(list[1])
            print(dnsSpider.st)
        print(urls)

