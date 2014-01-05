"""
"""
import hashlib


class MovementsCollector():
    """
    Class to collect movements from bank's report
    All movements have this attributes:
    transaction date, transaction type, currency date, amount, sign,
    description,refund type, main category, secondary category, status
    """
    labels = ['transaction date', 'transaction type', 'currency date', 'amount',
              'sign', 'description','refund type', 'main category',
              'secondary category']
    def __init__(self, logger, cf):
        self.movements = {}
        self.logger = logger
        self.cf = cf

    def _set_status(self, movement):
        if (movement['transaction type'] == 'Carta ricaricabile - ricarica') \
            or movement['transaction type'] == 'Utilizzo carta di credito ' \
                                             'Fineco':
            self.logger.info('movement from account to credit card: %s' %
                             str(movement['description']))
            movement['status'] = 'ignore'
        else:
            movement['status'] = 'regular'


    def add_movement_from_report(self, movement):
        """
        Adds a movement's details to the movements dictionary
        """
        uid = int(hashlib.md5('_'.join(str(movement.values()))).hexdigest(),
                  16)
        if uid in self.movements:
            self.logger.debug('movement already present: %s' % str(movement[
                'description']))
        else:
            self._set_status(movement)
            main_category, secondary_category = self.cf.get_categories(movement['description'])
            movement['main category'] = main_category
            movement['secondary category'] = secondary_category
            self.movements[uid] = movement

    def get_all_movements_uid(self):
        """
        Return a list of uids of all movements
        """
        return self.movements.keys()

    def get_all_regular_movements_uid(self):
        """
        Return a list of uids of all movements with status regular
        """
        uid_list = []
        for uid, mov in self.movements.iteritems():
            if mov['status'] == 'regular':
                uid_list.append(uid)
        return uid_list

    def get_movement_details(self, uid):
        """
        Retrieve all the details of a movement specified by his uid
        """
        if uid in self.movements:
            mov = self.movements[uid]
            details = {}
            details['year'] = mov['transaction date'].tm_year
            details['month'] = mov['transaction date'].tm_mon
            details['day'] = mov['transaction date'].tm_mday
            details['full_desc'] = mov['description']
            details['simple_desc'] = mov['transaction type']
            details['amount'] = mov['amount']
            details['amount_sign'] = mov['sign']
            details['main_cat'] = mov['main category']
            details['sec_cat'] = mov['secondary category']
            details['status'] = mov['status']
            return details
        else:
            raise ValueError('Movement uid {0} is unknown'.format(uid))


    def len(self):
        """
        Return the number of movements recorded
        """
        return int(len(self.movements))
