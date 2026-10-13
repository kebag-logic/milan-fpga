#!/bin/bash
python3 $WORK/validation_resume.py
result=$?
printf "%s\n" "$result" > $WORK/validation-resume.rc
exit "$result"
