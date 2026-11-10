# [A683ze] Another lane's gate driver stopped by this round (for the manager)

**What:** at about 15:26 CET on 2026-11-10, this round stopped its own superseded `firmware-verilator` and `firmware-boundary` workflow runs with `pgrep -f "firmware-verilator /data"`, then killed each match's whole process group. The pattern also matched lane **823-a753f**'s final gate driver: its `run_wf.py rtl-fast <sha> firmware-verilator /data-2/...` child, because `/data` is a prefix of `/data-2`. Two process groups matched that pattern, 426460 (this round's) and 3209317 (823-a753f's). Both were sent SIGTERM.

**Evidence** (read-only, in 823-a753f's scratch):
- `drive-a.log` ends at 15:24:42 with `rtl-fast.firmware-verilator__ci_step_13 rc=0`.
- `gates/final/logs/rtl-fast.firmware-verilator__ci_step_14.log` was last written at 15:24:44, and has no `.rc` file.
- No process of that job was alive at 15:27, while 823-a753f's other drivers (`elaborate-gates-1`, the `ctrl_nvm` self-test) were still running.

So driver A's `firmware-verilator` job (step 14, "Hold the TSN stack boundary over the Verilator builders' compiles"), and whatever driver A had queued after it, did not finish. They need to be re-run by that lane. Nothing of 823-a753f's was edited or deleted. The other matches killed in the same command were this round's own (the `firmware-boundary` run, group 4124299, and the sweep launcher, groups 282435 and 282437); 665s7-a757c's `firmware-boundary` and 665s11-a761's driver were checked alive afterwards.

**Why it happened:** the lane's own notes warned that generic patterns hit other lanes. This pattern was not scoped to this round's scratch path. From now on, every kill matches this round's scratch path or head SHA, and each match's arguments are listed before the kill.
