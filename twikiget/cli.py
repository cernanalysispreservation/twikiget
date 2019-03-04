#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of twikiget.
# Copyright (C) 2019 CERN.
#
# twikiget is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os

import click


@click.command()
@click.option('--options', default=('-p', '-k'),
              help='additional options to pass to wget')
@click.option('-o', '--out-warc-file',
              help='output file name for a warc file')
@click.option('-P', '--directory-prefix',
              help='output folder for raw files')
@click.argument('url')
def wget_warc(url, options, out_warc_file, directory_prefix):
    """ Downloading a page with attachments to a catalog
     and into a warc file """
    site_path = url.split('/bin/view/')[-1]
    options_string = ' '.join(options)
    directory_prefix = directory_prefix or '/'.join(('./cache', site_path))
    if not os.path.exists(directory_prefix):
        os.makedirs(directory_prefix)

    out_warc_file = out_warc_file or site_path.split('/')[-1]

    os.system('wget {opt} "{url}"'
              ' --warc-file="{out_warc_file}" '
              '--no-warc-compression '
              '-P {directory_prefix}'
              .format(url=url,
                      opt=options_string,
                      out_warc_file=out_warc_file,
                      directory_prefix=directory_prefix)
              )
