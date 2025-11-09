import os
import json
import asyncio
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.output_parsers import JsonOutputParser

SCHEMA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'schema.json')

try:
    with open(SCHEMA_FILE_PATH, 'r', encoding='utf-8') as f:
        LINKEDIN_PROFILE_SCHEMA = json.load(f)
except FileNotFoundError:
    print(f"Error: Schema file not found at {SCHEMA_FILE_PATH}.")
    LINKEDIN_PROFILE_SCHEMA = {}
except json.JSONDecodeError as e:
    print(f"Error decoding JSON schema from {SCHEMA_FILE_PATH}: {e}.")
    LINKEDIN_PROFILE_SCHEMA = {}

def setup_llm(config):
    ai_config = config['ai']
    llm = ChatOpenAI(
        api_key=ai_config.get('apiKey'),
        base_url=ai_config.get('baseUrl'),
        model=ai_config.get('modelName'),
        max_tokens=ai_config['maxTokens'],
        temperature=ai_config['temperature'],
        streaming=ai_config['stream'],
        callbacks=[StreamingStdOutCallbackHandler()] if ai_config['stream'] else []
    )
    return llm

async def process_profile_data_with_ai(profile_id, raw_data_path, config):
    if not os.path.exists(raw_data_path):
        print(f"Raw data file not found: {raw_data_path}")
        return None

    with open(raw_data_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    llm = setup_llm(config)
    parser = JsonOutputParser()

    schema_str = json.dumps(LINKEDIN_PROFILE_SCHEMA, indent=2)

    prompt_template = PromptTemplate(
        template="""You are an expert at extracting structured information from LinkedIn profiles.
        Your task is to convert the following LinkedIn profile text into a structured JSON object.
        You MUST adhere strictly to the provided JSON schema, including all top-level keys and their nested structures.

        **Key Rules for Extraction:**
        1.  **Strict Schema Adherence**: Only include fields that are defined in the `JSON Schema for the output` below.
            Do NOT add any extra fields that are not part of the schema definition.
        2.  **Missing Values**: If a field defined in the schema is not found or applicable in the profile text, set its value to `null`.
        3.  **'summary' vs. 'About'**: The 'About' section in the profile text should be mapped to the 'summary' field in the JSON output.
        4.  **Top-level 'location'**: Extract the primary geographical location of the user (e.g., "Gurugram, Haryana, India") to the top-level 'location' field.
        5.  **Positions Handling**:
            *   `currentPosition`: This should be a single object representing the *most recent and highest-level* ongoing position (if multiple 'Present' roles exist, prioritize the one most prominently described or the most recent start date).
            *   `previousPositions`: This array should include all other past positions, as well as any *other* ongoing positions that are not selected for `currentPosition`.
            *   For `startDate` and `endDate` in both position types:
                *   Parse dates like "Jan 2022 - Present" into `startDate: "Jan 2022"` and `endDate: null`.
                *   Parse "Jul 2019 - Dec 2021" into `startDate: "Jul 2019"` and `endDate: "Dec 2021"`.
                *   Map durations like "2 years 8 months" into the appropriate `startDate` and `endDate` if explicit dates are not available, or combine with provided dates.
        6.  **Education Handling**:
            *   Map 'institution' to 'university'.
            *   Map 'years' (e.g., "2015 - 2019") to 'startDate' and 'endDate' fields.
            *   Omit 'activities' and 'additional_info' if they are not part of the schema.
        7.  **Contact Information**: Extract email, LinkedIn URL, and portfolio links into the `contactInformation` object. Do not create a top-level `portfolio_link`.
        8.  **Skills**: Consolidate all mentioned skills (from "About" and "Top skills" sections) into the single 'skills' array.
        9.  **Licenses & Certifications**: Map 'date' to 'dateIssued' and 'credential_id' to 'credentialID'. If 'dateIssued' and 'date' both appear, prefer 'dateIssued'.
        10. **Projects**: Map 'years' to 'startDate' and 'endDate' fields for projects. Map 'company' to 'associatedWith'.
        11. **Honors & Awards**: Map 'date' to 'date'.

        JSON Schema for the output:
        ```json
        {schema_definition}
        ```
        {format_instructions}

        Profile Text:
        {profile_text}

        JSON Output:
        """,
        input_variables=["profile_text"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "schema_definition": schema_str
        }
    )

    chain = prompt_template | llm | parser

    max_retries = 3
    base_delay = 2

    for attempt in range(max_retries):
        try:
            print(f"Processing profile {profile_id} with AI (Attempt {attempt + 1}/{max_retries})...")
            structured_data = await chain.ainvoke({"profile_text": raw_text})
            
            output_dir = config['paths']['profilesJsonDir']
            os.makedirs(output_dir, exist_ok=True)
            output_filename = os.path.join(output_dir, f"{profile_id}.json")

            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=4)
            print(f"Structured data for {profile_id} saved to {output_filename}")
            return output_filename
            
        except Exception as e:
            print(f"Error on attempt {attempt + 1} for profile {profile_id}: {e}")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Waiting for {delay} seconds before retrying...")
                await asyncio.sleep(delay)
            else:
                print(f"All {max_retries} attempts failed for profile {profile_id}. Skipping.")
    
    return None