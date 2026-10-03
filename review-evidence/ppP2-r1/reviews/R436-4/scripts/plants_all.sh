#!/usr/bin/env bash
# plants_all.sh JOBS NAME... : run_plant.sh for each NAME with plants_drain.py, JOBS at a time,
# each to receipts/plant_NAME.log / .rc
P=$(cd "$(dirname "$0")/.." && pwd)
j=$1; shift
printf '%s\n' "$@" | xargs -P "$j" -I{} bash -c "'$P/scripts/run_plant.sh' {} '$P/scripts/plants_drain.py' > '$P/receipts/plant_{}.log' 2>&1; echo \$? > '$P/receipts/plant_{}.rc'"
