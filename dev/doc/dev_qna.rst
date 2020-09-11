.. _dev_gna:

*****************
Questions&Answers
*****************

.. include:: rst_directives.rst

.. contents:: 
    :local:

Seek
####

Is the SEEK-ID(json) persistent?
================================
- Answered on 03.09.2020 by SO
    - SEEK-id and version (i.e. https://fairdomhub.org/models/20.json?version=1) is bound to domain name
        - domain change → force recreate DB
    - the uuid is persistent

Are SEEK-ids reused?
====================
- Answered on 03.09.2020 by SO
- question was: Is it in any case possible, that Model Y gets the ID of a deleted Model X? (database reorganisation)
    - no, the ID stays unique, new models get the next free, never before used ID

Working with SEEK-versions
==========================
- Answered on 03.09.2020 by SO
- Has SEEK some kind of active version (use version 2 instead of version 3 as current version)
    - no
- Is it possible to delete versions in SEEK?
    - no
- Versioning is linear, right?
    - yes