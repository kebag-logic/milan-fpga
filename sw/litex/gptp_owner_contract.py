#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Shared gPTP-owner artifact enum and compiled soc.h encoding.

The 'software' code is RETIRED (#259, bare-metal-only product): no build
emits it any more and every flash tool refuses it. It stays in the enum so
old soc.h files and layouts DECODE to a named state that the tools can
refuse with a reason instead of an unknown-code crash."""

GPTP_OWNERS = ("none", "fabric", "software")
GPTP_OWNER_CODES = {owner: code for code, owner in enumerate(GPTP_OWNERS)}
GPTP_OWNER_BY_CODE = {code: owner for owner, code in GPTP_OWNER_CODES.items()}
