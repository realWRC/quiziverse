Running the Application
=============================

The Quiziverse application is built using Python with the Flask framework. It was developed with Python 3.12, so any system with a modern Python 3 interpreter should work. The application also uses MongoDB as its database. This tutorial assumes you have a running instance of MongoDB Community Edition on your machine. If you do not yet have MongoDB installed, please follow the instructions on the `MongoDB website <https://www.mongodb.com/>`_.

Follow the steps below to install and run the application.

1. Installing Python
---------------------

First, ensure that you have a modern version of Python 3 installed. Download it from the `official Python website <https://www.python.org/downloads/>`_. On many Linux distributions, Python is pre-installed.

After installing, open your terminal (or command prompt) and type:

.. code-block:: bash

   $ python3
   Python 3.12.4 (main, Dec 18 2024, 07:20:02) [GCC 9.4.0] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> exit()

2. Cloning the github repository
---------------------------------
Clone the quiziverse repository (Assuming you already have git installed) anywhere on your local machine using the following command:

.. code-block:: bash

   $ git clone https://github.com/realWRC/quiziverse.git

3. Configuring Your Virtual Environment
----------------------------------------

Create a virtual environment to manage the dependencies for the application. In this tutorial, we use Python’s built-in :program:`venv` module. Execute the following command in your project directory:

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

4. Installing Dependencies
---------------------------

Install the application's dependencies using pip. All required packages are listed in the ``requirements.txt`` file:

.. code-block:: bash

   $ pip install -r requirements.txt

5. Starting the Flask Server
-----------------------------

With your environment set up and dependencies installed, you can now start the Flask server. Run the following command:

.. code-block:: bash

   $ python -m api.app

> **Note:** On some Linux systems, you may need to use ``python3`` instead of ``python``:

.. code-block:: bash

   $ python3 -m api.app

If everything is configured correctly, the Flask server will start, and you can begin registering for the Quiziverse application.

6. Generating Fake Data (Optional)
----------------------------------

To generate fake data for testing, use the ``generator.py`` script located in the ``generator`` directory. Run the following command:

.. code-block:: bash

   $ python generator/generator.py

This script will create:
- **6 users**
- **300 quizzes**
- **300 results**

You can read the docstrings in the generator.py file for more details.

.. note::
   Ensure that your MongoDB instance is running before generating fake data.

Congratulations! You have now set up the Quiziverse application.
