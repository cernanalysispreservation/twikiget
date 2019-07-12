# This file is part of twikiget.
# Copyright (C) 2019 CERN.
#
# twikiget is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os.path
from shutil import rmtree

from click.testing import CliRunner

from twikiget.cli import archive


def test_archive_successful():
    runner = CliRunner()
    url = 'https://twiki.cern.ch/twiki/bin/view/Inspire/SystemDesignBibExport'
    warc_filename = url.split("/")[-1] + '.warc'
    raw_download_dir = 'test_download'

    result = runner.invoke(archive, [url, '-P', raw_download_dir])
    assert result.exit_code == 0
    assert os.path.isfile(warc_filename) is True
    assert os.path.exists(raw_download_dir) is True

    # clean up
    os.remove(warc_filename)
    rmtree(raw_download_dir)


def test_attachments_preset():
    runner = CliRunner()
    url = 'https://twiki.cern.ch/twiki/bin/view/Main/ZhuTopAnalysis'
    raw_download_dir = 'test_download'

    result = runner.invoke(archive, [url, '-P', raw_download_dir])
    assert result.exit_code == 0
    attachment = os.path.join(
        raw_download_dir,
        'twiki.cern.ch/twiki/pub/Main/ZhuTopAnalysis',
        'SlimCuts_leptonMoreThan0_jetsMoreThan3.txt'
    )
    assert os.path.isfile(attachment) is True

    # clean up
    rmtree(raw_download_dir)
