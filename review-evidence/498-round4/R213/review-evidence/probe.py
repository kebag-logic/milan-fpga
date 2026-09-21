import ast, collections, json, re, sys
from runner import load, ROOT, TMP
base = '--base' in sys.argv
m=load(base=base,expose=True)
x=m.test_baremetal_profile_contract()
f=x['firmware_source']; docs=x['docs_source']; csr=x['csr_source']; rows=[]
def observe(label,kind,fn,want=None,reason=None):
    try: fn(); result='ACCEPT'; message=''
    except (AssertionError,ValueError) as e: result='REFUSE'; message=str(e)
    rows.append(dict(label=label,kind=kind,result=result,message=message))
    print(label,kind,result,message[:180],flush=True)
    if want: assert result==want, (label,kind,result,message)
    if reason: assert reason in message,(label,kind,message)
def whole(s,listing=None):
    return x['assert_boot_contract'](s,docs,csr,listing=listing)
def pre(s):
    return x['assert_preprocessed_boot_path'](x['blanked'](s),s,x['preprocess_take'](s))
def resolved(s):
    take=x['census_take'](s)
    x['assert_compiled_census_is_clean'](s,taken=take)
    return x['assert_resolved_boot_flow'](take['text'],x['CsrModel'](x['blanked'](s),x['blanked_sv'](csr)),helper='milan_reg')
def body_span(src,name):
    found=re.search(r'\bstatic\s+(?:inline\s+)?(?:void|int|uint64_t)\s+'+name+r'\s*\([^;]*?\)\s*\{',src)
    assert found,name
    start=found.end()-1; depth=1; i=start+1
    # Braces use the gate's comment/string blanking, preserving offsets.
    b=x['blanked'](src)
    while depth:
        depth+=(b[i]=='{')-(b[i]=='}'); i+=1
    return found.start(),start,i-1
def insert(src,name,text):
    _,_,end=body_span(src,name); return src[:end]+text+'\n'+src[end:]
observe('pristine','whole',lambda:whole(f),'ACCEPT')
compiler=x['census_compiler'](); live=bool(x['census_used'].get('target'))
print('COMPILER',compiler,'LIVE',live,flush=True)
examples={
 'conditional_paste': insert(f,'configure_fabric','\n#ifndef MILAN_CENSUS_SOC\n#define REVIEW_JOIN(a,b) a##b\n\tREVIEW_JOIN(milan_,write)(MILAN_ADP_CTRL,1u);\n#endif'),
 'conditional_splice': insert(f,'configure_fabric','\n#ifndef MILAN_CENSUS_SOC\n\tmilan_\\\nwrite(MILAN_ADP_CTRL,1u);\n#endif'),
 'product_selected_splice': insert(f,'configure_fabric','\n#ifdef CSR_UART_BASE\n\tmilan_\\\nwrite(MILAN_ADP_CTRL,1u);\n#endif'),
 'nested_selected_splice': insert(f,'configure_fabric','\n#ifndef MILAN_CENSUS_SOC\n#if 1\n\tmilan_\\\nwrite(0x600u,1u);\n#endif\n#endif'),
 'splice_inside_common_statement':insert(f,'configure_fabric','\n\t(void)(\n#ifndef MILAN_CENSUS_SOC\n\tmilan_\\\nwrite(0x600u,1u),\n#endif\n\t0);'),
 'paste_inside_common_statement':insert(f.replace('static void configure_fabric(void)','#define REVIEW_PASTE(a,b) a##b\nstatic void configure_fabric(void)'),'configure_fabric','\n\t(void)(\n#ifndef MILAN_CENSUS_SOC\n\tREVIEW_PASTE(milan_,write)(0x600u,1u),\n#endif\n\t0);'),
 'dropped_external_statement':insert(f,'configure_fabric','\n#ifndef MILAN_CENSUS_SOC\n\tspiflash_master_cs_write(1u);\n#endif'),
 'conditional_argument':f.replace('milan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);','milan_write(\n#ifndef MILAN_CENSUS_SOC\nMILAN_ADP_CTRL\n#else\nMILAN_CRF_TX_CTRL\n#endif\n, MILAN_CRF_TX_CTRL_BOOT);'),
 'debug_printf':insert(f,'milan_init','\n#ifdef REVIEW_DEBUG_BOOT\n\tprintf("review boot\\n");\n#endif'),
 'plain_splice':insert(f,'configure_fabric','\n\tmilan_\\\nwrite(MILAN_ADP_CTRL,1u);'),
 'paste_outside_boot':f.replace('\tprint_tod(gettime_ns());','\tREVIEW_CAT(print_,tod)(gettime_ns());').replace('#include <stdio.h>','#include <stdio.h>\n#define REVIEW_CAT(a,b) a##b'),
 'extra_private_cast':insert(f.replace('static void configure_fabric(void)','static volatile unsigned int review_scratch;\nstatic void configure_fabric(void)'),'configure_fabric','\t*(volatile unsigned int *)&review_scratch = 9u;'),
 'extra_private_store':insert(f.replace('static void configure_fabric(void)','static volatile uint32_t review_private;\nstatic void review_poke(volatile uint32_t *p) { *p = 11u; }\nstatic void configure_fabric(void)'),'configure_fabric','\treview_poke(&review_private);'),
 'extra_crft_advertise':insert(f,'entity_advertise','\tmilan_write(MILAN_CRF_TX_CTRL,3u);'),
 'extra_caps_advertise':insert(f,'entity_advertise','\tmilan_write(0x614u,0x12345678u);'),
 'extra_crft_command':insert(f,'print_tod','\tmilan_write(0x700u+0x50u,0u);'),
}
a1,_,e1=body_span(f,'parse_u64'); a2,_,e2=body_span(f,'seconds_to_ns')
if a1>a2:a1,a2,e1,e2=a2,a1,e2,e1
examples['reorder_stores']=f[:a1]+f[a2:e2+1]+f[e1+1:a2]+f[a1:e1+1]+f[e2+1:]
for label,s in examples.items():
    assert s!=f,label
    target='REFUSE'
    if label.startswith('extra_crft') or label=='extra_caps_advertise': target='REFUSE' if live and not base else 'ACCEPT'
    observe(label,'whole',lambda s=s:whole(s),target)
    if live and not base:
        if label in ('extra_private_cast','extra_private_store','reorder_stores'):
            observe(label,'resolver',lambda s=s:resolved(s),'ACCEPT')
        elif label.startswith('extra_crft') or label=='extra_caps_advertise':
            observe(label,'resolver',lambda s=s:resolved(s),'REFUSE','resolved boot-word census')
        else:
            observe(label,'preprocessor',lambda s=s:pre(s),'ACCEPT' if label=='paste_outside_boot' else 'REFUSE')
observe('README and notes','whole',lambda:whole(f,('Makefile','milan_baremetal.c','README','notes.txt')),'REFUSE')
if live and not base:
    observe('README and notes','include',lambda:x['assert_include_resolution_is_pinned'](x['include_resolution_planted'](('README','notes.txt'),f)),'ACCEPT')
    observe('shadow command.h','include',lambda:x['assert_include_resolution_is_pinned'](x['include_resolution_planted'](('command.h',),f)),'REFUSE')
    take=x['preprocess_take'](f)
    before='configure_fabric();'; after='load_aem_image();'
    unit=take['text']; assert before in unit and after in unit
    # Swap the ordered boot tokens in the supplied comparison data without changing counts.
    changed=unit.replace('configure_fabric();','REVIEW_PLACEHOLDER();').replace('load_aem_image();','configure_fabric();').replace('REVIEW_PLACEHOLDER();','load_aem_image();')
    assert collections.Counter(re.findall(r'\b(?:configure_fabric|load_aem_image)\b',unit))==collections.Counter(re.findall(r'\b(?:configure_fabric|load_aem_image)\b',changed))
    observe('equal counts but reversed boot tokens','synthetic comparison data',lambda:x['assert_preprocessed_boot_path'](x['blanked'](f),f,dict(take,text=changed)),'REFUSE')
else: print('SKIP instrument-only probes: '+('validation base has no added instruments' if base else 'no RV32 compiler'),flush=True)
(TMP/('probe-'+('base-' if base else '')+sys.argv[1]+'.json')).write_text(json.dumps(rows,indent=2))
