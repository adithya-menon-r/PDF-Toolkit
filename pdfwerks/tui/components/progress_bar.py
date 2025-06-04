from rich import print as printf
from rich.progress import (
    Progress,
    BarColumn,
    TimeElapsedColumn,
    TextColumn,
    SpinnerColumn,
)


class ProgressBar:
    def __init__(self, message, tasks):
        self.message = message
        self.tasks = tasks

    def run(self, work_function):
        with Progress(
            SpinnerColumn(style="bold #FFA94D"),
            TextColumn("[bold #FFD580]{task.description}"),
            BarColumn(complete_style="bold green"),
            TextColumn("[#FFECB3]{task.percentage:>5.1f}%"),
            TimeElapsedColumn(),
        ) as progress:
            task_id = progress.add_task(self.message, total=len(self.tasks))
            for task in self.tasks:
                work_function(task)
                progress.advance(task_id)

            progress.remove_task(task_id)
            printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] {self.message} completed successfully![/bold #FFD580]")
