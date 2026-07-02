# Milan TSN NIC — Vivado build wrapper. Needs Vivado on PATH + a valid tool
# license (free "basic"/Standard tier covers xc7z020clg400-1).
#   make bd     — create project + block design, stop before synth (fast smoke test)
#   make synth  — through synthesis
#   make impl   — through implementation (no bitstream)
#   make bit    — full flow -> bitstream (default)
#   make clean  — remove bd/build/
VIVADO ?= vivado
.PHONY: bit synth impl bd clean
bit synth impl bd:
	$(VIVADO) -mode batch -notrace -source build.tcl -tclargs $@
clean:
	rm -rf build vivado*.jou vivado*.log .Xil
