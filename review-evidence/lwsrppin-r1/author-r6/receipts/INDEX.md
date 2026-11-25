# Receipts: round 6, the sync merge of dev-soft-core e608f8d8 (PR #992)

Head `2b98e219a5e2b0681f76be90083fc05e47a8f6c0`, the merge of `e608f8d8` into `67838b37`, local and not pushed. Every
file is text and under 200 KB. Scratch is under `/data-2/milan/tmp/lwsrppin-a834/r6/`. Raw logs carry local paths.

| File | Bytes | sha256 (16) | What it is |
|---|---:|---|---|
| `docs/docs_DOC_MAP.gen.py_--check.log` | 61 | `74408f0fbcdfc1c7` | a docs gate's log at 2b98e219 |
| `docs/docs_DOC_MAP.gen.py_--selftest.log` | 60 | `85ddf25d9a99974b` | a docs gate's log at 2b98e219 |
| `docs/docs_diagrams_submodule_boundaries.gen.py_--check.log` | 54 | `4f2d621c17d265a6` | a docs gate's log at 2b98e219 |
| `docs/docs_diagrams_submodule_boundaries.gen.py_--selftest.log` | 60 | `51bca8fb66fd6f0a` | a docs gate's log at 2b98e219 |
| `docs/docs_diagrams_timesync_chain.gen.py_--check.log` | 60 | `51058c96a481bf76` | a docs gate's log at 2b98e219 |
| `docs/docs_diagrams_timesync_chain.gen.py_--selftest.log` | 61 | `7c7ad79fa685d296` | a docs gate's log at 2b98e219 |
| `docs/run.txt` | 138 | `5b4549a8bdf83869` | the docs gates' head, porcelain before and after, and how each was run |
| `docs/scripts_check_diagram_pngs.py.log` | 66 | `05e0fcfa26a97494` | a docs gate's log at 2b98e219 |
| `docs/scripts_check_diagram_pngs.py_--selftest.log` | 59 | `918e8cc85a2a2b0d` | a docs gate's log at 2b98e219 |
| `docs/scripts_check_doc_style.py.log` | 47 | `680272641877f342` | a docs gate's log at 2b98e219 |
| `docs/scripts_check_submodule_docs.py.log` | 47 | `c4bbf250ee33a3cc` | a docs gate's log at 2b98e219 |
| `docs/scripts_docs_check.py.log` | 128 | `b521c0b022d41038` | a docs gate's log at 2b98e219 |
| `docs/scripts_docs_inventory.py_--check.log` | 78 | `5f7b6c432b31770d` | a docs gate's log at 2b98e219 |
| `docs/summary.txt` | 1,544 | `58887c40f543d3dc` | the 12 docs gates at 2b98e219: one line per gate with its rc, time and last line |
| `identity/identity.txt` | 2,894 | `14b8ff50c42bee48` | image identity at 2b98e219 against 67838b37: plat_ledger result, the 28-file comparison, the 8x8/1if and 1x1/1if ctrl ELFs, why gptp_ucode.hex differs |
| `identity/plat-ledger-2b98e219.log` | 14,065 | `e242649e37cb1eea` | plat_ledger.py --build-dir at 2b98e219, its log |
| `identity/sha-2b98e219.txt` | 3,796 | `9259c44818766930` | sha256 of every ELF/bin/hex plat_ledger.py --build-dir writes at 2b98e219 |
| `identity/sha-67838b37.txt` | 3,796 | `43a714649ee03535` | the same at 67838b37 (round 5's build) |
| `merge/blob-identity.txt` | 1,078 | `c631a1b543ac264a` | each of this PR's paths: HEAD's blob against 67838b37's; every path outside them against e608f8d8's (0 differ) |
| `merge/dev-delta-patches.txt` | 671 | `ce77362f0ba60809` | the whole-patch comparison (diagram files excluded) and why it is not byte-equal: SUBMODULES.md |
| `merge/dev-delta-per-path.txt` | 792 | `12ecb1c688ce8195` | 67838b37..HEAD against 2509db68..e608f8d8, path by path; SUBMODULES.md as git merge-file of the three sides |
| `merge/diagram-regeneration.txt` | 1,575 | `9620c6c7ead55c55` | the conflicts, how they were resolved (generator only), the word diff against each parent, the pins named, the generator's --check and --selftest |
| `merge/diff-e608-head.txt` | 3,030 | `14ba76b0906376d2` | git diff e608f8d8 HEAD --stat, and its path set against this PR's own (2509db68..67838b37): equal |
| `merge/merge-commit.txt` | 3,817 | `c1632443701626b0` | the merge commit's parents and subject, dev-soft-core's side (67838b37..HEAD --stat), the diagram files against e608f8d8 and the manifest diff |
| `suite/egress-ledger-selftest.log` | 13,379 | `9f1946557c9e0ea9` | egress_ledger.py --selftest at 2b98e219 (72 controls, 18 mutants) |
| `suite/run-self-test.log` | 180,157 | `0bca21ef117176a5` | run.py --self-test at 2b98e219, the ctrl_service_budget suite's self-test |
| `suite/run.txt` | 817 | `790f225f49dd3ce4` | run.py --self-test: head, start, end, rc, porcelain after |
| `tools/body.py` | 5,385 | `3f8cb242c9e748a3` | a script this round ran |
| `tools/index.py` | 3,183 | `3d472db86a38f8e4` | a script this round ran |
