import pandas as pd

input_csv = "baseline_verification_data_processed.csv"

# load data
df = pd.read_csv(input_csv)
Z_cols = [f"Z{i}" for i in range(7, -1, -1)]
X_cols = [f"X{i}" for i in range(3, -1, -1)]
Y_cols = [f"Y{i}" for i in range(3, -1, -1)]

# detect whether bit order is reversed
def detect_order(cols):
    # Count toggles for each bit -> fastest toggling bit is LSB
    toggle_counts = [df[c].diff().abs().sum() for c in cols]
    fastest = cols[toggle_counts.index(max(toggle_counts))]
    return fastest  # name of bit toggling fastest

fast_X = detect_order(X_cols)
fast_Y = detect_order(Y_cols)
X_reversed = (fast_X == "X3")
Y_reversed = (fast_Y == "Y3")

if X_reversed or Y_reversed:
    print(" Bit-order mismatch detected:")
    if X_reversed: print("   - Input A (X) appears reversed → fixing in software")
    if Y_reversed: print("   - Input B (Y) appears reversed → fixing in software")
else:
    print("Bit order appears correct")

# reconstruct integer values
# apply reversal automatically if detected
X_bits = X_cols if not X_reversed else X_cols[::-1]
Y_bits = Y_cols if not Y_reversed else Y_cols[::-1]
Z_bits = Z_cols[::-1]  # Z order normally MSB -> LSB

A = df[X_bits[::-1]].dot([1, 2, 4, 8])
B = df[Y_bits[::-1]].dot([1, 2, 4, 8])
Z = df[Z_bits].dot([1, 2, 4, 8, 16, 32, 64, 128])

df["A_val"], df["B_val"], df["Z_val"] = A, B, Z
df["Expected"] = df["A_val"] * df["B_val"]
df["Pass"] = (df["Z_val"] == df["Expected"])

# report summary
n_total = len(df)
n_pass = df["Pass"].sum()
n_fail = n_total - n_pass
print(f"\nVerification complete: {n_pass}/{n_total} cases correct.")

if n_fail > 0:
    print("\nMismatched cases:")
    print(df.loc[~df["Pass"], ["time", "A_val", "B_val", "Z_val", "Expected"]].to_string(index=False))
else:
    print("All outputs match A x B perfectly!")

# save csv
out_csv = input_csv.replace(".csv", "_verified.csv")
df.to_csv(out_csv, index=False)
print(f"\nResults saved to: {out_csv}")
