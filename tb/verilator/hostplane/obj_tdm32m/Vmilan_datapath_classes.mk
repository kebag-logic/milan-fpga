# Verilated -*- Makefile -*-
# DESCRIPTION: Verilator output: Make include file with class lists
#
# This file lists generated Verilated files, for including in higher level makefiles.
# See Vmilan_datapath.mk for the caller.

### Switches...
# C11 constructs required?  0/1 (always on now)
VM_C11 = 1
# Timing enabled?  0/1
VM_TIMING = 0
# Coverage output mode?  0/1 (from --coverage)
VM_COVERAGE = 0
# Parallel builds?  0/1 (from --output-split)
VM_PARALLEL_BUILDS = 1
# Tracing output mode?  0/1 (from --trace-fst/--trace-saif/--trace-vcd)
VM_TRACE = 0
# Tracing output mode in FST format?  0/1 (from --trace-fst)
VM_TRACE_FST = 0
# Tracing output mode in SAIF format?  0/1 (from --trace-saif)
VM_TRACE_SAIF = 0
# Tracing output mode in VCD format?  0/1 (from --trace-vcd)
VM_TRACE_VCD = 0
# VPI enabled?  0/1 (from --vpi)
VM_VPI = 0

### Object file lists...
# Generated module classes, fast-path, compile with highest optimization
VM_CLASSES_FAST += \
  Vmilan_datapath \
  Vmilan_datapath___024root__0 \
  Vmilan_datapath___024root__1 \
  Vmilan_datapath___024root__2 \
  Vmilan_datapath___024root__3 \
  Vmilan_datapath___024root__4 \
  Vmilan_datapath___024root__5 \
  Vmilan_datapath___024root__6 \
  Vmilan_datapath_axi_stream_if__0 \
  Vmilan_datapath_axi_stream_if__TC3__0 \

# Generated module classes, non-fast-path, compile with low/medium optimization
VM_CLASSES_SLOW += \
  Vmilan_datapath__ConstPool__0__Slow \
  Vmilan_datapath___024root__Slow \
  Vmilan_datapath___024root__0__Slow \
  Vmilan_datapath___024root__1__Slow \
  Vmilan_datapath___024root__2__Slow \
  Vmilan_datapath___024root__3__Slow \
  Vmilan_datapath___024unit__Slow \
  Vmilan_datapath_axi_stream_if__Slow \
  Vmilan_datapath_axi_stream_if__0__Slow \
  Vmilan_datapath_axi_stream_if__TC3__Slow \
  Vmilan_datapath_axi_stream_if__TC3__0__Slow \

# Generated support classes, fast-path, compile with highest optimization
VM_SUPPORT_FAST += \
  Vmilan_datapath__Dpi \

# Generated support classes, non-fast-path, compile with low/medium optimization
VM_SUPPORT_SLOW += \
  Vmilan_datapath__Syms__Slow \

# Global classes, need linked once per executable, fast-path, compile with highest optimization
VM_GLOBAL_FAST += \
  verilated \
  verilated_dpi \
  verilated_threads \

# Global classes, need linked once per executable, non-fast-path, compile with low/medium optimization
VM_GLOBAL_SLOW += \

# Verilated -*- Makefile -*-
