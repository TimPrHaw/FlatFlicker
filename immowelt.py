import configuration
from bs4 import BeautifulSoup
import requests
import telegram_bot
import time
import csv


def init_immowelt(mutex):
    flag = 1
    older_flats = []

    # read config
    config = configuration.read_config()
    immowelt_url = config['ImmoweltSettings']['url']

    try:
        with open("immowelt_ids.txt", "r") as f:
            for line in f:
                older_flats.append(line.strip())
    except:
        print('no old flat_ids to load')
    while flag:

        # parse website
        try:
            r = requests.get(immowelt_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            flat_list = soup.select('html body div main div.content-ccdd5 div.container-4753a div.SearchResults-606eb '
                                    'div.SearchList-22b2e div.EstateItem-1c115')
            # check table items, safe and send it
            for flat in flat_list:
                # check flat id
                flat_id = flat.select_one('a')['id']

                if flat_id not in older_flats:
                    # init facts
                    price = 'k.A'
                    area = 'k.A'
                    rooms = 'k.A'
                    address = 'k.A'

                    # get flat address
                    address = flat.select_one('div.FactsMain-bb891 div div.estateFacts-f11b0 div.IconFact-e8a23 span').text.strip()
                    # get flat url
                    url = flat.select_one('a')['href']
                    # iterate through key_fact list
                    key_facts = flat.select('div.FactsMain-bb891 div.KeyFacts-efbce div')
                    for key_fact in key_facts:
                        hard_fact = key_fact.attrs.get('data-test')
                        if 'price' in hard_fact:
                            price = key_fact.text.strip()
                        elif 'area' in hard_fact:
                            area = key_fact.text.strip()
                        elif 'rooms' in hard_fact:
                            rooms = key_fact.text.strip()
                    # send shenanigans to telegram
                    print('send new Immowelt flat to Telegram')
                    mutex.acquire()
                    telegram_bot.notify(price, area, rooms, address, url)
                    mutex.release()
                    # append flat to list
                    older_flats.append(flat_id)

                    # save list to txt
                    with open("immowelt_ids.txt", "w") as f:
                        for s in older_flats:
                            f.write(str(s) + "\n")

        except:
            flag = 0
            mutex.release()
            print('incorrect Immowelt URL')

    time.sleep(60)
