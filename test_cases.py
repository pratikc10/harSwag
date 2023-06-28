from app import app

from app import get_swagger




# create the test case for get_swagger
def test_get_swagger():
    har_file = open('knowledge.vidyard.com .har', 'rb')
    domain_name = 'play.vidyard.com'
    swagger = get_swagger(har_file, domain_name)
    assert (swagger['swagger'] == '2.0')
    assert (swagger['info']['title'] == 'API Documentation')
    assert (swagger['info']['version'] == '1.0')
    assert (swagger["host"] == 'play.vidyard.com')
    har_file.close()

# create the test case for get_swagger

def test_get_swaggerEmptyDomain():
    har_file = open('knowledge.vidyard.com .har', 'rb')
    domain_name = ''
    swagger = get_swagger(har_file, domain_name)
    assert (swagger['swagger'] == '2.0')
    assert (swagger['info']['title'] == 'API Documentation')
    assert (swagger['info']['version'] == '1.0')
    assert (swagger["host"] == '')
    har_file.close()





    