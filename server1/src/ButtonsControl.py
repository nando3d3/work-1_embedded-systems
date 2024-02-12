import RPi.GPIO as GPIO
import time
import threading


class ButtonsControl:
    def __init__(self, pin_ped_button_1, pin_ped_button_2, pin_sense_A_1, pin_sense_A_2, pin_sense_P_1, pin_sense_P_2):
        self.pin_ped_button_1 = pin_ped_button_1
        self.pin_ped_button_2 = pin_ped_button_2
        self.pin_sense_P_1 = pin_sense_P_1
        self.pin_sense_P_2 = pin_sense_P_2
        self.pin_sense_A_1 = pin_sense_A_1
        self.pin_sense_A_2 = pin_sense_A_2

        self.button_pressed = None
        
        # Sensores: 1, 2 , 3 e 4        
        self.car_speed = [0, 0, 0, 0]
        self.start_time = [None, None, None, None]

        self.stopped_car = [False, False, False, False]
        
        # Mapeamento de canais GPIO para índices de sensores
        self.sensor_mapping = {
            self.pin_sense_P_1: 0,
            self.pin_sense_P_2: 1,
            self.pin_sense_A_1: 2,
            self.pin_sense_A_2: 3
        }
        
    def set_car_speed(self, speed, i):
        self.car_speed[i] = speed
    
    def get_car_speed(self, i):
        return self.car_speed[i]

    def get_button_pressed(self):
        return self.button_pressed

    def get_sensor_index(self, channel):
        return self.sensor_mapping.get(channel, -1)
    
    def get_stopped_car(self, i):
        return self.stopped_car[i]
    
    def set_stopped_car(self, condicao, i):
        self.stopped_car[i] = condicao
    
    def initialize_callbacks(self):
        GPIO.add_event_detect(self.pin_ped_button_1, GPIO.FALLING, callback=lambda x: self.button_callback(self.pin_ped_button_1), bouncetime=400)
        GPIO.add_event_detect(self.pin_ped_button_2, GPIO.FALLING, callback=lambda x: self.button_callback(self.pin_ped_button_2), bouncetime=400)
        
        GPIO.add_event_detect(self.pin_sense_P_1, GPIO.BOTH, callback=lambda x: self.sensor_callback(self.pin_sense_P_1), bouncetime=14)
        GPIO.add_event_detect(self.pin_sense_P_2, GPIO.BOTH, callback=lambda x: self.sensor_callback(self.pin_sense_P_2), bouncetime=14)
        GPIO.add_event_detect(self.pin_sense_A_1, GPIO.BOTH, callback=lambda x: self.sensor_callback(self.pin_sense_A_1), bouncetime=14)
        GPIO.add_event_detect(self.pin_sense_A_2, GPIO.BOTH, callback=lambda x: self.sensor_callback(self.pin_sense_A_2), bouncetime=14)
    
    def button_callback(self, channel):
        if channel == self.pin_ped_button_1:
            print('Botão de pedestre 1 pressionado')
            self.button_pressed = self.pin_ped_button_1
        elif channel == self.pin_ped_button_2:
            print('Botão de pedestre 2 pressionado')
            self.button_pressed = self.pin_ped_button_2
    
    def sensor_callback(self, channel):
        if channel in self.sensor_mapping:
            sensor_index = self.sensor_mapping[channel]
            
            if GPIO.input(channel):  # Detecção de borda de subida
                #print(f'sensor {sensor_index + 1} up')
                self.start_time[sensor_index] = time.time()
                
                #um temporizador para verificar se não houve borda de descida em 500 ms (carro parado)
                timer = threading.Timer(0.5, self.check_for_car_stopped, args=(sensor_index, channel))
                timer.start()
            else:  # Detecção de borda de descida
                #print(f'sensor {sensor_index + 1} down')
                self.button_pressed = channel
                if self.start_time[sensor_index] is not None:
                    end_time = time.time()
                    elapsed_time = end_time - self.start_time[sensor_index]
                    speed = round((2 / elapsed_time) * 3.6, 2)
                    self.set_car_speed(speed, sensor_index)
                    print(f'vel: {speed:.3f} km/h')
                    self.start_time[sensor_index] = None
                    
                self.set_stopped_car(False, 0)
                self.set_stopped_car(False, 1)
                self.set_stopped_car(False, 2)
                self.set_stopped_car(False, 3)

    def check_for_car_stopped(self, sensor_index, channel):
        if self.start_time[sensor_index] is not None:
            self.set_stopped_car(True, sensor_index)
            self.button_pressed = channel
            self.start_time[sensor_index] = None