from prompt_toolkit import Application
from prompt_toolkit.styles import Style
from prompt_toolkit.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl


class ConfirmationMenu:
    def __init__(self, instruction):
        self.instruction = instruction
        self.choices = ["No", "Yes"]
        self.selected_index = 0
        self.result = None

        self.key_binding = KeyBindings()

        @self.key_binding.add("left")
        def _nav_left(event):
            self.selected_index = (self.selected_index - 1) % len(self.choices)

        @self.key_binding.add("right")
        def _nav_right(event):
            self.selected_index = (self.selected_index + 1) % len(self.choices)

        @self.key_binding.add("enter")
        def _enter(event):
            self.result = self.choices[self.selected_index] == "Yes"
            event.app.exit()

        @self.key_binding.add("c-c")
        def _exit(event):
            raise KeyboardInterrupt

        self.instr_content = FormattedTextControl([("class:instruction", self.instruction)])
        self.instr_window = Window(
            content=self.instr_content,
            height=1,
            always_hide_cursor=True,
        )

        def get_choice_fragments():
            fragments = []
            for i, choice in enumerate(self.choices):
                if i == self.selected_index:
                    fragments.append(("class:selected", f" [ {choice} ] "))
                else:
                    fragments.append(("", f" [ {choice} ] "))
                if i < len(self.choices) - 1:
                    fragments.append(("", "      "))
            return fragments

        self.choice_window = Window(
            content=FormattedTextControl(get_choice_fragments),
            height=2,
            always_hide_cursor=True,
        )

        self.layout = Layout(HSplit([self.instr_window, self.choice_window]))

        self.style = Style.from_dict({
            "instruction": "bold #FFD580",
            "selected": "bold #FFECB3 bg:black",
        })

    def run(self):
        app = Application(
            layout=self.layout,
            key_bindings=self.key_binding,
            style=self.style,
        )
        app.run()
        return self.result
