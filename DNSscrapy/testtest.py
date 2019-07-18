# url="https://atlas.ripe.net/api/v2/measurements/10301/timetravel/1563206268/?fields=responses.0.response_time,responses.0.abuf.answers.0.data_string,created&probe_ids="
# for i in range(50000,51000):
#     url=url+str(i)+","
# # url=url+"51000"
# list=['"473":[[6.481', '"ns1.za-jnb.k.ripe.net"', '"2019-07-15T20:10:02+00:00"]]', '"471":[[16.808', '"ns1.ch-zrh.k.ripe.net"', '"2019-07-15T20:10:26+00:00"]]', '"475":[[13.769', '"ns1.nl-ams.k.ripe.net"', '"2019-07-15T20:10:36+00:00"]]}']
#
# list_hostname=[]
# for i in range(0,int(len(list)/3)):
#     list_hostname.append(list[3*i+1])
# print(list_hostname)
s="aa"
b="mm"
c="aa"
if s != b:
    print("false")
else:
    print("true")
if s != c:
    print("false")
else:
    print("true")