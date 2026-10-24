#!/usr/bin/env bash
# copy a text receipt with host paths replaced by placeholders: sanitize.sh <src> <dst>
sed -e 's#$VALIDATION_STORAGE/scratch/780-a670#<scratch>#g' -e 's#$LANES/780-pin5-shard\([0-3]\)#<clone>\1#g' \
    -e 's#$LANES/780-pin5#<lane>#g' -e 's#$MANAGEMENT/2026-09-23/780-a670#<out>#g' \
    -e 's#$VALIDATION_TOOLS#<tools>#g' -e 's#$VALIDATION_STORAGE/scratch/a662#<tools>/a662#g' -e 's#$VALIDATION_STORAGE/679-a557/sdk#<sdk>#g' \
    -e 's#$WORKSPACE_HOME/Xilinx#<xilinx>#g' -e 's#$WORKSPACE_HOME#<home>#g' -e 's#$VALIDATION_STORAGE#<data>#g' "$1" > "$2"
