#!/usr/bin/python

import sys, os

if len(sys.argv) < 3:
	print "Usage: %s [REPOS] [TXN]" % sys.argv[0]
	sys.exit(1)
	
repos = sys.argv[1]
txn = sys.argv[2]

svnlook = '/usr/local/bin/svnlook'

author = os.popen("%s author -t %s %s" % (svnlook, txn, repos)).read().strip()
log = os.popen("%s log -t %s %s" % (svnlook, txn, repos)).read().strip()

if log == "":
	print "\nHello, %s.  Empty commit log is not permitted!\n" % author
	sys.exit(2)
	
sys.exit(0)
	