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

An `implemented` row describes behavior in the pinned source tree; it does not
waive dependency durability. A release candidate that changes a submodule
gitlink must pin a commit reachable from that donor's durable default branch,
then rerun the parent gates at the resulting exact head. A branch-only donor
commit can be fetched today and still disappear tomorrow, so it is never merge
evidence by itself.

## Values repeated in prose

A marked row is safe because the checker reads it. The same value written into
a sentence was not, and that is how the roadmap came to open with a version two
minors behind its own row, and to count six fewer served opcodes than the block
twenty lines below it (#98). Three prose forms are now judged against the
ledger, and none of them needs a marker while it is correct:

| Written as | Judged against | Notes |
|---|---|---|
| `VERSION `0x0002_0055`` — the name and the full two-word spelling on one line | `facts.gateware_version` | Only the CURRENT major is judged. `VERSION 0x0001_000B` and the minor-only idiom (`fixed at VERSION 0x000F`) are how this corpus writes history, and a bump to major 3 retires today's spellings the same way |
| `thirty AEM opcodes`, `one MVU command` | the length of the matching `facts.served_*_operations` list | Word and numeral spellings are both accepted. `N AEM commands` is deliberately not judged: in this corpus it counts commands still to land |
| a `milan-feature-order` block | `facts.firmware_boot_order`, itself read from `milan_init()` | Compared as a SEQUENCE, so reversing the documented steps fails even though the set is unchanged |

A page that deliberately records a superseded value — a dated audit, a release
note — marks that one line:

```markdown
<!-- milan-feature-value:gateware_version:historic -->
3. The repository README described the VERSION `0x0002_0053` control-plane
   surface as it stood at this audit.
```

The marker is not an exemption from being read. A historic marker on a line
carrying the CURRENT value is itself a finding: the value moved on to that
line, and the marker would otherwise hide a live claim behind a record.
`value_documents` in the ledger names the pages that must state the current
version in prose, so dropping the claim is a finding rather than a silence.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `gateware.current-version` | `implemented` | `0x0002_0055` |
| `aem.served-command-set` | `implemented` | - |
| `aem.acquire-entity-refusal` | `not-supported` | - |
| `aem.mandatory-missing-set` | `implemented` | - |
| `stream-input.start-stop` | `implemented` | - |
| `stream-input.stopped-crf-observation` | `implemented` | - |
| `stream-format.set` | `implemented` | - |
| `stream-info.set-acc-lat` | `implemented` | - |
| `crf.media-clock-consumption` | `missing` | - |
| `gptp.fabric-product-owner` | `implemented` | - |
| `state.nonvolatile-persistence` | `missing` | - |
| `notifications.change-events` | `implemented` | - |
| `notifications.controller-liveness` | `implemented` | - |
| `soc.baremetal-profile` | `implemented` | - |
| `host.sound-card-option` | `not-supported` | - |
| `verification.long-gate-policy` | `implemented` | `local-required, remote-required` |
<!-- milan-feature-status:end -->

## Exact command inventories

Served AEM operations:

<!-- milan-feature-fact:served_aem_operations:start -->
- `ACQUIRE_ENTITY`
- `LOCK_ENTITY`
- `ENTITY_AVAILABLE`
- `READ_DESCRIPTOR`
- `SET_CONFIGURATION`
- `GET_CONFIGURATION`
- `SET_STREAM_FORMAT`
- `GET_STREAM_FORMAT`
- `SET_SAMPLING_RATE`
- `GET_SAMPLING_RATE`
- `SET_CLOCK_SOURCE`
- `GET_CLOCK_SOURCE`
- `SET_CONTROL`
- `GET_CONTROL`
- `START_STREAMING`
- `STOP_STREAMING`
- `REGISTER_UNSOLICITED_NOTIFICATION`
- `DEREGISTER_UNSOLICITED_NOTIFICATION`
- `IDENTIFY_NOTIFICATION`
- `SET_STREAM_INFO`
- `GET_STREAM_INFO`
- `SET_NAME`
- `GET_NAME`
- `GET_AVB_INFO`
- `GET_AS_PATH`
- `GET_COUNTERS`
- `GET_AUDIO_MAP`
- `ADD_AUDIO_MAPPINGS`
- `REMOVE_AUDIO_MAPPINGS`
- `GET_DYNAMIC_INFO`
<!-- milan-feature-fact:served_aem_operations:end -->

Served Milan Vendor Unique operations:

<!-- milan-feature-fact:served_mvu_operations:start -->
- `GET_MILAN_INFO`
<!-- milan-feature-fact:served_mvu_operations:end -->

Missing mandatory AEM operations:

<!-- milan-feature-fact:missing_mandatory_aem_operations:start -->
None. Every operation Milan v1.2 mandates for this profile is served since
0x0002_0054 (the stream setters at 0x0053, name access at 0x0054).
<!-- milan-feature-fact:missing_mandatory_aem_operations:end -->

The JSON `facts` object owns the exact served AEM list, served MVU list,
mandatory missing AEM list, and current gateware version. A new repeated claim
gets a stable identifier here and in the JSON before another active page uses
it. The JSON also names every active page that must carry each row, so deleting
a marker is a gate failure rather than a silent loss of traceability.

The checker also compares the canonical version with the `VERSION` parameter
in `milan_csr.sv`. Its served AEM list is compared with the behavior model's
`SERVED` table, which the compliant tests independently gate against the
processor RTL.
