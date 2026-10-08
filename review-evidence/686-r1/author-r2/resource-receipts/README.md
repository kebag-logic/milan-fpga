# Resource-gate receipts, issue #686 (answers R549-1-F4)

These are the raw recipe receipts behind the three records of
`syn/ooc/pp_resource_baseline.json` that this lane committed (`route-1x1`,
`ooc-1x1`, `ooc-8x8`). Each record can be regenerated from them with the
repository's own `syn/ooc/pp_resource_gate.py` parsers and compared, field by
field, with the committed JSON.

## Which records

`r2-48f12dc1/` holds the receipts of the records the branch now carries. Round 2
Part B merged dev `291710b1` (#682: processor `2ad2f845` and baseline F) into
the lane as `e519e31f`. It ran the recipe on that tree with
`--single-thread-synthesis`, as F's flow identity requires, and wrote the three
records with `record --write` in `48f12dc1`. Each endpoint passed `check`
against F before the write (`gate/check_*.log`). Regenerate them with
`--git 48f12dc14099a3630a98eb07e9ec790695a72bfb`.

`r1-c7b69cd0/` holds the receipts of the round 1 records, committed in
`c7b69cd0` ("Re-record the resource gate's three endpoints ..."). They were
measured on the tree at `7b2896568`, whose RTL equals `c7b69cd0`'s. They answer
R549-1-F4 for the records that review read. Regenerate them with
`--git c7b69cd0fb2bdf980546ab413b3b82198267cbd8`. The round 2 Part A commits
(`b2e786bb1`, `359c42da7`, `30fce4b0a`) changed `KL_maap.sv` and a comment in
`milan_datapath.sv`, which is why Part B measured again.

## Layout of one endpoint directory

| File | What it is |
|---|---|
| `baseline_integrated.tcl` / `baseline_ooc.tcl` | The executed recipe script |
| `baseline_utilization.rpt`, `baseline_hierarchy.rpt` | Vivado reports the gate reads |
| `baseline_timing.summary.rpt` | The report header and the Design Timing Summary of `baseline_timing.rpt`, the only part the gate reads. The full report's sha256 and size are in `files.sha256` |
| `baseline_cells.carry4.tsv[.gz]` | The header and every `CARRY4` row of the primitive census `baseline_cells.tsv`. The gate's census counts `CARRY4` only, so this file gives the identical census. The full census's sha256 and size are in `files.sha256` |
| `*_route_status.rpt` | Route status (route endpoint only) |
| `clock.xdc`, `baseline_parameters.json`, `baseline_chparam.txt`, `baseline_scope_timing.tsv` | Standalone clock and parameter binding (standalone endpoints only) |
| `baseline_images.json` | The memory-image manifest the input digest covers |
| `inputs.manifest.json` | Every component of the input digest in digest order. Each entry gives the file name, its role, the sha256 of the bytes the gate digests, and for a repository file its repo-relative path |
| `inputs/<role>/` | The digested bytes of every input that is not a repository file. Generated files are given after the gate's own normalisation (comments removed, roots replaced by `$ROOT<n>`), which is what the digest covers |
| `record.json` | `pp_resource_gate.py record <dir> --endpoint <name>` output at measurement time |
| `baseline.log.gz` | The Vivado log |
| `files.sha256` | sha256 and size of every original file of the measurement directory, the checkpoints and full reports that are not copied included |
| `regen.log` | The output of the regeneration below |

Host path prefixes in the copied text are replaced by `<repo>`, `<work>`,
`<measurement>`, `<generated>`, `<scratch>` and `<home>`. No value a record holds
depends on them. The identity strips include directories and generics, and the
generic digest keeps only file names.

Each round's `recipe/` directory holds the export receipts: the builder dry runs, the
exact LiteX argv of each shape, the elaboration logs, the 8x8 RTL elaboration
script and log that bind the 8x8 standalone parameters, and the orchestration
scripts that ran the recipe steps. In `r2-48f12dc1/recipe/run/` are the chain's step log, its
exit statuses and durations in seconds, and its memory log (peak 12.37 GB, 11.57 GB
anonymous). Each round's `gate/` directory holds every `pp_resource_gate.py`
output of the round. It has `check` against the previous record (round 1: the
2026-10-05 record D; round 2: F), `record --write`, `check-baseline`, the
re-checks against the new record, and the gate's self-test and mutation
campaign. Round 1's `recipe_*.rc` gives each Vivado step's exit status and
duration in seconds.

## Regenerate a record

From any clone of the repository with the submodules fetched:

```sh
for e in route-1x1 ooc-1x1 ooc-8x8; do
  python3 scripts/regen_record.py <clone> r2-48f12dc1/$e $e --git 48f12dc14099a3630a98eb07e9ec790695a72bfb
  python3 scripts/regen_record.py <clone> r1-c7b69cd0/$e $e --git c7b69cd0fb2bdf980546ab413b3b82198267cbd8
done
```

With `--git`, the parsers, the baseline and every repository input are read from
that commit's objects. A file inside a submodule is read from the submodule's
pinned commit. The script re-hashes every repository input and every copied
input, recomputes the input digest, and rebuilds identity, figures and scopes
from the receipts. It then requires equality with both the committed record
and `record.json`, and for the route a complete route status. It prints
`record EQUAL` and exits 0, or names every difference and exits 1. All six
print `record EQUAL` (see each `regen.log`). Round 1's receipts checked against a
round 2 tree name `hdl/ieee1722/maap/KL_maap.sv` and
`hdl/milan/milan_datapath.sv` as changed inputs, which is the expected
consequence of Part A.

`MANIFEST.sha256` lists every file here with its sha256, paths relative to this
directory (`sha256sum -c MANIFEST.sha256`).

`scripts/collect_receipts.py` is the script that wrote each endpoint directory
from its measurement directory. It refuses unless the manifest reproduces the
record's input digest.
