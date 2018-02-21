# coding=utf-8
"""
filename: gunicorn_config.py
install : pip install gunicorn
sample: gunicorn flask_app:app -c gunicorn_config.py
"""

import sys
import os
import multiprocessing

# 获取本文件的所在路径
curr_dir = os.path.dirname(os.path.realpath(__file__))
# 获取上级目录的绝对路径
last_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# 设置Flask App工作目录路径
app_dir = last_dir

_file_name = os.path.basename(__file__)

sys.path.insert(0, app_dir)

# === Server Socket ===
bind = "0.0.0.0:8000"       # default: "127.0.0.1:8000"

# === Server Socket End ===



# === Server Mechanics ===

chdir = app_dir

# Switch worker processes to run as this user.
# user =

# === Server Mechanics End ===



# === Worker Processes ===

# 进程数
workers = 1
# workers = multiprocessing.cpu_count() * 2 + 1

# 'gevent' or 'sync', default gevent
worker_class = 'sync'

# The maximum number of simultaneous clients.
worker_connections = 1000

# Workers silent for more than this many seconds are killed and restarted.
timeout = 30

# The maximum number of requests a worker will process before restarting.
max_requests = 2000

# Timeout for graceful workers restart.
graceful_timeout = 30

# === Worker Processes End ===



# === Logging ===

# 错误日志

# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
# The granularity of Error log outputs.
loglevel = 'info'

# The Error log file to write to.
# Using '-' for FILE makes gunicorn log to stderr.
# Changed in version 19.2: Log to stderr by default.
# errorlog = '-'
errorlog = "/dev/null"
# accesslog = os.path.join(curr_dir, "err.err")

# Redirect stdout/stderr to Error log.
# default: False
# capture_output = False

# 访问日志

# 访问日志文件的路径
# The Access log file to write to.
# '-' means log to stdout.
accesslog = '-'
# accesslog = "/dev/null"
# accesslog = os.path.join(curr_dir, "acc.log")

# 设置gunicorn访问日志格式，错误日志无法设置
# """
# h           remote address
# l           '-'
# u           currently '-', may be user name in future releases
# t           date of the request
# r           status line (e.g. ``GET / HTTP/1.1``)
# s           status
# b           response length or '-'
# f           referer
# a           user agent
# T           request time in seconds
# D           request time in microseconds
# L           request time in decimal seconds
# p           process ID
# {Header}i   request header
# {Header}o   response header
# """
# default: %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

# default: False
# syslog = False

# === Logging End ===



# === Process Naming ===

# A base to use with setproctitle for process naming.
# proc_name =

# === Process Naming End ===
