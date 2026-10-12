#!/usr/bin/env python3
"""Isolate a multiline HTML-comment measurement escape without moving any document line."""
import json,pathlib,subprocess,sys
repo,packet,out=map(lambda s:pathlib.Path(s).resolve(),sys.argv[1:4])
f='629_MEDIA_CLOCK_FOLLOWING_BENCH.md';page=repo/'docs/findings'/f;text=page.read_text()
old="The tone sits in channels 0 and 1 of the peer's talker stream. Channels 2 and\n3 carry -1 to 0 LSB"
assert text.count(old)==1
forms={
 'unchanged':old,
 'single_line_comment':"The tone sits in channels 0 and 1 of the peer's talker stream. The residual was CLOCK_DOMAIN 7<!-- -->ppm. Channels 2 and\n3 carry -1 to 0 LSB",
 'multiline_comment':"The tone sits in channels 0 and 1 of the peer's talker stream. The residual was CLOCK_DOMAIN 7<!--\n-->ppm. Channels 2 and 3 carry -1 to 0 LSB",
}
results=[]
for name,new in forms.items():
 assert new.count('\n')==old.count('\n')
 d=out/'scratch/comment-probe'/name;d.mkdir(parents=True,exist_ok=True)
 (d/f).write_text(text.replace(old,new));(d/'README.md').write_bytes((page.parent/'README.md').read_bytes())
 r=subprocess.run([sys.executable,'-I',str(packet/'tools/check_b16_figures.py'),str(d/f),str(packet),str(d/'rows.tsv'),str(d/'coverage.tsv'),'--repo',str(repo)],capture_output=True,text=True,timeout=120)
 (out/f'receipts/comment-{name}.log').write_text(r.stdout+r.stderr)
 (out/f'receipts/comment-{name}.rc').write_text(str(r.returncode)+'\n')
 results.append({'name':name,'old':old,'new':new,'line':text[:text.index(old)].count('\n')+1,'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'additional_category_rows':[x for x in (d/'coverage.tsv').read_text().splitlines() if 'CLOCK_DOMAIN 7' in x or ('\t7\t' in x)]})
(out/'receipts/comment-probe.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps([{'name':x['name'],'rc':x['rc']} for x in results]))
# Acceptance for a corrected checker: baseline passes, both unsupported figures fail.
sys.exit(0 if [x['rc'] for x in results]==[0,1,1] else 1)
