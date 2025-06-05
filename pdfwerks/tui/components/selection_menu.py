from prompt_toolkit import Application
from prompt_toolkit.styles import Style
from prompt_toolkit.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl


class SelectionMenu:
    def __init__(self, instruction, choices, choice_messages=None, default_select=0):
        self.instruction = instruction
        self.choices = choices
        self.choice_messages = choice_messages or []
        self.selected_index = default_select
        self.result = None

        self.key_binding = KeyBindings()

        @self.key_binding.add("up")
        def _nav_up(event):
            if self.selected_index > 0:
                self.selected_index -= 1
            else:
                self.selected_index = len(self.choices) - 1

        @self.key_binding.add("down")
        def _nav_down(event):
            if self.selected_index < len(self.choices) - 1:
                self.selected_index += 1
            else:
                self.selected_index = 0

        @self.key_binding.add("enter")
        def _select(event):
            self.result = self.choices[self.selected_index]
            event.app.exit()

        @self.key_binding.add("c-c")
        def _exit(event):
            raise KeyboardInterrupt

        self.instr_content = FormattedTextControl([("class:instruction", self.instruction)])
        self.instr_window = Window(
            content=self.instr_content,
            height=1,
            always_hide_cursor=True
        )

        def get_menu_fragments():
            fragments = []
            for i, choice in enumerate(self.choices):
                if i == self.selected_index:
                    fragments.append(("class:arrow", "> "))
                    fragments.append(("class:selected", f" {choice} "))
                    if choice_messages:
                        fragments.append(("class:message", f" : {choice_messages[i]}\n"))
                    else:
                        fragments.append(("", "\n"))
                else:
                    fragments.append(("", f"  {choice} \n"))
            return fragments

        self.menu_content = FormattedTextControl(get_menu_fragments)
        self.menu_window = Window(content=self.menu_content, always_hide_cursor=True)

        container = HSplit([self.instr_window, self.menu_window])

        self.layout = Layout(container, focused_element=self.menu_window)

        self.style = Style.from_dict({
            "instruction": "bold #FFD580",
            "arrow": "bold #FFAA66",
            "selected": "bold #FFECB3 bg:black",
            "message": "italic #444444"
        })

    def run(self):
        app = Application(
            layout=self.layout,
            key_bindings=self.key_binding,
            style=self.style
        )
        app.run()
        return self.result
