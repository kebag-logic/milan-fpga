import re, sys
# summarise a Vivado report_timing file: slack, levels, source -> destination
for f in sys.argv[1:]:
    t = open(f).read()
    print("==", f)
    for blk in t.split("Slack")[1:]:
        s = re.search(r"([-+]?\d+\.\d+)ns", blk).group(1)
        src = re.search(r"Source:\s+(\S+)", blk).group(1)
        dst = re.search(r"Destination:\s+(\S+)", blk).group(1)
        lv = re.search(r"Logic Levels:\s+(\d+)\s*(\(.*?\))?", blk)
        dp = re.search(r"Data Path Delay:\s+(\S+)", blk).group(1)
        print(f"  slack {s:>8}  levels {lv.group(1):>2}  dp {dp:>9}  {src} -> {dst}")
