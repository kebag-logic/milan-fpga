"""Compare the head copy patterns with an underscore-safe boundary variant.
Usage: python3 -I underscore_boundary.py"""
import re
def head(value, unit):
    pats = [rf"(?<![\d.,]){value}[\s-]?{unit}\b"]
    if unit == "ms" and value % 60000 == 0:
        m = value // 60000; w = "one two three four five six seven eight nine ten".split()[m - 1]
        pats += [rf"(?<![\d.,])\b{m}[\s-]?min(?:ute)?s?\b", rf"(?<![\w-]){w}[\s-]min(?:ute)?s?\b"]
    return pats
def safe(value, unit):
    return [p.replace(r"\b", r"(?![^\W_])", 1) if p.endswith(r"\b") else p for p in
            [q.replace(r"(?<![\d.,])\b", r"(?<![\d.,A-Za-z])").replace(r"(?<![\w-])", r"(?<![A-Za-z0-9-])")
                .replace(r"s?\b", r"s?(?![A-Za-z0-9])").replace(r"{unit}\b", "") for q in head(value, unit)]]
cases = [("The watch is _375 ms_.", 375, "ms", True), ("After _5 minutes_ it ceases.", 300000, "ms", True),
         ("After _five minutes_ it ceases.", 300000, "ms", True), ("The watch is 375 ms.", 375, "ms", True),
         ("A 5min countdown.", 300000, "ms", True), ("A five min countdown.", 300000, "ms", True),
         ("A 2.5 min hold.", 300000, "ms", False), ("A twenty-five minutes soak.", 300000, "ms", False),
         ("At least 5 minimum samples.", 300000, "ms", False), ("A 375 msec gap.", 375, "ms", False),
         ("A 1375 ms gap.", 375, "ms", False), ("snake_5_min", 300000, "ms", False)]
for text, v, u, copy in cases:
    h = any(re.search(p, text, re.I) for p in head(v, u))
    s = any(re.search(p.replace(r"(?![^\W_])", "(?![A-Za-z0-9])"), text, re.I) for p in safe(v, u))
    print(f"copy={copy!s:5} head={h!s:5} underscore_safe={s!s:5} {text!r}")
