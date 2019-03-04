#!/bin/sh
#
# This file is part of twikiget.
# Copyright (C) 2019 CERN.
#
# twikiget is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

isort -rc -c -df **/*.py && \
# check-manifest --ignore ".travis-*" && \
# sphinx-build -qnNW docs docs/_build/html && \
python setup.py test
# sphinx-build -qnNW -b doctest docs docs/_build/doctest
