# Handwritten Mathematical Equation Solver

This project solves the problem of solving handwritten mathematical equations.
This has 2 components: React Front-end and Flask backend.

Use this to download dependencies in the Root folder.
> npm install

## RUN
Since the front-end depends on back-end, start the backend first.

### Start Back-End
In the folder "Equation-Solver-main" run this command:
`> flask run`
This will run Flask app in the port 5000 .
### Start Front-End
In the root folder run this command:
`> npm start`
This will run React app in the port 3000.

## Create the model
To Create the model go to the folder "Equation-Solver-main\Training" and use "Data_extraction.ipynb" file to create different training models. The dataset is in "Equation-Solver-main\Training\filtered_extracted_images" folder. This folder contains Alphabets, numbers and operators like [-,(,),+,=,/].

Most of the images were obtained from here: [https://www.kaggle.com/xainano/handwrittenmathsymbols](https://www.kaggle.com/xainano/handwrittenmathsymbols) .
Some of the images like parenthesis and operators were obtained from other sources.