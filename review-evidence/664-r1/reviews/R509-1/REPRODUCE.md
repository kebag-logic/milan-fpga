# R509-1 receipt reproduction

Use a checkout at the exact head named in `REPORT.md`, with its three required
submodules initialized at their gitlinks. `REPO` names that checkout and
`PACKET` names an independent output directory. Keep all disposable files under
`$PACKET/scratch`. Do not run the full implementation banks for this review.

```sh
python3 verify_integrity.py "$REPO" "$PACKET/integrity.json"
python3 audit_documents.py "$REPO" "$PACKET" --standards "$STANDARDS_DIR"
python3 run_focused_checks.py "$REPO" "$PACKET/focused-checks"
```

The document audit reads `pr-674.json` from the packet as the recorded public
approval-text snapshot. Its standards option hashes four locally supplied PDFs;
it does not download or publish them. Omitting the option still reproduces scope,
ownership-search counts and approval-text comparisons.

The first check execution used the existing Python environment. The TOC,
anchor and em-dash checks refused missing Markdown dependencies. For those
three rechecks, create a virtual environment under `$PACKET/scratch`, install
`$REPO/tools/markdown/requirements.txt` with `--require-hashes`, and invoke:

```sh
"$PACKET/scratch/markdown-venv/bin/python" run_focused_checks.py \
  "$REPO" "$PACKET/focused-rechecks" --only toc anchors em-dash
```

`dependency-setup.json` records the versions used. The focused driver waits for
all children in the foreground, writes an individual log and return-code file,
and uses at most four concurrent checks. Its temporary directory is under the
packet's scratch directory. No simulation/compiler campaign is part of these
commands.

`prior-public-findings.json` and `hosted-summary.json` are dated public-state
observations, not claims about later changes. Public scope snapshots are
`issue-664.json`, `issue-664-comments.json` and `pr-674.json`; account metadata
was omitted. `standards-audit.md` contains the independent clause conclusions.

Verify the publishable packet from its root:

```sh
sha256sum -c MANIFEST.sha256
```

Only manifest-listed files and `REPORT.md` are publication inputs. Scratch
contains disposable dependencies, extracted standards and original downloads;
none is a publication input.
