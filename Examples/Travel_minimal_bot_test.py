"""TASK G in Claude_Coop/COOP_RELAY.md -- does ANY Botting-driven map transition crash, or just LeaveGH?

The LeaveGH minimal bot (Examples/LeaveGH_minimal_bot_test.py) deterministically crashed Gw.exe on
4 characters. This is the control test App Claude proposed: same framework, same polling pattern,
but a completely ordinary Map.Travel() instead of LeaveGH(). No fresh character needed -- run this
on one of the already-crashed characters, who should already be standing in Chahbek Village outpost
(map 544) after their last crash+relaunch, since the transfer completed server-side before the
client died.

- CRASHES  -> any Botting bot that zones kills the client. Every bot in the repo opens with
              Map.Travel() -- this is the report to send Apo, and it's not LeaveGH-specific.
- SURVIVES -> the bug is specific to the LeaveGH transition, not map transitions generally.
              Narrows the search back to LeaveGH's own coroutine.

Travels Chahbek Village (544) -> Kamadan, Jewel of Istan (449), a normal outpost-to-outpost hop.
Uses the same Update()-before-Start() ordering fix already confirmed necessary for the LeaveGH test
(SetMainRoutine() only stores the routine; Update() is what actually runs it and populates the FSM).

Usage: load and run via Script Runner on a character already standing in Chahbek Village outpost.
"""
from Py4GWCoreLib import *

MODULE_NAME = "Travel Minimal Bot Test"

bot = Botting("Minimal Travel", config_log_actions=True)


def routine(bot: Botting) -> None:
    bot.Map.Travel(target_map_id=449)
    bot.Wait.ForMapToChange(target_map_id=449)


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
