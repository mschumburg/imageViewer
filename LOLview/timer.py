import time

class Timer():
    def start(self):
        self.startTime = time.time()

    def stop(self):
        end = time.time()
        print(end - self.startTime)
