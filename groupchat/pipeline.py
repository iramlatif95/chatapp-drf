
from .models import GroupMessage

class ValidateMessageNode:
    def process(self, user, group, message):
        if not message or message.strip() == "":
            raise ValueError("Message cannot be empty")
        return message

class SaveMessageNode:
    def process(self, user, group, message):
        group_message = GroupMessage.objects.create(
            sender=user,
            group=group,
            content=message
        )
        return group_message

class MessagePipeline:
    def __init__(self, nodes):
        self.nodes = nodes

    def run(self, user, group, message):
        data = message
        result = None
        for node in self.nodes:
            result = node.process(user, group, data)
            data = result
        return result