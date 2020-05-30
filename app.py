from flask import Flask
from flask_restful import Api

from resources.task import Task
from respositories.taskrepository import TaskRepository

app = Flask(__name__)
api = Api(app)

task_repository = TaskRepository()

api.add_resource(
    Task,
    "/tasks/<string:task_id>",
    resource_class_kwargs={"task_repository": task_repository},
)

if __name__ == "__main__":
    app.run()
