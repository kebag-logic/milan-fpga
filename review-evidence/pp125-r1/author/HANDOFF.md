# Contract documentation handoff

Status: review ready. Documentation complete, all gates passed, one local commit recorded, and the final notice posted.

## Checkout and scope

- Repository: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git
- Branch: `125-ownership-contract`.
- Verified starting commit: `493e5e4bf58a6146bf9310194d71c72e18610704`; initial working tree clean.
- Assignment: issue #125 comments [5853861179](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/125#issuecomment-5853861179) and [5853864238](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/125#issuecomment-5853864238), covering #125 and #122 together.
- Documentation only, two files. F07.2 and the L1–L10 rows are unchanged. No parent edits, code changes, hardware work, push or PR creation.

## Change list

| File:line | Change |
| --- | --- |
| `docs/architecture/07_memory_maps.md:78` | Cite the mandatory cluster minimum, distinguish map and cluster counts, and link the #122 STOP disposition and parent decision. |
| `docs/architecture/07_memory_maps.md:86` | State parent shipping semantics versus processor generic packed-image ownership; link the reviewed parent matrix; identify actual packer checks at 493e5e4b. |
| `docs/architecture/07_memory_maps.md:99` | Separate ownership from implementation and retain open #38, #39, #60, #89 and parent follow-ups. |
| `docs/architecture/07_memory_maps.md:130` | State exact AUDIO_UNIT extent, distinguish shipping counts, loader bound and conversion-supported rates, and record missing L6/L10 semantic checks. |
| `docs/guides/integrator.md:241` | Require ENTITY/ADP identity agreement, exclude zero/all-ones, and cite model-evolution exclusions. |
| `docs/guides/integrator.md:245` | Require maximum stream counts across configurations, matching ENTITY values and the primary IDENTIFY index; link the ownership contract. |

## Enforcement verification at 493e5e4b

`P` below is `hdl/aecp/desc/gen_desc_image.py` at the verified starting commit.
Its working copy was compared with that commit before the synthetic probes.
Parent paths below refer only to the designated read-only parent tree.

| Contract statement | Verification at 493e5e4b | Disposition |
| --- | --- | --- |
| Processor owns image extents and directory structure. | `P:352` (`_render_image`) constructs aligned offsets, lengths, directory entries and checksum; `P:434` controls the build. | Ownership and construction, not a claim that every possible image defect has a validator. |
| Packer rejects configuration index gaps. | `P:449` compares configuration keys with `range(n_config)` and raises `ImageError`. | Enforced. |
| Packer rejects per-type descriptor index gaps. | `P:338` (`_index_entries`), especially `P:344`, compares each configuration/type index set with its zero-based dense range. | Enforced; does not establish semantic parent/child ordering. |
| Packer rejects duplicate keys. | `P:229` checks occupied configuration/type/index entries and raises `ImageError`. | Enforced. |
| Packer rejects invalid name bindings. | `P:223` bounds name indices; `P:239` checks named/unnamed consistency, ENTITY index/name requirements, contiguous names, table bounds and inline bytes. | Enforced. |
| Packer rejects descriptors beyond the configured line-buffer bound. | `P:323` compares each run's descriptor length with `line_bytes`; the CLI supplies its bound at `P:465`. | Enforced; this is not an L10 semantic extent check. |
| Packer rejects body type/index disagreement for both input forms. | `P:178` assembles `fields` or literal `bytes`; `P:216` decodes and compares the first two 16-bit words against the directory key. Existing `tb/desc_store/test_gen_desc_image.py` passed: 6 tests, 24 key/form cases, public build and CLI. | Enforced, updating the older parent handoff's gap. |
| Packer does not enforce L10 sampling-rate offset. | The complete `P:178` / `P:203` / `P:338` / `P:434` build path does not decode this field. A structural control at offset 144 and an offset-143 variant both packed with body bytes preserved. | Not enforced; #89 and parent F6 remain open. |
| Packer does not enforce L10 count <=8. | The same build path does not decode sampling_rates_count. Eight-entry and nine-entry synthetic bodies both packed unchanged. | Not enforced; parent loader's bound is separate. |
| Packer does not enforce exact AUDIO_UNIT length = 144 + 4 × count. | `P:192` enforces a generic four-byte minimum; `P:325` enforces the line bound. Count/extent mismatch, one byte short and one extra byte all packed unchanged. | Contractual semantic requirement; not implemented in the packer. Stride padding is excluded. |
| Packer does not enforce the L6 identity clock-source list. | No CLOCK_DOMAIN list parsing exists in the build path. Both `[0,1]` and `[1,0]` packed with body bytes preserved. | Not enforced; #89 and parent F6 remain open. |
| The L1–L10 table does not establish a complete implemented model lint. | Reviewed `scripts/`, `.github/workflows/hdl.yml`, the packer and its existing tests. `scripts/check-matrix.py:23` checks documentation rows; `scripts/lint-diagrams.sh` parses diagrams; neither evaluates descriptor semantics. | Replaced the blanket enforcement claim with obligations and named open owners. |
| Parent loader allows at most eight distinct rates. | Read-only parent `sw/builder/endstation_builder.py:1193` sets MAX_AUDIO_UNIT_RATES=8; `:3829` onward refuses excess and duplicate entries. `P` does not supply these semantic checks. | Parent enforcement, distinct from processor packing. |
| Parent image conversion supports only 48000, 96000 and 192000 Hz. | Read-only parent `avdecc/aem_specs.py:219` rejects rates outside this set; the parent ownership matrix L10 records shipped counts of one or three and one configuration per image. | Separate conversion restriction; no assertion that every eight-entry loader input converts. |
| ADP transport does not prove the integrator's identity/count/IDENTIFY obligations. | `hdl/adp/KL_adp_engine.sv:859`, `:861`, `:863`, `:871` serialize the supplied inputs; top-level connections at `hdl/top/protocol_processor_top.sv:1651` onward pass them through. `P` does not consume those live inputs. | Integrator obligations remain explicit; #38/#39 and parent follow-ups retain validation work. |

`ENFORCEMENT-PROBES.txt` records the eight synthetic L6/L10 observations.
These isolate packing behavior, not complete model conformance or supported media operation.
No test or validator source was added or changed.

## Issue #122 clause disposition

| Clause | One-sentence paraphrase | Disposition |
| --- | --- | --- |
| Milan v1.2 §5.3.3.7, printed p. 27 / PDF p. 34 | Input Stream Ports use the IEEE descriptor format and have no attached AUDIO_MAP descriptors. | Dynamic mapping does not waive the cluster minimum. |
| Milan v1.2 §5.3.3.8, printed p. 27 / PDF p. 34 | Each input and output Stream Port must contain at least one AUDIO_CLUSTER, with one channel per cluster. | STOP applied: F07.2 retains `1..*`; the parent D8 zero-cluster input pools conflict with the requirement and require a parent decision. |
| IEEE 1722.1-2021 §7.2.13, pp. 81–82, Table 7-23 | number_of_clusters counts the port's cluster descriptors, while dynamic mapping sets the separate number_of_maps field to zero. | The generic field definition supplies no waiver from Milan's minimum. |

Public report: [issue #122 comment 5853884588](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/122#issuecomment-5853884588).
This resolves the processor contract interpretation; it does not repair or approve the parent model.

## Sources and boundaries

- Read processor `README.md`, `docs/README.md`, `hdl/README.md`, the contribution/gate conventions in `docs/guides/hdl-engineer.md`, and `.github/workflows/hdl.yml` / `Makefile`.
- Read parent `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`: ownership boundary, L1–L10 matrix, D8 discrepancy and follow-up allocation. Its measurements use the older processor pin; current processor claims were rechecked at 493e5e4b.
- Located parent D8 in `docs/ENDSTATION_BUILDER.md:647`; its zero physical-channel allocation is explained at `:689` onward.
- Fetched `509-review-evidence` into `/tmp/pp125-evidence.pi8pip`; fetched head `6ddca01017446a7a3a2cdc6e19c454ff568b7972`. Read `review-evidence/509-r1/author/HANDOFF.md`, section “Processor contract wording”.
- Extracted only cited pages with bounded page arguments into `/tmp/pp125-clauses`: Milan PDF pages 32 (§5.3.3.1, identity/counts), 34 (§5.3.3.7–.8, cluster disposition), 35 (§5.3.3.10, primary IDENTIFY); IEEE pages 50 (§6.2.2.8, model identity exclusions), 81–82 (§7.2.13, Table 7-23).
- No standards extracts, dependencies or tree exports are in the output directory. The PR body contains only two short standard citations.
- Scope is #125 acceptance items 1–4 and the #122 clause disposition. Existing semantic implementation issues remain open.

## Gates

All commands ran in the foreground without output pipelines. The documentation subcommands below ran directly through `make check`; its successful exit establishes each prerequisite's zero status. Output is in `DOCS-GATES.log`.

| Gate | rc | Evidence |
| --- | --- | --- |
| `make check` | 0 | All documentation prerequisites completed. |
| `./scripts/lint-diagrams.sh` | 0 | 41 Mermaid and 18 WaveDrom blocks. |
| `python3 scripts/check-links.py` | 0 | 917 links checked. |
| `python3 scripts/check-matrix.py` | 0 | 115 requirement rows, 17 gap findings. |
| `python3 scripts/check-integrator-params.py` | 0 | 24 top, guide and diagram parameters agree. |
| `python3 scripts/render-wavedrom.py --check` | 0 | 18 blocks fresh. |
| `make stale` | 0 | Diagram exports current; no output on success. |
| `python3 scripts/gen_matrix.py --check` | 0 | 92 rows, zero untested modules. |
| `git diff --check` | 0 | No whitespace errors. |
| `make -C tb/desc_store generator-check` | 0 | 6 existing tests / 24 key/form cases. |
| Synthetic L6/L10 packing verification | 0 | Eight observations, each preserving the assembled descriptor bytes. |

## Delivery

- Head: `1d249e6e18a91c16a2620904483634548b0414a6`.
- Commit: `docs: state descriptor ownership and preserve Milan cluster minimum`.
- Exactly one commit after the verified base; one-line subject with no body or trailers.
- Final working tree: clean. Committed diff whitespace check: rc 0.
- PR draft: `PR-BODY.md`.
- Review-ready notice: [posted on #125](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/125#issuecomment-5853927698); exact text in `REVIEW-READY.md`.
- No push or PR creation performed.
