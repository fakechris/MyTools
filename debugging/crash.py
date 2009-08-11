#!c:\python25\python.exe
import os, sys, subprocess, re, shutil

#C:\crash\cdb\cdb.exe -lines -y x:\2.0.1.41\artifacts\pdb -i x:\2.0.1.41\artifacts\root_server\bin_server;x:\2.0.1.41\artifacts\root_server\bin_client -z C:\crash\2.0.1.41\out\transcoredll\asio_connection.h.516\scs9d.090311175836_468.dmp -c ".ecxr; kv; Q"

#COMMAND_LINE = r"""C:\crash\cdb\cdb.exe -lines -y z:\%s\artifacts\pdb -i z:\%s\artifacts\root_server\bin_server;z:\%s\artifacts\root_server\bin_client -z %s -c ".ecxr; kv; Q"  > %s """
COMMAND_LINE = r"""C:\crash\cdb\cdb.exe -lines -y z:\%s\artifacts\pdb -i z:\%s\artifacts\root_server\bin_server;z:\%s\artifacts\root_server\bin_client -z %s -c ".ecxr; lm; kv; Q"  """

r = re.compile("(ChildEBP RetAddr  Args to Child.*)quit:", re.M|re.S)
r1 = re.compile(" ([a-zA-Z-_]+)!", re.M|re.S)
r2 = re.compile(r"d:\\luntbuild_new\\([^\]]+)\\([^\\\[\]]+) @ (\d+)\]", re.M|re.S)
#r3 = re.compile(r"\\([^\\\[\]]+) @ (\d+)\]", re.M|re.S)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		version = "2.0.1.39"
	else:
		version = sys.argv[1]
	
	input_dir = "c:\\crash\\" + version + "\\"	
	output_dir = "c:\\crash\\" + version + "\\out\\"
	failed_dir = "c:\\crash\\" + version + "\\failed\\"
	all_dmp_files = os.listdir(input_dir)
	try:
		os.mkdir(output_dir)
		os.mkdir(failed_dir)
	except:
		pass
			
	ef = file(failed_dir + "failed.txt", "w")
	for f in all_dmp_files:
		if f == "out" or f == "failed":
			continue
		is_server = False
		is_client = False
		
		#cmd = COMMAND_LINE % (version, version, version, input_dir+f, output_dir+f+".txt")
		cmd = COMMAND_LINE % (version, version, version, input_dir+f)
		#print cmd
		#import pdb; pdb.set_trace()
		#os.system(cmd)	
		outbuf = os.popen(cmd).read()
		outbuf.replace("\n", "\r\n")
		
		lb = outbuf.lower()
		if lb.find("scs_svc") > 0:
			is_server = True
		if lb.find("scs_client") > 0:
			is_client = True			
		
		m = r.search(outbuf)
		#print m.group(1)
		if not m:
			#print "failed parse ", f
			ef.write(f+"\r\n")
			ef.flush()		
			shutil.move(input_dir+f, failed_dir)
			continue
						
		final_output_path = output_dir
		
		# todo: skip ntdll		
		m1 = r1.search(m.group(1))
		if m1:
			sub_dir = m1.group(1)
			if sub_dir:			
				final_output_path = output_dir+sub_dir+"\\"
				try:
					os.mkdir(final_output_path)
				except:
					pass
					
				m2 = r2.search(m.group(1))
				if m2:
					sub_dir2 = m2.group(2) + "." + m2.group(3)
					final_output_path += sub_dir2+"\\"
					try:
						os.mkdir(final_output_path)
					except:
						pass
					print "process", is_server, is_client, sub_dir, sub_dir2
				else:
					print "process", is_server, is_client, sub_dir
					
		if is_server:
			final_output_path += "server\\"
			try:
				os.mkdir(final_output_path)
			except:
				pass
		if is_client:
			final_output_path += "client\\"
			try:
				os.mkdir(final_output_path)
			except:
				pass
				
		ff = file(final_output_path+f+".txt", "w")
		shutil.move(input_dir+f, final_output_path)
			
		ff.write(m.group(1))
		ff.close()
		#sys.exit(0)
		#p = subprocess.Popen(cmd, shell=True)
		#sts = os.waitpid(p.pid, 0)
		