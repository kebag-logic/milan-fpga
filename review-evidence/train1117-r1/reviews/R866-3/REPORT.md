[R866] POSITIVE - exact head 0839453f6d7135063e904bcaf4ac1852ad6b522a

R866-3, external independent composition review of PR #945. Tree: `55b7e53dfe517a40d9ec638307d9ba6b54862edd`. Reviewed delta: `b1f1161b0f72e6066f60c7e0fa5ba399e185493d..0839453f6d7135063e904bcaf4ac1852ad6b522a`; source base: `cb96336d7aaacbaec76990ab07ef64148808d4ac`.

All five lenses are CLEAN for this composition delta. No open BLOCKER, MAJOR or MINOR was found. The wording residues below remain on the residue checklist. This verdict does not complete physical acceptance or authorize a merge.

The review reconstructed the repository contract, documentation map, all fourteen issue bodies, relevant public scope decisions, requirements and interfaces before examining the train history and diff. The full base-to-head diff was acquired; the technical pass concentrated on step 12 and its dependencies, as assigned. `independent-pass.md` records the independent verdict and ledger before prior review findings were opened. Untouched composition coverage carries from R866-2 and R866-1. The source implementation was not re-reviewed. Published source verdict headers confirm R867-3 POSITIVE at `fe297847a3221997182fcb6a903b4e93a8997ef3` and R868-2 POSITIVE at `9f4f3de03f99dc8c7a72f5f8884f00df82c965d2`.

The public evidence is [author-r5 at archive 33c82526](https://github.com/kebag-logic/milan-fpga/tree/33c82526d5f62e39b1324b5dd3e34b63602f8c03/review-evidence/train1117-r1/author-r5). References below to `receipts/` and `RESOLUTIONS.md` name that archive. All 2,503 author-r5 files match `MANIFEST.json`'s published SHA-256 values. This is digest verification: the archive commit contains no cryptographic signature, and signer authentication is not claimed. No private author material was used, and no other checkout was edited.

**Composition and conflicts.** `composition.txt` reproduces the comparison. The history is a clean merge `d09c7118` of `66c6edf3`, ledger adjustment `967b1ca9`, then merges `7650a02d` of `9f4f3de0` and `0839453f` of `fe297847`. Thus `967b1ca9` is the round-1 ledger commit, not itself a merge.

There are 23 source-delta paths and 22 net train-delta paths, with no unexpected train path. All sixteen non-ledger paths carry exactly the same added/deleted lines as `cb96336d..fe297847`, including the production platform files, test wiring, tests, plants, receive-monitor harness and boot-SoC override. Hunk positions and blob IDs naturally differ where the train already changed surrounding material. Production RTL, the mailbox contract, AECP core/face, control-loop implementation and CPU-budget directory are unchanged from step 11.

The remerge diffs identify exactly the seven round-2 conflict files in `RESOLUTIONS.md:308`: `SPLIT_CONTROL_MEMORY.md`, the platform README, `ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py`, the split-boot README and `plat_ledger.py`. Six whole-file resolutions equal the first parent byte for byte. Only the platform README's two ROM hunks take the train's text; its format/change-port text carries. The round-3 conflict is only `ctrl_memory.py`'s comment, retained byte for byte from the first parent. The other three round-3 patches carry exactly.

Both intents survive. The source branch's smaller entries describe its smaller base; the composed train needs 63.0 and 58.0, already present before round 2. The train retains the source's point-specific overrides and refusal coverage, plus its ninth unlinked-override control. `boot_soc.py:100` receives the one-interface override. The fixture at `test_ctrl_memory.py:226` moves equal granules from SRAM to ROM so the half-tile-overflow case reaches 63.5 without first exceeding the address region. No refusal is weakened. Round 3's wording change concerned a source-only sentence absent from the train's comment; retaining the train block loses no allocation rule or executable behavior.

**Ledger and bounds.** The owner's [ROM-debt decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6892332745) and [composition ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6950343235) permit measured ROM entries as debt while preserving fit and timing. The exact-head `receipts/step12c/ledger/plat-ledger.log` reports:

| Point | ROM need, bytes | SRAM need, bytes | Planned RAMB36 | Limit |
|---|---:|---:|---:|---:|
| 1x1/1if | 125,984 | 56,736 | 45.0 | 56.0 |
| 1x1/2if | 127,584 | 59,040 | 46.0 | 56.0 |
| 8x8/1if | 138,624 | 98,160 | 58.0 | 58.0 |
| 8x8/2if | 140,200 | 115,504 | 63.0 | 63.0 |

All four pass, as do the nine ledger controls with their required findings. The final two-interface ROM is 936 bytes beyond the former capacity and has 1,112 bytes left in the new allocation; the one-interface ROM has 640 bytes left. The document's explicitly dated `66c6edf3` table records earlier round-1 sizes, not these final measurements. The fixture's separate 60.5 entry stays unchanged. Debts remain 7.0, 2.0 and 4.5 RAMB36 respectively, not timing exceptions.

The independent focused probe runs the real memory rule/refusal arm and its ten planted ledgers, then checks 62.5/63.0/63.5 explicitly. It reports zero failures: the first two are accepted under the platform override; 63.5 is refused by `allocation over budget`. This verifies the composition-specific fixture repair without running a full builder bank.

**Executable evidence and carry.** `receipt-audit.txt` names the inspected artifacts and their execution heads:

| Evidence | Execution and result | Applicability at final head |
|---|---|---|
| Firmware shards 0/4 and 1/4 | `0839453f`: PASS; control campaign 825/825; sink suites 11/11 at each shape | Executed at final head |
| Firmware shards 2/4 and 3/4 | `7650a02d`: PASS | Carried; final delta only changes sink tests/plants and their README, outside these AECP/SRP campaign inputs |
| Firmware coverage | `0839453f`: PASS, 40 files; both changed production files 100% lines and branches after documented exclusions | Executed at final head |
| Twin, twin-plants, twin-maps, twin-maps-plants | `7650a02d`: all rc 0 | Carried; production sources and these harnesses unchanged afterward |
| Receive monitor | `7650a02d`: flat/stack/lockstep pass; N=8 format contract 96 checks, zero failures; four engine plants caught plus unmutated control, 5/5 | Carried; receive-monitor input set unchanged afterward |
| Split boot, both shipping shapes | `7650a02d`: PASS, zero findings | Carried; final platform images byte-identical |
| Platform ledger and memory tests | `0839453f`: PASS; ledger controls 9/9 | Executed at final head; independent focused boundary probe also passes |
| Budget `run.py --self-test`, flip/load checks and controls | `0839453f`: zero self-test failures; load PASS; flip 616/616 controls | Executed at final head |
| Docs, TOC/anchors, inventory and generated checks | Final-head receipts pass applicable checks; register/HDL reference and WaveDrom supplements included | CI tool inventory remains an explicit environment refusal, not a pass |

The four-shard campaign has applicable evidence, but four fresh executions at `0839453f` are not claimed. The control campaign grew from 823 to 825; no plant was dropped. The final three-file delta is explicit in history, and phase ownership is in `test_ctrl_firmware.py` and `test_ctrl_firmware_shards.py`.

Independent flip/load checks, their controls, docs check and diff check passed their expected outcomes. The all-points flip command returns 1 for exactly the ruled eleven 8x8/2if findings. Its stdout is byte-identical to published final stdout and inspected earlier step-11/12 outputs after removing command/head/exit wrappers. No budget implementation input changed from `b1f1161b`. Load remains 0.522 at 1x1/1if and 0.744 at 8x8/1if. The optional two-interface findings are neither new nor silently treated as passes. Independent controls refuse 616/616 flip plants and 28/28 load plants.

**Images and timing.** All twelve CPU-budget hash rows are identical across published step-11, step-12, round-2 and final receipts. Every final platform whole-file hash equals round 2's: `e937ca14…`, `3e67aaea…`, `4818bec6…`, `9c67031d…`. Loaded-section hashes of the shipping images match the gating builds: `ff21e09148d33d7ea92ec3dd416b16946daaa10b5b1964d916830a760478eeb8` and `f2f81d5fa8597a7f9e8346a12a1cf76823f6226151761b010c40a3fd1c101f6c`.

The gating bitstream receipts are `550e2d8d3b72a8aca6feff387b83677dbf4ab7c6ea84a318d17bf1f5c66f6543` at 1x1/1if and `b449f2caa3675d2a70a536e5dcd379bdef100da9240d0679dff4b71d796f730b` at 8x8/1if. Their published identity gates bind manifest, firmware, placement and bitstream. Whole ELF equality is used where appropriate; the gating links use loaded sections because symbol order can differ.

Published release-export comparisons support unchanged loaded release bytes, init files, and Verilog outside comments across this delta. Build-directory intermediates and debug/path metadata differ; this is not a claim that every file in two export directories is identical. Raw ELFs and bitstreams are absent from the published packet. Their byte comparisons are the author's published receipts, corroborated by unchanged relevant production inputs, not an independently rebuilt binary comparison.

`receipts/step12/images/split-gateware-12.txt` identifies the 1x1 ROM bank change from 512 to 1,024 words, its address/decode changes, and 32,610 to 32,714 LUTs. Total block RAM remains 80. The 8x8 export retains bank depths and placed utilization, 94.5 total block-RAM tiles. Both fit the selected device. Three-directive route receipts meet [#818's floor](https://github.com/kebag-logic/milan-fpga/issues/818) on their best directive: 1x1 +0.334/+0.034 ns and 8x8 +0.073/+0.034 ns. The 8x8 AltSpreadLogic_high +0.006 ns setup miss remains visible.

Round 2 changes only init contents relative to those step-12 exports; final head changes no product image. Independently of that carry, actual round-2 gating builds have signoff receipts under `receipts/step12b/gating/`, distinct from the discarded diagnostics:

| Gating build | Slow corners WNS / WHS | Fast corners WNS / WHS | Result |
|---|---|---|---|
| 1x1/1if | +0.276 / +0.102 ns | +1.641 / +0.036 ns | Floor met at all four corners |
| 8x8/1if | +0.176 / +0.102 ns | +1.523 / +0.036 ns | Floor met at all four corners |

**F-G4 and documentation.** Public PR Status records F-G4 as withdrawn, agreeing with the published second board reading. The test machine observed the inline capture tap's advertisement; the DUT PHY advertised 1000BASE-T full duplex alone. No diagnostic or candidate fix entered the train, as the exact diff confirms. This resolves that finding's premise only, not physical calibration or stream, power and soak acceptance. The separately disclosed save/PHY scheduling observation is outside this step-12 delta; it is not certified fixed or reclassified as a wording defect here.

**Prior findings and wording residue.** These were inspected after `independent-pass.md` was written. Public sources: [R866-1](https://github.com/kebag-logic/milan-fpga/pull/945#issuecomment-6982365106), [R866-2](https://github.com/kebag-logic/milan-fpga/pull/945#issuecomment-6985380333), [R865-1](https://github.com/kebag-logic/milan-fpga/pull/945#issuecomment-6986847711). No earlier blocking finding remains to clear.

- **R866-1-R1; RESIDUE; Docs; RETAINED.** Artifact: `sw/firmware/ctrl/test/test_plat_boot.cpp:91,95,116,119`. Authority/evidence: owner source-comment rule; the unchanged blob retains the named labels. Impact: wording convention only. Exact outcome: remove the B24 prefix, parenthetical Phy label list and L5/L6 prefixes at those lines, retaining behavior and issue/clause references. Verification: comment-only diff, executable tests unchanged. The other review's differing label interpretation does not silently close this reviewer's retained item.
- **R866-1-R2 / R865-1-RES-2; RESIDUE; Docs; RETAINED.** Artifact: `sw/firmware/ctrl/plat/ctrl_split_hot.txt:14,19`. Authority/evidence: owner rule forbids issue-comment IDs in source comments; both IDs remain in the unchanged blob. Impact: wording only. Exact outcome: delete `issuecomment-6959600243` and `issuecomment-6967930396` and redundant adjacent commas, retaining #665, dates, item numbers and procedure. Verification: header-only change; ordered entries and trace hashes unchanged.
- **R865-1-RES-1; RESIDUE; Docs; RETAINED.** Artifact: `docs/design/AREA_BUDGET.md:139,141`. Authority/evidence: unchanged sentences describe the superseded record/directive; `syn/ooc/pp_resource_baseline.json` contains the accepted re-record. Impact: reader-facing wording only; the gate reads the unchanged JSON. Exact outcome: say the #883 measurement *was* the record until the flip train's record-only re-record of 2026-11-18, and the selected route directive has since been ExtraTimingOpt. Preserve figures and #640 debt. Verification: prose-only correction against the JSON; docs checks pass. The prior report's second line reference was 142; the sentence is at 141 here.
- **R866-2-R1; RESIDUE; Docs; RESOLVED.** Artifact: public PR Status and Composition commits. Evidence: Status names final `0839453f`, acknowledges R866-2 at `b1f1161b`, and the composition table includes the inventory-regeneration commit and its cause. Impact/outcome: the stale-head narrative is removed. Verification: the body preserves actual execution-head attribution.
- **R866-3-R1; RESIDUE; Docs; OPEN.** Artifact: public PR Known limitations, bullet beginning “The release export comparison”. Authority/evidence: it says the comparison “was last made at step 9”, while the same body's image section and `receipts/step12c/images/release-export-14.txt` document later comparisons. Impact: an obsolete duplicate narrative sentence; no measurement, figure, verdict, test, code, generated artifact, clause claim or privacy rule changes. Exact outcome: delete that obsolete bullet; retain the image section's precise loaded-byte comparison and execution-head labels. Verification: PR prose-only deletion, no evidence or numeric claim changed.

No additional suggestions are raised. Open items above are wording residues under the owner's rule and leave the lenses CLEAN.

**Reviewer-owned ledger.** Each row applies the lens to this delta and carries only untouched earlier coverage.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #946 acceptance; #665 ROM/composition rulings; REGISTER_MAP.md:3323,3530,3550; exact patch carriage; final ledger and unchanged budget outputs | R866-3; untouched R866-2/R866-1 carried | 0839453f6d7135063e904bcaf4ac1852ad6b522a |
| RTL | CLEAN | Three remerge diffs; unchanged RTL/mailbox dependencies; split-gateware-12.txt; gateware13.txt; final image hashes; gating signoffs and identity receipts against #818 | R866-3; untouched R866-2/R866-1 carried | 0839453f6d7135063e904bcaf4ac1852ad6b522a |
| Robustness | CLEAN | test_ctrl_memory.py:226 and real refusal arm; ten ledger mutations; explicit 63.5 rejection; nine final ledger controls; retained N=8 boundary/rebind tests and plants | R866-3; untouched R866-2/R866-1 carried | 0839453f6d7135063e904bcaf4ac1852ad6b522a |
| Tests | CLEAN | Shard ownership and receipts; final coverage; twin/boot/receive-monitor carry inputs; independent flip/load checks and 616/28 controls; no test/plant removal | R866-3; untouched R866-2/R866-1 carried | 0839453f6d7135063e904bcaf4ac1852ad6b522a |
| Docs | CLEAN | Seven resolved ledger/prose files; RESOLUTIONS.md:308-370; final PR body and F-G4 attribution; generated/docs receipts; prior-finding dispositions above | R866-3 | 0839453f6d7135063e904bcaf4ac1852ad6b522a |

**Limits and pending manager duties.** Source validation is distinct from the final current-dev merge candidate. There is no manager source bank at this exact head. No full parent/processor/gPTP/builder/synthesis bank, fresh route, hardware operation, host replica runner or container run was performed. Large-log stubs expose hashes and tails, not absent full contents. Hosted execution/skipping was not audited; CI-environment refusals remain explicit. Physical calibration is NOT RUN; field skips are not hardware proof.

The manager still owns the candidate against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, its builder/native banks and published receipts, hosted/local-replication acceptance distinguishing executed/skipped contexts, independent-review completion, hardware qualification, explicit merge authorization and containment. Preserve #640 resource debt, ROM debts, the optional 8x8/2if disposition and retained residues. #946's physical stream, power-cycle and soak acceptance is not discharged by simulation or image identity.

**Reproduction and integrity.** From the detached clone, portable scripts take the packet directory: `prepare_evidence.py`, `audit_composition.py`, `audit_receipts.py`; `run_probes.py` also takes a Python executable with documented simulation dependencies. `probe_ledger.py` uses `TMPDIR` under packet `scratch/`. `verify_checkout.py` runs from the candidate root. The archive object must already be fetched. Disposable builds and extractions stay under `scratch/`; no source file was edited.

`final-integrity.json` proves raw tracked blob bytes, executable/symlink modes and index entries for 1,932 root blobs and all five required initialized submodules. Pins: protocol processor `801ef2283ec793e35a2590fc6593c90313a64041`, gPTP processor `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, protocol stack `715589c1db7cf67e2f3259fd7083ebc7f0923376`, SRP library `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`. Root and submodules are clean; the unrelated external submodule is unused. All foreground probes have ended. `MANIFEST.sha256` lists every publishable receipt and script; scratch is excluded.

R866-3 FINISHED
