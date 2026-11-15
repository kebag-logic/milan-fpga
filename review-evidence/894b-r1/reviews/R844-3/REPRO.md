# Reproduction and receipt provenance

The review uses source head af2c4d7a4a1930aba712792a7facd8e9cb88e7c7 and public evidence archive d0318d2add19efec6d659b6c42201d143dea9658. Published archive paths below are under review-evidence/894b-r1. No private input is required.

Use a clean detached clone at the source head, initialized at its required submodule pins. Set `repo` to that clone and `packet` to a separate output directory. Disposable extraction and probe directories must stay under `packet/scratch`.

Fetch the evidence object read-only and extract only author-r5, author-r6 and MANIFEST.json:

```sh
rtk git -C "$repo" fetch origin d0318d2add19efec6d659b6c42201d143dea9658
rtk proxy mkdir -p "$packet/scratch"
rtk proxy bash -c 'git -C "$1" archive d0318d2add19efec6d659b6c42201d143dea9658 review-evidence/894b-r1/author-r5 review-evidence/894b-r1/author-r6 review-evidence/894b-r1/MANIFEST.json | tar -x -C "$2/scratch"' _ "$repo" "$packet"
```

The following foreground commands produced the independent receipts. The check runner uses six concurrent lightweight processes and waits for all of them; no detached jobs or broad banks are launched.

```sh
rtk proxy python3 -B "$packet/run_checks.py" "$repo" "$packet"
rtk proxy python3 -B "$packet/verify_evidence.py" "$packet/scratch/review-evidence/894b-r1"
rtk proxy python3 -B "$packet/probe_ledger.py" "$repo" "$packet" "$packet/scratch/review-evidence/894b-r1"
rtk proxy python3 -B "$packet/scratch/review-evidence/894b-r1/author-r6/scripts/gate_controls.py" "$repo" "$packet/scratch/review-evidence/894b-r1/author-r6/scripts/gate_r5.py" "$packet/scratch/packet-gate"
rtk proxy python3 -B "$packet/scratch/review-evidence/894b-r1/author-r6/scripts/comment_scan.py" "$repo" 7398ec0aeea468d92ff642a03a06e291a0cd58d1 HEAD
rtk proxy python3 -B "$packet/verify_integrity.py" "$repo"
```

The acceptance-control driver starts children with isolated Python and may create an ignored egress_ledger bytecode cache in the clone. This review removed that generated file after execution; no tracked source was edited. Its fixture tree is under scratch.

Receipt inventory:

- Six focused check logs and return-code files, plus focused-checks.json: exact commands and raw outputs.
- ledger-probes.log: independent decimal derivation, equality and one-cycle boundary cases, original large miss, new miss, run refusal, missing summary, and regrade of eight published logs. Seven logs are the 114-group formal measurement; the eighth is the additional platform SRP leg.
- packet-gate-controls.log: all 21 published wrapper controls rerun at the reviewed head.
- evidence-verification.log: 98 public manifest hashes, both packet indices, full image digest pairs, bare-merge BUDGET-line identity, and gate/sweep totals.
- source-comments.log: added-source wording scan over the full source-base range; output is empty apart from its zero-count header.
- public-scope.json: selected public scope rulings and source REVIEW READY, retrieved read-only.
- scope.log: head/tree, merge history, file inventory and whitespace check.
- integrity.log: raw Git blob hashes, Git modes, tree/index equality, hidden/sparse flags and initialized submodule pins/contents after all probes.

Broad execution receipts stay at their public archive URLs. They were inspected and hash-checked, not regenerated or silently represented as independent executions. The archive has no embedded Git signature, so no signer attestation is claimed. No fresh hardware, CPU measurement, full bank, image build or hosted execution occurred.

MANIFEST.sha256 lists every publishable receipt and script with paths relative to this packet. REPORT.md is published separately. scratch is never published.

