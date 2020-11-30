.. _dev_decisions:

*********************
Development Decisions
*********************

.. include:: rst_directives.rst

.. contents:: 
    :local:

Changes in SEEK
###############

Connecting SEEK - MaSyMoS Morre
===============================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - RH wrote code in 2016(±) - maybe parts of it could still work
    - visual: insert third blue source button
    - decide later: add as "external" search?

Changes in MaSyMoS Morre
########################

Reference Model via SEEK-ID
===========================
- Decision made on 17.09.2020 by RH, BW
- Description
    - in the MaSyMoS-database inside the document root is the following meta data
        - ``filename`` original filename
		- ``uid`` - generated unique Morre-ID
		- ``uri`` - internal URI
		- ``version_id`` - internal version
		- ``version`` - used by dokument (i.e. sbml)
		- ``level`` - used by dokument (i.e. sbml)
    - the used ID (URL to model.content) is stored in ``uri`` - this is the main ID
    - the used model-version is stored in ``version_id``
- impact
    - Morre needs a function to find model.contents by ``uri`` (i.e. ``https://fairdomhub.org/models/196/content_blobs/8745``)
    - Morre needs a function to find model.contents by short ``uri`` with only the model id for DELETE and UPDATE (i.e. ``https://fairdomhub.org/models/196``)

General Concept Middleware
##########################

SEEK is the leading project
===========================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - SEEK pushes to middleware (i.e. hook)
    - the middleware will not do things autonomous

MaSyMoS indexes only the latest version
=======================================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - for now MaSyMoS has no versioning of the models in relation with SEEK

Middleware and MaSyMoS-Morre will not unpack archives
=====================================================
- Decision made on 17.09.2020 by RH, BW
- Description
    - models packed in archives cannot be added

Allowed Content MIME Types
==========================
- Decision made on 18.09.2020 by RH, BW
- Description
    - ``application/sbml+xml``
    - ``application/xml``
    - ``text/xml``

Checks in MaSeMiWa before sending anything to MaSyMoS Morre
===========================================================
- Decision made on 19.10.2020 by RH, BW
- Description
    #. MIME (from JSON-Metadata)
    #. namespace, level, version (from file)
        - if level/version in namespace differ from level/version from attributes, ignore file

Connection SEEK - Middleware
############################

What ID to use between SEEK and MaSeMiWa to reference a Model?
==============================================================
- Decision made on 16.09.2020 by SO, RH, BW
- Description
    - use the full URL
    - optional ``.json``
    - ignore ``?version=*``
    - i.e. ``https://fairdomhub.org/models/196.json``, ``https://fairdomhub.org/models/196``, ``https://fairdomhub.org/models/196.json?version=3``

Restricted access rights for the middleware
===========================================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - middleware uses public API → only public models are used
    - SEEK needs another hook: when model-visibility is switched to private → delete model in MaSyMoS

Get data on activation of hook in seek pushing to the Middleware
================================================================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - question was: WHEN to get data
    - other options
        - ❌ B: cron job - request a list of all ID, optional filtered by timestamp every x minutes
            - feels bad and brings some unpredictable behaviour

call Seek API to get all necessary data
=======================================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - question was, HOW to get data for id 

Multiple contents for one model ID in the ``content_blobs``
===========================================================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - check file type
    - check for validity in middleware/MaSyMoS
    - import all valid contents

Batch/Bulk-import/reset is forced by SEEK
=========================================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - other options
        - ❌ B: PULL by middleware → MaSyMoS can reset database; create a trigger to start the procedure from outside/SEEK
            - SEEK is leading, MaSyMoS makes no decisions

Connection Middleware - MaSyMoS
###############################

What ID to use between MaSeMiWa and MaSyMoS Morre to reference a Content?
=========================================================================
- Decision made on 24.09.2020 by RH, BW
- Description
    - one SEEK model can have several valid entries inside the ``content_blobs`` field
    - to have all these entries inside Morre, we use the full URL to the Blobs instead the link to the model, i.e. ``https://fairdomhub.org/models/196/content_blobs/8745``
    - if any user uploaded an external linked model (with the external url in the ``content_blob``-field ``url``), the field ``link`` will also reference that file as a copy from the time the model was created
    - the SEEK model ID is included; it's human readable

Deleting a model will not delete any annotations
================================================
- Decision made on 17.09.2020 by RH, BW
- Description
    - deleting annotations can lead to unexpected behaviour

Annotation-Scanning in the background
=====================================
- Decision made on 17.09.2020 by RH, BW
- Description
    - getting all Annotations for all models can be difficult because this is highly depending on the network and the servers with the data
    - the middleware run automatically once or twice a day the ``create_annotation_index`` job

Response on INSERT an Batch/Bulk-import/reset after Check
=========================================================
- Decision made on 20.10.2020 by RH, BW
- Description
    - after checking the import-request and adding valid models to the Queue, MaSeMiWa will response with 200 - SUCCESS
    - if there is nothing to import, the return code will differ
