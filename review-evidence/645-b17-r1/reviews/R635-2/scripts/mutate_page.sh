#!/bin/sh
# usage: mutate_page.sh <author-packet> <page.md> <workdir>  -- each mutant: one sed edit on a copy, checker rc recorded
A=$1; PG=$2; M=$3; i=0
while IFS='	' read -r name from to; do
  i=$((i+1)); cp "$PG" "$M/m$i.md"
  python3 -I -c "import sys;p,f,t=sys.argv[1:];s=open(p).read();assert s.count(f)>=1,f;open(p,'w').write(s.replace(f,t,1))" "$M/m$i.md" "$from" "$to" || { echo "$name: PATTERN-MISSING"; continue; }
  (cd "$M" && python3 -I "$A/tools/check_b17_page.py" "$A" "$M/m$i.md" >"$M/m$i.log" 2>&1); rc=$?
  echo "$name: rc=$rc $(tail -1 "$M/m$i.log")"
done <<'LIST'
c09 last poll 31.78->31.79	80, -8.00 to +31.78	80, -8.00 to +31.79
c08 slip 1.17->1.18	1.17 to 1.94, +2 dups, 0 skips	1.18 to 1.94, +2 dups, 0 skips
priming table after-slip peak last poll 30.1->30.2	| To the last poll | 27.1 to 30.1 us |	| To the last poll | 27.1 to 30.2 us |
priming table bursts to last poll 9 to 19->9 to 18	| To the last poll | 9 to 19 |	| To the last poll | 9 to 18 |
prose last-poll range 31.93->31.94	+31.75 to +31.93 s after the bind	+31.75 to +31.94 s after the bind
prose end baseline 228->229	the end baseline, 228.	the end baseline, 229.
prose converged 0.64 to 0.67->0.64 to 0.68	by 0.64 to 0.67 s	by 0.64 to 0.68 s
prose further bursts 2 to 7->2 to 8	The 2 to 7	The 2 to 8
prose long polls 0.27 to 0.43->0.27 to 0.44	took 0.27 to 0.43 s	took 0.27 to 0.44 s
prose after-slip peak up to 30.1->30.2	up to 30.1 us, left	up to 30.2 us, left
LIST
