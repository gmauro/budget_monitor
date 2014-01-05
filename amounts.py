"""
"""
import collections
import matplotlib.pyplot as plt
import numpy as np
import time


class Amounts():
    """
    """
    def __init__(self, movs, cf):
        self.revenues = {}
        self.outputs = {}
        main_categories = cf.get_all_categories()
        for cat in main_categories:
            self.revenues[cat] = 0
            self.outputs[cat] = 0
        self.movs = movs
        self.cf = cf

    def _get_amounts_by_cat(self, year, month=None):
        revenues = {}
        outputs = {}
        main_categories = self.cf.get_all_categories()
        for cat in main_categories:
            revenues[cat] = 0
            outputs[cat] = 0
        for uid in self.movs.get_all_regular_movements_uid():
            details = self.movs.get_movement_details(uid)
            amount = details['amount']
            if (details['year'] == year and not month):
                if (details['amount_sign']):
                    revenues[details['main_cat']] += amount
                else:
                    outputs[details['main_cat']] += amount
            elif (details['year'] == year and details['month'] == month):
                if (details['amount_sign']):
                    revenues[details['main_cat']] += amount
                else:
                    outputs[details['main_cat']] += amount

        return revenues, outputs

    def _get_amounts(self, year, month=None):
        revenues = {year: 0}
        outputs = {year: 0}
        if (month):
            revenues[month] = 0
            outputs[month] = 0
        for uid in self.movs.get_all_regular_movements_uid():
            details = self.movs.get_movement_details(uid)
            amount = details['amount']
            if (details['year'] == year):
                if (details['amount_sign']):
                    revenues[year] += amount
                else:
                    outputs[year] += amount
            if (month and details['month'] == month):
                if (details['amount_sign']):
                    revenues[month] += amount
                else:
                    outputs[month] += amount

        return revenues, outputs



    def display_dashboard(self, year):
        revenues, outputs = self._get_amounts(year=year)
        labels = ['revenues', 'outputs']
        sizes = [revenues[year], outputs[year]]
        title = time.strftime("Year %Y", time.strptime("1 1 %s" % year, "%d %m %Y"))
        ind = np.linspace(0, 0.5, 2)
        width = 0.25
        p1 = plt.bar(0, revenues[year], width, color='YellowGreen')
        p2 = plt.bar(0.5, outputs[year], width, color='firebrick')
        plt.title(title)
        plt.yticks(np.arange(0, 80000, 100000))
    #plt.legend( (p1[0], p2[0]), labels )
        plt.xticks(ind + width / 2., labels)

        plt.show()

    def display_text_summary(self, label, revenues, outputs, outs_by_cat):
        labels = []
        sizes = []
        print label
        print "revs: %s" % revenues
        print "outs: %s" % outputs
        ord_categories = collections.OrderedDict(sorted(outs_by_cat.items()))
        for k, v in ord_categories.iteritems():
            if (outputs != 0):
                percentage = v * 100 / outputs
            else:
                percentage = 0
            print "\t%s \t%.2f%% \t%.2f" % (k, percentage, v)

    def show_all_monthly_budgets(self, year):
        for m in range(1, 13):
            self.show_monthly_budget(m, year)

    def show_annual_budget(self, year):
        revenues, outputs = self._get_amounts(year=year)
        revs, outs = self._get_amounts_by_cat(year=year)
        label = time.strftime("Year %Y", time.strptime("1 1 %s" % year,
                                                       "%d %m %Y"))
        self.display_text_summary(label, revenues[year], outputs[year], outs)
        self.display_dashboard(year)

    def show_monthly_budget(self, month, year):
        revenues, outputs = self._get_amounts(month=month, year=year)
        revs, outs = self._get_amounts_by_cat(month=month, year=year)
        label = time.strftime("%B %Y", time.strptime("1 %s %s" %
                                                     (month, year), "%d %m %Y"))
        self.display_text_summary(label, revenues[month], outputs[month], outs)

