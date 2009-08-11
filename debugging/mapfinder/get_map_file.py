#coding:utf-8

import urllib2, os.path
from get_pe_version import get_product_version

MAP_URL = "http://192.168.0.65/luntbuild/publish/%s/%s/%s/artifacts/%s.map"
#delphi/compile-server/1.0.0.43/artifacts/server.map"

MAP_PROJECTS = {
                "delphi": {
                           "compile-client":["client.exe"],
                           "compile-server":["server.exe"],
                           "compile-configset":["callerconfigset.exe"],
                           },
                "core": {
                         "clientuifacade.dll":["clientuifacade.dll"],
                         "serveruifacade.dll":["serveruifacade.dll"],
                         "exportdatauifacade.dll":["exportdatauifacade.dll"],
                         "tools":["configdlg.exe",
                                  "GameUpdateClient.exe",
                                  "GameUpdateServer.exe",
                                  "serverUpdater.exe",],
                         },
                "misc-tools": {
                               "ClientCallback.exe":["ClientCallback.exe"],
                               "InIEReg.exe":["iniereg.exe"],
                               "SCSSysChk.exe":["SCSSysChk.exe"],
                               "VerifyConditionCode.dll":["VerifyConditionCode.dll"],
                               "ietools.exe":["ietools.exe"],
                               
                               },
                "netspy2": {
                            "client.nss_dll":["nssystem.dll","nss_client.dll",],
                            "client.sys_dll":["gppdbg.dll","gppsys.dll",],
                            "clientapi.dll":["clientapi.dll"],
                            "server.nss_dll":["nss_dll.dll"],
                            },
                "scs_driver": {
                               "release.dlls":["RealDisk.dll","scsconfig.dll",],
                               "release.tools":["DriversUpdate.exe","scsset.exe","scs_serviceapp.exe",],
                               "release.scs_freeze.sys":["scs_freeze.sys"],
                               },
                "transport": {
                              "request":["scs_cbtt_exe.exe",
                                          "scs_transpro_dll.dll",
                                          "scs_transpro_dll32.dll",
                                          "scs_xbtc_exe.exe",],
                              },
                }

MAP_INDEX = {}

def build_index():
    for proj, v in MAP_PROJECTS.items():
        for subproj, files in v.items():
            for f in files:
                MAP_INDEX[f.lower()] = (proj, subproj)
                
def get_map_file(filename):
    try:
        version = get_product_version(filename)
    except:
        #print "no version"
        return None
    name = os.path.split(filename)[-1]
    base_name = os.path.splitext( os.path.split(filename)[-1] )[0]
    proj, subproj = MAP_INDEX[name.lower()]
    map_url = MAP_URL % (proj, subproj, version, base_name)
    #print "retriving", map_url
    try:
        f = urllib2.urlopen(map_url)
        #print len( f.read() )
        return f.readlines()
    except urllib2.HTTPError:
        return None

def get_map_fileversion(name, version):
    name = os.path.split(name)[-1]
    base_name = os.path.splitext( os.path.split(name)[-1] )[0]
    proj, subproj = MAP_INDEX[name.lower()]
    map_url = MAP_URL % (proj, subproj, version, base_name)
    #print "retriving", map_url
    try:
        f = urllib2.urlopen(map_url)
        #print len( f.read() )
        return f.readlines()
    except urllib2.HTTPError:
        return None

   
if __name__ == "__main__":
    import os
    #for base, p, f in os.walk("D:\\SCSNT\\bin_server"):
    base_path = "I:\\SCSNT\\bin_server"
    allfiles = [f for f in os.listdir(base_path) if f.lower().endswith(".dll") or f.lower().endswith(".exe")]
    build_index()
    for f in allfiles:
        try:
            print f
            get_map_file(base_path + "\\" + f)    
        except:
            raise
            print "No version or no map file"
            
    base_path = "I:\\SCSNT\\bin_client"
    allfiles = [f for f in os.listdir(base_path) if f.lower().endswith(".dll") or f.lower().endswith(".exe") or f.lower().endswith(".sys")]
    for f in allfiles:
        try:
            print f
            get_map_file(base_path + "\\" + f)    
        except:
            raise
            print "No version or no map file"
