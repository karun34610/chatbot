from flask import Flask, request
from flask_cors import CORS, cross_origin

from Functions import Chatbot

app = Flask(__name__)
CORS(app)
##################

############### Initiating the ChatBot class

ChatBot = Chatbot.Chatbot()

############### Setting up the documents, Embeddings and FIASS retrival
db, chain = ChatBot.run()


############### Route in the backend which handles the query by customer
@app.route("/", methods = ["GET"])
@cross_origin(origin='*')
def chatingBot():

  #### Input query
  query = request.args.get("query")
  # query = "What is a Pan ?"

  #### From the Chain and db initiated above, the response is generated from the query
  ans = ChatBot.chat(chain, query, db)

  print("---------Final Ans :", ans)

  return {
    "answer":ans
  }

if __name__=='__main__':
  app.run()