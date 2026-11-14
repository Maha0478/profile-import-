# PR 214 review for Sena

**Request changes on the original draft.** The replacement is ready for review against the current profile import contract and capability policy. The existing CLI and capability decision code remain the entry points.

| Draft finding | Code evidence in original profiles.py | Contract check on the replacement |
|---|---|---|
| Name validation accepts a trailing newline | Lines 12, 20 use a dollar anchor and prefix matching | Name boundary test requires a full match for new names |
| Non-list values and nonstring elements can pass | Lines 23–24 deduplicate any iterable of hashable elements without enforcing the JSON schema | Schema test rejects wrong containers, element types, and missing fields |
| Unknown capabilities and banned grants can pass | Lines 23–30 never consult the catalog policy | Capability test requires exact membership and rejects banned grants, including overlaps |
| An existing profile can lose a saved deny | Lines 27–30 overwrite the saved profile without checking its prior deny set | Sticky-deny test rejects omitted denies and accepts additional ones |
| Allow wins in a conflict | Line 27 removes overlapping entries from deny | Conflict test preserves deny, removes the redundant grant, and verifies stable deduplication |
| A successful proposal mutates trusted memory | Lines 29–30 assign into the store's live profiles dictionary, which the capability action reads | Shared-store test confirms the capability decision is unchanged and response edits cannot change saved profiles. CLI test verifies fixture bytes are unchanged |

The PR's full-validation and kiosk-safety claims fail against the contract. The authentication claim is unsupported: the CLI dispatches JSON and models no caller identity. The public-test claim is accurate (17 baseline tests passed), but those tests did not exercise profile import. Separate CLI calls reload the fixture, so a fresh process alone would miss the in-memory mutation.

I used the current contract and revision 3 policy. Capability matching stays case-sensitive, including when input differs only by capitalization. Authentication, signatures, and approval or persistence workflows are outside this model.

Run the post-fix contract checks from the workspace:

```sh
python3 -B cli.py examples/profile-import.json
python3 -B -m unittest discover -s tests -v
```

All 24 tests passed, including seven new import tests. The review cites the original code and the checks verify the replacement's behavior.
