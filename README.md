# Convert HAR file to SWAGGER file

### Overview
The ".har file to Swagger file" project aims to develop a tool that can convert HTTP Archive files (.har) into Swagger/OpenAPI specification files. The tool will provide an automated and streamlined solution for transforming network traffic data captured in .har format into a Swagger specification, which is widely used for documenting RESTful APIs.

### Motivation
HTTP Archive files (.har) are commonly used to record and analyze network traffic data. However, when it comes to documenting APIs, Swagger is a popular choice due to its rich features, ecosystem support, and compatibility with various API development tools. Converting .har files to Swagger specifications manually can be time-consuming and error-prone. This project aims to automate this conversion process, making it more efficient and reliable.
### Key Features
1. **Har File Parsing:** Develop a parser to read .har files and extract relevant information, such as HTTP requests, headers, parameters, and response details.
2. **Swagger Generation:** Implement a logic to transform the parsed data into a Swagger/OpenAPI specification file.
3. **Schema Inference:** Analyze the captured request and response payloads to infer data schemas and generate corresponding Swagger schema definitions.
4. **Path and Operation Generation:** Map the captured requests to Swagger paths and generate corresponding HTTP operations (GET, POST, PUT, etc.) with relevant details.
5. **Parameter Extraction:** Extract path parameters, query parameters, and request body parameters from the captured requests and include them in the Swagger specification.
6. **Response Mapping:** Map the captured response details, including status codes, headers, and response bodies, to appropriate Swagger definitions.
7. **CLI and GUI Interfaces:** Provide command-line and graphical user interfaces to facilitate easy usage and interaction with the conversion tool.
8. **Error Handling:** Implement robust error handling mechanisms to handle malformed .har files or other exceptional scenarios gracefully.
### Potential Technologies
The project can be implemented using a combination of the following technologies and tools:
- Programming Language: Python  for parsing and generating files
- Libraries: Python libraries like haralyzer   for parsing .har files 
- Swagger/OpenAPI Libraries: swagger_ui for Swagger Doc Editor Generator
- User Interface: Flask and  web-based front-end  is html and javascript for the graphical user interface
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