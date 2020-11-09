from flask import Flask
from flask_restful import Resource, Api, reqparse
import markdown
import os
import redis 
from rejson import Client, Path 
import binascii

# Initialize flask 
app = Flask(__name__)

# Intialize rejson client 
rj = Client(host='redis', port=6379, decode_responses=True)

# Create the API
api = Api(app)

@app.route("/")
def index():
    """ Present API Documentation """

    # Open the readme file 
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read contents of readme file 
        content = markdown_file.read()

        # Convert to HTML 
        return markdown.markdown(content)

class BookList(Resource):
    def get(self):
        book_data_list = []
        # get current data in redis db
        book_ids = rj.keys()

        for book_id in book_ids:
            book_data = rj.jsonget(book_id, Path('.book_title'))
            book_data_string = "{0}:{1}".format(book_id, book_data)
            book_data_list.append(book_data_string)

        return {'message':'Success', 'data':book_data_list}

    def post(self):

        # Generate a random six digit hex id for the book entry
        book_id = binascii.b2a_hex(os.urandom(6)) 
        
        # Create a parser for request args
        parser = reqparse.RequestParser()

        parser.add_argument('book_title', required=True)
        parser.add_argument('author', required=True)
        parser.add_argument('release_year', required=True)
        parser.add_argument('genre', required=True)
        parser.add_argument('read', required=True)
        parser.add_argument('page_nos', required=True)
        parser.add_argument('rating', required=True)

        # Parse the arguments into an object 
        args = parser.parse_args()

        # Write the object to redis 
        rj.jsonset(book_id, Path.rootPath(), args)

        response_data = "{0}:{1}".format(book_id, args)

        return {'message': 'Book record added', 'data':response_data}


class Book(Resource):
    def get(self, book_id):

        # If entry does not exist in the datastore , return a 404 error 

        try:
            response = rj.jsonget(book_id)
            return {'message': 'Book record found', 'data':response}, 200 
        except:
            return {'message': 'Book record not found', 'data': {}}, 404 

    def put(self, book_id):
        # Parse the input and collect the updated fields
        parser = reqparse.RequestParser()

        parser.add_argument('read', required = True)
        parser.add_argument('rating', required = True)

        # Parse the arguments into an object 
        args = parser.parse_args()

        # Update entry in redis db 
        try: 
            rj.jsonset(book_id, Path('.rating'),args['rating'])
            rj.jsonset(book_id, Path('.read'), args['read'])
            response = rj.jsonget(book_id)

            return {'message': 'Book record updated', 'data': response}, 204 
        except:
            return {'message': "Error updating book record", 'data':{} }, 503
            

api.add_resource(Book, '/book_list/<string:book_id>')
api.add_resource(BookList, '/book_list')









