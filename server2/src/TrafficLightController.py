import RPi.GPIO as GPIO
import time
import threading

class TrafficLightController(threading.Thread):
    def __init__(self, pin_P_1, pin_P_2, pin_A_1, pin_A_2, pin_buzzer, buttons_controller):
        super().__init__()
        self.pin_P_1 = pin_P_1
        self.pin_P_2 = pin_P_2
        self.pin_A_1 = pin_A_1
        self.pin_A_2 = pin_A_2
        self.buttons_controller = buttons_controller  # objeto ButtonsControl
        self.pin_buzzer = pin_buzzer

        self.sinal_P_cor = None
        
        # sensor 1, 2 ,3, 4
        self.count_car = [0, 0, 0 ,0] #Numero de carros que passam ou param em cada cruzamento
        self.car_sinal_v = [0, 0, 0, 0] #Numero de carros que avancam sinal vermelho
        self.car_speedup = [0, 0, 0, 0] #Numero de carros que ultrapassam vel. permitida
        self.car_velmedia = {
            'cruz1': [0, 0],  # [quantidade de carros, velocidade media geral]
            'cruz2': [0, 0],  # [quantidade de carros, velocidade media geral]
            'cruz3': [0, 0],  # [quantidade de carros, velocidade media geral]
            'cruz4': [0, 0]   # [quantidade de carros, velocidade media geral]
        }
        self.change_mode = False
        
        
        self.modo = 'normal'
        self.buzzer = False
        
    def get_count_sinal_v(self):
        return self.count_sinal_v
    
    def get_count_vel(self):
        return self.count_vel
    
    def set_sinal_P_cor(self, cor):
        self.sinal_P_cor = cor
    
    def get_sinal_P_cor(self):
        return self.sinal_P_cor
    
    def set_modo(self, modo):
        self.modo = modo
        
    def get_modo(self):
        return self.modo
    
    def true_table(self, pin_1, pin_2, signalColor = None):
        if signalColor == 'verde':
            GPIO.output(pin_1, GPIO.LOW)
            GPIO.output(pin_2, GPIO.HIGH)
        elif signalColor == 'amarelo':
            GPIO.output(pin_1, GPIO.HIGH)
            GPIO.output(pin_2, GPIO.LOW)
        elif signalColor == 'vermelho':
            GPIO.output(pin_1, GPIO.HIGH)
            GPIO.output(pin_2, GPIO.HIGH)
        else:
            GPIO.output(pin_1, GPIO.LOW)
            GPIO.output(pin_2, GPIO.LOW)
        
    def count_time(self, tempo):
        remaining_time = tempo[0]
        button_once = False
        cor = self.get_sinal_P_cor()
        while remaining_time > 0 and not self.change_mode:
            button_pressed = self.buttons_controller.get_button_pressed()
            sensor_index = self.buttons_controller.get_sensor_index(button_pressed)
            
            self.check_violation()
            
            
            if ((self.buttons_controller.get_stopped_car(sensor_index) and cor == 'verde' and sensor_index in [3, 4]) or (self.buttons_controller.get_stopped_car(sensor_index) and cor == 'vermelho' and sensor_index in [0, 1])):
                if not button_once:
                    button_once = True
                    self.buttons_controller.button_pressed = None
                    if remaining_time > tempo[1]:
                        remaining_time = tempo[1]
                    else:
                        break
            if (button_pressed == self.buttons_controller.pin_ped_button_1 and cor == 'verde') or (button_pressed == self.buttons_controller.pin_ped_button_2 and cor == 'vermelho'):
                if not button_once:
                    button_once = True
                    self.buttons_controller.button_pressed = None
                    if remaining_time > tempo[1]:
                        remaining_time = tempo[1]
                    else:
                        break
            self.buttons_controller.button_pressed = None
            # sinalizar quando o cruzamento de pedestres ira ser fechado
            if (remaining_time == 1 and cor == 'amarelo'):
                self.buzzer = True

            if self.buzzer:
                GPIO.output(self.pin_buzzer, GPIO.HIGH)
                self.buzzer = False
            print(f'{remaining_time}')
            time.sleep(1)
            GPIO.output(self.pin_buzzer, GPIO.LOW)
            remaining_time -= 1
        
    
    def check_violation(self):
        button_pressed = self.buttons_controller.get_button_pressed()
        cor = self.get_sinal_P_cor()
        # indice do sensor associado ao botao usando get_sensor_index
        sensor_index = self.buttons_controller.get_sensor_index(button_pressed)

        
        # Se um dos sensores foi acionado
        if sensor_index != -1:
            self.count_car[sensor_index] += 1
            
            # verifica avanco de sinal vermelho
            if ((sensor_index in [0, 1] and cor == 'vermelho') or (sensor_index in [2, 3] and cor == 'verde')) and self.buttons_controller.get_stopped_car(sensor_index) == False:
                # buzzer
                self.buzzer = True
                self.car_sinal_v[sensor_index] += 1
                print('avancou sinal vermelho!\n')
            
            #verifica velocidade dos carros
            car_speed = self.buttons_controller.get_car_speed(sensor_index)
            if car_speed > 0:
                # atualiza media do respectivo cruzamento
                qtd_carros, vel_media = self.car_velmedia['cruz' + str(sensor_index + 1)]
                qtd_carros += 1
                nova_vel_media = round((vel_media + car_speed)/qtd_carros,1)
                self.car_velmedia['cruz' + str(sensor_index + 1)] = [qtd_carros, nova_vel_media]
                
                # verifica se velocidade esta acima
                if (sensor_index in [0, 1] and car_speed > 80) or (sensor_index in [2, 3] and car_speed > 60):
                    # buzzer
                    self.buzzer = True
                    self.car_speedup[sensor_index] +=1
                    print('velocidade alta!\n')
                    
        self.buttons_controller.button_pressed = None
    
    def control_signal(self):
        
        t_P_red = [10, 5]
        t_P_green = [20, 10]
        t_amarelo = [2, 2]
        
        # t_P_red = [5, 2]
        # t_P_green = [10, 5]
        # t_amarelo = [2, 2]
    
        modo = self.get_modo()
        
        
        if modo == 'normal':
            self.change_mode = False
            # Sinal P verde
            print('\nVERDE')
            self.set_sinal_P_cor('verde')
            self.true_table(self.pin_P_1, self.pin_P_2, self.get_sinal_P_cor())
            
            # Sinal A vermelho
            self.true_table(self.pin_A_1, self.pin_A_2, 'vermelho')
            self.count_time(t_P_green)
            
            # Sinal P amarelo
            print('\nAMARELO')
            self.set_sinal_P_cor('amarelo')
            self.true_table(self.pin_P_1, self.pin_P_2, self.get_sinal_P_cor())
            self.count_time(t_amarelo)
            
            # Sinal P vermelho
            print('\nVERMELHO')
            self.set_sinal_P_cor('vermelho')
            self.true_table(self.pin_P_1, self.pin_P_2, self.get_sinal_P_cor())
            
            # Sinal A verde
            self.true_table(self.pin_A_1, self.pin_A_2, 'verde')
            self.count_time(t_P_red)
            
            
            # Sinal A amarelo
            self.true_table(self.pin_A_1, self.pin_A_2, 'amarelo')
            print('\n')
            # sinalizar quando o cruzamento de pedestres ira ser fechado
            self.buzzer = True
            self.count_time(t_amarelo)
            
            
        if modo == 'emergencia':
            self.change_mode = False
            self.check_violation()
            if self.buzzer:
                GPIO.output(self.pin_buzzer, GPIO.HIGH)
                self.buzzer = False
            # Sinal P verde
            self.set_sinal_P_cor('verde')
            self.true_table(self.pin_P_1, self.pin_P_2, self.get_sinal_P_cor())
            # Sinal A vermelho
            self.true_table(self.pin_A_1, self.pin_A_2, 'vermelho')
            time.sleep(1)
            GPIO.output(self.pin_buzzer, GPIO.LOW)
            
            
                
        if modo == 'noturno':
            self.change_mode = False
            self.check_violation()                
            self.set_sinal_P_cor('amarelo')
            self.true_table(self.pin_P_1, self.pin_P_2, self.get_sinal_P_cor())
            self.true_table(self.pin_A_1, self.pin_A_2, self.get_sinal_P_cor())
            time.sleep(1)
            
            self.true_table(self.pin_P_1, self.pin_P_2)
            self.true_table(self.pin_A_1, self.pin_A_2)
            time.sleep(1)
            
    def run(self):
        while True:
            try:
                self.control_signal()
                
            except KeyboardInterrupt:
                GPIO.cleanup()