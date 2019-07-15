import scrapy
class instanceItem(scrapy.Item):
    #record the domain name of the root-instance
    domain_name=scrapy.Field()
    #record the probe num provided by atlas
    probe_num=scrapy.Field()
    #record the time when probe works
    probe_root=scrapy.Field()