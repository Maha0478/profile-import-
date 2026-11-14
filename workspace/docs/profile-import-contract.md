# Profile import contract

Current. Owner Sena, effective 2026-10-23 08:30 UTC+01. Applies together with the capability section of `policy.md`. `docs/profile-import-history.md` is an older sketch and is superseded.

Studio and kiosk profiles are trusted saved policy. Administrators want to paste a profile as JSON and see the proposed result before Sena approves it. The import is a proposal: nothing is saved, and no request can change how the `capability` action decides today.

## Interface

- CLI: `python3 -B cli.py <request.json>` with `{"action": "profile-import", "profile": {"name": ..., "allow": [...], "deny": [...]}}`.
- Module: `extension_catalog.profiles.import_profile(store, proposal)`, where `store` is the object `storage.load()` returns.
- Accepted: `{"ok": true, "mode": "proposal-only", "name": <name>, "profile": {"allow": [...], "deny": [...]}, "profiles": {<every profile, with this one added or replaced>}}`.
- Rejected: `{"ok": false, "reason": <short text>}`. Reason wording is free. Both exit 0.

## Rules

1. `name` is an existing profile (`studio`, `kiosk`) or a new name of 2-24 characters: lowercase letters, digits and `-`, starting with a letter.
2. `allow` and `deny` are both required and must be JSON lists of strings. Anything else, including a single string, rejects the import. Repeated entries collapse to one, keeping first-appearance order.
3. Every capability in either list must appear in `catalog_policy.known_capabilities`; an unknown capability rejects the import. Capability names are matched exactly as written.
4. A banned capability (`catalog_policy.banned_capabilities`, today `clipboard.read`) may never appear in `allow`. It may appear in `deny`.
5. Denies are sticky. For an existing profile, every capability in its saved `deny` must still be in the proposed `deny`; otherwise the import is rejected. Removing a deny needs Sena's written approval outside this tool. Adding denies is fine.
6. Deny wins. A capability listed in both `allow` and `deny` must stay in `deny`; keeping or dropping it from `allow` are both acceptable.
7. The import never changes its inputs: the store object passed in, the request, and `fixtures/store.json` stay exactly as they were.

## Not covered

There is no administrator identity in this model. The import does not check who sent it, does not sign or verify anything, and does not save. Anything the review says about authentication or signatures would be outside what this code can show.
