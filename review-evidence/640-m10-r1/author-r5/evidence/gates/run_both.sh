#!/usr/bin/env bash
echo $$ > $VALIDATION_STORAGE/640-a720o/gates/run_both.pid
bash $VALIDATION_STORAGE/640-a720o/gates/run_all.sh > $VALIDATION_STORAGE/640-a720o/gates/run_all.out 2>&1
bash $VALIDATION_STORAGE/640-a720o/gates/run_extra.sh > $VALIDATION_STORAGE/640-a720o/gates/run_extra.out 2>&1
date -Is > $VALIDATION_STORAGE/640-a720o/gates/run_both.end
