

"""from django.contrib.auth import get_user_model
from django.db.models import Q
from chat.models import Chat, Message

User = get_user_model()




class BaseNode:
    def __init__(self, next_node=None):
        self.next = next_node

    def handle(self, data):
        if self.next:
            return self.next.handle(data)
        return data




class ValidateReceiverNode(BaseNode):

    def handle(self, data):
        receiver_username = data["receiver_username"]

        try:
            receiver = User.objects.only("id").get(username=receiver_username)
        except User.DoesNotExist:
            raise Exception("Receiver not found")

        data["receiver"] = receiver
        return super().handle(data)




class GetOrCreateChatNode(BaseNode):

    def handle(self, data):
        user = data["sender"]
        receiver = data["receiver"]

        chat = Chat.objects.filter(
            (Q(user1=user) & Q(user2=receiver)) |
            (Q(user1=receiver) & Q(user2=user))
        ).select_related("user1", "user2").first()

        if not chat:
            chat = Chat.objects.create(user1=user, user2=receiver)

        data["chat"] = chat
        return super().handle(data)






class CreateMessageNode(BaseNode):

    def handle(self, data):
        message = Message.objects.create(
            chat=data["chat"],
            sender=data["sender"],
            content=data.get("content"),
            image=data.get("image"),
            audio=data.get("audio"),
        )

        data["message"] = message
        return super().handle(data)






class ReloadOptimizedNode(BaseNode):

    def handle(self, data):
        message = Message.objects.select_related(
            "sender",
            "chat",
            "chat__user1",
            "chat__user2"
        ).prefetch_related("deleted_by").get(id=data["message"].id)

        data["message"] = message
        return super().handle(data)






class MessagePipeline:

    def __init__(self):
        self.pipeline = ValidateReceiverNode(
            GetOrCreateChatNode(
                CreateMessageNode(
                    ReloadOptimizedNode()
                )
            )
        )

    def run(self, data):
        return self.pipeline.handle(data)"""