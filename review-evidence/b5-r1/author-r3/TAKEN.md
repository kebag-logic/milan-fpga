[A474] TAKEN

Round 3 for PR #628 (bench lane B5, #117 acceptance box 4, the audio continuity row), under the [A10] assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5927406852). Docs only; no bench access.

Branch: `b5-bench-1001` at `e29d12b1d5ee858eaf4684aaa8dc6647f6309857`, local only.

Authoritative references: R424-2 (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5927400045) and R425-2 (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5927386225); the F1 note (https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5927406516); IEEE 1722.1 7.2.16 as `docs/ENDSTATION_BUILDER.md` and `avdecc/aem_descriptors.py` encode it.

Interpreted scope: (F1) where the page tells a reader how to reproduce the figures, add the `gunzip` step for the published `a-long-reads.u16.gz`. (1) The Direction B reason and the line 24 Evidence cell state that the descriptors naming each cluster's signal source were not read, because the survey walk is defective, so it was not established whether a known signal can reach the peer's talker without a wiring change; NOT RUN stays. (2) State what the walk actually sent: no map read. (3) The summary's "stall-aligned" and the 109,069-frame comparison name exactly the skips they cover, 236 of 239, and name the other three. (4) State, as an observation without attribution, that the 1 ms steps concentrate at the 121 off-stall clusters (22 of 121, against about 0.26 by chance). (5) Take R425-2 S3 and R424-2 S4 where cheap, otherwise record each as retained with the reason. Tables byte-identical except cells an item requires, proven by a diff.

Validation plan: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9`, `check_doc_paths.py` in the pinned Markdown environment; `scripts/ci_scope.py --selftest`; `scripts/check_baremetal_only.py --check`; `scripts/check_feature_status.py --self-test`; `git diff --check`; a table diff against `e29d12b1`; a public-text scan of the diff and the output.

Blockers: none.
