# PR 214: profile import

Author Bram, 2026-10-22 18:05 UTC+01. Written with an AI assistant from the ticket; I read it through and ran the example.

Adds `extension_catalog/profiles.py`, the `profile-import` action and `examples/profile-import.json`.

- Only administrators can call the import, so it is authenticated by design.
- Imports are fully validated and contradictory entries are cleaned up automatically.
- Kiosk can never be weakened by an import.
- The existing public tests pass.

## Review comments

- **Sena** (2026-10-23 08:40 UTC+01): I wrote the contract this morning; please review against it rather than against the ticket. I need a merge decision with each problem reproduced.
- **Izel** (2026-10-23 08:55 UTC+01): Could we lowercase capability names on import? People type `Canvas.Read`.
- **Bram** (2026-10-23 09:00 UTC+01): Happy to fix whatever the review finds; tell me what to change and why.
