# har_Swag

we are rendering “home.html” file on GUI once execution of flask application. In “home.html” file we are uploading a form that is carrying .har file. We are selecting form ID and once the upload button hits, we fire a POST request ('localhost/convertswag') to our backend for converting .har file to swagger JSON file. 
The “convert swagger” endpoint calls a function get Swagger, and after getting the swagger file we write the file and return the downloaded file.
The get swagger function first writes a few codes for swagger format after that it fetch the .har file and for each endpoint for the particular host appending all the PATH for swagger format. 
