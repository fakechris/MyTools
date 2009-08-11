import os
p = "D:\\work\\test\\SCS\\code\\delphicode"

for dirpath, dirname, filelist in os.walk(p):	
	if dirpath.endswith("CVS"):
		continue

	filelist = [f for f in filelist if f.endswith(".cpp")
		or f.endswith(".h")
		or f.endswith(".rc")
		or f.endswith(".rc2")
		or f.endswith(".pas")
		or f.endswith(".dfm")
		or f.endswith(".dpr")		
		or f.endswith(".dsp")
		or f.endswith(".dsw")
		or f.endswith(".vcproj")
		or f.endswith(".sln")
		or f.endswith(".bat")
		or f.endswith(".cfg")
		or f.endswith(".manifest")
		or f.endswith("README")
		or f.endswith(".txt")]

	for f in filelist:
		pf = dirpath + "\\" + f
		#print pf
		fi = file(pf, "r+b")
		r = fi.read()		
		fi.close()
		#import pdb; pdb.set_trace()
		if r.find("\r\r\n") >= 0:
			print dirpath + "\\" + f
			r = r.replace("\r\r\n", "\r\n")	
			fi = file(pf, "w+b")
			fi.write(r)
			fi.close()			
	#print dirpath, dirname, filelist

"""
p = "D:\\work\\tag\\code\\scs_driver\\Realdisk\\RealDiskTest_mfc"
for f in os.listdir(p):
	if f == "CVS":
		continue
	if f == "res":
		continue
	if f.endswith(".ico"):
		continue
	fp = p + "\\" + f
	#import pdb; pdb.set_trace()
	fi = file(fp, "r")	
	r = fi.read()
	fi.close()
	r.replace("\r\r\n", "\r\n")	
	fi = file(fp, "w+b")
	fi.write(r)
	fi.close()
"""	