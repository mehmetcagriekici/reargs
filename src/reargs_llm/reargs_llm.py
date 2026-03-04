from google import genai

import os
from dotenv import load_dotenv

import json

from .prompt_template import PROMPT_TEMPLATE

# load the api key from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# takes clusters from the server -> list[list[dict]] : check reargs_engine to see implementation
class ReargsLLM:
    def __init__(self):
        self.client = genai.Client(api_key=api_key)
        self.clusters = None
        self.response = list()

    # return llm response
    def get_response(self):
        return self.response

    # get clusters from the user
    def get_clusters(self, clusters):
        self.clusters = clusters

    # generate content with genai
    def generate_content(self, model="gemini-2.5-flash"):
        # loop over the clusters
        for cluster_idx in range(len(self.clusters)):
            # convert cluster into json before passing it to the prompt
            hydrated_cluster = self.clusters[cluster_idx]
            cluster_payload = {"cluster_id": cluster_idx, "sentences": hydrated_cluster}
            cluster_json = json.dumps(cluster_payload, ensure_ascii=False)

            # create the prompt using the json and template
            prompt = PROMPT_TEMPLATE.replace("{cluster_json}", cluster_json)

            # generate a response from genai once per cluster
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
            )

            # validate if response is valid json
            data = json.loads(response.text)
            # add to the self.response to be served
            self.response.append(data)
        
