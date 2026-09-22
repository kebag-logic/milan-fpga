            children = Path(f"/proc/self/task/{os.getpid()}/children").read_text().split() # CONFIG_NET=y
