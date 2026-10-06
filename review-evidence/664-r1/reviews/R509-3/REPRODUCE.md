This packet reviews the ingress requirement delta only. Run from the packet directory with the assigned detached source checkout as CHECKOUT. DOC_PYTHON must provide the repository's hash-locked Markdown dependencies and YAML support. The checks make no source edits; any temporary files go under scratch.

```sh
rtk proxy python3 audit_integrity.py "$CHECKOUT"
rtk proxy python3 audit_scope.py "$CHECKOUT" "$PWD"
rtk proxy python3 run_focused.py "$CHECKOUT" "$PWD" "$DOC_PYTHON"
rtk proxy python3 reconcile_prior.py "$CHECKOUT"
rtk proxy python3 audit_integrity.py "$CHECKOUT"
rtk proxy sha256sum -c MANIFEST.sha256
```

The foreground driver joins up to four concurrent, independent checks. Each check has its own raw log and exit receipt. audit_scope.py reconstructs a merge tree as a Git object; it makes no merge commit or checkout change. Source comparison receipts include the relevant ingress diff and commit history. The saved PR body is the public snapshot used for approval parity.

Primary PDFs were read locally. standards-identity.json identifies those files; clause-checks.md records the results without republishing licensed pages. The full extracts, page render and earlier public evidence downloads stay under scratch and are not published.

The independent verdict was recorded in independent-verdict.md before prior findings were read. REPORT.md is the final report. The manifest is the publication allowlist; scratch is excluded. Rerunning checks overwrites receipts and requires a fresh manifest before republication.
