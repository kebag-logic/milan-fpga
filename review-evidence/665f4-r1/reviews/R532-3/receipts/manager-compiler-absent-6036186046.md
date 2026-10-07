[A10] Manager run of the compiler-absent docs check at `c1049de1`, which the lane could not finish inside its foreground limit:

`python3 sw/builder/test_firmware_compiler.py --absent --audit <scratch>/rv32-absent.jsonl` → **rc 0**, about 10 min.

- GATE 1b PASS.
- 1 NOT RUN, which is expected in the compiler-absent mode: the compiled CSR-address census needs an RV32 compiler.
- 0 firmware compiler invocations.

Log sha256 `ab0330e44601be05…`.
