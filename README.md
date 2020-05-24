# Project done during my Udacity Full Stack Nanodegree

I used git during all the development of my Udacity Project.

## Fyyur project

The Fyyur project is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues.

The objective of this project was to demonstrate the ability of modeling and creating the databse using the Flask SQLAlchemy mdoule. Using the already made front end, I had to connect all the Form and View to real data saved in the database like :

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.

For more information look at the [README](01_fyyur/README.md) inside the Fyyur folder.

## Trivia App

The Trivia App is the game of Trivia playable online.

The objective here was to create all the API endpoints to retrieve, add or delete questions, categories, .. The main difficulty was to format the data properly to what the front end was expeting.

The second part of the project was to create API endpoints test. Doing tests ensure 3 things:

* Verify that each endpoints is tested and working
* Protect for unexpected bug when doint update to the API
* Ensure that the error are handled as expected

For more information look at the [README](02_trivia_api/README.md) inside the Fyyur folder.

## Coffee Shop

The goal of this project was to use Auth0 services to create an API that would serve drinks and menu from a database. Using **roles** and **permissions** we can restrict the access to specific endpoint depending on the user access level located in the permissions sent through the JWT after we logged with Auth0, the external login service.

We also used Postman application to test all our endpoints.

For more information look at the [README](03_coffee_shop/README.md) inside the Coffee Shop folder.

## Kubernetes EKS

In this project we had to containerize and deploy a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild. We also used Gunicorn for using our flask app in production.

For more information look at the [README](04_deploy_flask_kubernetes_eks/README.md) inside the Flask Kubernetes EKS folder.

## Capstone Project

For this last project, we had to start from scratch and build an API that was using all the previous tools we learnt, such as :

* Coding in Python 3
* Relational Database Architecture
* Modeling Data Objects with SQLAlchemy
* Internet Protocols and Communication
* Developing a Flask API
* Authentication and Access
* Authentication with Auth0
* Authentication in Flask
* Role-Based Access Control (RBAC)
* Testing Flask Applications
* Deploying Applications

I decided to build a photo album creation website where you can create anonymous album (you can log in too) where the users can only see one different picture everyday. The project is not live yet but will be soon !

Check the repository for the capstone project [here](https://github.com/MattiooFR/1pic1day) for more informations !
