.. _dev_gna:

*****************
Questions&Answers
*****************

.. include:: rst_directives.rst

.. contents:: 
    :local:

Seek
####

What links are used by the seek-users to link their models?
===========================================================
- Answered on 16.09.2020 by SO
    - there is no restriction on this field, the user can link the model directly or link a website
- impact
    - MaSeMiWa must check the target and try to find the model file in the ``content_blobs`` field

What SEEK-ID in json is persistent?
===================================
- Answered on 03.09.2020 by SO
    - SEEK-id(20) and version(1) (i.e. https://fairdomhub.org/models/20.json?version=1) is bound to domain name
        - domain change → force recreate DB
    - the uuid is persistent per model
- Overview of the if-related fields (`issue <https://github.com/MaSyMoS/masymos-seek-middleware/issues/6>`__)
    - ``data.id``
        - points to the model, ignoring the version (**model id**)
        - i.e. ``24``
    - ``data.meta.uuid``
        - points to the model, ignoring the version (**model uuid**)
        - i.e. ``67bb3ce0-caa7-0138-f7f7-0242ac120004``
    - ``data.links.self``
        - points to the model + version without domain dependency (**model relative link**)
        - i.e. ``/models/24?version=3``
    - ``data.attributes.version``
        - provides the current version number (**model version**)
        - i.e. ``3``
    - ``data.attributes.versions.?.url`` (*? is version number*)
        - provides the model + version with domain dependency (**model absolute link**)
        - i.e. ``https://sandbox2.fairdomhub.org/models/24.json?version=3``

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