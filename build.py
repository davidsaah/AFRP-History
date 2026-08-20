#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the book.

    python build.py

Writes out/AFRP_The_One_Line_v5.html and its two companion documents. The build
is deterministic: same sources in, byte-identical HTML out.
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'src'))
runpy.run_path(os.path.join(HERE, 'src', 'build_v5.py'), run_name='__main__')
