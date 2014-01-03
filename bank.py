"""
"""
import csv
from math import copysign

class MovementsReportReader(csv.DictReader):
    """
    A simple Movements Report reader.
    """
    #reader = csv.reader
    known = False
    movements_type = ''
    
    def __init__(self, f):
        magic = [] 
        magic.append(f.readline())
        magic.append(f.readline())
        if magic[0].startswith('Conto Corrente'):
            self.known = True
            self.movements_type = 'account'
            header = []
            l = f.readline()
            while not l.startswith(','):
                l = f.readline()
            self.reader = csv.DictReader(f)
        elif (magic[0].startswith(',') and magic[1].startswith('Carta di Credito')):
            self.known = True
            self.movements_type = 'rechargeable_credit_card'
            header = ['Data Operazione', 'Data Valuta', 'Descrizione', 
                      'Tipo operazione', 'Tipo rimborso', 'importo']
            block = []
            l = f.readline()
            while not l.startswith('Data'):
                print l
                l = f.readline()
            #block.append(",".join(header))
            block.append(l)
            l = f.readline()
            l = f.readline()
            while not l.startswith(','):
                block.append(l)
                l = f.readline()
            print block
            self.reader = csv.DictReader(block)
            print 'qui',  self.reader
        else:  
            raise ValueError('%s is not a known Movements Report' % f.name)

    def _get_movements_from_credit_card_report(self, reader):
        """
        """
        block = []
            #block.append(",".join(self.header))
        for row in reader:
            amount = float(row['Importo in \xe2\x82\xac'])
            if self._sign(amount) == 1.0:
                sign = False
            else:
                sign = True
            mv = {'transaction date': row['Data operazione'],
                  'currency date': row['Data Registrazione'],
                  'description': row['Descrizione Operazione'],
                  'transaction type': 'credit card',
                  'refund type': '',
                  'amount': abs(amount),
                  'sign': sign }
            block.append(mv)
        return block

    def _get_movements_from_account_report(self, reader):
        """
        """
        block = []
        for row in reader:
            if row['Entrate'] != '':
                amount = float(row['Entrate'])
                sign = True
            else:
                amount = float(row['Uscite'])
                sign = False
            mv = {'transaction date': row['Data Operazione'],
                  'currency date': row['Data Valuta'],
                  'description': row['Descrizione Completa'],
                  'transaction type': row['Descrizione'],
                  'refund type': '',
                  'amount': abs(amount),
                  'sign': sign }
            block.append(mv)
        return block

    def _sign(self, x):
        return lambda x: copysign(1, x)

    def get_movements(self):
        print self.reader
        if self.movements_type == 'account':
            return self._get_movements_from_account_report(self.reader)
        if self.movements_type == 'rechargeable_credit_card':
            return self._get_movements_from_credit_card_report(self.reader)

