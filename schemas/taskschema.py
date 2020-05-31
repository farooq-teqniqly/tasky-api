from marshmallow import Schema, fields, post_load

from models.taskmodel import TaskModel


class TaskSchema(Schema):

    task_id = fields.Str(required=False)
    name = fields.Str(required=True)
    priority = fields.Int(required=True)
    state = fields.Int(required=True)
    start_date = fields.Int(required=True)
    end_date = fields.Int(required=True)
    custom_fields = fields.Dict(required=False)
    sub_tasks = fields.List(fields.Nested(lambda: TaskSchema()))

    @post_load
    def make_task_model(self, data, **kwargs):
        if data.get("task_id") is None:
            data["task_id"] = "placeholder"
        return TaskModel(**data)
