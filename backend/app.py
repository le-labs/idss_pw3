from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

from idss import RecommenderSystem

app = Flask(__name__)

api = Api(app)
cors = CORS()
cors.init_app(app)

# Initialize Recommender at startup
recommender_system = RecommenderSystem()


class MovieRecommenderResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('movie_id', required=True)  # add title argument
        args = parser.parse_args()  # parse arguments to dictionary

        recommendation_result = recommender_system.recommend(args['movie_id'], min_count=0, limit=9)

        if recommendation_result is None:
            return {'message': 'Not enough data for movie'}, 500

        return {'data': recommendation_result}, 200  # return data and 200 OK code


# append Movie class with its get Method for "/recommend" URI
api.add_resource(MovieRecommenderResource, '/recommend')

if __name__ == '__main__':
    app.run()
