"""Diagnostic isolation test for TASK E in Claude_Coop/COOP_RELAY.md.

Fires ONLY Map.LeaveGH() -- nothing else -- to test whether calling it while NOT actually in a
guild hall is what crashes Gw.exe during the Nightfall leveler's Skip_Tutorial() step. No bot
framework, no other game calls, deliberately minimal so a crash can only be attributed to this one
native call.

Usage: load and run via Script Runner (or the in-game "Select Python Script" dialog) while standing
on Island of Shehkah (or wherever), NOT in a guild hall. The action is queued once on first main()
tick, then the queue is drained every frame same as any other Py4GW script.
"""
from Py4GWCoreLib import *

MODULE_NAME = "LeaveGH Isolation Test"

_fired = False


def main():
    global _fired
    if not _fired:
        _fired = True
        ConsoleLog(MODULE_NAME, "Firing Map.LeaveGH() now -- this is the only action this script takes.")
        Map.LeaveGH()

    ActionQueueManager().ProcessQueue("ACTION")


if __name__ == "__main__":
    main()
