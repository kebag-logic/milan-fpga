#!/usr/bin/env python3
"""Compare changed helper semantics with the main-base implementation."""
import argparse, pathlib, subprocess
p=argparse.ArgumentParser(); p.add_argument('source',type=pathlib.Path); p.add_argument('packet',type=pathlib.Path); a=p.parse_args()
src,out=a.source.resolve(),a.packet.resolve(); work=out/'scratch/helper-equivalence'; work.mkdir(exist_ok=True)
base=subprocess.check_output(['git','show','c3bff8f3dea03870ea7ae62965db360b509ee3b3:src/acmp.c'],cwd=src,text=True)
def extract(name):
    pos=base.index(' '+name+'('); start=base.rfind('\nstatic ',0,pos)+1; end=base.index('\n}',pos)+2
    return base[start:end].replace(name+'(', 'ref_'+name+'(')
code='#include "'+str(src/'src/acmp.c')+'"\n#include <stdio.h>\n'
code+='\n'.join(extract(n) for n in ['view_of','view_equal','record_of','same_record'])
code+='''
static uint32_t rng=0x9197345u;
static uint32_t draw(void) { rng^=rng<<13; rng^=rng>>17; rng^=rng<<5; return rng; }
static uint64_t draw64(void) { return ((uint64_t)draw()<<32)|draw(); }
int main(void) {
    unsigned checks=0;
    for(unsigned n=0;n<100000u;++n) {
        struct acmp_sink s={0};
        s.state=(enum acmp_sink_state)(draw()%8u); s.bound=draw()%2u; s.started=draw()%2u;
        s.binding.talker_entity_id=draw64(); s.binding.controller_entity_id=draw64();
        s.binding.talker_unique_id=(uint16_t)draw(); s.binding.streaming_wait=draw()%2u;
        s.stream.stream_id=draw64(); s.stream.dest_mac=draw64(); s.stream.vlan_id=(uint16_t)draw();
        s.probing=draw()%4u; s.acmp_status=(uint8_t)draw(); s.tk_failed=draw()%2u; s.discovered=draw()%2u;
        uint8_t record[20]; ref_record_of(&s,record); memcpy(s.saved,record,20);
        if(record_moved(&s)) return 1;
        for(unsigned byte=0;byte<20u;++byte) {
            s.saved[byte]^=(uint8_t)(1u<<(n%8u));
            if(record_moved(&s)==ref_same_record(record,s.saved)) return 2;
            s.saved[byte]=record[byte]; ++checks;
        }
        struct acmp_sink_view x,y,z;
        ref_view_of(&s,&x); view_of(&s,&z);
        if(memcmp(&x,&z,sizeof x)!=0) return 3;
        if(view_moved(&s,&x)) return 4;
        y=x;
        switch(n%10u) {
        case 0:y.stream.stream_id^=1ull<<(n%64u);break;
        case 1:y.stream.dest_mac^=1ull<<(n%64u);break;
        case 2:y.stream.vlan_id^=1u<<(n%16u);break;
        case 3:y.probing_status=(enum acmp_probing)(draw()%4u);break;
        case 4:y.acmp_status^=1u;break;
        case 5:y.bound=!y.bound;break;
        case 6:y.started=!y.started;break;
        case 7:y.talker_registered=!y.talker_registered;break;
        case 8:y.registering_failed=!y.registering_failed;break;
        case 9:y.talker_discovered=!y.talker_discovered;break;
        }
        if(view_moved(&s,&y)==ref_view_equal(&x,&y)) return 5;
    }
    printf("PASS 100000 seeded sink states; %u single-bit saved-record changes; base/head view construction and notification predicates agree\\n",checks);
    return 0;
}
'''
(work/'compare.c').write_text(code)
rec=out/'receipts/helper-equivalence.log'
with rec.open('w') as log:
    r=subprocess.run(['gcc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=undefined,address','-fno-sanitize-recover=all','-I'+str(src/'include'),str(work/'compare.c'),'-o',str(work/'compare')],stdout=log,stderr=subprocess.STDOUT)
    if r.returncode==0: r=subprocess.run([str(work/'compare')],stdout=log,stderr=subprocess.STDOUT)
(out/'receipts/helper-equivalence.rc').write_text(str(r.returncode)+'\n')
print(rec.read_text()); raise SystemExit(r.returncode)
