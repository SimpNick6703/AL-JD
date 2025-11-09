import time
import os
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

def google_search_linkedin_profiles(driver, post, num_results, config):
    query = config['googleSearch']['queryBase'].format(post=post)
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    
    try:
        driver.get(search_url)
        time.sleep(random.uniform(config['delays']['medium_min'], config['delays']['medium_max']))
    except WebDriverException as e:
        print(f"Error navigating to Google search URL: {e}")
        return []

    linkedin_urls = []
    try:
        links = driver.find_elements(By.XPATH, "//a[contains(@href, 'linkedin.com/in/')]")
        for link in links:
            href = link.get_attribute('href')
            if href and "linkedin.com/in/" in href and "google.com/url?q=" not in href:
                linkedin_urls.append(href)
    except Exception as e:
        print(f"Error extracting LinkedIn URLs from Google search results: {e}")

    output_dir = config['paths']['profileIdsDir']
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, f"google_results_{post.replace(' ', '_')}.txt")
    with open(output_filename, 'w', encoding='utf-8') as f:
        for url in linkedin_urls:
            f.write(url + '\n')
    print(f"Extracted {len(linkedin_urls)} LinkedIn URLs and saved to {output_filename}")
    return linkedin_urls