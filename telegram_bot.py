import requests
import configuration


def notify(price, area, rooms, address, url):
    # read config
    config = configuration.read_config()

    bot_token = config['TelegramSettings']['bot token']
    bot_chatID = config['TelegramSettings']['chat id']

    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + \
                '&parse_mode=Markdown&text=' + \
                f'\nAddress: {address}' + f'\nPrice: {str(price)}' + \
                f'\nArea: {str(area)}' + f'\nRooms: {str(rooms)}' + \
                f'\n {url}'
    return requests.get(send_text)
