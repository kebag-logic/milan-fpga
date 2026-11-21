#!/usr/bin/env python3
"""Exercise the padded-tail boundary through the real parser and monitor."""
import os,pathlib,shlex,subprocess,sys
p=pathlib.Path(__file__).resolve().parent;r=pathlib.Path(sys.argv[1]).resolve();suite=r/'tb/verilator/avtp_rxmon'
s=(suite/'sim_fanout.cpp').read_text().replace('kPayloadBytes = 192','kPayloadBytes = 65')
for call in ['three_inputs_on_one_stream','unbinding_one_leaves_the_others_receiving','each_input_judges_the_pdu_on_its_own','two_streams_back_to_back','all_eight_inputs_on_one_stream','a_pdu_no_input_accepts_then_one_they_do','a_frame_ending_on_its_match_beat_then_a_full_one','a_burst_of_frames_ending_on_their_match_beat_to_eight_inputs','a_dense_burst_to_eight_inputs_overflows_the_store']:
 s=s.replace('        '+call+'();','')
f=p/'scratch/stack_tail.cpp';f.write_text(s)
v=os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
cmd=shlex.split(subprocess.check_output(['make','-n','fanout-build','FO_MDIR='+str(p/'scratch/obj_stack_tail'),'VERILATOR='+v],cwd=suite,text=True).strip())
cmd=[str(f) if x=='sim_fanout.cpp' else x for x in cmd]
for i in range(len(cmd)-1):
 if cmd[i]=='-j':cmd[i+1]='4'
with (p/'scratch/stack-tail-build.log').open('w') as log:b=subprocess.run(cmd,cwd=suite,stdout=log,stderr=subprocess.STDOUT)
if b.returncode:sys.exit(b.returncode)
with (p/'stack-tail.log').open('w') as log:b=subprocess.run([str(p/'scratch/obj_stack_tail/Vavtp_rxmon_fanout')],cwd=suite,stdout=log,stderr=subprocess.STDOUT)
(p/'stack-tail.rc').write_text(str(b.returncode)+'\n');print((p/'stack-tail.log').read_text());sys.exit(b.returncode)
