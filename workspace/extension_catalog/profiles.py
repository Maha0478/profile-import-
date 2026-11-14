"""Validate a profile proposal against saved policy without changing the store."""
from __future__ import annotations

from copy import deepcopy
import re

from extension_catalog import models

NAME = re.compile(r"[a-z][a-z0-9-]{1,23}")


def import_profile(store: models.JsonObject, proposal: object) -> models.JsonObject:
    if not isinstance(proposal, dict):
        return {"ok": False, "reason": "profile must be an object"}

    saved_profiles = store["profiles"]
    name = proposal.get("name")
    if not isinstance(name, str) or (
        name not in saved_profiles and NAME.fullmatch(name) is None
    ):
        return {"ok": False, "reason": "invalid profile name"}

    allow = proposal.get("allow")
    deny = proposal.get("deny")
    for field, values in (("allow", allow), ("deny", deny)):
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            return {"ok": False, "reason": f"{field} must be a list of strings"}

    policy = store["catalog_policy"]
    known = set(policy["known_capabilities"])
    if any(capability not in known for capability in allow + deny):
        return {"ok": False, "reason": "unknown capability"}
    if set(allow).intersection(policy["banned_capabilities"]):
        return {"ok": False, "reason": "banned capability in allow"}

    denied = set(deny)
    if not denied.issuperset(saved_profiles.get(name, {}).get("deny", [])):
        return {"ok": False, "reason": "saved denies must be preserved"}

    profile = {
        "allow": list(dict.fromkeys(cap for cap in allow if cap not in denied)),
        "deny": list(dict.fromkeys(deny)),
    }
    proposed_profiles = deepcopy(saved_profiles)
    proposed_profiles[name] = profile
    return {
        "ok": True,
        "mode": "proposal-only",
        "name": name,
        "profile": profile,
        "profiles": proposed_profiles,
    }
