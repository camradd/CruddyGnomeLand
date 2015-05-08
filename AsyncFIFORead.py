import threading
from Queue import Queue, Empty

class AsyncFIFORead:

    '''
     Opens a file and gives you the ability to read lines asynchronously.
     The file automatically closes when the containing python process is
     exited.
    '''

    def __init__(self, f):
        self.file = f if isinstance(f, file) else open(f, 'r')
        self.queue = Queue()
        t = threading.Thread(target=lambda: self.enqueue_output())
        t.daemon = True
        t.start()

    def enqueue_output(self):
        for line in iter(self.file.readline, b''):
            self.queue.put(line)
        self.file.close()

    def close(self):
        return self.file.close()

    def readline(self):
        try: line = self.queue.get_nowait()
        except Empty: return None
        else: return line
