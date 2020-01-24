# Capstone Project: Cupcake Cafe
# Noreen Wu
# January 2020


## Introduction

The CupcakeCafe API provides functionality to enable a small bakery to manage its cupcake and ingredients
inventory, while also keeping track of orders. Cupcakes are comprised of ingredient types: typically, frosting, topping,
and cake. Orders are a collection consisting of the number of cupcakes a customer wishes to order, along
with their name: for example, one order might be for 15 Halloween Cupcakes + 30 Autumn Fest Cupcakes for a 
customer named Marty Smith.

The API assumes that bakery workers will take on several different roles: The Bakery Manager is focused on
taking customer orders and on which ingredients are in the most demand, and therefore has the capability to add,
create, update, delete and view all the orders, as well as view the ingredients in use and the current
cupcake selection. The Bakery Clerk is an assistant to the Manager and can only view the cupcake selection
and view the orders. The Chief Baker is most concerned with the current cupcake offering, and thus
can create, update, delete and view the cupcakes. Also the Chief Baker is concerned with managing
the available ingredients, and therefore can view, create, update, and delete the ingredients. The
Chief Baker has less interest in the actual orders, except through direct discussion with the Bakery
Manager, and thus does not have access to see these. 

The general public can view the cupcakes but does not have access to any of the other information.


## Running the Application


Heroku

local


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


