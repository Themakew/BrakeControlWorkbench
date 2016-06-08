# BrakeControlWorkbench

[![Build Status](https://travis-ci.org/Themakew/BrakeControlWorkbench.svg?branch=master)](https://travis-ci.org/Themakew/BrakeControlWorkbench)


# Installation

Clone the repository:
```bash
  $ git clone https://github.com/Themakew/BrakeControlWorkbench.git
```

Enter in the project directory:
```bash
  $ cd BrakeControlWorkbench/app
```

Install all the project dependencies:
```bash
  $ pip install -r requirements.txt
```


# Running the development server
Open three terminals into /app directory.

1) Open redis-server
```bash
  $ redis-server
```
2) Open celery
```bash
  $ celery worker -A main.celery -l info
```
3) Open python
```bash
  $ python main.py
```
