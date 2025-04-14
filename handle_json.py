import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from tqdm import tqdm

client = OpenAI(api_key="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")

def load_json_from_file(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON.")
        return []

def process_trading_policy_data(data):
    """Process the trading policy data, extracting description and summary."""
    for topic in data:
        print(f"Title: {topic.get('title', 'No title available')}")
        for subtopic in topic.get('subtopics', []):
            name = subtopic.get("name", "No name available")
            url = subtopic.get("url", "No URL available")
            description = subtopic.get("description", "No description provided.")
            summary = subtopic.get("summary", "No summary provided.")
            
            # Print or process each subtopic's information
            print(f"\nSubtopic Name: {name}")
            print(f"URL: {url}")
            print(f"Description: {description}")
            print(f"Summary: {summary}")
            print("-" * 40)



class ContentSummary(BaseModel):
    desciption: str
    summary: str
   




def structure_open_ai(prompt):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional financial analyst. Given a raw trading topic content"
                "Extract the relevant information, write a detailed description, and summarize it concisely. "
                "Return a JSON with two fields: 'description' and 'summary'."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format={
            
            "type": "json_schema",
            "json_schema": {
                "name": "trading_policy",
                "schema" : {
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string"
                        },
                        "summary": {
                            "type": "string"
                        },
                    },
                    "required": ["description", "summary"],
                    "additionalProperties": False,
                    
                },
                "strict": True
               
            },
            
        
        }
    )
    message = response.choices[0].message.content
    message_dict = json.loads(message)  # JSONDecodeError
    return message_dict




def handle_cases_from_file(file_path):
    """Load the JSON from the file and process it."""
    # Load the JSON data from the file
    data = load_json_from_file(file_path)

    for topic in tqdm(data):
        for subtopic in tqdm(topic.get("subtopics", [])):
            raw_text_description = subtopic.get("description", "")
            
            # Generate structured content using OpenAI
            result = structure_open_ai(raw_text_description)

            # Update subtopic with the generated content and summary
            subtopic["description"] = result.get("description", "")
            subtopic["summary"] = result.get("summary", "")

    # Write the updated JSON back to a new file
    with open("new_json.json", "w") as file:
        json.dump(data, file, indent=2)



handle_cases_from_file("main_and_subtopics.json")




