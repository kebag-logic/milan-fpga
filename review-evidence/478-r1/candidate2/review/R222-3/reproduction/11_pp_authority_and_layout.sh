#!/usr/bin/env bash
# R222-3: rate-bound authority and wire-layout facts at the candidate.
# Public PP authority lines are printed; Milan/IEEE text is NOT copied - only
# the local file hashes, the section/table identifiers located, and boolean
# layout checks are recorded.
# Usage: 11_pp_authority_and_layout.sh <scratch-cand> <scratch-root> <out>
set -euo pipefail
C=$1; SC=$2; out=$3
STANDARDS_DIR=${STANDARDS_DIR:-$HOME/standards}
PIN=424c688fa2205b934a7689a58f2aa766420f2326
P="$C/protocol-processor"
MIL="$STANDARDS_DIR/Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf"
IEEE="$STANDARDS_DIR/1722.1-2021.pdf"
{
  echo "## protocol-processor pin (candidate gitlink): $(git -C "$C" ls-tree HEAD protocol-processor | awk '{print $3}')"
  echo "checkout HEAD: $(git -C "$P" rev-parse HEAD)"
  for f in docs/architecture/07_memory_maps.md hdl/aecp/ucode/gen_ucode.py hdl/aecp/desc/gen_desc_image.py; do
    echo "$f blob $(git -C "$P" rev-parse "$PIN:$f")"
  done
  echo "-- 07_memory_maps.md section 3.1 heading and L10 row (public PP authority)"
  git -C "$P" show "$PIN:docs/architecture/07_memory_maps.md" | grep -n -E '^#+ 3\.1|^\| L10 \|'
  echo "-- gen_ucode.py SSR constants and walk (public PP authority)"
  git -C "$P" show "$PIN:hdl/aecp/ucode/gen_ucode.py" | grep -n -E '^SSR_LIST_OFF|^SSR_WALK_MAX|range\(0, SSR_WALK_MAX, 2\)'
  echo "## candidate builder facts (blob $(git -C "$C" rev-parse HEAD:sw/builder/endstation_builder.py))"
  git -C "$C" show HEAD:sw/builder/endstation_builder.py | grep -n -E '^BASE_RATE_HZ|^MAX_AUDIO_UNIT_RATES|section 3.1, L10|if len\(rates\) > MAX_AUDIO_UNIT_RATES|if len\(set\(rates\)\) != len\(rates\)|if rate not in rates'
  echo "## candidate AUDIO_UNIT emitter (avdecc/aem_descriptors.py blob $(git -C "$C" rev-parse HEAD:avdecc/aem_descriptors.py); unchanged by #513)"
  git -C "$C" show HEAD:avdecc/aem_descriptors.py | grep -n -E 'def d_audio_unit|144|sampling_rates' | head -20
  echo "## local standards (text not reproduced)"
  sha256sum "$MIL" "$IEEE" | sed "s#$STANDARDS_DIR#\$STANDARDS_DIR#"
  pdftotext -layout "$MIL" "$SC/milan12.txt" 2>/dev/null
  pdftotext -layout "$IEEE" "$SC/17221_2021.txt" 2>/dev/null
  echo "Milan v1.2 heading 5.3.3.3 located at text line: $(grep -n -m1 -E '^5\.3\.3\.3 AUDIO_UNIT' "$SC/milan12.txt" | cut -d: -f1)"
  echo "Milan v1.2 heading 5.3.5.1 located at text line: $(grep -n -m1 -E '^5\.3\.5\.1 Sampling rate' "$SC/milan12.txt" | cut -d: -f1)"
  echo "IEEE 1722.1-2021 7.2.3 AUDIO_UNIT entries located at text lines (TOC, table captions): $(grep -n -E '7\.2\.3\.? +AUDIO_UNIT|Table 7.5.AUDIO_UNIT Descriptor' "$SC/17221_2021.txt" | cut -d: -f1 | tr '\n' ' ')"
  for pair in 136:current_sampling_rate 140:sampling_rates_offset 142:sampling_rates_count 144:sampling_rates; do
    off=${pair%%:*}; field=${pair#*:}
    hit=$(grep -c -E "^ +$off +([24]|4\*S) +$field( |$)" "$SC/17221_2021.txt" || true)
    echo "Table 7-5: a row at offset $off naming $field present: $([ "$hit" -ge 1 ] && echo yes || echo no) ($hit)"
  done
} > "$out" 2>&1
cat "$out"
