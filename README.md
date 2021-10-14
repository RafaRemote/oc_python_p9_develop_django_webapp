# Project 9: LITReview

Menu

1. Usage
2. Technologies
3. Installation
4. Execution of the program
5. flake8 report
6. Important information about the database

## 1 - Usage

Ask book or article reviews through ticket creation.  
Post book or article reviews.  

User can:
    - login and register: a logout user can not access to the website,  
    - see the flow of recent tickets and reviews of the users that he is following, in an ascending order: most recent first,  
    - create new tickets to ask for a book or an article review,  
    - create reviews as an answers to tickets questions,  
    - create reviews which are not answers to tickets,  
    - create a ticket and create a review as an answer to its own ticket,  
    - read, update and delete his own tickets and reviews,  
    - follow other users by typing their names,  
    - read who he is following, and follow who he wants,  
    - can stop to follow another user.  

## 2 - Technologies

Programming language: Python 3.10  
Web framework: Django 3.2.8  
Database: Django's db SQLite3  

## 3 - Installation

You need to have Python installed on your machine. [install python](https://www.python.org/downloads/)  
You need to have Git installed on your machine. [install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)  
This app has been developed using python 3.10  
Check your version of Python, if needed, upgrade your version.  
  
Open a terminal wherever you want then follow these steps:  

- Clone the repository:  

```python
git clone https://github.com/RafaRemote/litreview.git
```

- Move to the root folder:  

```python
cd litreview
```

- Install the virtual environment:  

```python
python3 -m venv env
```

or on windows: py -m venv env  

- Activate the virtual environment:  

```python
source env/bin/activate
```

or on windows: env\Scripts\activate  

- Upgrade pip:  

```python
pip install --upgrade pip
```

- Install the project dependencies:  

```python
pip install -r requirements.txt
```

## 4 - Execution of the program

From the terminal, be sure to be in the root folder (named 'litreview'), then type:  

```python
python manage.py runserver
```

Development server starts at: [http://127.0.0.1:8000/](http://127.0.0.1:8000)  

## 5 - flake8 report

In the root folder (named: 'litreview') you'll find a folder called: 'flake8_report', including an index.html showing 'no flake8 violations'.  

To generate a new report:  

erase the folder 'flake8_report'.  
be sure to be in the root folder 'litreview', then type:  

```python
flake8 --format=html --htmldir=flake8_report
```

## 6 - Important information about the database

The database has been populated.  
For convenience here are the list of the users already in the database.  

| name_____| password | status____|  
|---------------------------------|  
| rafa_____| 1q2w3e$$ | superuser |  
| ewa______| 1q2w3e$$ |___________|  
| bernardo_| 1q2w3e$$ |___________|  
| antoine__| 1q2w3e$$ |___________|  
| alice____| 1q2w3e$$ |___________|  
