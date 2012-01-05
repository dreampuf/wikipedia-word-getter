#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os
import re
import sys
import time
import urllib2
from threading import currentThread, Thread
import cPickle as pickle
import random
import socket
socket.setdefaulttimeout(10)
from contextlib import closing

from cStringIO import StringIO
from httplib import HTTP, HTTPConnection

from threadpool import ThreadPool, Queue, makeRequests
from lxml import etree
import re

HOST = "http://zh.wiktionary.org"
ct_match = re.compile("Category:(.+)")
item_match = re.compile("wiki/([^:]+)")

def worker(cq, qcs, qns, cs, ns):
    #qcs : Queue Category list
    #qns : Queue Node list
    #cs : Categorey set s
    #ns : Node set s
    crt = currentThread()
    h = HTTPConnection("zh.wiktionary.org") #HTTP()
    h.connect()
    while not cq.empty():
        try:
            task = cq.get(timeout=5)
        except Queue.Empty:
            break

        print crt.getName(), task['url']
        h.putrequest('GET', task['url'])
        h.putheader("User-agent", "Mozilla/5.0")
        h.endheaders()
        
        with closing(h.getresponse()) as resp:
            f = resp.fp
            ret = f.read()

        cur_node = etree.HTML(ret)
        for node in cur_node.xpath("//div[@id='bodyContent']//a[starts-with(@href,'/wiki/Category:')]"):
            href, text = node.get("href"), node.text
            if "#" in href:
                href = href[:href.index("#")]

            if not href or href[:6] != "/wiki/":
                continue
            
            if href not in cs:
                #cts_will.append({"url": HOST + href, "alias": text})
                qcs.put({"url": "%s%s" % (HOST, href), "alias": text})
                cs[href] = [text]
            else:
                cs[href].append(text)
            
            #print node.get("href"), node.text

        for node in cur_node.xpath("//div[@id='bodyContent']//a[not(contains(@href,':'))]"):
            href, text = node.get("href"), node.text
            if "#" in href:
                href = href[:href.index("#")]
            if not href or href[:6] != "/wiki/":
                continue

            if href not in ns:
                qns.put({"url": "%s%s" % (HOST, href), "alias": text})
                ns[href] = [text]
            else:
                ns[href].append(text)
        

def main():

    cur_url = "http://zh.wikipedia.org/wiki/Category:%E9%A0%81%E9%9D%A2%E5%88%86%E9%A1%9E" #"http://zh.wikipedia.org/wiki/Wikipedia:%E5%88%86%E9%A1%9E%E7%B4%A2%E5%BC%95"
    cur_alias = "分类"
    cts = {}
    its = {} # ItemName(Wiki Item URL) : ([Alias1, Alias2, Alias3, ...], [InItemName1, InItemName, ..], [OutItemName1, OutItemName2, ..])
    h = HTTP()
    h.connect("zh.wikipedia.org")
    qcs = Queue.Queue()
    qns = Queue.Queue()
    qcs.put({"url": cur_url, "alias": cur_alias})
    #tp = ThreadPool(10)
    tds = [Thread(target=worker, args=(qcs if i % 2 else qns, qcs, qns, cts, its))
            for i in xrange(10)]

    t_start = time.time()
    for i in tds:
        i.start()
        time.sleep(5)

    for i in tds:
        i.join()
    
    #worker_c(qcs, qns, cts, its)
    #rqs = makeRequests(worker_c, args)
    #[tp.putRequest(req) for req in rqs]

    #try:
    #    tp.joinAllDismissedWorkers()
    #except KeyboardInterrupt:
    #    tp.joinAllDismissedWorkers()
    
    with open("CTS.db", "wb") as f:
        pickle.dump(cts, f)
    with open("ITS.db", "wb") as f:
        pickle.dump(its, f)

    print "CTS:", cts
    print "___________________________"
    print "ITEMS:", its
    print "Coust Time: %s" % (time.time() - t_start)


def analysis_db():
    #DBNAME = "CTS.db"
    #with open(DBNAME) as f:
    #    cts = pickle.load(f)

    #cts = dict([(k, list(set(v))) for k, v in cts.iteritems()])
    #cts = dict([(k, list(set([ct_match.match(v).group(1) if ct_match.match(v) else v for v in v]))) for k, v in cts.items() if len(v) > 1])
    #for k, v in cts.iteritems():
    #    for i in v:
    #        print i

    #with open(DBNAME, "w") as f:
    #    pickle.dump(cts, f)

    DBNAME = "ITS.db"
    with open(DBNAME) as f:
        its = pickle.load(f)
    #its = dict([(k, list(set([item_match.match(i.encode("utf-8")).group(1) if item_match.match(i.encode("utf-8")) else i for i in v]))) for k, v in its.items() if len(v) > 1])

    for k, v in its.iteritems():
        for i in v:
            print i.encode("u8")
    

if __name__ == "__main__":
    #main()
    analysis_db()
