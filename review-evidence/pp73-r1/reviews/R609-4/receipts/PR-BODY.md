[A595]

Generate the AECP command documentation from one table and hold its consumers to an explicit field registry.

Closes #73

The command model is `hdl/aecp/ucode/aecp_commands.json`, JSON schema
`aecp-command-table/1`: 30 AEM commands and MVU GET_MILAN_INFO, with opcodes,
sizes, statuses, hazard classes, lock/notification flags and dispatched programs.
It generates F06.14 and supplies the ROM generator's status codes and MVU opcode.
The engine constants, classifier, scoreboard, notification map, status codes,
ROM paths and realized inventory are gated. Decode and dispatch are held through
`tb/aecp_cmds` observations of the engine, including MVU sub-decode, GDI members
and unsolicited jobs. Production HDL and both ROM images remain unchanged.

The parent export is `protocol-processor/hdl/aecp/ucode/aecp_commands.json`,
with the sibling `aecp_fields.json` named by `fields`. Firmware consumption and
its parent gate remain follow-up work. The existing evidence-reader disposition
for the command campaign remains necessary when the parent adopts this pin.

## Round 2

The earlier round added the observed decode/dispatch gate, response-size and
command-floor checks, generator refusals, incremental ROM prerequisites and
standing controls. The gate package follows the parent's source style rules without
raising any budget.

Historical validation wording, corrected as requested:

- R608-2-R1: All results below were taken locally at those commits, before the head was pushed.
- R609-2-R1: All results below were run locally at those commits.

These two corrections refer to the published round-2 measurements at `99757648`.
The round-3 measurements below were run locally at the stated commits.

## Round 3

New commits follow `99757648`; no rebase or amend.

- The exhaustive registry names every field and its status, consumer, failure check
  and scope. Missing table fields, stale registry entries and incomplete held
  claims fail by name. A standing sweep changes every held field and requires its
  named failure after regenerating F06.14. The docstring, 09 §8.10, REQ-VER-002 Arch
  and the field reference below are generated or checked against this registry.
- Echo mapping `per` is held exactly by the gcd of accepted offsets. Count one
  is tried at cdl 24 and 28; count two at 28 and 36. Both four-byte and sixteen-byte
  engine drifts fail naming ADD_AUDIO_MAPPINGS and REMOVE_AUDIO_MAPPINGS, including
  after re-recording. Both are standing compiled controls. Zero, null and negative
  record steps are refused.
- `common_status`, `commands[].engine_status` and `commands[].oversize` are
  explicitly held to nothing. The status checks trust those exemptions; oversize
  is rendering input. Six `documented` rows supply semantic opcode, optional rtl
  and optional gdi fields for otherwise-unimplemented GDI members. Identity and
  diagnostic labels are distinct from section/cells rendering data.
- All eight generator probes print named refusals, normally and with optimization.
  A missing name is identified by message type, opcode and constant name. The
  sweep's digests now also include the descriptor validator, its rules and the
  shared simulation harness.

## Round 4

Head: `4029dc5de2a0a540d6a015c747319fbee7abba2e`, following `15981b51`.

`echo_entries` membership is now held by construction: each member is shared by
commands without a first-entry owner, or explicitly listed in `shared_entries`.
`BADARG` and `NSUPPE` are explicitly shared because they also serve as first entries.
The exemption applies only to non-SUCCESS answers in both ROM and observation
checks. SUCCESS must satisfy the table's response rule.

The self-test includes the exact `echo-hide` file edit and separate SUCCESS-size
controls with EAVL explicitly listed as shared, including numeric and symbolic
observations. The registry now has 30 held fields and 32 held-to-nothing fields;
its references have been regenerated. Validation catches all 231 plants, both
normally and with optimization.
All five processor commands pass at original base and head, with every original
suite record unchanged. The suite totals are 1,029,620 and 1,029,796 checks, with
zero failures. All nine existing campaign pairs pass with identical
records under the stated completion-order and scratch-path normalization. The
16 command controls and golden/restored records also match using original-base
production sources and head. Both ROMs and the elaborated engine are byte-identical.
Scratch-parent and source style budget checks pass with unchanged budgets.

The publication-wording residue remains assigned to the merge manager under parent #495; no existing public text is edited.

## Round 3 validation

Final head: `15981b511370a8cfb58ec023fae27f8a800c058c`; original base: `2cbed0a9`.

- All five required processor commands return 0 at base and head. The suite totals
  are 1,029,620 and 1,029,796 checks, with zero failures. Every original suite record
  is byte-identical; the added observer contributes 176 checks.
- All nine existing campaign pairs return 0. Records agree after accounting for
  completion order and scratch paths. The final 16 command controls also pass
  against original base production sources with the final observer and gates;
  all 18 records, including golden/restored runs, match head exactly.
- All 220 named plants are caught. The eight generator probes refuse by name,
  both normally and with optimization. The required mapping and documented-GDI
  probes fail semantically; the four permitted status/oversize probes are covered
  by explicit held-to-nothing declarations.
- Both ROM images, converted production sources and the elaborated engine are
  byte-identical. The final observer produces the same decode record from base
  and head production sources. All 46 original production HDL files are unchanged.
- The original parent at `e8454e27` passes its BDD, feature, source-list and ROM
  gates. The consumer at `ac2c5e77`, with the applicable evidence patches, passes
  the source style gate, listing and 54-check self-test with every budget unchanged.

No hardware was used. The source checks do not replace the manager's
merge-candidate or hosted acceptance.

## Field reference

<!-- BEGIN AECP FIELD REGISTRY -->
Generated from hdl/aecp/ucode/aecp_fields.json; edit the registry.
[] means table rows; * means named map members. Held means only the stated scope.
Rendering inputs generate F06.14; rendering equality is not behavioral proof.

- about: held to nothing. Explanatory prose; no consumer validates its assertions.
- commands: held to nothing. Container: shape is schema-checked; value claims belong to the individual
  fields below.
- commands[].clause: held to nothing. Specification citation prose; no semantic citation check.
- commands[].command: held to nothing. Command-size container; each leaf is classified below.
- commands[].command.cdl: held. Observed first-entry floor, unless floor is declared: ACQUIRE_ENTITY and
  REGISTER_UNSOLICITED_NOTIFICATION cdl are tied only by echo equality; IDENTIFY_NOTIFICATION also has an
  unsolicited body. Consumer: record._floor; table._sizes. Check: command floor or echo equality.
- commands[].command.floor: held. Explicit shorter accepted floor for echo commands. Consumer:
  record._floor. Check: declared floor.
- commands[].command.max: held to nothing. GET_DYNAMIC_INFO ceiling 524; the observed sweep stops at cdl 100
  and does not hold this ceiling.
- commands[].command.per: held. Exact gcd of accepted offsets for both mapping echo commands. Consumer:
  record._floor. Check: accepted-offset gcd.
- commands[].command.plus: held to nothing. Variable-part label used in rendering; presence selects a
  variable size rule, but its wording is not validated.
- commands[].command.unit: held to nothing. Rendering label for N records; existence is schema-checked,
  wording is not behavior.
- commands[].doc: held to nothing. F06.14 rendering data; no semantic validation of the prose.
- commands[].doc.class: held to nothing. F06.14 rendering prose; changes regenerate text without validating
  the assertion.
- commands[].doc.mandate: held to nothing. F06.14 rendering prose; changes regenerate text without
  validating the assertion.
- commands[].doc.scope: held to nothing. F06.14 rendering prose; changes regenerate text without validating
  the assertion.
- commands[].doc.size: held to nothing. F06.14 rendering prose; changes regenerate text without validating
  the assertion.
- commands[].engine_status: held to nothing. Held to nothing: engine-built status exemptions are trusted;
  their exact set and reachability are not independently held.
- commands[].entries: held. Every dispatched program and first-entry decode floor in the observed
  population. Consumer: record._dispatch; record._floor. Check: dispatch entries.
- commands[].gdi: held. Observed GET_DYNAMIC_INFO membership. Consumer: record._gdi_members. Check: GDI
  membership.
- commands[].hazard: held. Top-level classifier hazard name. Consumer: rtl.check_classifier. Check: command
  hazard.
- commands[].lock: held. ROM CHECK_LOCK reachability and scoreboard class membership. Consumer:
  rom._lock_and_notify; rtl.check_scoreboard. Check: lock protection.
- commands[].message: held. AEM/MVU dispatch identity, within the observed sweep. Consumer: record._served;
  table._identity. Check: message dispatch.
- commands[].name: held to nothing. Identity and diagnostic label; uniqueness is checked, but spelling is
  not an engine invariant (except the required MVU identity).
- commands[].notify: held. Presence of the notification contract. Consumer: rom._lock_and_notify;
  record._unsolicited. Check: notification presence.
- commands[].notify.body: held. Observed unsolicited dispatch and ROM body length. Consumer:
  record._unsolicited; rom._lock_and_notify. Check: unsolicited body.
- commands[].notify.class: held. Enqueued notification class; null means an engine event. Consumer:
  rom._lock_and_notify; rtl.check_notify. Check: notification class.
- commands[].notify.doc: held to nothing. F06.14 notification prose; no semantic validation.
- commands[].notify.kind: held. Notification kind mapping and observed unsolicited job. Consumer:
  rtl.check_notify; record._unsolicited. Check: notification kind.
- commands[].opcode: held. Engine constant and observed command_type, within the sweep. Consumer:
  rtl.check_engine; record._served. Check: opcode.
- commands[].oversize: held to nothing. Held to nothing: F06.14 rendering input; no gate derives the
  oversize flag from response size or the Milan list.
- commands[].response: held to nothing. Response-size container; each leaf is classified below.
- commands[].response.cdl: held. ROM fixed part, failure/unsolicited bodies and observed answers; echo
  responses equal command cdl (see command.cdl limits). Consumer: rom._entries; record._answers;
  table._sizes. Check: response size.
- commands[].response.echo: held. Observed command-length responses and ROM echo rule. Consumer:
  record._answers; rom._entries. Check: echo response.
- commands[].response.engine: held. Engine-built aggregate versus dispatched program. Consumer:
  record._dispatch. Check: engine-built answer.
- commands[].response.max: held to nothing. GET_DYNAMIC_INFO ceiling 524; the observed sweep stops at cdl
  100 and does not hold this ceiling.
- commands[].response.per: held. ROM variable step; echo step equals the command step, whose accepted-offset
  gcd is exact. Consumer: rom._entries; table._sizes; record._floor. Check: response record step.
- commands[].response.plus: held to nothing. Variable-part label used in rendering; presence selects a
  variable size rule, but its wording is not validated.
- commands[].response.stub: held. Fixed failure response length. Consumer: rom._entries; record._answers.
  Check: failure stub.
- commands[].response.unit: held to nothing. Rendering label for N records; existence is schema-checked,
  wording is not behavior.
- commands[].rtl: held. Declared engine constant identity. Consumer: rtl.check_engine. Check: opcode
  constant.
- commands[].status: held. ROM path statuses and observed answers, conditional on the trusted common_status
  and engine_status exemptions. Consumer: rom._statuses; record._answers. Check: command status set.
- common_status: held to nothing. Status exemptions trusted by the ROM and decode checks; reachability from
  a shared path only is not checked.
- common_status.AEM: held to nothing. Held to nothing: these shared-status exemptions are trusted, not
  proven reachable for every command; they can hide command-owned statuses.
- common_status.MVU: held to nothing. Held to nothing: these shared-status exemptions are trusted, not
  proven reachable for every command; they can hide command-owned statuses.
- documented: held to nothing. Includes six semantic unimplemented GDI members; individual fields below
  distinguish semantics from identity and rendering.
- documented[].cells: held to nothing. F06.14 rendering cells; cell count is checked, their prose is not
  machine semantics.
- documented[].gdi: held. Optional semantic membership flag for the six unimplemented GDI members. Consumer:
  record._gdi_members. Check: unimplemented GDI membership.
- documented[].name: held to nothing. Identity and diagnostic label, also rendered; required by schema,
  spelling has no behavioral consumer.
- documented[].opcode: held. Semantic input for the six unimplemented GDI members; other documented rows use
  opcode as rendering text only. Consumer: rtl._gdi_consts; record._gdi_members. Check: unimplemented GDI
  opcode.
- documented[].rtl: held. Optional semantic constant name for the six unimplemented GDI members. Consumer:
  rtl._gdi_consts. Check: unimplemented GDI constant.
- documented[].section: held to nothing. F06.14 rendering group and sort order; schema checks the allowed
  groups, not semantic placement.
- echo_entries: held. Each member is shared by commands without a first-entry owner, or listed in
  shared_entries. The exemption applies only to non-SUCCESS answers; SUCCESS must fit the response rule.
  Consumer: table._echo_entries; rom._entries; record._answers. Check: shared echo membership and
  non-SUCCESS scope.
- fields: held. Sibling registry filename. Consumer: fields.check_fields. Check: export registry.
- hazard_classes: held to nothing. Container: shape is schema-checked; value claims belong to the individual
  fields below.
- hazard_classes.*: held. Hazard code by name. Consumer: rtl.check_classifier. Check: hazard class code.
- schema: held. Export schema tag. Consumer: table.check_schema. Check: schema tag.
- shared_entries: held to nothing. Shared-entry inventory keys are checked for missing claims only; added
  claims are not independently held.
- shared_entries.*: held to nothing. Diagnostic explanations of shared program names; wording is not checked
  and adding a key only widens the inventory.
- status_codes: held to nothing. Container: shape is schema-checked; value claims belong to the individual
  fields below.
- status_codes.*: held to nothing. Container: shape is schema-checked; value claims belong to the individual
  fields below.
- status_codes.*.code: held. IEEE 1722.1-2021 Table 7-141 code; also consumed by the ROM generator.
  Consumer: table._status_rows; rtl.check_status_codes. Check: IEEE status code.
- status_codes.*.rtl: held. Optional status constant, where non-null; null for STREAM_IS_RUNNING has no RTL
  constant. Consumer: rtl.check_status_codes. Check: status constant.
- unserved: held. Default program for every unserved opcode in the observed population. Consumer:
  record._unserved. Check: unserved program.
<!-- END AECP FIELD REGISTRY -->

