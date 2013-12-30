"""
"""
import yaml


class Classifier():
    """
    Class to classify movements from bank's report
    """

    def __init__(self, logger, categories_filename):
        #categories_filename = 'categories.yml'
        self.categories = yaml.load(open(categories_filename))
        self.not_catched = 0
        self.logger = logger
        self.logger.debug(self.categories)

    def _increment_not_catched(self):
        self.not_catched += 1

    def get_all_categories(self):
        return self.categories.keys()

    def get_categories(self, description):
        d = description.lower()
        for main_cat in self.categories:
            for sub_cat, patterns in self.categories[main_cat].iteritems():
                if patterns['pattern']:
                    for pattern in patterns['pattern']:
                        try:
                            d.index(''.join(pattern))
                            return main_cat, sub_cat
                        except ValueError:
                            pass
                        continue
        self.logger.debug('Not catched: %s' % d)
        self._increment_not_catched()
        return 'other', 'other'

    def get_not_catched(self):
        return self.not_catched