# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Out-of-context synthesis of the WHOLE milan_datapath — the assembled,
# substituted design: the shipping 1722.1/SRP planes are deleted and the
# protocol processor stands in their place, instantiated unconditionally.
#
# Same instrument as syn/ooc/pp_shadow_ooc.tcl (post-synthesis utilization,
# ship part, 100 MHz OOC), because a net figure built from two different
# instruments is not a net figure.
#
# The per-block OOC number pp_shadow_ooc.tcl produces is a STANDALONE cost; it
# does not carry the datapath's own interconnect to the plane. This script is
# what closes that gap: it prices the assembled design, so a difference against
# a stored baseline is the number that actually decides the campaign.
#
#   vivado -mode batch -source .../milan_datapath_ooc.tcl -nojournal
#   TAG=<name> ...     ;# names the .rpt files
#
# There is no PP switch any more. milan_datapath instantiates KL_pp_shadow
# unconditionally (PP_PLANE_P is gone with the plane it used to gate), so
# "the datapath" and "the datapath with the processor" are the same design.
#
# The shape include MUST be named (milan_datapath and milan_csr both
# `include gen/adp_shape_defaults.svh); the 1x1 arty config is the default
# elaboration shape the yosys gate also uses.

set REPO [file normalize [file dirname [info script]]/../..]
set TAG  [expr {[info exists ::env(TAG)] ? $::env(TAG) : "base"}]
puts "milan_datapath OOC: tag=$TAG"

# The source list is printed by syn/yosys/run.sh itself (`--emit`) and relayed
# by dp_srcs.py -- the ONE list the portability gate proves elaborates. A copy
# here would drift, and since the processor's files are part of that list now, a
# copy would drift a whole control plane. Nothing is read outside it, and
# nothing re-reads run.sh: dp_srcs.py checks the record run.sh hands it, and
# resolves $TOP in it through `sv2v --top`, so sv2v is required to run this
# script as well as the Yosys gate (README.md's tool table). It runs FIRST
# because it is also the authority everything below derives from: the ROM
# geometry packages are found IN this record, never spelled here by hand
# ([R0] round three on PR #264 -- a spelled path is a hand list in waiting,
# and the pp_srcs.py literal gate cannot see Tcl semantics).
set SRC_LINES [split [string trim [exec python3 $REPO/syn/ooc/dp_srcs.py]] "\n"]

# Exactly one file in the derived record may carry the named basename; zero
# means the record no longer contains the geometry source (refuse, do not
# guess a path), and two means the name stopped being an identity.
proc one_source {src_lines tail} {
  set hits {}
  foreach f $src_lines {
    if {[string match "*/$tail" $f]} { lappend hits $f }
  }
  if {[llength $hits] != 1} {
    error "milan_datapath OOC: expected exactly one $tail in the derived\
 read set, found [llength $hits]. The geometry source comes from the record\
 dp_srcs.py hands this recipe; a record without it is a refusal, not a\
 license to spell a path by hand."
  }
  return [lindex $hits 0]
}

# BOTH control-plane $readmemh images, generated into the run directory
# before anything slow. protocol_processor_top reads its ACMP listener
# transition ROM by the RELATIVE name "ltn_rom.hex" and KL_aecp_ucpu its
# microcode by "ucode.hex" (UCODE_HEX_P); Vivado resolves both against ITS OWN
# run directory. This recipe is documented to run from an EMPTY directory, so
# it must generate what it requires: until #246 it generated only
# ltn_rom.hex, and Vivado read the absent ucode.hex as an all-zero ROM behind
# one CRITICAL WARNING (Synth 8-4445), constant-folded the AECP uCPU, and
# completed rc=0 with a full, plausible utilization report 7,923 LUT under
# the shipping design.
#
# The contract, per image ([R-parallel] and [R0] on PR #264 closed the
# survivors):
#   - the target is DELETED first, generation goes to a fresh temp file, and
#     the image is published by rename only after it validates, so a stale
#     file in the run directory plus a no-op generator can never be measured;
#   - `exec` takes the generator's exit status (a failed generator aborts);
#   - the image must hold EXACTLY its ROM's geometry, derived from the
#     pinned packages named by the record above (never copied here, where it
#     would drift): after comment stripping, depth words of width/4 hex
#     digits, x/z refused. $readmemh part-fills a short image with X and
#     Vivado prices the X-ROM; a one-word "non-empty" image is the same lie
#     as an absent one.

# The ONE live declaration of the named localparam, comments stripped FIRST:
# a `// stale example: UCODE_W_C = 48` above a live `= 52` must never win,
# and the name is boundary-anchored so MY_UCODE_W_C is not UCODE_W_C ([R0]
# round three). Zero live declarations, more than one, and any spelling this
# does not recognize are refusals, never a guess.
proc pkg_num {path name} {
  set fh [open $path r]; set text [read $fh]; close $fh
  regsub -all {/\*.*?\*/} $text "" text
  regsub -all -line {//.*$} $text "" text
  set pat [format {(?n)^\s*(?:localparam|parameter)\y[^=;]*?\y%s\y\s*=\s*(\d+)\s*;} $name]
  set hits [regexp -all -inline -- $pat $text]
  if {[llength $hits] != 2} {
    error "milan_datapath OOC: expected exactly one live declaration of\
 $name in $path, found [expr {[llength $hits] / 2}] (comments stripped; a\
 spelling this parser does not recognize is a refusal, not a guess)"
  }
  return [lindex $hits 1]
}

proc rom_check {path digits words} {
  set fh [open $path r]; set lines [split [read $fh] "\n"]; close $fh
  set n 0
  foreach line $lines {
    regsub {//.*$} $line "" line
    foreach tok [split $line] {
      if {$tok eq ""} continue
      incr n
      if {![regexp {^[0-9a-fA-F]+$} $tok] || [string length $tok] != $digits} {
        return "word $n ($tok) is not exactly $digits hex digits"
      }
    }
  }
  if {$n != $words} { return "$n words, expected exactly $words" }
  return ""
}

# A declared ROM width must be a positive multiple of 4, and a depth must be
# positive. The image contract is EXACT hex digits per word; truncating a
# 50-bit declaration to 50/4 = 12 digits would let a stale 48-bit image
# satisfy it with the new high bits silently zero-filled, which is #246's
# wrong-area class again ([R-parallel] round three probed exactly that:
# declared_width=50 accepted the 2,048x48 image). No pinned ROM is
# non-nibble-aligned; if one ever becomes so, THIS refusal is where ceiling
# division plus a high-bits-zero check must be added - it is not a width to
# guess past.
proc nibble_width {name w} {
  if {![string is integer -strict $w] || $w <= 0 || $w % 4 != 0} {
    error "milan_datapath OOC: $name = $w is not a positive nibble-aligned\
 ROM width. A truncated digit count would accept a stale undersized image;\
 add ceiling division AND a high-bits-zero check here before accepting such\
 a width."
  }
  return $w
}
proc positive_depth {name d} {
  if {![string is integer -strict $d] || $d <= 0} {
    error "milan_datapath OOC: $name = $d is not a positive ROM depth (an\
 expected word count of zero would let an empty image validate)."
  }
  return $d
}

set UCPU_PKG [one_source $SRC_LINES ucpu_pkg.sv]
set ACMP_PKG [one_source $SRC_LINES pp_acmp_pkg.sv]
set UCODE_W [nibble_width UCODE_W_C [pkg_num $UCPU_PKG UCODE_W_C]]
set UPC_W   [pkg_num $UCPU_PKG UPC_W_C]
set TROM_W  [nibble_width TROM_W_C [pkg_num $ACMP_PKG TROM_W_C]]
set TROM_D  [positive_depth TROM_DEPTH_C [pkg_num $ACMP_PKG TROM_DEPTH_C]]

foreach {img gen digits words} [list \
    ltn_rom.hex $REPO/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py \
                [expr {$TROM_W / 4}] $TROM_D \
    ucode.hex   $REPO/protocol-processor/hdl/aecp/ucode/gen_ucode.py \
                [expr {$UCODE_W / 4}] [expr {1 << $UPC_W}]] {
  set tmp $img.gen.[pid]
  file delete -force $img $tmp
  exec python3 $gen -o $tmp
  set diag "the generator exited 0 leaving no file"
  if {[file exists $tmp]} { set diag [rom_check $tmp $digits $words] }
  if {$diag ne ""} {
    file delete -force $tmp
    error "milan_datapath OOC: $img is malformed after generation by $gen:\
$diag (expected ${words}x[expr {$digits * 4}]-bit). Refusing to synthesize:\
an area report built on a ROM \$readmemh part-fills with X is not a\
measurement (#246)."
  }
  file rename -force $tmp $img
}

# The absolute paths reach synth_design as generics, so the figure cannot
# depend on where vivado was launched from and cannot quietly measure an
# all-zero ROM. UG901: a STRING generic's value must reach -generic wrapped
# in literal double quotes, or Vivado takes it for an integer/bit-vector and
# drops it.
set TROM_GENERIC  "PP_TROM_HEX_P=\"[file normalize ltn_rom.hex]\""
set UCODE_GENERIC "PP_UCODE_HEX_P=\"[file normalize ucode.hex]\""

# And the refusal the tool itself already offers: a $readmem image Vivado
# cannot open is CRITICAL WARNING Synth 8-4445 and a completed run with a
# wrong number -- the one failure of this instrument that still returns a
# figure. Promote it to an ERROR so any image this preflight does not cover
# (a future option-ON gptp_ucode.hex, a renamed image) fails the run outright
# instead of shaping the report. What must hold at synth_design is the
# EFFECTIVE severity: a later downgrade of the same id is the same defect as
# never promoting, and the self-test asserts the final state, not this line's
# spelling ([R0] round three).
set_msg_config -id {Synth 8-4445} -new_severity ERROR

set SV {}
set V  {}
foreach f $SRC_LINES {
  if {[string match "*.sv" $f]} { lappend SV $f } else { lappend V $f }
}
puts "milan_datapath OOC: [llength $SV] SystemVerilog + [llength $V] Verilog sources"
read_verilog -sv $SV
read_verilog $V

set INCS [list $REPO/hdl/common $REPO/hdl/common/csr \
               $REPO/hdl/common/eth_event_counter $REPO/hdl/ieee17221/adp \
               $REPO/hdl/ieee8021q/ts $REPO/hdl/ieee8021as/ptp_timestamp \
               $REPO/hdl/ieee1722/avtp \
               $REPO/configs/generated/endstation_arty_current]

synth_design -mode out_of_context -top milan_datapath -part xc7a100tfgg484-2 \
  -include_dirs $INCS -generic $TROM_GENERIC -generic $UCODE_GENERIC

create_clock -period 10.000 -name clk [get_ports -quiet axis_clk]
report_utilization -hierarchical -file util_hier_$TAG.rpt
report_utilization -file util_$TAG.rpt
report_timing_summary -delay_type max -max_paths 3 -file timing_$TAG.rpt
