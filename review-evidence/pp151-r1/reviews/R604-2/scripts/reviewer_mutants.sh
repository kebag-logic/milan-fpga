#!/usr/bin/env bash
# Reviewer-owned mutants, planted with sed in scratch copies of hdl/, graded by the
# head's tb/elab_guards/guards.py with --only the affected guard (Verilator + Yosys).
# usage: reviewer_mutants.sh CLONE SCRATCH BINDIR
# Each row: name # guard # file # sed expression # expectation (KILLED or SURVIVES).
# Exit 0 = every mutant met its expectation.
set -uo pipefail
clone=$1 scratch=$2 bindir=$3
export PATH="$bindir:$PATH"
rows=(
"rm1-shadow-rstmo-lt2#KL_acmp_nvm_shadow.g_rs_tmo_check#hdl/acmp/KL_acmp_nvm_shadow.sv#s/if (RS_TMO_CYC_P < 1)/if (RS_TMO_CYC_P < 2)/#KILLED"
"rm2-respbuf-size-le23#KL_aecp_resp_buf.gen_g_size#hdl/aecp/KL_aecp_resp_buf.sv#s/if (RESP_BYTES_P <= 16)/if (RESP_BYTES_P <= 23)/#KILLED"
"rm3-listener-base-initial#KL_pp_acmp_listener.g_strm_tmo_check#hdl/acmp/KL_pp_acmp_listener.sv#s/^  if (STRM_TIMEOUT_CYC_P == 0) begin : g_strm_tmo_check/  initial begin : g_strm_tmo_check if (STRM_TIMEOUT_CYC_P == 0)/#KILLED"
"rm4-writer-agg-warning-msg-kept#KL_aecp_nvm_writer.g_rs_agg_check#hdl/aecp/KL_aecp_nvm_writer.sv#s/\$fatal(1, \"KL_aecp_nvm_writer: RS_AGG/\$warning(\"KL_aecp_nvm_writer: RS_AGG/#KILLED"
"rm5-encoder-error#KL_srp_encoder.g_depth_check#hdl/srp/KL_srp_encoder.sv#s/\$fatal(1, \"DEPTH_P/\$error(\"DEPTH_P/#KILLED"
"rm6-originator-floor-dropped#KL_pp_originator.g_inflight_check#hdl/packet_engine/KL_pp_originator.sv#s/if (INFLIGHT_P < 32'd1 || /if (1'b0 || /#SURVIVES"
"rm7-names-zero-dropped#KL_aecp_desc_store.gen_g_names#hdl/aecp/KL_aecp_desc_store.sv#s/if ((NAME_ENTRIES_P == 0) || /if ((1'b0) || /#SURVIVES"
)
one() {
  IFS='#' read -r name guard file expr expect <<<"$1"
  local tree=$scratch/$name log=$scratch/$name.log
  rm -rf "$tree"; mkdir -p "$tree"; cp -r "$clone/hdl" "$tree/hdl"
  sed -i -e "$expr" "$tree/$file"
  if cmp -s "$clone/$file" "$tree/$file"; then echo "$name: PLANT FAILED (no change)" > "$scratch/$name.summary"; return; fi
  python3 -B "$clone/tb/elab_guards/guards.py" --root "$tree" --only "$guard" \
    --verilator verilator --frontend verilator --frontend yosys --jobs 2 > "$log" 2>&1
  local rc=$? fails
  fails=$(grep -c '^FAIL:' "$log")
  local got=SURVIVES; [ "$rc" -ne 0 ] && got=KILLED
  local ok=MET; [ "$got" = "$expect" ] || ok=NOT-MET
  { echo "$name: rc=$rc $got (expected $expect) $ok; $(tail -n1 "$log")"
    grep '^FAIL:' "$log" | cut -c1-190 | sed 's/^/    /'
    /usr/bin/diff "$clone/$file" "$tree/$file" | grep '^[<>]' | sed 's/^/    planted: /'
  } > "$scratch/$name.summary"
}
export -f one; export clone scratch
printf '%s\n' "${rows[@]}" | xargs -d '\n' -P 4 -I{} bash -c 'one "$1"' _ {}
for r in "${rows[@]}"; do cat "$scratch/${r%%#*}.summary"; done | tee "$scratch/summary.txt"
! grep -qE 'NOT-MET|PLANT FAILED' "$scratch/summary.txt"
