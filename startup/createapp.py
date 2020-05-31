from typing import Tuple

from flask import Flask
from flask_restful import Api

from resources.taskresource import TaskResource
from respositories.taskrepository import TaskRepository


def create_app_and_api(env: str = "development") -> Tuple[Flask, Api]:
    flask_app = Flask(__name__)
    flask_api = Api(flask_app)

    if env and env.lower() == "production":
        task_repository = TaskRepository()

        flask_api.add_resource(
            TaskResource,
            "/tasks/<string:task_id>",
            resource_class_kwargs={"task_repository": task_repository},
        )

    return flask_app, flask_api
