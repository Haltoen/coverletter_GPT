import os
import openai

class GPT_Handler():
    def __init__(self):
        self.has_api_key = False

    def check_API_KEY(self):
        return self.has_api_key
    def setup_API_KEY(self, txt):
        openai.api_key = txt
        self.has_api_key= True

    def build_task_prompt(self, task: str, context: dict):
        prompt = f"Task: {task}\n\nContext:"
        for key in context.keys():
            prompt = prompt + key + +": " + str(context[key]) + "\n"
        return prompt

    def chat_complete(self, prompt, temperature=0.7, max_tokens=150, funcs=None):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            functions= funcs
        )
        return response['choices'][0]['message']['content']
    
    def gen_coverletter(self, input : tuple):
        language = input[0]
        employer = input[1]
        job_description = input[2]
        extra_info = input[3] # (bool) let gpt ask for additional info

        dict_context = {
            "Employer": employer,
            "Job description": job_description
        }

        if extra_info:
            extra_prompt = self.build_task_prompt(task="Your task is to ask the user for information related to skills")

        prompt = self.build_task_prompt(task="Your task is to create a coverletter given the following information" )


