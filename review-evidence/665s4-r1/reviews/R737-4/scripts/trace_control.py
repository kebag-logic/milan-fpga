import os, signal, subprocess, sys, time
kid = "import os,signal,time; time.sleep(0.2); os.kill(os.getppid(), signal.SIGTERM)"
inner = f"import subprocess,sys,signal; signal.signal(signal.SIGTERM, lambda *_: sys.exit(0)); p=subprocess.Popen([sys.executable,'-c',{kid!r}], start_new_session=True); p.wait()"
print(subprocess.run([sys.executable, '-c', inner]).returncode)
