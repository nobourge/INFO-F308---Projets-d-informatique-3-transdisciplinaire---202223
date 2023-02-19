import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from contextlib import contextmanager
from contextvars import ContextVar

_PROGRESSBAR_VAR = ContextVar[tqdm.tqdm]("_PROGRESSBAR_VAR")

@contextmanager
def progress_bar(*args, **kwargs):
    with logging_redirect_tqdm():
        ctx_token = None
        try:
            _bar = tqdm.tqdm(*args, **kwargs)
            ctx_token = _PROGRESSBAR_VAR.set(_bar)
            yield _bar
        finally:
            _PROGRESSBAR_VAR.reset(ctx_token)
            _bar.close()

from loguru import logger

def update_bar(i):
    _bar = _PROGRESSBAR_VAR.get(None)
    if _bar is not None:
        _bar.update(i)
