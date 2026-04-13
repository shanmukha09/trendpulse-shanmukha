import pandas as pd
import matplotlib.pyplot as plt
import os

# Load analysed data
file_path = "data/trends_analysed.csv"
df = pd.read_csv(file_path)

# Create outputs folder
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# -------- Chart 1: Top 10 Stories by Score --------
top10 = df.sort_values(by="score", ascending=False).head(10)

# Shorten long titles
top10["title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure()
plt.barh(top10["title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# -------- Chart 2: Stories per Category --------
category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

# -------- Chart 3: Score vs Rank --------
plt.figure()

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["score_rank"], label="Popular")
plt.scatter(not_popular["score"], not_popular["score_rank"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Score Rank")
plt.title("Score vs Rank")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

# -------- Dashboard (Bonus) --------
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Chart 1 in dashboard
axes[0].barh(top10["title"], top10["score"])
axes[0].set_title("Top Stories")
axes[0].invert_yaxis()

# Chart 2 in dashboard
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Categories")
axes[1].tick_params(axis='x', rotation=30)

# Chart 3 in dashboard
axes[2].scatter(popular["score"], popular["score_rank"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["score_rank"], label="Not Popular")
axes[2].set_title("Score vs Rank")

fig.suptitle("TrendPulse Dashboard")
plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("Charts saved in outputs/ folder")