"""TASK F (revised) in Claude_Coop/COOP_RELAY.md.

Minimal Botting-framework isolation test. The raw Map.LeaveGH() call (LeaveGH_isolation_test.py)
did NOT crash, but the same call wrapped in the Botting framework's routine (LeaveGH() then
ForMapToChange(), with the framework's own polling during the transition) crashed 3/3 times on
fresh characters. This strips the leveler down to exactly those two steps -- no UI window, no
event callbacks, no upkeep config, no templates -- with action logging on so the console shows a
step-by-step trace right up to the faulting call.

Deliberately no bot.UI.draw_window() -- that's where the Start button lives, so this script starts
itself explicitly instead (see _started guard in main()), keeping the UI panel out as its own
separate variable for a later bisect.

Usage: load and run via Script Runner on a fresh character standing at Kormir on Island of Shehkah
(map 490), quest 0x82A501 already taken BY HAND first. Watch the Py4GW console for the log_actions
trace.
"""
from Py4GWCoreLib import *

MODULE_NAME = "LeaveGH Minimal Bot Test"

bot = Botting("Minimal LeaveGH", config_log_actions=True)


def routine(bot: Botting) -> None:
    bot.Map.LeaveGH()
    bot.Wait.ForMapToChange(target_map_id=544)


bot.SetMainRoutine(routine)

_started = False


def main():
    global _started
    if not _started:
        _started = True
        bot.Start()
    bot.Update()


if __name__ == "__main__":
    main()
