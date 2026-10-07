# BBEH500 accepted_B patch report

Status: PATCHED_OFFLINE_VERIFIED

Root cause:
- `word_sorting_key_engine` treated all numbered trace groups as first-letter groups.
- In subpart sorting thoughts, group numbers can refer to second/third/etc. letters.
- The accepted_B row `bbeh_full_word_sorting_0132_4195006c6a` had a valid second-letter group `(1) "paddy"`, but the executor compared `paddy` against first-letter `p=16` and incorrectly answered `4`.

Fix:
- Track active letter position from thought text (`first/second/third/... letters`).
- Validate numbered groups against that active letter position.
- When a thought contains a subpart prefix followed by `Hence`, validate only the subpart clause before `Hence` to avoid mixing subpart group numbers with the full ordering restatement.

Regression test:
- Added `test_word_sorting_executor_does_not_flag_valid_subpart_letter_groups_as_first_letter_mistakes`.

Offline replay against existing BBEH500 locked base answers:
- Base: 91/500
- Patched REVAS final: 268/500
- accepted_C: 177
- accepted_B: 0
- override accepted: 222

Claim boundary:
- This is a post-run patch/offline replay artifact, not a fresh API rerun.
- It proves the accepted_B mechanism is fixed on the locked BBEH500 outputs without additional API calls.
