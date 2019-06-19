import string
import random

from username_generator import get_uname


def get_random_pass(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for i in range(size))


def get_random_uname():
    return get_uname(4, 10, True)


def get_email_by_uname(uname):
    return uname + "@gravmail.com"