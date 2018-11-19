.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
	:target: http://www.gnu.org/licenses/agpl
	:alt: License: AGPL-3

==================
Check Lot End Life
==================

Check lots end life date to avoid being exceeded by its contained products in incoming pickings.


Installation
============

Just install.


Configuration
=============

Set products tracking by serial number or lots and set a product life time. Then create lots for those products and set an end of life date.


Usage
=====

When creating an incoming picking, choose products which are trackable by serial number or lots and set lots for them. When trying to validate, the lot end of life date will be checked in order to ensure it is not exceeded by its product life time. If (Today Date + Product Life Time > Lot End Life Date) an error will appear.


ROADMAP
=======

[ Enumerate known caveats and future potential improvements.
  It is mostly intended for end-users, and can also help
  potential new contributors discovering new features to implement. ]

* ...


Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/QubiQ/qu-stock-logistics-workflow/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/QubiQ/qu-stock-logistics-workflow/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.


Credits
=======

Authors
~~~~~~~

* QubiQ, Odoo Community Association (OCA)


Contributors
~~~~~~~~~~~~

* Xavier Piernas <xavier.piernas@qubiq.es>
* Valentín Vinagre <valentin.vinagre@qubiq.es>


Maintainer
~~~~~~~~~~

This module is maintained by QubiQ.

.. image:: https://pbs.twimg.com/profile_images/702799639855157248/ujffk9GL_200x200.png
   :alt: QubiQ
   :target: https://www.qubiq.es

This module is part of the `QubiQ/qu-stock-logistics-workflow <https://github.com/QubiQ/qu-stock-logistics-workflow>`_.

To contribute to this module, please visit https://github.com/QubiQ.
