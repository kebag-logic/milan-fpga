#!/usr/bin/env bash
# plants_r4_all.sh JOBS NAME... : run_plant.sh NAME plants_r4.py, JOBS at a time,
# each to receipts/r4plant_NAME.log / .rc (make -k run; the first failing build ends the recipe)
P=$(cd "$(dirname "$0")/.." && pwd)
j=$1; shift
printf '%s\n' "$@" | xargs -P "$j" -I{} bash -c "'$P/scripts/run_plant.sh' {} '$P/scripts/plants_r4.py' > '$P/receipts/r4plant_{}.log' 2>&1; echo \$? > '$P/receipts/r4plant_{}.rc'"
