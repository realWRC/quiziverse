# Quiziverse

## Table of Contents
1. [Project Overview](#project-overview)
2. [Running the Application](#running-the-application)
   - [1. Installing Python](#1-installing-python)
   - [2. Configuring Your Virtual Environment](#2-configuring-your-virtual-environment)
   - [3. Installing Dependencies](#3-installing-dependencies)
   - [4. Starting the Flask Server](#4-starting-the-flask-server)
   - [5. Generating Fake Data (Optional)](#5-generating-fake-data-optional)
3. [Documentation](#documentation)
4. [Contributing](#contributing)
5. [License](#license)

---

## Project Overview

Quiziverse is a dynamic and interactive web application designed to simplify the process of creating, managing, and participating in quizzes. Its intuitive user interface enables users to create quizzes effortlessly and take part in them with ease. For developers, Quiziverse offers a robust backend API, allowing seamless integration of quizzes into their own applications. 

Key Features:
- User-friendly quiz creation and participation.
- Backend API for integration into external applications (refer to our [RESTful API routes documentation](https://realwrc.github.io/quiziverse/api.blueprints.html#restful-api-routes)).
- Flexibility in customizing scoring and time limits.

To set up and run the application, follow the tutorial below. For more technical details about the architecture and inner workings of Quiziverse, explore our comprehensive [documentation](https://realwrc.github.io/quiziverse/index.html).

---

## Running the Application


The Quiziverse application is built using Python with the Flask framework. It was developed with Python 3.12, so any system with a modern Python 3 interpreter should work. The application also uses MongoDB as its database. This tutorial assumes you have a running instance of MongoDB Community Edition on your machine. If you do not yet have MongoDB installed, please follow the instructions on the [MongoDB website](https://www.mongodb.com/).

Follow the steps below to install and run the application.

### 1. Installing Python

First, ensure that you have a modern version of Python 3 installed. Download it from the [official Python website](https://www.python.org/downloads/). On many Linux distributions, Python is pre-installed.

To verify your installation, open your terminal (or powershell) and type:

- **On Linux/macOS:**

```bash
$ python3
Python 3.12.4 (main, Dec 18 2024, 07:20:02) [GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
```
- **On Windows (PowerShell):**

```powershell
PS C:\> python
Python 3.12.4 (tags/v3.12.4:8e8a4ba, Jun  6 2024, 19:30:16) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
```

### 2. Configuring Your Virtual Environment

Create a virtual environment to manage the dependencies for the application. In this tutorial, we use Python’s `venv` module. Execute the following command in your project directory:

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

### 3. Installing Dependencies

Install the application's dependencies using `pip`. All required packages are listed in the `requirements.txt` file:

```bash
$ pip install -r requirements.txt
```

### 4. Starting the Flask Server

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

### 5. Generating Fake Data (Optional)

To populate the database with test data, use the `generator.py` script located in the `generator` directory.

```bash
$ python -m generator.generator
```

This script will create:
- **6 users**
- **300 quizzes**
- **300 results**

> **Note:** Ensure that your MongoDB instance is running before executing this script.

---

Congratulations! You have now set up the Quiziverse application. You can register, login and have some fun.

## Documentation

Detailed information about Quiziverse's architecture, API routes, and functionality is available in our [official documentation](https://realwrc.github.io/quiziverse/index.html).

---

## Contributing

We welcome contributions to Quiziverse! If you would like to contribute, please fork the repository, make your changes, and submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
