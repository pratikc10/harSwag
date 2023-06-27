# Convert HAR file to SWAGGER file

## Description
we are rendering “home.html” file on GUI once execution of flask application. In “home.html” file we are uploading a form that is carrying .har file. We are selecting form ID and once the upload button hits, we fire a POST request ('localhost/convertswag') to our backend for converting .har file to swagger JSON file. 
The “convert swagger” endpoint calls a function get Swagger, and after getting the swagger file we write the file and return the downloaded file.
The get swagger function first writes a few codes for swagger format after that it fetch the .har file and for each endpoint for the particular host appending all the PATH for swagger format.


### Steps to Build  and Run Project without Docker
1. Clone GitHub repository  for harSwag.( https://github.com/pratikc10/harSwag)

2. Go to root directory by executing "cd harSwag"

3. We need to create .venv and install the required python dependencies mentioned in the ‘requirements.txt’ file
```
pip install -r requirements.txt
```

4. Now execute the command ‘python app.py’ to run the application

5. Open browser and go to http://127.0.0.1:5000

### Steps to Build  and Run Project with Docker
1. Clone GitHub repository for harSwag.( https://github.com/pratikc10/harSwag)

2. Then excute "cd harSwag" to go into the project root directory

3. Now execute the below command to build the docker image
```
docker build -t harswag:latest .
```
4. Now excute the below command to start the docker container
```
docker run -p 5000:5000 harswag
```
5. Open browser and go to http://localhost:5000

![MicrosoftTeams-image (16)](https://github.com/Debadri-007/harSwag/assets/70701923/67ff3687-f386-4da3-8a0b-ad58db04b328)


### Functional Use Case
1. From http://127.0.0.1:5000/ URL link we can see the UI interface.

![MicrosoftTeams-image (15)](https://github.com/Debadri-007/harSwag/assets/70701923/b0bd3884-8336-40f9-b86c-2d0f09b5b9c3)

2. "Select .har File" from this we can add our .har file.
3. In the Domain Name we can put domain name as per .har file has or we can keep it empty.
4. After uploading  .har file It will generate har_Swagger json type file.

![MicrosoftTeams-image (17)](https://github.com/Debadri-007/harSwag/assets/70701923/5b8bf117-002d-4575-83d7-4c0c73d578f3)

5. We need to open Swagger editor (https://editor.swagger.io/) in from “File” section we can “Import file”
for importing the json file.

![MicrosoftTeams-image (18)](https://github.com/Debadri-007/harSwag/assets/70701923/6e33dc13-b795-40b7-9c13-9f4593b5d884)

6. Or we can “/api/doc/editor” with our URL http://127.0.0.1:5000/api/doc/editor it will redirect swagger editor, after that from “File” section we can “Import file” for importing the json file.
![MicrosoftTeams-image (19)](https://github.com/Debadri-007/harSwag/assets/70701923/dd383ffa-150e-4ab7-ad11-447dfe9df50e)

7. In right hand side we can get the Swagger Api documentation properly.