# Milan feature status ledger

This page explains the machine-checked status rows used by active Milan v1.2
documentation. The canonical data is
[`milan_feature_status.json`](milan_feature_status.json). Prose may explain why
a feature has its status, but it must not redefine the status.

The checker reads every active Markdown file, ignores archive directories and
files whose first line is a valid obsolete banner, and compares marked rows
with the ledger. Run both the fixture controls and the live-tree check with:

```console
python3 scripts/check_feature_status.py --self-test
```

Allowed statuses are `implemented`, `partial`, `missing`, and `not-supported`.
`not-supported` is used only where refusal is the intended compliant behavior,
such as Milan's required `ACQUIRE_ENTITY` result. A `partial` command can be
served on the wire while still having a known behavioral defect.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `gateware.current-version` | `implemented` | `0x0002_0051` |
| `aem.served-command-set` | `implemented` | - |
| `aem.acquire-entity-refusal` | `not-supported` | - |
| `aem.mandatory-missing-set` | `missing` | - |
| `stream-input.start-stop` | `partial` | - |
| `stream-input.stopped-crf-observation` | `missing` | - |
| `crf.media-clock-consumption` | `missing` | - |
| `state.nonvolatile-persistence` | `missing` | - |
| `notifications.change-events` | `partial` | - |
| `notifications.controller-liveness` | `missing` | - |
| `verification.long-gate-policy` | `implemented` | `local-required, remote-optional` |
<!-- milan-feature-status:end -->

The JSON `facts` object owns the exact served AEM list, served MVU list,
mandatory missing AEM list, and current gateware version. A new repeated claim
gets a stable identifier here and in the JSON before another active page uses
it. The JSON also names every active page that must carry each row, so deleting
a marker is a gate failure rather than a silent loss of traceability.

The checker also compares the canonical version with the `VERSION` parameter
in `milan_csr.sv`. Its served AEM list is compared with the behavior model's
`SERVED` table, which the compliant tests independently gate against the
processor RTL.
