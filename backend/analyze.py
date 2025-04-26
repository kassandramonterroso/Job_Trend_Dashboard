import pandas as pd
from collections import Counter
import re

df = pd.read_csv("jobs.csv")

df = df.dropna(subset=["job_title", "job_city", "job_description"])

top_titles = df["job_title"].value_counts().head(10)
print("\n Top Job Titles:\n", top_titles)

top_cities = df["job_city"].value_counts().head(10)
print("\n Top Cities:\n", top_cities)

all_text = " ".join(df["job_description"].astype(str).values).lower()
words = re.findall(r'\b\w+\b', all_text)
stopwords = {"and", "the", "to", "in", "of", "for", "a", "with", "on", "is", "as", "an", "be", "or"}
filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
top_keywords = Counter(filtered_words).most_common(10)
print("\n Top Keywords in Descriptions:\n", top_keywords)
