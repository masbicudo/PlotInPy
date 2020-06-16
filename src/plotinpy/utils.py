class _Result(dict):
    def __init__(self, *args, **kwargs):
        super(_Result, self).__init__(*args, **kwargs)
        self.__dict__ = self
