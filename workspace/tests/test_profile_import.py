"""Regression checks for the corrected profile proposal boundary."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from extension_catalog import profiles, service, storage


class ProfileImportTests(unittest.TestCase):
    def setUp(self):
        self.store = storage.load()

    def proposal(self, **changes):
        return {"name": "new-profile", "allow": ["canvas.read"], "deny": [], **changes}

    def assert_rejected(self, proposal):
        before_store = deepcopy(self.store)
        before_proposal = deepcopy(proposal)
        result = profiles.import_profile(self.store, proposal)
        self.assertEqual(set(result), {"ok", "reason"})
        self.assertIs(result["ok"], False)
        self.assertTrue(result["reason"])
        self.assertEqual(self.store, before_store)
        self.assertEqual(proposal, before_proposal)

    def test_name_boundaries(self):
        for name in ("ab", "a" + "9" * 23, "a-9", "studio"):
            with self.subTest(name=name):
                self.assertTrue(profiles.import_profile(self.store, self.proposal(name=name))["ok"])
        for name in ("a", "a" * 25, "Ab", "-ab", "ab\n", 42):
            with self.subTest(name=name):
                self.assert_rejected(self.proposal(name=name))

    def test_object_and_list_schema(self):
        self.assert_rejected(None)
        self.assert_rejected([])
        for field in ("allow", "deny"):
            missing = self.proposal()
            del missing[field]
            self.assert_rejected(missing)
            for value in ("canvas.read", {"canvas.read": True}, [True], [1], [[]], None):
                with self.subTest(field=field, value=value):
                    self.assert_rejected(self.proposal(**{field: value}))

    def test_capabilities_are_exact_and_banned_grants_reject(self):
        self.assert_rejected(self.proposal(allow=["Canvas.Read"]))
        self.assert_rejected(self.proposal(deny=["unknown.cap"]))
        self.assert_rejected(self.proposal(allow=["clipboard.read"], deny=["clipboard.read"]))
        self.assertTrue(profiles.import_profile(self.store, self.proposal(deny=["clipboard.read"]))["ok"])

    def test_sticky_denies(self):
        self.assert_rejected(self.proposal(name="kiosk"))
        result = profiles.import_profile(
            self.store, self.proposal(name="kiosk", deny=["palette.write", "clipboard.read"])
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["profile"]["deny"], ["palette.write", "clipboard.read"])

    def test_deny_wins_and_duplicates_keep_order(self):
        result = profiles.import_profile(
            self.store,
            self.proposal(
                allow=["palette.write", "canvas.read", "palette.write"],
                deny=["canvas.read", "clipboard.read", "canvas.read"],
            ),
        )
        self.assertEqual(result["profile"], {
            "allow": ["palette.write"],
            "deny": ["canvas.read", "clipboard.read"],
        })

    def test_proposal_is_detached_and_capability_uses_saved_policy(self):
        query = {
            "action": "capability", "profile": "kiosk",
            "extension_id": "inkframe", "capability": "palette.write",
        }
        original = deepcopy(self.store)
        before = service.dispatch(query, self.store)
        proposal = self.proposal(name="kiosk", deny=["palette.write"])
        original_proposal = deepcopy(proposal)
        result = service.dispatch({"action": "profile-import", "profile": proposal}, self.store)
        self.assertTrue(result["ok"])
        self.assertEqual(result["mode"], "proposal-only")
        self.assertEqual(set(result["profiles"]), set(original["profiles"]))
        self.assertEqual(result["profiles"]["kiosk"], result["profile"])
        result["profile"]["deny"].clear()
        result["profiles"]["studio"]["allow"].clear()
        self.assertEqual(self.store, original)
        self.assertEqual(proposal, original_proposal)
        self.assertIs(before["ok"], False)
        self.assertEqual(service.dispatch(query, self.store), before)

    def test_cli_accepts_and_rejects_without_writing_fixture(self):
        fixture = Path("fixtures/store.json")
        before = fixture.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            request = Path(directory) / "proposal.json"
            for proposal, accepted in ((self.proposal(), True), (self.proposal(name="kiosk"), False)):
                request.write_text(json.dumps({"action": "profile-import", "profile": proposal}), encoding="utf-8")
                run = subprocess.run(
                    [sys.executable, "-B", "cli.py", str(request)],
                    capture_output=True, text=True, check=True,
                )
                self.assertIs(json.loads(run.stdout)["ok"], accepted)
        self.assertEqual(fixture.read_bytes(), before)
