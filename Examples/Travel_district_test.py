"""TASK H (part 2) in Claude_Coop/COOP_RELAY.md -- does ANY map transition crash, or just LeaveGH?

Supersedes Travel_minimal_bot_test.py, which was broken: it tried to Travel() to a different
outpost (Kamadan, 449), but a level-1 who just cleared the tutorial has no other outpost unlocked
to travel TO. Travel_To_Random_District() sidesteps that entirely -- it forces a real reload of
the map you're ALREADY standing in (a district change), so it works with zero unlocks required.

Run on an already-crashed character (Rogue/Grim/Hollow/Nomad), all of whom are confirmed sitting
safely in Chahbek Village outpost (map 544) -- the server-side transfer completed before their
client died last time, so nothing was lost.

- CRASHES  -> any Botting bot that triggers a map transition kills the client. Every bot in the
              repo opens with some form of travel -- this is the bigger, more damning report.
- SURVIVES -> it's specific to the LeaveGH transition, not map transitions generally.

Usage: run via Script Runner on a character currently in Chahbek Village outpost.
"""
from Py4GWCoreLib import *

MODULE_NAME = "Travel District Test"

bot = Botting("District Travel")


def routine(bot: Botting) -> None:
    bot.Map.Travel_To_Random_District(target_map_id=544)
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
