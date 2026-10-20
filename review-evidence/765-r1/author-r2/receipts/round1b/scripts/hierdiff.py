import sys
def parse(p):
    d={}
    for line in open(p):
        if not line.startswith('|'): continue
        cols=[c.strip() for c in line.strip().strip('|').split('|')]
        if len(cols)<7 or not cols[2].isdigit(): continue
        name=line.split('|')[1]; depth=len(name)-len(name.lstrip())
        d[(depth,name.strip(),cols[1])]=(int(cols[2]), int(cols[6]) if cols[6].isdigit() else 0)
    return d
b=parse(sys.argv[1]); c=parse(sys.argv[2])
print("| LUT delta | depth | instance | module | LUT base -> cand | FF base -> cand |")
print("|---:|---:|---|---|---|---|")
rows=[]
for k in set(b)|set(c):
    lb,fb=b.get(k,(0,0)); lc,fc=c.get(k,(0,0)); rows.append((lc-lb,k,lb,lc,fb,fc))
for d,k,lb,lc,fb,fc in sorted(rows,key=lambda r:(-abs(r[0]),r[1])):
    if abs(d)>=10 or k[1] in ("avtp_rx_monitor","crf_rx"):
        print(f"| {d:+d} | {k[0]} | `{k[1]}` | `{k[2]}` | {lb} -> {lc} | {fb} -> {fc} |")
