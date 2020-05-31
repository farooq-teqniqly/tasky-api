from unittest import TestCase
from unittest.mock import MagicMock

from models.taskmodel import TaskModel
from resources.taskresource import TaskResource
from respositories.taskrepository import TaskRepository
from schemas.taskschema import TaskSchema


class TaskResourceTests(TestCase):
    def setUp(self):
        self._mock_task_repo = MagicMock(spec=TaskRepository)

    def test_get(self):
        # Arrange
        expected_task = TaskResourceTests._get_task_model()
        self._mock_task_repo.get_task.return_value = expected_task
        task_resource = TaskResource(task_repository=self._mock_task_repo)

        # Act
        response = task_resource.get("task-123")

        # Assert
        self.assertEqual(expected_task, TaskSchema().load(response[0]))
        self.assertEqual(200, response[1])
        self._mock_task_repo.get_task.assert_called_with("task-123")

    def test_get_when_task_not_found_returns_empty_body_and_200_status(self):
        # Arrange
        self._mock_task_repo.get_task.return_value = None
        task_resource = TaskResource(task_repository=self._mock_task_repo)

        # Act
        response = task_resource.get("task-123")

        # Assert
        self.assertEqual({}, response[0])
        self.assertEqual(200, response[1])

    def test_get_when_repository_error_returns_error_and_500_status(self):
        # Arrange
        self._mock_task_repo.get_task.side_effect = Exception()
        task_resource = TaskResource(task_repository=self._mock_task_repo)

        # Act
        response = task_resource.get("task-123")

        # Assert
        self.assertEqual({"message": "Error GETing task."}, response[0])
        self.assertEqual(500, response[1])

    @staticmethod
    def _get_task_model():
        return TaskModel("task-123", "foo", 1, 1, 100, 101)
