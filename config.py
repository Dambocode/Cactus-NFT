import json

def loadconfig():
    config_file = open("config.json", "r")

    config_data = json.load(config_file)

    config_file.close()
    
    return config_data



# data = loadconfig()
# print(data)