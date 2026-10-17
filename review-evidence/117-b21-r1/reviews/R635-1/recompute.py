#!/usr/bin/env python3
"""Offline media audit. Inputs: public evidence author directory, retained raw directory, output.

Only named media, timing and decoder products are read from the raw directory.
Raw filenames are matched by published size and hash; equipment names are never printed.
The output directory must be disposable scratch. No hardware or network access.
"""
import concurrent.futures as cf
import hashlib
import json
import struct
import sys
from pathlib import Path

import numpy as np

E, RAW, OUT = map(Path, sys.argv[1:4])
OUT.mkdir(parents=True, exist_ok=True)
PK = np.dtype([('ns','<i8'),('seq','u1'),('ts','<u4'),('flags','u1'),('sdl','<u2')])
PS = struct.Struct('<qBIBH')
EXPECTED = {
 'dA-dut': ('dA',1501053012,'59a86f99427ce8ef62530e4da87fa16eaf17ea51a37f3552493f56311b31212f',3,'0200000000010000',8),
 'dA-peer': ('dA',1501066590,'a848c00b319904d337da99cf19a3ff2ca3d8dc6b52d7d568562cdb1929c34b85',2,'0200000000010000',8),
 'dB-dut': ('dB',967051444,'6cd1c9b4929025078ad29e2a7c659351fe09c9b3c6f8dfc792ba3a782b878e1f',2,'3cc0c60102030000',4),
 'dB-peer': ('dB',966912850,'5d60d73376b683f5b835744f84a0d0b5026f3e4f37f0bf08f9c8694af0b3c278',3,'3cc0c60102030000',4),
}

def locate(directory,size):
    fs=[p for p in (RAW/directory).iterdir() if p.is_file() and p.stat().st_size==size]
    assert len(fs)==1,(directory,size,len(fs))
    return fs[0]

def decode(label):
    directory,size,sha,port,sid,nch=EXPECTED[label]
    sid=bytes.fromhex(sid)
    p=locate(directory,size)
    h=hashlib.sha256()
    count=0; first=None; crf={}; pcap_count=0
    with p.open('rb') as f,(OUT/(label+'.pk')).open('wb') as pk,(OUT/(label+'.samples')).open('wb') as sm:
        gh=f.read(24);h.update(gh)
        magic,_,_,_,_,_,network=struct.unpack('<IHHIIII',gh)
        assert magic in (0xa1b2c3d4,0xa1b23c4d) and network==1
        scale=1 if magic==0xa1b23c4d else 1000
        while True:
            rh=f.read(16)
            if not rh:break
            assert len(rh)==16
            sec,frac,inc,orig=struct.unpack('<IIII',rh)
            b=f.read(inc);assert len(b)==inc and inc==orig
            h.update(rh);h.update(b);pcap_count+=1
            assert len(b)>=42
            tag,elen,pt=struct.unpack_from('<III',b)
            assert tag==6 and pt in (2,3)
            host=sec*10**9+frac*scale; lo=struct.unpack_from('<I',b,16)[0]
            if first is None:first=(host,lo)
            ns=lo-first[1]+round(((host-first[0])-(lo-first[1]))/2**32)*2**32
            fr=b[28:];et=struct.unpack_from('>H',fr,12)[0];off=14
            if et==0x8100:et=struct.unpack_from('>H',fr,16)[0];off=18
            if et!=0x22f0:continue
            a=fr[off:]
            if len(a)<24:continue
            if a[0]==4:
                key=(pt,a[4:12].hex()); c=crf.setdefault(key,[0,0,None,ns,ns])
                if c[2] is not None:c[1]+=((a[2]-c[2])%256!=1)
                c[0]+=1;c[2]=a[2];c[4]=ns
            if pt!=port or a[0]!=2 or a[4:12]!=sid:continue
            sdl=struct.unpack_from('>H',a,20)[0]
            assert sdl==6*nch*4 and len(a)>=24+sdl
            pk.write(PS.pack(ns,a[2],struct.unpack_from('>I',a,12)[0],a[1],sdl))
            sm.write(a[24:24+sdl]);count+=1
    assert h.hexdigest()==sha,(label,'hash mismatch')
    pk=np.memmap(OUT/(label+'.pk'),dtype=PK,mode='r')
    S=np.memmap(OUT/(label+'.samples'),dtype='>u4',mode='r').reshape(-1,nch)
    r={'sha256':sha,'pcap_records':pcap_count,'packets':count,'frames':len(S),
       'seq_breaks':int(np.count_nonzero(np.diff(pk['seq'].astype('i8'))%256!=1)),
       'tv_zero':int(np.count_nonzero((pk['flags']&1)==0)),
       'seconds':float(pk['ns'][-1]-pk['ns'][0])/1e9,
       'crf':{str(k):{'packets':v[0],'seq_breaks':v[1],'pps':(v[0]-1)/((v[4]-v[3])/1e9)} for k,v in crf.items()}}
    ds=np.diff(pk['ts'].astype('i8'))%2**32
    r['timestamp_step_ns']={'min':int(ds.min()),'max':int(ds.max()),'median':float(np.median(ds))}
    if label.startswith('dA'):
        first_valid=None;last_valid=None;valid_count=0;invalid_inside=0;last_n=None
        defects={'repeats':0,'skips':0,'backward':0,'torn':0,'invalid':0}
        for start in range(0,len(S),100000):
            s=S[start:start+100000].astype('u4');n=(s>>8)&65535
            tags=np.all((s>>24)==np.arange(1,nch+1),axis=1)&np.all((s&255)==0,axis=1)
            same=np.all(n==n[:,:1],axis=1);v=tags&same
            defects['torn']+=int(np.count_nonzero(tags&~same))
            inds=np.flatnonzero(v)
            if len(inds):
                if first_valid is None:first_valid=start+int(inds[0])
                last_valid=start+int(inds[-1]);valid_count+=len(inds)
                seq=n[inds,0].astype('i8')
                if last_n is not None:seq=np.r_[last_n,seq]
                d=np.diff(seq)%65536;last_n=int(seq[-1])
                defects['repeats']+=int(np.count_nonzero(d==0));defects['skips']+=int(np.count_nonzero((d>1)&(d<32768)))
                defects['backward']+=int(np.count_nonzero(d>=32768))
        defects['invalid']=last_valid-first_valid+1-valid_count
        r['pattern']={'first':first_valid,'last':last_valid,'valid':valid_count,**defects}
    (OUT/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n')
    return label,r

if __name__=='__main__':
    result={}
    with cf.ThreadPoolExecutor(max_workers=4) as pool:
        for k,r in pool.map(decode,EXPECTED):result[k]=r;print(k,json.dumps(r),flush=True)
    for run,nch in [('dA',8),('dB',4)]:
        pa=np.memmap(OUT/(run+'-dut.pk'),dtype=PK,mode='r');pb=np.memmap(OUT/(run+'-peer.pk'),dtype=PK,mode='r')
        sa=np.memmap(OUT/(run+'-dut.samples'),dtype='>u4',mode='r').reshape(-1,nch)
        sb=np.memmap(OUT/(run+'-peer.samples'),dtype='>u4',mode='r').reshape(-1,nch)
        matches=np.flatnonzero((pa['seq'][:10000]==pb['seq'][0])&(pa['ts'][:10000]==pb['ts'][0]))
        assert len(matches)==1
        i=int(matches[0]);m=min(len(pa)-i,len(pb));he=pe=0
        for j in range(0,m,100000):
            n=min(100000,m-j);a=pa[i+j:i+j+n];b=pb[j:j+n]
            he+=int(np.count_nonzero((a['seq']==b['seq'])&(a['ts']==b['ts'])))
            pe+=int(np.count_nonzero(np.all(sa[6*(i+j):6*(i+j+n)].reshape(n,-1)==sb[6*j:6*(j+n)].reshape(n,-1),axis=1)))
        dt=(pb['ns'][:m]-pa['ns'][i:i+m]).astype('f8')
        t=(pa['ns'][i:i+m]-pa['ns'][i]).astype('f8')
        slope,intercept=np.polyfit(t,dt,1);res=(dt-slope*t-intercept)/1000
        result[run+'-cross']={'common_packets':m,'dut_offset':i,'header_equal':he,'payload_equal':pe,'tap_rate_ppm':slope*1e6,'detrended_transit_us':[float(res.min()),float(res.max())]}
        print(run+'-cross',json.dumps(result[run+'-cross']),flush=True)
    # Exact words, rather than the published grader's per-frame hashes.
    M=np.memmap(RAW/'dB/dB.pcm',dtype='<u4',mode='r').reshape(-1,4)
    W=np.memmap(OUT/'dB-dut.samples',dtype='>u4',mode='r').reshape(-1,4)
    off=148874;bad=0;repeated=0;zero=0
    for j in range(0,len(M),100000):
        a=M[j:j+100000];b=W[j+off:j+off+len(a)]
        bad+=int(np.count_nonzero(np.any(a!=b,axis=1)))
        zero+=int(np.count_nonzero(np.all(a==0,axis=1)))
        left=max(0,j-1);z=M[left:j+len(a)]
        repeated+=int(np.count_nonzero(np.all(z[1:]==z[:-1],axis=1)))
    result['dB-exact']={'frames':len(M),'offset':off,'unequal_frames':bad,'adjacent_identical_frames':repeated,'all_zero_frames':zero}
    print('dB-exact',json.dumps(result['dB-exact']),flush=True)
    (OUT/'recomputed.json').write_text(json.dumps(result,indent=2)+'\n')
