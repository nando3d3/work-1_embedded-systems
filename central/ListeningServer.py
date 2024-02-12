import socket
import threading
import json
from MessageHandler import MessageHandler
import time

class Listening(threading.Thread):
    def __init__(self, socket, report, server_num):
        super().__init__()
        self.socket = socket
        self.report = report
        self.msgHandler = MessageHandler()
        self.stop_event = False
        self.server_num = server_num
    
    def run(self):
        self.msgHandler.create_or_load_report(self.report)

        while True:
            try:
                conn, ender = self.socket.accept()
                #print('conectado a ', ender)
                data = conn.recv(1024)
                message = data.decode('utf-8')
                if not data:
                    conn.close()
                    #print('fechando conexao')
                    #break
                try:
                    json_data = json.loads(message)
                    if json_data['server_num'] == self.server_num:
                        #print('recebi msg!')
                        self.msgHandler.processMessage(json_data, self.report)
                except json.JSONDecodeError:
                    print('msg nao json:', message)
                finally:
                    conn.close()                   
            except Exception as e:
                print("Erro de conexao: ", e)
                #time.sleep(3)
                break
                
            except KeyboardInterrupt:
                conn.close()
                self.socket.close()
        
