import pandas as pd
import numpy as np
import re

input_csv = "baseline_verification_data_raw.csv"            # exported ADE L CSV
output_csv = "baseline_verification_data_processed.csv"     # new processed file
T = 10e-9                                                   # LSB period (10 ns)
n_vectors = 256                                             # total input combinations
v_high = 1.0                                                # logic 1 threshold
v_low = 0.2                                                 # logic 0 threshold

# load and clean column names
df = pd.read_csv(input_csv)
df.rename(columns=lambda c: re.sub(r'v\("/(\w+)"[^\)]*\).*', r'\1', c), inplace=True)
df.rename(columns=lambda c: c.replace('time (s)', 'time'), inplace=True)

# define signal groups
time_col = 'time'
Z_cols = [f"Z{i}" for i in range(7, -1, -1)]
X_cols = [f"X{i}" for i in range(3, -1, -1)]
Y_cols = [f"Y{i}" for i in range(3, -1, -1)]

# sample one point per input vector (n*T/2 + T/4)
def nearest_row(time):
    return df.iloc[(df[time_col] - time).abs().idxmin()]

sample_times = np.arange(0, n_vectors) * T/2 + T / 4
sampled_rows = [nearest_row(t) for t in sample_times]
d = pd.DataFrame(sampled_rows).reset_index(drop=True)

# convert voltages to digital 0/1
def logic_level(v):
    if v > v_high: return 1
    elif v < v_low: return 0
    else: return np.nan  # in-between region (unsettled)

for col in Z_cols + X_cols + Y_cols:
    if col in d.columns:
        d[col] = d[col].apply(logic_level)

# keep only the signals of interest
cols_out = ["time"] + Z_cols + X_cols + Y_cols
d["time"] = sample_times

# save csv
d.to_csv(output_csv, index=False, columns=cols_out)
print(f"Bit-level data saved to {output_csv}")
print(d.head())
