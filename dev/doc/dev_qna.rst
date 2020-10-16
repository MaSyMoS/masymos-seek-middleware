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

MaSyMoS Morre
#############

Supported Model Types: SBML, CELLML, SEDML
==========================================
- Answered on 30.09.2020 by RH
- Description
    - SBML < Level 3, namespaces:
        - ``http://www.sbml.org/sbml/level1/*``
        - ``http://www.sbml.org/sbml/level2/*``
        - SBML versions have no big impact
    - SEDML < Level 1 Version 3
    - CELLML <= Version 1.1

Check of the SEEK Model data - numbers
######################################

The small python scripts for reproduction `can be found here <https://github.com/BradleyScrim/seek_model_investigator>`__.

Results (30.09.2020 fairdomhub.org)
===================================

* Counters: Versions by namespace for "valid MIME" ``('application/sbml+xml', 'application/xml', 'text/xml')``

    .. code-block:: text

        'http://www.sbml.org/sbml/level2/version4'       →    71
        'http://www.sbml.org/sbml/level3/version1/core'  →    40
        'http://www.sbml.org/sbml/level2'                →    17
        'http://www.copasi.org/static/schema'            →    13
        'http://www.sbml.org/sbml/level2/version3'       →    13
        'http://sbgn.org/libsbgn/pd/0.1'                 →    5
        'http://www.sbml.org/sbml/level2/version2'       →    1

- Counters: Metadata from json

    .. code-block:: text

        Number of public models: 334
        Number of models with fairdomhub.org-content in link-field: 333
        Number of models with non-fairdomhub.org-content in link-field: 0
        Number of models without fairdomhub.org-content in any link-field: 0
        Number of models without content_blobs: 1
        Number of models with valid MIME¹: 187
        Number of models with maybe MIME¹: 0
        Number of models with invalid MIME¹: 146
        Number of models with more then one MIME-valid content: 6: ['225', '231', '269', '325', '326', '734']
        Number of MIME-valid models (usable by MaSyMoS): 187

        ¹MIME-overview:
        - valid MIME: ('application/sbml+xml', 'application/xml', 'text/xml')
        - maybe MIME: ()
        - invalid MIME: ('namespace', 'application/gzip', 'application/json', 'application/mathematica', 'application/matlab', 'application/octet-stream', 'application/pdf', 'application/x-compressed-tar', 'application/x-rar', 'application/x-ruby', 'application/x-tar', 'application/xhtml+xml', 'application/zip', 'image/png', 'text/html', 'text/plain', 'text/x-python', 'text/x-uuencode', 'text/nlogo')

* All Mime Types

    .. code-block:: text

        application/gzip
        application/json
        application/mathematica
        application/matlab
        application/octet-stream
        application/pdf
        application/sbml+xml
        application/x-compressed-tar
        application/xhtml+xml
        application/xml
        application/x-rar
        application/x-ruby
        application/x-tar
        application/zip
        image/png
        text/html
        text/nlogo
        text/plain
        text/xml
        text/x-python
        text/x-uuencode
