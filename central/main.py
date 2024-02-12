from Application import Application

from ModelConfig import *

def main():
    config = ModelConfig('../modelconfig/config.json')
    
    app = Application(config)
    app.run()
    
if __name__ == "__main__":
    main()