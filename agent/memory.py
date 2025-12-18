class Memory:
    def __init__(self):
        self.data = {
            "age": None,
            "income": None,
            "occupation": None
        }

    def update(self, key, value):
        if self.data.get(key) and self.data[key] != value:
            return "CONTRADICTION"
        self.data[key] = value
        return "OK"

    def missing_fields(self):
        return [k for k, v in self.data.items() if v is None]
