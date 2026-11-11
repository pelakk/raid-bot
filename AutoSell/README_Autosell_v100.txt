Panda End Game autosell rules v100 (7 Nov 2026) - RaidBot 8.4

v100 = v99 + Anh's 7 Nov review (Make100_v0.1.py):
  1. Protection artifacts are A tier, not S (Protection accessories stay S: unchanged). It is taken out of v99's S-tier artifact lines ("S tier Epic+ to +12 before judging" and
     "kept from +12 on a substat rolled twice"), so it is judged by its own Protection rules again, as in v97.
     Example: a 5* Epic Protection chest, ATK% main, DEF / HP / ATK substats - v99 took it to +12 and kept it on
     the ATK x2; v100 sells it at +0.
  2. Upgrades that never fired now fire. In v99, some Upgrade 12 lines sat under a Keep that already matched every item
     they could match. RaidBot uses the first matching line, so the Keep always won and the upgrade never happened.
     Those Upgrade lines move right above their Keep: Harsh 28, End Game 28, Mid Game 39.
     Examples: Rare Mercurial/Merciless with SPD rolled at +8..+11, Feral SPD boots, 5* Mythic Protection
     accessories. After the upgrade the item is judged again at +12, where the Keep decides as before.
     A moved line that said "Set = GroupSets" has its set list written out, so it keeps its meaning in the new place.
  3. Never-reached lines removed (what RaidBot 8.4.4.0's rules editor shows as "never reached"). A line goes when an
     earlier line that stays in the file matches every item it could match, so it can never decide anything.
     Removed: Harsh 639, End Game 646, Mid Game 660. Almost all of them are v99's old Sell / Keep lines left
     under the new "Upgrade 12" lines.
  4. End Game and Mid Game: A-tier Mythics (5* and 6*) at +12 or more are kept when any substat has 2 rolls.
     RaidBot's log does not show which substat holds the Mythic bonus. Not for flat-main boots, which still need a 4x.
     A Keep line goes right above every artifact Sell that could catch such a piece, so Keeps and Upgrades above
     still decide first. Harsh is unchanged here.
     A tier = Protection, Speed, Swift Parry, Stone Skin, Shield, Savage, Instinct, Stonecleaver, Cruel, Slayer,
     Reflex, Impulse, Provoke, Relentless, Chronophage, Supersonic, Rebirth, Pinpoint, Bolster, Defiant.

Rules:   Harsh 4,587 -> 3,944   End Game 3,965 -> 3,378   Mid Game 3,502 -> 2,901
Battles12 = the Storage rules of the same level, line for line (only the header differs).
Weights: PandaHarsh_v0.3, PandaEndGame_v0.3, PandaMidGame_v0.5 (were v0.1 / v0.1 / v0.3). These are the same files
  with the tiers brought up to date: Swift Parry and Speed are A (were S), and Instinct is A with the damage
  profile (was not listed, so C / junk). Protection stays S: the weight file has one tier list for artifacts and
  accessories, and Protection accessories are S. Weights only rank the pieces the rules sell; Swift Parry
  accessories stay protected (never sold).

Checked (Python replay of RaidBot's first-match rules; an Upgrade N line only catches items below +N):
  - 542,711 different items through v99 and v100, for all 6 files: 400k random, 150k S/A Epic+ pieces at
    +8..+16, plus 3,752 items RaidBot logged on the farm on 6-7 Nov.
  - Several Sub conditions were read two ways (any substat may satisfy each, or each needs its own).
  - Every verdict that changed is one of the 4 changes above; nothing else changed.
  - Syntax: ASCII, CRLF, at most 4 Sub conditions per line, upgrade levels 4/8/12/16 only.
  - Changes_v100_<level>.csv lists every moved and every removed line, with the line that decided instead.
