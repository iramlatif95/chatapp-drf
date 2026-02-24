# chat/pipeline.py

class MessagePipeline:
    
    def __init__(self, nodes):
        self.nodes = nodes

    def run(self, user, group, message):
        data = message
        result = None

        for node in self.nodes:
            result = node.process(user, group, data)
            data = result  # pass result to next node

        return result  # final node returns saved message
