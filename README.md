# TECHGUYTOOL-VIVO

Repair-first workspace for Vivo devices. Current target: Vivo 1727 / PD1730BF_EX in Qualcomm EDL mode.

## START HERE — session recovery

Any new chat/session continuing Device 001 must read these in order before touching the phone:

1. [`evidence/PD1730BF_EX/CHECKPOINT.md`](evidence/PD1730BF_EX/CHECKPOINT.md) — **live device boundary and corrections first**. The 2026-09-02 correction supersedes the older assumption that `reset_to_edl` is a safe generic transition between programmers.
2. [`RECOVERY.md`](RECOVERY.md) — canonical cross-session plan, current boundary, continuation sequence, safety gates, and local paths. Where it conflicts with the live correction in `CHECKPOINT.md`, the checkpoint wins until `RECOVERY.md` is reconciled.
3. [`tools/candidate_proof.py`](tools/candidate_proof.py) and [`tools/stage_loader.py`](tools/stage_loader.py) — guarded execution helpers.
4. `tests/` — proof-harness and loader-verification tests.

Do not reconstruct the repair state from an old conversation when the repository contains the evidence.

## Current priority

Recover the first device from bootloop safely. Full TECHGUYTOOL-VIVO product architecture comes after Device 001 is successfully recovered and the procedure is proven.

## Current boundary

- Device/firmware/read path: proven.
- Protected NV/calibration backups: complete and local-only.
- Stock and existing local V9 Youth programmer writes: blocked by Vivo authorization.
- Candidate 1 exact-model `V9_YOUTH_PD1730BF.mbn`: staged and pinned; live read-only proof still requires confirmation.
- `reset_to_edl` / `ResetToEDL.xml`: **do not use as a programmer-transition method on Device 001**. A live 2026-09-02 attempt moved the handset to Vivo `VID_2D95&PID_6008` mass-storage mode instead of fresh Qualcomm 9008/Sahara.
- Actual firmware writes remain blocked until a controlled same-data write proof succeeds.

See `evidence/PD1730BF_EX/CHECKPOINT.md` for the authoritative live continuation boundary.

## Safety

Raw device NV/calibration backups and large firmware packages are local-only and must never be committed.
