Queue prevent duplicate jobs
++++++++++++++++++++++++++++


This module simply avoids the creation of a job, if there's already one executing the same function with absolutely the
equal parameters and it's state isn't in `Started` or `Done`.


Default behaviour of Job Queue
------------------------------

The default implementation doesn't identifies and eliminates duplicate pending jobs in the queue. So it is
possible that there are multiple jobs in the queue, which does eventually the same action e.g. exporting a product.


.. image:: /queue_job_prevent_duplicates/static/description/example_queue_before.png
   :alt: Without Queue job prevent duplicates installed
   :width: 100%


After installation
------------------

Everytime a job will be created but there is already at least one job executing the same function and hasn't state
`Done` or `Started`, the job creation will be aborted. Instead a log information will be created.


.. image:: /queue_job_prevent_duplicates/static/description/example_queue_after.png
   :alt: After installation duplicate job creation will be prevented
   :width: 100%


Log prevented job-creation
--------------------------

If the creation of a duplicate job was prevented, a log information will be created (see below):

.. code-block::

    2017-12-11 08:02:51,770 10505 INFO v10_connector_db odoo.addons.sewi_queue_job_prevent_duplicates.models.queue_job: A job already exists for domain [('state', 'not in', ['started', 'done']), ('func_string', '=', 'sewi.shopware.synchronizer(6,)._import_all_records(only_new=True)')]
    2017-12-11 08:02:51,775 10505 INFO v10_connector_db odoo.addons.sewi_queue_job_prevent_duplicates.models.queue_job: A job already exists for domain [('state', 'not in', ['started', 'done']), ('func_string', '=', 'sewi.shopware.synchronizer(7,)._import_all_records(only_new=True)')]


Know Issues
-----------

It can be expected, that it's possible when a record is modified but a job creation was prevented, because in this
cursors context was a pending job which does already the same action, but until the modifying cursor has
committed the record changes, the other job was already executed in a parallel thread / process. This will
lead to different versions of the record in both systems.


