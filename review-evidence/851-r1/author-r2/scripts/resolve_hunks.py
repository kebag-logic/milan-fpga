"""resolve_hunks.py <file> <choice>...: resolve a file's merge-conflict hunks in order, one choice per hunk.
choice: ours | theirs | ours+theirs | theirs+ours | custom:<path> (the hunk becomes that file's text).
Refuses unless the number of choices equals the number of hunks, and unless no marker is left afterwards.
Prints one line per hunk: index, first line number, choice, line counts of each side."""
import sys
from pathlib import Path

path = Path(sys.argv[1]); choices = sys.argv[2:]
lines = path.read_text().splitlines(keepends=True)
out, i, hunk = [], 0, 0
while i < len(lines):
    if lines[i].startswith("<<<<<<< "):
        start = i + 1
        j = i + 1
        while not lines[j].startswith("======="):
            j += 1
        k = j + 1
        while not lines[k].startswith(">>>>>>> "):
            k += 1
        ours, theirs = lines[i + 1:j], lines[j + 1:k]
        if hunk >= len(choices):
            sys.exit(f"more hunks than choices ({len(choices)})")
        c = choices[hunk]
        if c == "ours":
            out += ours
        elif c == "theirs":
            out += theirs
        elif c == "ours+theirs":
            out += ours + theirs
        elif c == "theirs+ours":
            out += theirs + ours
        elif c.startswith("custom:"):
            out += Path(c[7:]).read_text().splitlines(keepends=True)
        else:
            sys.exit(f"unknown choice {c}")
        print(f"hunk {hunk}: line {start}, {c}, ours {len(ours)} lines, theirs {len(theirs)} lines")
        hunk += 1
        i = k + 1
    else:
        out.append(lines[i]); i += 1
if hunk != len(choices):
    sys.exit(f"{hunk} hunks, {len(choices)} choices")
text = "".join(out)
if any(l.startswith(("<<<<<<< ", ">>>>>>> ")) or l.rstrip("\n") == "=======" for l in text.splitlines()):
    sys.exit("marker left")
path.write_text(text)
