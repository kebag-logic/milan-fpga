# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0

@aecp @firmware
Feature: back-to-back state-changing commands from two controllers, with AECP's owed-notice queue
  The split firmware's AECP takes its next command while an earlier command's
  unsolicited notification is still owed (#894; the ruling of 2026-11-12 on
  aecp_ready). No clause orders a notification ahead of the next command or its
  response: IEEE 1722.1-2021 9.3.5.4 (Figure 9-3 gives the WAITING state's
  doUnsolicited and rcvdAEMCommand guards no priority) and 7.5.2; Milan v1.2
  5.4.5.2 ("sent asynchronously of any command", "immediately"). It holds under
  four conditions, and these scenarios state them on the wire:
    (a) every recipient receives the notifications in the order their commands
        were taken, each at its own next sequence_id (Milan v1.2 5.4.5.1;
        IEEE 1722.1-2021 9.3.5.2.6), and a requester never receives its own;
    (b) a command's own response precedes the notifications it causes (Milan
        v1.2 5.4.5.2);
    (c) the queue is bounded: AECP takes no command while it is full;
    (d) this feature and the firmware's unit tests (test_aecp.cpp, Queued) cover
        two controllers' back-to-back commands.

  WHAT THIS LAYER IS. An offline model of the queue's rules, in the manner of
  the rest of the suite, each rule pinned to the shipped source that makes it
  (sw/firmware/ctrl/aecp/aecp.c and aecp_mbx.h): a source change that drops a
  rule fails the scenario that states it. The unit tests run the firmware.

  Background:
    Given AECP's owed-notice rules read from the shipped firmware
    And controllers A, B and C registered for unsolicited notifications

  Scenario: A's and B's commands back to back, the second taken while the first's notice is owed
    When A sends a state-changing command and B sends one before any notice leaves
    Then the wire carries A's response, then B's response, then the notices
    And C receives A's notice before B's, at consecutive sequence_ids
    And A receives only B's notice and B only A's

  Scenario: the queue is bounded and AECP takes no command while it is full
    When commands fill the owed-notice queue at its depth
    Then AECP is not ready for the next command
    And one notice sent frees one slot and AECP is ready again

  Scenario: a notification longer than a slot waits behind the queue, its response first
    When A sends a state-changing command and B sends one whose notice is longer than a slot
    Then B's response is held until the poll and precedes B's notice
    And C receives A's notice before B's
