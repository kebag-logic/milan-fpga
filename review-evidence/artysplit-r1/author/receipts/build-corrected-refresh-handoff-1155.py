"""Replace stale checkpoint prose with the current author handoff; preserve history."""
import datetime,hashlib,json,re
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
p=Path('<home-path>/milan-fpga-management/2026-09-23/artysplit-a829/round4')
live=json.loads((r/'live-status.json').read_text())
privacy=json.loads((p/'receipts/privacy-check.json').read_text())
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
old=(p/'HANDOFF-r4.md').read_bytes()
backup=r/'handoff-before-1155.log';assert not backup.exists();backup.write_bytes(old)
text=f'''Status: IN PROGRESS. Fresh qualification has 8/8 service builds and {live['service_groups']}/145 native cases complete. Final measured grading and routing remain pending.
ETA: approximately 4–7 more hours from 2026-11-24 11:55 UTC, including remaining native cases, final grading, three routed candidates and packaging. The current native-only forecast is about 2.5 hours; host contention, route-slot waits or a finding can extend this.

[A829] #878 round 4, updated {now}.
Checkout: $LANES/arty-split; branch pf-arty-split-1.
Current head: 4a89ddcdb18bdfaafc9e999daeee1e7ba56274a2; base 854bd7236792ce1adbd10c43b13a6a5002ad3bb6. No round-4 commit yet. Never push.

The settled entity is one interface, one AAF talker, one AAF listener and one CRF input: FPGA shape (1,1,2). CPU/sys is exactly 80,000,000 Hz, VCO is 800 MHz, datapath is 50 MHz, margin=0. No Linux row. No flash, JTAG, console or bench operation.

Rulings: [option 1](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7096503672), [80 MHz](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097204685), [held-egress ledger](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097474930). The latest recheck is retained in build-corrected/manager-rulings-recheck.json. The seven held-egress rows remain recorded misses under their own ledger; a new or larger miss fails.

The installed row uses slice 950 us, pace 9 ms, queued bound 125 ms and ordinary transmit statement 30 ms. Both-MRPDU build is 1035 us, one-MRPDU build 660 us, SRP record 300 us, aged step 1060 us and centisecond work 150 us. Retry cold/attempt/notice are 125/30/230 us. The 1035 us build statement selects the existing one-MRPDU-per-pass path. The old four shape blocks and old cost rows are byte-identical.

The complete calibration and fresh partial census give load 0.4966771140, txL 48.74 ms, last notice 121.84 ms and ACMP 28.82 ms. The fresh maximum whole pass so far is 134507 cycles, 1.6813375 ms at 80 MHz. These remain progress measurements until all 145 cases and final grading pass. No new measured cost, owner failure or unauthorized row miss has appeared.

Frozen firmware tree: 7e5a1ae880340481da1ca0b8850e3f2a07e57b366405d2cbef2c358fa22eca63. The active phase is $VALIDATION_STORAGE/artysplit-a829/r4/build-corrected. run-pipeline.py remains in the foreground; final-census/completed.json, final-progress/latest.json and pipeline-results.json carry reproducible progress. Do not change frozen firmware while that campaign runs.

All four fresh firmware shards pass. Fresh boot, six native controls, six plants and eight placement controls pass. The service grader catches 297 mutants. Both AX configurations pass 42 generated/product comparisons and 13 controlled SoC-export comparisons, including full firmware ELF identity. The current 11 documentation gates pass; the final service prose will receive the same gates again. AX bitstreams were not rebuilt.

The unchanged port evidence includes the exact PLL and wrong-clock controls; eight MII host cases and seven planted defects; Arty region simulation with both original decode mutants; writable timestamp, shadow and timestamp-return tests; builder gates; RTL lint and front-end checks. Historical area calibration was skipped because its external reference report is absent. These receipts do not claim the full merge bar, independent review or hardware qualification.

The final product ELF is 159532 bytes, SHA256 b81f300e205f1067170458898b8b62f8407ecdb46bd38467e540efb89b9e84e5. ROM live extent is 124412 bytes, SRAM including stack is 53392 bytes, allocation 44/56 RAMB36 equivalents. A new Arty firmware ledger is in docs/design/SPLIT_CONTROL_MEMORY.md section 15. No bitstream or qualified flash pair exists yet.

After all 145 cases and all eight pipeline results pass: run qualify-final-census.py with census-preliminary-complete.json; require all six final checks PASS. Then run finalize-service-docs.py and its eleven gates, verify source/old-row identity, and commit locally with a one-line message and no trailers. Prepared build-images.py requires that commit and the complete qualification. Run it with PYTHONHASHSEED=0 through the required slot wrapper (at most two, MemAvailable >=20 GB), using the final product ELF. grade-images.py selects the best of three directives at +0.030 ns WNS and zero WHS across all four reports, also requiring zero failing hold endpoints. publish-image.py copies and rechecks the matched inputs without hardware I/O.

Finish REPORT.md, PR-BODY.md and the receipt index with actual selected-route utilization, sizes and hashes. Every compressed receipt and its expanded contents must pass the privacy fixed-point check. Post exactly one [A829] REPORT on #878 at the end. The manager runs the bench after IMAGE READY; independent reviews, hosted checks, merge and Issue completion remain pending.

Scratch remains below the 30 GB cap. At most four harness legs run in this campaign. An early superseded bootstrap briefly admitted a fifth leg; it was terminated, excluded and rerun within the limit, as recorded in concurrency-correction.json. Closed generated precompiled headers were reclaimed with hash inventories; source, executables, traces and receipts were preserved. The completed dispatch-test fixture was moved out of the checkout into owned scratch, with hashes retained.

{len(privacy['checked'])} compressed receipts currently pass the privacy fixed-point checks. A new incremental receipt checkpoint is running. The earlier handoff is preserved as handoff-before-1155.log; REPORT.md and the receipts retain the calibration history.

Live foreground-gate status: {live['summary']}.
Live census changes from this phase's calibration: {{}}.

IN PROGRESS; no qualified image yet.
'''
(p/'HANDOFF-r4.md').write_text(text)
report=p/'REPORT.md';body=report.read_text()
status=(f'Status: IN PROGRESS, 2026-11-24 11:55 UTC. The corrected 80 MHz image has completed {live["service_groups"]} of 145 fresh service scenarios. '
        'All four firmware shards, boot and fault controls, service grader, AX identity comparisons and current documentation gates pass. '
        'Final service grading and three routed candidates remain pending. ETA: approximately 4–7 more hours, subject to host contention, routing and findings.')
report.write_text(re.sub(r'^Status: .*$',lambda _:status,body,count=1,flags=re.M))
(r/'handoff-refresh-1155.json').write_text(json.dumps(dict(time=now,status='UPDATED',
 before_sha256=hashlib.sha256(old).hexdigest(),after_sha256=hashlib.sha256(text.encode()).hexdigest(),
 completed=live['service_groups'],note='Current status replaces superseded checkpoint prose; history retained.'),indent=2)+'\n')
print('Current handoff refreshed; prior handoff preserved.')
