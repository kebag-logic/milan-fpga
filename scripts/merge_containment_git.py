"""Git transport for the containment checker: filenames stay bytes (#423).

Git names files with bytes, not text.  Each path Git lists reaches the next
Git command as those bytes, and each patch reaches ``patch-id`` the same way;
Python's filesystem codec never sits between them.  Other Git output is text,
and output that does not encode back to its own bytes is not measured.
Diagnostics quote names as ASCII byte literals in every locale.
"""

import os
import subprocess

#! git_text's status for output it cannot decode reversibly.  No process exit
#! status is 256, so no caller can mistake it for Git's own 0 or 1.
RC_LOSSY_OUTPUT = 256


def git_bytes(*args: str | bytes) -> tuple[int, bytes]:
    """Run git, returning (rc, stdout bytes).  Never raises on a non-zero rc.

    A bytes argument reaches Git unchanged: a filename Git printed goes back
    as the same bytes, never through Python's filesystem codec.
    """
    #! Replacement objects rewrite the commit graph for every plumbing command.
    #! A local refs/replace entry can otherwise make a stranded branch appear
    #! to be an ancestor of the base.  Containment must measure stored commits,
    #! not a caller-specific alternate history.
    p = subprocess.run(("git", "--no-replace-objects", *args),
                       capture_output=True)
    return p.returncode, p.stdout


def git_text(*args: str | bytes) -> tuple[int, str]:
    """Run git, returning (rc, stdout text).  Never raises on a non-zero rc.

    Text uses the filesystem codec, which is also how a str argument reaches
    Git.  Output that does not encode back to the same bytes returns
    RC_LOSSY_OUTPUT and no text.
    """
    rc, out = git_bytes(*args)
    text = os.fsdecode(out)
    #! Some codecs map distinct bytes to one character: Big5 decodes a1 fe
    #! and re-encodes it as a2 41.  Returning that text would let a later
    #! command measure a different name.
    if os.fsencode(text) != out:
        return RC_LOSSY_OUTPUT, ""
    return rc, text.rstrip("\n")


def path_label(name: bytes) -> str:
    """Quote exact filename bytes as ASCII, whatever the process encoding."""
    return repr(name)[1:]
