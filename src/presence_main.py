import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from presence_manager import PresenceManager


if __name__ == "__main__":
    fc = PresenceManager()
    fc.run("presence_list.csv")
