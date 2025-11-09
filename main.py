import os
import json
import dotenv
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from google_search import google_search_linkedin_profiles
from linkedin_scraper import linkedin_login, scrape_linkedin_profile
from ai_processor import process_profile_data_with_ai

def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        dotenv.load_dotenv()
        config['ai']['apiKey'] = os.getenv("API_KEY")
        config['ai']['baseUrl'] = os.getenv("BASE_URL")
        config['ai']['modelName'] = os.getenv("MODEL")
        return config
    except FileNotFoundError:
        print("Error: config.json not found. Please create it.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: Could not decode config.json. Please check for syntax errors.")
        exit(1)

def setup_driver(config):
    chrome_options = Options()
    chrome_options.add_argument(f"--remote-debugging-port={config['selenium']['remoteDebuggingPort']}")
    chrome_options.add_argument(f"--user-data-dir={config['selenium']['chromeUserDataDir']}")
    chrome_service = Service(executable_path=config['selenium']['chromeDriverPath'])
    try:
        print("Initializing Selenium Chrome driver...")
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        print("Driver initialized successfully.")
        return driver
    except WebDriverException as e:
        print(f"Failed to initialize Chrome driver: {e}")
        exit(1)

async def process_batch(file_paths_batch, config, semaphore):
    if not file_paths_batch:
        return

    print(f"\nStarting AI processing for a batch of {len(file_paths_batch)} profiles...")

    tasks = []
    for raw_data_path in file_paths_batch:
        profile_id = os.path.basename(raw_data_path).replace('.txt', '')
        task = asyncio.create_task(
            run_with_semaphore(profile_id, raw_data_path, config, semaphore)
        )
        tasks.append(task)

    await asyncio.gather(*tasks)
    print(f"Finished processing batch\n")

async def run_with_semaphore(profile_id, raw_data_path, config, semaphore):
    async with semaphore:
        rate_limit = config['concurrency']['aiRateLimitPerMinute']
        delay_between_requests = 60.0 / rate_limit if rate_limit > 0 else 0
        
        await process_profile_data_with_ai(profile_id, raw_data_path, config)
        await asyncio.sleep(delay_between_requests)

async def main():
    config = load_config()
    driver = setup_driver(config)

    post_query = config['searchParameters']['postQuery']
    num_results = config['searchParameters']['numResults']
    
    linkedin_profiles = google_search_linkedin_profiles(driver, post_query, num_results, config)
    
    max_concurrent_tasks = 4 
    semaphore = asyncio.Semaphore(max_concurrent_tasks)

    batch_size = config['concurrency']['batchSize']
    scraped_files_batch = []

    for url in linkedin_profiles:
        output_path = scrape_linkedin_profile(driver, url, config)
        if output_path:
            scraped_files_batch.append(output_path)

        if len(scraped_files_batch) >= batch_size:
            # Pass the semaphore to the batch processor
            await process_batch(scraped_files_batch, config, semaphore)
            scraped_files_batch = []

    if scraped_files_batch:
        print("Processing the final batch of profiles...")
        # Pass the semaphore to the final batch processor
        await process_batch(scraped_files_batch, config, semaphore)

    driver.quit()
    print("Selenium driver closed.")

if __name__ == "__main__":
    asyncio.run(main())