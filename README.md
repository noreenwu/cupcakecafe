# Capstone Project: Cupcake Cafe
# Noreen Wu
# January 2020


## Introduction

## Running the Application

### Database


### Back-end


### Tests

In order to run the unit tests, first ensure that the DATABASE_URL environment variable is set to
the name of the test database (example: cupcakecafe_test). This is pre-configured
in the shell script setuptest.sh. To run it in bash, use ```source ./setupsh.sh```

Create the test database and load it with some data.

     createdb cupcakecafe_test
     python load_data.py


Run the server (still using the test database):

     python app.py


Now run the test script:

     python test_cupcake.py


