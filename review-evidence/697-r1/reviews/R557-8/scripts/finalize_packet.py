#!/usr/bin/env python3
import hashlib,json,pathlib,re,sys
p=pathlib.Path(sys.argv[1]).resolve()
report=(p/'REPORT.md').read_text();assert report.splitlines()[0]=='[R557] POSITIVE - exact head abe2476c4771bedc84531cf8d05fd12ef947c0cf';assert report.splitlines()[-1]=='R557-8 FINISHED';assert 'SKELETON' not in report
for target in re.findall(r'\]\(([^)]+)\)',report):
 if target.startswith(('http:','https:','#')):continue
 assert (p/target.split('#',1)[0]).exists(),target
integrity=json.loads((p/'receipts/checkout-integrity.json').read_text());assert integrity['status_including_ignored']=='' and integrity['tracked_entries']==74 and integrity['gitlinks']==[] and integrity['base_gitlinks']==[]
scripts=['setup_sdk.py','probe_package_prefix.py','run_round.py','assertion_audit.py','replay_public.py','replay_round8.py','replay_extra.py','prior-fetch_prior.py','fetch_round8.py','prior-audit_results.py','preservation.py','verify_checkout.py','audit_hosted.py','audit_replays.py','export_receipts.py','finalize_packet.py']
files=[p/'REPORT.md',p/'REPLAY.md',*[p/'scripts'/x for x in scripts],*[x for x in (p/'receipts').rglob('*') if x.is_file()]]
for f in files:
 text=f.read_text();assert not re.search(r'/(?:home|data)/(?!runner)',text),f.relative_to(p)
 assert not f.relative_to(p).as_posix().startswith('scratch/')
manifest=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(p).as_posix()+'\n' for f in sorted(files))
(p/'MANIFEST.sha256').write_text(manifest)
for line in manifest.splitlines():
 digest,name=line.split('  ',1);assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest
print(len(files),'publishable files; links, privacy, tracked integrity and SHA256 manifest verified')
