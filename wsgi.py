# wsgi.py — entry point untuk pythonanywhere
import sys
import os

# Sesuaikan path ini dengan lokasi proyek di pythonanywhere,
# contoh: /home/USERNAME/klasterid
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application  # noqa: E402
