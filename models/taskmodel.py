class TaskModel:
    def __init__(
        self,
        task_id: str,
        name: str,
        priority: int,
        state: int,
        start_date: int,
        end_date: int,
        custom_fields: dict = {},
        sub_tasks: list = [],
    ):
        self.task_id = task_id
        self.name = name
        self.priority = priority
        self.state = state
        self.start_date = start_date
        self.end_date = end_date
        self.custom_fields = custom_fields
        self.sub_tasks = sub_tasks

        for sub_task in sub_tasks:
            if not isinstance(sub_task, TaskModel):
                raise ValueError("Sub-tasks must be an instance of TaskModel.")

    def __eq__(self, other):
        if not isinstance(other, TaskModel):
            return False

        return self.task_id == other.task_id
