# wize-employees

A simple API collection to register, promote and create duties for employees of an organization.

# How to run

To run wize-employees in development mode; Just use steps below:

    Install python3, pip, virtualenv in your system.
    Clone the project https://github.com/sina-chaichi/wize-employees.git.
Make development environment ready using commands below;

    $ git clone https://github.com/sina-chaichi/wize-employees.git 
    $ cd wize
    $ virtualenv -p python3 venv  # Create virtualenv named venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python3 manage.py migrate  # Create database tables

    Run wize-employees using:
    $ python3 manage.py runserver 8080 #local server on port 8080
    
Go to http://localhost:8000 to see your wize apis.
From the directory wize import Wize_Employees_postman_collection.json file into your postman API manager
and test all APIs!



