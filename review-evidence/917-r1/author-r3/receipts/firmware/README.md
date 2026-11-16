# The firmware gate at 394612c5

`python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32` on a clean clone of 394612c5, with the
pinned gates venv's Python and the pinned RV32 SDK: `test_ctrl_firmware: PASS`, rc 0, the clone clean before and
after. Its arms build the mailbox contract's two-interface variant through `gen_mailbox.py --variant-interfaces`,
the path this round's generator change sits beside.

The first attempt (`first-attempt-without-pyyaml.log`) ran the host's system Python under the runner's scratch
HOME, which has no PyYAML; `mailbox_model.py` has always imported yaml, so the gate refused at its first generator
call. A second attempt was started without the venv by mistake and stopped by PID before it compiled anything; its
log held only the header line. The run above is the third.
