from flask_pymongo import PyMongo
import server as s

s.app.config['MONGO_DBNAME'] = 'samuka'

s.app.config['MONGO_URI'] = 'mongodb+srv://user:password@cluster0.daw3o.mongodb.net/flora?retryWrites=true&w=majority'

mongo = PyMongo(s.app)
