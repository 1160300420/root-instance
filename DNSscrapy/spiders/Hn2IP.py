import dns.resolver
import pymysql
import datetime
from pandas.tseries.offsets import Day


legal_domain=[]
# 打开数据库连接
#query mysql
def get_domain_list(i):
    today = datetime.datetime.now()
    st = (today - 1 * Day()).strftime('%Y%m%d')
    db = pymysql.connect(host="localhost", user="root",
                         password="12345678", db="dnsinfo", port=3306)
    print(st)
    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    # 编写sql 查询语句  user 对应我的表名
    sql = "select domain_name from table_%s"% st+" where root_num='%s'"% i
    print(sql)
    list_domain=[]
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        # 遍历结果
        for row in results:
            row=str(row)
            row=row[3:len(row)-4]
            if "." in row and "_" not in row and "localdomain" not in row and ".eroot" not in row:
                list_domain.append(row)
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接
    list_domain= {}.fromkeys(list_domain).keys()
    return list_domain
root_list=[1,4,5,6,8,9,10,11,12,13,14,15,16]
f = open('./test.txt', 'w')
for ic in root_list:
    list=get_domain_list(ic)
    print(str(ic)+"------"+str(len(list)))
    f.write(str(ic)+"------"+str(len(list)))
    f.write("\n")
    resolver=dns.resolver.Resolver()
    resolver.timeout = 1
    resolver.lifetime = 1
    for dom in list:
        try:
            print(dom)
            a=resolver.query(dom,'A')
            for i in a.response.answer:
                for j in i.items:
                    print(j)
                    f.writelines([dom,"-----",str(j)])
                    f.write("\n")
        except Exception as e:
            print(e)
            continue
    print("\n")
f.close()