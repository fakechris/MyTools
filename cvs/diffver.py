#coding:utf-8

import urllib2, difflib

def getFileContent(url):
    try:
        f = urllib2.urlopen(url)
        #print len( f.read() )
        return f.readlines()
    except urllib2.HTTPError:
        return ""

HOST = "192.168.0.65"
CLIENT_LIST = "http://%s/luntbuild/publish/autoupdate/request/%s/artifacts/root_idc/bin_client/list.dat"
SERVER_LIST = "http://%s/luntbuild/publish/autoupdate/request/%s/artifacts/root_idc/bin_server/list.dat"

def get_version_list(ver):
    client_ver = getFileContent(CLIENT_LIST % (HOST, ver))
    server_ver = getFileContent(SERVER_LIST % (HOST, ver))
    return client_ver, server_ver

def parse_ver(content):
    file_map = {}
    content = [l.strip() for l in content if not l.strip().startswith("//") ]
    content = [l.split("\"") for l in content]
    for l in content:
        file_map[l[1]] = (l[3].replace("(","").replace(")",""), l[5])
    return file_map

def samefiles(map1, map2):
    def same(i):
        try:
            return (map2[i][0] == map1[i][0] and map2[i][1] == map1[i][1])
        except:
            return False
    return filter(same, map1)

def campare_version(ver1, ver2):
    c1_ver, s1_ver = get_version_list(ver1)
    c2_ver, s2_ver = get_version_list(ver2)
            
    c1_map = parse_ver(c1_ver)
    c2_map = parse_ver(c2_ver)    
    c_same = samefiles(c1_map, c2_map)    
    c1_diff = filter(lambda x:x not in c_same,  c1_map)
    c2_diff = filter(lambda x:x not in c_same,  c2_map)

    s_diff = set(c1_diff)
    s_diff.update(set(c2_diff))
    c_result = {}
    for i in s_diff:        
        try:
            v1 = c1_map[i][0]
            f1 = c1_map[i][1]
        except:
            v1 = f1 = "none"
        try:
            v2 = c2_map[i][0]
            f2 = c2_map[i][1]
        except:
            v2 = f2 = "none"
        c_result[i] = (v1, v2, f1, f2)
    
    s1_map = parse_ver(s1_ver)
    s2_map = parse_ver(s2_ver)    
    s_same = samefiles(s1_map, s2_map)
    s1_diff = filter(lambda x:x not in s_same,  s1_map)
    s2_diff = filter(lambda x:x not in s_same,  s2_map)
    
    s_diff = set(s1_diff)
    s_diff.update(set(s2_diff))
    s_result = {}
    for i in s_diff:        
        try:
            v1 = s1_map[i][0]
            f1 = s1_map[i][1]
        except:
            v1 = f1 = "none"
        try:
            v2 = s2_map[i][0]
            f2 = s2_map[i][1]
        except:
            v2 = f2 = "none"
        s_result[i] = (v1, v2, f1, f2)
    
    return c_result, s_result
    
def pretty(ver1, ver2, c_result, s_result):
    print "Files changed %s <-> %s"  % (ver1, ver2)
    print "client filename,%sversion,%supdates"  % (" "*(28-len("client filename,")), " "*(20-len("version,")) )
    for c, v in c_result.items():
        print "%s,%s%s/%s,%s%s/%s" % (c, " "*(27-len(c)), v[0], v[1], " "*(18-len(v[0])-len(v[1])),  v[2], v[3])    

    print ""
    
    print "server filename,%sversion,%supdates"  % (" "*(28-len("server filename,")), " "*(20-len("version,")) )
    for c, v in s_result.items():
        print "%s,%s%s/%s,%s%s/%s" % (c, " "*(27-len(c)), v[0], v[1], " "*(18-len(v[0])-len(v[1])),  v[2], v[3])     

    
if __name__ == "__main__":
    ver1 =  "1.0.0.97"
    ver2 =  "1.0.0.94"
    c_result, s_result = campare_version(ver1, ver2)
    pretty(ver1, ver2, c_result, s_result)
    