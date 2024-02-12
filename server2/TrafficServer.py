import threading
from src import *

from Listening import Listening
from Client import Client
from ModelConfig import *

class TrafficServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.host, self.port, self.host_central, self.port_central, self.pins_output, self.pins_input = ModelConfig('../modelconfig/config.json').config_server2()

        buttons_controller = ButtonsControl(*self.pins_input)
        buttons_controller.initialize_callbacks()
        
        self.traffic_controller = TrafficLightController(*self.pins_output, buttons_controller)
        
        #traffic_count = ()
        
        self.listener = Listening(self.host, self.port)
        self.connection = Client(
            2,
            self.traffic_controller.count_car, 
            self.traffic_controller.car_sinal_v, 
            self.traffic_controller.car_speedup, 
            self.traffic_controller.car_velmedia,
            self.host_central, 
            self.port_central)
 
    def run(self):
        
        self.traffic_controller.start()
        self.connection.start()
        self.listener.start()
        
        try:
            while True:
                msg = self.listener.get_data()
                if msg is not None:
                    # Reinicia o controle de sinal com o novo modo
                    print('Modo: ', msg)
                    self.traffic_controller.set_modo(msg)
                    self.traffic_controller.change_mode = True
                    self.listener.set_data(None)
        except KeyboardInterrupt:
            self.connection.send_message('servidor 2 encerrado!')
            print('mensagem enviada!')