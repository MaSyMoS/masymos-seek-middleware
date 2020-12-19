.. _use_configure:

*********
Configure
*********

.. include:: rst_directives.rst

.. contents:: 
    :local:

Configuration and Log Configuration
###################################

- the configuration file is expected in ``/opt/config/masemiwa_config.cfg`` (as defined in the Dockerfile)
- the path for the log configuration can be set in the configuration with the field ``LOG_CONFIGURATION``; the default is ``/opt/config/masemiwa_log.cfg``
- if there is no configuration file/log configuration file or an empty file, MaSeMiWa will create such a file with the default values on startup -so you can reset any misconfigured file by deleting it

Troubleshooting
###############

ConfigurationFileException: the configuration file defines an unknown key 'X'; known keys: Y
============================================================================================
- a problem with your **configuration file**
- check the **name** of key *X*, it must be one of the list provided in *Y* (case-insensitive)
- if nothing helps. reset the log configuration by deleting the file

ConfigurationFileException: value of X cannot be converted to type Y
====================================================================
- a problem with your **configuration file**
- check the **value** of key *X*, MaSeMiWa cannot parse it to the right type (*Y*)
- if nothing helps. reset the log configuration by deleting the file

configparser.ParsingError: Source contains parsing errors: '/opt/config/masemiwa_log.cfg'
=========================================================================================
- there is some problem with your **logger configuration**
- please read the error message carefully and `maybe check the docs <https://docs.python.org/3/library/logging.config.html#configuration-file-format>`__
- if nothing helps. reset the log configuration by deleting the file

PermissionError: [Errno 13] Permission denied: '/opt/…
======================================================
- MaSeMiWa has no rights to
    - read/write the configuration files
    - or write to the log file
- please check permissions for the file and the parent folders
    - remember to check this on your machine when mapping the log and config folder to the docker container
    - see docker configuration for the instructions: :ref:`use_docker`