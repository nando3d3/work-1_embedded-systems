import RPi.GPIO as GPIO
import json


class ModelConfig:
    def __init__(self, file_path):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        with open(file_path, "r") as f:
            self.file = json.load(f)
        
    def config_server2(self):
        host = self.file["host_server_2"]
        port = self.file["port_server_2"]
        host_central = self.file["host_central"]
        port_central = self.file["port_central"]
        
        jsons_outputs2 = self.file["outputs_2"]       
        jsons_inputs2 = self.file["inputs_2"]
        
        pin_P_1 = None
        pin_P_2 = None
        pin_A_1 = None
        pin_A_2 = None
        pin_buzzer = None
        pin_ped_button_1 = None
        pin_ped_button_2 = None
        pin_sense_P_1 = None
        pin_sense_P_2 = None
        pin_sense_A_1 = None
        pin_sense_A_2 = None
        
        for output in jsons_outputs2:
            GPIO.setup(output['gpio'], GPIO.OUT)
            if output['tag'] == 'semaforo_1_pino_1':
                pin_P_1 = output['gpio']
            elif output['tag'] == 'semaforo_1_pino_2':
                pin_P_2 = output['gpio']
            elif output['tag'] == 'semaforo_2_pino_1':
                pin_A_1  = output['gpio']
            elif output['tag'] == 'semaforo_2_pino_2':
                pin_A_2  = output['gpio']
            elif output['tag'] == 'buzzer':
                pin_buzzer  = output['gpio']
        
        for input in jsons_inputs2:
            GPIO.setup(input['gpio'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            if input['tag'] == 'botao_pedestre_1':
                pin_ped_button_1  = input['gpio']
            elif input['tag'] == 'botao_pedestre_2':
                pin_ped_button_2  = input['gpio']
            elif input['tag'] == 'sensor_via_auxiliar_1':
                pin_sense_P_1  = input['gpio']
            elif input['tag'] == 'sensor_via_auxiliar_2':
                pin_sense_P_2  = input['gpio']
            elif input['tag'] == 'sensor_via_principal_1':
                pin_sense_A_1  = input['gpio']
            elif input['tag'] == 'sensor_via_principal_2':
                pin_sense_A_2  = input['gpio']    
        
        pins_output = (pin_P_1, pin_P_2, pin_A_1, pin_A_2, pin_buzzer)
        pins_inputs = (pin_ped_button_1, pin_ped_button_2, pin_sense_P_1, pin_sense_P_2, pin_sense_A_1, pin_sense_A_2)
        
        return host, port, host_central, port_central, pins_output, pins_inputs