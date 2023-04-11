import openai
import os
# import requests
# import json

openai.api_key = os.environ.get("API")


class GPTInterface:
    SAVED_MESSAGES = [{"role": "system", "content": "You are an english assistant, you are in a chat with a user, so always speak english and correct the user if has an incorrect grammar, you have to act as human as possible."}]
    LANGUAGE = "English"
    CHANGED = False

    @staticmethod
    async def ProcessRequest(user_req):
        if (GPTInterface.CHANGED):
            GPTInterface.SAVED_MESSAGES = [{"role": "system", "content": "You are an" + GPTInterface.LANGUAGE +
                                            "assistant, you are in a chat with a user, so always speak english and correct the user if has an incorrect grammar, you have to act as human as possible."}]
            GPTInterface.CHANGED = False

        GPTInterface.SAVED_MESSAGES.append(
            {'role': 'user', 'content': user_req})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=GPTInterface.SAVED_MESSAGES
        )

        GPTInterface.SAVED_MESSAGES.append(
            {'role': 'system', 'content': response.choices[0].message["content"]})
        return response.choices[0].message["content"]
