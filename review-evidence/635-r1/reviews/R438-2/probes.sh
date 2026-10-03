#!/usr/bin/env bash
# R438-2 probes for milan-fpga PR #636 at 420b778a52e4f4bcc8040c13bbc4bef9bc94ada0.
# Usage: probes.sh <parent-clone> <packet-dir> <verilator>
# Every processor probe runs in a git-archive copy of protocol-processor
# 631eeb34 under <packet-dir>/scratch; the clone itself is never edited.
set -u
CLONE=${1:?parent clone}; PKT=${2:?packet dir}; V=${3:?verilator}
S=$PKT/scratch; R=$PKT/receipts; PIN=631eeb342ca1e3fa80e734077a56a943aee76ff1
mkdir -p "$S" "$R"
"$V" --version > "$R/tool_identity.txt"

# 1. processor copies: base, roll-back fallback arm, MVU fault-echo arm
for d in pp_base pp_hardreset pp_mvufault; do
  mkdir -p "$S/$d"
  git -C "$CLONE/protocol-processor" archive "$PIN" | tar -x -C "$S/$d"
  # build parallelism cap only (5 jobs per build, three builds at once)
  sed -i 's/--build -j 0/--build -j 5/' "$S/$d/tb/pp_top/Makefile"
done
(cd "$S/pp_hardreset" && git apply tb/adp_engine/mutations/cfg-valid-hard-reset.patch)
(cd "$S/pp_mvufault" && git apply tb/pp_top/mutations/mvu-fault-status-10.patch)

(cd "$S/pp_base/tb/pp_top" && make VERILATOR="$V" adp-config > "$R/pp_base_adp_config.log" 2>&1
 echo $? > "$R/pp_base_adp_config.rc"
 ./obj_dir/Vpp_top_sim --deadline-only > "$R/pp_base_deadline.log" 2>&1
 echo $? > "$R/pp_base_deadline.rc") &
(cd "$S/pp_hardreset/tb/pp_top" && make VERILATOR="$V" adp-config > "$R/arm_cfg_valid_hard_reset.log" 2>&1
 echo $? > "$R/arm_cfg_valid_hard_reset.rc") &
(cd "$S/pp_mvufault/tb/pp_top" && make VERILATOR="$V" deadline > "$R/arm_mvu_fault_status_10.log" 2>&1
 echo $? > "$R/arm_mvu_fault_status_10.rc") &
wait

# 2. style gate: the reviewers' one-sentence deadline text, rejoined, in a copy
mkdir -p "$S/parent_style"
git -C "$CLONE" archive HEAD | tar -x -C "$S/parent_style"
(cd "$S/parent_style" && python3 - <<'EOF'
p = 'CHANGELOG.md'; s = open(p).read()
old = ("- Its answer is ENTITY_MISBEHAVING unless a refusal was already chosen.\n"
       "- A command that had already changed state answers for itself.\n")
new = ("- Its answer is ENTITY_MISBEHAVING unless a refusal was already chosen;"
       " a command that had already changed state answers for itself.\n")
assert s.count(old) == 1
open(p, 'w').write(s.replace(old, new))
EOF
python3 scripts/check_doc_style.py > "$R/probe_style_joined_sentence.log" 2>&1
echo $? > "$R/probe_style_joined_sentence.rc")

# 3. the KL_pp_shadow edit is comment-only
strip() { git -C "$CLONE" show "$1:hdl/milan/KL_pp_shadow.sv" | sed -E 's://.*$::'; }
diff <(strip 3370c6cbd5e4b096167c19ca709556a40207e538) <(strip 420b778a52e4f4bcc8040c13bbc4bef9bc94ada0) \
  > "$R/kl_pp_shadow_comment_stripped.diff"
echo "stripped-diff rc=$?" > "$R/kl_pp_shadow_comment_stripped.rc"
