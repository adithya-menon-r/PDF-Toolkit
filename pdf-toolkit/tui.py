from rich import print as printf
from prompt_toolkit import Application
from prompt_toolkit.styles import Style
from prompt_toolkit.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TextColumn, SpinnerColumn

class SelectionMenu:
    def __init__(self, message, choices):
        self.message = message
        self.choices = choices
        self.selected_index = 0
        self.result = None

        self.key_binding = KeyBindings()

        @self.key_binding.add("up")
        def nav_up(event):
            if self.selected_index > 0:
                self.selected_index -= 1
            else:
                self.selected_index = len(self.choices) - 1

        @self.key_binding.add("down")
        def nav_down(event):
            if self.selected_index < len(self.choices) - 1:
                self.selected_index += 1
            else:
                self.selected_index = 0

        @self.key_binding.add("enter")
        def select(event):
            self.result = self.choices[self.selected_index]
            event.app.exit()

        self.msg_content = FormattedTextControl([("class:message", self.message)])
        self.msg_window = Window(
            content=self.msg_content,
            height=1,
            always_hide_cursor=True
        )

        def get_menu_fragments():
            fragments = []
            for i, choice in enumerate(self.choices):
                if i == self.selected_index:
                    fragments.append(("class:arrow", "> "))
                    fragments.append(("class:selected", f" {choice} \n"))
                else:
                    fragments.append(("", f"  {choice} \n"))
            return fragments

        self.menu_content = FormattedTextControl(get_menu_fragments)
        self.menu_window = Window(
            content=self.menu_content,
            always_hide_cursor=True
        )

        container = HSplit([
            self.msg_window,
            self.menu_window
        ])

        self.layout = Layout(
            container,
            focused_element=self.menu_window
        )

        self.style = Style.from_dict({
            "message": "bold #FFD580",
            "arrow": "bold #FFAA66",
            "selected": "bold #FFECB3 bg:black",
        })

    def run(self):
        app = Application(
            layout=self.layout,
            key_bindings=self.key_binding,
            style=self.style
        )
        app.run()
        return self.result


class ReorderMenu:
    def __init__(self, message, items):
        self.message = message
        self.items = list(items)
        self.cursor_index = 0
        self.selected_index = None
        self.moving = False

        self.key_binding = KeyBindings()

        @self.key_binding.add("up")
        def nav_up(event):
            if self.moving:
                if self.cursor_index > 0:
                    self.items[self.cursor_index], self.items[self.cursor_index - 1] = self.items[self.cursor_index - 1], self.items[self.cursor_index]
                    self.cursor_index -= 1
                    self.selected_index -= 1
            else:
                if self.cursor_index > 0:
                    self.cursor_index -= 1
                else:
                    self.cursor_index = len(self.items) - 1

        @self.key_binding.add("down")
        def nav_down(event):
            if self.moving:
                if self.cursor_index < len(self.items) - 1:
                    self.items[self.cursor_index], self.items[self.cursor_index + 1] = self.items[self.cursor_index + 1], self.items[self.cursor_index]
                    self.cursor_index += 1
                    self.selected_index += 1
            else:
                if self.cursor_index < len(self.items) - 1:
                    self.cursor_index += 1
                else:
                    self.cursor_index = 0

        @self.key_binding.add(" ")
        def select(event):
            if not self.moving:
                self.moving = True
                self.selected_index = self.cursor_index
            else:
                self.moving = False
                self.selected_index = None

        @self.key_binding.add("enter")
        def confirm(event):
            event.app.exit(result=self.items)

        self.msg_content = FormattedTextControl([("class:message", self.message)])
        self.msg_window = Window(
            content=self.msg_content,
            height=1,
            always_hide_cursor=True
        )

        def get_menu_fragments():
            fragments = []
            for i, item in enumerate(self.items):
                if i == self.cursor_index:
                    if self.moving:
                        fragments.append(("class:moving_arrow", "⇅ "))
                        fragments.append(("class:moving", f"[ {item} ]\n"))
                    else:
                        fragments.append(("class:arrow", "> "))
                        fragments.append(("class:selected", f" {item} \n"))
                else:
                    fragments.append(("", f"  {item}\n"))
            return fragments

        self.menu_content = FormattedTextControl(get_menu_fragments)
        self.menu_window = Window(
            content=self.menu_content,
            always_hide_cursor=True
        )

        container = HSplit([
            self.msg_window,
            self.menu_window
        ])

        self.layout = Layout(
            container,
            focused_element=self.menu_window
        )

        self.style = Style.from_dict({
            "message": "bold #FFD580",
            "arrow": "bold #FFAA66",
            "selected": "bold #FFECB3 bg:black",
            "moving_arrow": "#FFAA66",
            "moving": "bold black bg:#FFE082"
        })

    def run(self):
        app = Application(
            layout=self.layout,
            key_bindings=self.key_binding,
            style=self.style
        )
        return app.run()


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
            TimeElapsedColumn()
        ) as progress:
            task_id = progress.add_task(self.message, total=len(self.tasks))
            for task in self.tasks:
                work_function(task)
                progress.advance(task_id)

            progress.remove_task(task_id)
            printf(f"[#A3BE8C]✔[/#A3BE8C] [bold #FFD580] {self.message} completed successfully!")
