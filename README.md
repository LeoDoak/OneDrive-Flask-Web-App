# Notes Web Flask Application 

## Install Flask
* Flask is necessary for this project to function correctly. 
* [Install Flask Link](https://code.visualstudio.com/docs/python/tutorial-flask)


### Can also be downloaded using a package manager such as pip: 
 
MacOS / Linux / Windows
```bash
$ pip install flask 
```

## Create Virtual Environment
* A virtual environment is necessary to run the flask project in
* [Info found here](https://flask.palletsprojects.com/en/3.0.x/installation)

MacOS / Linux
```bash
$ mkdir myproject
$ cd myproject
$ python3 -m venv .venv
```
Windows 
```bash
> mkdir myproject
> cd myproject
> py -3 -m venv .venv
```

## Activate Virtual Environment 

MacOS / Linux
```bash
$ . .venv/bin/activate
```

Windows 
```bash
> .venv\Scripts\activate
```

## Packages Included and their Documenation 

* [Waitress Documentation](https://pypi.org/project/waitress)
* [Pillow Documentation](https://pypi.org/project/pillow/)
* [sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
* [numpy Documentation](https://numpy.org/doc/)
* [Flask-login Documentation](https://flask-login.readthedocs.io/en/latest/)
* [msal Documentation](https://pypi.org/project/msal/)
* [requests Documentation](https://pypi.org/project/requests/)
* [ipython Documentation](https://ipython.org/)
* [Flask_wtf Documentation](https://flask-wtf.readthedocs.io/en/1.2.x/)

### Install Packages via Pip packages

```bash
$ pip install waitress pillow numpy flask-login msal requests ipython flask_wtf
```
### or via Requirments document

```bash
$ pip install -r requirements.txt
```

## Running the flask project: 
* Run the server.py file and enter whatever local host number you want
* go into a browser and in the search bar,type in localhost:(Number), ex: localhost:8000
* The project will be started from that link. 

## IDE Used 
* Whichever application you may be using to run the code, we used VS Code or PyCharm, make sure to install the necessary frameworks, including Flask, waitress and any other import you might see in the code above.

## Executing Tests

* How to install testing library:
```bash
$ pip install pytest
```

### Command to execute tests

* Run this in your terminal with the name of the test file you want to check and it will display test cases and if they succeeded or not.
```bash
$ pytest test_myfile.py
```
* Executing user_test.py (Registration Test)
```bash
$ cd flasknotesapp
$ python3 user_test.py 
```

### Deployment:
* Deployed on python anywhere
URL: https://ldoak.pythonanywhere.com/

**That's all it takes to be able to run our program so far. Enjoy!**

### Deployment 

* Deployed on python anywhere
Link: https://ldoak.pythonanywhere.com/

