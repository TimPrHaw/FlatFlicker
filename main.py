import immowelt
import threading
import configuration
import kleinanzeigen


def immowelt_task(mutex):
    immowelt.init_immowelt(mutex)


def kleinanzeigen_task(mutex):
    kleinanzeigen.init_kleinanzeigen(mutex)


if __name__ == "__main__":
    print('Start FlatFlicker')
    telegram_mutex = threading.Lock()
    config = configuration.read_config()
    if config['ImmoweltSettings']['url'] != '<url path>':
        print('Start Immowelt')
        thread_immowelt = threading.Thread(target=immowelt_task, args=(telegram_mutex,))
        thread_immowelt.start()
    """
    if config['KleinanzeigenSettings']['url'] != '<url path>':
        print('Start Kleinanzeigen')
        thread_kleinanzeigen = threading.Thread(target=kleinanzeigen_task, args=(telegram_mutex,))
        thread_kleinanzeigen.start()
    """
