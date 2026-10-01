import os, sys, time, json, subprocess
sys.path.insert(0, sys.argv[1] + "/tools")
import hostsrv
res = {}
r = hostsrv.TcpReceiver("/tmp/b4-a468/raw/r2-tcp-test", 18468, "tcp-test.bin", lambda **kw: res.update(kw))
rc = subprocess.run(["python3", "-B", sys.argv[1] + "/tools/soccon.py", os.environ["SOC_CONSOLE"], sys.argv[1] + "/soc/r2-tcp-test.log", "20", sys.argv[2]], timeout=50, capture_output=True).returncode
r.close(5)
print("SOC_RC=%d" % rc); print(json.dumps(res))
