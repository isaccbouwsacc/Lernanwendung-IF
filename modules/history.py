#veraltet
class ChatHistory:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})

    def get_history(self):
        return self.messages

    def clear(self):
        if len(self.messages) > 0:
            system_prompt = self.messages[0]
            self.messages = []
            self.messages.append(system_prompt)
