# Capstone Project: Cupcake Cafe
# Noreen Wu
# January 2020


## Introduction



## Running the Application

### Database

Models:

    Cupcakes with name and description
        is linked to Ingredient model via secondary cupcake_ingredient table (many cupcakes to many ingredients)
        is linked to OrderItem; (one cupcake may be in one or more OrderItem)

    Ingredient with kind, name and usage_count
        linked to Cupcake as described above

    Order with customer_name
        is linked to OrderItem (one order may contain one or more OrderItem)

    OrderItem with foreign keys cupcake_id (Cupcake) and order_id (Order)
        also contains quantity ordered
    
    

### Back-end

### Endpoint Overview

GET /cupcakes, /ingredients, /orders
DELETE /cupcakes, /ingredients, /orders
POST /cupcakes, /ingredients, /orders
PATCH /cupcakes, /ingredients, /orders


Roles:  

    the public (unauthenticated user) - can view cupcakes or individual cupcakes specified by id

    Bakery Clerk - can view cupcakes (or individual cupcakes) and view orders (or individual orders by id)

    Bakery Manager - can view cupcakes, ingredients, orders; can create, edit and delete orders

    Chief Baker - can view, create, update, delete cupcakes and ingredients; cannot see orders


Tests:

    Postman tests are organized by role and emphasize RBAC testing.

    Unittest tests are also organized by role but emphasize correct input.


### Endpoint Library


GET /cupcakes

    Does not require credentials

GET /cupcakes/int:id

    Does not require credentials


POST /cupcakes

    Requires the permission "post:cupcakes", which only the users with the ChiefBaker role possess.

PATCH /cupcakes/int:id

    Requires the permission "patch:cupcakes", which only the users with the ChiefBaker role possess.


DELETE /cupcakes/int:id

    Requires the permission "delete:cupcakes", which only the users with the ChiefBaker role possess.


GET /ingredients

    Requires the permission "get:ingredients", which users with either the ChiefBaker or 
    BakeryManager roles possess.


GET /ingredients/int:id

    Requires the permission "get:ingredients", which users with either the ChiefBaker or 
    BakeryManager roles possess.


POST /ingredients

    Requires the permission "post:ingredients", which only users with the ChiefBaker role possess.


PATCH /ingredients/int:id

    Requires the permission "patch:ingredients", which only users with the ChiefBaker role possess.


DELETE /ingredients/int:id

    Requires the permission "delete:ingredients", which only users with the ChiefBaker role possess.


GET /orders

    Requires the permission "get:orders", which users with either the BakeryManager or BakeryClerk
    roles possess.

GET /orders/int:id

    Requires the permission "get:orders", which users with either the BakeryManager or BakeryClerk
    roles possess.


POST /orders

    Requires the permission "post:orders", which only users with the BakeryManager role possess.

PATCH /orders/int:id

    Requires the permission "patch:orders", which only users with the BakeryManager role possess.


DELETE/orders/int:id

    Requires the permission "delete:orders", which only users with the BakeryManager role possess.



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


