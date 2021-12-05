import time


class Timer:
    _start: float
    _end: float

    def start(self):
        self._start = time.time()

    def finish(self):
        self._end = time.time()

    @property
    def elapsed(self) -> float:
        return self._end - self._start
