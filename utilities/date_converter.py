# -*- coding: utf-8 -*-
from dateutil.parser import parse
import parsedatetime
from datetime import datetime
from unidecode import unidecode
import re
import codecs


class DateConverter(object):

    @staticmethod
    def parse_datetime(value):

        if value is None or value is '':
            return None
        else:
            try:
                return parse(value).strftime("%Y-%m-%d %H:%M:%S")

            except ValueError:
                return None

    @staticmethod
    def parse_datetime_europe(value):

        if value is None or value is '':
            return None
        else:
            try:
                return parse(value).strftime("%Y-%d-%m %H:%M:%S")

            except ValueError:
                return None

    @staticmethod
    def parse_date(value):
        try:
            d = parse(value)
        except ValueError:
            return value
        else:
            return d.strftime("%Y-%m-%d")

    @staticmethod
    def extract_date(v):

        import string
        printable = set(string.printable)
        value = filter(lambda x: x in printable, v)

        value = value.lower().replace(' a ', ' -a- ')

        cal = parsedatetime.Calendar()
        time_struct, parse_status = cal.parse(value)

        date = datetime(*time_struct[:6])
        return date

    def get_date_from_url(self, url):

        def parse_date_str(date_str):
            try:
                datetime_obj = parse(date_str)
                return datetime_obj
            except:
                # near all parse failures are due to URL dates without a day
                # specifier, e.g. /2014/04/
                return None

        date_regex = r'([\./\-_]{0,1}(19|20)\d{2})[\./\-_]{0,1}(([0-3]{0,1}[0-9][\./\-_])|' \
                             r'(\w{3,5}[\./\-_]))([0-3]{0,1}[0-9][\./\-]{0,1})?'

        date_match = re.search(date_regex, url)
        if date_match:
            date_str = date_match.group(0)
            datetime_obj = parse_date_str(date_str)
            if datetime_obj:
                return datetime_obj
        #
        # date_match = re.search(date_regex, url)
        # if date_match:
        #     date_str = date_match.group(0).replace('/', '-') + '1'
        #
        #     datetime_obj = self.extract_date(date_str)
        #     if datetime_obj:
        #         return datetime_obj
        # else:
        #     return None


if __name__ == '__main__':

    import string

    printable = set(string.printable)

    url = ''
    description = 'May 04, 2007 · a surveillance video shows 17-year-old Kara Kopetsky walking out of her high school on May 4, 2007, before classes let out.'
    description = filter(lambda x: x in printable, description)
    title = 'Egypts Dr. Ruth: Lets talk sex in the Arab world - CNN.com'

    date = DateConverter().get_date_from_url(url)
    if not date:
        date = DateConverter.extract_date(description[:18])
    if not date:
        date = DateConverter.extract_date(title)

    print date