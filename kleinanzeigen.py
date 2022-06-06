import configuration
from bs4 import BeautifulSoup
import requests
import telegram_bot
import time
import threading
from urllib.request import Request, urlopen
import json


def init_kleinanzeigen(mutex):
    flag = 1
    older_flats = []

    try:
        with open("kleinanzeigen_ids.txt", "r") as f:
            for line in f:
                older_flats.append(line.strip())
    except:
        print('no old flat_ids to load')

    while flag:
        # read config
        config = configuration.read_config()
        kleinanzeigen_url = config['KleinanzeigenSettings']['url']
        req = Request(kleinanzeigen_url, headers={'User-Agent': 'Mozilla/5.0'})
        # parse website
        try:
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, "html.parser")
            #r = requests.get(kleinanzeigen_url)
            #soup = BeautifulSoup(r.content, 'html.parser')
            flat_list = soup.select('html body#srchrslt div.site-base div.site-base--content '
                                    'div#site-content.l-page-wrapper.l-container-row div.l-splitpage-flex '
                                    'div#srchrslt-content.l-splitpage-content.position-relative '
                                    'div.l-container-row.contentbox-unpadded.no-bg div.position-relative '
                                    'ul#srchrslt-adtable.itemlist.ad-list.lazyload.it3 li.ad-listitem.lazyload-item')
            # check table items, safe and send it
            for flat in flat_list:
                # check flat id
                flat_id = flat.select_one('article')['data-adid']
                time.sleep(3)

                if flat_id not in older_flats:
                    # init facts
                    price = 'k.A'
                    area = 'k.A'
                    rooms = 'k.A'
                    address = 'k.A'

                    # get flat url
                    url = 'https://www.ebay-kleinanzeigen.de' + flat.select_one('div.aditem-main--middle '
                                                                                'h2.text-module-begin a.ellipsis')['href']

                    # open subpage
                    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    webpage = urlopen(req).read()
                    subpage_flat = BeautifulSoup(webpage, "html.parser")

                    # get flat address
                    address = subpage_flat.select_one('html body#vap div.site-base div.site-base--content '
                                              'div#site-content.l-page-wrapper.l-container-row '
                                              'section#viewad-main.l-container-row '
                                              'section#viewad-cntnt.l-row.a-double-margin.l-container-row '
                                              'section.a-span-16.l-col '
                                              'article#viewad-product.l-container-row.no-overflow '
                                              'div#viewad-main-info.contentbox--vip.boxedarticle.no-shadow.l'
                                              '-container-row div.boxedarticle--details '
                                              'div.boxedarticle--details--full a.scrollable '
                                              'span#viewad-locality').text.strip()

                    # get flat price
                    price = subpage_flat.select_one('html body#vap div.site-base div.site-base--content '
                                            'div#site-content.l-page-wrapper.l-container-row '
                                            'section#viewad-main.l-container-row '
                                            'section#viewad-cntnt.l-row.a-double-margin.l-container-row '
                                            'section.a-span-16.l-col '
                                            'article#viewad-product.l-container-row.no-overflow '
                                            'div#viewad-main-info.contentbox--vip.boxedarticle.no-shadow.l-container'
                                            '-row div.boxedarticle--flex--container '
                                            'h2#viewad-price.boxedarticle--price').text.strip()
                    # iterate through key_fact list
                    key_facts = subpage_flat.select('html body#vap div.site-base div.site-base--content '
                                            'div#site-content.l-page-wrapper.l-container-row '
                                            'section#viewad-main.l-container-row '
                                            'section#viewad-cntnt.l-row.a-double-margin.l-container-row '
                                            'section.a-span-16.l-col '
                                            'article#viewad-product.l-container-row.no-overflow '
                                            'div#viewad-details.splitlinebox.l-container-row ul.addetailslist '
                                            'li.addetailslist--detail')
                    for key_fact in key_facts:
                        hard_fact = key_fact.text
                        if 'Wohnfläche' in hard_fact:
                            area = key_fact.select_one('span.addetailslist--detail--value').text.strip()
                        elif 'Zimmer' in hard_fact:
                            rooms = key_fact.select_one('span.addetailslist--detail--value').text.strip()
                    # send shenanigans to telegram
                    print('send new Kleinanzeigen flat to Telegram')
                    mutex.acquire()
                    telegram_bot.notify(price, area, rooms, address, url)
                    mutex.release()
                    # append flat to list
                    older_flats.append(flat_id)

                    # save list to txt
                    with open("kleinanzeigen_ids.txt", "w") as f:
                        for s in older_flats:
                            f.write(str(s) + "\n")

        except:
            flag = 0
            try:
                mutex.release()
            except:
                print('e')

            print('incorrect Kleinanzeigen URL')

    time.sleep(60)
