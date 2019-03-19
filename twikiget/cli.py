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
@click.option('--wget-options',
              default='',
              help='additional options to pass to wget')
@click.option('-o', '--out-warc-file',
              help='output file name for a warc file')
@click.option('-P', '--directory-prefix',
              help='output folder for raw files')
@click.argument('url')
def wget_warc(url, wget_options, out_warc_file, directory_prefix):
    """ Downloading a page with attachments to a catalog
     and into a warc file """
    site_path = url.split('/bin/view/')[-1]
    directory_prefix = directory_prefix or '/'.join(('./cache', site_path))
    if wget_options != '':
        wget_options = wget_options + ' '
    if not os.path.exists(directory_prefix):
        os.makedirs(directory_prefix)

    include = ','.join(['/twiki/pub/' + site_path,
                        '/twiki/pub/TWiki/',
                        '/twiki/pub/Main/'])

    out_warc_file = out_warc_file or site_path.split('/')[-1]

    os.system('wget '
              '--recursive '
              '--level=1 '
              '--span-hosts '
              '--include {include} '
              '--warc-file="{out_warc_file}" '
              '--no-warc-compression '
              '--convert-links '
              '--adjust-extension '
              '--directory-prefix={directory_prefix} '
              '{opt} '
              '{url}'
              .format(url=url,
                      opt=wget_options,
                      out_warc_file=out_warc_file,
                      directory_prefix=directory_prefix,
                      include=include)
              )
