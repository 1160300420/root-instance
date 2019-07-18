# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime
from pandas.tseries.offsets import Day
class DnsscrapyPipeline(object):
    """
    同步操作
    """
    def __init__(self):
        # 建立连接
        today = datetime.datetime.now()
        self.st = (today - 1 * Day()).strftime('%Y%m%d')
        print(self.st)
        self.conn = pymysql.connect('localhost', 'root', '12345678', 'dnsinfo')  # 有中文要存入数据库的话要加charset='utf8'
        create_sql="CREATE TABLE table_%s"% self.st+"(probe_num INT NOT NULL,root_num INT NOT NULL,domain_name CHAR(50))"
        print("create success")
        # 创建游标
        self.cursor = self.conn.cursor()
        self.cursor.execute(create_sql)
        self.conn.commit()

    def process_item(self, item, spider):
        # sql语句
        insert_sql = "insert into table_%s"% self.st+"(probe_num,root_num,domain_name) VALUES(%s,%s,%s)"
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql,(item['probe_num'], item['probe_root'], item['domain_name']))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
# import pymysql
# from twisted.enterprise import adbapi
# class DnsscrapyPipeline(object):
#     def __init__(self,dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
#         """
#         数据库建立连接
#         :param settings: 配置参数
#         :return: 实例化参数
#         """
#         # adbparams = dict(
#         #     host=settings["127.0.0.1"],
#         #     db=settings["dnsinfo"],
#         #     user=settings["root"],
#         #     password=settings["12345678"],
#         #     cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
#         # )
#         # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
#         dbpool = adbapi.ConnectionPool("pymysql", host=settings["MYSQL_HOST"], db=settings["MYSQL_DBNAME"],
#                                        user=settings["MYSQL_USER"], password=settings["MYSQL_PASSWORD"], charset="utf8",
#                                        cursorclass=pymysql.cursors.DictCursor,
#                                        use_unicode=True)
#         # 返回实例化参数
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         """
#         使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
#         """
#         query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
#         # 添加异常处理
#         query.addCallback(self.handle_error)  # 处理异常
#         return item
#
#     def do_insert(self, cursor, item):
#         # 对数据库进行插入操作，并不需要commit，twisted会自动commit
#         insert_sql ="""insert into probe_instance(probe_num,root_num,instance_num) VALUES(%s,%s,%s)"""
#
#         cursor.execute(insert_sql, (item['probe_num'], item['probe_root'], item['domain_name']))
#
#     def handle_error(self, failure):
#         if failure:
#             # 打印错误信息
#             print(failure)