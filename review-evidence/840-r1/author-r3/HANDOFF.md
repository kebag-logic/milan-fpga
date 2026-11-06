# HANDOFF: #840 round 3, [A732c]

Status: REVIEW READY for the manager. No push or PR edit performed.

- Original lane base: `604899c08ff1cd1830e1dd08b733109ef852400c`.
- Round-2 head: `cadb63b4985c0ad4fb7dc036a23bf9fe93eb6276`.
- Merged dev and sole merge base: `cc204c6fd2349b543d73f15c97162a2c4434c86e`.
- Validated head: `beb38447d07cceac5170ba0a35c7615f5714b7f7`.
- Repository identity and clean-tree evidence: [repository state](receipts/repository-state.json).

## Authorized commits

| Commit | Change |
|---|---|
| `c6b34bd08c` | Merge dev cc204c6f into 840-identity-link-cert |
| `af9a8a33ed` | Regenerate documentation inventory through its generator |
| `beb38447d0` | Six interface spellings replaced with `<host-iface>` |

All three commits have one-line messages without bodies or trailers.

## Changes and authority

| Artifact at head | Change | Governing clause |
|---|---|---|
| `ci/image/command-table.json`, `docs/README.md` | Automatic merge retained both sides | Round-3 instruction 1 |
| `docs/DOCUMENTATION_AUDIT.md:30`, `:314` | 214 pages, 177 current; stricter readings registered | Round-3 instruction 2; documentation generation contract |
| `tb/tools/avdecc_ctl.py:312`, `tb/tools/crf_vs_phc.py:30` | Interface defaults use `<host-iface>` | Round-3 instruction 3; CONTRIBUTING section 6 |
| `tb/tools/hive_compliance.py:6`, `tb/tools/hive_compliance_clusters.py:6`, `:8` | Usage lines use `<host-iface>` | Round-3 instruction 3; CONTRIBUTING section 6 |
| `tb/tools/torture_campaign.py:6872` | Fixture uses `<host-iface>` | Round-3 instruction 3; CONTRIBUTING section 6 |

The [merge import inventory](receipts/merge-imports.md) lists each imported file and its first changed line.

Merge conflicts: none. Reconstructing the automatic merge reproduces its committed tree exactly.
See [merge evidence](receipts/merge-verification.log).
Re-running the inventory generator leaves the validation clone clean: [regeneration evidence](receipts/inventory-regeneration.log).
No new protocol interpretation or protocol behavior was introduced this round.

## Clean-clone gates

Every row below ran at the validated head. Exit status was 0 for each listed gate.

| Gate | Result | Receipt |
|---|---|---|
| Full builder, `python3 sw/builder/test_builder.py --require-rv32` | See log's exact final summary and NOT RUN qualifications | [builder](receipts/gates/builder.log) |
| PHY peer, `python3 sw/firmware/nvm_hosttest/test_phy_firmware.py` | 26 PHY mutants and 5 boot-path mutants caught; PHY_BOOT_OK | [PHY](receipts/gates/phy_firmware.log) |
| Reviewer PHY mutant sets | 8/8 caught in each set | [R775](receipts/gates/r775_phy_mutants.log), [R776](receipts/gates/r776_phy_mutants.log) |
| `python3 scripts/docs_inventory.py --check` | Fresh | [check](receipts/gates/inventory_check.log) |
| `python3 scripts/docs_inventory.py --selftest` | 50 controls pass | [selftest](receipts/gates/inventory_selftest.log) |
| Documentation workflow local runner and verifier | 65 steps ran, 31 not run with a reason, 0 bad | [all steps and qualifications](receipts/docs-yml-table.md) |
| `git diff --check` against the sole merge base | No whitespace errors | [diff](receipts/gates/diffcheck.log) |
| `git merge-base --all HEAD origin/dev` | Exactly one, equal to merged dev | [base](receipts/gates/merge_bases.log) |
| `python3 push-privacy-check.py . origin/dev` | 0 private lines | [privacy](receipts/gates/privacy.log) |
| `cd tests && behave` | 14 features, 508 scenarios, 2330 steps pass | [behavior](receipts/gates/behave.log) |
| `python3 tb/tools/torture_campaign.py --self-test` | Exit 0 | [campaign self-test](receipts/gates/torture_selftest.log) |

The documentation runner and verifier are the supplied copies with local paths adjusted.
Their step table explicitly distinguishes local execution from hosted-only actions and already-satisfied installations.
NOT RUN rows are not claimed as successful executions.

No new check was added in round 3. Existing planted mutants and required failing words appear in the [mutation mapping](receipts/phy-mutation-map.md).
The reviewer mutation receipts also print each actual failed assertion.

## Scope and remaining review

Round-3 implementation is complete. The full sweep was not rerun, as explicitly instructed.
Earlier-round sweep and service measurements remain historical evidence, not new-head runs.
The companion processor issue remains outside this implementation.
Independent review, hosted checks, pushing and PR updates remain with the manager.
No closure keyword was added.

PR-BODY.md preserves the live PR body with its historical round-2 claims and adds the round-3 result at the top.
The TAKEN comment was posted once after checking public comments; REVIEW READY is posted after packet verification.

## Receipt handling

[INDEX.md](INDEX.md) is generated from the files actually present.
Logs use path placeholders; [raw-log-manifest.json](receipts/raw-log-manifest.json) records original sizes and SHA-256 digests.
Files larger than 200 KB are represented by their digest, size, and labeled excerpts.
No build tree, installed package, virtual environment or generated binary is included.

## Builder qualifications

- Full builder: ALL GATES PASS EXCEPT 2 NOT RUN
- Documentation builder leg 0: ALL GATES PASS EXCEPT 1 NOT RUN
- Documentation builder leg 1: ALL GATES PASS EXCEPT 16 NOT RUN

The inherited sequential scheduler was stopped without stopping its active documentation job. Independent remaining jobs ran in foreground sessions on separate clones; no gate was discarded or restarted.
