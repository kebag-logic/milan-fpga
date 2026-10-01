[A473] TAKEN

Round 2 for PR #628 (bench lane B5, #117 acceptance box 4, the audio continuity row), under the [A10] assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5926598386). Docs and evidence only; no bench access.

Branch: `b5-bench-1001` at `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2`, local only.

Authoritative references: #117 acceptance boxes 4 and 5; R424-1 F1 and F2 (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5926590622); R425-1 F1, F2 and F3 (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5926558221); `avdecc/aem_descriptors.py` for the AEM descriptor numbering.

Interpreted scope: (1) state each cause of the continuity loss only as strongly as the packet carries it: the skips of 60 frames or more as stall-aligned capture-path loss, the 2-to-59-frame class as consistent with capture-path loss but not separated from a packet-sized drop downstream of the peer's receive counters unless published evidence separates it, and the 1.266 s one-frame drops as attributed to the peer's output rate by inference; the index row follows the same wording. (2) Publish the analysis behind each attribution figure as a tool with derived receipts of the read-time record (stall definition stated), reconcile or correct 115,614 against `summary.json`'s `window_time`, and drop or qualify any figure that cannot be reproduced. (3) State the Direction B reason as observed only, and record the survey tool's descriptor type-code defect against the repository's AEM numbering. (4) Establish from the packet's records which controller tool revision ran the binds and format sets, or state that it cannot be established. The measurement tables stay byte-identical except where a figure is corrected under item 2. Raw artifacts stay local; only derived receipts are published.

Validation plan: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9`, `check_doc_paths.py` in the pinned Markdown environment; `scripts/ci_scope.py --selftest`; `scripts/check_baremetal_only.py --check`; `scripts/check_feature_status.py --self-test`; `git diff --check`; a diff proving the measurement tables unchanged; a public-text scan of the diff and the output.

Blockers: none.
