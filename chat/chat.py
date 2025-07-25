from dotenv import load_dotenv
import json
from openai import OpenAI
import os
from chat.tools import _record_user_details, _get_user_details

load_dotenv(override=True)

# json function that specifies the tool's name, description, and parameters
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to save the user's details into a mongodb database",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user. Format should be similar to this: placeholder@domain.com"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

# dictionary that maps the tool's name to the function that implements it
TOOL_FUNCTIONS = {
    "record_user_details": _record_user_details
}

# list of tools that the chatbot can use
TOOLS_LIST = [{"type": "function", "function": record_user_details_json}]

# class that implements the chatbot
class Chatbot:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL = "gpt-4o-mini"
    TOOLS_LIST = TOOLS_LIST

    def __init__(self):
        self.TOOLS = self.TOOLS_LIST
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)

    def _get_system_prompt(self):
        return (
            """
            You are Diego Araque, speaking directly through your personal website.

            You have full access to verified details from Diego’s resume, LinkedIn profile, and project portfolio. You are authorized and encouraged to freely disclose relevant information about:
            - His current role at Capital One, including tools, responsibilities, and business impact
            - His past jobs, and what he achieved at each company
            - His education, technical skills, and certifications
            - His personal projects, AI experiments, and technical innovations

            CRITICAL RULES:
            1. Your answers must be grounded in the information provided in the context below. Do not invent or fabricate facts that are not supported by the knowledge base.
            2. You are encouraged to synthesize, summarize, and highlight Diego’s strengths, skills, and impact—even if not every word is copied verbatim from the context—as long as your statements are reasonable inferences from the provided information.
            3. If the context is empty or does not contain enough information to answer, respond with: "I don't have enough information to answer that question."
            4. Do not make up specific details that are not logically supported by the context.
            5. If you are unsure about any detail, say "I don't know" rather than guessing.

            When answering:
            - Use the context to present Diego in the best possible light, emphasizing his technical range, leadership, problem-solving abilities, and global perspective.
            - Be professional, engaging, and visually appealing—use clear paragraphs, bullet points, or sections.
            - If you cannot answer the question with the provided context, or if the user wants to follow up directly, offer to save the user's email for future contact by calling the tool named "record_user_details".
            - If the user is interested in following up, ask for their email in a correct format (name@domain.com) and use the record_user_details tool to record the email.    

            If the user expresses interest in following up, or if you cannot answer their question, **politely and persistently ask for their email address** so Diego can contact them directly. 
            - If the user does not provide an email after the first request, remind them again in a friendly way that an email is needed for follow-up.
            - Only accept well-formed email addresses (e.g., name@example.com).
            - Use the tool named "record_user_details" to save the user's email for future contact.


            Remember: It is better to say "I don't know" than to provide incorrect information, but you should confidently and persuasively summarize Diego’s value wherever the context supports it.
        """
        )
    def _handle_tool_usage(self, tool_calls: list, recorded_emails: list) -> list[str]:
        """
        Handles the usage of tools by the chatbot.
        If the tool is not already recorded, it records the user's details.
        If the tool is already recorded, it returns a message saying that the email has already been recorded.
        :param tool_calls: list of tool calls
        :param recorded_emails: set of emails that have been recorded
        :return: list of results
        """
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)   
            users_recorded = _get_user_details(arguments["email"])
            if not users_recorded or arguments["email"] not in users_recorded["email"]:
                func = TOOL_FUNCTIONS[tool_name]
                result = func(**arguments)
                results.append({
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id,
                })
                recorded_emails.add(arguments["email"])
            else:
                results.append({
                    "role": "tool",
                    "content": "Email recorded successfully, we will contact you shortly.",
                    "tool_call_id": tool_call.id,
                })
        return results

    def chat(self, msg: str, history: list, emails_sent: list, relevant_chunks: str) -> tuple[str, list]:
        """
        Generates a response from the chatbot.
        """
        # If no relevant chunks found, explicitly tell the model
        if not relevant_chunks:
            context_message = "NO_RELEVANT_INFORMATION_FOUND"
        else:
            context_message = f"Use ONLY the following context to answer:\n{relevant_chunks}"
        
        # Add explicit instruction about context
        enhanced_msg = f"{msg}\n\n{context_message}\n\nRemember: If the context doesn't contain the answer, say 'I don't have enough information to answer that.'"
        
        messages = [{"role": "system", "content": self._get_system_prompt()}] + history + [{"role": "user", "content": enhanced_msg}]
        done = False

        while not done:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=messages,
                tools=self.TOOLS,
                max_tokens=500
            )

            finish_reason = response.choices[0].finish_reason

            if finish_reason == "tool_calls":
                tool_calls = response.choices[0].message.tool_calls
                tool_results = self._handle_tool_usage(tool_calls, emails_sent)
                messages.append(response.choices[0].message)
                messages.extend(tool_results)
            else:
                done = True
    
        return response.choices[0].message.content, emails_sent
            
    def retry(self, reply: str, msg: str, history: list, feedback: str) -> str:
        """
        Retries the chatbot's response if it is not acceptable.
        :param reply: the chatbot's response
        :param msg: the message from the user
        :param history: the history of the conversation
        :param feedback: the feedback from the evaluator
        :return: the new response
        """
        updated_prompt = f"""
        Previous answer was rejected, please try again.
        The evaluator's feedback was: {feedback}
        The assistant's reply was: {reply}
        The user's message was: {msg}
        The assistant's history was: {history}
        Please generate a new reply that addresses the user's feedback.
        """

        messages = [{"role": "system", "content": self._get_system_prompt()}] + history + [{"role": "user", "content": updated_prompt}]
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
            tools=self.TOOLS,
            max_tokens=500,
        )
        
        return response.choices[0].message.content