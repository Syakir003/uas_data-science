# Deploy KlasterID ke PythonAnywhere

## 1. Upload kode
- Buat akun di pythonanywhere.com.
- Di tab **Files**, buat folder `klasterid` lalu upload semua file:
  `app.py`, `clustering.py`, `data_loader.py`, `wsgi.py`,
  folder `templates/`, `static/`, dan `data/` (6 file Excel).

## 2. Buat Web App
- Tab **Web** → **Add a new web app** → **Manual configuration** → Python 3.10.

## 3. Virtualenv
Di tab **Web** bagian *Virtualenv*, atau via console:
```bash
mkvirtualenv klasterid --python=python3.10
pip install flask pandas numpy scikit-learn plotly openpyxl
```
Masukkan nama virtualenv (`klasterid`) di kolom Virtualenv pada tab Web.

## 4. WSGI configuration
- Di tab **Web** → klik file WSGI configuration → ganti seluruh isinya:
```python
import sys
project_home = '/home/USERNAME/klasterid'   # ganti USERNAME
if project_home not in sys.path:
    sys.path.insert(0, project_home)
from app import app as application
```
- Ganti `USERNAME` dengan username pythonanywhere.

## 5. Reload
- Klik tombol hijau **Reload** di tab Web.
- Buka `https://USERNAME.pythonanywhere.com`.

## Troubleshooting
- Error 500 → cek **Error log** di tab Web.
- `ModuleNotFoundError` → pastikan virtualenv terpasang & paket ter-install.
- File Excel tak terbaca → pastikan folder `data/` ikut ter-upload.
