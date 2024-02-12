import socket

class Client:
    def __init__(self, client1, client2):
        self.host1, self.port1 = client1
        self.host2, self.port2 = client2
    
    def send_message_1(self, data):
        try:
            serv_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv_conn.connect((self.host1, self.port1))
            serv_conn.sendall(data.encode('utf-8'))
            serv_conn.close()
            print('Mensagem enviada server 1')
        except Exception as e:
            print(f'Erro servidor 1: ', e)
        
    def send_message_2(self, data):
        try:
            serv_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv_conn.connect((self.host2, self.port2))
            serv_conn.sendall(data.encode('utf-8'))
            serv_conn.close()
            print('Mensagem enviada server 2')
        except Exception as e:
            print(f'Erro servidor 2: ', e)
