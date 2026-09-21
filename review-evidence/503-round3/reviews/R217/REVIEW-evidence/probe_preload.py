import importlib.util,json,os,shutil,sys,subprocess,re
from pathlib import Path
scratch=Path(os.environ['REVIEW_SCRATCH']);ev=Path(os.environ['EVIDENCE_ROOT'])/'design-evidence/500-materialization/proposal-evidence'
spec=importlib.util.spec_from_file_location('r217_d3',ev/'run.py');r=importlib.util.module_from_spec(spec);sys.modules[spec.name]=r;spec.loader.exec_module(r)
h=scratch/'probe-harness';shutil.copytree(r.HARNESS,h,dirs_exist_ok=True);r.HARNESS=h;r.STUBS=h/'stubs'
f=h/'d3_top.sv';s=f.read_text();s=s.replace('    input  wire         prog_busy_i,','    input  wire         reviewer_pre_ready_i,\n    input  wire         prog_busy_i,')
assert s.count(".pre_ready_i      (1'b1)")==1
s=s.replace(".pre_ready_i      (1'b1)",'.pre_ready_i      (reviewer_pre_ready_w)')
s=s.replace('assign pre_take_o         = pre_valid_w;','assign pre_take_o         = pre_valid_w && reviewer_pre_ready_w;')
# The pinned suite already drives this exact listener backpressure lever.
wrap=(r.ROOT/'protocol-processor/tb/acmp_nvm/acmp_nvm_wrap.sv').read_text()
listener=wrap[wrap.index('  KL_pp_acmp_listener #('):wrap.index('  // ---- observability mirrors')]
rom=scratch/'ltn_rom.hex'
subprocess.run(['python3','-B',str(r.PP/'acmp/rom/gen_ltn_rom.py'),'-o',str(rom)],check=True)
replace={'N_SINKS_P (N_SINKS_P)':'N_SINKS_P (N_STREAM_IN_P)',
 'TROM_HEX_P(TROM_HEX_P)':'TROM_HEX_P("'+str(rom)+'")',
 'ENTITY_ID_C':"64'h0011223344556677",'pp_txn_t': 'pp_pkg::pp_txn_t',
 'evt_block_i':'!reviewer_pre_ready_i','pre_talker_eid_w':'pre_teid_nc_w',
 'pre_talker_uid_w':'pre_uid_nc_w','pre_ctlr_eid_w':'pre_ceid_nc_w',
 'pre_sw_w':'pre_sw_nc_w','pre_started_w':'pre_started_nc_w','pre_ready_w':'reviewer_pre_ready_w'}
for old,new in replace.items():listener=listener.replace(old,new)
listener=re.sub(r'\((lsn_\w+)\)', '()',listener)
s=s.replace('endmodule', '  logic reviewer_pre_ready_w;\n'+listener+'\nendmodule');f.write_text(s)
r.DONOR_SV.insert(0,r.PP/'common/pp_pkg.sv')
r.DONOR_SV.append(r.PP/'acmp/KL_pp_acmp_listener.sv')
r.SOURCES['top']=(f,'d3_top.sv')
f=h/'d3_bridge.cpp';s=f.read_text();needle='static void drive_ucpu() {';assert s.count(needle)==1
s=s.replace(needle,needle+'''\n  const char *pr = std::getenv("R217_PRELOAD_RELEASE");
  dut->reviewer_pre_ready_i = !pr || (cyc >= std::strtoull(pr, nullptr, 10));
''')
f.write_text(s)
f=h/'d3_cases.cpp';s=f.read_text();needle='  cases["V10_blank_first_boot"] = [] {';assert s.count(needle)==1
addition='''  cases["R217_preload"] = [] {
    boot(); idle(200); snap("terminal");
    read_row(SEL_PTOF, 0, "post.ptof0");
    idle(2000); snap("observed");
  };
  cases["R217_descriptor_boundary"] = [] {
    desc_delay_after_apply = std::stoll(variant);
    boot(); idle(200); snap("terminal");
    command_after_recovery(); snap("recovered");
  };
'''
f.write_text(s.replace(needle,addition+needle))
s=r.prep_shape('1x1');b=r.do_build(r.Build('reviewer-adjacent','1x1'),s,8)
seed=scratch/'d3/runs/base-1x1/V1a_set_everything';slots=(seed/'cut-slotA.bin',seed/'cut-slotB.bin')
results=[]
for name,release in [('control',None),('held','999999999'),('finite','100000')]:
 if release is None:os.environ.pop('R217_PRELOAD_RELEASE',None)
 else:os.environ['R217_PRELOAD_RELEASE']=release
 result=r.run_case(b,s,'R217_preload',name,slots)
 d={'variant':name,'rc':result.rc,'done':result.done,'obs':result.obs,'events':result.evts};results.append(d)
 print(json.dumps(d),flush=True)
os.environ.pop('R217_PRELOAD_RELEASE',None)
for delay in [4094,4095,4096,4097,24090,24098,24100]:
 result=r.run_case(b,s,'R217_descriptor_boundary',str(delay),slots)
 d={'variant':str(delay),'rc':result.rc,'done':result.done,'obs':result.obs,'events':result.evts};results.append(d)
 print(json.dumps(d),flush=True)
(scratch/'adjacent-probes.json').write_text(json.dumps(results,indent=2))
