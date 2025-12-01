from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of video",location="json", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video",location="json", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video",location="json",required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of video",location="json")
video_update_args.add_argument("views", type=int, help="Views of the video",location="json")
video_update_args.add_argument("likes", type=int, help="Likes of the video",location="json")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.get(video_id)
        if not result:
            abort(404, message="Video not found")
        return result
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        video = VideoModel(id=video_id,name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 200
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.get(video_id)

        if not result:
            abort(404, message="Video not found")

        # Only these columns are allowed to be updated
        update_fields = ["name", "views", "likes"]

        for field in update_fields:
            if args.get(field) is not None:
                setattr(result, field, args[field])

        db.session.commit()
        return result, 200


    
    def delete(self, video_id):
        video = VideoModel.query.get(video_id)
        if not video:
            abort(404, message="video not found")
        db.session.delete(video)
        db.commit()
        return '', 204
    

api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)