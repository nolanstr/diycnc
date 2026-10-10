#!/bin/sh
# Optimization sweep, one run at a time (CHOLMOD already uses all cores).
# The published results used FEA_VOX=vox_previous (the frame before the optimization).
PY=${PY:-python3}
cd "$(dirname "$0")"
for run in "pocket 21" "pocket 28.5" "free 21" "pocket 24.5" "pocket 18" "free 18"; do
    set -- $run
    $PY topopt.py $1 $2 > log_$1_$2.txt 2>&1
done
