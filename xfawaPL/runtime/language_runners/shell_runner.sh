#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <script>" >&2
    exit 1
fi

script="$1"

# 执行脚本
bash "$script"
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "Shell execution failed with code $exit_code" >&2
    exit $exit_code
fi
