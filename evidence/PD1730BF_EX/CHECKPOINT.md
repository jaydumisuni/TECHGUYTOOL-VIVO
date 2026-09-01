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
- Stock programmer accepts Sahara/Firehose read path
- Direct stock-programmer write attempt: REJECTED by target authorization (`ret_auth=0 / Unauthorized`) before a successful partition program was reported

## Dedicated local loader discovered
`D:\###\techguytool\Qualcomm-Tool-master\assets\devices\loaders\vivo\prog_firehose_8953_ddr_vivo_v9_youth.mbn`

Qualcomm Tool menu explicitly maps this loader to `VIVO V9 Yth (PD1730BF)`.

## Protected backups — LOCAL ONLY
Backups live under `evidence/PD1730BF_EX/backup/` and are git-ignored.

| Partition | Bytes | SHA-256 |
|---|---:|---|
| modemst1 | 2621440 | E3736FBFEADFDD7AEB04C25B070A47D771200DDDFA86B2383969952FB6379A91 |
| modemst2 | 2621440 | 265004136C2404BB9A3429D3700FA8B838909993936893FEE178260AD3A9C44C |
| fsg | 2621440 | 667C42E6B53820FB5A85EEA573559D0AF1D80AE5082B43289DBEB4F2664FC85E |
| persist | 33554432 | 573CE76C1B8A1DBA3C7EF49834FC79E2028998D23DA7B1152F3B22DB9A326F60 |

## Current boundary
The handset is currently responsive in Firehose on COM10, but that Firehose instance was loaded using the stock firmware programmer. A GPT read using the dedicated V9 Youth loader path succeeded only because the device was already in Firehose, so the dedicated programmer itself is not yet proven uploaded.

Next: return to fresh EDL/Sahara, upload the dedicated V9 Youth programmer, perform read-only GPT/storage proof, then choose the minimum write required to recover boot.
