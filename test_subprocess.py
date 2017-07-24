# -*- coding: utf-8 -*-


import subprocess
import fcntl, os
import time

# pipe = subprocess.Popen("sh", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# flags = fcntl.fcntl(pipe.stdout, fcntl.F_GETFL)
# fcntl.fcntl(pipe.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

# pipe.stdin.write("ls \n")
# pipe.stdin.flush()

# time.sleep(2)
# out = pipe.stdout.read()

# print out


# 执行 qq 命令
pipe = subprocess.Popen("qq send buddy summer发 '---you'", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

flags = fcntl.fcntl(pipe.stdout, fcntl.F_GETFL)
fcntl.fcntl(pipe.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

# pipe.stdin.write("ls \n")
pipe.stdin.flush()

time.sleep(2)
out = pipe.stdout.read()

print out