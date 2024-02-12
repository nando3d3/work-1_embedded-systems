from Client import *
import threading
import sys
import json
from ListeningServer import *


class Application(threading.Thread):
    def __init__(self, config):
        super().__init__()
        
        self.central, client1, client2 = config.config_central()
        self.host, self.port = self.central
        self.connection = Client(client1, client2)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener1 = Listening(self.socket, 'report1.json', 1)
        self.listener2 = Listening(self.socket, 'report2.json', 2)
        self.msgData1 = self.listener1.msgHandler
        self.msgData2 = self.listener2.msgHandler
        
    def run(self):
        self.msgData1.create_or_load_report('report1.json') #le report sobre quantidade de carros no server 1
        self.msgData2.create_or_load_report('report2.json') #le report sobre quantidade de carros no server 2
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen()
            print(f'Ouvindo em {self.host}:{self.port}')
            self.listener1.start()
            self.listener2.start()
        except Exception as e:
            print("Erro ao criar servidor: ", e)
            self.socket.close()
            
        try:
            while True:  
                print('''
0 - Sair
1 - Modo de Emergência
2 - Modo Noturno
3 - Modo Normal
4 - Info Tráfego 1
5 - Info Tráfego 2
                ''')
                
                map_msg = {'1': 'emergencia', '2': 'noturno', '3': 'normal'}
                
                option = input()
                msg = {}
                if option == '0':
                    self.msgData1.save_report_to_file('report1.json')
                    self.msgData2.save_report_to_file('report2.json')
                    self.socket.close()
                    print('saindo...')
                    sys.exit(0)
                elif option in ['1', '2', '3']:
                    msg['mode'] = map_msg[option]
                    json_msg = json.dumps(msg)
                    
                    self.connection.send_message_1(json_msg)
                    self.connection.send_message_2(json_msg)
                    #envia a mensagem para os servidores usando threads
                    # thread1 = threading.Thread(target=self.connection.send_message_1, args=(json_msg,))
                    # thread2 = threading.Thread(target=self.connection.send_message_2, args=(json_msg,))
                    # thread1.start()
                    # thread2.start()
                    # thread1.join()
                    # thread2.join()  
                    
                elif option == '4':
                    print(35*'_')
                    print('Server 1: [->, <-, V, ^]')
                    print(f'Total de carros:{self.msgData1.get_car_countTotal()}\n',)
                    print(f'Total de avanços no sinal vermelho: {self.msgData1.get_car_sinalV()}\n')
                    print(f'Total de velocidade alta: {self.msgData1.get_car_speedUp()}\n')
                    print(f'Velocidade media: {self.msgData1.get_car_velmed()}\n')
                    print(35*'_')
                elif option == '5':
                    print(35*'_')
                    print('Server 2: [->, <-, V, ^]')
                    print(f'Total de carros:{self.msgData2.get_car_countTotal()}\n',)
                    print(f'Total de avanços no sinal vermelho: {self.msgData2.get_car_sinalV()}\n')
                    print(f'Total de velocidade alta: {self.msgData2.get_car_speedUp()}\n')
                    print(f'Velocidade media: {self.msgData2.get_car_velmed()}\n')
                    print(35*'_')
                else:
                    print('Opção inválida.')

        except KeyboardInterrupt:
            self.msgData1.save_report_to_file('report1.json')
            self.msgData2.save_report_to_file('report2.json')
            self.socket.close()
