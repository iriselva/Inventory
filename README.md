# Backend and Infrastructure
## Module 5 group project for Web development in Reykjavik Technical School

For this project our group used the FARM stack (FastAPI, React, MongoDB)

We started with the FastAPI Swagger and connected it to a database in MongoDB. The database is then hosted on Heroku. We also created simple example frontend with React. In the application you can create a user and login. The loggin will give you an authenication token to secure your account. After loggin in you can create your own inventory database, list the items, delete and update.

## Creative Inventory API

The inspiration for this web application is for creative people and artist to have an online place to organize and keep inventory of their creations. 

In the future we want to add more security and a better front-end infrastructure to hande all of the database objects. 

We hope you like it!

## Files
+ [main.py](main.py) - Main app FastAPI
+ [models.py](models.py) - Basemodels and validations
+ [users.py](users.py) - Users functions (GET, POST, DELETE)
+ [inventory.py](inventory.py) - Inventory functions (GET, POST, DELETE, PATCH) 
+ [mysecurity.py](mysecurity.py) - Security functions (Access token, OAuth2, JWT)

## Front-end
We have two frontends in process on Github
+ [Frontend Test Client repository](https://github.com/Pauneren/inventory-test-client) LIVE!
+ [Creative Inventory Frontend repository](https://github.com/iriselva/inventory-frontend)

## Live version
Link to the live verion of the web application (Heroku)
>  [Creative Inventory](https://inventory-test-client.herokuapp.com/)

## Recources
This project was made with:
+ VS Code
+ Python
+ MongoDB
+ FastAPI
+ React
+ Heroku
+ Trello
+ And more..

## Creators
Made with love by these talented Web development students!
+ [Iris Elva Olafsdottir](https://github.com/iriselva)
+ [Kolbrun Jonsdottir](https://github.com/kollaaj)
+ [Paula Nerenberg](https://github.com/Pauneren)


---
