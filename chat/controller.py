from chat.chat import Chatbot
from chat.rag import RAG
from chat.evaluator import Evaluator

class ChatController:
    def __init__(self):
        self.chatbot = Chatbot()
        self.rag = RAG()
        self.evaluator = Evaluator()

    def get_response(self, msg: str, history: list, emails_sent: list) -> tuple[str, list]:
        # get relevant chunks from our knwoledge base
        relevant_chunks = self.rag.get_relevant_chunks(msg)
        # get response from the chatbot
        reply, emails = self.chatbot.chat(msg, history, emails_sent, relevant_chunks)
        # evaluate response
        evaluation = self.evaluator.evaluate(reply, msg, history)

        # if the response is not good, get a new response
        # evaluate response until we get a good one
        while not evaluation.is_good_response:
            reply = self.chatbot.retry(reply, msg, history, evaluation.feedback)
            evaluation = self.evaluator.evaluate(reply, msg, history)

        return reply, emails