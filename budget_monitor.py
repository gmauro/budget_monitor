"""
"""
import argparse
import logging
import os
import sys
from bank import MovementsReportReader as DataReader
import movements as MV
import classifier as CF
import amounts as AM

LOG_FORMAT = '%(asctime)s|%(levelname)-8s|%(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def make_parser():
    parser = argparse.ArgumentParser(description="Budget monitor")
    parser.add_argument('--input-dir', type=str, help='input dir',
                        required=True)
    parser.add_argument('--categories', type=str,
                        help='yaml file with a dict of categories',
                        required=True)
    parser.add_argument('--logfile', type=str, help='log file(default=stderr)')
    parser.add_argument('--loglevel', type=str, choices=LOG_LEVELS,
                        help='logging level', default='INFO')
    return parser


def main(argv):
    """
    """
    parser = make_parser()
    args = parser.parse_args(argv)

    log_level = getattr(logging, args.loglevel)
    kwargs = {'format': LOG_FORMAT,
              'datefmt': LOG_DATEFMT,
              'level': log_level}
    if args.logfile:
        kwargs['filename'] = args.logfile
        logging.basicConfig(**kwargs)
    logger = logging.getLogger('budget_monitor')

    if not os.path.isfile(args.categories):
        sys.exit('ERROR: categories file does not exists')
    else:
        cf = CF.Classifier(logger, args.categories)

    mvs = MV.MovementsCollector(logger, cf)

    movements_recorded = 0
    movements_not_catched = 0
    if not os.path.isdir(args.input_dir):
        sys.exit('ERROR: input source is not a dir')
    else:
        path = args.input_dir
        for files in os.listdir(args.input_dir):
            if files.endswith('.csv'):
                logger.info('importing file %s' % files)
                with open(os.path.join(path, files)) as f:
                    try:
                        data_reader = DataReader(f)
                        for row in data_reader:
                            mvs.add_from_account_report(row)
                    except ValueError as e:
                        logger.info(e)
                logger.info('number of movements recorded: %d' %
                            (mvs.len() - movements_recorded))
                movements_recorded = mvs.len()
                logger.info('number of movements not catched: %d' %
                            (cf.get_not_catched() - movements_not_catched))
                movements_not_catched = cf.get_not_catched()


    am = AM.Amounts(mvs, cf)
    logger.info('Total number of movements recorded: %d' % mvs.len())
    #am.show_annual_budget(2013)
    am.show_monthly_budget(12, 2013)
    #am.show_all_monthly_budgets(2013)

    
if __name__ == "__main__":
    main(sys.argv[1:])
