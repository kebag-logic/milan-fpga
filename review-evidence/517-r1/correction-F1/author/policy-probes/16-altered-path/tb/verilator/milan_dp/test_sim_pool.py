            children = Path(f"/proc/foreign/self/task/{os.getpid()}/children").read_text().split()
