from prompt_toolkit import Application
from prompt_toolkit.styles import Style
from prompt_toolkit.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl


class ReorderMenu:
    def __init__(self, message, items):
        self.message = message
        self.items = list(items)
        self.cursor_index = 0
        self.selected_index = None
        self.moving = False

        self.key_binding = KeyBindings()

        @self.key_binding.add("up")
        def _nav_up(event):
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
        def _nav_down(event):
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
        def _select(event):
            if not self.moving:
                self.moving = True
                self.selected_index = self.cursor_index
            else:
                self.moving = False
                self.selected_index = None

        @self.key_binding.add("enter")
        def _confirm(event):
            event.app.exit(result=self.items)

        @self.key_binding.add("c-c")
        def _exit(event):
            raise KeyboardInterrupt

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
        self.menu_window = Window(content=self.menu_content, always_hide_cursor=True)

        container = HSplit([self.msg_window, self.menu_window])

        self.layout = Layout(container, focused_element=self.menu_window)

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
