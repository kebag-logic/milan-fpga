import os,subprocess,sys,shlex
from pathlib import Path
work=Path(os.environ["WORK"]); root=work/"fabric-tree"
os.chdir(root)
os.environ["PYTHONPATH"]=os.environ["PICOLIBC_PYTHON"]+":"+os.environ["COMPILER_RT_PYTHON"]+":"+os.environ.get("PYTHONPATH","")
os.environ.update(PYTHONHASHSEED="0",SOURCE_DATE_EPOCH="1791849600")
subprocess.run([sys.executable,"sw/builder/endstation_builder.py","configs/endstation_ax7101_1x1_tdm8.yaml"],check=True)
code="import os,runpy,sys; os.cpu_count=lambda:8; sys.path.insert(0,os.path.abspath(\"sw/litex\")); sys.argv[0]=os.path.abspath(\"sw/litex/milan_soc.py\"); runpy.run_path(sys.argv[0],run_name=\"__main__\")"
args=shlex.split("--board ax7101 --milan-clk-freq 50e6 --gtx-tx-invert --floorplan --eth-port e1 --no-i2s-playback --no-render-lpf --num-streams 1 --audio-interface tdm8 --audio-interface-master --audio-interface-render 8 --talker-wire-chans 8 --loopback-lane --fabric-gptp --gptp-ingress-lat-ns 656 --gptp-egress-lat-ns 219 --cpu vexiiriscv --software-profile baremetal --xlen 32 --full --with-spiflash --flashboot baremetal --timing-opt --l2-bytes 0 --uart-baudrate 115200 --cpu-count 1")
subprocess.run([sys.executable,"-c",code,*args,"--entity-gen-dir",str(root/"configs/generated/endstation_ax7101_1x1_tdm8"),"--output-dir",str(work/"fabric-output")],check=True)
