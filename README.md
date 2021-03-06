# On-Demand Learning

On-Demand learning is a project that aims to perform a machine learning process when it is needed, and not have dedicated servers that are idle for a long time.

## Problem
A lot of online systems that have to make decisions based on machine learning models will often need to retrain the model whenever a new set of input is given, so the system adapts to the new data.

The issue is that these models need high computational servers to run the learning algorithms, which consumes the resources and also has high costs as well.

In this project we developed an IaC solution, that automatically creates the learning resources only when it is required and then deletes these resources after the task is finished. To better optimize the resources and the money.

## Infrastructure

This project consists of four main components, that work together to perform an on-demand learning process using AWS services, and terraform. The components are:

### Webserver 
It is an EC2 machine with NGINX, that contains the [ice cream web app](https://github.com/dmrimawi/ice_cream_web_app) repository and the [machine-learner](https://github.com/dmrimawi/machine-learner) repository in the server configuration.

During run-time, the web application allows the user first to classify the recipe given through the root (/) route, and insert new rating values for new recipes through the (/rate_some_recipe) route, and mainly these are two pages in the website:

__Rating recipe__: Using a trained classifier model to classify given recipe ingredients from 1 to 5.

__Adding new rate__: Allow the user to insert new ratings for new recipes or and existed ones.

Rating some new recipes will update the CSV data file with the new rates, and when the new records count reaches a specific number (in this project is set to 5 new records) the new CSV file will be pushed back to the [machine-learner](https://github.com/dmrimawi/machine-learner) repository to allow the machine learning server to train the classification model using the new data.

### Serverless
This is the key service used to make the learning happens on-demand only. AWS Lambda function allows idle containers to wait for requests as a backend service and will only work if received a request.

A docker container was created to perform the following tasks:

__Creation__: create a new EC2 machine with a security group to allow SSH connection and key pairs.

__Learning__: as part of the EC2 properties it passes a shell script to spin the learning process.

__Destruction__: after the learning is finished, the docker container will make sure to destroy all the resources created.

The technology used in the container is depending on Terraform and the code and further information can be found on the [aws-lambda-terraform-docker](https://github.com/dmrimawi/aws-lambda-terraform-docker) repository.

### Machine learning server
This server is created by the Terraform container running inside the serverless Lambda function, and during starting up the EC2 receives a shell script as a user-data, that runs the following stages:

__Preperation__: it creates the environment, installs the packages needed, sets up the SSH keys, and clones the [machine-learner](https://github.com/dmrimawi/machine-learner) repository.

__Learning__: It executes the Python script to run the classification learner, and produces a new classification model.

__Wrapping up__: it pushed back the new classification model to the [machine-learner](https://github.com/dmrimawi/machine-learner) repository.

For the code and more information, please check the [machine-learner](https://github.com/dmrimawi/machine-learner) repository.

### Storage
An accessible place to store the data file and the model is needed to facilitate the way. It can be any cloud storage service like an S3 bucket. 

In this project, we have selected Github as the common storage area and the repository is [machine-learner](https://github.com/dmrimawi/machine-learner) repository.

The following image illustrates these components.

![On Demand Learning Infrastructure Diagram](https://github.com/dmrimawi/ice_cream_web_app/blob/master/CloudComputing.jpg)



## About us

This project is a result of the Cloud computing and distributed systems course at Free university of Bozen-Bolzano.

By: __Diaeddin Rimawi__, and __Eduardo Suraci Picchiotti__. Supervised by __Dr. Nabil El Ioini__.
