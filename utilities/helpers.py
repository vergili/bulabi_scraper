# -*- coding: utf-8 -*-
import os
import re
from unidecode import unidecode


def get_file_paths(dir):
    """
    Parameters
    ----------
    dir: directory path

    Returns
    -------
    file_paths: list of files
    """
    dirpath, dirnames, filenames = os.walk(dir).next()
    file_paths = [os.path.join(dirpath, filename) for filename in filenames]

    return file_paths


def read_html_file(datadir, fileroot):
    """
    Encoding:  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    Parameters
    ----------
    datadir:  html files directory
    fileroot: html file prefix
    Returns  raw content and  encoding
    -------
    """
    raw_content = open('%s/html/%s.html' % (datadir, fileroot), 'r').read()
    selector = 'content="text/html.{1,7}charset=(.*?)"'
    charset = re.findall(re.compile(selector, re.DOTALL), raw_content)

    if charset:
        encoding = charset[0].strip().lower()
    else:
        encoding = None

    return raw_content, encoding


def non_decimal_clean(val):
    if val and isinstance(val, basestring):
        non_decimal = re.compile(r'[^\d.]+')
        return non_decimal.sub('', val)
    return val


def sqlalchemy_row_to_dict(row, reject_columns=()):
    d = {}
    for column in row.__table__.columns:
        if column.name in reject_columns:
            continue
        d[column.name] = getattr(row, column.name)

    return d


def sqlalchemy_rows_to_dict(rows):
    data = []
    for row in rows:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)
        data.append(d)

    return data


def dict_to_unicode(d):
    return {k: unidecode(v).encode(encoding='UTF-8') if isinstance(v, basestring) else v for k, v in d.items()}


if __name__ == '__main__':

    print non_decimal_clean('113,000 results')