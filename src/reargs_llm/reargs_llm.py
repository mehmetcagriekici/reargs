from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

import json

from lib.models import LLMCluster

from .prompt_template import PROMPT_TEMPLATE

# load the api key from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# takes clusters from the server, check reargs_engine to see implementation
class ReargsLLM:
    def __init__(self):
        self.client = client
        self.clusters = []
        self.response = []

    # return llm response
    def get_response(self):
        return self.response

    # get clusters from the user
    def get_clusters(self, clusters):
        self.clusters = clusters

    # generate content with genai
    def generate_content(self, model="gemini-2.5-flash"):
        # loop over the clusters
        for i in range(len(self.clusters)):
            # convert cluster into json before passing it to the prompt
            hydrated_cluster = self.clusters[i]
            cluster_json = json.dumps(hydrated_cluster, ensure_ascii=False)

            # create the prompt using the json and template
            prompt = PROMPT_TEMPLATE.replace("{cluster_json}", cluster_json)

            # generate a response from genai once per cluster
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=LLMCluster
                    )
            )

            # validate if response is valid json
            data = json.loads(response.text)
            # add to the self.response to be served
            self.response.append(data)
        
