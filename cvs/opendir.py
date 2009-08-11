import os, re, sys

RE_GAMEDIR = re.compile("(.+)_idc_game_(\d+)")
gamelist = os.listdir("i:\\SCSNT\\game_data")

def is_match(dirname, ids):
    m = RE_GAMEDIR.match(dirname)
    if m and m.groups()[1] in ids:
        return True
    return False

def get_dir_from_idlist(ids):    
    global gamelist
    dirlist = [g for g in gamelist if is_match(g, ids)]
    return dirlist

if len(sys.argv) < 2:
    print "usage opend.py <gameids>"
    print "usage opend.py 1,2,3 or opend.py 2"
    sys.exit(0)

#print sys.argv[1]

idlist = sys.argv[1].split(",")
for d in get_dir_from_idlist(idlist):
    os.system("""start %s""" % ("i:\\SCSNT\\game_data\\" + d))
    
"""
for g in gamelist:
    m = RE_GAMEDIR.match(g)
    if m:
        gid = m.groups()[1]
        if gid == sys.argv[1]:
            os.system("start %s" % ("i:\\SCSNT\\game_data\\" + g))
            sys.exit(0)
        
"""        