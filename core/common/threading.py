from threading import Thread

class Threading(Thread):
    
    def __init__(self, func):
        Thread.__init__(self)
        self.func = func

    def run(self):
        self.func()