import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

input_csv = "baseline_verification_data_processed_verified.csv"
save_fig = "baseline_verification_visualization.png"

# ---- load
df = pd.read_csv(input_csv)
A, B, Z, E = df["A_val"].astype(int), df["B_val"].astype(int), df["Z_val"].astype(int), df["Expected"].astype(int)

n = 16
actual   = np.zeros((n, n), dtype=int)
expected = np.zeros((n, n), dtype=int)
mask     = np.zeros((n, n), dtype=bool)

for a, b, z, e in zip(A, B, Z, E):
    if 0 <= a < n and 0 <= b < n:
        actual[b, a]   = z
        expected[b, a] = e
        mask[b, a]     = (z == e)

# ---- plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, n); ax.set_ylim(0, n)
ax.invert_yaxis()
ax.set_xticks(np.arange(n) + 0.5); ax.set_yticks(np.arange(n) + 0.5)
ax.set_xticklabels(range(n)); ax.set_yticklabels(range(n))
ax.set_xlabel("X (Input 1)"); ax.set_ylabel("Y (Input 2)")
ax.set_title("4x4 Multiplier Verification Table (Actual Z vs Expected Z)")

# grid lines
for i in range(n+1):
    ax.axhline(i, color='black', lw=0.5)
    ax.axvline(i, color='black', lw=0.5)

for i in range(n):
    for j in range(n):
        # color cell
        ax.add_patch(plt.Rectangle((j, i), 1, 1, color=("#b3ffb3" if mask[i, j] else "#ff9999")))
        # draw "\" diagonal (top-left -> bottom-right)
        ax.plot([j, j+1], [i, i+1], color='black', lw=0.5)
        # place texts: actual (upper-left), expected (lower-right)
        ax.text(j+0.30, i+0.73, f"{actual[i,j]}", ha='center', va='center', fontsize=9)  # left/top of "\"
        ax.text(j+0.73, i+0.3, f"{expected[i,j]}", ha='center', va='center', fontsize=9) # right/bottom

plt.tight_layout()
plt.savefig(save_fig, dpi=300)
print(f"Saved: {save_fig}")
plt.show()
