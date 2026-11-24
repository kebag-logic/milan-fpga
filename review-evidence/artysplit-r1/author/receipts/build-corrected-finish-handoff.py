"""Prepare the final author handoff and the single authorized Issue report."""
import datetime,hashlib,json,subprocess,sys
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
p=Path('<home-path>/milan-fpga-management/2026-09-23/artysplit-a829/round4')
root=Path('$LANES/arty-split')
sys.path.insert(0,'<home-path>/milan-fpga-management/2026-09-23');import privacy
def read(path):return json.loads(path.read_text())
im=read(r/'image-ready.json');q=read(r/'final-census/qualification.json')
assert im['status']=='PASS' and q['status']=='PASS'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
assert head==im['head']
assert not subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip()
for artifact in im['artifacts'].values():
 data=Path(artifact['path']).read_bytes()
 assert len(data)==artifact['bytes'] and hashlib.sha256(data).hexdigest()==artifact['sha256']
checks=read(p/'receipts/privacy-check.json');assert checks['status']=='PASS'
for row in checks['checked']:
 data=(p/'receipts'/row['file']).read_bytes()
 assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
bit=im['artifacts']['Bitstream'];layout=im['artifacts']['flashboot_layout.json']
manifest=im['artifacts']['Matched image_manifest.json'];u=im['utilization']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
report=read(r/'issue-report-posted.json') if (r/'issue-report-posted.json').exists() else None
url=report.get('url') if report else None
handoff=f'''Status: IMAGE READY. Qualified 80 MHz Arty split image and matched deployment inputs are preserved.
ETA: complete for the author image handoff. The manager's bench and independent reviews remain pending.

[A829] #878 round 4, updated {now}.
Checkout: $LANES/arty-split; branch pf-arty-split-1 -> dev-soft-core.
Local head: {head}; base 854bd7236792ce1adbd10c43b13a6a5002ad3bb6. Worktree clean. No push.

The entity retains one interface, one AAF talker, one AAF listener and one CRF input: FPGA shape (1,1,2). Sys/CPU is exactly 80,000,000 Hz, VCO 800 MHz, datapath 50 MHz and margin=0. MII advertises only 100BASE-TX full duplex. No Linux row was added.

All 145 fresh service cases across eight variants, thirteen final command checks and six qualification checks pass. Load 0.49667711403508774 <=0.70; txL 48.74 <=49 ms; maximum whole pass 1.6813375 <=2 ms; last notice 121.84 <=140 ms; ACMP 28.82 <=30 ms. Slice 950 us, pace 9 ms, queued bound 125 ms and ordinary transmit statement 30 ms follow the existing rules. The seven held-egress rows remain the only recorded misses, each within its own unchanged 80 MHz ledger. No owner bound failed.

Selected directive: {im['directive']}. Best worst-corner WNS {im['worst_wns_ns']:.3f} ns and WHS {im['worst_whs_ns']:.3f} ns, with zero failing setup/hold endpoints in all four signoff reports. All three directives completed; REPORT.md records each result. The slot wrapper admitted at most two builds and checked at least 20 GB available memory. Slow/Fast are fixed speed models; 0/85 C are endpoint power metadata.

Selected attempt's post-placement utilization: {u['Slice LUTs']:g} LUTs, {u['Slice Registers']:g} FFs, {u['Block RAM Tile']:g} BRAM tiles and {u['Slice']:g} occupied slices. A new Arty firmware ledger records ELF 159532 bytes; text/rodata/data/bss/stack 112748/11558/100/45072/8192 bytes; ROM live extent 124412, SRAM live extent 53392; allocation 44/56 RAMB36 equivalents.

Deployment pair inputs, preserved with their original manifest/layout bytes:

- Bitstream: {bit['path']}
  {bit['bytes']} bytes; SHA256 {bit['sha256']}
- Layout: {layout['path']}
  {layout['bytes']} bytes; SHA256 {layout['sha256']}
- Matched manifest: {manifest['path']}
  {manifest['bytes']} bytes; SHA256 {manifest['sha256']}

The image directory also contains matched AEM files, the exact ELF, CSR maps and generated gateware. Original and copied input sets pass image identity and offline deploy input checks. No flash, JTAG, console or bench operation ran.

All four firmware shards, the complete service grader, boot/region simulations and fault controls, MII host tests and plants, affected timestamp suites, builder checks, lint/front-end checks and eleven final documentation gates pass for their executed scope. Historical area calibration is SKIP for its absent external reference. The original four scheduler blocks and old cost rows remain byte-identical. AX identity passes 42 generated/product plus thirteen controlled SoC-export comparisons, including both full ELFs; AX bitstreams were not rebuilt.

Evidence: REPORT.md, PR-BODY.md, receipts/INDEX.md and image/provenance.json in this directory. All indexed compressed receipts pass privacy.scrub_redact on their compressed and expanded bytes. The receipt index and privacy-check.json contain the complete count and hashes. Full service qualification SHA256: {im['qualification']['sha256']}.

The active scratch is $VALIDATION_STORAGE/artysplit-a829/r4/build-corrected. Source and full campaign provenance are in qualified-source.json and final-census/qualification.json. The final campaign used four shared harness slots. An early exploratory fifth leg was terminated, excluded and rerun within the limit; concurrency-correction.json records the deviation. Scratch stayed below 30 GB; only closed generated precompiled headers were reclaimed with hash inventories.

The manager runs the bench after this handoff. Independent internal/external reviews, hosted checks, candidate-merge validation, merge and Issue completion remain pending. This is author evidence, not a review verdict.
{'Issue REPORT: '+url if url else 'The single final [A829] REPORT is prepared for posting on #878.'}

IMAGE READY {head} {bit['sha256']}
'''
(p/'HANDOFF-r4.md').write_text(handoff)
comment=f'''[A829] REPORT — ROUND 4 — IMAGE READY

Local head: `{head}` on `pf-arty-split-1` -> `dev-soft-core`. Committed locally; not pushed.

The Arty retains one AAF talker, one AAF listener and one CRF input. Sys/CPU is exactly 80 MHz, VCO 800 MHz and datapath 50 MHz; margin=0 is unchanged. Its own FPGA `(1,1,2)` costs derive slice 950 us, pace 9 ms and queued bound 125 ms. Complete fresh qualification passes 145 cases across eight variants: load 0.4966771140, txL 48.74 ms, maximum pass 1.6813375 ms, last notice 121.84 ms and ACMP 28.82 ms. All five owner bounds pass. Only the seven authorized held-egress rows remain recorded misses, within their own unchanged 80 MHz ledger; no new or larger miss.

MII advertises 100BASE-TX full duplex only, with host cases and planted defects. The four existing scheduler rows remain byte-identical. AX7101 1x1/1if and 8x8/1if pass 42 generated/product and thirteen controlled SoC-export identity comparisons, including full firmware ELFs. AX bitstreams were not rebuilt. No Linux row was added.

All three routing directives completed through the required slot wrapper. Selected `{im['directive']}`: worst WNS **+{im['worst_wns_ns']:.3f} ns**, WHS **+{im['worst_whs_ns']:.3f} ns**, zero failing endpoints across all four reports. Post-placement utilization: **{u['Slice LUTs']:g} LUTs / {u['Slice Registers']:g} FFs / {u['Block RAM Tile']:g} BRAM / {u['Slice']:g} slices**. A new Arty firmware ledger records a 159532-byte ELF and 44/56 RAMB36 equivalents.

Deployment inputs are preserved together and pass offline identity/input checks:

- Bitstream: {bit['bytes']} bytes, SHA256 `{bit['sha256']}`.
- `flashboot_layout.json`: {layout['bytes']} bytes, SHA256 `{layout['sha256']}`.
- Matched `image_manifest.json`: {manifest['bytes']} bytes, SHA256 `{manifest['sha256']}`.

Four firmware shards, service qualification and grader controls, Arty boot/region and fault controls, affected timestamp suites, builder checks, lint/front-end and eleven final docs gates pass for their executed scope. Historical area calibration remains SKIP for its absent external reference. An early exploratory fifth harness leg was excluded and rerun within the limit; the deviation is recorded.

Complete service qualification receipt SHA256: `{im['qualification']['sha256']}`. Reproduction entry points, with N = 0, 1, 2, 3 and owned scratch directories:

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --self-test --require-rv32 --shard N/4 --jobs 1 --build-dir <scratch>/firmware-N
python3 tb/verilator/ctrl_service_budget/selftest.py
PYTHONHASHSEED=0 python3 tb/verilator/ctrl_split_boot/run.py --shape endstation_arty_split --interfaces 1 --self-test --build-dir <scratch>/boot-controls
PYTHONHASHSEED=0 python3 tb/verilator/ctrl_region_decode/run.py --shape endstation_arty_split --self-test --build-dir <scratch>/region
```

The packet preserves the complete 145-case enumeration, native trace/input hashes, cost derivation, individual docs commands and all three route commands and reports.

The round-4 manager packet contains HANDOFF-r4.md, REPORT.md, PR-BODY.md, the privacy-checked receipt index and matched image directory. No flash, JTAG or bench operation ran. The manager's bench, independent reviews, hosted checks and merge validation remain pending; this report is author evidence, not a review verdict.

IMAGE READY {head} {bit['sha256']}
'''
(r/'issue-report-body.log').write_text(comment)
# The local handoff intentionally names the exact user-requested deployment
# paths. Public prose must already be scrubbed; compressed receipts are
# independently scrubbed and fixed-point checked by keep-receipts.py.
for path in (p/'REPORT.md',p/'PR-BODY.md',r/'issue-report-body.log'):
 data=path.read_bytes();assert privacy.scrub_redact(data)==data,path
record=dict(status='PASS',time=now,head=head,bitstream_sha256=bit['sha256'],
 compressed_receipts=len(checks['checked']),issue_report_url=url,
 packet_files=[dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
               for path in (p/'HANDOFF-r4.md',p/'REPORT.md',p/'PR-BODY.md')])
(r/'final-packet-check.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
