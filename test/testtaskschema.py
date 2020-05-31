from unittest import TestCase

from models.taskmodel import TaskModel
from schemas.taskschema import TaskSchema


class TaskSchemaTests(TestCase):
    def test_make_task_model_sets_placeholder_task_id(self):
        # Arrange
        task_json = {
            "name": "foo",
            "priority": 0,
            "state": 0,
            "start_date": 0,
            "end_date": 0,
            "custom_fields": {},
        }

        # Act
        task_model: TaskModel = TaskSchema().load(task_json)

        # Assert
        self.assertEqual("placeholder", task_model.task_id)
