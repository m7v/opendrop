# coding:utf-8
import threading

import opendrop.client
import opendrop.config

import ipaddress
import logging
import time

FILE_PATH = '/Users/a/Downloads/kak_dela.jpeg'
used_ids = {}

# Timeout between sends
timeout = 60 * 15 # 15 minutes


def _process_target_thread(info):
    address = str(ipaddress.ip_address(info.address))

    #logging.info(address)
    config = opendrop.config.AirDropConfig(interface='awdl0')
    client = opendrop.client.AirDropClient(config, (address, info.port))
    client_name = client.send_discover()
    logging.info('Name: %s, address: %s', client_name, address)
    if client_name in used_ids and (time.time() - used_ids[client_name]) < timeout:
        return

    try:
        if client.send_ask(FILE_PATH):
            logging.info('%s Accepted ✅', client_name)
            client.send_upload(FILE_PATH)
            used_ids[client_name] = time.time()
        else:
            logging.info('%s Declined ❌', client_name)

    except:
        pass

def _process_target(info):
    thread = threading.Thread(target=_process_target_thread, args=(info,))
    thread.start()


def _find_targets(config):
    browser = opendrop.client.AirDropBrowser(config)
    browser.start(callback_add=_process_target)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


def main():
    config = opendrop.config.AirDropConfig(interface='awdl0')
    _find_targets(config)


if __name__ == '__main__':
    logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S')
    main()
