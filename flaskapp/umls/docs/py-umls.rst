py-umls package
===============

This package contains three modules with classes useful for dealing with **RxNorm**, then a module each for UMLS and SNOMED handling.


rxnorm
------

Provides classes that deal with RxNorm. This is very much WiP!

.. automodule:: rxnorm
    :members:
    :undoc-members:
    :show-inheritance:

rxnorm_link
-----------

A script used to create JSON documents from most RxNorm concepts and store them into a NoSQL database. This is very much WiP!

.. automodule:: rxnorm_link
    :members:
    :undoc-members:
    :show-inheritance:

rxnorm_graph
------------

A useful script to help visualize relationships between RxNorm concepts, starting from a given RXCUI.
Just run this script in your command line and follow the leader.

.. automodule:: rxnorm_graph
    :members:
    :undoc-members:
    :show-inheritance:

umls
----

Module to deal with UMLS lexica.

.. automodule:: umls
    :members:
    :undoc-members:
    :show-inheritance:

snomed
------

Module to deal with the SNOMED terminology.

.. automodule:: snomed
    :members:
    :undoc-members:
    :show-inheritance:

graphable
---------

Provides classes that can be used to create an interdependency graph.

.. automodule:: graphable
    :members:
    :undoc-members:
    :show-inheritance:

sqlite
------

Our SQLite connection class.

.. automodule:: sqlite
    :members:
    :undoc-members:
    :show-inheritance:

