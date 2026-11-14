# Review the AI-drafted profile import

**2026-10-23 09:30 UTC+01.** You are a security intern on the fictional Dovetailmoss desktop team. Bram used an AI assistant to write a profile import, so administrators can paste a studio or kiosk profile and see the proposed result. His pull request says it is validated and safe. Sena, who reviews security, wrote the contract this morning and wants a merge decision before lunch.

## Your mission

Give Sena a merge decision she can stand behind, with each problem you find reproduced locally, and an import that follows the contract so Bram has something concrete to merge or copy.

At minimum, by minute 35 `python3 -B cli.py <request>` with action `profile-import` accepts and rejects imports as `docs/profile-import-contract.md` describes, and you have a short review that lists each defect with a request that reproduces it and says which pull-request claims do not hold. Anything beyond that is up to you.

There is no single right answer. You choose whether to patch the draft, rewrite it or wrap it, and how you check it; explain your choices in `CHOICES.md`.

## What you have

`workspace/` is a small Python model of the Dovetailmoss catalog desk with a JSON CLI. Start with `workspace/README.md`, the source map in `docs/map.md` and the offline hints in `docs/offline-hints.md`. The decisive sources are `docs/profile-import-contract.md` (current rules), `docs/profile-import-pr.md` (the PR description and comments), `extension_catalog/profiles.py` (the draft) and the capability section of `docs/policy.md`. `docs/profile-import-history.md` is an older sketch.

Setup, before the clock starts: `cd workspace && python3 -B setup.py`. Sample: `python3 -B cli.py examples/profile-import.json`. Tests: `python3 -B -m unittest discover -s tests -v`; they do not cover the import.

Everything in `workspace/` is fictional and is the only source of truth. Python 3.11+ and its standard library are enough; no downloads.

## Rules

- You have **50 minutes** from the moment setup succeeds. The session is recorded.
- Use any editor and local tools. We expect you to use AI when available; local hints support the task if access fails. We assess verification, not subscriptions or internet speed.
- The engineer on the call can help with setup, audio or time, but not with the task. If something is unclear, make a reasonable assumption and note it in `CHOICES.md`.
- Do not contact real people or systems, publish anything, or use real credentials. Values marked `DEMO` are nonfunctional.

## What to send at minute 50

- Your workspace with your changes (git commits welcome), your checks, and the review for Sena as `workspace/REVIEW.md` (any layout).
- `CHOICES.md` (at most 300 words): what you built and why, what you chose not to do, how you checked the result, and one AI output you corrected or rejected (or a local check you used if AI was unavailable).

Aim for a result by minute 35, verify through 45. Unfinished work is fine; send what you have and say what you would do next.

## How it is assessed

Result 35 (does it help Sena decide), accuracy 25 (correct against the material), judgment 20 (sensible scope and trade-offs), process 20 (how you worked, as seen in the recording). Every approach can reach full marks. We do not score typing speed, tool choice, connection quality, machine speed, polish or volume.
