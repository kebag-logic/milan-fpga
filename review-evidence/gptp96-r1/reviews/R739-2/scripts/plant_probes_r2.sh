#!/usr/bin/env bash
# Plant defects in disposable copies of the reviewed tree and run the docs
# gate (check_docs.py, then --selftest) on each.
# Usage: plant_probes_r2.sh <clone> <scratch-dir>
# Prints: probe name, expected outcome, gate rc, first finding.
set -u
SRC=$1; WORK=$2
mkdir -p "$WORK"
fresh() { rm -rf "$WORK/t"; mkdir -p "$WORK/t"; git -C "$SRC" archive HEAD | tar -x -C "$WORK/t"; }
run() { # name expect
  local out rc
  out=$(cd "$WORK/t" && python3 scripts/check_docs.py 2>&1); rc=$?
  printf '%-36s expect=%-6s rc=%s | %s\n' "$1" "$2" "$rc" "$(printf '%s' "$out" | grep -v '^docs check: PASS' | head -1)"
  printf '%s\n' "$out" | sed "s/^/    [$1] /" >> "$WORK/probe_full.log"
}
I=docs/INTEGRATION.md; H=docs/HDL_DEVELOPER.md; T=docs/TEST_DEVELOPER.md; M=docs/MANAGER.md
: > "$WORK/probe_full.log"
fresh; run control_unmutated pass
# Stale constants rows
fresh; sed -i 's/| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | 376 |/' "$WORK/t/$I"; run stale_const_plain fail
fresh; sed -i 's/| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | **376** |/' "$WORK/t/$I"; run stale_const_bold fail
fresh; sed -i 's/| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | -1 |/' "$WORK/t/$I"; run stale_const_negative fail
fresh; sed -i 's/| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | 376 ms |/' "$WORK/t/$I"; run stale_const_unit fail
fresh; sed -i 's/| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | 0x178 |/' "$WORK/t/$I"; run stale_const_hex fail
fresh; sed -i 's/| `CEASE_MS_C` | 300,000 |/| `CEASE_MS_C` | 3,00,000 |/' "$WORK/t/$I"; run bad_grouping_const fail
fresh; sed -i '/^| `P1_C` | 248 |/d' "$WORK/t/$I"; run deleted_const_row fail
fresh; sed -i 's/^| `P1_C` | 248 |/| P1_C | 249 |/' "$WORK/t/$I"; run unnamed_const_row fail
fresh; sed -i 's/^| `DEPTH` | 1,024 |/| `DEPTH` | 2,048 |/' "$WORK/t/$I"; run stale_depth fail
fresh; sed -i 's/^NPD_HI_C = 800 /NPD_HI_C = 900 /' "$WORK/t/hdl/ucode/gen_gptp_ucode.py"; grep -q '^NPD_HI_C = 900' "$WORK/t/hdl/ucode/gen_gptp_ucode.py" && run generator_const_changed fail || echo "generator_const_changed: SED MISSED"
# Broken ROM rows
fresh; sed -i 's/| Shipping | 1,022 of 1,024 | 2 |/| Shipping | 1,021 of 1,024 | 3 |/' "$WORK/t/$M"; run rom_stale_shipping fail
fresh; sed -i 's/| Shipping | 1,022 of 1,024 | 2 |/| Shipping | **1,022** of 1,024 | 2 |/' "$WORK/t/$M"; run rom_bold_count fail
fresh; sed -i 's/| Shipping | 1,022 of 1,024 | 2 |/| Shipping | 1,022 of 1,024 | two |/' "$WORK/t/$M"; run rom_word_free fail
fresh; sed -i 's/| Shipping | 1,022 of 1,024 | 2 |/| Shipping | 1,022 \/ 1,024 | 2 |/' "$WORK/t/$M"; run rom_slash_count fail
fresh; sed -i '/^| Seeded regression |/d' "$WORK/t/$M"; run rom_deleted_row fail
fresh; sed -i 's/^| Shipping | 1,022 of 1,024 | 2 |/&\n| Shipping | 1,022 of 1,024 | 2 |/' "$WORK/t/$M"; run rom_duplicate_row fail
# Restated unit-bearing values on current pages
fresh; printf '\nThe watch is 375 ms.\n' >> "$WORK/t/$H"; run copy_hdl_375ms fail
fresh; printf '\nA 20 us link-up threshold.\n' >> "$WORK/t/$T"; run copy_test_20us fail
fresh; printf '\nInside 200 ppm.\n' >> "$WORK/t/docs/GLOSSARY.md"; run copy_glossary_200ppm fail
fresh; printf '\nThe five-minute cease.\n' >> "$WORK/t/$M"; run copy_manager_fiveminute fail
fresh; printf '\nA 300 s cease.\n' >> "$WORK/t/README.md"; run copy_readme_300s fail
fresh; printf '\nA 100\xc2\xb5s step.\n' >> "$WORK/t/tb/tsngen/README.md"; run copy_tbreadme_100micro fail
fresh; printf '\nA 20,000 ns step.\n' >> "$WORK/t/$I"; run copy_integration_20000ns fail
fresh; sed -i 's/^Timer slot 4 is the .*Sync receipt watch\./Timer slot 4 is the 375 ms Sync receipt watch./' "$WORK/t/$H"; run copy_revert_hdl_line fail
# Coverage limits: expected to pass (outside the declared unit-bearing scope)
fresh; printf '\nA 0.375 s watch.\n' >> "$WORK/t/$H"; run limit_decimal_seconds pass?
fresh; printf '\nA 375 milliseconds watch.\n' >> "$WORK/t/$H"; run limit_spelled_unit pass?
fresh; printf '\nThe fifth consecutive loss clears asCapable.\n' >> "$WORK/t/$H"; run limit_unitless_ordinal pass?
fresh; printf '\nROM contains 1,024 words.\n' >> "$WORK/t/$H"; run limit_unitless_depth pass?
fresh; sed -i 's/syncReceiptTimeout, ms |/syncReceiptTimeout (ms) |/' "$WORK/t/$I"; printf '\nThe watch is 375 ms.\n' >> "$WORK/t/$H"; run limit_meaning_unit_dropped pass?
rm -rf "$WORK/t"
