The report and receipts review exact head `1496558d82cf35fc98dda0e781b2a1be643c301a`, tree `e8d797554a935c5514e25be9e1dda119f4f8c999`. Scripts require existing Git, Python, RTK, authenticated read-only GitHub access for public evidence, and the candidate's already-installed Python dependencies. They install nothing. The candidate checkout is read-only to these scripts; tests and mutations run in temporary exported sources. Keep downloaded evidence and generated outputs outside the candidate checkout.

Run from the packet directory, replacing `/path/to/review-clone` and output paths. Use fresh output directories for the focused runner. Every shell command begins with `rtk`.

```sh
rtk proxy python3 integrity.py /path/to/review-clone /path/to/results/integrity-initial.json
rtk proxy python3 docs_probe.py /path/to/review-clone /path/to/results/docs-final-controls
rtk proxy python3 run_focused.py /path/to/review-clone /path/to/results/focused-receipts
rtk proxy python3 fetch_evidence.py /path/to/results/public-evidence
rtk proxy python3 verify_evidence.py /path/to/review-clone /path/to/results
rtk proxy python3 integrity.py /path/to/review-clone /path/to/results/integrity-final.json
```

`focused_worker.py` is called by `run_focused.py`; keep them together. It runs only gates 36a, 1 and 32, independent loader controls, source mutations, the isolated main-loop check, and image generation/comparison. It does not run the full builder suite, native/processor suites, or act. Sources come from Git archives at explicitly recorded revisions, including pinned PP/gPTP/verilog-axis populations. Seven loader mutations and six actual C++ declaration mutations must fail, with three dispatch sentinels propagated. The worker retains full images and logs under each head prefix. `comparison.json` establishes exact binary equality against two independently generated baselines. `execution.json` retains their individual head identities.

`docs_probe.py` creates uninitialized standalone Git clones, then moves their metadata aside for the no-Git condition. Corrected-head docs and feature status must pass in both conditions. The same current checker with only the old link restored must fail, as must the original-head failure control. Each expected failure is a successful discriminating control, not an unresolved test failure. `docs-receipts/` contains the first successful probe; `docs-final-controls/` adds the current-checker old-link controls. No-Git inventory parity is explicitly skipped by the checker.

`fetch_evidence.py` reads immutable Git tree/blob APIs, using at most four concurrent reads. It selects current manager factual evidence and two original author rate receipts; it does not download other review reports. Git blob hashes and published manifest hashes are verified. `verify_evidence.py` confirms command/result/completion identities, bounded source changes, all four pins, and original author/baseline image hashes. It writes `evidence-verification.json`, `diff-identity.json`, the issue patch, correction patch and history. It does not inspect hosted checks or run candidate tools.

`integrity.py` compares every tracked file's real bytes, type and executable mode with its commit blob, independently of status flags. It requires exact index records, rejects hidden index flags, recursively verifies initialized submodule heads/populations, and disables Git replacement objects. The initial and final JSON populations compare equal. `integrity-comparison.json` records that comparison.

`issue478.json`, `pr512.json` and `public-pr-selected-comments.json` are public-state snapshots. PR metadata was requested with explicit JSON fields excluding `statusCheckRollup`. The original R221 report was read solely to reconstruct F1 and its assignments. Manager evidence stays attributed to its recorded head; no later candidate or CI pass is inferred.

`standards-identities.json` identifies the locally read Milan v1.2 and IEEE 1722.1-2021 PDFs. Read Milan section 5.3.3.3, IEEE section 7.2.3/Table 7-5 and section 7.4.21.1 with `rtk proxy pdftotext -layout <standard.pdf> -`. The report paraphrases the governing facts and does not redistribute standards text. `REPORT.md` names the corresponding pinned implementation artifacts.

All receipts are factual results or reproducible procedures. Path neutralization is a publication step owned by the manager. This packet contains no approval to merge and no claim of physical calibration, hosted CI completion, act completion, or post-merge containment.
