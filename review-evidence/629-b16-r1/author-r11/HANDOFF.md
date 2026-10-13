# [A603] Round 11 handoff

Refs #629. 2026-10-13. Packet-only composition repair under assignment 6144924772 and finding R624-11-F1. Executor [A603]; independent composition re-review remains R624-12.

PR head: `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, unchanged.
Candidate: `ada26e56ac42ee5de311aef84cb86c8435b97cee`, read-only input.
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6144950822.
Status: REVIEW READY posted and read back equal.
https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6145360198

| Cycle | Work | Result | Evidence |
|---|---|---|---|
| r11-0 | Read public assignment, R624-11 and prior packet; write skeleton and TAKEN | Manager chose regeneration without a new head | TAKEN.md |
| r11-1 | Read exact candidate blobs and public review receipts | Remote object fetch unavailable; authorized read-only repository supplied blobs. No checkout created | receipts/bindings.json |
| r11-2 | Regenerate from unchanged spec/build | Exactly 1,934 page rows +7; check otherwise byte-equal | receipts/build.stdout; bindings.json |
| r11-3 | Source, original-candidate and regenerated-candidate checks | rc 0 / 1 / 0; all three runs match R624-11 stdout/rows/coverage | receipts/figcheck.json |
| r11-4 | Earlier control runners and supplementary checks | Same outcomes; 117/117 standing controls and 172/172 self-probes | receipts/control-comparison.json; supplementary-comparison.json |
| r11-5 | Earlier review probes on a temporary symlink fixture | Invalid fixture: out-of-root packet paths refused. Excluded from final proof; replaced by a physical temporary packet copy | See setup notes below |
| r11-6 | Earlier review probes on physical packet; three fixed locators | All outcomes retained after the named +7 relocations; originals and their stale selections/refusal retained | receipts/probe-comparison.json; receipts/probes/; receipts/relocated-*.json |
| r11-7 | Reproduction step cand, regeneration and normalized comparison | rc 0; 1,960/1,960 rows; 0 uncovered; 0 MARKUP; byte-equal rebuild | receipts/reproduce/ |
| r11-8 | Required local gates at unchanged head | All 14 entries rc 0; no repository edit | gates/results.json |
| r11-9 | Bindings, prior-packet audit, proposed PR body and manifests | 31 reused scripts equal published originals; full source check unchanged | receipts/reused-inputs.json; PR-BODY.md |
| r11-10 | Public REVIEW READY and final manifests | Posted once; readback equal; manifests verified | REVIEW-READY.readback.md; review-ready-url.txt; MANIFEST.sha256 |

## Bindings and results

`receipts/bindings.json` gives full Git blob IDs, SHA-256 and sizes. The source check remains bound to `844ff7fb2e958ebb12368d22fa620dc094dd5888`; this packet's check binds `cdd3121f567e3a37784f98b962713db3de5c7687`. Each passing run covers 1,960 rows and 15,597 digits, zero uncovered or MARKUP. The spec and build are copied byte for byte from the published source packet; their anchors resolve the new lines without a spec edit.

Rounds 3-10: 5/5, 7/8, 21/22, 38/39, 48/50, 73/73, 97/97, 117/117. Historical rc 1 expectations remain recorded under decision 6132293481; they are not described as fully green. The 15 review probes retain their frozen results, including their recorded limits. All 59 parser cases, 15 parser-output mutations and the layer-isolation cases match the previous packet.

The original two line-3200 probes select no candidate row. Their relocated copies select 3015, 3181 and 3207, and each planted defect makes its own line-3207 row MISMATCH. R624-6's original attribution probe refuses at 3244; its copy changes only ANCHOR to 3251 and retains the same 37 outcomes, including the four recorded not-meeting cases. Full before/after locators are in control-comparison.json and probe-comparison.json; README stays at line 15.

## Reuse and changes

| Artifact | Change |
|---|---|
| tools/check_b16_figures.py | Regenerated page-row locators only; source check preserved |
| tools/r10_figures_spec.py, tools/r10_figures_build.py | Unchanged public copies |
| tools/r11_probe_reruns.py | Copy of r10 runner: output r11/, 570-second deadline, preserve child stdout/stderr |
| tools/relocated/ | Three published probes copied; only the named page locators +7 |
| tools/run_validation.py | New foreground dispatcher; inherited scripts unchanged |
| tools/reproduce.sh | R624-11 step 1 with separate checks; add spec rebuild and normalized receipt comparison |
| tools/compare_figures.py, tools/compare_validation.py | New offline comparisons; outcomes never rewritten |
| PR-BODY.md | Proposed full body: both bindings and R624-10-R1 wording; manager applies |

## Reproduction

Supply the previous `author-r10/` packet at `5775cfa78dc9250ea1b689fc2cfa8e20c41281bb`, a source repository with the lane history, the candidate page inputs and the pinned parser environment. The new check uses the previous packet as its receipt root. All large or temporary files stay outside this packet.

```sh
timeout 590s bash author-r11/tools/reproduce.sh   "$CANDIDATE_INPUT" "$SOURCE_REPO" "$PREVIOUS_PACKET" "$PARSER_PY" "$OUTPUT"
timeout 30s python3 -B author-r11/tools/compare_validation.py   "$PREVIOUS_PACKET" author-r11
```

`run_validation.py` documents individual foreground modes. The candidate input fixture used here contains only the two page blobs, the design reference, renderer and requirements; Git history reads use the source repository. Probe modes use a physical copy of the old packet, with only the new checker installed, under their temporary parent directory's `packet/`. No symlink overlay is suitable: packet-path identifiers must resolve within the packet.

Setup notes: the first direct trial used a wrong Git-history path and refused 89 git-derived rows; the corrected path passed without a checker change. A symlink-based probe fixture then made legitimate packet paths resolve outside its root; those trial results were discarded from proof and retained in temporary storage. The final source and candidate receipts match the independent review. The original rc receipt uses a labeled string; comparison judges its numeric status. No expectation was altered to repair these setup issues.

Large page blobs and the two original-check negative-control TSVs remain outside the packet; sizes and SHA-256 are recorded in bindings.json and large-artifacts.json. Incidental bytecode was moved out. No package, environment, toolchain, tree export or file over 200,000 bytes remains in the new packet.

No bench access or lock acquisition occurred. The prior restore evidence stands unchanged. No source file, index row, PR, branch head or existing public comment was edited; no commit, push, merge or new checkout occurred. The manager owns publication, PR-body application and R624-12; page-binding wording goes to #495 as assigned. Issue #629 remains open with its earlier acceptance limitations.
