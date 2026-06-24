# Deploy KlasterID ke PythonAnywhere

Repo: https://github.com/Syakir003/uas_data-science

## 1. Buat akun
- Daftar gratis di https://www.pythonanywhere.com (akun **Beginner** sudah cukup).
- Username yang kamu pilih akan jadi alamat web: `https://USERNAME.pythonanywhere.com`.

## 2. Clone repo lewat Bash console
- Di dashboard → tab **Consoles** → **Bash**.
- Jalankan:
```bash
git clone https://github.com/Syakir003/uas_data-science.git
```
Ini menarik semua kode **beserta folder `data/`** (6 file Excel) sekaligus — tidak perlu upload manual.

## 3. Dependencies (akun gratis — pakai paket bawaan, JANGAN virtualenv)
Akun Beginner (gratis) cuma punya kuota disk 512 MB — bikin virtualenv berisi
pandas + numpy + scipy + scikit-learn + plotly akan kena `Disk quota exceeded`.
PythonAnywhere sudah menyediakan pandas, numpy, scikit-learn, flask, openpyxl
di system Python-nya, jadi cukup pakai itu.

Cek paket yang sudah ada:
```bash
python3.11 -c "import flask, pandas, numpy, sklearn, openpyxl; print('paket inti OK')"
python3.11 -c "import plotly; print('plotly OK')"
```
- Kalau `plotly OK` muncul → tidak perlu install apa pun.
- Kalau plotly error → install hanya plotly: `pip3.11 install --user plotly`

> Kalau sudah terlanjur bikin venv yang gagal, bersihkan dulu:
> `rmvirtualenv klasterid && rm -rf ~/.cache/pip`

(Akun berbayar dengan kuota besar boleh pakai venv biasa:
`mkvirtualenv klasterid --python=python3.11 && pip install -r uas_data-science/requirements.txt`)

## 4. Buat Web App
- Tab **Web** → **Add a new web app** → **Next**.
- Pilih **Manual configuration** (BUKAN "Flask") → **Python 3.11** → **Next**.

## 5. Isi konfigurasi di tab Web
**a. Virtualenv** → **KOSONGKAN** (biar pakai system Python yang sudah punya semua paket).
Isi hanya kalau kamu memang bikin venv di akun berbayar.

**b. Source code & Working directory**
```
/home/USERNAME/uas_data-science
```

**c. WSGI configuration file** (klik link-nya, hapus semua isi, ganti dengan):
```python
import sys
project_home = '/home/USERNAME/uas_data-science'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
from app import app as application
```
Ganti **USERNAME** dengan username pythonanywhere-mu di semua tempat.

## 6. Reload & buka
- Klik tombol hijau **Reload** di tab Web.
- Buka `https://USERNAME.pythonanywhere.com`.

## Update kode setelah deploy
Kalau ada perubahan kode, push ke GitHub dari laptop, lalu di Bash console PythonAnywhere:
```bash
cd uas_data-science && git pull
```
Lalu klik **Reload** lagi di tab Web.

## Troubleshooting
- **Error 500** → buka **Error log** di tab Web (paling bawah), lihat baris terakhir.
- **ModuleNotFoundError** → pastikan virtualenv terisi benar di tab Web & `pip install -r requirements.txt` sudah jalan di dalam venv `(klasterid)`.
- **Halaman blank / chart tidak muncul** → cek koneksi internet browser (chart pakai Plotly dari CDN).
- **File Excel tak terbaca** → pastikan `git clone` berhasil dan folder `data/` ada: `ls uas_data-science/data`.
