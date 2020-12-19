.. _use_usage:

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
- example with curl: :c_bash:`curl -v POST http://localhost:4242/insert -H "Content-Type: application/json" -d '{"link":"https://fairdomhub.org/models/24.json?version=3"}'`
- return codes
    - ``200`` success - something was added to Morre-Insert-Queue
    - ``204`` success - data checked successfully, nothing added to Morre-Queue
    - ``404`` unable to get metadata for this link (cannot connect to SEEK)
    - ``405`` malformed request
    - ``500`` a fatal server error occurred
    - ``502`` unable to download at least one of the content_blob files (cannot connect to server)
    - ``503`` something stopped the Morre-Queue-Thread running in MaSeMiWa, check the logs to find the problems. You can restart the Queue with ``/restart_queue``

UPDATE entry
############
- POST-request to ``/update``
- define link in field ``link``
- example with curl: :c_bash:`curl -v POST http://localhost:4242/update -H "Content-Type: application/json" -d '{"link":"https://fairdomhub.org/models/24.json?version=3"}'`
- return codes
    - ``200`` success - something was added to Morre-Update-Queue
    - ``404`` unable to get metadata for this link (cannot connect to SEEK)
    - ``405`` malformed request
    - ``406`` model is invalid and cannot be used - nothing will be done here (no insert, no delete)
    - ``500`` a fatal server error occurred
    - ``502`` unable to download at least one of the content_blob files (cannot connect to server)
    - ``503`` something stopped the Morre-Queue-Thread running in MaSeMiWa, check the logs to find the problems. You can restart the Queue with ``/restart_queue``
    
DELETE entry
############
- POST-request to ``/delete``
- define link in field ``link``
- example with curl: :c_bash:`curl -v POST http://localhost:4242/delete -H "Content-Type: application/json" -d '{"link":"https://fairdomhub.org/models/24.json?version=3"}'`
- return codes
    - ``200`` success - something was added to Morre-Delete-Queue
    - ``404`` unable to get metadata for this link (cannot connect to SEEK)
    - ``405`` malformed request
    - ``500`` a fatal server error occurred
    - ``502`` unable to download at least one of the content_blob files (cannot connect to server)
    - ``503`` something stopped the Morre-Queue-Thread running in MaSeMiWa, check the logs to find the problems. You can restart the Queue with ``/restart_queue``

BATCH-INSERT
############
- POST-request to ``/batch``
- define link list in field ``links``
- example with curl: :c_bash:`curl -v POST http://localhost:4242/batch -H "Content-Type: application/json" -d '{"links":["https://fairdomhub.org/models/24.json?version=3", "https://fairdomhub.org/models/23", "https://fairdomhub.org/models/42.json"]}'`
- Attention: many possible errors are ignored here by MaSeMiWa in the return 
- return codes
    - ``200`` success - something was added to Morre-Insert-Queue
    - ``204`` success - data checked successfully, nothing added to Morre-Queue
    - ``405`` malformed request
    - ``500`` a fatal server error occurred
    - ``503`` something stopped the Morre-Queue-Thread running in MaSeMiWa, check the logs to find the problems. You can restart the Queue with ``/restart_queue``

Restarting the Morre queue
##########################
- POST-request to ``/restart_queue``
- example with curl: :c_bash:`curl -v POST http://localhost:4242/restart_queue`
- return codes
    - ``200`` success

