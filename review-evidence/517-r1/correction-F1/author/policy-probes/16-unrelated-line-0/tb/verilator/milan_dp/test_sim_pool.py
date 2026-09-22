            children = Path(f"/proc/self/task/{os.getpid()}/children").read_text().split()
The target requires /proc
