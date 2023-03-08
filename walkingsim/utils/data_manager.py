import datetime
import os
import pickle
import re
import sys

from loguru import logger


class DataManager:
    def __init__(self):
        self.__data_dir = "solutions/" + self._generate_data_dirname()
        self.__log_dir = self.__data_dir + "logs/"
        self._create_data_dir()

    @staticmethod
    def _generate_data_dirname():
        """
        Format: YYYYMMDD-HHMMSS
        """
        date_now = str(datetime.datetime.now())
        date_now = re.sub("\..*|-|:", "", date_now)
        date_now = re.sub(" ", "-", date_now)

        return date_now + "/"

    def _create_data_dir(self):
        try:
            os.mkdir(self.__data_dir)
        except FileExistsError:
            logger.error(f"The directory {self.__data_dir} already exists")
            sys.exit()
        except FileNotFoundError:
            logger.error(f"The parent directory for {self.__data_dir} doesn't exist")
            sys.exit()
        else:
            os.mkdir(self.__log_dir)

    def save_dat_file(self, filename, obj):
        """
        In .dat format
        """
        with open(self.__data_dir + filename, "wb") as fp:
            pickle.dump(obj, fp)
            logger.info(f"Saved {obj} in {self.__data_dir}/{filename}")
