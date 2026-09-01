# Device 001 — Vivo 1727 / PD1730BF_EX

## Proven identity
- Brand: Vivo
- Model: 1727
- Product: PD1730BF_EX
- Platform family: Qualcomm 8953-class Firehose target
- USB mode: Qualcomm HS-USB QDLoader 9008
- Current port: COM10
- Storage: eMMC, 64 GB class
- GPT read: PASS

## Firmware
- Package: PD1730BF_EX_A_1.12.3 Android 8.1 branch
- Package manifest: 97/97 MD5 entries verified
- Complete TAR extracted locally under `firmware/PD1730BF_EX_A_1.12.3/` (firmware is git-ignored)
- Stock programmer accepts Sahara/Firehose read path
- Direct stock-programmer write attempt: REJECTED by target authorization (`ret_auth=0 / Unauthorized`) before a successful partition program was reported

## Dedicated V9 Youth loader — PROVEN
`D:\###\techguytool\Qualcomm-Tool-master\assets\devices\loaders\vivo\prog_firehose_8953_ddr_vivo_v9_youth.mbn`

Qualcomm Tool explicitly maps this loader to `VIVO V9 Yth (PD1730BF)`.

After a QFIL-compatible `reset_to_edl`, the phone returned to fresh Sahara and this exact loader was uploaded successfully. It booted Firehose (`TargetName=8953`) and read the full GPT successfully. Therefore the dedicated loader itself is now proven compatible with this handset.

## Protected backups — LOCAL ONLY
Backups live under `evidence/PD1730BF_EX/backup/` and are git-ignored.

| Partition | Bytes | SHA-256 |
|---|---:|---|
| modemst1 | 2621440 | E3736FBFEADFDD7AEB04C25B070A47D771200DDDFA86B2383969952FB6379A91 |
| modemst2 | 2621440 | 265004136C2404BB9A3429D3700FA8B838909993936893FEE178260AD3A9C44C |
| fsg | 2621440 | 667C42E6B53820FB5A85EEA573559D0AF1D80AE5082B43289DBEB4F2664FC85E |
| persist | 33554432 | 573CE76C1B8A1DBA3C7EF49834FC79E2028998D23DA7B1152F3B22DB9A326F60 |

A full 64 MiB `boot` backup was also taken locally before write testing.

## Controlled write-capability proof
To test write authority without intentionally changing device content:
1. Read the current `boot` partition.
2. SHA-256: `14269D687B944965107E527A6E1AFEE8F24FB6D30EF17E1492530A36D1CDAAB0`.
3. Attempted to write that exact same dump back to `boot` with the proven dedicated V9 Youth loader.
4. Target rejected the `<program>` request with `ret_auth=0` / `Unauthorized` and returned NAK.
5. Re-read `boot`; SHA-256 remained exactly `14269D687B944965107E527A6E1AFEE8F24FB6D30EF17E1492530A36D1CDAAB0`.

Result: dedicated loader solves Sahara/Firehose compatibility but does **not** remove Vivo write authorization. The failed proof write did not alter `boot`.

## Current boundary
- Device transport: PROVEN
- Dedicated PD1730BF programmer: PROVEN
- GPT/read access: PROVEN
- Firmware integrity: PROVEN
- Protected device data backups: COMPLETE
- Vivo write authorization: REQUIRED / BLOCKING
- Evidence of partial write from current attempts: NONE

Next: use a legitimate server-authorized Vivo Qualcomm service path from the existing local tool arsenal, perform a read/info preflight first, then flash the verified firmware while preserving QCN/NV partitions.
