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

Multiple models for one model ID in the ``content_blobs``
=========================================================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - check file type
    - check for validity in middleware/MaSyMoS

Batch/Bulk-import/reset is forced by SEEK
=========================================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - other options
        - ❌ B: PULL by middleware → MaSyMoS can reset database; create a trigger to start the procedure from outside/SEEK
            - SEEK is leading, MaSyMoS makes no decisions

Connection Middleware - MaSyMoS
###############################

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

Response on INSERT directly after inserting the model; Response on Batch/Bulk-import/reset after annotation runner finished
===========================================================================================================================
- Decision made on 17.09.2020 by RH, BW
- Description
    - after an INSERT, the middleware returns SUCCESS to the caller, then the ``create_annotation_index`` job is triggered
    - when starting a Batch/Bulk-import/reset, the Response is sent after the ``create_annotation_index`` job
        - because the database is not usable for SEEK until this job has finished