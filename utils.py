import math, gzip, io, os, logging, logging.config, zipfile
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class Timer(object):

    @classmethod
    def default_print_if(cls, nb_done):
        """ only prints 0,1,2,3,9,10,20,30,..,90,100,200,300,...etc.
        """
        return nb_done % (10**int(math.log10(nb_done))) == 0

    def __init__(self, nb_total=None, dont_print_before=1, print_if=None):
        self.nb_total = nb_total
        self.min_print = dont_print_before
        self.start = datetime.utcnow()
        self.nb_done = 0

        if print_if is None:
            print_if = self.default_print_if
        self.print_if = print_if

    def update(self, nb_done=None):
        """ if nb_done is None, we will assume we did one more """
        if nb_done is None:
            self.nb_done += 1
            nb_done = self.nb_done
        else:
            self.nb_done = nb_done

        if nb_done >= self.min_print and self.print_if(nb_done):
            delta = datetime.utcnow() - self.start
            speed = 1. * nb_done /delta.total_seconds()
            # without a nb_total specified, there is not much we can tell
            if self.nb_total is None:
                logger.info('done {} in {} @ {:0.2f}/s'.format(
                    nb_done, delta, speed))
            # with a nb_total specified, we can have more stats (like an ETA)
            else:
                logger.info(
                    'done {} out of {} in {} @ {:0.2f}/s eta {}s'.format(
                    nb_done, self.nb_total, delta, speed,
                    timedelta(seconds=(self.nb_total - nb_done) / speed)))


def open(filename, *args, **kwargs):
    """ Open different types of files based on the extension """
    if filename.endswith('.gz'):
        return gzip.open(filename, *args, **kwargs)
    elif filename.endswith('.zip'):
        z = zipfile.ZipFile(filename)
        names = z.namelist()
        if len(names) != 1:
            raise ValueError('.zip files containing more than one file are not'
                             ' supported')
        return io.TextIOWrapper(z.open(names[0], 'rU'))
    else:
        return io.open(filename, *args, **kwargs)


def ask_before_overwrite(filename):
    """ if `filename` already exists, will prompt before overwriting """
    if os.path.exists(filename):
        return are_you_sure(
            u'The file {} already exists. Overwrite?'.format(filename))
    else:
        return True


def are_you_sure(msg='Are you sure?'):
    """ prompts and asks if sure to do X """
    while True:
        choice = input(msg + ' (Y/N) ')
        if choice == 'Y':
            return True
        elif choice == 'N':
            return False
