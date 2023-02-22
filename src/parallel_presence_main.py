from threading import Thread
from presence_manager import PresenceManager
from image_bus_consumer import ImageBusConsumer

if __name__ == "__main__":
    presence_main = PresenceManager()
    image_consumer = ImageBusConsumer()

    presence_main_thread = Thread(target=presence_main.run, args=("presence_list.csv",))
    image_consumer_thread = Thread(target=image_consumer.run)

    presence_main_thread.start()
    image_consumer_thread.start()

    presence_main_thread.join()
    image_consumer_thread.join()
