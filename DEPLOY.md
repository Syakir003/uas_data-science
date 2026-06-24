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

## 3. Buat virtualenv & install dependencies
Masih di Bash console yang sama:
```bash
mkvirtualenv klasterid --python=python3.11
pip install -r uas_data-science/requirements.txt
```
- Catatan: prompt akan berubah jadi `(klasterid) ...` menandakan virtualenv aktif.
- Lokasi virtualenv: `/home/USERNAME/.virtualenvs/klasterid`.

## 4. Buat Web App
- Tab **Web** → **Add a new web app** → **Next**.
- Pilih **Manual configuration** (BUKAN "Flask") → **Python 3.11** → **Next**.

## 5. Isi konfigurasi di tab Web
Scroll dan isi tiga bagian ini:

**a. Virtualenv**
```
/home/USERNAME/.virtualenvs/klasterid
```

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
