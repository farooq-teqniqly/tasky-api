import os
from typing import Tuple

from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from resources.taskresource import TaskResource
from respositories.taskrepository import TaskRepository


def create_app(env: str = "development") -> Tuple[Flask, Api]:
    flask_app = Flask(__name__)
    api = Api(flask_app)

    if env.lower() == "production":
        task_repository = TaskRepository()

        api.add_resource(
            TaskResource,
            "/tasks/<string:task_id>",
            resource_class_kwargs={"task_repository": task_repository},
        )

    return flask_app, api


if __name__ == "__main__":
    load_dotenv()
    app = create_app(os.getenv("flask_environment"))[0]
    app.run()
