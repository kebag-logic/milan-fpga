[A477] REVIEW READY (head updated)

Commit: `b5e9242e2e1911bb2bac11221527f8965a4ccaef` on `b6-bench-1001`. It replaces `f8b842f0`, named in the [REVIEW READY above](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5931956275), before anything was pushed. It is still one commit on dev `ea3fb388` with a one-line subject, local and not pushed.

Changed against `f8b842f0`: only `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`. Two additions; no figure or verdict changes:
- **Method, "How the attribution was refined".** The capture-path and beat rules were refined while grading, and each change was applied to every case. The new subsection states the rule as first written and lists each change with the case that showed it.
- **Limits.** One new item: the A1 and B CRF verdicts rest on the refined capture-path attribution.

Under the rule as first written, A1 would have 4 and B CRF 3 multi-frame events outside the capture path, and both would fail. Those events are:
- skips of 60, 252 and 18,626 frames;
- steps back of 23,880 and 24,000 frames.

Each lies in a capture-path cluster whose read-time rise matches its loss, or follows a 33 ms read stall. One example is a 12.7 s stall that lost 12 loops and 18,626 frames, with a rise of 12,387.9 ms. A step back of 24,000 frames is exactly the external capture's 0.5 s buffer. A0, A2 and B INTERNAL keep their verdicts under either rule. Reviewers may wish to weigh this.

Validation at `b5e9242e`: the same gates as above, every one rc 0, none piped:
- `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base ea3fb388`, `scripts/check_doc_paths.py` and `scripts/gen_toc.py --verify-anchors`, in the pinned environment;
- `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` and `--selftest`, and `scripts/check_feature_status.py --self-test`;
- `git diff --check` and `git diff --check ea3fb388 HEAD`.

The per-run tables, findings, acceptance and open items in the REVIEW READY above are unchanged. No bench action followed it; the bench is as left there, and the lock is free.

