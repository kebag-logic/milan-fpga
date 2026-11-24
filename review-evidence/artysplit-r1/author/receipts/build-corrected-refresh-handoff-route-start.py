import datetime,json
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
p=Path('<home-path>/milan-fpga-management/2026-09-23/artysplit-a829/round4/HANDOFF-r4.md')
before=p.read_text();(r/'handoff-before-routing.log').write_text(before)
head=json.loads((r/'qualified-source.json').read_text())['head']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
text=before
text=text.replace('approximately 2–5 more hours from 2026-11-24 18:10 UTC for final grading, three routed candidates and packaging',
 'approximately 2–4 more hours from 2026-11-24 19:00 UTC for three routed candidates and packaging')
text=text.replace('Current head: 4a89ddcdb18bdfaafc9e999daeee1e7ba56274a2; base 854bd7236792ce1adbd10c43b13a6a5002ad3bb6. No round-4 commit yet. Never push.',
 f'Current head: {head}; base 854bd7236792ce1adbd10c43b13a6a5002ad3bb6. Qualified source committed locally; worktree clean. Never push.')
start=text.index('The complete calibration and fresh partial census')
end=text.index('\n\nThe unchanged port evidence',start)
text=text[:start]+'''The complete fresh 80 MHz campaign passed all 145 cases across eight variants. Its 13 final command checks and six qualification checks all pass. Load is 0.4966771140, txL 48.74 ms, last notice 121.84 ms, ACMP 28.82 ms and maximum whole pass 134507 cycles (1.6813375 ms). All five owner bounds pass. Only the seven authorized held-egress rows miss their original service budgets; each stays within its own unchanged ledger.

Frozen firmware tree: 7e5a1ae880340481da1ca0b8850e3f2a07e57b366405d2cbef2c358fa22eca63. The active phase is $VALIDATION_STORAGE/artysplit-a829/r4/build-corrected. final-census/qualification.json has SHA256 f6f1d2f535a8de0ec2348dbb0998a152103f3583e9bf4cc72b0115552ef1886c. qualified-source.json ties the complete evidence to the local commit. No firmware changes remain pending.

All four fresh firmware shards pass. Fresh boot, six native controls, six plants and eight placement controls pass. The service grader catches 297 mutants. Both AX configurations pass 42 generated/product comparisons and 13 controlled SoC-export comparisons, including full firmware ELF identity. All eleven documentation gates pass after the final measured service prose. AX bitstreams were not rebuilt.''' +text[end:]
start=text.index('After all 145 cases and all eight pipeline results pass:')
end=text.index('\n\nFinish REPORT.md',start)
text=text[:start]+'''The three implementation attempts are running under build-images.py with PYTHONHASHSEED=0 and the owned TMPDIR. The required slot wrapper limits active builds to two and requires MemAvailable >=20 GB. Directives: ExtraPostPlacementOpt, AltSpreadLogic_high and ExtraTimingOpt. Their input is the qualified final product ELF. grade-images.py will select the best worst-corner result at +0.030 ns WNS and zero WHS across all four reports, with zero failing setup and hold endpoints. publish-image.py then copies and rechecks the matched inputs without hardware I/O. No route has completed yet.''' +text[end:]
text=text.replace('Live census changes from this phase\'s calibration: {}.','Complete qualification: PASS; native groups 145/145; final command checks 13/13; final documentation gates 11/11.')
p.write_text(text)
(r/'handoff-route-start.json').write_text(json.dumps(dict(time=now,head=head,status='ROUTING'),indent=2)+'\n')
