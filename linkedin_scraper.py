import time
import os
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def linkedin_login(driver, username, password, config):
    login_url = "https://www.linkedin.com/login"
    print(f"Navigating to LinkedIn login page: {login_url}")
    try:
        driver.get(login_url)
        time.sleep(random.uniform(config['delays']['medium_min'], config['delays']['medium_max']))

        username_field = WebDriverWait(driver, config['delays']['long_max']).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        time.sleep(random.uniform(config['delays']['long_min'], config['delays']['long_max']))

        if "feed" in driver.current_url or "linkedin.com/in" in driver.current_url:
            print(f"Successfully logged in as {username}")
            return True
        else:
            print(f"Login failed for {username}. Current URL: {driver.current_url}")
            if "challenge" in driver.current_url or "security-check" in driver.current_url:
                print("Security challenge detected. Manual intervention might be required.")
            return False
    except (WebDriverException, NoSuchElementException) as e:
        print(f"Error during LinkedIn login for {username}: {e}")
        return False

def scrape_linkedin_profile(driver, profile_url, config):
    print(f"Navigating to profile: {profile_url}")
    try:
        driver.get(profile_url)
        time.sleep(random.uniform(config['delays']['long_min'], config['delays']['long_max']))

        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(config['delays']['medium_min'], config['delays']['medium_max']))

        page_content = driver.find_element(By.TAG_NAME, "body").text

        profile_id = profile_url.split("/in/")[-1].split("/")[0]
        
        output_dir = config['paths']['profileTxtDir']
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, f"{profile_id}.txt")

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(page_content)
        print(f"Scraped content from {profile_url} and saved to {output_filename}")
        return output_filename
    except (WebDriverException, NoSuchElementException) as e:
        print(f"Error scraping profile {profile_url}: {e}")
        return None