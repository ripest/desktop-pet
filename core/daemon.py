import os
import sys
from core.conf import settings


def daemonize():
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    os.chdir(".")
    os.setsid()
    os.umask(0)
    _pid = os.fork()
    if _pid > 0:
        sys.exit(0)
    sys.stdout.flush()
    sys.stdin.flush()
    sys.stderr.flush()
    si = open(str(settings.SETUP_DIR / "stdin"), 'a+')
    so = open(str(settings.SETUP_DIR / "stdout"), 'a+')
    se = open(str(settings.SETUP_DIR / "stderr"), 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


