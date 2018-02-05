from pyindi_sequence import INDIClient
import uuid

class Server:
    DEFAULT_PORT = INDIClient.DEFAULT_PORT

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
        self.id = uuid.uuid4().hex

    def to_map(self):
        return {'id': self.id, 'host': self.host, 'port': self.port, 'connected': self.is_connected() }

    def connect(self):
        self.client = INDIClient()

    def disconnect(self):
        if self.client:
            self.client.disconnectServer()
        self.client = None

    def is_connected(self):
        return self.client.isServerConnected() if self.client else False
