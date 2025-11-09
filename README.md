# LinkedIn Scraping
This project automates finding LinkedIn profiles via Google search, scraping their public content, and processing that content into a structured JSON format using an AI model asynchronously.

## Project Structure
```
Linkedin Scraper/
├── .env
├── .env.example
├── ai_processor.py        # Async AI text to JSON conversion
├── config.json            # Configuration settings
├── google_search.py       # Google Search results extraction
├── linkedin_scraper.py    # LinkedIn Login and Profile Scrape
├── main.py                # Main driver with async orchestration
├── profile_ids/
├── profile_txt/
├── profiles_json/
└── schema.json            # LinkedIn Profiles JSON schema
```

## Workflow
1. **Initialize Driver**: A Selenium Chrome driver is set up.
2. **Google Search**: Finds public LinkedIn profile URLs based on a query.
3. **LinkedIn Login**: Logs into LinkedIn.
4. **Profile Scraping**: Navigates to each profile, scrolls to load content, and saves the raw text to `profile_txt/`.
5. **Concurrent AI Processing**: Profiles batches are processed concurrently using semaphore to control API requests, rate limits and failed calls.
6. **Cleanup**: The Selenium driver is closed.

## Things to Edit Before Execution
> [!NOTE]
> Since LinkedIn is strict with bot detection, new accounts and/or better delays are necessary. LinkedIn take Browser Cache and Device IP address for bot detection and flags accounts for authentication if bot activity is detected.

1.  **`config.json`**:
    *   `searchParameters`: Set the `postQuery` and `numResults`.
    *   `concurrency`: Configure the `batchSize` and `aiRateLimitPerMinute`.
    *   `linkedin`: Replace `usernames` and `password` with your credentials.
    *   `selenium`: Specify the absolute path to your `chromeDriverPath` and a `chromeUserDataDir`.

2.  **`.env`**: Create from `.env.example` and add your AI provider's Base URL, API key, and Model name.
    ```bash
    cp .env.example .env
    ```

## Execution

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Main Script**:
    ```bash
    python main.py
    ```

The script will perform the workflow sequentially, saving intermediate and final results in the respective output directories.