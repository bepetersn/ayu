"""
are_you_up.py

Python code to make sure a website is up.

"""
from abc import abstractmethod
import requests
from datetime import datetime
from time import sleep


class Result(object):
    """

    """

    def __init__(self, response):
        self.response = response
        self.ok = response.status_code == requests.codes.ok
        self.uri = response.url
        self.time = datetime.now()


class BaseChecker(object):
    """

    """

    def __init__(self, units_of_work, sleep_time, handler):
        self.units_of_work = units_of_work
        self.sleep_time = sleep_time
        self.handler = handler

    def run(self, should_run):

        while should_run(self):
            for result in self.check():
                if result.ok:
                    self.handler.on_up(result)
                else:
                    self.handler.on_down(result)

            self.sleep()

    def sleep(self):
        sleep(self.sleep_time)

    def check(self):
        return map(self.handle_unit_of_work, self.units_of_work)

    @abstractmethod
    def handle_unit_of_work(self, u):
        pass


class UrlChecker(BaseChecker):

    def handle_unit_of_work(self, u):
        return Result(requests.get(u))
