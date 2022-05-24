# ice_cream_web_app

This erpository contains the web application for the ice cream recipe rating website.

The application is developed using Python3/Flask framework __ice_cream_rater.py__

## Description
This code has beed deployed on an EC2 machine, on the same directory level the [machine-learner](https://github.com/dmrimawi/machine-learner) repository should be cloned as well.

The website has two main pages:

__Rating recipe__: That uses a trained classifier model to classify a given recipe ingerdiants from 1 - 5.

__Adding new rate__: Allow the user to insert new ratings for new recipes or and existed ones.

## Infrastructure

This project consists of four main componenets, that work together to perferm an on-demand learning proess using aws services, and terraform. The components are:

__Web server__: It is an EC2 machine with NGINX, that contains the [ice cream web app](https://github.com/dmrimawi/ice_cream_web_app) reposiroty and the [machine-learner](https://github.com/dmrimawi/machine-learner) repository in the server configuration.

During run-time, the web application allows the user to first classify the recipe given through the root (/) rout, and inserting new rating values for new recipes though the (/rate_some_recipe) rout.

Rating some recipe, will update the CSV data file with the new rates, and when the new records count reaches a specific number (in this project it set to 5 new records) the new CSV file will be pushed back to the [machine-learner](https://github.com/dmrimawi/machine-learner) repository to allow the machone learning server to train the classification model using the new data.

__Serverless__:

__Machine learning server__:

__Storage__:


