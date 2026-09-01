# TECHGUYTOOL-VIVO

Repair-first workspace for Vivo devices. Current target: Vivo 1727 / PD1730BF_EX in Qualcomm EDL mode.

## START HERE — session recovery

Any new chat/session continuing Device 001 must read these in order before touching the phone:

1. [`RECOVERY.md`](RECOVERY.md) — canonical cross-session plan, current boundary, exact continuation sequence, safety gates, local paths, and fresh-chat instruction.
2. [`evidence/PD1730BF_EX/CHECKPOINT.md`](evidence/PD1730BF_EX/CHECKPOINT.md) — detailed device evidence and loader/write-auth results.
3. [`tools/candidate_proof.py`](tools/candidate_proof.py) and [`tools/stage_loader.py`](tools/stage_loader.py) — guarded execution helpers.
4. `tests/` — proof-harness and loader-verification tests.

Do not reconstruct the repair state from an old conversation when the repository contains the evidence.

## Current priority

Recover the first device from bootloop safely. Full TECHGUYTOOL-VIVO product architecture comes after Device 001 is successfully recovered and the procedure is proven.

## Current boundary

- Device/firmware/read path: proven.
- Protected NV/calibration backups: complete and local-only.
- Stock and existing local V9 Youth programmer writes: blocked by Vivo authorization.
- Next candidate: exact-model `V9_YOUTH_PD1730BF.mbn`.
- Actual firmware writes remain blocked until a controlled same-data write proof succeeds.

See `RECOVERY.md` for the authoritative continuation procedure.

## Safety

Raw device NV/calibration backups and large firmware packages are local-only and must never be committed.
