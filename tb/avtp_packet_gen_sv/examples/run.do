if [file exists "work"] {vdel -all}
vlib work

vlog -f tb.f

vopt top -o top_optimized
vsim top_optimized -sv_seed random
set NoQuitOnFinish 1
run -all
quit -sim