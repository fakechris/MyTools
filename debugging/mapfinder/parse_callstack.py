#coding:utf-8

import re
from get_map_file import build_index, get_map_file
from mapfinder import map_find, delphi_map_find

RE_MAPNEED = re.compile(">?\t?([^!]+)!([0-9a-f]+)\(\)\s*")

g_cached_map = {}
delphi_modules = ["client.exe", "server.exe", "callerconfigset.exe",] 

def parse_address(input):
    return [int(c,16) for c in input.strip().replace("*","").split("-")]

class Module:
    name = ""
    fullpath = ""
    pdb = ""
    version = ""
    loadaddr = 0
    endaddr = 0

class InputParser:
    def __init__(self, inputfile):
        f = file(input)
        self.lines = [ l.strip() for l in f.readlines() ]
        f.close()
        
        self.modules = {}
        self.callstacks = []

    def parse(self):
        module_lines = [l for l in self.lines if len(l.split("\t")) > 6]
        callstack_lines = [l for l in self.lines if len(l.split("\t")) < 6]
        
        for m in module_lines:
            module = Module()
            mval = m.split("\t")
            module.name = mval[0]
            module.fullpath = mval[1]
            module.pdb = mval[5]
            module.version = mval[7]
            module.loadaddr, module.endaddr = parse_address(mval[9])
            
            self.modules[module.name] = module
            
        for c in callstack_lines:
            m = RE_MAPNEED.match(c)
            if m:                
                name, addr = m.groups()
                addr = int(addr,16)
                mod = self.modules[name]
                #print "parse needed", mod.name, addr, mod.fullpath, mod.loadaddr
                if g_cached_map.has_key(mod.fullpath):
                    map_content = g_cached_map[mod.fullpath]
                else:
                    map_content = get_map_file(mod.fullpath)
                    g_cached_map[mod.fullpath] = map_content
                if map_content:
                    try:
                        if name.lower() not in delphi_modules:
                            loc = map_find(map_content, mod.loadaddr, addr)
                            #print loc                        
                        else:
                            loc = delphi_map_find(map_content, mod.loadaddr, addr)
                            #print loc
                        c = "%s!%s() %s(%s) %04x:%08x" % (name, loc[2], loc[3], loc[4], loc[0], loc[1])
                    except:
                        pass
                self.callstacks.append(c)
            else:
                self.callstacks.append(c)
       
if __name__ == "__main__":
    input = "D:\\work\\scsgit\\mapfinder\\input.txt"
    #lines = [ l.strip() for l in file(input).readlines() ]
    #module_lines = [l for l in lines if len(l.split("\t")) > 6]
    #callstack_lines = [l for l in lines if len(l.split("\t")) < 6]    
    #print module_lines
    #print callstack_lines
    build_index()
    ip = InputParser(input)
    ip.parse()
    for c in ip.callstacks: 
        print c 
    #for n,m in ip.modules.items(): 
    #    print m.name, m.loadaddr, m.endaddr, m.version, m.fullpath, m.pdb 
        