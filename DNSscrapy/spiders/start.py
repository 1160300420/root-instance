import scrapy
import re
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
    timestamp=str(int(ts.gen(st)))
    start_count=1
    end_count=55
    base_url = "https://atlas.ripe.net/api/v2/measurements/10301/timetravel/"
    static_part = "/?fields=responses.0.response_time,responses.0.abuf.answers.0.data_string,created&probe_ids="
    fix_url=base_url+timestamp+static_part+"1"
    start_urls=[fix_url]
    def parse(self, response):
        for count in range(self.start_count,self.end_count):
            temp_url = self.base_url + self.timestamp + self.static_part
            for i in range(1000*(count-1),1000*count):
                temp_url=temp_url+str(i)+","
            temp_url=temp_url+str(1000*count)
            print(temp_url)
            req=scrapy.Request(temp_url,callback=self.parse_one,dont_filter=True)
            req.meta['root_num']=1
            yield req
        for count_rootnum in range(8,10):
            temp_base_url = "https://atlas.ripe.net/api/v2/measurements/1030"+str(count_rootnum)+"/timetravel/"
            for count in range(self.start_count,self.end_count):
                temp_url = temp_base_url + self.timestamp + self.static_part
                for i in range(1000 * (count- 1), 1000 * count):
                    temp_url = temp_url + str(i) + ","
                temp_url = temp_url + str(1000 * count)
                print(temp_url)
                req = scrapy.Request(temp_url, callback=self.parse_one, dont_filter=True)
                req.meta['root_num'] = count_rootnum
                yield req
        #
        for count_rootnum in range(10,17):
            temp_base_url = "https://atlas.ripe.net/api/v2/measurements/103"+str(count_rootnum)+"/timetravel/"
            for count in range(self.start_count, self.end_count):
                temp_url = temp_base_url + self.timestamp + self.static_part
                for i in range(1000 * (count - 1), 1000 * count):
                    temp_url = temp_url + str(i) + ","
                temp_url = temp_url + str(1000 * count)
                print(temp_url)
                req = scrapy.Request(temp_url, callback=self.parse_one, dont_filter=True)
                req.meta['root_num'] = count_rootnum
                yield req
        for count_rootnum in range(4,7):
            temp_base_url = self.base_url="https://atlas.ripe.net/api/v2/measurements/1030"+str(count_rootnum)+"/timetravel/"
            for count in range(self.start_count, self.end_count):
                temp_url = temp_base_url + self.timestamp + self.static_part
                for i in range(1000 * (count - 1), 1000 * count):
                    temp_url = temp_url + str(i) + ","
                temp_url = temp_url + str(1000 * count)
                print(temp_url)
                req = scrapy.Request(temp_url, callback=self.parse_one, dont_filter=True)
                req.meta['root_num'] = count_rootnum
                yield req

    def parse_one(self,response):
        urls = response.xpath('body//p/text()').extract()
        if len(urls) == 0:
            print("none")
        # print(len(urls))
        print(urls)
        pattern = re.compile('"(\d+)"')
        list_item = pattern.findall(urls[0])#probe_num list
        list_temp=urls[0].split(",")
        print(list_item)
        print(list_temp)
        print("len of list_item",len(list_item))
        print("len of list_temp",len(list_temp))
        list_hostname=[]
        for i in range(0,int(len(list_temp)/3)):
            list_hostname.append(list_temp[3*i+1])#hostname list
        num=0
        for count in range(0,len(list_item)):
            if list_hostname[count] != "null":
                num+=1
                items=instanceItem()
                items['domain_name'] = list_hostname[count]
                items['probe_num'] = list_item[count]
                items['probe_root'] = response.meta['root_num']
                yield items
        print("num",num)

