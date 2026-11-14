import os
import sys
import subprocess

# A cached tool installation is read-only for this review.
original = subprocess.check_call
def guarded_call(command, *args, **kwargs):
    if isinstance(command, str) and ('sbt ' in command or 'git pull' in command or 'git checkout' in command):
        raise RuntimeError('Review refuses shared tool generation or checkout mutation: ' + command)
    return original(command, *args, **kwargs)
subprocess.check_call = guarded_call

def guard(event, args):
    if event == 'open':
        name, mode, flags = args
        if not isinstance(name, (str, bytes)):
            return
        if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC):
            path = os.path.realpath(name)
            allowed = os.environ['REVIEW_SCRATCH']
            if path != '/dev/null' and not path.startswith(allowed + '/'):
                raise RuntimeError('Review refuses write outside scratch: ' + path)
sys.addaudithook(guard)
