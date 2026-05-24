class Task:

    def __init__(
        self,
        task_id,
        capability,
        params,
        dependencies
    ):

        self.task_id = task_id
        self.capability = capability
        self.params = params
        self.dependencies = dependencies

    def __repr__(self):

        return (
            f"Task("
            f"id={self.task_id}, "
            f"capability={self.capability}, "
            f"params={self.params}, "
            f"deps={self.dependencies}"
            f")"
        )