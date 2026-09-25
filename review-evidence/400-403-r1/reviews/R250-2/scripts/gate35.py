#!/usr/bin/env python3
"""Run builder gate 35 (firmware boot transcript) alone from a tree root."""
import sys
sys.path.insert(0, "sw/builder")
import test_builder
test_builder.test_boot_policy_follows_the_declaration()
