Project Overview
================

Table of Contents
-----------------
1. `Project Description <#project-description>`_
2. `Running the Application <#running-the-application>`_
3. `Documentation <#documentation>`_
4. `Contributing <#contributing>`_
5. `License <#license>`_


Project Description
----------------
.. _project-description:

Quiziverse is a dynamic and interactive web application designed to simplify the process of creating, managing, and participating in quizzes. Its intuitive user interface enables users to create quizzes effortlessly and take part in them with ease. For developers, Quiziverse offers a robust backend API, allowing seamless integration of quizzes into their own applications.

**Key Features:**

- User-friendly quiz creation and participation.
- Backend API for integration into external applications (refer to our `RESTful API routes documentation <https://realwrc.github.io/quiziverse/api.blueprints.html#restful-api-routes>`_).
- Flexibility in customizing scoring and time limits.

To set up and run the application, follow the tutorial below. For more technical details about the architecture and inner workings of Quiziverse, explore our comprehensive `documentation <https://realwrc.github.io/quiziverse/index.html>`_.


Running the Application
-----------------------
.. _running-the-application:

The Quiziverse application is built using Python with the Flask framework. It was developed with Python 3.12, so any system with a modern Python 3 interpreter should work. The application also uses MongoDB as its database. This tutorial assumes you have a running instance of MongoDB Community Edition on your machine. If you do not yet have MongoDB installed, please follow the instructions on the `MongoDB website <https://www.mongodb.com/>`_.

Follow the steps below to install and run the application.

1. Installing Python
~~~~~~~~~~~~~~~~~~~~
.. _1-installing-python:

First, ensure that you have a modern version of Python 3 installed. Download it from the `official Python website <https://www.python.org/downloads/>`_. On many Linux distributions, Python is pre-installed.

To verify your installation, open your terminal (or PowerShell) and type:

**On Linux/macOS:**

.. code-block:: bash

   $ python3
   Python 3.12.4 (main, Dec 18 2024, 07:20:02) [GCC 9.4.0] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> exit()

**On Windows (PowerShell):**

.. code-block:: powershell

   PS C:\> python
   Python 3.12.4 (tags/v3.12.4:8e8a4ba, Jun  6 2024, 19:30:16) [MSC v.1940 64 bit (AMD64)] on win32
   Type "help", "copyright", "credits" or "license" for more information.
   >>> exit()

2. Configuring Your Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. _2-configuring-your-virtual-environment:

Create a virtual environment to manage the dependencies for the application. In this tutorial, we use Python’s ``venv`` module. Execute the following command in your project directory:

.. code-block:: bash

   $ python -m venv .venv

Next, activate the virtual environment:

- **On Linux/macOS:**

  .. code-block:: bash

     $ source .venv/bin/activate

- **On Windows (PowerShell):**

  .. code-block:: powershell

     > .venv\Scripts\activate

After activating the environment, set an environment variable called ``SECRET`` for cryptographic operations.

- **On Linux/macOS:**

  .. code-block:: bash

     $ export SECRET="your_secret_key"

- **On Windows (PowerShell):**

  .. code-block:: powershell

     > $Env:SECRET = "your_secret_key"

3. Installing Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. _3-installing-dependencies:

Install the application's dependencies using ``pip``. All required packages are listed in the ``requirements.txt`` file:

.. code-block:: bash

   $ pip install -r requirements.txt

4. Starting the Flask Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. _4-starting-the-flask-server:

With your environment set up and dependencies installed, you can now start the Flask server. Run the following command:

.. code-block:: bash

   $ python -m api.app

**Note:** On some Linux systems, you may need to use ``python3`` instead of ``python``:

.. code-block:: bash

   $ python3 -m api.app

If everything is configured correctly, the Flask server will start, and you can begin registering for the Quiziverse application.

5. Generating Fake Data (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. _5-generating-fake-data-optional:

To populate the database with test data, use the ``generator.py`` script located in the ``generator`` directory.

.. code-block:: bash

   $ python -m generator.generator

This script will create:
- **6 users**
- **300 quizzes**
- **300 results**

**Note:** Ensure that your MongoDB instance is running before executing this script.


Congratulations! You have now set up the Quiziverse application. You can register, log in, and have some fun.

Documentation
-------------
.. _documentation:

For more detailed information, visit the official `Quiziverse documentation <https://realwrc.github.io/quiziverse/index.html>`_.

Contributing
------------
.. _contributing:

If you wish to contribute, please fork the `repository <https://github.com/realWRC/quiziverse>`_, make your changes, and submit a pull request.

License
-------
.. _license:

Quiziverse is released under the MIT License. See the ``LICENSE`` file in our `repository <https://github.com/realWRC/quiziverse>`_ for more details.
