# Choices

I limited the patch to the importer. The existing dispatcher already passes the proposal and trusted store through the correct interface. I validate types and exact capability membership before constructing the preview. Saved denies are a minimum for any replacement, and I remove overlapping grants while preserving the explicit denies. I copy the saved profiles so the preview can include every profile without aliasing the trusted store.

I followed the current contract and capability policy. I deferred authentication, signatures, persistence and changes to unrelated actions. I also left capability spelling exact as specified by the contract.

The AI-drafted code kept the allow entry when a capability appeared in both lists. I rejected that choice because both current documents say an explicit deny wins. The overlap regression test checks the corrected result and its ordering.

Setup and all 17 original tests passed before the patch. Afterward, all 24 tests passed. New checks cover name and schema boundaries, exact and banned capabilities, sticky denies, overlap, stable deduplication, and the CLI accept/reject shape. I checked capability behavior using the same store object before and after a proposal, since separate CLI runs reload the fixture and can hide an in-memory side effect. I also compared fixture bytes before and after the CLI runs.

# to verify that all tests are OK
first : `cd workspace && py -3 -B setup.py`
then : `py -3 -B -m unittest discover -s tests -v`
for the specific 7 test : `py -3 -B -m unittest discover -s tests -p "test_profile_import.py" -v`
