from django.conf import settings


def _get_name()
    from socket import gethostname
    from getpass import getuser
    return '%s@%s' % (getuser(), gethostname())