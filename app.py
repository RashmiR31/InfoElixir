from flask import Flask,jsonify,request
from flask_restx import Api, Resource, fields, Namespace
from build_graph import create_graph,add_subjects_to_graph,update_topics,delete_subject
from upload_files import upload_blob
import os 

app = Flask(__name__)
api = Api(app, title='InfoElixir API')


# Create a namespace for knowledge graph
graph_ns = Namespace('knowledge_graph', description='knowledge graph operations')
api.add_namespace(graph_ns)


data_model = api.model('Document',{
    'name':fields.String(required=True, description='Name'),
    'subject': fields.String(required=True, description='Subjects'),
    'topic': fields.Raw(required=False, description="Topics"),
})

# api endpoints
@graph_ns.route("/create")
class CreateGraph(Resource):
    @api.expect(data_model,validate=True)
    def post(self):
        data = request.get_json()
        print(data)
        create_graph(data)
        return {'message': 'Graph created successfully'}, 201
    
@graph_ns.route("/add_subject")
class AddSubject(Resource):
    @api.expect(data_model,validate=True)
    def post(self):
        data = request.get_json()
        name=data["name"]
        subject=data["subject"]
        topic=data["topic"]
        add_subjects_to_graph(name=name,subject=subject,topic=topic)
        return {'message': 'Subject added successfully'}, 201
    
@graph_ns.route("/update_topics")
class UpdateTopics(Resource):
    @api.expect(data_model,validate=True)
    def put(self):
        data = request.json
        name = data.get('name')
        subject = data.get('subject')
        topic = data["topic"]
        update_topics(name, subject, topic)
        return {'message': 'Topics updated successfully'}, 200
    
@graph_ns.route("/delete_subject")
class DeleteSubject(Resource):
    @api.expect(data_model,validate=True)
    def delete(self):
        data = request.json
        name = data.get('name')
        subject = data.get('subject')
        delete_subject(name, subject)
        return {'message': 'Subject deleted successfully'}, 200

if __name__ == '__main__':
    app.run(debug=True)
