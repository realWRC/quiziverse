# QUIZIVERSE

Quiziverse is a web application with a user friendly interface to users to create and answer quizzes. It also provides a backend api for developers to reuse the quizzes in their own application (for more detailed information checkout our RESTful API routes documentation).
Follow the tutorial below  to setup the application and run it for yourself. For more information about the inner workings of the application check out the documentation.

---

# Running the Application

The Quiziverse application is built using Python with the Flask framework. It was developed with Python 3.12, so any system with a modern Python 3 interpreter should work. The application also uses MongoDB as its database. This tutorial assumes you have a running instance of MongoDB Community Edition on your machine. If you do not yet have MongoDB installed, please follow the instructions on the [MongoDB website](https://www.mongodb.com/).

Follow the steps below to install and run the application.

## 1. Installing Python

First, ensure that you have a modern version of Python 3 installed. Download it from the [official Python website](https://www.python.org/downloads/). On many Linux distributions, Python is pre-installed.

After installing, open your terminal (or command prompt) and type:

```bash
$ python3
Python 3.12.4 (main, Dec 18 2024, 07:20:02) [GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
```

## 2. Configuring Your Virtual Environment

Create a virtual environment to manage the dependencies for the application. In this tutorial, we use Python’s built-in `venv` module. Execute the following command in your project directory:

```bash
$ python -m venv .venv
```

Next, activate the virtual environment:

- **On Linux/macOS:**

  ```bash
  $ source .venv/bin/activate
  ```

- **On Windows (PowerShell):**

  ```powershell
  > .venv\Scripts\activate
  ```

After activating the environment, set an environment variable called `SECRET` for cryptographic operations.

- **On Linux/macOS:**

  ```bash
  $ export SECRET="your_secret_key"
  ```

- **On Windows (PowerShell):**

  ```powershell
  > $Env:SECRET = "your_secret_key"
  ```

## 3. Installing Dependencies

Install the application's dependencies using `pip`. All required packages are listed in the `requirements.txt` file:

```bash
$ pip install -r requirements.txt
```

## 4. Starting the Flask Server

With your environment set up and dependencies installed, you can now start the Flask server. Run the following command:

```bash
$ python -m api.app
```

> **Note:** On some Linux systems, you may need to use `python3` instead of `python`:
>
> ```bash
> $ python3 -m api.app
> ```

If everything is configured correctly, the Flask server will start, and you can begin registering for the Quiziverse application.

## 5. Generating Fake Data (Optional)

To generate fake data for testing, use the `generator.py` script located in the `generator` directory. Run the following command:

```bash
$ python generator/generator.py
```

This script will create:
- **6 users**
- **300 quizzes**
- **300 results**

> **Note:** Ensure that your MongoDB instance is running before generating fake data.

---

Congratulations! You have now set up the Quiziverse application.
