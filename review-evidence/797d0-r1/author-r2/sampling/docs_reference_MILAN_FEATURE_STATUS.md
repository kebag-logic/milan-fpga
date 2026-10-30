# Sampling ledger: docs/reference/MILAN_FEATURE_STATUS.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 3 | sentence | This page explains the machine-checked status rows used by active Milan v1.2 documentation. | - | ok: scripts/check_feature_status.py checks the marked rows |
| 3 | sentence | Prose may explain why a feature has its status, but it must not redefine the status. | - | ok: scripts/check_feature_status.py checks the marked rows |
| 8 | sentence | The checker reads every active Markdown file, ignores archive directories and files whose first line is a valid obsolete banner, and compares marked rows wit... | - | ok: same script's population rule |
| 12 | code | ```console python3 scripts/check_feature_status.py --self-test ``` | command 1 | ok: gate a027 rc 0 at round 1; --self-test defined (auto) |
| 16 | sentence | Allowed statuses are `implemented`, `partial`, `missing`, and `not-supported`. | - | ok: scripts/check_feature_status.py:25 ALLOWED_STATUSES |
| 16 | sentence | `not-supported` is used only where refusal is the intended compliant behavior, such as Milan's required `ACQUIRE_ENTITY` result. | - | ok: scripts/check_feature_status.py:25 ALLOWED_STATUSES |
| 21 | sentence | An `implemented` row describes behavior in the pinned source tree; it does not waive dependency durability. | - | policy: CONTRIBUTING submodule durability rule |
| 21 | sentence | A release candidate that changes a submodule gitlink must pin a commit reachable from that donor's durable default branch, then rerun the parent gates at the... | - | policy: CONTRIBUTING submodule durability rule |
| 21 | sentence | A branch-only donor commit can be fetched today and still disappear tomorrow, so it is never merge evidence by itself. | - | policy: CONTRIBUTING submodule durability rule |
| 30 | sentence | The same value written into a sentence was not, and that is how the roadmap came to open with a version two minors behind its own row, and to count six fewer... | - | ok: the three prose forms are rows 38-40; #98 CLOSED is the history cited |
| 30 | sentence | Three prose forms are now judged against the ledger, and none of them needs a marker while it is correct: | - | ok: the three prose forms are rows 38-40; #98 CLOSED is the history cited |
| 38 | row | \| `VERSION `0x0002_0060`` - the name and the full two-word spelling on one line \| `facts.gateware_version` \| Only the CURRENT major is judged. `VERSION 0x... | version 1 | ok: scripts/check_feature_status.py:175 facts.gateware_version |
| 39 | row | \| `thirty AEM opcodes`, `one MVU command` \| the length of the matching `facts.served_*_operations` list \| Word and numeral spellings are both accepted. `N... | - | ok: scripts/check_feature_status.py:110 COUNT_FACTS |
| 40 | row | \| a `milan-feature-order` block \| `facts.firmware_boot_order`, itself read from `milan_init()` \| Compared as a SEQUENCE, so reversing the documented steps... | - | ok: scripts/check_feature_status.py:120, 192 firmware_boot_order compared as a sequence |
| 45 | code | ```markdown <!-- milan-feature-value:gateware_version:historic --> 3. The repository README described the VERSION `0x0002_0053` control-plane surface as it s... | version 1 | ok: example block marked historic |
| 51 | sentence | The marker is not an exemption from being read. | - | ok: value_documents in the ledger JSON |
| 51 | sentence | `value_documents` in the ledger names the pages that must state the current version in prose, so dropping the claim is a finding rather than a silence. | - | ok: value_documents in the ledger JSON |
| 121 | sentence | The other Milan v1.2 Table 5.18 commands are absent from that list on purpose. | issue 1 | ok: #510 owner decision cited; P4 (#416) |
| 121 | sentence | `SET/GET_SYSTEM_UNIQUE_ID` and `SET/GET_MEDIA_CLOCK_REFERENCE_INFO` are RECOMMENDED (Milan v1.2 Sections 5.4.4.2 to 5.4.4.5), and the [owner decision on #510... | issue 1 | ok: #510 owner decision cited; P4 (#416) |
| 121 | sentence | Implementation moves to P4 (#416) if the conformance lab requires it, and the served list grows only when it lands. | issue 1 | ok: #510 owner decision cited; P4 (#416) |
| 129 | sentence | Missing mandatory AEM operations: | - | ok: the missing-mandatory list is the ledger's |
| 136 | sentence | The JSON `facts` object owns the exact served AEM list, served MVU list, mandatory missing AEM list, and current gateware version. | - | ok: facts object keys (check_feature_status.py:175-198) |
| 136 | sentence | The JSON also names every active page that must carry each row, so deleting a marker is a gate failure rather than a silent loss of traceability. | - | ok: facts object keys (check_feature_status.py:175-198) |
