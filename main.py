# put method use korte chaile request import kora lagbe. put method er through te jei data ashbe oita update korte lageb.
from flask import Flask, request
# reqparse diyeo argument pass kora jay, request object theke easier.
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)  # ekta app initialize korlam
# bole dilam j amra restful services use korbo.eta ekhon api hishabe cholbe
api = Api(app)
# bole dicchi database koi ase

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
# database use korbo je oita bole dilam


class videoModel(db.Model):  # database e ki ki field thakbe, model kemon hobe.
    id = db.Column(db.Integer, primary_key=True)
    # 100 maane character limit, nullable=false maane nam thakai lagbe, null hoa jabena.
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        # ek ek ta object print korar ekta format. ei method call korlei hbe.
        return f"video(name={name},views={views},likes={likes} )"


# db.create_all() --> ekbar eta likhe run korsi. tarpor comment kore dite hobe. barbar database create kore labh nai. ekbar korlei hoy.
# ekta resource banailam hello world name,sheta Resource theke inherit korlo, Resource er diffeerent method ekhane override korajabe.

'''
names = {"Sumit": {"age": "26", "gender": "male"},
         "Sumita": {"age": "26", "gender": "female"}}


class Helloworld(Resource):
    def get(self, name):
        # api response JSON serializable hoa lagbe tai emon format.
        return {"data": names[name]} '''


# notun request parser object banabo, request ja jabe sheigula parse kore nishchit korbe j amader deya nirdeshona follow kore.
videos_put_args = reqparse.RequestParser()
# ki ki argument dite hobe sheigula specify kore dibo.
# required=true dile oi argument er value deyai lagbe request send korar shomoy nahoy error dibe, mainly help message ta dekhabe.
videos_put_args.add_argument(
    "name", type=str, help="Name of the video", required=True)
videos_put_args.add_argument(
    "views", type=int, help="Views of the video", required=True)
videos_put_args.add_argument(
    "likes", type=int, help="Likes of the video", required=True)
# ekhon same vabe update korar jonno argument parser banabo, required=true dibona jate user jekonota pathate pare.

videos_update_args = reqparse.RequestParser()
videos_update_args.add_argument(
    "name", type=str, help="Name of the video")
videos_update_args.add_argument(
    "views", type=int, help="Views of the video")
videos_update_args.add_argument(
    "likes", type=int, help="Likes of the video")
videos = {}

# database chhara request pathano nicher commented block e
'''
 # jodi vidoe id na thake tokhon jeno onk lomba error message na dekhay.
    # thik moto bondho kore r ami ja chai shei err msg dekhay.
    # erokom onno condition eo error kora jabe

def video_id_na_thakle_bondho(video_id):
    if video_id not in videos:
        abort(404, message="video id is not valid")


def video_thakle_bondho(video_id):
    if video_id in videos:
        abort(409, message="video already exists")

class Videos(Resource):

    def put(self, video_id):
        # aage specify kora shob argument ekhane parse hobe. jodi thikmoto argument na ashe request e tahole error dekhabe.
        video_thakle_bondho(video_id)
        args = videos_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

    def get(self, video_id):
        video_id_na_thakle_bondho(video_id)
        return videos[video_id]

    def delete(self, video_id):
        video_id_na_thakle_bondho(video_id)
        del videos[video_id]
        return '', 204
'''
# ekhon databse diye korbo

# bole dicchi je videoModel er object gula ke kivabe dekhate chai, odr ki ki ase.
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Videos(Resource):
    @marshal_with(resource_fields)  # object take json serializable banabe.
    def get(self, video_id):
        results = videoModel.query.filter_by(id=video_id).first()
        # eirokom bhabe query korle videoModel class er instance return korbe jekhane id ta given video_id er shathe match korbe.
        #  java er object er mto
        # video_id diye filter kore then first response ta return korbe
        if not results:
            abort(404, message="could not find video")
        return results

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = videos_put_args.parse_args()
        results = videoModel.query.filter_by(id=video_id).first()
        if results:
            abort(403, message="..video id already taken..")
        # jate eki id wala video agei thakle program crash na kore
        video = videoModel(id=video_id, name=args['name'],
                           views=args['views'], likes=args['likes'])
        # ekta new object banailam argument e ja ja pass hoise sheigula niye
        db.session.add(video)  # temporary vabe add hoilo databse e
        db.session.commit()  # changes permanent hoilo database e
        return video, 201

    def delete(self, video_id):

        del videos[video_id]
        return '', 204

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = videos_update_args.parse_args()
        results = videoModel.query.filter_by(id=video_id).first()
        if not results:
            abort(404, message="..video does not exist. cannot update..")
        if args["name"]:
            results.name = args['name']
        if args['views']:
            results.views = args['views']
        if args['likes']:
            results.likes = args['likes']
        db.session.commit()

        return results


        # ei helloworld resource ke je banaisi ekhon etake api er resource hishabe add korbo jaate ekta specific endpoint hit korle user ke hello world rerutn kore.
        # ekhon /helloworld e get request dile ei resource return korbe Hello world.
        # api.add_resource(Helloworld, "/helloworld/<string:name>")  --> eita helloworld er jonno chhilo
api.add_resource(Videos, "/video/<int:video_id>")


if __name__ == "__main__":  # app ta start korbe
    # bole dicchi j debug mode tahole jodi kono kisu golmal hoy tahole log bhalomoto dekhabe.
    app.run(debug=True)
