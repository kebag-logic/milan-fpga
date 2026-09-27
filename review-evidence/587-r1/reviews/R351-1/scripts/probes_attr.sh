#!/bin/bash
# Recipe "Boundary-preserving attribution" probes, applied to the reviewer attribution checkpoint.
S=$REVIEWS/587-r351-1-packet/scratch; D=$S/work-attr/probes; C=$S/work-attr/ax8x8/gateware/alinx_ax7101_synth.dcp
export PATH="$HOME/Xilinx/2026.1/Vivado/bin:/usr/bin:/bin" HOME=$HOME
cd $D
vivado -mode batch -source $S/probes/boundary.tcl -nojournal -log boundary.log -tclargs $C $D/boundary.tsv > /dev/null 2>&1; echo "boundary rc=$?" > $D/probes.rc
vivado -mode batch -source $S/probes/loads.tcl -nojournal -log loads.log -tclargs $C milan_datapath/pp_shadow/u_pp/u_aecp/u_dyn $D/loads.tsv > /dev/null 2>&1; echo "loads rc=$?" >> $D/probes.rc
vivado -mode batch -source $S/probes/loads.tcl -nojournal -log wrapper-loads.log -tclargs $C milan_datapath/pp_shadow $D/wrapper-loads.tsv > /dev/null 2>&1; echo "wrapper-loads rc=$?" >> $D/probes.rc
