from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

from idss import recommender

app = Flask(__name__)

api = Api(app)
cors = CORS()
cors.init_app(app)

# Initialize Recommender at startup
recommender = recommender(machine_powerful=False, info=True)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


class Movie(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('title', required=True)  # add title argument
        args = parser.parse_args()  # parse arguments to dictionary

        recommendation_result = recommender.recommend(args['title'], min_count=0, limit=5)

        return {'data': recommendation_result}, 200  # return data and 200 OK code

# append Movie class with its get Method for "/recommend" URI
api.add_resource(Movie, '/recommend')

if __name__ == '__main__':
    app.run()
