import urllib, urllib2, gzip
import simplejson
import sys
import glob
import traceback
from cStringIO import StringIO

COOKIE="	apn-user-id=980472fd-2b9e-4f45-896a-8fb0f6863da3; session-id-time=1282114800l; session-id=183-6006057-6049028; ubid-main=188-6297372-6848067; session-token=VHmR9rzuh1tP+/3mAR41D7WCP6kLRuq0cWt/BojjlnJBoaVEsYExbcXY1amDsqiKy2Qmifm4Y2NKXN05jYiCJBqtPc8iMGNIo9i2f6ftZWvzgl7hBaxPMpnO+7w1f+0kzdh/Ycig5Y6R+M2tAFF45OH2UWwiPMKdMe003l2JLN4susE/XpOkeEQjm+01JN7lxWsrpaUm7VdQje34xLt3VSwLR4gViQLY5L/sTh+1IcWOp5NsHI8inw==; x-main=c16i3SVFt4d?PX9D7Ju6TE6UpATxxjZO"
REFER="http://www.amazon.com/reader/1439083452?_encoding=UTF8&page=509"
ASIN=1439083452
TOKEN="6keeTUqhnXhtYGuHy5H/hJqhiFodR3W0aVfeUWjJoBFipPN4XUzgnw=="

def prepare_req(req):
    req.add_header("Cookie", COOKIE)
    req.add_header("Referer", REFER)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 (.NET CLR 3.5.30729) XPCOMViewer/0.9.2")
    req.add_header("Accept", "application/json, text/javascript, */*")
    req.add_header("Accept-Language", "zh-cn")
    req.add_header("Accept-Encoding", "gzip,deflate")
    req.add_header("Accept-Charset", "GB2312,utf-8;q=0.7,*;q=0.7")
    req.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    req.add_header("X-Requested-With", "XMLHttpRequest")
    req.add_header("Pragma", "no-cache")
    req.add_header("Cache-Control", "no-cache")                

def prepare_req2(req):
    req.add_header("Cookie", COOKIE)
    req.add_header("Referer", REFER)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 (.NET CLR 3.5.30729) XPCOMViewer/0.9.2")
    req.add_header("Accept", "image/png,image/*;q=0.8,*/*;q=0.5")
    req.add_header("Accept-Language", "zh-cn")
    req.add_header("Accept-Encoding", "gzip,deflate")
    req.add_header("Accept-Charset", "GB2312,utf-8;q=0.7,*;q=0.7")
    
def get_gzip_content(req, input=None):
    if input:
        res = urllib2.urlopen(req, input).read()
    else:
        res = urllib2.urlopen(req).read()
    outstream = StringIO(res)
    return gzip.GzipFile(fileobj=outstream).read()

def get_json(v_page):
    req = urllib2.Request("http://www.amazon.com/gp/search-inside/service-data")
    prepare_req(req)
    input = urllib.urlencode({"asin":ASIN,"buyingAsin":ASIN,"method":"goToPage","page":v_page,"token":TOKEN})
    data = get_gzip_content(req, input)
    return simplejson.loads(data)

def fetch_image(id, url):
    req = urllib2.Request("http:" + url)
    prepare_req2(req)
    data = urllib2.urlopen(req).read()
    f = open("%03d.jpg" % id, "wb")
    f.write(data)
    f.close()
    
def main(max_page=509):
    pages = {}
    done_id = set([int(x.split("\\")[-1].split(".")[0]) for x in glob.glob("*.jpg")])
    for i in range(1, max_page+1):
        if i in done_id:
            pages[i] = {'url':None, 'done':True}
        else:
            pages[i] = {'url':None, 'done':False}
    
    for i in range(1, max_page+1):
        try:
            if not pages[i]['done']:
                if not pages[i]['url']:
                    result = get_json(i)
                    try:
                        for k,v in result['largeImageUrls'].items():
                            pages[int(k)]['url'] = v
                    except:
                        print "result", result
                        raise
                fetch_image(i, pages[i]['url'])
        except:
            print "fetch", i, "failed", traceback.format_exc()
    
if __name__ == "__main__":
    main()