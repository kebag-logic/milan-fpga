# Verilated -*- Makefile -*-
# DESCRIPTION: Verilator output: Make include file with class lists
#
# This file lists generated Verilated files, for including in higher level makefiles.
# See Vsim.mk for the caller.

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
  Vsim \
  Vsim___024root__0 \
  Vsim_sim__0 \
  Vsim_sim__1 \
  Vsim_sim__2 \
  Vsim_sim__3 \
  Vsim_sim__4 \
  Vsim_sim__5 \
  Vsim_sim__6 \
  Vsim_sim__7 \
  Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0 \
  Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1 \
  Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2 \
  Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__3 \
  Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__4 \
  Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__5 \
  Vsim_VexiiRiscv__0 \
  Vsim_VexiiRiscv__1 \
  Vsim_RegFileMem__0 \

# Generated module classes, non-fast-path, compile with low/medium optimization
VM_CLASSES_SLOW += \
  Vsim__ConstPool__0__Slow \
  Vsim__ConstPool__1__Slow \
  Vsim___024root__Slow \
  Vsim___024root__0__Slow \
  Vsim_sim__Slow \
  Vsim_sim__0__Slow \
  Vsim_sim__1__Slow \
  Vsim_sim__2__Slow \
  Vsim_sim__3__Slow \
  Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__Slow \
  Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__0__Slow \
  Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__1__Slow \
  Vsim_VexiiRiscvLitex_9fdf25696b8f525f981b84f78b4a1952__2__Slow \
  Vsim_VexiiRiscv__Slow \
  Vsim_VexiiRiscv__0__Slow \
  Vsim_VexiiRiscv__1__Slow \
  Vsim_KL_mbx_pkg__Slow \
  Vsim_RegFileMem__Slow \
  Vsim_RegFileMem__0__Slow \

# Generated support classes, fast-path, compile with highest optimization
VM_SUPPORT_FAST += \
  Vsim__Dpi \

# Generated support classes, non-fast-path, compile with low/medium optimization
VM_SUPPORT_SLOW += \
  Vsim__Syms__ctor__0__Slow \
  Vsim__Syms__dtor__0__Slow \
  Vsim__Syms__Slow \

# Global classes, need linked once per executable, fast-path, compile with highest optimization
VM_GLOBAL_FAST += \
  verilated \
  verilated_dpi \
  verilated_threads \

# Global classes, need linked once per executable, non-fast-path, compile with low/medium optimization
VM_GLOBAL_SLOW += \

# Verilated -*- Makefile -*-
