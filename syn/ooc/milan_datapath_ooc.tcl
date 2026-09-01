# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Out-of-context synthesis of the WHOLE milan_datapath — the assembled,
# substituted design: the shipping 1722.1/SRP planes are deleted and the
# protocol processor stands in their place, instantiated unconditionally.
#
# Meant to be the same instrument as syn/ooc/pp_shadow_ooc.tcl
# (post-synthesis utilization, ship part, 100 MHz OOC), because a net figure
# built from two different instruments is not a net figure. It is NOT that
# today: pp_shadow_ooc.tcl neither generates nor geometry-checks its images,
# does not promote Synth 8-4445, and passes no -include_dirs or
# -verilog_define. Any net figure spanning the two is owed that convergence
# first.
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
# Named ONCE: it reaches dp_srcs.py, the record assertion and synth_design
# from this one variable (pp_shadow_ooc.tcl's discipline).
set TOP  milan_datapath
# TAG names the .rpt files. NOT via `expr`, which coerces its operand
# numerically: TAG=007 wrote util_7.rpt and collided with a TAG=7 run, so a
# campaign comparing two tags compared one file against itself.
set TAG "base"
if {[info exists ::env(TAG)] && $::env(TAG) ne ""} { set TAG $::env(TAG) }
puts "milan_datapath OOC: tag=$TAG"

# Invalidated HERE, before the first refusal can fire -- not beside
# synth_design, where every guard below would still have left the previous
# run's numbers standing under the same names. The reports are the only
# artifact a human reads directly, so they must be the first thing this run
# takes responsibility for.
foreach r [list util_hier_$TAG.rpt util_$TAG.rpt timing_$TAG.rpt] {
  file delete -force $r
}

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
#
# --record hands over the PREPROCESSOR half too (top=/define=/incdir=), not
# just src=. Deriving the sources and then spelling the include path by hand
# left the two halves free to disagree, and they did: run.sh puts the
# elaboration-shape config dir FIRST for milan_datapath, this recipe had it
# LAST, and BOTH hdl/common/csr/gen/ and configs/generated/*/gen/ carry an
# adp_shape_defaults.svh -- so synth_design priced milan_datapath as the
# ax7101_1x1_tdm8 entity (2 talker sources, 31 name entries, 8 wire channels)
# while the portability gate elaborates it as arty_current (1 / 29 / 2). That
# is #246's own class one layer up: a complete, plausible report for a design
# nobody asked for.
#
# What this does NOT fix, and must not be read as fixing: milan_csr.sv sits
# beside its OWN hdl/common/csr/gen/ copy, and a quoted `include resolves
# against the including file's directory before any -I. So under the
# authority order milan_csr still sees the tracked copy (2 / 31) while
# milan_datapath sees the config (1 / 29) -- the two-includer invariant
# asserted at milan_datapath.sv:1526 does not hold on this tree, for the
# gate either. Matching the gate is this recipe's job; making the tracked
# copy agree with the config is endstation_builder.py --write-rtl's, and is
# not attempted here. The
# define half is live too -- KL_gptp_engine.sv gates simulation-only $error
# blocks on `ifndef SYNTHESIS`, which the gate defines and this recipe did
# not.
#
# `exec` treats ANY child stderr byte as an error even on a zero exit, so one
# DeprecationWarning out of python3 would abort the run with that warning as
# its entire diagnostic. The exit STATUS is the contract. stdout here IS the
# payload, so stderr cannot be merged into it -- it goes to a file instead,
# because -ignorestderr alone would replace dp_srcs.py's own "missing
# sources:" report with Tcl's bare "child process exited abnormally".
set DP_SRCS $REPO/syn/ooc/dp_srcs.py
set REC_ERR dp_srcs.err.[pid]
file delete -force $REC_ERR
set REC_RC [catch {exec python3 $DP_SRCS --top $TOP --record 2>$REC_ERR} REC]
set REC_WHY ""
if {[file exists $REC_ERR]} {
  set fh [open $REC_ERR r]; set REC_WHY [string trim [read $fh]]; close $fh
  file delete -force $REC_ERR
}
if {$REC_RC} {
  error "milan_datapath OOC: the derived record is not available -- \
dp_srcs.py failed. Everything below derives from it, so this is a refusal,\
 not a license to fall back to a hand list:\n$REC\n$REC_WHY"
}

set DP_TOP    {}
set DEFINES   {}
set INCS      {}
set SRC_LINES {}
foreach line [split [string trim $REC] "\n"] {
  if {[regexp {^top=(.*)$} $line -> v]}    { lappend DP_TOP    $v; continue }
  if {[regexp {^define=(.*)$} $line -> v]} { lappend DEFINES   $v; continue }
  if {[regexp {^incdir=(.*)$} $line -> v]} { lappend INCS      $v; continue }
  if {[regexp {^src=(.*)$} $line -> v]}    { lappend SRC_LINES $v; continue }
  error "milan_datapath OOC: unrecognized record line \"$line\". A key this\
 recipe does not know is a refusal: silently skipping it is how a consumer\
 stops consuming half of the record it asked for."
}
# The top is named ONCE here and asserted against the record, the discipline
# pp_shadow_ooc.tcl states explicitly. Counting tops is cardinality; #235 is
# about IDENTITY -- a record that names one top which is not this one would
# have satisfied a count and quietly priced another module.
if {[llength $DP_TOP] != 1 || [lindex $DP_TOP 0] ne $TOP} {
  error "milan_datapath OOC: the record names \"$DP_TOP\", expected exactly\
 one top and that top to be $TOP. The module this script reads and the\
 module it synthesizes must not be two different strings (#235)."
}
# DEFINES is guarded too: it is the half that silently reverts this recipe to
# its pre-fix state if the authority ever stops emitting it, and an empty
# ELEMENT satisfies a length check while passing "" to the tool.
foreach {nm lst} [list "include dir" $INCS "source" $SRC_LINES \
                       "define" $DEFINES] {
  if {[llength $lst] == 0} {
    error "milan_datapath OOC: the record carries no ${nm}s. Every half of\
 the record is consumed here, so an absent half is a refusal, not a default."
  }
  foreach e $lst {
    if {[string trim $e] eq ""} {
      error "milan_datapath OOC: the record carries an empty $nm entry.\
 A blank element satisfies a length check and then reaches the tool as \"\"."
    }
  }
}

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

# ALL THREE control-plane $readmemh images, generated into the run directory
# before anything slow. protocol_processor_top reads its ACMP listener
# transition ROM by the RELATIVE name "ltn_rom.hex", KL_aecp_ucpu its
# microcode by "ucode.hex" (UCODE_HEX_P), and the default-on fabric gPTP
# engine's KL_gptp_ucpu its microcode by "gptp_ucode.hex"
# (GPTP_UCODE_HEX_P); Vivado resolves each against ITS OWN run directory.
# This recipe is documented to run from an EMPTY directory, so
# it must generate what it requires: until #246 it generated only
# ltn_rom.hex, and Vivado read the absent ucode.hex as an all-zero ROM behind
# one CRITICAL WARNING (Synth 8-4445), constant-folded the AECP uCPU, and
# completed rc=0 with a full, plausible utilization report 8,012 LUT under
# the shipping design. (That delta is PR #264's, measured at its own head;
# the 7,923 this comment used to carry is #246's calibration of the same
# pair at the older head 6be50377 -- a different measurement, not an
# estimate. Both predate the shape correction below, so both are owed a
# re-measurement.)
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
  # SystemVerilog reads an unbased literal as DECIMAL; Tcl's expr reads a
  # leading zero as OCTAL, so `UPC_W_C = 011` would be 9 here and 11 in the
  # RTL. scan %d fixes the base at ten.
  return [scan [lindex $hits 1] %d]
}

proc rom_check {path digits words} {
  set fh [open $path r]; set text [read $fh]; close $fh
  # $readmemh accepts BOTH comment forms and pkg_num strips both; stripping
  # only // here made a generator banner written as /* */ a false refusal.
  regsub -all {/\*.*?\*/} $text "" text
  set lines [split $text "\n"]
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

# UPC_W_C is not a depth, it is the EXPONENT of one: the ucode ROM is
# 1<<UPC_W_C words. It reached `expr` with no guard, so UPC_W_C = 0 asked for
# a ONE-WORD image -- "the same lie as an absent one" by the contract above,
# admitted through the single constant that skipped a check.
proc positive_exp {name e} {
  if {![string is integer -strict $e] || $e <= 0} {
    error "milan_datapath OOC: $name = $e is not a positive ROM address\
 width (the image is 1<<$e words). A zero exponent would accept a one-word\
 image, which is the absent-image lie under another name."
  }
  return $e
}

set UCPU_PKG [one_source $SRC_LINES ucpu_pkg.sv]
set ACMP_PKG [one_source $SRC_LINES pp_acmp_pkg.sv]
set GPTP_PKG [one_source $SRC_LINES gptp_ucpu_pkg.sv]
set UCODE_W [nibble_width UCODE_W_C [pkg_num $UCPU_PKG UCODE_W_C]]
set UPC_W   [positive_exp UPC_W_C [pkg_num $UCPU_PKG UPC_W_C]]
set TROM_W  [nibble_width TROM_W_C [pkg_num $ACMP_PKG TROM_W_C]]
set TROM_D  [positive_depth TROM_DEPTH_C [pkg_num $ACMP_PKG TROM_DEPTH_C]]
set GUCODE_W [nibble_width UCODE_W_C [pkg_num $GPTP_PKG UCODE_W_C]]
set GUPC_W   [positive_exp UPC_W_C [pkg_num $GPTP_PKG UPC_W_C]]

foreach {img gen digits words} [list \
    ltn_rom.hex $REPO/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py \
                [expr {$TROM_W / 4}] $TROM_D \
    ucode.hex   $REPO/protocol-processor/hdl/aecp/ucode/gen_ucode.py \
                [expr {$UCODE_W / 4}] [expr {1 << $UPC_W}] \
    gptp_ucode.hex $REPO/gptp-processor/hdl/ucode/gen_gptp_ucode.py \
                [expr {$GUCODE_W / 4}] [expr {1 << $GUPC_W}]] {
  set tmp $img.gen.[pid]
  file delete -force $img $tmp
  # 2>@1, not -ignorestderr: a generator's stdout is unused, so merging keeps
  # its own diagnostic IN the refusal (-ignorestderr would leave only Tcl's
  # "child process exited abnormally") while still refusing on exit status
  # alone. A generator that writes a perfect image, exits 0 and emits one
  # Python warning used to abort here -- with the warning as the whole
  # message, $img already deleted at the line above, and $tmp orphaned
  # because the cleanup below is only on the validation path.
  if {[catch {exec python3 $gen -o $tmp 2>@1} out]} {
    file delete -force $tmp
    error "milan_datapath OOC: the generator for $img exited non-zero:\
 $gen\n$out"
  }
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
set GUCODE_GENERIC "GPTP_UCODE_HEX_P=\"[file normalize gptp_ucode.hex]\""

# And the refusal the tool itself already offers: a $readmem image Vivado
# cannot open is CRITICAL WARNING Synth 8-4445 and a completed run with a
# wrong number -- the one failure of this instrument that still returns a
# figure. Promote it to an ERROR so any image this preflight does not cover
# (a renamed image, a fourth $readmemh this preflight has not met) fails the
# run outright
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

# $INCS and $DEFINES are the record's own, in the record's own ORDER --
# see the derivation at the top. There is no hand list here to drift.
set DEFARGS {}
foreach d $DEFINES { lappend DEFARGS -verilog_define $d }

synth_design -mode out_of_context -top $TOP \
  -part xc7a100tfgg484-2 -include_dirs $INCS {*}$DEFARGS \
  -generic $TROM_GENERIC -generic $UCODE_GENERIC \
  -generic $GUCODE_GENERIC

# -quiet on a renamed port would hand create_clock an EMPTY object list and
# define a VIRTUAL clock: timing_$TAG.rpt would then report an essentially
# unconstrained design, at rc=0. Refuse instead of reporting that.
set CLK_NAME axis_clk
set CLK_PORT [get_ports -quiet $CLK_NAME]
if {[llength $CLK_PORT] != 1} {
  error "milan_datapath OOC: expected exactly one $CLK_NAME port after\
 synthesis, found [llength $CLK_PORT]. A virtual clock would report an\
 unconstrained design as if it were a timing result."
}
create_clock -period 10.000 -name clk $CLK_PORT
report_utilization -hierarchical -file util_hier_$TAG.rpt
report_utilization -file util_$TAG.rpt
report_timing_summary -delay_type max -max_paths 3 -file timing_$TAG.rpt
