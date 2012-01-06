#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os
import re
import sys
import time
import Queue
import threading
import urllib2
import cPickle as pickle
import random
import socket
socket.setdefaulttimeout(10)
from contextlib import closing

from cStringIO import StringIO


PROCESS_FILE = ".last"
PROCESS_FILE = os.path.realpath(PROCESS_FILE)

class _woker(threading.Thread):
    def __init__(self, dl, tout=5, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(1)
        self._dl = dl
        self._tout = tout
        self.start()

    def run(self):
        while True:
            try:
                task = self._dl._tq.get(True, self._tout)
            #except Queue.Empty, ex:  #some time error processing exit before threading exit
            except (TypeError, Exception), ex:
                self._dl._tds.remove(self)                    
                break
            else:
                ##CORE##
                opener = urllib2.build_opener()
                opener.addheaders = [("User-agent", "Mozilla/5.0 %s" % random.randint(10000))]
                try:
                    req = opener.open(task["url"])
                    data = req.read() #BLOCK
                    req.close()
                    self._dl._rq.put((task["alias"], data), True, self._tout)
                except (urllib2.URLError, socket.timeout), ex:
                    self._dl._tq.put(task)


out = sys.stdout
class Downloader(object):
    def __init__(self, t_num=None):
        self._tnum = t_num or 10
        self._tq = Queue.Queue()
        self._rq = Queue.Queue()
        self._tds = []

    def d(self, tasks, category=None):

        
        #TO SHOW PROCESS
        if isinstance(tasks, basestring): #convert testcase
            tasks = [{"url": tasks }]
        elif isinstance(tasks, dict):
            tasks = [tasks]

        for i in tasks:
            alias = i["url"] if i.get("alias") is None else i["alias"]
            self._tq.put(({"url": i["url"], "alias": alias}))

        rlen = len(tasks)
        ntd = self._tnum - len(self._tds)
        for i in xrange(min(self._tnum - len(self._tds),
                            rlen)):
            self._tds.append(_woker(self))

        while True:
            try:
                out.write("\r%s/%s - theading num: %s" % (self._rq.qsize(), rlen, len(self._tds)))
                out.flush()
                if rlen == self._rq.qsize():
                    break
                else:
                    time.sleep(.5)
            except KeyboardInterrupt, ex:
                #SAVE PROCESS
                #TODO I confused of how to continue to saved process
                if not os.path.exists(PROCESS_FILE):
                    with open(PROCESS_FILE, "wb") as f:
                        pickle.dump({}, f)
                with open(PROCESS_FILE, "rb") as f:
                    try:
                        origin = pickle.load(f)
                    except EOFError, ex: #may error format of file
                        origin = {}
                        with open(PROCESS_FILE, "wb") as nf:
                            pickle.dump({}, nf)

                if category not in origin:
                    origin[category] = {"taskqueue": [],
                                        "retqueue": [],
                                        "thmax": 10 }
                
                c = origin[category]
                c["taskqueue"].extend([i for i in self._tq.queue if i not in c["taskqueue"]])
                c["retqueue"].extend([i for i in self._rq.queue if i not in c["retqueue"]])
                c["thmax"] = self._tnum
                
                with open(PROCESS_FILE, "wb") as f:
                    pickle.dump(origin, f)
                print "\nthe process has saved, start will be load at next time"
                raise StopIteration("stop by user")
        out.write("\n")

        while not self._rq.empty():
            yield self._rq.get()            


def main(*arg):
    from lxml import etree
    import re

    ct_match = re.compile("wiki/Category:(.+)")
    item_match = re.compile("wiki/([^:]+)")

    dl = Downloader(10)
    HOST = "http://zh.wiktionary.org"
    spells = []

    cts = ([], set()) # (will fetch, has fetch)
    cts_will, cts_has = cts
    its = {} # ItemName(Wiki Item URL) : ([Alias1, Alias2, Alias3, ...], [InItemName1, InItemName, ..], [OutItemName1, OutItemName2, ..])

    cur_url = "http://zh.wikipedia.org/wiki/Wikipedia:%E5%88%86%E9%A1%9E%E7%B4%A2%E5%BC%95"
    cur_alias = "分类"
    cts_will.append({"url": cur_url, "alias": cur_alias})
    cur_pos = 0
    while cts_will[cur_pos:]:
        #cur = cts_will.pop(0)
        #cur_alias, cuR_url = cur["alias"], cur["url"]
        #print "also:%s Categorys Item, CurCategory:%s" % (len(cts_will), cur["alias"])
        cur_len = len(cts_will)
        for i in dl.d(cts_will[cur_pos:]):
            cur_node = etree.HTML(i[1])
            for node in cur_node.xpath("//div[@id='bodyContent']//a[starts-with(@href,'/wiki/Category:')]"):
                href, text = node.get("href"), node.text
                if "#" in href:
                    href = href[:href.index("#")]
                if href not in cts_has:
                    cts_will.append({"url": HOST + href, "alias": text})
                
                #print node.get("href"), node.text

            for node in cur_node.xpath("//div[@id='bodyContent']//a[not(contains(@href,':'))]"):
                href, text = node.get("href"), node.text
                if "#" in href:
                    href = href[:href.index("#")]
                if not href and href[:6] != "/wiki/":
                    continue

                if href not in  cts_has:
                    cts_will.append({"url": HOST + href, "alias": text})
                
                if href in its:
                    cn = its[href]
                else:
                    cn = its[href] = (set(), set(), set())
                cn[0].add(text)
                cn[1].add(cur_alias)
                cn[2].add(cur_alias)
                #print node.get("href"), node.text
        cur_pos = cur_len

    
    with open("CTS.db", "wb") as f:
        pickle.dump(cts, f)
    with open("ITS.db", "wb") as f:
        pickle.dump(its, f)

    print "CTS:", cts
    print "___________________________"
    print "ITEMS:", its
        

    
    #for i in dl.d({"url": "http://zh.wiktionary.org/wiki/Wiktionary:%E6%B1%89%E8%AF%AD%E6%8B%BC%E9%9F%B3%E7%B4%A2%E5%BC%95", "alias": "首页"}):
    #    et = etree.HTML(i[1])
    #    for node in et.xpath("//div[@id='bodyContent']/p/a"):
    #        spells.append({"url": "%s%s" % (HOST, node.get("href")), "alias": node.text})

    #letters = []
    #for i in dl.d(spells[:50]):
    #    et = etree.HTML(i[1])
    #    for node in et.xpath("//div[@id='bodyContent']/p/a"):
    #        title = node.get("title")
    #        if title and not title.startswith("Wiktionary"):
    #            letters.append({"url": "%s%s" % (HOST, node.get("href")), "alias": node.text})

    #for i in dl.d(letters[:200]):
    #    et = etree.HTML(i[1])
    #    for node in et.xpath(u"//div[@id='bodyContent']/h3/span[text()='组词']"):
    #        n = node.getparent().getnext()
    #        if n.tag == "ul":
    #            for j in n.xpath("//li/a"):
    #                print j.text

    #        n = node.getnext()
    #        if n and n.tag == "dl" and n.text == "逆序":
    #            n = node.getnext()
    #        if n and n.tag == "ul":
    #            for j in n.xpath("//li/a"):
    #                print j.text
    


#########################################
import unittest

class DownloaderTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDownload(self):
        dl = Downloader(5) #set threading num
        #for i in dl.d("http://zh.wiktionary.org/wiki/Wiktionary:%E6%B1%89%E8%AF%AD%E6%8B%BC%E9%9F%B3%E7%B4%A2%E5%BC%95"):
        #    self.assertTrue(len(i), 2)
        #    self.assertTrue(len(i[0]) > 0)

        #from BeautifulSoup import BeautifulSoup as bs
        from lxml import etree
        sub_matcher = re.compile("""<p>(?P<sub>.+)<a href="/wiki/""", re.U)
        for i in dl.d([{"url": "http://zh.wiktionary.org/wiki/Wiktionary:%E6%B1%89%E8%AF%AD%E6%8B%BC%E9%9F%B3%E7%B4%A2%E5%BC%95/h#huang", "alias": "huang"},
                       {"url": "http://zh.wiktionary.org/wiki/Wiktionary:%E6%B1%89%E8%AF%AD%E6%8B%BC%E9%9F%B3%E7%B4%A2%E5%BC%95/x#xin", "alias": "xin"}]):
            et = etree.HTML(i[1])
            print "\n".join([i.text for i in et.xpath("//div[@id='bodyContent']/p/a[@href]")])
            #soup = bs(i[1])
            #for node in map(lambda x: x.findAll("a"), soup.findAll("div", id="bodyContent")):
            #    for j in node:
            #        print j["href"]


if __name__ == "__main__":
    main(*sys.argv[1:])
    #unittest.main()
