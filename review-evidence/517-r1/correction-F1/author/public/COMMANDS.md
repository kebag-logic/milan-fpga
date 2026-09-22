R245-1 reproduction commands and receipt guide

All source paths are supplied explicitly. Choose a fresh writable output directory outside the source checkout; scripts refuse existing per-probe output directories. Use the exact reviewed detached head and initialized pinned submodules. The examples retain the required `rtk` shell prefix. Python subprocess argv are recorded without shell interpolation.

```sh
rtk proxy python3 integrity.py /path/to/reviewed-repo initial-integrity.json
rtk proxy python3 focused.py /path/to/reviewed-repo /path/to/new-output/focused
rtk proxy python3 blackbox.py /path/to/reviewed-repo /path/to/new-output/blackbox
rtk proxy python3 policy_probes.py /path/to/reviewed-repo /path/to/new-output/policy-probes
rtk proxy python3 output_backpressure.py /path/to/reviewed-repo /path/to/new-output/output-backpressure
rtk proxy python3 make_backpressure.py /path/to/reviewed-repo /path/to/new-output/make-backpressure /path/to/new-output/blackbox/normal
rtk proxy python3 check_backpressure.py /path/to/new-output/output-backpressure/results.json
rtk proxy python3 check_backpressure.py /path/to/new-output/make-backpressure/results.json
rtk proxy python3 -B evidence_review.py /path/to/reviewed-repo /path/to/downloaded-evidence-root
rtk proxy python3 integrity.py /path/to/reviewed-repo final-integrity.json
```

`focused.py`: five commands, all exit 0 at this head. Individual stdout/stderr and exact argv/exits are in `focused/`.

`blackbox.py`: 15 positive/control cases accepted and six planted faults rejected, driver exit 0. It runs the complete original Makefile with fixture compiler and models; no Verilator compilation or full bank. The generated-input prerequisites are marked old with explicit `-o` flags only in the disposable fixture. Actual `run`, gPTP prerequisite and render ordering are executed. `MAKEFLAGS=-j8`, compiler limit 8. Each receipt preserves argv, outcome and individual predicates; ledgers preserve model argv and overlap snapshots. Deliberately mutated runner/Makefile copies remain in their fixture directories.

`policy_probes.py`: 264 expected literal CLI cases and five broadened-mask defects, driver exit 0. It creates synthetic Git inventories under the output directory. The original public 21-finding receipt, downloaded under `public/source-first-failure/29.log` beside this script, supplies the actual line references. Positive source literals are read from the reviewed checkout, never generated from production regexes. `results.json` marks the deliberate mutants rejected by the policy expectations; their individual gate exit 0 is the intentionally planted defect, not a source pass.

`output_backpressure.py` and `make_backpressure.py`: diagnostic drivers exit 0 after producing raw kernel/pidfd receipts and cleaning up. At the reviewed source, both following `check_backpressure.py` commands intentionally exit **1**, because owned processes have not exited/reaped while stdout remains blocked. Their draining positive controls must pass before that acceptance result is emitted. The initial exact-wait-channel setup failure is preserved in `output-backpressure/setup-failure.txt`; the successful direct diagnostic used the separate `output-backpressure-v2` directory. Reproduction scripts support this kernel's `anon_pipe_write` spelling.

`evidence_review.py`: consumes the downloaded public evidence tree and emits `source-scope-proof.json` plus `public-evidence-review.json`. It compares all four benchmark process-sample streams, logs, executable/input/header identities, the corrected manager's real milan_dp log, the 50+5 manager ledgers, and exact Git artifacts. It does not run those banks. Original measurements remain at 7ab1c8d0. The evidence root must have a `public/` directory laid out like the immutable source below.

Read-only public retrieval used these explicit APIs/metadata fields, with raw JSON stored here:

```sh
rtk proxy gh pr view 524 --repo kebag-logic/milan-fpga --json number,title,body,headRefOid,baseRefOid,baseRefName,headRefName,state,isDraft,commits,files,comments,reviews
rtk proxy gh issue view 517 --repo kebag-logic/milan-fpga --json number,title,body,comments,labels,state,assignees
rtk proxy gh api repos/kebag-logic/milan-fpga/issues/comments/5783078964
rtk proxy gh api 'repos/kebag-logic/milan-fpga/git/trees/7c2f4357167e5398524f7980ab1a09690256544f?recursive=1'
```

Linked issues 259, 386, 445, 444 and 523 were read with `gh issue view NUMBER --json number,title,body,comments`. No Actions/run/check endpoint was queried. Public files were fetched from `https://raw.githubusercontent.com/kebag-logic/milan-fpga/7c2f4357167e5398524f7980ab1a09690256544f/review-evidence/517-r1/` and their Git blob SHA-1s checked against the tree inventory before writing. `public-download-receipts.json` records 462 initial files; `sample-download-receipts.json` records all four large raw sample streams. These downloaded files are evidence, not scripts executed with host/Docker authority. No act_ci copy or selftest was executed.

`download_public.py` can recreate those precise downloaded paths from the two receipt lists, with SHA-256 verification. It does not discover or retrieve unrelated files.

The approved scoped Verilator command was used only for identity after hashes matched:

```sh
rtk proxy $VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator --version
```

`tool-identity.json` records the wrapper, driver and actual binary hashes and 5.050 version. No model build or real suite rerun was performed by R245; real execution evidence is the immutable manager/author evidence reviewed above.
