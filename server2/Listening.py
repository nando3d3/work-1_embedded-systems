import socket
import threading
import json

class Listening(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.data = None

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f'Ouvindo em {self.host}:{self.port}')

        try:
            while True:
                conn, ender = self.socket.accept()
                print(f'Conectado a {ender}')

                while True:
                    data = conn.recv(1024)
                    if not data:
                        print('Conexão encerrada')
                        conn.close()
                        break
                    message = data.decode('utf-8')

                    try:
                        json_data = json.loads(message)
                        print('mensagem recebida:', json_data)
                        if 'mode' in json_data:  # Verifica se 'mode' está presente no JSON
                            self.set_data(json_data['mode'])
                    except json.JSONDecodeError:
                        print('mensagem inválida:', message)

        except KeyboardInterrupt:
            self.socket.close()
            print('Porta liberada')

        except Exception as e:
            print('Erro:', e)
