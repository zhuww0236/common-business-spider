# -*- coding: utf-8 -*-


import platform, time
import requests, re
import urllib2
import AnalyticalURL
import JdItemsPage
import JdGoodsPage
import JdLogin
import MjdLogin
import JdCouponsPage
import SqliteData
import Jd2in1Page
import bs4

mjdlogin = MjdLogin.MjdLogin()
jdlogin = JdLogin.JdLogin()
jdgoodspage = JdGoodsPage.JdGoodsPage()
analyticalurl = AnalyticalURL.AnalyticalURL()
jditemspage = JdItemsPage.JdItemsPage()
jdcouponspage = JdCouponsPage.JdCouponsPage()
sqlitedata = SqliteData.SqliteData()
jd2in1page = Jd2in1Page.Jd2in1Page()

def filter_special_characters(content):
    tmp = content.replace('SKU', ' ').replace('sku', ' ').replace(':', ' ').replace('：', ' ').replace('—', ' ').replace('--', ' ').replace('  ', ' ')
    tmp = tmp.replace('https //', 'https://').replace('http //', 'http://')
    tmp = tmp.replace('https://', ' https://').replace('http://', ' http://')
    return tmp

def TestPlatform( ):
    print ("----------Operation System--------------------------")
    #  获取Python版本
    print platform.python_version()

    #   获取操作系统可执行程序的结构，，(’32bit’, ‘WindowsPE’)
    print platform.architecture()

    #   计算机的网络名称，’acer-PC’
    print platform.node()

    #获取操作系统名称及版本号，’Windows-7-6.1.7601-SP1′
    print platform.platform()  

    #计算机处理器信息，’Intel64 Family 6 Model 42 Stepping 7, GenuineIntel’
    print platform.processor()

    # 获取操作系统中Python的构建日期
    print platform.python_build()

    #  获取系统中python解释器的信息
    print platform.python_compiler()

    if platform.python_branch()=="":
        print platform.python_implementation()
        print platform.python_revision()
    print platform.release()
    print platform.system()

    #print platform.system_alias()
    #  获取操作系统的版本
    print platform.version()

    #  包含上面所有的信息汇总
    print platform.uname()

def UsePlatform( ):
    sysstr = platform.system()
    if(sysstr =="Windows"):
        print ("Call Windows tasks")
    elif(sysstr == "Linux"):
        print ("Call Linux tasks")
    else:
        print ("Other System tasks")


if __name__ == "__main__" :

    # TestPlatform( )

    # UsePlatform( )

    urls = [
        'http://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=019cb02928854b2ba2125bfdf1c6830a&roleId=6190975&to=yinluo.jd.com',
        'http://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=382c2a4b1d50481b8b9fb53167ac213e&roleId=6314715&to=sale.jd.com/act/5hz2j7blrfcfa.html',
        'http://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=64d5b965bc564973a2abeb29dc33fdfa&roleId=6380630&to=jahvery.jd.com',
        'http://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=70019f66e1c24b9cb7e303e195600a6d&roleId=6386350&to=haodangjia.jd.com',
        'http://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=882f0944772e430cb79181eef7986d7f&roleId=6314703&to=sale.jd.com/act/5hz2j7blrfcfa.html',
        'http://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=db52e1a99fba43b0bd1dd34287a92f99&roleId=6389795&to=mall.jd.com/index-600329.html',
        'http://coupon.jd.com/ilink/couponActiveFront/front_index.action?key=e670f11e795545b7b3bb469ed31805e3&roleId=5999504&to=qianpinya.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=0023172c63e7479b8a5ca504c6a60c75&roleId=5813953&to=mall.jd.com/index-102092.html',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=00a24c11393a43998d2ac1aaf9ccee48&roleId=5848556&to=toten.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=0318398a5fc847da8346b695e96808c3&roleId=3727866&to=mall.jd.com/index-600315.html',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=04d1be06f84c4a018304b3eac3cf0927&roleId=6328479&to=mall.jd.com/index-80124.html',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=0d4413d5027e413b8d72f37e5d777915&roleId=5919256&to=ophna.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=158ac5575f984a6cae328489e1a5049d&roleId=6343579&to=sale.jd.com/act/b6k0j2qm1zfihi.html',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=1f6ab63381a94064b910d0a8a6a82442&roleId=6258461&to=lami.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=6d8b93d43ab741fd8c0c33de44821e9c&roleId=6271769&to=kasiteng.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=7744b401ec6b42bb8a45a26bd1ce83ff&roleId=6258459&to=lami.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=7e9f373ac690400193f578fbe6bd7f05&roleId=6403277&to=sale.jd.com/act/c7ogxsnbzpgxuf6s.html',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=91fcc91a880546b1a1d81d64cede8912&roleId=6245926&to=luodunbull.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=9c4044f37cb043cea653af9a1e86ac5d&roleId=6370694&to=qiaocheng.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=bb0144bcba1b469eafde62e29a082299&roleId=5741778&to=hometang.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=befaa069fe174ff2bbcd69325eea94c1&roleId=6128711&to=luodunbull.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=e505a25ec0974b89a3d927e99f481206&roleId=6306949&to=alikes.jd.com',
        'http://coupon.jd.com/ilink/couponSendFront/send_index.action?key=e8645227fa1d4383a8a52c39cc5c19c8&roleId=3739583&to=mall.jd.com/index-609020.html',
        'http://dwz.cn/5SQIJ4',
        'http://sep9.cn/5x2maw',
        'http://sep9.cn/ghkmr5',
        'http://suo.im/1qLt5G',
        'http://t.cn/RaZ48Mo',
        'http://t.cn/RaZ4eUP',
        'http://t.cn/RaZ4sKl',
        'http://t.cn/RaZ4YSj',
        'http://t.cn/RaZbhAk',
        'http://t.cn/RXQTtRw',
        'http://t.im/1dapz',
        'http://www.dwz.cn/5SQEnx',
        'https://item.jd.com/11146818602.html',
        'http://item.jd.com/11146818602.html',
        'https://union-click.jd.com/jdc?d=X5riiL'
    ]
    # for url in urls:
    #     print u'目标 ' + str(url)
    #     print u'item 结果 ' + str(analyticalurl.get_real_item_url(url))
    #     # print analyticalurl.get_real_item_url('https://union-click.jd.com/jdc?d=X5riiL')
    #     print u'coupon 结果 ' + str(analyticalurl.get_real_coupon_url(url))
    #     print u'----------------------------'
    #     time.sleep(0.5)
    # print jditemspage.items_page_m('https://item.m.jd.com/product/1861091.html') # 自营
    # print jditemspage.items_page_m('https://item.m.jd.com/product/1571257432.html') # 商家
    # print jditemspage.items_page_m('https://item.m.jd.com/product/10163264234.html') # 京东发货商家售后

    # 测试前台商品详情页代码
    # print jditemspage.items_page_pc_new('https://item.jd.com/1861091.html') # 自营
    # print jditemspage.items_page_pc('https://item.jd.com/12066070252.html') # 商家
    # print jditemspage.items_page_pc('https://item.jd.com/10163264234.html') # 京东发货商家售后

    # 测试联盟商品代码
    # jdlogin.check_login()
    # jdgoodspage.set_sess(jdlogin.get_sess())
    # jdgoodspage.set_cookies(jdlogin.get_cookies())
    # url = 'https://media.jd.com/gotoadv/goods?pageIndex=&pageSize=10&property=&sort=&adownerType=&pcRate=&wlRate=&category=&category1=0&condition=0&fromPrice=&toPrice=&goodsView=list&keyword=20104658'
    # tmp = jdgoodspage.goods_page(url)
    # print tmp
    # print tmp[0]['title']

#     print filter_special_characters('月底冲业绩 亏本卖钟 错过再等一年?久久达【升级版】木头闹钟创意静音学生懒人夜光电子时钟 —————————————?京东价：148.00元券后价：48元?—————————————?领券：http://jd.cn.hn/k7m---------------------------抢购：https://union-click.jd.com/jdc?d=V9Qw0s')
#     ttt = '''
# 59.0内购价：￥29.0内购券：http://dwz.cn/6399DJ
# 内购链接：https://union-click.jd.com/jdc?d=ZiU7iS
#     '''
#     print filter_special_characters(ttt)

'''
# MAC
----------Operation System--------------------------
2.7.10
('64bit', '')
RedrumMBP.local
Darwin-16.5.0-x86_64-i386-64bit
i386
('default', 'Feb  6 2017 23:53:20')
GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)
CPython

16.5.0
Darwin
Darwin Kernel Version 16.5.0: Fri Mar  3 16:52:33 PST 2017; root:xnu-3789.51.2~3/RELEASE_X86_64
('Darwin', 'RedrumMBP.local', '16.5.0', 'Darwin Kernel Version 16.5.0: Fri Mar  3 16:52:33 PST 2017; root:xnu-3789.51.2~3/RELEASE_X86_64', 'x86_64', 'i386')
Other System tasks



# centos
----------Operation System--------------------------
2.7.10
('64bit', 'ELF')
ac0.jixun.local
Linux-2.6.32-431.29.2.el6.x86_64-x86_64-with-centos-6.8-Final
x86_64
('default', 'Apr  6 2017 19:56:50')
GCC 4.4.7 20120313 (Red Hat 4.4.7-17)
CPython

2.6.32-431.29.2.el6.x86_64
Linux
#1 SMP Tue Sep 9 21:36:05 UTC 2014
('Linux', 'ac0.jixun.local', '2.6.32-431.29.2.el6.x86_64', '#1 SMP Tue Sep 9 21:36:05 UTC 2014', 'x86_64', 'x86_64')
Call Linux tasks



# ubuntu
----------Operation System--------------------------
2.7.8
('64bit', 'ELF')
hust-danfo
Linux-3.16.0-34-generic-x86_64-with-Ubuntu-14.10-utopic
x86_64
('default', 'Oct 20 2014 15:05:19')
GCC 4.9.1
CPython

3.16.0-34-generic
Linux
#47-Ubuntu SMP Fri Apr 10 18:02:58 UTC 2015
('Linux', 'hust-danfo', '3.16.0-34-generic', '#47-Ubuntu SMP Fri Apr 10 18:02:58 UTC 2015', 'x86_64', 'x86_64')
Call Linux tasks


# windows
----------Operation System--------------------------
2.7.13
('64bit', 'WindowsPE')
Redrum-Work-E430
Windows-10-10.0.14393
Intel64 Family 6 Model 42 Stepping 7, GenuineIntel
('v2.7.13:a06454b1afa1', 'Dec 17 2016 20:53:40')
MSC v.1500 64 bit (AMD64)
CPython

10
Windows
10.0.14393
('Windows', 'Redrum-Work-E430', '10', '10.0.14393', 'AMD64', 'Intel64 Family 6 Model 42 Stepping 7, GenuineIntel')
Call Windows tasks

'''



urls = [
    'https://item.m.jd.com/product/3133827.html',       # 自营
    'https://item.m.jd.com/product/13205723989.html',   # 商家
    'hhttps://item.m.jd.com/product/10459442922.html',  # 京东配送
]



# for url in urls:
#     print jditemspage.items_page_m(url)

# str_text = [
#     '领券：http://jd.cn.hn/stt下单：SKU：12395383082   佣金：30%',
#     '领券：http://dwz.cn/69fLHL抢购：SKU:12808406788  P:20',
#     '领券：http://jd.cn.hn/sv3下单：SKU：11258866098    佣金：20%',
#     'sku 13106953916',
#     'sku   131069539199',
# ]

# for st in str_text:
#     print st
#     print u'-'*30
#     st = st.replace('SKU', 'sku')
#     st = st.replace('sku：', 'sku:')
#     # print st
#     # print u'-'*30
#     tmp = re.findall(r'((?i)SKU[:|：]? *\d+)', st)
#     # print tmp
#     tmp2 = st + u' https://item.m.jd.com/product/' + str(tmp[0]) + u'.html'
#     print tmp2
#     print u'='*30

# print jditemspage.get_item_price_4_3cn('1732523')
# print jdcouponspage.coupons_page('10136556702', 'http://coupon.m.jd.com/coupons/show.action?key=fdcf8706ecd84f999210868392353026&roleId=6853348&to=item.jd.com/10136556702.html')

# tmp = '''
# -=[ REDRUM ]=- 转发时删除该行
# SKU：10761315647       20%【京东商城】！618返场?亏本继续?只求销量！男女同款，戴上它秒变男神女神，把妹利器，老司机专属！开车出行旅游必备，抢到就是赚到。【赠运费险】京东价：58元  内购价：38元包邮自动领卷链接：http://t.cn/RSza1TC手动领卷链接：http://dwz.cn/69rbQ9 下单SKU： 10761315647京东商城正品保证，支持7天无理由退货！
# '''
# print tmp
# print tmp.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
# print tmp.replace(r' +', ' ')


# sqlitedata.create_table_items()
# jd2in1page.set_sess(mjdlogin.get_sess())
# jd2in1page.set_cookies(mjdlogin.get_cookies())
# jd2in1page.get_2in1_page('https://jingfen.jd.com/item.html?sku=12220245851&q=EHIRFhVsFXUbERRfEXAVRkNmF3YSHBA6FSIXRR1vGHdHRkdnR3dAEhI4FiQiExdqEXIVFiQoRC5HQVcBGSJBQEZrFSQSHBVmFXIbR0c9EyUWHBI9GSFFQkRsECIiEBBuFnQbEBI=&cu=true&utm_source=other_x_short&utm_medium=tuiguang&utm_campaign=t_1000055918_XPGOAX4T&utm_term=77b3c9a68a0f4e0b9a5e5fd260d5a994&abt=3')

# resp = requests.get(
#     'https://item.taobao.com/item.htm?id=525737305953',
#     headers = {
#             'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
#             'ContentType': 'text/html; charset=utf-8',
#             'Accept-Encoding':'gzip, deflate, sdch',
#             'Accept-Language':'zh-CN,zh;q=0.8',
#             'Connection' : 'keep-alive',
#         },
#     timeout = (2, 2)
# )
# soup = bs4.BeautifulSoup(resp.text, "lxml")
# tmp = soup.select('#J_ImgBooth')[0].get('src')
# print tmp



print time.strftime("%Y-12-31", time.localtime())
