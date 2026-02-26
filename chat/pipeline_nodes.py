
from .pipeline import Node

class LoggingNode(Node):
    async def process(self, message_data):
        print(f"[LOG] Message from {message_data.get('sender')}: {message_data.get('message')}")
        return message_data

class ProfanityFilterNode(Node):
    async def process(self, message_data):
        bad_words = ["badword1", "badword2"]
        content = message_data.get("message", "")
        for word in bad_words:
            content = content.replace(word, "***")
        message_data["message"] = content
        return message_data