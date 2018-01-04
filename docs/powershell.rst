Powershell
==========

My most used or useful powershell commands.

Stop/stop sql server
--------------------

The server Metrel for example::

    $ net start|stop 'SQL Server (ELLESMERE)'
    $ net start|stop 'SQL Server (METREL)'

Stop/stop postgresql server
---------------------------

The server Ellesmere for example::

    $ net start|stop 'SQL Server (ELLESMERE)'

Grepping the powershell way
---------------------------

In current directory::

    $ ls * -filter *.py | sls 'string to search'

Recursively::

    $ ls * -r -filter *.py | sls 'string to search'


