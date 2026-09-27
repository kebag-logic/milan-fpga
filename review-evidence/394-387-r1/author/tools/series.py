"""Sequential foreground cycles; each releases its own bench lock."""
from pathlib import Path
import json,subprocess,sys
p=Path(__file__).resolve().parent
for n in range(int(sys.argv[1]),int(sys.argv[2])+1):
 prev=json.loads((p.parent/f"cycle{n-1:02d}"/'analysis.json').read_text())
 assert prev['steady_recovered'],"STOP: preceding cycle not recovered"
 assert prev['switch_frames_absent_off'] and prev['proof_dut_alive'],"STOP: outlet proof failed"
 name=f"cycle{n:02d}";dest=p.parent/name;dest.mkdir(exist_ok=True)
 print("START "+name,flush=True)
 args=["rtk","proxy","timeout","-k","20s","120s","flock","-w","5","/tmp/milan-bench.lock","timeout","-k","15s","112s","python3","-B",str(p/'action.py'),name,"90",*sys.argv[3:]]
 with (dest/'action-log.txt').open('w') as out:r=subprocess.run(args,stdout=out,stderr=subprocess.STDOUT,timeout=142)
 if r.returncode:raise SystemExit("STOP: action rc "+str(r.returncode))
 r=subprocess.run(["rtk","proxy","timeout","20s","python3","-B",str(p/'analyze.py'),name],stdout=subprocess.DEVNULL,timeout=22,check=True)
 subprocess.run(["rtk","proxy","timeout","10s","python3","-B",str(p/'ledger.py')],timeout=12,check=True)
 s=json.loads((dest/'analysis.json').read_text())
 print(json.dumps(dict(cycle=n,recovered=s['steady_recovered'],gptp_s=s['gptp_recovery_s'],media=s['media_locked_at'],servo=s['servo_locked_at'],step=s['large_phc_discontinuities'],wire=s['wire'],link_delta=s['counter_endpoints']['dut:counter-9-0']['delta'])),flush=True)
 if not s['steady_recovered']:raise SystemExit("PAUSE: observe through the 180 s recovery deadline before deciding STOP")
