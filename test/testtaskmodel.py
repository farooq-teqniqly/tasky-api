from unittest import TestCase

from models.taskmodel import TaskModel


class TaskModelTests(TestCase):
    def test_create_when_sub_task_not_TaskModel_raises_ValueError(self):
        # Arrange, Act, Assert
        with self.assertRaises(ValueError):
            TaskModel("task-123", "foo", 1, 2, 100, 101, sub_tasks=[{"bar": "baz"}])

    def test_create_with_sub_tasks(self):
        # Arrange
        sub_tasks = [
            TaskModel("task-123", "foo", 1, 2, 100, 101),
            TaskModel("task-456", "bar", 2, 4, 101, 102),
        ]

        # Act
        task_model = TaskModel("task-000", "qux", 0, 0, 0, 0, sub_tasks=sub_tasks)

        # Assert
        self.assertEqual(task_model.sub_tasks, sub_tasks)

    def test_TaskModels_not_equal(self):
        # Arrange
        task_model1 = TaskModel("task-000", "qux", 0, 0, 0, 0)
        task_model2 = {"task_id": "task-000"}

        # Act and Assert
        self.assertNotEqual(task_model1, task_model2)
