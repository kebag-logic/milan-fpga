[A331] REVIEW READY
Commit: `ad4a5ff6ba15502ed60d58b3ca91830b50fa9e1c` on `532-pasta-invoked-name`, one local, unpushed commit from `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.

Changed: `scripts/act_ci.py:701` preserves the absolute `pasta` spelling returned by SAFE_PATH lookup. Other tool resolution and identity checks stay unchanged. Seven new offline arms at `scripts/act_ci.py:11428` execute a fake multi-call uplink through a real symlink and check lookup provenance, other-tool resolution, and missing/dangling/non-executable refusals. `docs/testing/CI_WORKFLOWS.md:1855` documents the rule.

Validation: all following commands returned 0 at this head, in the foreground without pipelines:

```sh
python3 -I scripts/act_ci.py --selftest
bash scripts/act_slot_proof.sh --selftest
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/act_ci.py --selftest
python3 -B scripts/docs_check.py
python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_py_idiom.py
python3 scripts/check_sh_idiom.py
git diff --check
git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD
```

The runner's embedded unit and slot checks pass 432 arms in both invocations; the second command form is exactly docs.yml's local runner contract gate. Slot proof: 44 offline cases. CI contract: 1655 items and 2197 self-test arms. The docs command also returned 0 in a metadata-free temporary export of this exact head, matching the other CI mode; both inventories report 166 Markdown files and 884 scrubbed text files, with zero findings.

Mutation evidence: resolving the pasta path again makes the full offline self-test exit 1 on exactly the two new name checks. Focused controls also kill resolution at the uplink launch and preserving every tool's symlink name (3/3 mutants killed, unchanged control passes). Before the fix, the new arms failed on exactly the same two checks.

Acceptance: assignment items 1-2 met. Item 3 remains the manager's live proof after merge, from the trusted merged runner. Relates to #532; the issue stays open. No live replay, privileged execution, Docker, or network namespaces were used. No push, PR operation, or merge performed.

Handoff: `HANDOFF.md` and `PR-BODY.md`, with logs and reproducible mutation scripts, are in the assigned output directory. Reviewers [R266] and [R267] can review this head. Open risks/questions: live proof remains outstanding; no new design decision is needed.
