__author__ = 'cirnotxm'
# -*- coding: utf-8 -*-
import urllib2
import urllib
import re
import sys
import codecs
from threading import Thread
from Queue import Queue
from time import sleep

reload(sys)
sys.setdefaultencoding('utf8')
print sys.getdefaultencoding()

#对单个参数页面进行爬取
class PhoneCrawl():

    def __init__(self):
        self.phoneinfo = {}
        self.title = ""

    def GetData(self, url):

        req = urllib2.Request("http://detail.zol.com.cn"+url)
        html = urllib2.urlopen(req).read()
        html = unicode(html, "gb2312",errors='ignore').encode("utf8")

        myItems = re.findall('<span.*?class="param-name.*?".*?>(.*?)</span>.+?>(.*?)</span>', html, re.S)
        myItems2 = re.findall('<span.*?id="newPmVal_.*?">(.*?)</span>', html, re.S)
        mytitle = re.findall('<div class="mod_hd"><h3>(.*?)</h3>', html, re.S)

        #print len(myItems)

        #print len(myItems2)

        self.title = mytitle[0]
        self.phoneinfo = {'手机名称':self.title}

        for item in myItems:

            temp = item[1].split('，')
            if len(temp)>1:
                oneitem = ""
                for i in temp:
                    if i.startswith('<'):
                        myItems3 = re.findall('>(.*?)</a>',i,re.S)
                        oneitem = oneitem+myItems3[0]+","
                    else:
                        oneitem = oneitem+i+","
                self.phoneinfo[item[0]] = oneitem
            else:
                if item[1].startswith('<'):
                        myItems3 = re.findall('>(.*?)</a>',item[1],re.S)
                        self.phoneinfo[item[0]]=myItems3[0]
                else:
                    self.phoneinfo[item[0]] = item[1].encode("utf-8")
    #对抓取到的数据进行保存
    def Savedata(self, Filename):
        phoneinfo = self.phoneinfo
        fm=codecs.open("/Users/cirnotxm/others/phonecrawl/"+Filename, "wb", "utf-8")
        fm.write("{\n")
        for param,info in phoneinfo.items():
            param.encode("utf-8")
            info.encode("utf-8")
            if param =='包装清单'or param=='详细内容'or param=='支持频段':
                continue
            para_string = "'"+param+"':'"+info+"'"
           # print para_string
            fm.write(para_string+",\n")

        fm.write("}")

        fm.close()

    def CStart(self, url, filename):
        self.GetData(url)
        self.Savedata(filename)

#简单的多线程队列
class ThreadPool():

    def __init__(self, pages, url):
        self.q = Queue()
        self.NUM = 2
        self.JOBS = pages
        self.url=url

    def Clist(self, arg):
        print self.url+str(arg)+".html"
        req = urllib2.Request(self.url+str(arg)+".html")
        html = urllib2.urlopen(req).read()
        #html = html.decode("utf8")
        print html
        Ahref = re.findall('<a class="more".*?href="(.*?)".*?', html, re.S)
        i = 0
        pc = PhoneCrawl()
        for item in Ahref:
            name = str(arg)+"-"+str(i)+".txt"
            pc.CStart(item,name)
            print item+"----------finish!"
            i=i+1

    def working(self):
        while True:
            arguments = self.q.get()
            self.Clist(arguments+1)
            sleep(1)
            self.q.task_done()

    def PoolStart(self):
        for i in range(self.NUM):
            t = Thread(target=self.working)
            t.setDaemon(True)
            t.start()

        for i in range(self.JOBS):
            self.q.put(i)
        self.q.join()

ThreadPool(10,"http://detail.zol.com.cn/cell_phone_index/subcate57_list_2000-3000_").PoolStart()