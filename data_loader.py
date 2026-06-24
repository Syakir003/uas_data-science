import os
from functools import reduce

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

FEATURE_COLUMNS = [
    'Miskin_2023', 'Miskin_2024', 'Miskin_2025',
    'IPM_2023', 'IPM_2024', 'IPM_2025',
]


def _load_miskin(filename, year):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f'File data tidak ditemukan: {path}')
    df = pd.read_excel(path, header=None)
    return pd.DataFrame({
        'Provinsi': df.iloc[5:43, 0].astype(str).str.strip().values,
        f'Miskin_{year}': df.iloc[5:43, 7].values,   # kolom 7 = Jumlah, Semester 1 (Maret)
    })


def _load_ipm(filename, year):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f'File data tidak ditemukan: {path}')
    df = pd.read_excel(path, header=None)
    return pd.DataFrame({
        'Provinsi': df.iloc[3:41, 0].astype(str).str.strip().values,
        f'IPM_{year}': df.iloc[3:41, 1].values,
    })


def load_data():
    """Baca semua file Excel, gabung berdasarkan Provinsi, dan ubah '-' jadi NaN."""
    frames = [
        _load_miskin('miskin_2023.xlsx', 2023),
        _load_miskin('miskin_2024.xlsx', 2024),
        _load_miskin('miskin_2025.xlsx', 2025),
        _load_ipm('ipm_2023.xlsx', 2023),
        _load_ipm('ipm_2024.xlsx', 2024),
        _load_ipm('ipm_2025.xlsx', 2025),
    ]
    data = reduce(lambda left, right: pd.merge(left, right, on='Provinsi'), frames)
    for col in FEATURE_COLUMNS:
        data[col] = pd.to_numeric(data[col].replace('-', np.nan), errors='coerce')
    return data.reset_index(drop=True)
