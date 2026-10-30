#!/usr/bin/env bash
# Plant stale-table defects in disposable copies of the reviewed tree and run
# the docs gate on each. Usage: plant_probes.sh <clone> <scratch-dir>
# Prints one line per probe: name, expected outcome, gate rc, first finding.
set -u
SRC=$1; WORK=$2
mkdir -p "$WORK"
fresh() { rm -rf "$WORK/t"; mkdir -p "$WORK/t"; git -C "$SRC" archive HEAD | tar -x -C "$WORK/t"; }
run() { # name expect
  local out rc
  out=$(cd "$WORK/t" && python3 scripts/check_docs.py 2>&1); rc=$?
  printf '%-34s expect=%-4s rc=%s | %s\n' "$1" "$2" "$rc" "$(printf '%s' "$out" | grep -v '^docs check: PASS' | head -1)"
  printf '%s\n' "$out" | sed "s/^/    [$1] /" >> "$WORK/probe_full.log"
}
: > "$WORK/probe_full.log"
fresh; run control_unmutated pass
fresh; sed -i 's/| Shipping | 1,022 of 1,024 | 2 |/| Shipping | 1,021 of 1,024 | 3 |/' "$WORK/t/docs/MANAGER.md"; run stale_rom_shipping fail
fresh; sed -i 's/| Seeded regression | 1,023 of 1,024 | 1 |/| Seeded regression | 1,022 of 1,024 | 2 |/' "$WORK/t/docs/MANAGER.md"; run stale_rom_seeded fail
fresh; sed -i 's/| Shipping | 1,022 of 1,024 | 2 |/| Shipping | 1,022 of 1,024 | 3 |/' "$WORK/t/docs/MANAGER.md"; run stale_rom_free_only fail
fresh; sed -i '/^| Seeded regression |/d' "$WORK/t/docs/MANAGER.md"; run deleted_rom_row fail
fresh; sed -i 's/| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | 376 |/' "$WORK/t/docs/INTEGRATION.md"; run drifted_constant fail
fresh; sed -i 's/| `CEASE_MS_C` | 300,000 |/| `CEASE_MS_C` | 30,000 |/' "$WORK/t/docs/INTEGRATION.md"; run drifted_constant_comma fail
fresh; sed -i 's/| `DEPTH` | 1,024 |/| `DEPTH` | 2,048 |/' "$WORK/t/docs/INTEGRATION.md"; run drifted_depth fail
fresh; sed -i 's/| `P1_C` | 248 |/| `P1_X` | 248 |/' "$WORK/t/docs/INTEGRATION.md"; run unknown_constant fail
fresh; sed -i 's/^NPD_HI_C = 800 /NPD_HI_C = 900 /' "$WORK/t/hdl/ucode/gen_gptp_ucode.py"; run generator_constant_changed fail
fresh; sed -i 's/^ROM_CID_HI_C, ROM_CID_LO_C = 1022, 1023/ROM_CID_HI_C, ROM_CID_LO_C = 1022, 1023  # x/' "$WORK/t/hdl/ucode/gen_gptp_ucode.py"; run generator_comment_only pass
fresh; sed -i '\#^| `tb/verilator/gaskets/README.md` |#d' "$WORK/t/docs/README.md"; run deleted_status_row fail
fresh; sed -i 's#^| `docs/GLOSSARY.md` | Every reader | Defined terms and their clauses | Current |#| `docs/GLOSSARY.md` | Every reader | Defined terms and their clauses | Historical |#' "$WORK/t/docs/README.md"; run wrong_status_value fail
fresh; printf '| `docs/GONE.md` | X | Y | Current |\n' > /tmp/.r739row; sed -i '\#^| `docs/history/v1/` |#r /tmp/.r739row' "$WORK/t/docs/README.md"; rm -f /tmp/.r739row; run row_for_missing_page fail
fresh; mkdir -p "$WORK/t/tb/newsuite"; printf '<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->\n# New suite\n\nRuns.\n' > "$WORK/t/tb/newsuite/README.md"; run new_page_without_row fail
fresh; sed -i '\#^| `docs/history/v1/` |#d' "$WORK/t/docs/README.md"; run deleted_history_row fail
# Coverage limits (not claimed by the PR): these are expected to PASS silently
fresh; sed -i '/^| `P1_C` | 248 |/d' "$WORK/t/docs/INTEGRATION.md"; run limit_deleted_constant_row pass?
fresh; sed -i 's/| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | 376 ms |/' "$WORK/t/docs/INTEGRATION.md"; run limit_reformatted_constant_cell pass?
fresh; sed -i 's/| Pdelay_Req interval | 1 s |/| Pdelay_Req interval | 2 s |/' "$WORK/t/docs/INTEGRATION.md"; run limit_cadence_literal pass?
fresh; sed -i 's/^Timer slot 4 is the 375 ms Sync receipt watch./Timer slot 4 is the 376 ms Sync receipt watch./' "$WORK/t/docs/HDL_DEVELOPER.md"; run limit_prose_copy pass?
rm -rf "$WORK/t"
