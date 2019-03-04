# This file is part of twikiget.
# Copyright (C) 2019 CERN.
#
# twikiget is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os.path
from shutil import rmtree

from click.testing import CliRunner

from twikiget.cli import wget_warc


def test_download_successful():
    runner = CliRunner()
    url = 'https://twiki.cern.ch/twiki/bin/view/Main/ZhuTopAnalysis'
    filename = url.split("/")[-1] + '.warc'
    raw_download_dir = 'test_download'

    result = runner.invoke(wget_warc, [url, '-P', raw_download_dir])
    assert result.exit_code == 0
    assert os.path.isfile(filename) is True
    assert os.path.exists(raw_download_dir) is True

    # clean up
    os.remove(filename)
    rmtree(raw_download_dir)
