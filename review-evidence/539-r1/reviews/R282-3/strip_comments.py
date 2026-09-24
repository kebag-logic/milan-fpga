#!/usr/bin/env python3
"""Strip SystemVerilog // and /* */ comments (string-literal aware) and trailing whitespace; print result."""
import sys
def strip(s):
    out=[];i=0;n=len(s);ins=False
    while i<n:
        c=s[i]
        if ins:
            out.append(c)
            if c=='\\' and i+1<n: out.append(s[i+1]); i+=2; continue
            if c=='"': ins=False
            i+=1; continue
        if c=='"': ins=True; out.append(c); i+=1; continue
        if s.startswith('//',i):
            j=s.find('\n',i); i=n if j<0 else j; continue
        if s.startswith('/*',i):
            j=s.find('*/',i+2); i=n if j<0 else j+2; continue
        out.append(c); i+=1
    return '\n'.join(l.rstrip() for l in ''.join(out).split('\n'))
sys.stdout.write(strip(sys.stdin.read()))
