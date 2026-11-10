# commit-activity

Repo kecil buat nge-track aktivitas harian. Tujuannya cuma satu: contribution graph
di profil kelihatan hijau konsisten (>= 100 hari terisi).

## Isi

| File | Fungsi |
|---|---|
| `activity.log` | log aktivitas harian (append-only) |
| `generate.py` | bikin commit backdate buat ngisi hari-hari yang kosong |
| `daily-commit.sh` | commit harian, tinggal dipasang ke cron / systemd timer |

## Aturan main biar beneran kehitung

1. Repo harus **public** dan commit masuk ke **default branch**.
2. Email di commit harus **terverifikasi** di akun GitHub.
3. Satu hari = satu kotak, walau commit-nya banyak. Jadi butuh banyak *hari*, bukan banyak commit.

## Pakai

```bash
python3 generate.py                 # 110 hari aktif dalam 150 hari terakhir
python3 generate.py --days 130 --span 200
git push origin HEAD:main
```

Commit harian otomatis:

```bash
./daily-commit.sh                   # manual
crontab -e
# 0 9 * * * /path/ke/commit-activity/daily-commit.sh
```
