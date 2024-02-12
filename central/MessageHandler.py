import json

class MessageHandler:
    def __init__(self) -> None:
        self.car_countTotal = [0, 0, 0, 0]
        self.car_sinalV = [0, 0, 0, 0]
        self.car_speedUp = [0, 0, 0 , 0]
        self.car_velmed = [0, 0, 0, 0]        
    
    def get_car_countTotal(self):
        return self.car_countTotal
    
    def get_car_sinalV(self):
        return self.car_sinalV
    
    def get_car_speedUp(self):
        return self.car_speedUp
    
    def get_car_velmed(self):
        return self.car_velmed
    
    
    def create_or_load_report(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Tente carregar o conteúdo do arquivo JSON existente
                report = json.load(file)
            
            if 'semaforo 1' in report:
                data_semaforo1 = report['semaforo 1']
                self.car_countTotal[0] = data_semaforo1.get("total de carros", 0)
                self.car_sinalV[0] = data_semaforo1.get("total de avancos", 0)
                self.car_speedUp[0] = data_semaforo1.get("total de velocidade alta", 0)
                self.car_velmed[0] = data_semaforo1.get("velocidade media", 0)
                
            if 'semaforo 2' in report:
                data_semaforo2 = report['semaforo 2']
                self.car_countTotal[1] = data_semaforo2.get("total de carros", 0)
                self.car_sinalV[1] = data_semaforo2.get("total de avancos", 0)
                self.car_speedUp[1] = data_semaforo2.get("total de velocidade alta", 0)
                self.car_velmed[1] = data_semaforo2.get("velocidade media", 0)
                
            if 'semaforo 3' in report:
                data_semaforo3 = report['semaforo 3']
                self.car_countTotal[2] = data_semaforo3.get("total de carros", 0)
                self.car_sinalV[2] = data_semaforo3.get("total de avancos", 0)
                self.car_speedUp[2] = data_semaforo3.get("total de velocidade alta", 0)
                self.car_velmed[2] = data_semaforo3.get("velocidade media", 0)
                
            if 'semaforo 4' in report:
                data_semaforo4 = report['semaforo 4']
                self.car_countTotal[3] = data_semaforo4.get("total de carros", 0)
                self.car_sinalV[3] = data_semaforo4.get("total de avancos", 0)
                self.car_speedUp[3] = data_semaforo4.get("total de velocidade alta", 0)
                self.car_velmed[3] = data_semaforo4.get("velocidade media", 0)
                
        except FileNotFoundError:
            pass
    
    def save_report_to_file(self, file_path):
        # Crie um dicionário com os valores atualizados
        report = {
            "semaforo 1": {
                "total de carros": self.car_countTotal[0],
                "total de avancos": self.car_sinalV[0],
                "total de velocidade alta": self.car_speedUp[0],
                "velocidade media": self.car_velmed[0]
            },
            "semaforo 2": {
                "total de carros": self.car_countTotal[1],
                "total de avancos": self.car_sinalV[1],
                "total de velocidade alta": self.car_speedUp[1],
                "velocidade media": self.car_velmed[1]
            },
            "semaforo 3": {
                "total de carros": self.car_countTotal[2],
                "total de avancos": self.car_sinalV[2],
                "total de velocidade alta": self.car_speedUp[2],
                "velocidade media": self.car_velmed[2]
            },
            "semaforo 4": {
                "total de carros": self.car_countTotal[3],
                "total de avancos": self.car_sinalV[3],
                "total de velocidade alta": self.car_speedUp[3],
                "velocidade media": self.car_velmed[3]
            }
        }

        # Salve o relatório atualizado no arquivo
        with open(file_path, 'w') as file:
            json.dump(report, file, indent=4)
    
    def sum_Numbers(self, valorTotal, valor):
        return [a + b for a, b in zip(valorTotal, valor)]
        
    def processMessage(self, data, file_path):
        car_count = data.get('car_count', [])
        car_sinal_v = data.get('car_sinal_v', [])
        car_speed_up = data.get('car_speed_up', [])
        car_velmed = data.get('car_velmed', [])
        
        self.car_countTotal = car_count
        self.car_sinalV = car_sinal_v
        self.car_speedUp = car_speed_up
        self.car_velmed = car_velmed
        
        self.save_report_to_file(file_path)
     
        #self.car_countTotal = self.sum_Numbers(self.car_countTotal, car_count)
        #self.car_sinalV = self.sum_Numbers(self.car_sinalV, car_sinal_v)
        #self.car_speedUp = self.sum_Numbers(self.car_speedUp, car_speed_up)       