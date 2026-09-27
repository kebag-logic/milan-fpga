# Round 2 handoff

Status: all five assigned documentation changes are committed at `e04234e115cfdcaace393ae62ba68562d47834c6`; every gate passed; review-ready notice posted.

Repository: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan
Branch: `125-ownership-contract`
Starting head: `1d249e6e18a91c16a2620904483634548b0414a6`
Origin URL and starting head verified; working tree initially clean.

## Assignment and evidence read

- [Round 2 decision and five assignment items](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/125#issuecomment-5854030459).
- [First review](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/126#issuecomment-5854021294) and its [full report](https://github.com/kebag-logic/milan-fpga/blob/ddb65582d8d90d846bf60cc5ed0b0571f952e045/review-evidence/pp125-r1/reviews/R342-1/REPORT.md).
- [Second review](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/126#issuecomment-5854028198) and its [full report](https://github.com/kebag-logic/milan-fpga/blob/ddb65582d8d90d846bf60cc5ed0b0571f952e045/review-evidence/pp125-r1/reviews/R343-1/REPORT.md).
- Both full public reports match the report text in their respective review comments. The complete memory-map document and integrator guide, documentation conventions, workflow, Makefile, and current PR body were read.
- The designated parent ownership page was read only, at `e0920d77`, lines 23–38 and 58–68. The public reference is [PP_DESCRIPTOR_OWNERSHIP.md](https://github.com/kebag-logic/milan-fpga/blob/e0920d77/docs/reference/PP_DESCRIPTOR_OWNERSHIP.md#L23).
- Milan v1.2 §5.3.3.1, printed p. 25 (PDF p. 32), was checked by extracting only page 32 with `pdftotext -f 32 -l 32 -layout` into scratch storage under `/tmp`. It requires a valid EUI-64 excluding zero and all-ones. No standards extract is in this output directory.

## Change list

1. `docs/architecture/07_memory_maps.md:100`: parent shipping checks are authoritative for all generated model content, explicitly covering every L1–L10 semantic obligation, F07.2 minima and ADP maxima. All processor semantic checks, including future #60 coverage, are defence in depth; generic packer acceptance remains authoritative. `:115` applies that split explicitly to the #60 follow-up. Resolves the shared minor authority finding.
2. `docs/architecture/07_memory_maps.md:140`: identifies the generic packed-image checks in the §3.1 introduction, removing the ambiguous reference after the L1–L10 table.
3. `docs/architecture/07_memory_maps.md:80`: states that dynamic mapping sets `number_of_maps` to zero without relaxing the cluster count. `:84` links the D8 correction owner, [milan-fpga#584](https://github.com/kebag-logic/milan-fpga/issues/584), verified open. F07.2's `1..*` minima remain intact.
4. `docs/guides/integrator.md:257`: names `cfg_src_en_i`, `cfg_src_iface_i` and `cfg_stream_id_i` as the three packed per-source vectors.
5. `docs/guides/integrator.md:242` and `docs/architecture/07_memory_maps.md:132`: cite Milan v1.2 §5.3.3.1 for the invalid model-ID values. The existing model-evolution clause and IEEE exclusions remain.

## L1–L10 authority comparison, side by side

The processor references below use `docs/architecture/07_memory_maps.md`. Every semantic row is governed by its authority statement at `:100–107`. The parent references use `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md@e0920d77`; its `:36–38` statement governs every matrix row. Authority is an allocation, not a claim of complete implemented refusal coverage.

| Rule | Processor contract: authoritative layer for model content | Parent page: same authority and measured coverage |
| --- | --- | --- |
| L1 (`:124`) | Parent shipping checks: partition, single parent and cardinalities, including F07.2 minima (`:101–102`). | Parent shipping checks (`:36`, row `:58`): assembly and cluster layout construct the partition; no general partition refusal. The D8 zero-cluster discrepancy remains parent-owned. |
| L2 (`:125`) | Parent shipping checks: multi-level ordering (`:102`). Generic packer acceptance separately owns dense indices (`:107`), with no processor semantic authority. | Parent shipping checks (`:36`, row `:59`): constructs multi-level ordering. Generic packer acceptance (`:38`) owns duplicate-key and index-gap refusals. |
| L3 (`:126`) | Parent shipping checks: role presence, Base formats, rate completeness and configuration uniformity (`:102`). | Parent shipping checks (`:36`, row `:60`): stream declarations refuse an empty direction and construct/test the shipped Base-rate formats; multi-configuration coverage remains untested. |
| L4 (`:127`) | Parent shipping checks: buffer floor, CLASS_A, format-family separation, current membership and format-count cap (`:102`). | Parent shipping checks (`:36`, row `:61`): descriptor construction and shipped-format tests; general refusal coverage remains incomplete under the allocated follow-ups. |
| L5 (`:128`) | Parent shipping checks: stable physical-port descriptor index across configurations (`:102`). | Parent shipping checks (`:36`, row `:62`): one interface/configuration constructed; no cross-configuration mapping refusal claimed. |
| L6 (`:129`) | Parent shipping checks: clock-source construction, domain list shape and restricted gPTP chain (`:102–103`). Processor semantic coverage is defence in depth. | Parent shipping checks (`:36`, row `:63`): source/domain construction and loader refusals cover shipping cases; arbitrary packed lists are not graded. The single-interface gPTP media-clock arm is unreachable in the current loader. |
| L7 (`:130`) | Parent shipping checks: dynamic input maps, output mapping uniqueness and mono clusters (`:103`). | Parent shipping checks (`:36`, row `:64`): refuses static listener maps and duplicate output targets; constructs mono clusters. Stream-channel-width refusal remains a follow-up. |
| L8 (`:131`) | Parent shipping checks: primary IDENTIFY presence at one stable index (`:103`). | Parent shipping checks (`:36`, row `:65`): constructs IDENTIFY[0] and its ADP input; no general missing/wrong CONTROL refusal. |
| L9 (`:132`) | Parent shipping checks: valid model identity and evolution (`:103`); validity now cites §5.3.3.1. | Parent shipping checks (`:36`, row `:66`): model hashing and identity joins/tests; zero/all-ones and some evolution gaps remain allocated follow-ups. |
| L10 (`:133`) | Parent shipping checks: AUDIO_UNIT rate-list offset, count, full words and exact extent (`:103–104`, `:135`). Processor semantic checks are defence in depth. | Parent shipping checks (`:36`, row `:67`): loader refuses excess/distinct ninth entries and duplicates; construction supplies offset/extent; exact-length/general packed-list checks remain open. |

ADP maxima are parent-authoritative at processor `:104–105` and parent `:29`, `:36`, row `:68`. The parent currently generates one configuration. Across all rows, retained and future processor semantic checks are defence in depth (processor `:105–106`; parent `:37`), and generic packer checks are authoritative only for packed-image acceptance (processor `:106–107`; parent `:38`).

The parent snapshot's L2 body/key enforcement gap predates processor `493e5e4b`; the current processor contract and the unchanged probe retain its now-implemented refusal. This implementation difference does not change the authority split.

## Probe provenance

The unchanged [public probe](https://github.com/kebag-logic/milan-fpga/blob/ddb65582d8d90d846bf60cc5ed0b0571f952e045/review-evidence/pp125-r1/reviews/R342-1/scripts/probe_packer_claims.py) was downloaded from `pp125-review-evidence` to `/tmp/pp125-round2.8s6RyCMr/probe_packer_claims.py` and compared byte for byte with the public contents at branch commit `ddb65582d8d90d846bf60cc5ed0b0571f952e045`.

- Git blob: `059aebc38cb55d99cf1d650f2b95ff10ac525e47`.
- SHA-256: `f5ca7619559c84096a12707f7cc83378c6efe77774b06899ca2bf68c8ce595d5`.
- Execution used `python3 -B` against this checkout: **18/18 OK**, rc 0. The probe SHA-256 is unchanged after execution. See `PACKER-CLAIMS.tsv` and `gate-packer-probe.log`.

## Gate results

All commands ran in the foreground, without output pipelines, with 900-second individual timeouts. The workflow documentation commands came from `.github/workflows/hdl.yml:14`; `make check` additionally satisfies `docs/README.md` and the Makefile. The Python environment and WaveDrom dependency (2.0.3.post3) are under `/tmp/pp125-round2.8s6RyCMr/venv`; nothing was installed in the checkout or output directory. `GATES.tsv` records the return codes.

| Gate | Return code | Evidence |
| --- | --- | --- |
| `python3 scripts/check-links.py` | 0 | `gate-check-links.log`: 917 links, OK |
| `python3 scripts/check-matrix.py` | 0 | `gate-check-matrix.log`: 115 REQ rows, 17 GAP findings, OK |
| `python3 scripts/check-integrator-params.py` | 0 | `gate-check-integrator-params.log`: top/guide/diagram 24/24/24, OK |
| `python3 scripts/render-wavedrom.py --check` | 0 | `gate-render-wavedrom.log`: 18 blocks, OK |
| `make stale` | 0 | `gate-stale.log`: no stale exports |
| `make check` | 0 | `gate-make-check.log`: 41 Mermaid + 18 WaveDrom blocks; generated matrix 92 rows, 0 untested; links, matrix, parameters and freshness all pass |
| Unchanged public `probe_packer_claims.py`, run with `python3 -B` | 0 | `gate-packer-probe.log`, `PACKER-CLAIMS.tsv`: 18/18 OK |
| `git diff --check` | 0 | `gate-diff-check.log`: clean |
| `git diff --check 1d249e6e HEAD` | 0 | `gate-committed-diff-check.log`: committed range clean |

## Delivery

Commit: `e04234e115cfdcaace393ae62ba68562d47834c6` — `docs: align descriptor rule authority with parent contract`.
Exactly one new commit on the requested starting head, touching only the two documentation files. The subject is one line, with no body or trailers. `COMMIT.txt` records the final integrity checks: the `hdl`, `tb`, `scripts`, `syn`, `.github` and `Makefile` objects match the starting head, and the working tree/index are clean.
Replacement PR body: complete in `PR-BODY.md`; prepared for the maintainer, not applied to the PR.
Review-ready issue comment: [posted on issue #125](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/125#issuecomment-5854096496) with the final head and `[A350] REVIEW READY` marker. Its exact body is `REVIEW-READY.md`; its URL is recorded in `ISSUE-COMMENT.txt`.
No push, PR mutation, merge, other checkout, hardware operation or code change has been made.
