from haralyzer import HarParser, HarPage
import json
import os
import io
from urllib.parse import urlparse
from flask import Flask, request, jsonify, render_template, send_file
from swagger_ui import flask_api_doc

app = Flask(__name__)
config = {
    "openapi": "3.0.1",
    "info": {
        "title": "python-swagger-ui test api",
        "description": "python-swagger-ui test api",
        "version": "1.0.0",
    },
    "servers": [{"url": "http://127.0.0.1:8989/api"}],
    "tags": [{"name": "default", "description": "default tag"}],
    "paths": {
        "/hello/world": {
            "get": {
                "tags": ["default"],
                "summary": "output hello world.",
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {
                            "application/text": {
                                "schema": {
                                    "type": "object",
                                    "example": "Hello World!!!",
                                }
                            }
                        },
                    }
                },
            }
        }
    },
    "components": {},
}

parameters = {
    "deepLinking": "true",
    "displayRequestDuration": "true",
    "layout": '"StandaloneLayout"',
    "plugins": "[SwaggerUIBundle.plugins.DownloadUrl]",
    "presets": "[SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset]",
}
flask_api_doc(
    app,
    config=config,
    url_prefix="/api/doc",
    title="API doc",
    editor=True,
    parameters=parameters,
)


def get_swagger(file, domain_name):
    # Initialize the Swagger specification

    swagger_spec = {
        "swagger": "2.0",
        "info": {"version": "1.0", "title": "API Documentation"},
        "host": "",
        "schemes": [],
        "paths": {},
    }
    

    har_data = json.loads(file.read())
    h = HarParser(har_data)

    har_data = h.har_data

    web = har_data["entries"][0]["request"]["url"]
    schemes = web.split("//")[0].split(":")[0]

    if domain_name is None:
        domain1 = urlparse(web).netloc
        print("this is domain is none", domain1)
    else:
        domain1 = domain_name
    swagger_spec["host"] = str(domain1)
    swagger_spec["schemes"] = [schemes]

    for request in har_data["entries"]:
        # Extract request details and add them to the Swagger specification
        a = request["request"]

        url = request["request"]["url"]

        method = request["request"]["method"]
        path = "/" + url.split("//")[-1].split("/", 1)[-1].split("?", 2)[0]
        domain = urlparse(url).netloc

        if domain == domain1:
            if ".js" in path:
                print("this is js", path)
            elif ".gif" in path:
                print("this is gif", path)
            elif ".css" in path:
                print("this is css", path)
            elif ".png" in path:
                print("this is png", path)
            elif ".jpg" in path:
                print("this is jpg", path)
            else:
                if path not in swagger_spec["paths"]:
                    swagger_spec["paths"][path] = {}
                swagger_spec["paths"][path][method.lower()] = {
                    "tags": ["api"],
                    "summary": request["request"]["method"],
                    "description": request["request"]["url"],
                    "parameters": [],
                    "consumes": ["application/json"],
                    "responses": {},
                }

                # Extract response details and add them to the Swagger specification
                if "response" in request:
                    status_code = request["response"]["status"]
                    # status code is 0 then add status code 200
                    if status_code == 0:
                        status_code = 200
                    if (
                        status_code
                        not in swagger_spec["paths"][path][method.lower()]["responses"]
                    ):
                        response_status = request["response"]["status"]
                        response_headers = request["response"]["headers"]
                        # if mime type is present in response content application/json
                        if "mimeType" in request["response"]["content"]:
                            # if request['response']['content']['mimeType'] == 'application/json':
                            swagger_spec["paths"][path][method.lower()]["consumes"] = [
                                request["response"]["content"]["mimeType"]
                            ]
                        if "text" in request["response"]["content"]:
                            response_body = (
                                request["response"]["content"]["text"]
                                if "content" in request["response"]
                                else None
                            )
                        else:
                            response_body = None
                        # Add response details to the Swagger specification
                        swagger_spec["paths"][path][method.lower()]["responses"][
                            response_status
                        ] = {
                            "description": "Response",
                            "headers": {
                                header["name"]: {"type": "string"}
                                for header in response_headers
                            },
                            "schema": {"type": "string", "example": response_body},
                        }
                # Bearer authentication is a security scheme with type: http and scheme: bearer. You first need to define the security scheme under components/securitySchemes, then use the security keyword to apply this scheme to the desired scope – global (as in the example below) or specific operations:
                for header in request["request"]["headers"]:
                    if header["name"] == "bearerAuth":
                        print(request["request"]["headers"])
                        # Add security scheme to the Swagger specification
                        swagger_spec["securityDefinitions"] = {
                            "bearerAuth": {
                                "in": "header",
                                "type": "apiKey",
                                "name": header["name"],
                            }
                        }
                        # Add security keyword to the Swagger specification and metion according swagger documentation and The square brackets [] in bearerAuth: [] contain a list of security scopes required for API calls
                        swagger_spec["paths"][path][method.lower()]["security"] = [
                            {"bearerAuth": []}
                        ]
                    # defines a security scheme named basicAuth (an arbitrary name). This scheme must have type: http and scheme: basic. The security section then applies Basic authentication to the entire API. The square brackets [] denote the security scopes used; the list is empty because Basic authentication does not use scopes
                    if header["name"] == "basicAuth":
                        swagger_spec["securityDefinitions"] = {
                            "basicAuth": {
                                "in": "header",
                                "type": "basic",
                                "name": header["name"],
                            }
                        }
                        swagger_spec["paths"][path][method.lower()]["security"] = [
                            {"basicAuth": []}
                        ]
                    # To describe an API protected using OAuth 2.0, first, add a security scheme with type: oauth2 to the global components/securitySchemes section. Then add the security key to apply security globally or to individual operations
                    if header["name"] == "oauth2":
                        swagger_spec["securityDefinitions"] = {
                            "oauth2": {
                                "type": "oauth2",
                                "tokenUrl": "https://api.example.com/oauth2/authorize",
                                "flow": "application",
                                "scopes": {"extended": ""},
                            }
                        }
                        swagger_spec["paths"][path][method.lower()]["security"] = [
                            {"oauth2": []}
                        ]
                # add query parameters if present
                request_query_params = request["request"]["queryString"]
                if (
                    request_query_params is not None
                    and "query"
                    not in swagger_spec["paths"][path][method.lower()]["parameters"]
                ):
                    for query_param in request_query_params:
                        query_param_name = query_param["name"]
                        query_param_description = query_param[
                            "value"
                        ]  # You can change this to a more descriptive description
                        swagger_spec["paths"][path][method.lower()][
                            "parameters"
                        ].append(
                            {
                                "name": query_param_name,
                                "in": "query",
                                "description": query_param_description,
                                "required": True,
                                "type": "string",
                            }
                        )
                # Add request body if present
                a = request["request"]
                if "postData" in a:
                    if "mimeType" in a["postData"]:
                        # if a['postData']['mimeType']=='application/json':

                        request_body = request["request"]["postData"]["text"]
                        # print("this is request bosy",request_body)
                        if (
                            request_body is not None
                            and "body"
                            not in swagger_spec["paths"][path][method.lower()][
                                "parameters"
                            ]
                        ):
                            swagger_spec["paths"][path][method.lower()][
                                "parameters"
                            ].append(
                                {
                                    "name": "body",
                                    "in": "body",
                                    "description": "Request body",
                                    "required": True,
                                    "schema": {
                                        "type": "string",
                                        "example": request_body,
                                    },
                                }
                            )
    return swagger_spec


@app.route("/convertswag", methods=["POST"])
def covnvertswag():
    har_file1 = request.files["har_file"]
    har_file = har_file1
    
    domain_name = request.form["domainName"]
    
    if domain_name == "":
        domain_name = None
    
    swagger = get_swagger(har_file, domain_name)
    swagger_json = json.dumps(swagger)

    # Create a file-like object from the json_response
    output = io.BytesIO(swagger_json.encode("utf-8"))

    # Return the file-like object as a response
    return send_file(
        output,
        mimetype="application/json",
        as_attachment=True,
        download_name="har_swagger.json",
    )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
