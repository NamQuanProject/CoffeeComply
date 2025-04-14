import requests
from bs4 import BeautifulSoup
from google import genai
from dotenv import load_dotenv
import os
from google.genai.types import (
    FunctionDeclaration,
    GenerateContentConfig,
    GoogleSearch,
    HarmBlockThreshold,
    HarmCategory,
    MediaResolution,
    Part,
    Retrieval,
    SafetySetting,
    Tool,
    ToolCodeExecution,
    VertexAISearch,
)
from crawler.utils import safe_request



load_dotenv()
class Config:
    def __init__(self, api_key=None, model_name=None, temperature=0.0, name="DefaultAgent", max_tokens=2048):
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.name = name
        self.max_tokens = max_tokens
        

class History:
    def __init__(self, request, response, timestamp):
        self.request = request
        self.response = response
        self.timestamp = timestamp

class AIAgent:
    def __init__(self, config=None, default_agent=False):
        if default_agent == True :
            config = Config()
            config.api_key = "AIzaSyAVtquUcri8ehMleX4xF-H48P1Ox_Zc1yU"
            config.model_name = "gemini-2.5-pro-exp-03-25"
            config.temperature = 0.0
            config.name = "DefaultAgent"
        
        
        self.config = config
        self.client = None 
        self.model = None
        self.safety_setting = self.default_safety_settings()
        self.history = []
        self.api_key = config.api_key
        self.model_name = config.model_name
        self.max_tokens = config.max_tokens
        self.temperature = config.temperature

        self.initialize()

    def default_safety_settings(self):
        safety_settings = [
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
        ]
        self.safety_setting = safety_settings



    def initialize(self):
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.default_safety_settings()


    def close(self):
        self.client = None
    


    def generate_response(self, prompt):
        if self.client:
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt,
                config= GenerateContentConfig(
                    # system_instruction=self.system_instruction,

                    safety_settings=self.safety_setting,
                )
            )
            if response.candidates:
                return response.candidates[0].content.parts[0].text
            return None
        else:
            print("Not initialize the models")

    def generate_response_with_structure(self, prompt, structure):
        if self.client:
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt,
                
                config= {
                    "response_mime_type":"application/json",
                    "response_schema" : list[str]
                }
            )
            if response.candidates:
                return response.candidates[0].content.parts[0].text
            return None
        else:
            print("Not initialize the models")



    def fetch_full_text(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        response = safe_request(url, headers=headers)
        
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup and get text from element with id='main'
            soup = BeautifulSoup(response.content, 'html.parser')
            main_div = soup.find(id="main-content")
            if main_div:
                content = main_div.get_text(separator="\n", strip=True)  # More readable text
                return content
            else:
                return "No content found in element with id='main'"
        else:
            return f"Failed to fetch content: HTTP {response.status_code}"

    def summarize_content(self, raw_content):
        # Use the AI model to summarize the content
        prompt = f"Summarize the following content:\n\n{raw_content}"
        summary = self.generate_response(prompt)
        return summary
       


    
    def set_up_instruction(self, instruction):
        # You can add a method to set up any instructions if needed
        self.system_instruction = instruction


    def add_history(self, request, response, timestamp):
        self.history.append(History(request, response, timestamp))

    def clear_history(self):
        self.history.clear()