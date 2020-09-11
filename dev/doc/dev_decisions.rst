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

Bulk-import/reset is forced by SEEK
===================================
- Decision made on 03.09.2020 by SO, RH, BW
- Description
    - other options
        - ❌ B: PULL by middleware → MaSyMoS can reset database; create a trigger to start the procedure from outside/SEEK
            - SEEK is leading, MaSyMoS makes no decisions

Connection Middleware - MaSyMoS
###############################