import requests
import pandas as pd

def fetch_jobs():
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": "13b73c44c5msh2b4a7490d191c85p1828c8jsn59d55b0ed7f8",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": "data scientist",
        "location": "Canada",
        "page": "1",
        "num_pages": "2",
        "remote_jobs_only": "false"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()["data"]
        df = pd.DataFrame(data)
        df = df[df["job_country"].str.lower() == "ca"]
        df = df[df["job_state"].str.lower().str.contains("on")]
        df.to_csv("jobs.csv", index=False)
        print("✅ Saved jobs.csv with", len(df), "rows")
    else:
        print("❌ Failed to fetch data:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    fetch_jobs()
