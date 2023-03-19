from loader import dp
from .throttling import ThrottlingMiddleware
# from .check_registr import DbMan


def setup(dp):
    dp.middleware.setup(ThrottlingMiddleware())
