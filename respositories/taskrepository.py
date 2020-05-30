from typing import List, Union

from models.taskmodel import TaskModel


class TaskRepository:
    def __init__(self):
        self._tasks: List[TaskModel] = []

    def create_task(self, task_model: TaskModel):
        self._tasks.append(task_model)

    def get_task(self, task_id: str) -> Union[TaskModel, None]:
        task = list(filter(lambda t: t.task_id == task_id, self._tasks))

        if not task:
            return None
        else:
            return task[0]

    def delete_task(self, task_id: str) -> Union[TaskModel, None]:
        task = self.get_task(task_id)

        if task is None:
            return None

        self._tasks.remove(task)
        return task
