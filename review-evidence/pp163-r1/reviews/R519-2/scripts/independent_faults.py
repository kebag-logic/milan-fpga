#!/usr/bin/env python3
"""Reviewer-owned clock, cancellation and capacity faults on isolated copies."""
import concurrent.futures, difflib, importlib.util, json, os, pathlib, sys, tempfile
sys.dont_write_bytecode = True
src=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve()
os.environ['TMPDIR']=str(p/'scratch/tmp');os.environ['MAKEFLAGS']='-j16';tempfile.tempdir=str(p/'scratch/tmp')
spec=importlib.util.spec_from_file_location('notify_review',src/'tb/pp_top/notify_mutants.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
T='hdl/top/protocol_processor_top.sv';N='hdl/aecp/KL_aecp_notify.sv'
faults=[
 m.Mutant('review-two-withdraw-stages',m.WITHDRAW,((T,"  logic [7:0]              org_withdraw_mask_r;\n","  logic [7:0]              org_withdraw_mask_r;\n  logic [7:0] review_delay;\n  always_ff @(posedge clk_i) begin\n    if (!rst_n) review_delay <= '0;\n    else review_delay <= org_withdraw_slot_mask_w;\n  end\n"),(T,"else        org_withdraw_mask_r <= org_withdraw_slot_mask_w;","else        org_withdraw_mask_r <= review_delay;")),('WD2:','WD3:')),
 m.Mutant('review-command-cancel-missing',m.INDEX,((N,"    assign cx_ok_w   = ca_cancel_ok_w\n","    assign cx_ok_w   = 1'b0\n"),),('CX1:',)),
 m.Mutant('review-second-cancel-lost',m.INTERFACES,((N,'        cx_pend_r <= cx_work_w;\n',"        cx_pend_r <= '0;\n"),),('CA1:','CA1b:')),
 m.Mutant('review-port-one-capacity-missing',m.INTERFACES,((N,"    assign wk_port_ok_w = (PORT_W_C'(wk_ix_r) == hold_port_r);\n","    assign wk_port_ok_w = (PORT_W_C'(wk_ix_r) == hold_port_r) && !hold_port_r;\n"),),('PD1:',))]
faults.append(m.Mutant('review-abort-bypasses-stage',m.WITHDRAW,((T,'  assign arb_start_abort_w = org_withdraw_mask_r[ser_slot_w]','  assign arb_start_abort_w = org_withdraw_slot_mask_w[ser_slot_w]'),),('WD1:',)))
if len(sys.argv)>3: faults=[f for f in faults if f.name in sys.argv[3:]]
out=p/('receipts/independent-faults-extra' if len(sys.argv)>3 else 'receipts/independent-faults');out.mkdir(exist_ok=True)
for f in faults:
    texts={}
    for path,old,new in f.edits:
        text=texts.get(path,(src/path).read_text());assert text.count(old)==1;texts[path]=text.replace(old,new,1)
    diff=''.join(''.join(difflib.unified_diff((src/path).read_text().splitlines(True),text.splitlines(True),fromfile='a/'+path,tofile='b/'+path)) for path,text in texts.items())
    (out/(f.name+'.patch')).write_text(diff)
work=(src,out,str(p/'scripts/simulator.py'))
with concurrent.futures.ThreadPoolExecutor(2) as pool: golden=list(pool.map(lambda f:m.judge(f,work),m.goldens(faults)))
assert all(x['verdict']=='PASS' for x in golden)
with concurrent.futures.ThreadPoolExecutor(2) as pool: results=list(pool.map(lambda f:m.judge(f,work),faults))
(out/'results.json').write_text(json.dumps(golden+results,indent=2)+'\n')
for x in golden+results:print(json.dumps(x),flush=True)
raise SystemExit(0 if all(x['verdict']=='KILLED' for x in results) else 1)
