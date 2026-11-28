import os,sys,time
log='$MANAGEMENT/2026-09-23/disk-cleanup.log'
def audit(event,args):
 if event not in ('os.remove','os.rmdir','shutil.rmtree'):return
 path=args[0]
 if isinstance(path,int):return
 path=os.fsdecode(path)
 if not os.path.isabs(path):
  fd=args[1] if event in ('os.remove','os.rmdir') and len(args)>1 else -1
  base=os.readlink('/proc/self/fd/'+str(fd)) if fd not in (None,-1) else os.getcwd()
  path=os.path.join(base,path)
 with open(log,'a') as f:
  f.write(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+' [A855 r7] BEFORE '+event+' '+os.path.abspath(path)+'\n')
  f.flush();os.fsync(f.fileno())
sys.addaudithook(audit)
