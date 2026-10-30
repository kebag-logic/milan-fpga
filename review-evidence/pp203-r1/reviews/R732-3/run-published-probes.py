import pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
S=pathlib.Path(sys.argv[1]).resolve()
T=P/'scratch/reboot-control'; f=T/'tb/pp_top/sim_main.cpp'
original=subprocess.check_output(['git','-C',str(S),'show','HEAD:tb/pp_top/sim_main.cpp'])
patches=[('prior-window','reviews/R731-1/probes/window-after-notification-round.patch'),('prior-post-departure','reviews/R732-2/post-departure-probe.patch'),('prior-nonadvertising','reviews/R732-2/nonadvertising-probe.patch')]
for name,patch in patches:
 if len(sys.argv)>2 and name!=sys.argv[2]: continue
 f.write_bytes(original)
 with (P/(name+'-apply.log')).open('w') as log:
  rc=subprocess.run(['patch','-p1','--batch','-i',str(P/'public'/patch)],cwd=T,stdout=log,stderr=subprocess.STDOUT).returncode
 (P/(name+'-apply.rc')).write_text(str(rc)+'\n')
 if rc!=0 and name=='prior-nonadvertising':
  # The unchanged patch's body applied; new test calls moved its call-site context.
  s=f.read_text()
  assert '  void nonadvertising_pending_frame_probe()' in s
  assert '    nonadvertising_pending_frame_probe();' not in s
  s=s.replace('    every_slot_taken_at_the_shutdown();','    every_slot_taken_at_the_shutdown();\n    nonadvertising_pending_frame_probe();',1)
  f.write_text(s)
  (P/(name+'-context-adaptation.txt')).write_text('Original patch retained byte-for-byte. Its method hunk applied unchanged. Only the call insertion context moved around the new RBT12/RBT13 calls; inserted the exact original call after every_slot_taken_at_the_shutdown(). No probe logic or assertion changed.\n')
 elif rc!=0: raise RuntimeError(name)
 cmd=['make','-j16','gsi-build','VERILATOR='+str(P/'scratch/bounded-simulator.py')]
 with (P/(name+'-build.log')).open('w') as log: rc=subprocess.run(cmd,cwd=f.parent,stdout=log,stderr=subprocess.STDOUT).returncode
 (P/(name+'-build.rc')).write_text(str(rc)+'\n'); assert rc==0
 with (P/(name+'.log')).open('w') as log: rc=subprocess.run(['./obj_dir/Vpp_top_sim','--reboot-only'],cwd=f.parent,stdout=log,stderr=subprocess.STDOUT).returncode
 (P/(name+'.rc')).write_text(str(rc)+'\n')
 print(name,rc,flush=True)
 print('\n'.join((P/(name+'.log')).read_text().splitlines()[-4:]),flush=True)
 assert rc==0
f.write_bytes(original)
