from datetime import datetime

class Spy:
    def __init__(self, name, salutation, age, rating,password):
        self.name = name
        self.salutation = salutation
        self.age = age
        self.rating = rating
        self.is_online = True
        self.chats = []
        self.current_status_message = None
        self.password = password


class ChatMessage:

  def __init__(self, message, sent_by_me):
    self.message = message
    self.time = datetime.now()
    self.sent_by_me = sent_by_me

password = '$pbkdf2-sha256$29000$ihEiJMRYCwGA0DrnPMc4xw$0LKeUEGPaVJCF4UZt8ogRxXDXI0YsHmzgO.oWVi30to'
spy = Spy('bond', 'Mr.', 24, 4.7,password)

friends = []