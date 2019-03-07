.. _gettingstarted:

User Guide
===============

Install twikiget
--------------------

If you are interested in archiving twikis using twikiget,
all you need to install is the ``twikiget``, ideally in a new virtual
environment:

.. code-block:: console

   $ # create new virtual environment
   $ virtualenv ~/.virtualenvs/twikiget
   $ source ~/.virtualenvs/twikiget/bin/activate
   $ # install twikiget
   $ pip install twikiget

Basic usage
--------------

.. code-block:: console

    $ # download twiki
    $ twikiget https://twiki.cern.ch/twiki/bin/view/Main/ZhuTopAnalysis
    $ # list downloaded files
    $ ls
    ZhuTopAnalysis.warc cache

CLI API
----------

.. click:: twikiget.cli:wget_warc
   :prog: twikiget
   :show-nested:
