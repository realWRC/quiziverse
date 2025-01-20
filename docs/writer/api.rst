API Documentation
=================

app
---

.. automodule:: api.app
   :members:
   :undoc-members:
   :show-inheritance:

config
------

.. automodule:: api.config
   :members:
   :undoc-members:
   :show-inheritance:

.. code-block:: python

   app.config['SESSION_PERMANENT'] = False
   app.config['SESSION_USE_SIGNER'] = True
   app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
   app.config['SESSION_TYPE'] = 'mongodb'
   app.config['SESSION_MONGODB'] = client
   app.config['SESSION_MONGODB_DB'] = 'quiziverse'
   app.config['SESSION_MONGODB_COLLECTION'] = 'sessions'

blueprints
----------
The blueprints defined in this submodule include all routes that allow the application
to function as intended. The route for exposed quizzes can are all in the apiroutes
blueprint.

.. toctree::
   :maxdepth: 2

   api.blueprints
