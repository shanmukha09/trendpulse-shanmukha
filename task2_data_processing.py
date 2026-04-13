import pandas as pd
import os

# Path to JSON file (output from Task 1)
file_path = "data/task1_output.json"

# Load JSON into DataFrame
df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")

# Remove duplicate id
df = df.drop_duplicates(subset="id")
print(f"After removing duplicates: {len(df)}")

# Drop rows with missing important fields
df = df.dropna(subset=["id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert data types
df["score"] = df["score"].astype(int)

# Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Clean title (remove extra spaces)
df["title"] = df["title"].str.strip()

# Save cleaned CSV
output_path = "data/trends_clean.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")

# Print category summary
print("\nStories per category:")
print(df["category"].value_counts())