# WattSmart Supporting Documents

## Attached Documents:
- WattSmart entire code
- No executable

There is no executable attached as this application is hosted locally on your machine.

## Steps to run application

### Step 1
Open a terminal/cmd/any CLI (command line interface) on the root folder

E.g., the root directory must end in `/WattSmart/` and not  anything else

### Step 2
Run the commands below in order

1. `cd frontend/`
2. `npm install`
3. `cd..` (double dots)
4.  `pip install -r requirements. txt`
5. `python .\manage.py makemigrations`
6. `python .\manage.py migrate`
7. `python .\manage.py runserver`

#### What is it doing?

The following steps will install all required dependencies and libraries for both the frontend and backend.

It will initliase and setup the database then run the server

The server is typically hosted on `127.0.0.1:8000`, if not, it will state on the terminal after executing command 7

### Final Steps

The database will be empty so you will need to create a user


