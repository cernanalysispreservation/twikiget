# This file is part of twikiget.
# Copyright (C) 2019 CERN.
#
# twikiget is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os.path
from shutil import rmtree

from click.testing import CliRunner

from twikiget.cli import archive, list


def test_list_successful():
    runner = CliRunner()
    url = 'https://twiki.cern.ch/twiki/bin/view/Inspire/SystemDesignBibExport'
    warc_filename = url.split("/")[-1] + '.warc'
    raw_download_dir = 'test_download'

    # archive
    download_result = runner.invoke(archive, [url, '-P', raw_download_dir])
    assert download_result.exit_code == 0
    assert os.path.isfile(warc_filename) is True
    assert os.path.exists(raw_download_dir) is True

    # list
    list_result = runner.invoke(list, [warc_filename])
    assert list_result.exit_code == 0
    for table_header in ['uri', 'title', 'content_type']:
        assert table_header in list_result.output

    # clean up
    os.remove(warc_filename)
    rmtree(raw_download_dir)
