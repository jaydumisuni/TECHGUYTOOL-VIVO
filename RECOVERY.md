# TECHGUYTOOL-VIVO — Canonical Recovery Handoff

Last consolidated: 2026-09-02

This file is the **first document a new chat/session must read** before doing any Vivo work.

The repository is the source of truth. Do not reconstruct state from memory or from an older chat when the repo contains evidence.

---

## 1. Mission

Current priority is **not** to build the full TECHGUYTOOL-VIVO product.

Current priority is to recover the first handset safely:

- Vivo 1727
- Product: `PD1730BF_EX`
- Family: Vivo V9 Youth
- Qualcomm MSM8953-class EDL/Firehose target
- Symptom: bootloop

Once this handset is recovered and the procedure is proven, the successful flow can become the first TECHGUYTOOL-VIVO device profile/workflow.

Commercial servicing GUIs are not part of the execution path. Use inspectable/open-source tooling and our own wrappers/harnesses.

---

## 2. Session-start protocol for a new chat

A new session must do these steps **before changing the phone**:

1. Read this `RECOVERY.md` completely.
2. Read `evidence/PD1730BF_EX/CHECKPOINT.md` completely.
3. Inspect `tools/candidate_proof.py` and `tools/stage_loader.py`.
4. Inspect the tests under `tests/`.
5. Use Oracle Live directly on ATHENA when available.
6. Recover the current workstation/device state instead of assuming COM10 is still correct.
7. Verify the local repository/worktree and required local paths before executing anything.
8. Continue from the **Current live boundary** in this document. Do not restart already-proven experiments.

When Oracle is available, the user should not be asked to manually execute terminal commands that Oracle can execute directly.

If Oracle disconnects, preserve progress in this repository before ending the session.

---

## 3. Repository and local paths

GitHub repository:

`jaydumisuni/TECHGUYTOOL-VIVO`

Primary local project path:

`D:\projects\TECHGUY TOOL VIVO`

Open-source Qualcomm EDL source already available locally:

`D:\projects\my tool\for use\Android\edl-master`

Isolated Python environment:

`D:\projects\TECHGUY TOOL VIVO\.venv`

Additional Android/tool arsenal available for evidence/reuse:

`D:\projects\my tool\for use\Android`

`D:\###\techguytool`

Do not copy large firmware, device dumps, QCN, NV, or calibration data into Git. `.gitignore` intentionally blocks these artifacts.

---

## 4. Proven handset identity

The following is already proven and should not be re-guessed:

- Brand: Vivo
- Model: `1727`
- Product: `PD1730BF_EX / V9 Youth`
- Qualcomm family: MSM8953-class
- EDL USB identity: Qualcomm HS-USB QDLoader 9008
- Last proven COM port: `COM10`
- Hardware ID: `0009A0E1`
- Vivo/OEM PK hash: `60BA997FEF6DA9F05885FA11F1DD6D2A90D052A257A09C2075D7246CC73C0D43`
- eMMC: `RH64AB`, 64 GB class
- GPT read: PASS
- Sahara -> Firehose transport: PASS with compatible programmers

`COM10` is historical evidence only. Rediscover the active port every new live session.

---

## 5. Verified firmware

Firmware package:

`PD1730BF_EX_A_1.12.3`

Branch:

Android 8.1-era stock package for this product.

Integrity status:

- Package manifest verified: `97/97` MD5 entries PASS.
- Complete firmware was extracted locally under:

  `firmware/PD1730BF_EX_A_1.12.3/`

- `firmware/` is intentionally git-ignored.

Do not redownload or substitute firmware unless new evidence proves this package is wrong or incomplete.

---

## 6. Protected backups already completed

Protected device data is backed up locally under:

`evidence/PD1730BF_EX/backup/`

That directory is git-ignored and must remain local-only.

Verified backup hashes:

| Partition | Bytes | SHA-256 |
|---|---:|---|
| `modemst1` | 2621440 | `E3736FBFEADFDD7AEB04C25B070A47D771200DDDFA86B2383969952FB6379A91` |
| `modemst2` | 2621440 | `265004136C2404BB9A3429D3700FA8B838909993936893FEE178260AD3A9C44C` |
| `fsg` | 2621440 | `667C42E6B53820FB5A85EEA573559D0AF1D80AE5082B43289DBEB4F2664FC85E` |
| `persist` | 33554432 | `573CE76C1B8A1DBA3C7EF49834FC79E2028998D23DA7B1152F3B22DB9A326F60` |

A full 64 MiB `boot` backup was also taken before write testing.

Known boot baseline SHA-256:

`14269D687B944965107E527A6E1AFEE8F24FB6D30EF17E1492530A36D1CDAAB0`

Never erase or overwrite QCN/NV/calibration partitions as part of normal bootloop recovery.

---

## 7. What has already failed — do not repeat blindly

### 7.1 Stock firmware programmer

The stock programmer successfully reached Firehose/read operations, but a direct partition program request was rejected by Vivo authorization:

`ret_auth=0 / Unauthorized`

No successful partition program was reported.

Conclusion: stock programmer compatibility is not the problem; Vivo write authorization is the blocker.

### 7.2 Existing local dedicated V9 Youth loader

Local loader:

`D:\###\techguytool\Qualcomm-Tool-master\assets\devices\loaders\vivo\prog_firehose_8953_ddr_vivo_v9_youth.mbn`

Evidence:

- Size: `401620` bytes
- SHA-256: `F944E16659B9A4C7A67C6B5806B13DF1491057B83645C664A7BA1192BCD45FCA`
- Explicit mapping: `VIVO V9 Yth (PD1730BF)`
- Fresh Sahara upload: PASS
- Firehose `TargetName=8953`: PASS
- GPT read: PASS
- Controlled same-data `boot` write: REJECTED
- Error: `ret_auth=0 / Unauthorized`
- Post-failure boot re-read matched the original baseline hash

Conclusion: this loader is compatible for reads but does not remove Vivo write authorization.

Do not spend another session proving the same fact unless needed as a control experiment.

---

## 8. Untested loader candidates — exact order

No candidate is considered write-capable until it passes the controlled same-data write proof.

### Candidate 1 — highest priority

Public repository:

`Iqinix/Qualcomm-firehoses`

Path:

`Vivo/V9_YOUTH_PD1730BF.mbn`

Pinned identity:

- Size: `387361` bytes
- Git blob SHA-1: `6c1ae1dd5894d5f082f4c1c8dcd5c9194104e10f`

Reason for priority: exact `PD1730BF` model naming and binary identity distinct from the already-failing local V9 Youth programmer.

Stage it only through `tools/stage_loader.py`, which verifies the pinned Git object before writing the local file.

### Candidate 2

Public repository:

`Iqinix/Qualcomm-firehoses`

Path:

`Vivo/V9_YOUTH.elf`

Pinned identity:

- Size: `406200` bytes
- Git blob SHA-1: `8fa768e4abb08defd77e1e73879c68a78b3eed3a`

Use only if Candidate 1 fails the controlled proof.

### Candidate 3 — exact HWID/PK-hash loader

Local path:

`D:\###\techguytool\Qualcomm-Tool-master\assets\devices\loaders\auto\vivo\0009a0e100000000_60ba997fef6da9f0_fhprg_peek.bin`

Evidence:

- Filename matches exact handset HWID and Vivo PK-hash prefix
- Size: `363460` bytes
- SHA-256: `E66632E006586B9CA9636379BBFFF5E22E2345B4F7A6A8E7A0113FEA25D2493B`
- Same loader identity is present in the public bkerler Vivo loader collection
- `_peek` means memory peek/poke capability; it is **not** evidence of an authorization bypass

Use only after Candidates 1 and 2 unless new static evidence changes the order.

---

## 9. Repo tooling already prepared

### `tools/stage_loader.py`

Purpose:

- Downloads only pinned public Vivo programmer candidates.
- Verifies exact byte size.
- Computes Git blob SHA-1 using Git object format.
- Refuses mismatched content.
- Prints final SHA-256 for local evidence.

Current supported names:

- `v9-youth-pd1730bf`
- `v9-youth-elf`

Example staging pattern:

```powershell
& "D:\projects\TECHGUY TOOL VIVO\.venv\Scripts\python.exe" `
  "D:\projects\TECHGUY TOOL VIVO\tools\stage_loader.py" `
  v9-youth-pd1730bf `
  --outdir "D:\projects\TECHGUY TOOL VIVO\loaders"
```

### `tools/candidate_proof.py`

Purpose:

1. `printgpt`
2. `getstorageinfo`
3. read `boot`
4. require the exact known boot baseline hash
5. stop in read-only mode unless explicitly authorized with `--same-data-write-proof`
6. if enabled, write the exact bytes just read back to `boot`
7. re-read `boot`
8. require identical before/after hashes

This harness is specifically designed to prevent a candidate-loader test from becoming an accidental firmware flash.

The harness uses:

- explicit loader path
- explicit serial COM path
- `--memory=emmc`
- local `edl.py`
- known boot baseline guard

Tests exist under:

- `tests/test_candidate_proof.py`
- `tests/test_stage_loader.py`

At the start of a new engineering session, run the tests again before using changed harness code. Tests confirm implementation behavior; they do not replace recovering the device evidence above.

---

## 10. Exact next live-device procedure

This is the active continuation point.

### Phase A — recover live state

1. Connect to ATHENA through Oracle Live.
2. Confirm ATHENA identity and that the local project exists.
3. Recover repository state (`git status`, branch/head, latest commits) before editing.
4. Confirm the following local assets still exist:
   - `.venv`
   - `edl-master`
   - verified firmware directory
   - local protected backups
   - local exact-HWID `_peek` loader
5. Detect the handset's current Qualcomm COM port. Do not assume COM10.
6. Determine whether the device is currently in Sahara or an already-running Firehose session.
7. Inspect the locally installed `edl.py -h` / source before issuing reset syntax. Do not invent command syntax from memory.

### Phase B — force a clean programmer test boundary

If the handset is already running a previous Firehose programmer:

1. use the locally verified QFIL-compatible reset-to-EDL method;
2. prove the device returned to fresh Sahara;
3. rediscover the COM port if Windows re-enumerated it.

Every candidate loader test starts from fresh Sahara. Do not swap programmers inside an old Firehose session and call that a valid compatibility result.

### Phase C — Candidate 1 read-only proof

1. Stage `v9-youth-pd1730bf` using `tools/stage_loader.py`.
2. Record its printed byte count, Git blob SHA-1, and SHA-256.
3. Load it from fresh Sahara using our local `edl-master`/wrapper.
4. Run the candidate proof harness **without** `--same-data-write-proof` first.
5. Require:
   - programmer upload PASS
   - Firehose starts
   - GPT read PASS
   - storage-info PASS
   - boot read PASS
   - boot SHA-256 equals `14269D...DAAB0`
6. If any read gate fails, stop. Do not attempt a write.

### Phase D — Candidate 1 controlled write-authority proof

Only after all Phase C gates pass:

1. run the same harness with `--same-data-write-proof`;
2. the only permitted write is the exact `boot` dump just read from the handset;
3. require target ACK and no `ret_auth=0 / Unauthorized`;
4. re-read `boot`;
5. require the post-read hash to equal the original baseline exactly.

Outcome classification:

- `SAME_DATA_WRITE_PROOF=PASS` -> write authority is proven for Candidate 1.
- `ret_auth=0 / Unauthorized` -> Candidate 1 is compatible but authorization-blocked; move to Candidate 2.
- any transport/program error without proven unchanged post-read -> stop and diagnose before another write.
- ACK followed by hash mismatch -> stop immediately; do not continue flashing.

### Phase E — remaining candidates

If Candidate 1 is authorization-blocked:

1. reset to fresh Sahara;
2. repeat the exact read-only and same-data proof with Candidate 2;
3. if Candidate 2 is also authorization-blocked, reset again and test Candidate 3;
4. never infer write capability merely because GPT/read works.

---

## 11. If a candidate proves write authority

Do **not** immediately issue an indiscriminate full-flash/erase-all operation.

The next sequence is:

1. Freeze the successful programmer identity and evidence in this repo.
2. Reconfirm protected backups are readable and hashes still match.
3. Inspect the verified firmware's rawprogram/patch XML and partition-image mapping against the phone's live GPT.
4. Separate repairable system/boot partitions from identity/NV/calibration partitions.
5. Explicitly exclude protected identity/calibration partitions from the recovery write set unless there is specific evidence they are corrupt and a restoration plan exists.
6. Choose the smallest stock write set reasonably capable of fixing the bootloop.
7. Record the exact planned partition list in the checkpoint **before** executing it.
8. Flash only verified stock images from `PD1730BF_EX_A_1.12.3`.
9. Verify every programmer response; stop on first NAK/auth/hash/transport anomaly.
10. Reset/reboot only after the programmed set finishes cleanly.
11. Observe first boot and collect evidence.
12. If it still bootloops, diagnose from the new boundary rather than immediately repeating/full-erasing.

If evidence later shows a complete stock restore is necessary, perform it using firmware-defined XML while explicitly preserving NV/QCN/calibration partitions.

---

## 12. If all three candidates remain authorization-blocked

Do not fall back to EFT or another opaque commercial servicing application merely because the signed candidates reject writes.

The research path becomes the exact-HWID `_peek` programmer because it provides memory peek/poke primitives.

Required research discipline:

1. confirm fresh-Sahara upload and read behavior first;
2. recover the exact Firehose binary/ELF layout;
3. statically locate Vivo's write-authentication decision or handler;
4. correlate static findings with safe memory reads;
5. identify a minimal, reversible RAM-only modification if one is technically justified;
6. do **not** perform blind poke/patch attempts;
7. after any RAM-only auth experiment, repeat the same-data `boot` proof before any firmware write;
8. document offsets, original bytes, replacement bytes, loader hash, and outcome in the repo.

No persistent device modification is approved merely to investigate the auth branch.

---

## 13. Failure interpretation guide

Use evidence to classify failure before changing approach.

### Sahara upload fails

Likely classes:

- incompatible programmer/signature
- wrong current device mode
- COM re-enumeration
- USB/driver/transport issue

This is not evidence about Firehose write authorization.

### Firehose starts and reads work, but `<program>` returns Unauthorized

This is the already-observed Vivo write-auth boundary.

Do not troubleshoot GPT, firmware integrity, or USB as though they were the primary blocker unless new evidence points there.

### Read-only proof produces a different boot hash

Stop before all writes.

The device state has changed since the baseline or the read is unreliable. Recover why before continuing.

### Program reports success but post-read hash differs

Stop immediately. Treat the device state as changed and investigate. Do not continue into firmware programming.

---

## 14. Explicit safety rules

Until the phone is recovered:

- no `erase all`;
- no blind raw XML execution;
- no QCN/NV wipe;
- no `modemst1`, `modemst2`, `fsg`, `persist` overwrite without specific proven need;
- no assumption that a loader filename means compatibility or bypass capability;
- no actual firmware write until a same-data write proof succeeds;
- no loader test without fresh Sahara when changing programmer;
- no commercial tool dependency in the final TECHGUYTOOL-VIVO solution;
- no publishing local protected dumps or customer/device calibration data;
- no replacing verified firmware because another package merely looks newer;
- no repeating a known-failed experiment without a reason that changes one controlled variable.

---

## 15. Documentation discipline during continuation

After every material live-device result, update:

`evidence/PD1730BF_EX/CHECKPOINT.md`

Update this `RECOVERY.md` whenever the global continuation boundary changes.

Each important result should record:

- date/session
- exact programmer filename and hashes
- fresh Sahara confirmation
- COM port used
- operation attempted
- exact ACK/NAK/auth result
- pre/post partition hashes when applicable
- whether device content changed
- next approved action

Firmware and raw dumps stay local; only hashes/metadata/evidence go to Git.

---

## 16. Product direction after Device 001 is recovered

Do not expand scope before the repair is proven.

After successful recovery:

1. Freeze the exact successful Vivo 1727/PD1730BF flow.
2. Convert it into the first TECHGUYTOOL-VIVO device profile.
3. Preserve the engineering sequence:
   - identify device
   - verify firmware
   - protect NV/calibration
   - select/verify loader
   - prove read access
   - prove write authority safely
   - execute repair
   - verify result
4. Generalize only the portions that are truly reusable across Vivo/Qualcomm devices.
5. Keep model-specific auth/loader behavior in device profiles rather than assuming one global Qualcomm rule.
6. Build the larger TECHGUYTOOL-VIVO application only after the repair path has real device evidence.

---

## 16A. Candidate 1 bounded Sahara result - 2026-09-02

Candidate 1 `V9_YOUTH_PD1730BF.mbn` was rerun from the physically established Qualcomm 9008 state on COM10 using the repo-owned direct Sahara uploader.

- Pinned SHA-256: `61D3F76C2CE04467A6672D50C4AE7AA0B528FE71FC5DE09B9BEB7CF0BBA4DF11`.
- The Windows serial transport now uses a bounded `5.0` second pyserial timeout instead of inheriting the legacy `1500` value as seconds.
- Initial protocol proof: `INITIAL_MODE=sahara` PASS.
- Programmer upload started.
- Sahara returned: `Error: Protocol mismatch between host and target`.
- Direct uploader result: `explicit loader did not reach firehose, got 'error'`.
- Firehose was **not** reached.
- Therefore GPT, storage-info, boot reads, and the same-data write proof were **not** executed with Candidate 1.
- No partition program, erase, reset, or firmware write occurred in this bounded test.

Candidate 1 is now classified as **rejected before Firehose / incompatible at the Sahara transfer handshake** for the observed Device 001 state. Do not repeat it without a controlled reason that changes the hypothesis.

## 17. Current live boundary

As of this handoff:

- Device identity: PROVEN
- Firmware package/integrity: PROVEN
- Sahara/Firehose transport: PROVEN
- GPT/read access: PROVEN
- Protected backups: COMPLETE
- Stock programmer write: BLOCKED BY VIVO AUTH
- Existing local V9 Youth programmer write: BLOCKED BY VIVO AUTH
- Candidate 1 `V9_YOUTH_PD1730BF.mbn`: TESTED FROM FRESH SAHARA / REJECTED BEFORE FIREHOSE (`Protocol mismatch between host and target`)
- Candidate 2 `V9_YOUTH.elf`: UNTESTED ON DEVICE
- Candidate 3 exact-HWID `_peek`: UNTESTED ON DEVICE
- Evidence of partial firmware write from current work: NONE
- Approved next device action: physically establish fresh 9008/Sahara, then Candidate 2 read-only proof; no write unless all read gates for that candidate pass

**There is no approved actual firmware write yet.**

---

## 18. Suggested fresh-chat instruction

A minimal new-chat message can be:

> Resume the Vivo 1727 / PD1730BF_EX recovery from `jaydumisuni/TECHGUYTOOL-VIVO`. Treat `RECOVERY.md` and `evidence/PD1730BF_EX/CHECKPOINT.md` as authoritative. Recover the current repo and ATHENA/device state through Oracle Live first, then continue from the documented current boundary. Do not repeat known-failed loaders, do not use commercial servicing tools, and do not perform an actual firmware write until the controlled same-data write proof succeeds. Proceed directly and keep the repo checkpoint updated.

That is sufficient. The new chat should recover the details from the repository rather than relying on this conversation.
