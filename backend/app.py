from flask import Flask
from flask_restful import Resource, Api, reqparse
from idss import recommender
app = Flask(__name__)
api = Api(app)

recommender = recommender(machine_powerful=False, info=True)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


class Movie(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('title', required=True)  # add arguments
        args = parser.parse_args()  # parse arguments to dictionary

        recommendation_result = recommender.recommend(args['title'], 0)

        return {'data': recommendation_result}, 200  # return data and 200 OK code


api.add_resource(Movie, '/recommend')  # '/users' is our entry point for Users

if __name__ == '__main__':
    app.run()
