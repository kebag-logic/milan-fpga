R225-2 reproducible factual receipts

The review source is the detached clone `$VALIDATION_STORAGE/reviews/r225-507-r2`.
All executed probes used isolated scratch named in `scratch-path.txt`. No probe
modified its source checkout. Concurrency was at most four worker jobs, below
the requested eight-job cap. No product/branch commit was made. Real-Git tests
create synthetic base/head commits only in disposable fixture repositories.

Copy this receipt directory before rerunning instruments; outputs are overwritten.
The scripts require Python, Git, rtk, and authenticated gh already installed.
No installer, Docker, act, RTL, builder, Yosys, or hardware command is invoked.

```sh
rtk proxy python3 probes/setup.py
rtk proxy python3 probes/run_review.py
rtk proxy python3 probes/consumer_batch.py
rtk proxy python3 -B probes/boundaries.py
rtk proxy python3 probes/renderer.py
rtk proxy python3 probes/renderer_consumer.py
```

`setup.py` creates fresh scratch at the two pinned revisions. `run_review.py`
compares fixture identities, sources, and predicate bytecode; audits production
source equality; and runs both selftests at old/head under the correct engine
and three closer-only mutations. The mutations construct the same five-name
closer tuple as R15/R16/X04 using tuple unpacking instead of tuple addition.
They leave the shared RAW_HTML_TAGS and both opener regexes unchanged.
Exact unified patches are in `mutations/`; `mutations.json` records commands,
working directories, and return codes. No verdict rests on a source guard.

`consumer_batch.py` uses eight independent real-Git pages per engine, the shipped
TOC generator, and both direct judge_page calls and the actual em-dash CLI.
Its per-variant outputs are cached once complete; remove `consumer/` from the
copied receipt directory before replaying it. Direct judge_page probes isolate
the defect; CLI runs preserve the mandatory selftest and prove refusal before
page judgment. `consumer.json` summarizes all 64 per-page observations.

`renderer.py` sends only 26 synthetic fixtures to GitHub's Markdown renderer:
24 new raw cases and two valid cross-name controls. `renderer_consumer.py`
renders the eight exact independent consumer base pages. Each saves requests,
HTML responses, timestamps and SHA-256 values. These POSTs render text and do
not create public repository objects. The h2 counts are the observed oracle;
no byte-for-byte HTML stability claim is made.

`boundaries.json` contains all 328 independent fixtures, expected classifications,
and actual classifications. Recovery, EOF, ASCII capitals, malformed names,
fence delimiters/lengths/trailers, and block precedence are covered.

`gates.json` supplies exact focused commands, cwd, rc and complete logs under
`gates/`. Execute these in the fresh `head` scratch checkout created by setup.
The two standalone selftest logs are `mutations/head-correct.*.log`.

`retention.json`, `populations/`, and `guard-floor-closures.json` record the
683 retained TOC cases and the 24 additions, plus the 17 retained I440 label
rows and six additions. check_em_dash.py is byte-identical, preserving its
other 34 arms. Four tally guard closures derive totals 5464/5656 from the old
and new floors; their fixture identities and predicate bytecode are unchanged.
`unchanged-production.json`, `correction.diff`, `candidate.diff`, `history.txt`,
and `changed-paths.txt` bind the scope and retention decisions to Git objects.

`public/` contains GitHub API snapshots, both original published review reports,
issue decisions, and the referenced historical public reports. No private
conversation or author scratchpad was read. `public-evidence/` contains selected
factual author/manager records retrieved from their published archive commits.
The download manifest verifies each Git blob and gives its local SHA-256.
The archives were read as evidence and were never merged or checked out.

`initial-integrity.json` and `final-integrity.json` verify every tracked file's
actual blob and mode against the index and prove index-tree equality with HEAD.
`integrity-comparison.json` checks equality across the review. Reproduce with:

```sh
rtk proxy python3 probes/integrity.py $VALIDATION_STORAGE/reviews/r225-507-r2 integrity-recheck.json
```

`remote-final.json` is the final read-only PR head/live-dev/comment snapshot.
No hosted check/run/status endpoint was queried. No actual-runner-start notice
was present in the public comments at the recorded final observation.

Authoritative web clauses were read live: CommonMark 0.31.2 sections
[4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks) and
[4.6](https://spec.commonmark.org/0.31.2/#html-blocks). The linked repository
contracts were read at the exact reviewed head. `MANIFEST.sha256` covers all
receipts and REPORT.md, excluding the manifest itself.
