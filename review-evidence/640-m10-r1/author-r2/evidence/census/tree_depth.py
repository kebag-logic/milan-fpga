import re,sys
lines=open(sys.argv[1],encoding='utf-8').read().splitlines()
maxd=int(sys.argv[2]); only=sys.argv[3:] 
cur=None
for l in lines[1:]:
    m=re.match(r'^((?:│    |     )*)(├── |└── )(.*)$',l)
    if not m:
        continue
    d=len(m.group(1))//5
    if d==0: cur=m.group(3).split()[0]
    if only and cur not in only: continue
    if d<=maxd: print('  '*d+m.group(3))
