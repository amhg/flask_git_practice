from flask import current_app, jsonify, request, Response, make_response
from flask.json import dumps
from datetime import date, datetime

@current_app.get("/index2")

#dictionary
#before today=date.today()
def index2():
   books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': datetime.now()},

    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': datetime.now()},

    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': None}
    ]
   #tuple
   data = [
      (1, "sherwin", 89.6, date.today()),
      (1, "sherwin", 89.6, date.today()),
      (1, "sherwin", 89.6, date.today()),
      (1, "sherwin", 89.6, date.today())]

    
   resp = Response(response = dumps(books), status=200, mimetype="application/json" )

   return resp

@current_app.post("/accept")
def accept_json():
   print(request.get_json())
   
   return "successul", 201

#before today=date.today()
@current_app.route("/index", methods = ['GET'])
def index():
   response = make_response(jsonify(message='This is an Online Pizza Ordering System.', today=datetime.now()), 200)
   return response


@current_app.get('/shark')
def shark():
   return("Shark🦈!")

