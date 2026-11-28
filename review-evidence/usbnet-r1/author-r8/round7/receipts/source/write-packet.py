"""Write the final private handoff from completed, hash-bound evidence."""
import hashlib,json,sys
from pathlib import Path
root=Path.cwd();base=Path('$MANAGEMENT/2026-09-23/usbnet-a855/round7');p=base/'receipts';s=Path('$VALIDATION_STORAGE/usbnet-a855/round7/census')
head=json.loads((p/'final-head.json').read_text())['head']
q=json.loads((s/'qualification.json').read_text());d=json.loads((s/'derived-model.json').read_text())
assert q['groups']==159 and q['status']=='FAIL'
sys.path.insert(0,str(root/'tb/verilator/usbnet'));import egress_grade as g
rows={}
for f in (p/'egress-cases').glob('*/*.json'):
 x=json.loads(f.read_text());rows['/'.join(x['case'])]=x['result']
assert len(rows)==159
params=g.usb.base.params(g.usb.base.arty_spec());ok,lines=g.verdict(rows,params)
witness=max(rows,key=lambda name:rows[name]['wait_ps'])
maximum=rows[witness]['wait_ps']/1e6
wire=(maximum+g.usb.base.gptp_wire_ps(params)/1e6)*1.05+.32+.26
model=q['model'];r=model['rows_ms'];share=q['worst_pass']['worst_pass_cycles']/80000
bounds=f"""| Check | Measured or derived | Unchanged bound | Result |
|---|---:|---:|---|
| Load | {model['load']:.12f} | 0.70 | {q['checks']['owner-model']} |
| ACMP | {r['ACMP']:.5f} ms | 30 ms | {q['checks']['owner-model']} |
| txL | {r['txL']:.5f} ms | 49 ms | {q['checks']['owner-model']} |
| Last notice | {r['last']:.5f} ms | 140 ms | {q['checks']['owner-model']} |
| THE SHARE | {share:.7f} ms | 2 ms | {q['checks']['share']} |
| Wire egress, including all terms | {wire:.6f} us | 1000 us | {q['checks']['egress-100']} |
| Held AECP last delivery | 62.03635 ms | 61.99 ms | FAIL |
"""
identity=json.loads((p/'firmware-identity.json').read_text())
elfs='\n'.join(f"| {x['recipe']} | `{x['hashes']['ctrl_app.elf']}` | identical |" for x in identity if x['tree']=='candidate')
pins=json.loads((p/'final-head.json').read_text())['pins']
fixed=q['checks']['owner-model']=='PASS'
summary=f"""Status: STOP. ETA: measurement and evidence complete; a corrective design decision is required before implementation can resume. No completion ETA is claimed for that undecided change.

Local head: `{head}`. Branch: `1011-usbnet`. No push or posting. Bench and flash untouched.

The requested dependency `640699e6866602b2a5de5d404c43f3bd4df8037c` is a parent of merge `91252ecf7457287079d5d2f794b8544f0d9d34c4`; its commits were not rewritten. All fourteen files changed by its round-10 commit are byte-identical at the final head. The conflict in the firmware mutation fixture took the dependency version. Round-7 implementation changes only tests and documentation; the fabric LED design and control firmware remain unchanged.

The full injected link-rate census finished: 159 cases, all eight images, no omitted stimulus. The replay of the original census changed 44 cases' tails and refused 15 cases' successful-commit free-space outcomes, so its cost evidence was not carried alone. The fresh census includes one 1539-wire-octet injection (123.2 us) plus the measured 260 ns handshake at every busy period, through the live queue's backpressure. Every trace was independently replayed across eight stream phases with exact phase-zero departure agreement. All native stimuli are byte-identical to the dependency campaign.

The unchanged rule and #969 disposition {'reproduce the installed row as a fixed point' if fixed else 'do not qualify the installed row; see the complete derivation'}. No scheduling constant or bound was adjusted. The complete candidate and cost tables are in [DERIVATION.md](receipts/DERIVATION.md). The rule-selected row remains slice 1250 us, AECP pace 10 ms, queued bound 125 ms and stated TX bound 35 ms. Retry cold/attempt/notice terms remain {d['retry_us']} us; poll base is {d['costs']['base']} us, centisecond {d['costs']['centisecond']} us, LINK {d['costs']['event.LINK']} us, MAAP {d['costs']['event.MAAP']} us and withdrawal {d['costs']['item.withdraw']} us.

{bounds}
The blocking case is `none/backlog-owed`: last AECP delivery exceeds the frozen held-egress ledger by 46.35 us. Six other held-egress rows pass. The ordinary owner model and the 1 ms wire gate do not waive that failure. The service gate explicitly rejects any increase beyond a frozen ledger entry. No smaller host segment, empty-ring injection rule or firmware pacing change was selected.

The shipping MII attachment measured 257.5 ns maximum across 512 length/phase cases; it rounds to 260 ns. The fixed path independently measured 312.5 ns and remains stated at 320 ns. The queue already charges the handshake; the final expression conservatively adds it once more: `({maximum:.3f} + 54.88) * 1.05 + 0.32 + 0.26 = {wire:.6f} us`. The largest-wait witness is `{witness}`, stream phase {rows[witness]['phase']}. The 54.88 us term is the inherited gPTP burst. The maximum recorded queue occupancy is 27 records, below the inherited 254-record capacity. Host-local RX remains bounded at 38.075 us by the production mailbox test (81 checks); together with the derived ACMP row this is {r['ACMP']+.038075:.6f} ms, below 30 ms.

Six fresh builds establish same-pin ELF and map-header identity against the dependency. Fresh Arty SoC generation also confirms the map used by those builds; the raw CSV changes only its generation timestamp. These comparisons use the requested dependency and its current pins. The earlier packet used a different tsn-c-stack pin, so its older ELF hashes are not the comparison baseline. Whole-ALINX-bitstream identity is not claimed.

| Image | ELF SHA-256 | Comparison |
|---|---|---|
{elfs}

Every control map header has SHA-256 `5f0c602687dacba302959ebb99763e5922aff8ad19f76e7c7c05919b45a936fa`. Pins on both sides:

```text
{pins.rstrip()}
```

Validation: 92,755 USB/LED checks and four real SET_CLOCK_SOURCE cases pass; all 72 existing named RTL plants are caught. The new shipping-chain test catches both physical handshake plants. The injection grader passes nine clean controls and catches nine planted defects. The inherited egress grader passes 17 controls. Existing CBS, shaper-core and queue regressions pass (130,256 / 1,521,627 / 13 checks). Full traces, manifests, commands and source hashes are retained in [receipts/INDEX.md](receipts/INDEX.md).

A second gate remains failed: keeping `docs/DOCUMENTATION_AUDIT.md` byte-identical to the dependency leaves out the two existing USB documentation pages. The freshness gate reports that exact difference. No exception to the byte-identity instruction was assumed. The prior inventory, failing output and decision record are preserved. Other focused code, documentation and evidence gates pass as listed in the index.

No current-head physical route or release is claimed. This round generated maps through the required lowest-priority slot but did not synthesize or route. Earlier route, attachment, external-I/O and whole-image crossing limitations remain open; the earlier physical result is not promoted to proof for the new firmware ROM. No independent approval, hosted gate success or merge into `dev` is claimed. Issues #1011 and #1018 remain related, not closed.
"""
(base/'HANDOFF-r7.md').write_text(summary)
(base/'REVIEW-READY.md').write_text(f"""Status: NOT REVIEW READY. Local head `{head}`.

The complete 159-case census fails the frozen held-egress ledger: `none/backlog-owed` last AECP delivery is 62.03635 ms against 61.99 ms, exceeding it by 46.35 us. No allowance was relaxed. The exact dependency inventory also fails freshness for two existing USB pages; an exception to byte identity has not been authorized.

{bounds}
The installed row is {'a measured fixed point' if fixed else 'not qualified'} under the unchanged rule and #969 disposition. Arty and both ALINX ELF/map comparisons are byte-identical at equal pins. USB/LED, planted-defect, handshake, injection-grader and shaper checks pass. All eight images and all 159 cases are retained, including the failure.

See [HANDOFF-r7.md](HANDOFF-r7.md), [the derivation table](receipts/DERIVATION.md) and [receipts](receipts/INDEX.md). A design decision and a corrected full qualification are required before another review-ready claim. This is executor evidence, not a review verdict. No push, posting, bench operation or physical release occurred.
""")
(base/'PR-BODY.md').write_text(f"""The USB network path copies permitted frames and injects rate-limited best-effort traffic while preserving endpoint priority. Arty status LEDs follow the [fabric-level ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7213370880): LD2 means any media-locked input or open output transmit gate; LD3 means internal selection or a locked selected source. There is no firmware LED register or LED code in the control image.

This update merges #1004's 100 Mb/s qualification and adds the [required injection envelope](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7216971645): one longest injected frame before every busy period, with the measured shipping-chain handshake. The live queue delays mailbox tails, so free-space tests and completion readers include the injected traffic.

Qualification is blocked. All 159 cases across eight images completed, retaining the unchanged rule and dispositions. The derived owner row {'remains a fixed point' if fixed else 'does not qualify'}, and the complete wire bound is {wire:.3f} us against 1000 us. However, last AECP delivery in the held-egress case is 62.03635 ms against its unchanged 61.99 ms ledger. The 46.35 us excess remains a failure. No bound or ledger entry was relaxed.

Control ELF and map-header identity passes for Arty and both ALINX configurations at the same dependency pins. The shipping handshake measures 257.5 ns across 512 cases, stated as 260 ns. USB/LED tests, 72 existing planted defects, both shipping-handshake defects, 18 injection controls and the existing shaper regressions pass. Keeping the dependency's documentation inventory byte-identical also leaves its freshness gate failing on the two USB pages.

Board observations, attachment integration, broader candidate gates and independent review remain open. Existing whole-image crossing and external-I/O limitations remain. No physical release or issue completion is claimed.

Relates to #1011
Relates to #1018
""")
print(head,'final packet written; STOP')
