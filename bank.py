"""
"""
import csv


class MovementsReportReader(csv.DictReader):
    """
    A simple Movements Report reader.
    """
    def __init__(self, f):
        magic = f.readline()
        if not magic.startswith('Conto'):
            raise ValueError('%s is not a Movements Report' % f.name)
        header = []
        l = f.readline()
        while not l.startswith(','):
            l = f.readline()
            csv.DictReader.__init__(self, f)
