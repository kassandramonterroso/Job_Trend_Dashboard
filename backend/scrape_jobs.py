from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scrape_indeed_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        query = "data scientist"
        location = "Ontario"
        jobs = []

        for page_num in range(0, 5):  # 5 pages = ~50 jobs
            start = page_num * 10
            url = f"https://ca.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}&start={start}"
            print(f"Scraping: {url}")
            page.goto(url)
            print(f"visiting URL: {url}")
            page.wait_for_timeout(3000)

            job_cards = page.locator("div.job_seen_beacon")

            titles = job_cards.locator("h2.jobTitle").all_text_contents()
            companies = job_cards.locator("span.companyName").all_text_contents()
            locations = job_cards.locator("div.companyLocation").all_text_contents()
            snippets = job_cards.locator("div.job-snippet").all_text_contents()

            for i in range(min(len(titles), len(companies), len(locations))):
                jobs.append({
                    "title": titles[i].strip(),
                    "company": companies[i].strip(),
                    "location": locations[i].strip(),
                    "description": snippets[i].strip().replace("\n", " ")
                })

            time.sleep(1)

        browser.close()

        df = pd.DataFrame(jobs)
        df.to_csv("jobs.csv", index=False)
        print(f"✅ Scraped and saved {len(df)} jobs from Indeed.ca")

if __name__ == "__main__":
    scrape_indeed_jobs()
