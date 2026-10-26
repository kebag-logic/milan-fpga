#!/usr/bin/env python3
"""Plant a real wrapper port and a G-to-wire source consumer in disposable elaborations."""
import concurrent.futures,dataclasses,multiprocessing,os,pathlib,sys
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parent
os.environ['TMPDIR']=str(packet/'scratch')
os.environ['SV2V']='$VALIDATION_TOOLS/sv2v-v0.0.12/sv2v'
sys.path.insert(0,str(root/'sw/mailbox'))
import publication_census as pc
from census_elab import RECIPE,WORK
src=pc.load(pc.DATAPATH,pc.WRAPPER_SV)
known=pc.fields(pc.mailbox_model.load())
def once(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new)
port=dataclasses.replace(src,
    wrapper=once(src.wrapper,'    input  wire        clk_i,','    input wire review_unmapped_i,\n    input  wire        clk_i,'),
    datapath=once(src.datapath,') pp_shadow (',") pp_shadow (\n      .review_unmapped_i(1'b0),"))
wire=dataclasses.replace(src,datapath=once(src.datapath,'.vlan_en_i  (crft_class_a_w),',
                                             '.vlan_en_i  (crft_class_a_w | pp_rdata_w[0]),'))
def check(item):
    name,source,needle=item
    out,sv=pc.census(source,pc.CENSUS,known,pc.Plan(at=(RECIPE,),jobs=1))
    result='\n'.join(out)
    assert needle in result,(name,result)
    return name+'\n'+result+'\nPASS: rejected the planted source defect\n'
WORK.roms()
with concurrent.futures.ProcessPoolExecutor(max_workers=2,mp_context=multiprocessing.get_context('fork')) as pool:
    results=list(pool.map(check,[('unmapped wrapper port',port,'unmapped port: review_unmapped_i'),
                               ('G consumer on the wire',wire,'G port host_rdata_o reaches the wire')]))
text='\n'.join(results)
(packet/'census-source-probes.log').write_text(text)
print(text)
