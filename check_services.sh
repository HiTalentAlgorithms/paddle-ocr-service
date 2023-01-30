#!/bin/bash
unset GREP_OPTIONS
pid_result=`ps -aux | grep web_service.py | awk '{printf $2 "\n"}'`
gpid_result=`nvidia-smi --query-compute-apps=pid --format=csv,noheader`
python3 -c """
import os
import re
pid_result = '''$pid_result'''
gpid_result = '''$gpid_result'''
pid_list = set(l for l in pid_result.split('\n') if l)
gpid_list = set(l for l in gpid_result.split('\n') if l)
with open('config.yml','r') as f:
    content = f.read()
all_result = re.findall(r'concurrency:\s*([0-9]+)', content, re.I)
if len(pid_list & gpid_list) != sum(int(i) for i in all_result):
    exit(1)
exit(0)"""
python_exit_code=$?
echo "python exit code $python_exit_code"
if [ $python_exit_code != 0 ]; then
  echo "ocr server is not ready"
  exit $python_exit_code
  fi
