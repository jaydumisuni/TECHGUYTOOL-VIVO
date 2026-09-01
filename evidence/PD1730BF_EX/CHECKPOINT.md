# Device 001 — Vivo 1727 / PD1730BF_EX

## Repair objective
Recover this handset from bootloop using TECHGUYTOOL-VIVO / inspectable open-source Qualcomm tooling. Commercial servicing applications are **not** part of the execution path.

## LIVE CORRECTION — 2026-09-02

This section supersedes any older instruction that treats `reset_to_edl` as a safe generic way to obtain fresh Sahara on this handset.

- Windows can show `Qualcomm HS-USB QDLoader 9008` while an already-uploaded Firehose programmer is still active; **9008 enumeration alone does not prove fresh Sahara**.
- On 2026-09-02, `edl.py` positively detected the handset as `Mode detected: firehose` on COM10.
- The command path then sent the previously saved QFIL-style XML `<power value="reset_to_edl" />`.
- Firehose acknowledged the XML command, but the handset re-enumerated as Vivo USB mass storage `VID_2D95&PID_6008`, **not** Qualcomm `VID_05C6&PID_9008` fresh Sahara.
- Therefore **do not use `reset_to_edl` / `ResetToEDL.xml` as the transition between programmer candidates on Device 001**.
- The user physically returned the handset to Qualcomm HS-USB QDLoader 9008 on COM10 immediately afterward. No partition program, erase, or firmware write occurred during the bad transition.
- Before any candidate programmer test, require both:
  1. Windows shows `VID_05C6&PID_9008` / Qualcomm HS-USB QDLoader 9008, and
  2. the first EDL interaction proves Sahara and uploads the intended candidate; do not infer Sahara from Device Manager alone.
- If a candidate test leaves an active Firehose session, stop at that boundary. Obtain fresh hardware EDL/9008 using the proven physical entry method before testing another programmer; do not send `reset_to_edl` again.

## Proven identity
- Brand: Vivo
- Model: 1727
- Product: PD1730BF_EX / V9 Youth
- Platform family: Qualcomm 8953-class Firehose target
- USB mode: Qualcomm HS-USB QDLoader 9008
- Last live port: COM10
- Hardware ID: `0009A0E1`
- Vivo/OEM PK hash: `60BA997FEF6DA9F05885FA11F1DD6D2A90D052A257A09C2075D7246CC73C0D43`
- Storage: eMMC `RH64AB`, 64 GB class
- GPT read: PASS

## Firmware
- Package: `PD1730BF_EX_A_1.12.3` Android 8.1 branch
- Package manifest: 97/97 MD5 entries verified
- Complete TAR extracted locally under `firmware/PD1730BF_EX_A_1.12.3/` (firmware is git-ignored)
- Stock programmer accepts Sahara/Firehose read path
- Direct stock-programmer write attempt: REJECTED by target authorization (`ret_auth=0 / Unauthorized`) before a successful partition program was reported

## Dedicated local V9 Youth loader — PROVEN READ, WRITE AUTH BLOCKED
`D:\###\techguytool\Qualcomm-Tool-master\assets\devices\loaders\vivo\prog_firehose_8953_ddr_vivo_v9_youth.mbn`

- Size: 401620 bytes
- SHA-256: `F944E16659B9A4C7A67C6B5806B13DF1491057B83645C664A7BA1192BCD45FCA`
- Explicit local device mapping: `VIVO V9 Yth (PD1730BF)`
- Uploaded successfully from fresh Sahara after QFIL-compatible `reset_to_edl`
- Firehose booted with `TargetName=8953`
- Full GPT read succeeded
- Controlled same-data `boot` write was rejected with `ret_auth=0 / Unauthorized`

> Historical note: the sentence above records the older experiment as originally observed. The 2026-09-02 live correction proves that `reset_to_edl` must **not** be used as the generic transition for future candidate tests.

## Exact HWID + PK-hash Vivo loader — DISCOVERED, NOT YET DEVICE-TESTED
`D:\###\techguytool\Qualcomm-Tool-master\assets\devices\loaders\auto\vivo\0009a0e100000000_60ba997fef6da9f0_fhprg_peek.bin`

This filename matches the handset's exact HWID and Vivo PK-hash prefix.

- Size: 363460 bytes
- SHA-256: `E66632E006586B9CA9636379BBFFF5E22E2345B4F7A6A8E7A0113FEA25D2493B`
- Same loader identity is present in the public bkerler Vivo loader collection
- `_peek` denotes extra Firehose memory peek/poke capability; it is **not** assumed to bypass write authorization
- Next test must start from fresh Sahara and use a controlled same-data write proof

## Public PD1730BF candidate programmers — STAGED FOR TEST ORDER
Public loader indexes and repositories expose multiple distinct Vivo 8953 programmers. They must be treated as independent candidates, not equivalent by filename.

### Candidate 1 — exact PD1730BF
Repository: `Iqinix/Qualcomm-firehoses`

`Vivo/V9_YOUTH_PD1730BF.mbn`

- Git blob SHA: `6c1ae1dd5894d5f082f4c1c8dcd5c9194104e10f`
- Size: 387361 bytes
- Staged on ATHENA on 2026-09-02
- SHA-256: `61D3F76C2CE04467A6672D50C4AE7AA0B528FE71FC5DE09B9BEB7CF0BBA4DF11`
- Historical servicing packages also contain an exact `V9_YOUTH_PD1730BF.mbn` path
- This was the highest-priority untested programmer before the 2026-09-02 live test because it is exact-model-specific and structurally distinct from the already-failing local V9 Youth loader

### Candidate 1 live result - 2026-09-02

- COM port: `COM10` / Qualcomm HS-USB QDLoader 9008.
- Fresh protocol proof: `INITIAL_MODE=sahara` PASS.
- Repo transport guard: pyserial timeout bounded to `5.0` seconds; focused tests and full suite pass.
- Candidate SHA-256 reverified: `61D3F76C2CE04467A6672D50C4AE7AA0B528FE71FC5DE09B9BEB7CF0BBA4DF11`.
- Upload result: `Error: Protocol mismatch between host and target`.
- Firehose: **NOT REACHED**.
- GPT/storage/boot read gates: **NOT RUN** because Firehose did not pass.
- Same-data write proof: **NOT RUN**.
- Device-content change from this attempt: **NONE**; failure occurred in Sahara before partition access.
- Candidate 1 classification: **REJECTED BEFORE FIREHOSE**.

### Candidate 2 — V9 Youth generic ELF
Repository: `Iqinix/Qualcomm-firehoses`

`Vivo/V9_YOUTH.elf`

- Git blob SHA: `8fa768e4abb08defd77e1e73879c68a78b3eed3a`
- Size: 406200 bytes
- Public loader index places it in a different content-fingerprint group from the exact-HWID `_peek` loader

### Candidate 3 — exact-HWID `_peek`
Use the local `0009a0e1...60ba997f...fhprg_peek.bin` described above.

No candidate is considered write-capable until it passes the controlled proof below.

## Open-source execution substrate
Local source:
`D:\projects\my tool\for use\Android\edl-master`

Isolated environment:
`D:\projects\TECHGUY TOOL VIVO\.venv`

Required Python dependencies were installed successfully. `edl.py -h` runs and exposes Sahara/Firehose operations including `printgpt`, reads, writes, `peek/poke`, raw XML, reset-to-EDL and QFIL XML processing.

Future device execution should use this source / our wrapper, not a commercial servicing GUI.

## Protected backups — LOCAL ONLY
Backups live under `evidence/PD1730BF_EX/backup/` and are git-ignored.

| Partition | Bytes | SHA-256 |
|---|---:|---|
| modemst1 | 2621440 | E3736FBFEADFDD7AEB04C25B070A47D771200DDDFA86B2383969952FB6379A91 |
| modemst2 | 2621440 | 265004136C2404BB9A3429D3700FA8B838909993936893FEE178260AD3A9C44C |
| fsg | 2621440 | 667C42E6B53820FB5A85EEA573559D0AF1D80AE5082B43289DBEB4F2664FC85E |
| persist | 33554432 | 573CE76C1B8A1DBA3C7EF49834FC79E2028998D23DA7B1152F3B22DB9A326F60 |

A full 64 MiB `boot` backup was also taken locally before write testing.

## Controlled write-capability proof baseline
1. Read current `boot` partition.
2. Baseline SHA-256: `14269D687B944965107E527A6E1AFEE8F24FB6D30EF17E1492530A36D1CDAAB0`.
3. Write that exact same 64 MiB dump back to `boot`.
4. Require target ACK with no `ret_auth=0` / Unauthorized result.
5. Re-read `boot`.
6. Require post-read SHA-256 to equal the baseline.

The already-tested local V9 Youth loader failed step 4; post-read hash still matched, proving no device-content change.

## Deterministic next live-device sequence
When ATHENA/Oracle device control is available:
1. Detect current COM port and verify `VID_05C6&PID_9008`.
2. Do **not** use `reset_to_edl` / `ResetToEDL.xml` to create the candidate boundary.
3. Candidate 1 is closed as rejected before Firehose (`Protocol mismatch between host and target`); do not repeat it without new evidence.
4. Physically establish fresh 9008/Sahara before Candidate 2.
5. Stage/verify Candidate 2 and run its read-only proof first.
6. Only if Candidate 2 reaches Firehose: run GPT/storage-info reads.
7. Read `boot` and confirm the baseline hash.
8. Execute the same-data boot write proof only after every read gate passes.
9. Re-read and compare SHA; if Candidate 2 fails, physically restore fresh 9008 before Candidate 3.
10. Only after a candidate proves safe write authority should actual boot-recovery firmware writes begin.

If all signed candidates still enforce Vivo auth, the exact-HWID `_peek` loader becomes the controlled research path for locating the Firehose auth decision in memory; no blind RAM patching is approved.

## Current boundary
- Device transport: PROVEN
- Firmware integrity: PROVEN
- Protected device backups: COMPLETE
- GPT/read access: PROVEN
- Local V9 Youth loader write authority: BLOCKED BY VIVO AUTH
- Exact-HWID `_peek` loader: DISCOVERED / UNTESTED
- Exact PD1730BF public Candidate 1: TESTED FROM FRESH SAHARA / REJECTED BEFORE FIREHOSE (protocol mismatch)
- Evidence of partial write from current attempts: NONE
- `reset_to_edl` as a candidate-transition method: **REJECTED for Device 001**
- Last confirmed live USB state after the bounded Candidate 1 run: Qualcomm HS-USB QDLoader 9008 (COM10)
- Candidate 1 bounded rerun completed: fresh Sahara PASS; loader rejected with `Protocol mismatch between host and target`; Firehose not reached
- Next destructive action: **none until same-data write proof succeeds**
