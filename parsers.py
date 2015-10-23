__author__ = 'arthur'

import re
import logging

from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from grab import Grab, DataNotFound

from config import PARSER_LOG_FILE, OUTPUT_FILE


# update date pattern
FMT_DATE_TIME_PATTERN_RATE_AM = '%Y %d %b, %H:%M'

# Target URLs
URL_AM = 'http://rate.am/am/armenian-dram-exchange-rates/banks/non-cash'
URL_EN = 'http://rate.am/en/armenian-dram-exchange-rates/banks/non-cash'
URL_RU = 'http://rate.am/ru/armenian-dram-exchange-rates/banks/non-cash'


class Parser:
    """Main parser class: requests target website and retrieves/parses the HTML content."""
    __g = Grab(log_file=OUTPUT_FILE)

    # Logging handler configuration
    handler = TimedRotatingFileHandler(PARSER_LOG_FILE, when='midnight', backupCount=7)
    handler.setLevel(logging.INFO)
    handler.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Logger initialization
    log = Logger('Parser-log')
    log.addHandler(handler)

    # Banks map {bank_logo: bank}
    banks = {}

    # Rates map {banks_name: rate}
    rates = {}

    # Requests counter
    number_of_requests = 0

    def __init__(self):
        """Initializes a new instance of the class."""
        self.log.info('parser is started')

    def get_rates(self):
        """Gets latest rates from target resource and stores in maps."""
        self.__g.go(URL_EN)
        self.banks = {}
        self.rates = {}

        # acquiring current time
        now = datetime.now()

        # parsing response HTML
        for table_row in self.__g.doc.select('//table[@id="rb"]/tr'):
            try:
                # acquiring bank logo
                img_selector_list = table_row.select('.//td[@class="bank"]/img/@src').one()
                bank_logo_uri = img_selector_list.text()

                # acquiring bank name in English
                bank_html_name = table_row.select('.//td[@class="bank"]/a').text()
                bank_name_en = re.sub('[.]', '', bank_html_name).strip()

                # initializing bank and rate objects
                from models import Bank, Rate
                bank = Bank(bank_logo_uri, now)
                bank.name_en = bank_name_en
                rate = Rate(now)

                # acquiring currency rates
                column = 1
                for td in table_row.select('.//td'):
                    if column == 5:
                        time_str = str(now.year) + ' ' + td.text()
                        update_time = datetime.strptime(time_str, FMT_DATE_TIME_PATTERN_RATE_AM)
                        rate.declared_update_time = update_time
                    if column == 6:
                        rate.usd_buying = td.text()
                    if column == 7:
                        rate.usd_selling = td.text()
                    if column == 8:
                        rate.eur_buying = td.text()
                    if column == 9:
                        rate.eur_selling = td.text()
                    if column > 9:
                        break
                    column += 1

                # adding bank and rates to containers
                self.banks[bank_logo_uri] = bank
                self.rates[bank_logo_uri] = rate
            except DataNotFound:
                pass  # Rows passed through filter, that do not contain valuable data
            except UnicodeEncodeError, err:
                self.log.error(str(err))

        # acquiring name of the banks in Armenian
        self.__g.go(URL_AM)
        for table_row in self.__g.doc.select('//table[@id="rb"]/tr'):
            try:
                img_selector_list = table_row.select('.//td[@class="bank"]/img/@src').one()
                bank_html_name = table_row.select('.//td[@class="bank"]/a').text()
                bank_logo_uri = img_selector_list.text()
                bank_name_am = re.sub('[.]', '', bank_html_name).strip()
                bank = self.banks[bank_logo_uri]
                bank.name_am = bank_name_am
            except DataNotFound:
                pass  # Rows passed through filter, that do not contain valuable data

        # acquiring name of the banks in Russian
        self.__g.go(URL_RU)
        for table_row in self.__g.doc.select('//table[@id="rb"]/tr'):
            try:
                img_selector_list = table_row.select('.//td[@class="bank"]/img/@src').one()
                bank_html_name = table_row.select('.//td[@class="bank"]/a').text()
                bank_logo_uri = img_selector_list.text()
                bank_name_ru = re.sub('[.]', '', bank_html_name).strip()
                bank = self.banks[bank_logo_uri]
                bank.name_ru = bank_name_ru
            except DataNotFound:
                pass  # Rows passed through filter, that do not contain valuable data

        # increasing counter
        self.number_of_requests += 1

    # /get_rates()
# /class Parser