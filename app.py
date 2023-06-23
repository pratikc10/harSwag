from haralyzer import HarParser,HarPage
import json
import os
import io
from flask import Flask, request, jsonify,render_template,send_file

app = Flask(__name__)

def get_swagger(file):
    # Initialize the Swagger specification

    swagger_spec = {
        'swagger': '2.0',
        'info': {
            'version': '1.0',
            'title': 'API Documentation'
        },
        
        'paths': {}
    }
    print(file)
    print(swagger_spec)
    
    har_page = HarPage('unknown', har_data=json.loads(file.read()))

    requests = har_page

    
    for request in requests.entries:
        # Extract request details and add them to the Swagger specification
        url = request['request']['url']
        method = request['request']['method']
        path = "/"+url.split('//')[-1].split('/', 1)[-1].split('?')[0]
        #remove querystring from path
        # path = path.split('?')[0]
        # print(path)
        if path not in swagger_spec['paths']:
            swagger_spec['paths'][path] = {}
        swagger_spec['paths'][path][method.lower()] = {
            'tags': ['api'],
            'summary': request['request']['method'],
            'description': request['request']['url'],
            
            'parameters': [],
            
            'consumes': ['application/json'],
            
            'responses': {
                
            }
        }

        # Extract response details and add them to the Swagger specification
        if 'response' in request:
            status_code = request['response']['status']
            if status_code not in swagger_spec['paths'][path][method.lower()]['responses']:
                response_status = request['response']['status']
                response_headers = request['response']['headers']
                if  'text'in  request['response']['content']:
                    response_body = request['response']['content']['text'] if 'content' in request['response'] else None
                else :
                    response_body = None
                # Add response details to the Swagger specification
                swagger_spec['paths'][path][method.lower()]['responses'][response_status] = {
                    'description': 'Response',
                    'headers': {header['name']: {'type': 'string'} for header in response_headers},
                    
                    'schema': {
                        'type': 'string',
                        'example': response_body
                    }
                        
                    }
                
        # Bearer authentication is a security scheme with type: http and scheme: bearer. You first need to define the security scheme under components/securitySchemes, then use the security keyword to apply this scheme to the desired scope – global (as in the example below) or specific operations:
        for header in request['request']['headers']:
            if header['name']=='bearerAuth':            
                print(request['request']['headers'])
                # Add security scheme to the Swagger specification
                swagger_spec['securityDefinitions'] = {
                    'bearerAuth': {
                        'in': 'header',
                        'type': 'apiKey',
                        'name': header['name']
                    }
                }
                # Add security keyword to the Swagger specification and metion according swagger documentation and The square brackets [] in bearerAuth: [] contain a list of security scopes required for API calls
                swagger_spec['paths'][path][method.lower()]['security'] = [{'bearerAuth':[]}]
            # defines a security scheme named basicAuth (an arbitrary name). This scheme must have type: http and scheme: basic. The security section then applies Basic authentication to the entire API. The square brackets [] denote the security scopes used; the list is empty because Basic authentication does not use scopes
            if header['name']=='basicAuth':
                swagger_spec['securityDefinitions'] = {
                    'basicAuth': {
                        'in': 'header',
                        'type': 'basic',
                        'name': header['name']
                    }
                }
                swagger_spec['paths'][path][method.lower()]['security'] = [{'basicAuth':[]}]
            #To describe an API protected using OAuth 2.0, first, add a security scheme with type: oauth2 to the global components/securitySchemes section. Then add the security key to apply security globally or to individual operations
            if header['name']=='oauth2':
                swagger_spec['securityDefinitions'] = {
                    'oauth2': {
                        'type': 'oauth2',
                        'tokenUrl': 'https://api.example.com/oauth2/authorize',
                        'flow': 'application',
                        'scopes':{
                            'extended': ''
                        }

                    }
                }
                swagger_spec['paths'][path][method.lower()]['security'] = [{'oauth2':[]}]


                 
                
        # swagger_spec['paths'][path][method.lower()]['security'] = [{'bearerAuth': ["Bearer qjsajcsjcscxsjvas2bhbhjbjbnkljk"]}]
                

        
        # add query parameters if present
        request_query_params = request['request']['queryString']
        if request_query_params is not None and 'query' not in swagger_spec['paths'][path][method.lower()]['parameters']:
            for query_param in request_query_params:
                query_param_name = query_param['name']
                query_param_description = query_param['value']  # You can change this to a more descriptive description
                swagger_spec['paths'][path][method.lower()]['parameters'].append({
                    'name': query_param_name,
                    'in': 'query',
                    'description': query_param_description,
                    'required': True,
                    'type': 'string'
                })
                # print(query_param_name)
                
        #Add request body if present
        a=request['request']
        if 'postData' in a:
            # print("this is post data",a['postData'])
            request_body = request['request']['postData']['text']
            # print("this is request bosy",request_body)
            if request_body is not None and 'body' not in swagger_spec['paths'][path][method.lower()]['parameters']:
                swagger_spec['paths'][path][method.lower()]['parameters'].append({
                    'name': 'body',
                    'in': 'body',
                    'description': 'Request body',
                    'required': True,
                    'schema': {
                        'type': 'string',
                        'example': request_body
                    }
                })
                
    return swagger_spec           
    





@app.route('/convertswag', methods=['POST'])
def covnvertswag():
    har_file = request.files['har_file']
    # print(har_file)
    
    # file= r'C:\Users\pratik_chauhan1\projects\smartchat\imagevisioncaption-njsl6nofca-ue.a.run.app.har'
    swagger=get_swagger(har_file)
    print(type(swagger))
    # print(swagger)
    # response_data = {
    #     'result': 'Success',
    #     'data': swagger
    # }
    swagger_json = json.dumps(swagger)

    # Save swagger_spec as a JSON file
    with open('swagger.json', 'w') as file:
        file.write(swagger_json)
    # return send_file('swagger.json')
    # Convert the response data to JSON
    # json_response = json.dumps(swagger)
    
    # Create a file-like object from the json_response
    output = io.BytesIO(swagger_json.encode('utf-8'))
    
    # Return the file-like object as a response
    return send_file(output, mimetype='application/json', as_attachment=True, download_name='har_swagger.json')
    
    # return send_file(output, mimetype='application/json', as_attachment=True, attachment_filename='har_Swagger.json')


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


