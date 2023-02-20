import typing as t
from contextlib import contextmanager
from contextvars import ContextVar

import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

_PROGRESSBARS: t.MutableMapping[str, tqdm.tqdm] = {}

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


def create_pb(__name: str, *args, **kwargs):
    global _PROGRESSBARS
    if __name in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' already exists !")

    _PROGRESSBARS[__name] = tqdm.tqdm(*args, **kwargs)
    return _PROGRESSBARS[__name]


def set_pb_desc(__name: str, desc: str):
    global _PROGRESSBARS
    if __name not in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' does not exists !")

    return _PROGRESSBARS[__name].set_description(desc)


def refresh_pb(__name: str):
    global _PROGRESSBARS
    if __name not in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' does not exists !")

    return _PROGRESSBARS[__name].refresh()


def update_pb(__name: str, i: int = 1):
    global _PROGRESSBARS
    if __name not in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' does not exists !")

    return _PROGRESSBARS[__name].update(i)


def reset_pb(__name: str, new_total: int = None):
    global _PROGRESSBARS
    if __name not in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' does not exists !")

    return _PROGRESSBARS[__name].reset(new_total)


def close_pb(__name: str):
    global _PROGRESSBARS
    if __name not in _PROGRESSBARS:
        raise RuntimeError(f"Progress bar '{__name}' does not exists !")

    return _PROGRESSBARS[__name].close()


def close_all_pb():
    for value in _PROGRESSBARS.values():
        value.close()
