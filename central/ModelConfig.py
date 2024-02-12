import json


class ModelConfig:
    def __init__(self, file_path):
        
        with open(file_path, "r") as f:
            self.file = json.load(f)
    
    def config_central(self):
        
        serv_central = (self.file["host_central"], self.file["port_central"])
        client1 = (self.file["host_server_1"], self.file["port_server_1"])
        client2 = (self.file["host_server_2"], self.file["port_server_2"])
        
        return serv_central, client1, client2
    
    
    