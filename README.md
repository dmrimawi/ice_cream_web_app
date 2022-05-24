# ice_cream_web_app

This repository contains the web application for the ice cream recipe rating website.

The application is developed using Python3/Flask framework __ice_cream_rater.py__

## Description
This code has been deployed on an EC2 machine, on the same directory level, the [machine-learner](https://github.com/dmrimawi/machine-learner) repository should be cloned as well.

The website has two main pages:

__Rating recipe__: Using a trained classifier model to classify given recipe ingredients from 1 to 5.

__Adding new rate__: Allow the user to insert new ratings for new recipes or and existed ones.

## Infrastructure

This project consists of four main components, that work together to perform an on-demand learning process using AWS services, and terraform. The components are:

### Webserver 
It is an EC2 machine with NGINX, that contains the [ice cream web app](https://github.com/dmrimawi/ice_cream_web_app) repository and the [machine-learner](https://github.com/dmrimawi/machine-learner) repository in the server configuration.

During run-time, the web application allows the user first to classify the recipe given through the root (/) route, and insert new rating values for new recipes through the (/rate_some_recipe) route.

Rating some recipes will update the CSV data file with the new rates, and when the new records count reaches a specific number (in this project is set to 5 new records) the new CSV file will be pushed back to the [machine-learner](https://github.com/dmrimawi/machine-learner) repository to allow the machine learning server to train the classification model using the new data.

### Serverless
This is the key service used to make the learning happens on-demand only. AWS Lambda function allows idle containers to wait for requests as a backend service and will only work if received a request.

A docker container was created to perform the following tasks:

__Creation__: create a new EC2 machine with a security group to allow SSH connection and key pairs.

__Learning__: as part of the EC2 properties it passes a shell script to spin the learning process.

__Destruction__: after the learning is finished, the docker container will make sure to destroy all the resources created.

The technology used in the container is depending on Terraform and the code and further information can be found on the [aws-lambda-terraform-docker](https://github.com/dmrimawi/aws-lambda-terraform-docker) repository.

### Machine learning server

### Storage


