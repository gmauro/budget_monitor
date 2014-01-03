"""
"""
import csv
from math import copysign
from time import strptime

class MovementsReportReader(csv.DictReader):
    """
    A simple Movements Report reader.
    """
    def __init__(self, f):
        self.known = False
        magic = [f.readline(), f.readline()]
        if magic[0].startswith('Conto Corrente'):
            self.known = True
            self.movements_type = 'account'
            l = f.readline()
            while not l.startswith(','):
                l = f.readline()
            csv.DictReader.__init__(self, f)
        elif (magic[0].startswith(',') and magic[1].startswith('Carta di Credito')):
            self.known = True
            self.movements_type = 'rechargeable_credit_card'
            block = []
            l = f.readline()
            while not l.startswith('Data'):
                l = f.readline()
            block.append(l)
            l = f.readline()
            l = f.readline()
            while not l.startswith(','):
                block.append(l)
                l = f.readline()
            csv.DictReader.__init__(self, block)
        else:  
            raise ValueError('%s is not a known Movements Report' % f.name)

    def _get_movements_from_rechargeable_credit_card_report(self):
        """
        """
        block = []
        for row in self:
            amount = float(row['Importo in \xe2\x82\xac'])
            if self._sign(amount) == 1.0:
                sign = False
            else:
                sign = True
            mv = {'transaction date': self._format_date(row['Data operazione']),
                  'currency date': self._format_date(row['Data Registrazione']),
                  'description': row['Descrizione Operazione'],
                  'transaction type': 'credit card',
                  'refund type': '',
                  'amount': abs(amount),
                  'sign': sign }
            block.append(mv)
        return block

    def _get_movements_from_account_report(self):
        """
        """
        block = []
        for row in self:
            if row['Entrate'] != '':
                amount = float(row['Entrate'])
                sign = True
            else:
                amount = float(row['Uscite'])
                sign = False
            mv = {'transaction date': self._format_date(row['Data Operazione']),
                  'currency date': self._format_date(row['Data Valuta']),
                  'description': row['Descrizione Completa'],
                  'transaction type': row['Descrizione'],
                  'refund type': '',
                  'amount': abs(amount),
                  'sign': sign }
            block.append(mv)
        return block

    def _format_date(self, mov_date):
        return strptime(mov_date, "%d/%m/%Y")

    def _sign(self, x):
        return copysign(1, x)

    def get_movements(self):
        if self.movements_type == 'account':
            return self._get_movements_from_account_report()
        if self.movements_type == 'rechargeable_credit_card':
            return self._get_movements_from_rechargeable_credit_card_report()

