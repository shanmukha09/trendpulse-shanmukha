import pandas as pd
import numpy as np

# Load cleaned CSV file
file_path = "data/trends_clean.csv"
df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}")

# Display first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average values
avg_score = df["score"].mean()

print(f"\nAverage score: {avg_score:.2f}")

# --- NumPy Analysis ---
scores = df["score"].values

print("\n--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):.2f}")
print(f"Median score : {np.median(scores):.2f}")
print(f"Std deviation: {np.std(scores):.2f}")
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Highest scored story
max_score_idx = df["score"].idxmax()
top_story = df.loc[max_score_idx]

print(f"\nHighest scored story: \"{top_story['title']}\" — {top_story['score']} points")

# Add new columns
df["score_rank"] = df["score"].rank(ascending=False).astype(int)
df["is_popular"] = df["score"] > avg_score

# Save new CSV
output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")