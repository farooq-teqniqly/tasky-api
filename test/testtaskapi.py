from unittest import TestCase
from unittest.mock import MagicMock

from app import create_app
from models.taskmodel import TaskModel
from resources.taskresource import TaskResource
from respositories.taskrepository import TaskRepository
from schemas.taskschema import TaskSchema


def _get_task_model():
    return TaskModel("task-123", "foo", 1, 1, 100, 101)


def _get_task_model_json():
    task_model = _get_task_model()

    return {
        "task_id": task_model.task_id,
        "name": task_model.name,
        "priority": task_model.priority,
        "state": task_model.state,
        "start_date": task_model.start_date,
        "end_date": task_model.end_date,
        "custom_fields": task_model.custom_fields,
    }


class TaskApiGetTests(TestCase):
    def setUp(self):
        self._mock_task_repo = MagicMock(spec=TaskRepository)
        app, api = create_app()
        api.add_resource(
            TaskResource,
            "/tasks/<string:task_id>",
            resource_class_kwargs={"task_repository": self._mock_task_repo},
        )

        self._test_app = app.test_client()

    def test_get(self):
        # Arrange
        expected_task = _get_task_model()
        self._mock_task_repo.get_task.return_value = expected_task

        # Act
        response = self._test_app.get("/tasks/task-123")

        # Assert
        self.assertEqual(expected_task, TaskSchema().load(response.get_json()))
        self.assertEqual(200, response.status_code)
        self._mock_task_repo.get_task.assert_called_with("task-123")

    def test_get_when_task_not_found_returns_empty_body_and_200_status(self):
        # Arrange
        self._mock_task_repo.get_task.return_value = None

        # Act
        response = self._test_app.get("/tasks/task-123")

        # Assert
        self.assertEqual({}, response.get_json())
        self.assertEqual(200, response.status_code)

    def test_get_when_repository_error_returns_error_and_500_status(self):
        # Arrange
        self._mock_task_repo.get_task.side_effect = Exception()

        # Act
        response = self._test_app.get("/tasks/task-123")

        # Assert
        self.assertEqual({"message": "Error GETing task."}, response.get_json())
        self.assertEqual(500, response.status_code)

    @staticmethod
    def _get_task_model():
        return TaskModel("task-123", "foo", 1, 1, 100, 101)


class TaskApiPostTests(TestCase):
    def setUp(self):
        self._mock_task_repo = MagicMock(spec=TaskRepository)
        app, api = create_app()
        api.add_resource(
            TaskResource,
            "/tasks/<string:task_id>",
            resource_class_kwargs={"task_repository": self._mock_task_repo},
        )

        self._test_app = app.test_client()

    def test_post(self):
        # Arrange
        self._mock_task_repo.get_task.return_value = None
        expected_task = _get_task_model()

        # Act
        response = self._test_app.post("/tasks/task-123", json=_get_task_model_json())

        # Assert
        actual_task: TaskModel = TaskSchema().load(response.get_json())
        self.assertEqual(expected_task, actual_task)
        self.assertEqual(response.status_code, 201)

    def test_post_when_task_exists_returns_error_and_400_status(self):
        # Arrange
        self._mock_task_repo.get_task.return_value = _get_task_model()

        # Act
        response = self._test_app.post("/tasks/task-123", json=_get_task_model_json())

        # Assert
        self.assertEqual(
            {"message": f"The task with id 'task-123' already exists."},
            response.get_json(),
        )
        self.assertEqual(400, response.status_code)

    def test_post_when_create_task_fails_returns_error_and_500_status(self):
        # Arrange
        self._mock_task_repo.get_task.return_value = None
        self._mock_task_repo.create_task.side_effect = Exception()

        # Act
        response = self._test_app.post("/tasks/task-123", json=_get_task_model_json())

        # Assert
        self.assertEqual({"message": "Error POSTing task."}, response.get_json())
        self.assertEqual(500, response.status_code)

    def test_post_when_get_task_fails_returns_error_and_500_status(self):
        # Arrange
        self._mock_task_repo.get_task.side_effect = Exception()

        # Act
        response = self._test_app.post("/tasks/task-123", json=_get_task_model_json())

        # Assert
        self.assertEqual({"message": "Error POSTing task."}, response.get_json())
        self.assertEqual(500, response.status_code)

    def test_post_when_post_data_invalid_returns_400_status(self):
        # Arrange
        self._mock_task_repo.get_task.return_value = None

        # Act
        response = self._test_app.post("/tasks/task-123", json={"task_id": "foo"})

        # Assert
        self.assertEqual(400, response.status_code)


class TaskApiDeleteTests(TestCase):
    def setUp(self):
        self._mock_task_repo = MagicMock(spec=TaskRepository)
        app, api = create_app()
        api.add_resource(
            TaskResource,
            "/tasks/<string:task_id>",
            resource_class_kwargs={"task_repository": self._mock_task_repo},
        )

        self._test_app = app.test_client()

    def test_delete(self):
        # Arrange
        expected_task = _get_task_model()
        self._mock_task_repo.delete_task.return_value = expected_task

        # Act
        response = self._test_app.delete("/tasks/task-123")

        # Assert
        actual_task: TaskModel = TaskSchema().load(response.get_json())
        self.assertEqual(expected_task, actual_task)
        self.assertEqual(response.status_code, 200)

    def test_delete_when_repository_error_returns_error_and_500_status(self):
        # Arrange
        self._mock_task_repo.delete_task.side_effect = Exception()

        # Act
        response = self._test_app.delete("/tasks/task-123")

        # Assert
        self.assertEqual({"message": "Error DELETINGing task."}, response.get_json())
        self.assertEqual(500, response.status_code)
