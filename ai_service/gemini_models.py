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
            config.api_key = "AIzaSyB22ThtcCvZuXual9uaT_6v4Bo5R6oBdok"
            config.model_name = "gemini-2.0-flash"
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


    def generate_response(self, prompt):
        self.client.models.generate_content(
            model=self.model_name, contents=prompt,
            config= GenerateContentConfig(
                # system_instruction=self.system_instruction,
                
                safety_settings=self.safety_settings,
            )
        )

    def add_history():
        pass

    def clear_history():
        pass