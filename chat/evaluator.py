from dotenv import load_dotenv
from openai import OpenAI
import os
from pydantic import BaseModel

load_dotenv(override=True)

# class that specifies the evaluation of the response
class Evaluation(BaseModel):
    is_good_response: bool
    feedback: str

# class that implements the evaluator
class Evaluator:
    MODEL = "gemini-2.0-flash"
    NAME = "Diego"
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    def __init__(self):
        # init of the gemini client since we are using the gemini api for the evaluator
        self.client = OpenAI(api_key=self.GOOGLE_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

    def _get_evaluation_system_prompt(self):
        """
        Returns the system prompt for the evaluator.
        The system prompt is a string that describes the evaluator's role and behavior.
        It is used to guide the evaluator's responses and interactions with the user.
        The system prompt is also used to evaluate the evaluator's responses.
        The system prompt is also used to generate the evaluator's responses.
        The system prompt is also used to evaluate the evaluator's responses.
        :return: the system prompt
        """
        return f"You are an evaluator that decides whether a response to a question is acceptable. \
            You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
            The Agent is playing the role of {self.NAME} and is representing {self.NAME} on their website. \
            The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer who came across the website. \
            The Agent has been provided with context on {self.NAME} in the form of their summary, experience and CV. \
            With this context, please evaluate the latest response, replying with whether the response is a good response and your feedback. "
    def _get_evaluation_user_prompt(self, reply: str, msg: str, history: list) -> str:
        """
        Returns the user prompt for the evaluator.
        The user prompt is a string that describes the evaluator's role and behavior.
        It is used to guide the evaluator's responses and interactions with the user.
        The user prompt is also used to evaluate the evaluator's responses.
        The user prompt is also used to generate the evaluator's responses.
        The user prompt is also used to evaluate the evaluator's responses.
        :return: the user prompt
        """
        user_prompt = f"""
        The Agent's latest response was: {reply}
        The User's latest message was: {msg}
        The conversation history was: {history}
        Please evaluate the response and provide feedback or say it is acceptable.
        """
        return user_prompt


    def evaluate(self, reply: str, msg: str, history: list) -> Evaluation:
        """
        Evaluates the response of the chatbot.
        :param reply: the response of the chatbot
        :param msg: the message from the user
        :param history: the history of the conversation
        :return: the evaluation of the response
        """
        system_prompt = self._get_evaluation_system_prompt()
        user_prompt = self._get_evaluation_user_prompt(reply, msg, history)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.client.beta.chat.completions.parse(
            model=self.MODEL,
            messages=messages,
            response_format=Evaluation,
        )

        return response.choices[0].message.parsed        
