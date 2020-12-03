.. _usage:

*****
Usage
*****

.. include:: rst_directives.rst

.. contents:: 
    :local:

INSERT single entry
###################
- POST-request to ``/insert``
- define link in field ``link``
- example with curl: :c_bash:`curl -X POST http://localhost:5000/insert -H "Content-Type: application/json" -d '{"link":"https://fairdomhub.org/models/24.json?version=3"}'`
- return codes
    - ``200`` success - something was added to Morre-Insert-Queue
    - ``204`` success - data checked successfully, nothing added to Morre-Queue
    - ``404`` unable to get metadata for this link (cannot connect to SEEK)
    - ``405`` malformed request
    - ``502`` unable to download at least one of the content_blob files (cannot connect to server)

UPDATE entry
############
- POST-request to ``/update``
- define link in field ``link``
- example with curl: :c_bash:`curl -X POST http://localhost:5000/update -H "Content-Type: application/json" -d '{"link":"https://fairdomhub.org/models/24.json?version=3"}'`
- return codes
    - .. Note:: TODO error codes
    
DELETE entry
############
- POST-request to ``/delete``
- define link in field ``link``
- example with curl: :c_bash:`curl -X POST http://localhost:5000/delete -H "Content-Type: application/json" -d '{"link":"https://fairdomhub.org/models/24.json?version=3"}'`
- return codes
    - ``200`` success - something was added to Morre-Delete-Queue
    - ``404`` unable to get metadata for this link (cannot connect to SEEK)
    - ``405`` malformed request
    - ``502`` unable to download at least one of the content_blob files (cannot connect to server)

BATCH-INSERT
############
- POST-request to ``/batch``
- define link list in field ``links``
- example with curl: :c_bash:`curl -X POST http://localhost:5000/batch -H "Content-Type: application/json" -d '{"links":["https://fairdomhub.org/models/24.json?version=3", "https://fairdomhub.org/models/23", "https://fairdomhub.org/models/42.json"]}'`
- return codes
    - .. Note:: TODO error codes


