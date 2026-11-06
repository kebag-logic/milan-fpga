# HANDOFF — issue #839, round 4 (dev sync and inventory regeneration only)

Status: REVIEW READY. Nothing pushed; the manager pushes PR #841.

| | |
|---|---|
| Branch | `839-boot-source-address` |
| Round-3 head (start) | `3c22947861e5c057a6195ad46e1a379d67592559` (R773-3 and R774-3 POSITIVE) |
| New base (live `origin/dev`) | `cc204c6fd2349b543d73f15c97162a2c4434c86e` (PR #815) |
| Merge commit | `dc7eebff351074991e8b4cae9f0f866608a3e8d9`, parents `3c229478` and `cc204c6f`, subject `Merge dev cc204c6f into 839-boot-source-address`, no body |
| Round-4 head | `4f210018e6556a9753ed409885d82744c8f5effa` |
| Merge base (`git merge-base --all origin/dev HEAD`) | one: `cc204c6fd2349b543d73f15c97162a2c4434c86e` |
| Origin | `https://github.com/kebag-logic/milan-fpga.git` |
| Issue comments | `[A731d] TAKEN` (issuecomment-6674674241); `[A731d] REVIEW READY` (issuecomment-6675710674) |

## Changes

1. **Merge** (`dc7eebff`): `git merge --no-ff origin/dev`, with the SHA resolved by `git rev-parse`.
   - **Conflicts: none.** Git's ort strategy auto-merged the one file both sides touched,
     `docs/reference/REGISTER_MAP.md`. Dev changed line 428 (the #599 link-cycle finding
     link). This PR changed the `MAC_ADDR_LO/HI` rows (lines 414-415). Both are kept, as merged.
   - The merge brings exactly dev's 10 files onto the round-3 head. On dev, it adds exactly
     this PR's files (`receipts/merge/merge-and-regeneration.txt`). No submodule pin changed.
2. **Regeneration** (`4f210018`, one commit): `python3 scripts/docs_inventory.py --write`
   and nothing else. It changes only `docs/DOCUMENTATION_AUDIT.md`, 13 lines:
   - `:30-31`, `:34`: the line totals (current 73,487 to 73,640, stale 10,638 to 10,643, total 92,127 to 92,285).
   - `:124`: `CHANGELOG.md`, 1087 to 1111 lines.
   - `:273`: `BAREMETAL_FIRMWARE.md`, 2335 to 2338.
   - `:337`: `TESTING.md`, 1935 to 1937.
   - `:435`: `tb/verilator/milan_dp/README.md`, 1688 to 1817.
   - `:488-492`: the lines that D0-011, D0-012, D0-013, D0-061 and D0-062 cite in `BAREMETAL_FIRMWARE.md`, moved by 3.
   - `:540`: the line D0-057 cites in `TESTING.md`, moved by 2.

   The generator does not write `scripts/docs_inventory.json`, so that file is unchanged.
   Before this commit, `--check` on the merged tree failed with the manager's figures
   (`receipts/merge/inventory-check-before.log`). No clause applies: these are generated
   counts of this PR's existing #839 page edits.
3. Nothing else changed: no RTL, harness, test, hand-written document or submodule.

## Checks and planted mutants

This round adds no check. The leg's twelve planted controls are unchanged. I ran them at the
round-4 head (`receipts/gates/lane/bootsa_mutants.log`), and the named words caught each one:

| Planted mutant | Failing words |
|---|---|
| the defect as shipped: no hold and no stamp | "no frame carries the all-zero source address"; "no CSR-addressed transmitter starts a frame before the station MAC is written"; "every MSRP frame's source address is the station MAC" |
| no hold: the stamp alone | same three as above |
| no stamp: the hold alone | "no frame carries the all-zero source address"; "every MSRP frame's source address is the station MAC" |
| `MAC_ADDR_LO` alone completes the pair | "pair: MAC_ADDR_LO alone opens no CSR-addressed transmitter" |
| `MAC_ADDR_HI` alone completes the pair | "pair: MAC_ADDR_HI alone opens no CSR-addressed transmitter" |
| the stamp lands on octets 0 to 5 | "every MSRP frame's destination address is its protocol's"; "every MSRP frame's source address is the station MAC" |
| the stamp's beat position survives a frame's last beat | "every ADP frame's destination address is its protocol's" |
| no hold on MAAP, AAF and CRF | "early-enable, MAAP on: no MAAP frame leaves before the station MAC is written"; "... MAAP on: no CRF frame ..."; "... MAAP off: no AAF frame ..." |
| no hold on MAAP alone | "early-enable, MAAP on: no MAAP frame leaves before the station MAC is written" |
| no hold on the AAF talkers alone | "early-enable, MAAP off: no AAF frame leaves before the station MAC is written" |
| no hold on the CRF talker alone | "early-enable, MAAP on: no CRF frame ..."; "early-enable, MAAP off: no CRF frame ..." |
| the stamp's beat position wraps | "every control-lane octet outside 6 to 11 leaves the stamp as it entered" |

## Gate table (round-4 gate set), head `4f210018`, each gate on a clean clone

| Gate | Result | rc | Receipt |
|---|---|---:|---|
| `git merge-base --all origin/dev HEAD` | one base, `cc204c6f` | 0 | `gates/lane/merge_base_one.log` |
| `git diff --check cc204c6f HEAD` | no output | 0 | `gates/lane/diffcheck.log` |
| `python3 scripts/docs_inventory.py --check` | `documentation inventory: OK (540 lines, docs/DOCUMENTATION_AUDIT.md is fresh)` | 0 | `gates/lane/docs_inventory_check.log` |
| `python3 scripts/docs_inventory.py --selftest` | `documentation inventory selftest: OK (50 controls)` | 0 | `gates/lane/docs_inventory_selftest.log` |
| `make -C tb/verilator/milan_dp bootsa` | `== bootsa: checks: 67   failures: 0 ==`, `RESULT: PASS` | 0 | `gates/lane/bootsa.log` |
| `make -C tb/verilator/milan_dp bootsa-mutants` | `13 checks: 13 PASS, 0 FAIL` | 0 | `gates/lane/bootsa_mutants.log` |
| every `run:` step of `.github/workflows/docs.yml` | `65 steps ran, 31 not run with a reason, 0 bad`. Every job's clone was clean after it. The builder legs gave `ALL GATES PASS EXCEPT 1 NOT RUN` and `ALL GATES PASS EXCEPT 16 NOT RUN`. `gate_46`, the inventory freshness gate, passes | 0 (verifier) | `gates/docsyml/docs-yml-table.md`, `gates/docsyml/logs/` |

The lane clone's tree was clean after its gates (`gates/lane/tree-after.txt` is empty). The full
sweep was not run because it is not in the round-4 gate set. `scripts/ci_tool_inventory.py --check`
was not run either: it is tracked in #838 and is not this round's gate.

### docs.yml run attempts (environment fixes only, no code change between them)

The verifier's table comes from the final run. The logs of each failed attempt are under
`receipts/gates/attempts/`.

1. `attempt1-venv-removed`: an outside scratch cleanup deleted the round-3 virtualenv the
   runner pointed at while `docs-gates-2` ran. That job also hit the 10-minute tool limit and
   was stopped. I reran with this round's own virtualenv and home, in user service units.
2. `attempt2-sdk-copy`: `ci_step_13` failed in `docs-gates-1` and `docs-gates-2` with
   `SDK provenance mismatch`. I had copied the round-3 home, and the SDK receipt records the
   path it was installed to. I installed the SDK fresh with `scripts/ci_rv32_sdk.py --destination`
   (`attempts/sdk-install.log.tail`, `SDK fresh installation: verified`) and reran both jobs on
   fresh clones.
3. `attempt3-no-wavedrom`: `gate_13` in `docs-gates-0` failed with `the 'wavedrom' package is
   missing`. The step that installs wavedrom (`ci_step_10`: apt, then `pip install wavedrom==2.0.3.post3`)
   is not run here. Its stated reason is that the virtualenv already carries that wavedrom,
   which the new virtualenv did not yet. I installed `wavedrom==2.0.3.post3` and reran the whole
   job on a fresh clone.

### Runner and verifier

`receipts/gates/tools/run_docs_yml.py` and `verify_docs_yml.py` are the round-3 copies of the
829 runner and verifier, with the lane, virtualenv and home paths changed. `not_run.json` adds
one entry, `docs-gates-0/ci_step_55`: the hosted `ci_gate_receipts.py record` step, which was
`ci_step_54` until PR #815 added `gate_46`. `collect.py` copies logs into the receipts and
replaces the scratch, home and data prefixes. `ORIGINALS.sha256` in each directory holds the
hashes of the original bytes. One log is over 200 KB: `docs-gates-2__gate_41.log` (354,255 bytes).
Its size and sha256 are in `gates/docsyml/logs/LARGE-LOGS.txt`, and its last 20,000 bytes are kept.

## Outputs

- `PR-BODY.md`: the live PR #841 body with first line `[A731d]`, a Round 4 section, and updated
  status line, roles and inventory note. It still says "Relates to #839".
- `taken.md`, `review-ready.md`: the two issue comments as posted.
- `receipts/INDEX.md`: generated from the files present.
