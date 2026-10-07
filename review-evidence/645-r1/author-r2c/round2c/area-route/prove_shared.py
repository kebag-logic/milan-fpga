"""Exhaustively compare shared band-detector LUT functions over all 16 error bits."""
from pathlib import Path
import functools, hashlib, json, re, sys
area=Path(sys.argv[1])
route=Path(sys.argv[2])
assignments=1<<16
mask=(1<<assignments)-1
variables=[(mask//((1<<(1<<i))+1))<<(1<<i) for i in range(16)]

def evaluator(path, invert_cell=None):
    rows={}
    for line in path.read_text().splitlines():
        name,kind,init,terms=line.split('\t')
        rows[name]=(kind,init,dict(term.split('=',1) for term in terms.split(';') if term))
    def lut(init,args):
        if not args: return mask if init&1 else 0
        half=1<<(len(args)-1)
        lo=lut(init & ((1<<half)-1),args[:-1])
        hi=lut(init>>half,args[:-1])
        return ((mask^args[-1]) & lo) | (args[-1] & hi)
    @functools.lru_cache(None)
    def value(driver):
        match=re.fullmatch(r'milan_datapath/media_grid_align/err_r_reg\[([0-9]+)\]/Q',driver)
        if match:
            i=int(match[1]); assert 0<=i<16
            return variables[i]
        name,pin=driver.rsplit('/',1)
        if name not in rows: raise ValueError('Unsupported leaf: '+driver)
        kind,init,inputs=rows[name]
        if kind=='GND': return 0
        if kind=='VCC': return mask
        if kind.startswith('LUT'):
            n=5 if kind=='LUT6_2' and pin=='O5' else int(kind[3])
            bits=int(init.split("'h",1)[1],16)
            if name==invert_cell: bits ^= (1<<(1<<n))-1
            return lut(bits,[value(inputs['I'+str(i)]) for i in range(n)])
        if kind=='CARRY4':
            match=re.fullmatch(r'(CO|O)\[([0-3])\]',pin)
            if not match: raise ValueError('Unknown carry output: '+driver)
            carry=value(inputs['CI']) | value(inputs['CYINIT'])
            for i in range(int(match[2])+1):
                select=value(inputs['S['+str(i)+']'])
                out=select ^ carry
                carry=(select & carry) | ((mask^select) & value(inputs['DI['+str(i)+']']))
            return carry if match[1]=='CO' else out
        raise ValueError('Unsupported primitive: '+kind)
    return value
base=evaluator(area/'base.shared_logic.tsv')
head=evaluator(area/'head.shared_logic.tsv')
results=[]
for i in range(6,16):
    name='milan_datapath/media_grid_align/src_band_ticks_r[0]_i_'+str(i)
    a=base(name+'/O'); b=head(name+'/O')
    results.append({'cell':name,'assignments':assignments,'identical':a==b,
                    'base_sha256':hashlib.sha256(a.to_bytes(assignments//8,'little')).hexdigest(),
                    'head_sha256':hashlib.sha256(b.to_bytes(assignments//8,'little')).hexdigest()})
matched=[row['cell'] for row in results if row['identical']]
control=None
if matched:
    mutated=evaluator(area/'head.shared_logic.tsv',invert_cell=matched[0])
    control={'cell':matched[0],'change':'invert all LUT INIT output bits','caught':base(matched[0]+'/O')!=mutated(matched[0]+'/O')}
    assert control['caught']
result={'negative_control':control,'method':'Complete truth tables over registered err_r[15:0], LUT INIT and CARRY4 primitive equations; unsupported leaves fail closed','cells':results,'identical_count':sum(row['identical'] for row in results)}
(route/'shared_logic_equivalence.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
