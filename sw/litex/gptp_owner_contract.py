#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Shared gPTP-owner artifact enum and compiled soc.h encoding."""

#: "software": gPTP in the split firmware, the fabric keeping the timestamp unit and the PHC (#884, #665 F6)
GPTP_OWNERS = ("none", "fabric", "software")
GPTP_OWNER_CODES = {owner: code for code, owner in enumerate(GPTP_OWNERS)}
GPTP_OWNER_BY_CODE = {code: owner for owner, code in GPTP_OWNER_CODES.items()}
