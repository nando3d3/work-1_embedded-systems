import socket
import threading
import time
import json

class Client(threading.Thread):
    def __init__(self, server_num, count_car, sinal_v, speed_up, vel_media, host_central, port_central):
        super().__init__()
        self.server_num = server_num
        self.count_car = count_car
        self.sinal_v = sinal_v
        self.speed_up = speed_up
        self.vel_media = vel_media
        self.host_central = host_central
        self.port_central = port_central

    def format_msg(self, data):
        msg = json.dumps(data)
        return msg
       
    def send_message(self, data1):
        try:
            serv_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv_conn.connect((self.host_central, self.port_central))
            serv_conn.sendall(data1.encode('utf-8'))
            #print(data1)
            
            serv_conn.close()
            
            #print(f'enviei {data1}\n')
            
        except Exception as e:
            #print(f'Error sending message: ', e)
            pass
            
    def run(self):
        while True:
            car_velmedia = [i[1] for i in self.vel_media.values()]
        
            
            data = {
                'server_num': self.server_num,
                'car_count': self.count_car,
                'car_sinal_v': self.sinal_v,
                'car_speed_up': self.speed_up,
                'car_velmed': car_velmedia
            }
            
            msg = self.format_msg(data)
            self.send_message(msg)
            time.sleep(2)
