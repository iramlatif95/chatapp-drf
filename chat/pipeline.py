

class Node:
    
    async def process(self, message_data):
        return message_data  # override in child classes

class Pipeline:
    
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    async def run(self, message_data):
        for node in self.nodes:
            message_data = await node.process(message_data)
        return message_data
    