#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of twikiget.
# Copyright (C) 2019 CERN.
#
# twikiget is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
import sys

import click
import tablib
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from warcio.archiveiterator import ArchiveIterator


@click.group()
def twikiget():
    pass


@twikiget.command()
@click.option('--wget-options',
              default='',
              help='additional options to pass to wget')
@click.option('-o', '--out-warc-file',
              help='output file name for a WARC file')
@click.option('-P', '--directory-prefix',
              help='output folder for raw files')
@click.argument('url')
def archive(url, wget_options, out_warc_file, directory_prefix):
    """ Archive a TWiki page with attachments into a WARC archive.

    Raw archived files are also saved to a directory specified in
    `directory-prefix` option (default=./cache).

    Options passed in `wget-options` will overwrite the twikiget defaults,
     and should be used with caution.
    """
    site_path = url.split('/bin/view/')[-1]
    directory_prefix = directory_prefix or '/'.join(('./cache', site_path))
    if wget_options != '':
        wget_options = wget_options + ' '
    if not os.path.exists(directory_prefix):
        os.makedirs(directory_prefix)

    include = ','.join(['/twiki/pub/' + site_path,
                        '/twiki/pub/TWiki/',
                        '/twiki/pub/Main/',
                        '/twiki/bin/view/Main/'])

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


@twikiget.command('list')
@click.option(
    '--json',
    'output_format',
    flag_value='json',
    default=None,
    help='Get output in JSON format.')
@click.option(
    '--content-type',
    'filter_content_type',
    default='',
    help='Filter files in an archive by content_type. '
         'It can be either full version or just a begging of type name')
@click.argument('warc_file')
def list(warc_file, output_format, filter_content_type):
    """ List files in the WARC archive.

    The list can be filtered by the HTTP Content Type,
     and exported as json if needed.\n
    Note that `content-type` option can be a full name of a type
     or, to search broader, just the first part of it
     e.g. `text/css` and `text`

    Examples::

        $ twikiget list ExampleTwiki.warc \n
        $ twikiget list ExampleTwiki.warc --content-type=text/html \n
        $ twikiget list ExampleTwiki.warc --content-type=text \n
        $ twikiget list ExampleTwiki.warc --json \n
    """
    tablib_data = tablib.Dataset()
    tablib_data.headers = ['uri', 'title', 'content_type']
    with open(warc_file, 'rb') as fh:
        for r in ArchiveIterator(fh):
            if (r.rec_type == 'response' and
                    r.http_headers.get_statuscode().startswith('2')):
                title = None
                content_type = r.http_headers.get_header('content-type')
                uri = r.rec_headers.get_header('warc-target-uri')
                # print(r.http_headers)
                if content_type is None:
                    content_type = 'application/octet-stream'
                if content_type.lower().startswith(filter_content_type):
                    if content_type.lower().startswith('text/html'):
                        payload = r.content_stream().read()
                        title = BeautifulSoup(
                            payload, 'html.parser').find('title').getText()
                    tablib_data.append(
                        [str(uri), str(title), str(content_type)])

        if output_format:
            click.echo(tablib_data.export(output_format))
        else:
            table = PrettyTable()
            table.field_names = ['uri', 'title', 'content_type']
            for row in tablib_data:
                table.add_row(row)
            click.echo(table)


@twikiget.command()
@click.argument('warc-file')
@click.argument('file-uri')
def view(warc_file, file_uri):
    """ View raw content of one of the files in the WARC archive.

    View command is usefull to inspect contents of one file from the archive.
    It can be used with a pipe or a stream to view the file in a web-browser or
    other suitable program.
    FILE-URI argument can be copied form the outputs of `twikiget list`.

    Examples::

        $ twikiget view ExampleTwiki.warc https://example.com/twiki?raw=on
        $ twikiget view ExampleTwiki.warc http://example.com/style.css \n
        $ twikiget view ExampleTwiki.warc http://example.com/img.png > img.png

    """
    try:
        with open(warc_file, 'rb') as fh:
            for r in ArchiveIterator(fh):
                if (r.rec_headers.get_header('warc-target-uri') == file_uri and
                        r.http_headers.get_statuscode().startswith('2')):
                    sys.stdout.buffer.write(r.raw_stream.read())
                    return 0
            click.echo(click.style('Specified URI: {} is not in the archive'
                                   .format(file_uri),
                                   fg='red'), err=True)
    except OSError as e:
        click.echo(click.style('Specified file: {} does not exist'
                               .format(warc_file),
                               fg='red'), err=True)
