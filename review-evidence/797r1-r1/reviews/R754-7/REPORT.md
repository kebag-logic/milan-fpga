[R754] POSITIVE - exact head 1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33

Round R754-7, external independent review of PR #825 (issue #797, register reference lane), delta round.
Tree `f6a15be8c87d2ec70163e7a0b8cb94cd32ff6afc`. Previous round R754-6 was POSITIVE at `2c500d0a`.
Live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c` is a parent of the merge `57264e30`, and `git merge-base 1de759d3 0a75aa77` is `0a75aa77`.
The lane's own base moved from `1f29f189` (round 6) to `0a75aa77` (this round).

## Scope and method

The delta is the lane's net patch at round 7 (`0a75aa77..1de759d3`, 266 files) against its net patch at round 6 (`1f29f189..2c500d0a`, 265 files).
I compared them file by file, using the added and removed lines of each file.
The file set is the same except for one addition, `docs/DOCUMENTATION_AUDIT.md`.
Only five shared files carry a different patch: `.github/workflows/docs.yml`, `scripts/ci_events.py`, `docs/design/CSR_REGISTER_NOTES.md`, `docs/reference/REGISTER_MAP.md` and `scripts/register_map_soc.json`.
`REGISTER_MAP.md` and every file under `docs/diagrams/regmap/` are byte-identical to round 6. The patch differs only because dev's old page, the base of the patch, changed.
Every file outside the lane's 266 carries dev's bytes unchanged, so the merge dropped nothing of dev's.
All other lane code (the generator, decoder, sweep, descriptions and selftests) is unchanged since round 6 and keeps its round-6 verdict.
Only the merge's interaction with dev re-opens it. I checked that interaction below.

I verified the author's round-7 receipts on evidence commit `d04d7dfa`: all 226 `author-r7/` entries match `published_sha256` in `review-evidence/797r1-r1/MANIFEST.json`, with no unlisted file (`receipts/evidence_manifest_author-r7.txt`).
The evidence commit is not GPG-signed (`%G?` = N). The integrity claim rests on the manifest hashes.
Then I ran my own probes in disposable shared clones under `scratch/`. The generator needs the pinned `wavedrom==2.0.3.post3`, so I installed it in a disposable venv. Without it, `--check` refuses with rc 2, which is correct fail-closed behaviour (`receipts/gates/head_gen_check_no_wavedrom.log`).

## Checks against the five focus items

1. **Conflict resolutions.**
   - `docs.yml`:
     - `.github/ci-templates/docs.yml` carries both dev's "Documentation inventory freshness gate" and the lane's "Register reference freshness gate".
     - `ci_gate_workflows.py --check` gives rc 0 at the head (`receipts/gates/head_ci_gate_workflows_check.*`).
     - Running the generator in write mode on a clean head clone left the tree byte-identical, so the committed workflow is exactly the generator's output.
     - The register step is `gate_51`. The later ids each moved up by one (`ci_step_54`, `gate_52`, `ci_step_56`, `ci_step_57`).
   - `check_doc_style.py`: `DOCUMENTS` keeps both `REGISTER_MAP.md` and dev's `STRICTER_READINGS.md` (lines 37-38). The gate prints `OK (25 current documents)`, rc 0.
   - `REGISTER_MAP.md`:
     - Dev changed no CSR input: `git diff 1f29f189 0a75aa77 -- hdl/common/csr` is empty.
     - `--check` is fresh at the merge and at the head, and the page is byte-identical to round 6.
     - Dev's two old-page edits are kept. The #599 sentence was already on the lane's page and notes.
     - The #839 sequencing text appears verbatim, exactly once each, in `CSR_REGISTER_NOTES.md`'s MAC_ADDR_LO and MAC_ADDR_HI cells (lines 188 and 192). That is the 839-character LO addition and the 64-character HI addition, compared programmatically against dev's page.
     - Each register section links to those notes (`REGISTER_MAP.md:478`, `:492`).
     - The same contract is in the firmware contract, `BAREMETAL_FIRMWARE.md:113-114` and `:217`.
2. **SoC extract refresh (`c73cecf1`).** The 8 changed constants are dev's #842 identity, which I decoded independently:
   - station MAC `0x014C`/`0x4B4C4B02` = `02:4B:4C:4B:4C:01`, matching `configs/endstation_ax7101_1x1_tdm8.yaml:67`;
   - entity ID `0x024B4CFF`/`0xFE4B4C01`, the EUI-64 of that MAC, matching `entity_id: mac-derived`;
   - model ID, AEM image CRC and `csr_csv_sha256`.

   I re-derived the csv and aem part of the extract from the author's published head export. The hash, constants, CSR registers, banks, memory regions and processor windows all match the committed file. Against the merge's file, exactly those 7 constants and the hash differ (`receipts/soc/partial_extract.txt`).
   The datapath-parameter part needs the export's `gateware/`, which is not published, so I did not compare it. `c73cecf1` did not change that part.
   Whether anything should gate the file: see S1.
3. **`ci_events.py` step count (`1de759d3`).**
   - At head, `CARRIER_STEP_LISTS[(docs.yml, docs-check)]` has 53 entries.
   - At the merge `57264e30`, `ci_events.py --selftest` fails exactly 7 arms. Each one expects "52 steps" but finds 53 (`receipts/gates/merge_ci_events_selftest.*`).
   - At the head, the selftest passes 2215 items and 5514 arms with 0 failures, and `--check` gives rc 0.
   - The commit touches exactly the 7 literals both sides had edited.
   - Plant p7: removing the register step from the template and regenerating makes `ci_events.py --check` fail with rc 1 ("must carry exactly 53 steps ... (found 52)"), so the new gate cannot be dropped silently.
4. **Freshness-gate plants.** I wrote my own script, `plants.py`, and ran it on fresh clones of the head. 7 of 7 plants behaved as expected (`receipts/plants/`):

   | Plant | rc | Result |
   |---|---:|---|
   | control | 0 | fresh |
   | dev's hand-written page | 1 | STALE |
   | `MAC_IFG` reset change in the flop and the ROM | 1 | STALE, 4 files |
   | field signal `mac_ifg` renamed `mac_gap` (4 word matches; the port `o_mac_ifg` is left alone) | 1 | fingerprint STALE |
   | `A_ETH_GUARD` renamed `A_ETH_LOCK` | 2 | REFUSED, "needs a name and a purpose" |
   | comment-only edit | 0 | fresh |
   | extra: description-only prose edit | 1 | STALE |

   `--selftest` passes 61/61 at the head.
5. **Inventory and docs.yml steps.**
   - `docs_inventory.py --check` gives rc 0, "548 lines, fresh".
   - The audit's +1 design page is `CSR_REGISTER_NOTES.md`.
   - The author's `verify_docs_yml` receipt reports 66 steps ran, 31 not run with a reason, 0 bad. No `gate_*` step is among the not-run ones: those are package installs already satisfied on the host, plus hosted-only record and cancel steps.
   - The `gate_51`, `gate_46` and `gate_41` receipts name the head on their first line and have rc 0.
   - The earlier `c73cecf1` run records the `gate_41` failure that led to `1de759d3`.

**Hosted, informational only.** Hosted runs at this exact head failed broadly: `docs-gates-0/1/2`, `elaborate-gates-*`, `verilator-suites` and `yosys-*`. The failing step is "Install the pinned sv2v release", with `curl: (22) The requested URL returned error: 504`, a download error from upstream. `docs-check` fails only at its aggregator, "Require every gate exactly once".
The delta does not touch that install step. These are infrastructure failures, not results of executed gates (`receipts/hosted_check_runs.tsv`). Hosted acceptance belongs to the manager.

## Findings

No BLOCKER, MAJOR or MINOR finding.

**RES1 - RESIDUE - Docs - merge commit `57264e30` subject.**
- Evidence: the subject says the merge was "regenerating the workflow, page and inventory". The page and its diagrams came out byte-identical, so only the workflow and the inventory changed. The lane cannot amend the commit.
- Impact: wording only. It changes no artifact, measurement or verdict.
- Exact fix: no history rewrite. The PR body's round-7 summary should say "ran the page generator, which wrote `REGISTER_MAP.md` byte-identical", as `author-r7/HANDOFF.md` already does.

**RES2 - RESIDUE - Docs - `author-r7/HANDOFF.md` gate table, row `docs-gates-2 | gate_41`.**
- Evidence: the row's log column names `docs-gates-2__gate_41.log`. The published file is `docs-gates-2__gate_41.log.tail`, and it states the full log's sha256 (`7c7563…`, 355074 bytes). `INDEX.md` lists the `.tail` name correctly.
- Impact: wording in a receipt table only.
- Exact fix: change that cell to `docs-gates-2__gate_41.log.tail (tail; full log sha256 7c7563376187…)`.

**S1 - SUGGESTION - Robustness, Tests - `scripts/register_map_soc.json`.**
- Evidence: nothing in CI compares the extract with the builder. The docs job runs `--check` without `--soc-from`, because it cannot run a LiteX export. Dev's #842 made the file stale without any gate noticing. The 7 identity constants that changed, and `csr_csv_sha256`, are read by nothing that renders: they appear in neither the page, the decoders nor the memory-map diagram, so no published byte depended on them.
- Impact: the next config identity change will silently re-stale the extract again. That is harmless today, but it erodes the file's claim to be the export.
- Optional outcome, any one of:
  - (a) drop the constants the page does not read from the extract;
  - (b) add a cheap no-LiteX consistency check of `milan_station_mac_*` and `milan_entity_id_*` against `platform.mac_address` in the shipping YAML;
  - (c) have the manager's builder bank run `gen_register_reference.py --check --soc-from <export>` at the candidate merge.

**S2 - SUGGESTION - Docs - `REGISTER_MAP.md:466-492` (MAC_ADDR_LO and MAC_ADDR_HI).**
- Evidence: the page's own text for these two registers does not mention the #839 rule that holds transmitters until both halves are written. It is a programming-order rule, reached only through a link labelled "Rationale and history". The rule is correct and present verbatim in the design notes and in the firmware contract, so no current document contradicts the code.
- Optional outcome: add one sentence through `register_descriptions.json` saying that transmitters taking their source address from this pair are held until both halves are written, with a link to `BAREMETAL_FIRMWARE.md`'s step. Doing it in a later content round respects this sync round's no-new-content rule.

**S3 - SUGGESTION - Docs - `docs/DOCUMENTATION_AUDIT.md:529-544` (D0 rows on `REGISTER_MAP.md` and `REGISTER_MAP_CLASSES.md`).**
- Evidence: 12 D0 rows on `REGISTER_MAP.md` and 5 on `REGISTER_MAP_CLASSES.md` now read "re-verify: quote not found", because the generated page removed the quoted text.
- I checked whether the substance still holds and found that the page applies D0's fixes:
  - D0-006 → `:1769` cites 35.2.2.7.2 (Table 35-3);
  - D0-007/008 → `:1957`, IEEE 1722.1-2021 Table 7-156 and Milan Table 5.6;
  - D0-015 → `:561`, PHY_RESET inert, with `milan_mac_phy_crg_reset` named as the reset that reaches the pin;
  - D0-016 → `:2329`/`:2360`;
  - D0-058 → `:2907`, bindings persist through the restore walk;
  - none of the D0-040/041/043/044 quotes appears in the page, the classes page or the notes.
- Optional outcome: the D0 ledger owner closes these rows against the page lines. That is outside this sync round.

## Prior public review findings at this head

I read these only after my own pass. The two round-6 reports (R753-6 and R754-6, both POSITIVE at `2c500d0a`) record no open BLOCKER, MAJOR or MINOR. All earlier MINORs were resolved there. The rows below are what they carried forward.

| Prior item | State at `1de759d3` | Evidence |
|---|---|---|
| R753-5 F1 / R754-5 F1 (MINOR, Tests) | Resolved (round 6), stays resolved | `scripts/register_read_sweep.py` byte-identical to `2c500d0a` |
| R753-6 S1, S2; R754-6 S1, S2 (SUGGESTION, sweep state order and wording) | Retained, optional | `register_read_sweep.py` unchanged |
| R753-5 S1 (SUGGESTION, "since" anchor) | Retained, optional | `register_descriptions.json` and `REGISTER_MAP.md` unchanged |
| R754-4 S1, S2 (SUGGESTION, `register_sv.py`) | Retained, optional | `register_sv.py` unchanged |
| R753-3 RES2 | Retained, residue checklist | `REGISTER_MAP.md:4503` unchanged |
| R753-3 RES3 | Retained, residue checklist | `CSR_REGISTER_NOTES.md:974` unchanged; the file's line count is the same (1285), so the line numbers are unchanged |
| R754-3 R1 | Retained, residue checklist | `CSR_REGISTER_NOTES.md:78` unchanged |

None of these was in this sync round's scope, and none blocks.

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #797 acceptance and rules ("single source"; "no document marked current contains a statement contradicted by the code"); #839 text carried verbatim to `CSR_REGISTER_NOTES.md:188,192` and present in `BAREMETAL_FIRMWARE.md:113-114,217`; SoC identity decoded against `configs/endstation_ax7101_1x1_tdm8.yaml:67`; D0 fixes on `REGISTER_MAP.md:561,1769,1957,2329,2360,2907` | R754-7 | `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` |
| RTL | CLEAN | Lane patch touches no `hdl/`, `configs/`, `sw/litex` or `sw/firmware` file (0 files); `hdl/common/csr` unchanged `1f29f189..0a75aa77`; dev's `milan_datapath.sv` (+119/-11, #839) leaves the fingerprinted `milan_csr` instance unchanged (`--check` fresh at merge and head; `rtl_fingerprint.txt` unchanged) | R754-7 | `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` |
| Robustness | CLEAN | Generator fail-closed: rc 2 refusal without the pinned wavedrom and on an undescribed register (p4); plants p1-p3 and p6 STALE, p5 fresh; p7 gate removal caught by `ci_events.py --check`; SoC extract stale at merge, fresh at head (S1 optional) | R754-7 | `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` |
| Tests | CLEAN | `ci_events.py --selftest`: 7 FAIL at `57264e30`, PASS 5514 arms at head; `gen_register_reference.py --selftest` 61/61; `plants.py` 7/7; `ci_gate_workflows.py --check` and write-mode regeneration byte-identical; author `verify_docs_yml` 66 ran / 0 bad, manifest-verified | R754-7 | `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` |
| Docs | CLEAN | `REGISTER_MAP.md` and `docs/diagrams/regmap/*` byte-identical to round 6 and `--check` fresh; `check_doc_style.py` 25 documents OK; `docs_inventory.py --check` fresh; `DOCUMENTATION_AUDIT.md` +`CSR_REGISTER_NOTES.md` row; `HANDOFF.md` accuracy (RES1 and RES2 are residue only) | R754-7 | `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` |

Coverage applies to the merge candidate only if no lens-scoped artifact changes after `1de759d3`. The manager's current-dev candidate build is a separate object, and this ledger does not cover it.

## Limits

- I ran no full parent, processor, gPTP, Yosys or builder bank, no Docker or act, and no Verilator build. I used no hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.
- I did not reproduce the builder export. The extract's datapath-parameter part is unverified by me, because `gateware/` is not published.
- My docs.yml evidence is my own runs of the register, workflow, events, style and inventory gates, plus the author's manifest-verified receipts for the rest. I did not rerun every docs.yml step.
- The hosted exact-head runs did not execute their gates, because of the sv2v 504 failure.
- To read the evidence commit, I fetched `d04d7dfa` into the review clone's object store (`FETCH_HEAD`). That changed no tracked byte.

## Pending manager duties

- Re-run the hosted docs, elaborate, verilator and yosys workflows at this head once the sv2v download recovers, and accept them.
- At the merge turn, validate the current-dev candidate: builder and native banks, and optionally `gen_register_reference.py --check --soc-from <export>` (S1(c)).
- Carry RES1 and RES2 to the residue checklist.

## Clone restoration

- The review clone is at `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33`, with worktree and index clean and no untracked files.
- The index equals `HEAD`'s tree in mode and oid for all 1731 entries.
- The submodule gitlinks and checkouts all match and are clean: gptp-processor `1616fc8f`, protocol-processor `92100657`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`. `external` is not initialised, gitlink `efeb541a`.
- All probes ran in shared clones under `scratch/`.

R754-7 FINISHED
