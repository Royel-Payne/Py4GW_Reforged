"""TASK H (part 1) in Claude_Coop/COOP_RELAY.md -- which of the two polls actually faults?

LeaveGH_minimal_bot_test.py runs bot.Map.LeaveGH() + bot.Wait.ForMapToChange() together and
crashes deterministically. This splits them: ONLY LeaveGH() here, ForMapToChange removed entirely.

- CRASHES  -> the fault is inside LeaveGH's own internal coroutine (_coro_leave_gh), specifically
              its internal Wait._coro_until_on_outpost() poll.
- SURVIVES -> the fault is in ForMapToChange's _coro_for_map_to_change poll instead.

Either result hands Apo the exact guilty coroutine, not "somewhere in the framework."

Usage: run on a FRESH character on Island of Shehkah (map 490), quest 0x82A501 taken by hand at
Kormir (10289, 6405) first, via Script Runner.
"""
from Py4GWCoreLib import *

MODULE_NAME = "LeaveGH Only Test"

bot = Botting("LeaveGH Only")


def routine(bot: Botting) -> None:
    bot.Map.LeaveGH()


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
