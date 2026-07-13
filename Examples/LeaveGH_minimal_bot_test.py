"""TASK F (revised) in Claude_Coop/COOP_RELAY.md.

Minimal Botting-framework isolation test. The raw Map.LeaveGH() call (LeaveGH_isolation_test.py)
did NOT crash, but the same call wrapped in the Botting framework's routine (LeaveGH() then
ForMapToChange(), with the framework's own polling during the transition) crashed 3/3 times on
fresh characters. This strips the leveler down to exactly those two steps -- no UI window, no
event callbacks, no upkeep config, no templates -- with action logging on so the console shows a
step-by-step trace right up to the faulting call.

Deliberately no bot.UI.draw_window() -- that's where the Start button lives, so this script starts
itself explicitly instead, keeping the UI panel out as its own separate variable for a later bisect.

Start() must come AFTER the first Update() call, not before: SetMainRoutine() only stores the
routine, it never runs it -- Update() is what calls Routine() (registering the FSM's states) on its
first tick, gated by `not self.config.initialized`. Start() requires non-empty states or it raises
ValueError. So the sequence has to be Update() first (registers + sets initialized), then Start()
once initialized is confirmed true -- not the other way around.

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
    bot.Update()
    if not _started and bot.config.initialized:
        _started = True
        bot.Start()


if __name__ == "__main__":
    main()
