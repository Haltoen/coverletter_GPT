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

    def build_task_prompt(self, task, context: dict):
        prompt = f"Task: {task}\n\nContext:"
        for key in context.keys():
            prompt = prompt + key + +": " + str(context[key]) + "\n"
        return prompt

    def chat_complete(self, prompt, temperature=0.7, max_tokens=150):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content']
    
    def gen_coverletter(self, context : dict):
        prompt = self.build_task_prompt(task="Your task is to create a coverletter given the following information", )


