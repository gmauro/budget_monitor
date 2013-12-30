"""
"""
import hashlib
import time


class MovementsCollector():
    """
    Class to collect movements from bank's report
    """
    def __init__(self, logger, cf):
        self.movements = {}
        self.logger = logger
        self.cf = cf

    def add_from_account_report(self, movement):
        """
        Adds a movement's details to the movements dictionary
        """
        labels = ['Data Operazione', 'Uscite', 'Entrate', 'Data Valuta',
                  'Descrizione', 'Descrizione Completa']
        uid = int(hashlib.md5('_'.join(movement.values())).hexdigest(), 16)
        if (uid in self.movements):
            self.logger.debug('movement already present: %s' % '_'.join(
                movement.values()))
        else:
            if movement[labels[1]] != '':
                amount = float(movement[labels[1]])
                sign = False
            elif movement[labels[2]] != '':
                amount = float(movement[labels[2]])
                sign = True
            else:
                amount = float(0)
                sign = True
            transaction_date = time.strptime(movement[labels[0]], "%d/%m/%Y")
            simple_description = movement[labels[4]]
            full_description = movement[labels[5]]
            main_category, secondary_category = self.cf.get_categories(full_description)
            self.movements[uid] = (transaction_date, amount, sign,
                                   simple_description, full_description,
                                   main_category, secondary_category)

    def get_all_movements_uid(self):
        """
        Return a list of uids of all movements
        """
        return self.movements.keys()

    def get_movement_details(self, uid):
        """
        Retrieve all the details of a movement specified by his uid
        """
        details = {}
        details['year'] = self.movements[uid][0].tm_year
        details['month'] = self.movements[uid][0].tm_mon
        details['day'] = self.movements[uid][0].tm_mday
        details['full_desc'] = self.movements[uid][4]
        details['simple_desc'] = self.movements[uid][3]
        details['amount'] = self.movements[uid][1]
        details['amount_sign'] = self.movements[uid][2]
        details['main_cat'] = self.movements[uid][5]
        details['sec_cat'] = self.movements[uid][6]
        return details


    def len(self):
        """
        Return the number of movements recorded
        """
        return int(len(self.movements))
