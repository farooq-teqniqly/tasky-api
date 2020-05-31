from flask import Flask
from flask_restful import Api

from resources.taskresource import TaskResource
from respositories.taskrepository import TaskRepository

app = Flask(__name__)
api = Api(app)

task_repository = TaskRepository()

api.add_resource(
    TaskResource,
    "/tasks/<string:task_id>",
    resource_class_kwargs={"task_repository": task_repository},
)

if __name__ == "__main__":
    app.run()
