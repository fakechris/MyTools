#coding:utf-8

import os, sys, datetime, re, types
from bisect import bisect_left, bisect_right

"""
class Addr:
    section = 1
    offset = 0
"""

def parse_secoff(input):
    return [int(c,16) for c in input.strip().split(":")]

class Section:
    section = 1
    offset = 0
    length = 0
    name = ""
    type = "CODE"

class Function:
    section = 1
    offset = 0
    name = ""
    rvabase = 0
    f = False
    i = False
    obj = ""
    
class Symbols:
    section = 1
    offset = 0
    name = ""
    rvabase = 0
    f = False
    i = False
    obj = ""

class Line:
    section = 1
    offset = 0
    line = 0
    obj = ""
    src = ""

RE_LINE_HEADER = re.compile("Line numbers for ([^\(]+)\(([^\)]+)\) segment.*")
RE_SECTION = re.compile("Start\s+Length\s+Name\s+Class")
RE_FUNCTION = re.compile("Address\s+Publics by Value\s+Rva\+Base\s+Lib:Object")
RE_STATICSYMS = re.compile("Static\s+symbols")

S_NAME = "name"
S_TIMESTAMP = "timestamp"
S_PREFERBASE = "preferredbase"
S_SECTIONS = "section"
S_FUNCTIONS = "function"
S_ENTRYPOINT = "entry"
S_STATICSYMS = "staticsyms"
S_LINE_HEADER = "line_header"
S_LINE_NO = "line_no"
S_END = "end"

RE_DETAILMAP = re.compile("Detailed map of segments")
RE_FUNCTION1 = re.compile("Address\s+Publics by Name")
RE_FUNCTION3 = re.compile("Address\s+Publics by Value")
S_DETAILMAP = "detailmap"
S_DETAILMAP1 = "detailmap1"
S_FUNCTIONS1 = "function1"
S_FUNCTIONS2 = "function2"
S_FUNCTIONS3 = "function3"
S_FUNCTIONS4 = "function4"

class VCMapParser:
    def __init__(self, contents):
        self.contents = contents
        
        self.look_forward = False
        self.stage = S_NAME    
        
        self.current_obj = ""
        self.current_src = ""
                
        self.entry = None
        self.timestamp = None
        self.sections = {}
        self.staticsyms = {}
        
        self.preferred_base = 0        
        self.functions = {}
        self.lines = {}
            
        self.lines_idx = {}    
        self.functions_idx = {}        
    
    def find(self, rvapos):
        #print "%x" % (rvapos - 0x1000)
        
        #import pdb; pdb.set_trace()
        i = bisect_right(self.lines_idx[1], rvapos - 0x1000)
        l = self.lines[1][i-1]

        j = bisect_right(self.functions_idx[1], rvapos - 0x1000)
        f = self.functions[1][j-1]
        
        #print "%s %s %s %s %x" % (l.line, l.src, l.obj, f.name, f.rvabase)
        #return "%04x:%08x %s %s(%s) %s" % (f.section, f.offset, f.name, l.src, l.line, l.obj)
        return (f.section, f.offset, f.name, l.src, l.line)
    
    def print_stage(self):
        return
        print l, " next level is ", self.stage 
       
    def parse(self):
        for l in self.contents:
            fn = getattr(self, "parse_" + self.stage)
            fn(l.strip())
        #print self.functions
        #print self.preferred_base
        #print self.lines
        for f in self.functions:
            self.functions[f].sort(key=lambda x:x.offset)
            #print [i.offset for i in self.functions[f]]
            self.functions_idx[f] = [i.offset for i in self.functions[f]]
        for f in self.lines:
            self.lines[f].sort(key=lambda x:x.offset)
            #print [i.offset for i in self.lines[f]]
            self.lines_idx[f] = [i.offset for i in self.lines[f]]

    def parse_end(self, l):
        pass

    def parse_line_no(self, l):
        if l == "":
            self.stage = S_LINE_HEADER
            self.print_stage()
            return        
        s = [i for i in l.split(" ") if i != '']
        #lno = []
        for i in range(len(s) / 2):
            line = Line()
            line.line = int(s[i*2])
            line.section, line.offset = parse_secoff(s[i*2+1])
            line.obj = self.current_obj
            line.src = self.current_src
            #lno.append( line )
            if not self.lines.has_key(line.section):
                self.lines[line.section] = []
                #self.lines_idx[line.section] = []
            self.lines[line.section].append(line)
            #self.lines_idx[line.section].append(line.offset)
    
    def parse_line_header(self, l):
        if l == "":
            self.stage = S_LINE_NO
            self.print_stage()
            return
        m = RE_LINE_HEADER.match(l)
        if m:
            self.current_obj, self.current_src = m.groups()
        else:
            self.stage = S_END
            self.print_stage()
    
    def parse_staticsyms(self, l):
        if RE_STATICSYMS.match(l):
            pass
        if l == '':
            if not self.look_forward:
                self.look_forward = True               
            else:
                self.look_forward = False
                self.stage = S_LINE_HEADER    
                self.print_stage()        
        return
    
    def parse_entry(self, l):
        if l == '':
            self.stage = S_STATICSYMS
            self.print_stage()
            return
        self.entry = parse_secoff(l.split(" ")[-1])        
    
    def parse_function(self, l):
        if RE_FUNCTION.match(l):
            return
        if l == '':
            if not self.look_forward:
                self.look_forward = True               
            else:
                self.look_forward = False
                self.stage = S_ENTRYPOINT
                self.print_stage()
            return
        s = [i for i in l.split(" ") if i != '']
        f = Function()
        if len(s) == 5:
            f.f = True
        if len(s) == 6:
            f.i = True
        s = [i for i in s if i!='f' and i!='i']
        f.section, f.offset = parse_secoff(s[0])
        f.name = s[1]
        f.rvabase = int(s[2], 16)
        f.obj = s[3]
        
        if not self.functions.has_key(f.section):
            self.functions[f.section] = []
            #self.functions_idx[f.section] = []
        self.functions[f.section].append(f)
        #self.functions_idx[f.section].append(f.offset)
           
    def parse_section(self, l):
        if RE_SECTION.match(l):
            self.look_forward = True
        if l == '':
            if not self.look_forward:
                return
            else:
                self.look_forward = False
                self.stage = S_FUNCTIONS  
                self.print_stage()         
        return
        s = [i for i in l.split(" ") if i != '']
        section = Section()
        section.section, section.offset = parse_secoff(s[0])
        section.length = int(s[1], 16)
        section.name = s[2]
        section.type = s[3]
        return section
            
    def parse_preferredbase(self, l):
        if l == '':
            return
        self.preferred_base = int(l.split(" ")[-1], 16)
        self.stage = S_SECTIONS
        self.print_stage()
                    
    def parse_timestamp(self, l):
        if l == '':
            return
        self.stage = S_PREFERBASE
        self.print_stage()

    def parse_name(self, l):
        self.stage = S_TIMESTAMP 
        self.print_stage() 
        
class DelphiMapParser:
    def __init__(self, contents):
        self.contents = contents
        
        self.look_forward = False
        self.stage = S_SECTIONS    
        
        self.current_obj = ""
        self.current_src = ""
                
        self.entry = None
        self.timestamp = None
        self.sections = {}
        self.staticsyms = {}
        
        self.preferred_base = 0        
        self.functions = {}
        self.lines = {}
            
        self.lines_idx = {}    
        self.functions_idx = {}        

    def print_stage(self):
        return
        print l, " next level is ", self.stage 
            
    def find(self, rvapos):
        #print "%x" % (rvapos - 0x1000)
        
        #import pdb; pdb.set_trace()
        i = bisect_right(self.lines_idx[1], rvapos - 0x1000)
        l = self.lines[1][i-1]

        j = bisect_right(self.functions_idx[1], rvapos - 0x1000)
        f = self.functions[1][j-1]
        
        #print "%s %s %s %s %x" % (l.line, l.src, l.obj, f.name, f.rvabase)
        #return "%04x:%08x %s %s(%s)" % (f.section, f.offset, f.name, l.src, l.line)
        return (f.section, f.offset, f.name, l.src, l.line)
        
    def parse(self):
        for l in self.contents:
            fn = getattr(self, "parse_" + self.stage)
            fn(l.strip())
        #print self.functions
        #print self.preferred_base
        #print self.lines
        for f in self.functions:
            self.functions[f].sort(key=lambda x:x.offset)
            #print [i.offset for i in self.functions[f]]
            self.functions_idx[f] = [i.offset for i in self.functions[f]]
        for f in self.lines:
            self.lines[f].sort(key=lambda x:x.offset)
            #print [i.offset for i in self.lines[f]]
            self.lines_idx[f] = [i.offset for i in self.lines[f]]
            
    def parse_end(self, l):
        pass
    
    def parse_line_no(self, l):
        if l == "":
            self.stage = S_LINE_HEADER
            self.print_stage()
            return        
        s = [i for i in l.split(" ") if i != '']
        #lno = []
        for i in range(len(s) / 2):
            line = Line()
            line.line = int(s[i*2])
            line.section, line.offset = parse_secoff(s[i*2+1])
            line.obj = self.current_obj
            line.src = self.current_src
            #lno.append( line )
            if not self.lines.has_key(line.section):
                self.lines[line.section] = []
                #self.lines_idx[line.section] = []
            self.lines[line.section].append(line)
            #self.lines_idx[line.section].append(line.offset)
    
    def parse_line_header(self, l):
        if l == "":
            self.stage = S_LINE_NO
            self.print_stage()
            return
        m = RE_LINE_HEADER.match(l)
        if m:
            self.current_obj, self.current_src = m.groups()
        else:
            self.stage = S_END
            self.print_stage()

    def parse_function4(self, l):
        if l == '':
            if not self.look_forward:
                self.look_forward = True
            else:
                self.look_forward = False
                self.stage = S_LINE_HEADER 
                self.print_stage()       
            return  

    def parse_function3(self, l):
        if RE_FUNCTION3.match(l):
            self.look_forward = True
        if l == '':
            if not self.look_forward:
                return
            else:
                self.look_forward = False
                self.stage = S_FUNCTIONS4 
                self.print_stage()         

    def parse_function2(self, l):
        if l == '':
            if not self.look_forward:
                self.look_forward = True
            else:
                self.look_forward = False
                #self.stage = S_LINE_HEADER 
                self.stage = S_FUNCTIONS3
                self.print_stage()       
            return  
            
        s = [i for i in l.split(" ") if i != '']
        f = Function()
        f.section, f.offset = parse_secoff(s[0])
        f.name = s[1]
        
        if not self.functions.has_key(f.section):
            self.functions[f.section] = []
            #self.functions_idx[f.section] = []
        self.functions[f.section].append(f)
        #self.functions_idx[f.section].append(f.offset)

    def parse_function1(self, l):
        if RE_FUNCTION1.match(l):
            self.look_forward = True
        if l == '':
            if not self.look_forward:
                return
            else:
                self.look_forward = False
                self.stage = S_FUNCTIONS2 
                self.print_stage()         
            
    def parse_detailmap1(self, l):
        if l == '':
            self.stage = S_FUNCTIONS1 
            self.print_stage()         
    
    def parse_detailmap(self, l):
        if RE_DETAILMAP.match(l):
            self.look_forward = True
        if l == '':
            if not self.look_forward:
                return
            else:
                self.look_forward = False
                self.stage = S_DETAILMAP1 
                self.print_stage()         
                
    def parse_section(self, l):
        if RE_SECTION.match(l):
            self.look_forward = True
        if l == '':
            if not self.look_forward:
                return
            else:
                self.look_forward = False
                self.stage = S_DETAILMAP 
                self.print_stage()         
        return
        s = [i for i in l.split(" ") if i != '']
        section = Section()
        section.section, section.offset = parse_secoff(s[0])
        section.length = int(s[1], 16)
        section.name = s[2]
        section.type = s[3]
        return section
        
def map_find(content, modulebase, address):
    m = VCMapParser(content)
    m.parse()
    
    if type(modulebase) != types.IntType:
        modulebase = int(modulebase, 16)
    if type(address) != types.IntType:
        address = int(address, 16)    
    return m.find(address - modulebase)

def delphi_map_find(content, modulebase, address):
    m = DelphiMapParser(content)
    m.parse()
    
    if type(modulebase) != types.IntType:
        modulebase = int(modulebase, 16)
    if type(address) != types.IntType:
        address = int(address, 16)    
    return m.find(address - modulebase)


#def get_map(name, version, loc, base):

if __name__ == '__main__':
    #f = file("serveruifacade.map")
    #content = f.readlines()
    #f.close()    
    #map_find(content, "7e0000", "86e4eb")
    
    from get_map_file import get_map_fileversion, build_index
    build_index()
    content = get_map_fileversion("serveruifacade.dll", "1.0.0.48")    
    #f = file("server.map")
    #content = f.readlines()
    #f.close()    
    #print delphi_map_find(content, "10049bd1", "10000000")
    print map_find(content, "10049bd1", "10000000")