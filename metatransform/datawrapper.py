class MetaTransformDataWrapper():
    def __init__(self, data=None, target=None):
        self.data = data
        self.target = target
        self._dict = {
            'data': self.data,
            'target': self.target
        }

    def __repr__(self) -> dict:
        return self.to_dict

    def to_dict(self):
        return self._dict