#coding:utf-8

import pefile

def get_product_version(filename):
    pe = pefile.PE(filename)

    rt_string_idx = [entry.id for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries].index(pefile.RESOURCE_TYPE['RT_VERSION'])
    rt_string_directory = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_string_idx]
    entry = rt_string_directory.directory.entries[0]
    pe.parse_version_information(entry.directory.entries[0].data.struct)
    #import pdb; pdb.set_trace()    
    #pe.VS_FIXEDFILEINFO.FileVersionLS/MS ProductVersionLS/MS
    return pe.FileInfo[0].StringTable[0].ProductVersion

if __name__ == "__main__":
    #print get_product_version("D:\\SCSNT\\bin_server\\serveruifacade.dll")
    import os
    #for base, p, f in os.walk("D:\\SCSNT\\bin_server"):
    base_path = "I:\\SCSNT\\bin_server"
    allfiles = [f for f in os.listdir(base_path) if f.lower().endswith(".dll") or f.lower().endswith(".exe")]
    for f in allfiles:
        try:
            print f
            print get_product_version(base_path + "\\" + f)
        except:
            print "No version"
            
    base_path = "I:\\SCSNT\\bin_client"
    allfiles = [f for f in os.listdir(base_path) if f.lower().endswith(".dll") or f.lower().endswith(".exe") or f.lower().endswith(".sys")]
    for f in allfiles:
        try:
            print f
            print get_product_version(base_path + "\\" + f)
        except:
            print "No version"            