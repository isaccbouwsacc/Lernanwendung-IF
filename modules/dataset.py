import json
class DatasetManager:
    def __init__(self):
        self.dataset = ""
    def set_dataset(self, choice):
        self.dataset = choice
        #self.load_dataset()

    #def load_dataset(self):
    #    with open(f".\\dataset\\{self.dataset}.json", "r") as file:
    #        self.dataset_data = json.load(file)
