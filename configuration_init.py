import configparser


config_file = configparser.ConfigParser()

config_file.add_section("ImmoweltSettings")
config_file.set("ImmoweltSettings", "url", "<url path>")

config_file.add_section("KleinanzeigenSettings")
config_file.set("KleinanzeigenSettings", "url", "<url path>")

config_file.add_section("TelegramSettings")
config_file.set("TelegramSettings", "bot token", "<insert bot token>")
config_file.set("TelegramSettings", "chat id", "<insert chat ID>")

with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")

read_file = open("configurations.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()
