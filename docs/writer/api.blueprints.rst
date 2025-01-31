Application routes
==================
These routes are used by the application and can only be accessed through
the quiziverse frontend. Most of the routes require the user to be logged
in and enforce authentication.

Blueprint for answering quizzes (answering\_quiz.py)
----------------------------------------------------

.. automodule:: api.blueprints.answering_quiz
   :members:
   :undoc-members:
   :show-inheritance:


Blueprint for authentication routes (authentication.py)
-------------------------------------------------------

.. automodule:: api.blueprints.authentication
   :members:
   :undoc-members:
   :show-inheritance:

Blueprint for dashboard routes (dashboard.py)
---------------------------------------------

.. automodule:: api.blueprints.dashboard
   :members:
   :undoc-members:
   :show-inheritance:

Blueprint for information routes (information.py)
-------------------------------------------------

.. automodule:: api.blueprints.information
   :members:
   :undoc-members:
   :show-inheritance:

Blueprint for creating and editing quizzes (quiz\_routes.py)
------------------------------------------------------------

.. automodule:: api.blueprints.quiz_routes
   :members:
   :undoc-members:
   :show-inheritance:

Blueprint for interacting with results (resultsblueprint.py)
------------------------------------------------------------

.. automodule:: api.blueprints.resultsblueprint
   :members:
   :undoc-members:
   :show-inheritance:

RESTful API routes
==================
These routes can be used to obtain data from the quiziverse API. The route
retian any session state. The route does not require authentication as of
not but my be included in the future.

Blueprint for RESTful routes (apiroutes.py)
-------------------------------------------

.. automodule:: api.blueprints.apiroutes
   :members:
   :undoc-members:
   :show-inheritance:
