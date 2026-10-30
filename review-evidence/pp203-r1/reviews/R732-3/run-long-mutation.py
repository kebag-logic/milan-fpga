import pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
S=pathlib.Path(sys.argv[1]).resolve(); T=P/'scratch/long-frame'
f=T/'hdl/top/protocol_processor_top.sv'; original=f.read_bytes()
try:
 subprocess.run(['git','apply',str(S/'tb/pp_top/aecp_dispatch_mutations/rbt-last-frame-unwatched.patch')],cwd=T,check=True)
 with (P/'long-mutation-build.log').open('w') as log:
  rc=subprocess.run(['make','-j16','gsi-build','VERILATOR='+str(P/'scratch/simulator-j4.py')],cwd=T/'tb/pp_top',stdout=log,stderr=subprocess.STDOUT).returncode
 (P/'long-mutation-build.rc').write_text(str(rc)+'\n');assert rc==0
 with (P/'long-mutation.log').open('w') as log:
  rc=subprocess.run(['./obj_dir/Vpp_top_sim','--reboot-only'],cwd=T/'tb/pp_top',stdout=log,stderr=subprocess.STDOUT).returncode
 (P/'long-mutation.rc').write_text(str(rc)+'\n')
 s=(P/'long-mutation.log').read_text()
 assert rc!=0 and '[build default,' in s and 'FAIL: HELD-NA request low with non-ADP frame stretched two seconds at EOF' in s
 print('Removed all-producer wait: own probe KILLED; simulation rc',rc)
 print('\n'.join(s.splitlines()[-8:]))
finally:
 f.write_bytes(original)
