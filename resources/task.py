from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from models.taskmodel import TaskModel
from respositories.taskrepository import TaskRepository
from schemas.taskschema import TaskSchema


class Task(Resource):
    def __init__(self, **kwargs):
        self._task_repository: TaskRepository = kwargs["task_repository"]

    def get(self, task_id: str):
        try:
            task_model = self._task_repository.get_task(task_id)
            task_schema = TaskSchema()
            return task_schema.dump(task_model), 200
        except:
            return {"message": "Error GETing task."}, 500

    def post(self, task_id: str):
        if self._task_repository.get_task(task_id) is not None:
            return {"message": f"The task with id '{task_id}' already exists."}, 400

        try:
            task_schema = TaskSchema()
            task_model: TaskModel = task_schema.load(request.get_json())
            task_model.task_id = task_id
            self._task_repository.create_task(task_model)
            return task_schema.dump(task_model), 201
        except ValidationError as err:
            return err.messages, 400
        except:
            return {"message": "Error POSTing task."}, 500

    def delete(self, task_id: str):
        try:
            task_schema = TaskSchema()
            task_model = self._task_repository.delete_task(task_id)
            return task_schema.dump(task_model), 200
        except:
            return {"message": "Error DELETINGing task."}, 500
