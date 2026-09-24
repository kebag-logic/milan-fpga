import sys, subprocess, tempfile, io, contextlib
from pathlib import Path
from unittest.mock import patch
sdk=Path(sys.argv[1]); spelling=sys.argv[2]
REPO=Path("$REVIEWS/r272-2-408")
sys.path.insert(0,str(REPO/"scripts")); sys.path.insert(0,str(REPO/"sw/builder"))
import ci_rv32_sdk as sdklib
import zzz_dev_probe_builder as builder
fw_path=REPO/"sw/firmware/milan_baremetal/milan_baremetal.c"
real_fw=fw_path.read_text(encoding="utf-8")
uart_tail="\tprint_tod(gettime_ns());\n}"
store="\t*(volatile unsigned int *)0x90000600u = 1u;"
guards={"control_hash":("#ifdef CSR_UART_BASE","#endif"),
        "split_digraph":("%\\\n:ifdef CSR_UART_BASE","%\\\n:endif")}
go,gc=guards[spelling]
hostile=real_fw.replace(uart_tail,f"{go}\n{store}\n{gc}\n{uart_tail}",1)
selector=str(Path.home()/"br-milan-rv32/host/bin/riscv32-linux-gcc"); mapped=str(sdk/sdklib.COMPILER)
real_run=subprocess.run
def run(argv,**kw):
    argv=[str(a) for a in argv]
    if argv and argv[0]==selector: argv=[mapped]+argv[1:]
    return real_run(argv,**kw)
real_rt=Path.read_text
def rt(self,*a,**k): return hostile if self.resolve()==fw_path.resolve() else real_rt(self,*a,**k)
sdklib.verify(sdk)
with tempfile.TemporaryDirectory(prefix="pdev-") as tmp:
    with patch.object(subprocess,"run",side_effect=run),patch.object(Path,"read_text",rt), \
         patch.object(sys,"argv",[__file__,"--require-rv32"]),patch.object(builder,"OUT",Path(tmp)), \
         patch.object(builder,"SKIPPED",[]):
        try:
            with contextlib.redirect_stdout(io.StringIO()): builder.test_baremetal_profile_contract()
        except (AssertionError,ValueError) as exc:
            print(f"[dev {spelling}] REFUSED: {str(exc).replace(chr(10),' ')[:280]}"); sys.exit(0)
        else:
            print(f"[dev {spelling}] ACCEPTED"); sys.exit(7)
