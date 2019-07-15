import time
import datetime
class gen_timestamp():
    def gen(self,st):
        #st ="2019-06-30 03:47:00"
        lt=datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")
        btime=time.mktime(lt.timetuple())+28800
        #print(btime)
        return btime
# st=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
# print(gen_timestamp().gen(st))