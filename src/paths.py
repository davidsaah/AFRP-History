# -*- coding: utf-8 -*-
"""One place that knows where things are, so the build runs from any checkout.

Override the repository root with the AFRP_ROOT environment variable if you keep
the sources and the outputs apart.
"""
import os

ROOT = os.environ.get('AFRP_ROOT') or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
SRC = os.path.join(ROOT, 'src')
OUTDIR = os.path.join(ROOT, 'out')
ASSETS = os.path.join(ROOT, 'assets')
DATA = os.path.join(ROOT, 'data')

os.makedirs(OUTDIR, exist_ok=True)


def out(name):
    return os.path.join(OUTDIR, name)


def asset(*parts):
    return os.path.join(ASSETS, *parts)


def data(name):
    return os.path.join(DATA, name)
