#!/bin/bash
python3 $WORK/record_measurements.py
echo "$?" > $WORK/record-measurements.rc
