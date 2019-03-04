# -*- coding: utf-8 -*-
#
# This file is part of twikiget.
# Copyright (C) 2019 CERN.
#
# twikiget is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""twikiget version test."""


def test_version():
    """Test version import."""
    from twikiget import __version__
    assert __version__
