# R274-2 independent verdict and ledger, written BEFORE reading any prior review finding on PR #537

Exact head 70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6, tree ef96bf2fe0d66dd9c0b1ba45c6b4300d89ba658c.
Inputs read so far: AGENTS.md, CONTRIBUTING.md, docs/README.md, issues #394/#510/#511 bodies and the
manager's decision/assignment comments, the author's public REVIEW READY comments, the PR body, the full
diff 759da623..70f2c50d and the round diff 64bcf768..70f2c50d, the 802.1AS-2011/Cor1/Cor2/2020 and Milan
v1.2 texts, the pinned processors, the author's public correction-round receipts (gates, scope, history).
NOT yet read: PR comments by R274-1 and R275-1, their REPORT.md files and receipts.

Provisional verdict: POSITIVE (no BLOCKER, MAJOR or MINOR found in my own pass).

| Lens | State | Covering round | Head |
|---|---|---|---|
| Conformance | CLEAN | R274-2 | 70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6 |
| RTL | CLEAN | R274-2 | 70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6 |
| Robustness | CLEAN | R274-2 | 70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6 |
| Tests | CLEAN | R274-2 | 70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6 |
| Docs | CLEAN | R274-2 | 70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6 |

Own SUGGESTIONs (optional, do not affect coverage):
- S1 Conformance, Docs: A.5 MGT reads "management of the timing synchronization in Bridges"; end-station
  optionality also follows from 5.3/5.3.1 and Annex A having no management item. Cite both.
- S2 Docs: pre-existing AS-11 "12-16 Non-Ethernet media layers" spans Clauses 14/15 (management/MIB) in
  both editions, so the new AS-13 (14.6.9, Excluded) sits inside a range AS-11 marks Not applicable; the
  page also mixes 2020 (AS-8, AS-11) and 2011 (AS-13) numbering. Follow-up Issue, not this lane.
- S3 Conformance, Docs: PICS MINTA-8 (A.7, status O, 8.3) is the conformance-statement basis for optional
  modelling; the record cites only 8.3.
- S4 Docs: the 802.1AS-2020 comparison row's CMLDS cell summarises 11.2.17.2 a) only; with CMLDS the term
  also enters the Pdelay_Req correctionField and computePdelayRateRatio (11.2.17.2 b) and f)).
- S5 Tests: pinned pp_top has no per-command arm for 0x0001/0x0003/0x0004; a decode mutant accepting 0x0003
  as GET_MILAN_INFO passes the unmodified suite and is caught only by the probe arms. Processor-owned.
- S6 Tests: no committed builder test plants a gptp asymmetry key; the probe shows the refusal works.
