cd $CLONE/tb/pp_top && python3 aecp_dispatch_mutants.py --output $PACKET/scratch/disp-mut --verilator verilator --jobs 3 --only ai-entity-image-copy,ai-gather-constant,rdc-base-no-overlay
