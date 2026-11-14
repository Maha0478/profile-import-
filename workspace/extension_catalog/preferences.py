"""Pure recursive preference merge with trusted policy locks applied last."""
from __future__ import annotations

import copy

from extension_catalog import models


def _merge_overrides(defaults: models.JsonObject, overrides: models.JsonObject, prefix: str = "") -> models.JsonObject:
    result = copy.deepcopy(defaults)
    for key, value in overrides.items():
        location = f"{prefix}{key}"
        if key not in defaults:
            raise ValueError(f"unknown preference: {location}")
        baseline = defaults[key]
        if type(value) is not type(baseline):
            raise ValueError(f"incompatible preference type: {location}")
        if isinstance(value, dict) is True:
            result[key] = _merge_overrides(baseline, value, f"{location}.")
        else:
            result[key] = copy.deepcopy(value)
    return result


def _apply_locks(preferences: models.JsonObject, locked: models.JsonObject) -> None:
    for key, value in locked.items():
        if isinstance(value, dict) is True:
            _apply_locks(preferences[key], value)
        else:
            preferences[key] = copy.deepcopy(value)


def merge(defaults: models.JsonObject, overrides: models.JsonObject, locked: models.JsonObject) -> models.JsonObject:
    """Reject unknown keys/types while preserving false, zero and independent lists."""
    if isinstance(overrides, dict) is False:
        return {"ok": False, "reason": "overrides must be an object"}
    try:
        result = _merge_overrides(defaults, overrides)
    except ValueError as error:
        return {"ok": False, "reason": str(error)}
    _apply_locks(result, locked)
    return {"ok": True, "preferences": result}
