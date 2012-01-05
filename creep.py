#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import re
import random
import socket
import cPickle as pickle
from threading import currentThread, Thread
from Queue import Queue
socket.setdefaulttimeout(10)
from contextlib import closing
from httplib import HTTP, HTTPConnection
from lxml import etree


class Factory(object):
    def __init__(self, op, mp):
        pass
    def hold(self):
        pass

class Crawl(Thread):
    def __init__(self):
        super(self, Crawl).__init__(self)

class OpenNode(Queue):
    def __init__(self):
        #super(self, OpenNode).__init__(self)
        Queue.__init__(self)
        self._history = []
        self._matchrule = []

    def put(self, obj):
        # obj is a URI
        self.analysis(obj)
        #super(self, OpenNode).put(self, obj)
        Queue.put(self, obj)

    def analysis(self):
        #fetch the URL, GROUP NUMBER : #1: scheme #2: auth name #3: auth password #4: domain, #5: port, #6: path, #7: I DO NOT KWON, #8: GET arg, #9 anchor
        major = re.compile("(?:(\w+)://)?(?:(\w+)(?::(\w+))?@)?([^/;\?:#]+)(?::(\d+))?(?:/?([^;\?#]+))?(?:;([^\?#]+))?(?:\?([^#]+))?(?:#(\w+))?")
        cluster = {(2, "*"): [(url, major.match(url).groups()) for url in URLS]}
        exche = 1
        while exche:
            exche = 0
            
        
        #for url in URLS:
        #    for i in major.finditer(url):
        #        if not i.group(8):
        #            continue
        #        #Path
        #        
        #        paths = i.group(6)
        #        
        #        
        #        print i.groups()

URLS = ['http://www.sina.com.cn',
 'http://tech.sina.com.cn/focus/sinahelp.shtml',
 'http://sina.allyes.com/main/adfclick?db=sina&bid=344807,404080,409394&cid=0,0,0&sid=406736&advid=13662&camid=65569&show=ignore&url=http://ent.sina.com.cn/v/m/2011-12-27/11103518258.shtml',
 'http://travel.sina.com.cn/china/2011-11-16/1446164918.shtml',
 'http://travel.sina.com.cn/china/2011-11-15/1530164865.shtml',
 'http://travel.sina.com.cn/world/2011-11-21/1005165051.shtml',
 'http://travel.sina.com.cn/world/2011-11-18/1549165029.shtml',
 'http://travel.sina.com.cn/hotel/2011-11-21/1043165068.shtml',
 'http://travel.sina.com.cn/world/2011-11-21/1120165074.shtml',
 'http://travel.sina.com.cn/world/2011-11-21/1017165063.shtml',
 'http://travel.sina.com.cn/world/2011-11-16/1117164896.shtml',
 'http://sina.allyes.com/main/adfclick?db=sina&bid=346702,406120,411433&cid=0,0,0&sid=408839&advid=13753&camid=65941&show=ignore&url=http://han.house.sina.com.cn/scan/2011-12-31/092644358.shtml',
 'http://edu.sina.com.cn/zxx/2011-10-09/1725314778.shtml',
 'http://edu.sina.com.cn/zxx/2011-07-12/1700305757.shtml',
 'http://edu.sina.com.cn/a/2010review/index.shtml',
 'http://sina.allyes.com/main/adfclick?db=sina&bid=347122,406540,411853&cid=0,0,0&sid=409260&advid=13772&camid=66098&show=ignore&url=http://cq.sina.com.cn/zt/gwkhj/index.shtml',
 'http://sina.allyes.com/main/adfclick?db=sina&bid=345680,405068,410381&cid=0,0,0&sid=407765&advid=3406&camid=65765&show=ignore&url=http://fj.sina.com.cn/xm/life/wbdrzy/index.shtml',
 'http://sina.allyes.com/main/adfclick?db=sina&bid=342543,401700,407014&cid=0,0,0&sid=404254&advid=3406&camid=65136&show=ignore&url=http://fj.sina.com.cn/xm/zt/weijiyi/index.shtml',
 'http://sina.allyes.com/main/adfclick?db=sina&bid=343805,404323,409637&cid=0,0,0&sid=406980&advid=3406&camid=65377&show=ignore&url=http://henan.sina.com.cn/food/zt/daren2011/index.shtml',
 'http://sports.sina.com.cn/z/nbablog/index.shtml',
 'http://ent.sina.com.cn/f/v/wsknhz2012/index.shtml',
 'http://ent.sina.com.cn/bn/entreport/index.shtml',
 'http://ent.sina.com.cn/f/v/jswskn2012video/index.shtml',
 'http://video.sina.com.cn/z/2011video/index.shtml',
 'http://video.sina.com.cn/z/2011-12-24/052022916.shtml',
 'http://ent.sina.com.cn/z/hsp/index.shtml',
 'http://video.sina.com.cn/movie/movie/index.shtml',
 'http://ent.sina.com.cn/z/2011zuiysj/index.shtml',
 'http://ent.sina.com.cn/z/zymovie/index.shtml',
 'http://ent.sina.com.cn/z/wyz/index.shtml',
 'http://ent.sina.com.cn/z/wdkz2/index.shtml',
 'http://ent.sina.com.cn/z/CNEX/index.shtml',
 'http://ent.sina.com.cn/f/m/xindianyingchuanqi/index.shtml',
 'http://video.sina.com.cn/weiboshow/index.shtml',
 'http://edu.sina.com.cn/j/2011-09-06/1520206500.shtml',
 'http://roll.edu.sina.com.cn/gkkzxzx/zxzx/index.shtml',
 'http://edu.sina.com.cn/l/2011-10-18/1803207869.shtml',
 'http://news.sina.com.cn/z/chinajd90/index.shtml',
 'http://news.sina.com.cn/c/2012-01-03/221123741211.shtml',
 'http://news.sina.com.cn/c/2012-01-03/184123741058.shtml',
 'http://news.sina.com.cn/c/2012-01-03/180723741006.shtml',
 'http://news.sina.com.cn/c/2012-01-04/032923741938.shtml',
 'http://news.sina.com.cn/c/2012-01-04/023323741678.shtml',
 'http://news.sina.com.cn/z/2012chunyun/index.shtml',
 'http://news.sina.com.cn/c/2012-01-04/072723743130.shtml',
 'http://news.sina.com.cn/c/2012-01-04/012923741398.shtml',
 'http://news.sina.com.cn/m/2012-01-04/023323741689.shtml',
 'http://news.sina.com.cn/c/2011-12-23/141623682749.shtml',
 'http://news.sina.com.cn/z/bjjs/index.shtml',
 'http://finance.sina.com.cn/chanjing/gsnews/20120103/233611117890.shtml',
 'http://news.sina.com.cn/w/2012-01-04/040723742437.shtml',
 'http://news.sina.com.cn/w/2012-01-04/071723743154.shtml',
 'http://news.sina.com.cn/z/2012ghd/index.shtml',
 'http://news.sina.com.cn/c/2012-01-04/025323741844.shtml',
 'http://news.sina.com.cn/c/sd/2012-01-04/104223744323.shtml',
 'http://news.sina.com.cn/c/2012-01-04/040423742377.shtml',
 'http://news.sina.com.cn/c/2012-01-04/091623743716.shtml',
 'http://news.sina.com.cn/c/2012-01-04/021423741564.shtml',
 'http://news.sina.com.cn/photo/2011niandupic/index.shtml',
 'http://finance.sina.com.cn/blank/nzch_2011.shtml',
 'http://news.sina.com.cn/c/2012-01-04/144923745280.shtml',
 'http://ent.sina.com.cn/f/v/2011gjsd/index.shtml',
 'http://bj.house.sina.com.cn/news/2012-01-04/0724387812.shtml',
 'http://dichan.sina.com.cn/zt/2011phb/index.shtml',
 'http://sina.allyes.com/main/adfclick?db=sina&bid=346150,405554,410867&cid=0,0,0&sid=408266&advid=5510&camid=65854&show=ignore&url=http://news.sina.com.cn/c/2011-12-30/203723726402.shtml',
 'http://vic.sina.com.cn/20111226/141412082.shtml',
 'http://sina.allyes.com/main/adfclick?db=sina&bid=340042,399057,404369&cid=0,0,0&sid=401470&advid=1293&camid=64305&show=ignore&url=http://client.sina.com.cn/zt/xingfulantu/index.shtml',
 'http://games.sina.com.cn/ghmm/index.shtml',
 'http://l.sina.com.cn/zhuanti/20111229/index.shtml',
 'http://ent.sina.com.cn/f/s/netchina2011/index.shtml',
 'http://ent.sina.com.cn/y/2012-01-04/03023524166.shtml',
 'http://ent.sina.com.cn/y/2012-01-04/06303524218.shtml',
 'http://ent.sina.com.cn/s/h/2012-01-04/10123524344.shtml',
 'http://ent.sina.com.cn/v/m/2012-01-04/14273524591.shtml',
 'http://ent.sina.com.cn/s/h/2012-01-04/08283524236.shtml',
 'http://ent.sina.com.cn/s/h/2012-01-04/10263524359.shtml',
 'http://ent.sina.com.cn/m/c/2012-01-03/23373524108.shtml',
 'http://ent.sina.com.cn/m/c/2012-01-04/02013524129.shtml',
 'http://ent.sina.com.cn/f/v/guomyx/index.shtml',
 'http://ent.sina.com.cn/f/v/xuanya/index.shtml',
 'http://ent.sina.com.cn/f/v/wdntsh/index.shtml',
 'http://ent.sina.com.cn/f/v/chuanqzwang/index.shtml',
 'http://sports.sina.com.cn/cba/2012-01-04/09395893268.shtml',
 'http://sports.sina.com.cn/t/2012-01-04/04105892919.shtml',
 'http://sports.sina.com.cn/t/2012-01-04/14295893757.shtml',
 'http://sports.sina.com.cn/o/2012-01-03/22045892741.shtml',
 'http://sports.sina.com.cn/k/2012-01-04/03475892906.shtml',
 'http://sports.sina.com.cn/g/2012-01-04/06505892982.shtml',
 'http://sports.sina.com.cn/j/2012-01-04/09015893167.shtml',
 'http://sports.sina.com.cn/o/2012-01-04/01055892851.shtml',
 'http://sports.sina.com.cn/o/2012-01-04/08245893085.shtml',
 'http://sports.sina.com.cn/c/2012-01-04/11315893516.shtml',
 'http://sports.sina.com.cn/k/2012-01-04/11415893544.shtml',
 'http://sports.sina.com.cn/k/2012-01-04/10265893359.shtml',
 'http://sports.sina.com.cn/k/2012-01-04/10215893354.shtml',
 'http://sports.sina.com.cn/nba/weekenddime21/index.shtml',
 'http://sports.sina.com.cn/k/2012-01-04/14145893739.shtml',
 'http://sports.sina.com.cn/k/2012-01-04/14235893752.shtml',
 'http://sports.sina.com.cn/k/2012-01-04/10315893371.shtml',
 'http://sports.sina.com.cn/k/2012-01-04/10355893379.shtml']

        


if __name__ == "__main__":
    o = OpenNode()
    o.analysis()
    pass
