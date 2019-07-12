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
    $ twikiget archive https://twiki.cern.ch/twiki/bin/view/Main/ZhuTopAnalysis
    $ ls
    ZhuTopAnalysis.warc cache
    $ # once the twiki is archived we can list it's contents:
    $ twikiget list ZhuTopAnalysis.warc
    $ ...
    $ # we can also view the raw content of each file:
    $ twikiget view ZhuTopAnalysis.warc https://twiki.cern.ch/twiki/bin/view/Main/ZhuTopAnalysis
    $ ...

CLI API
----------

.. click:: twikiget.cli:archive
   :prog: archive
   :show-nested:

.. click:: twikiget.cli:list
   :prog: list
   :show-nested:

.. click:: twikiget.cli:view
   :prog: view
   :show-nested:
