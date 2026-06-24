import numpy as np
import data_loader

def test_load_data_columns_and_shape():
    df = data_loader.load_data()
    assert list(df.columns) == ['Provinsi'] + data_loader.FEATURE_COLUMNS
    assert len(df) == 38  # 38 provinsi (tanpa baris INDONESIA)

def test_feature_columns_are_numeric():
    df = data_loader.load_data()
    for col in data_loader.FEATURE_COLUMNS:
        assert np.issubdtype(df[col].dtype, np.number)

def test_papua_baru_missing_miskin_2023():
    df = data_loader.load_data()
    row = df[df['Provinsi'] == 'PAPUA TENGAH'].iloc[0]
    assert np.isnan(row['Miskin_2023'])      # tidak ada data 2023
    assert not np.isnan(row['IPM_2023'])     # IPM 2023 ada
