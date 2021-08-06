# based on https://github.com/willmcgugan/rich/blob/master/examples/fullscreen.py
from time import sleep
from rich.live import Live
from datetime import datetime

from rich import box
from rich.align import Align
from rich.console import Console, RenderGroup
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

import requests

console = Console()


class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Apisim[/b] Dashboard",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on red")


def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=7),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
    )
    layout["side"].split(Layout(name="statusbox"), Layout(name="box2"))
    return layout


def make_config_display(mode, loop, urls) -> Panel:
    """Some example content."""
    info = Table.grid(padding=1)
    info.add_column(style="green", justify="right")
    info.add_column(no_wrap=True)

    info.add_row(
        "Mode",
        "{}".format(mode),
    )
    info.add_row(
        "Loop",
        "{}".format(loop),
    )
    info.add_row(
        "Urls", "{}".format(urls)
    )

    intro_message = Text.from_markup(
        """Running with the following configuration;"""
    )

    message = Table.grid(padding=1)
    message.add_column()
    message.add_column(no_wrap=True)
    message.add_row(intro_message, info)

    message_panel = Panel(
        Align.center(
            RenderGroup(intro_message, "\n", Align.center(info)),
            vertical="middle",
        ),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b white]Config",
        border_style="bright_red",
    )
    return message_panel


def make_syntax() -> Syntax:
    code = """\
def ratio_resolve(total: int, edges: List[Edge]) -> List[int]:
    sizes = [(edge.size or None) for edge in edges]
    # While any edges haven't been calculated
    while any(size is None for size in sizes):
        # Get flexible edges and index to map these back on to sizes list
        flexible_edges = [
            (index, edge)
            for index, (size, edge) in enumerate(zip(sizes, edges))
            if size is None
        ]
        # Remaining space in total
        remaining = total - sum(size or 0 for size in sizes)
        if remaining <= 0:
            # No room for flexible edges
            sizes[:] = [(size or 0) for size in sizes]
            break
        # Calculate number of characters in a ratio portion
        portion = remaining / sum((edge.ratio or 1)
                                  for _, edge in flexible_edges)
        # If any edges will be less than their minimum, replace size with the minimum
        for index, edge in flexible_edges:
            if portion * edge.ratio <= edge.minimum_size:
                sizes[index] = edge.minimum_size
                break
        else:
            # Distribute flexible space and compensate for rounding error
            # Since edge sizes can only be integers we need to add the remainder
            # to the following line
            _modf = modf
            remainder = 0.0
            for index, edge in flexible_edges:
                remainder, size = _modf(portion * edge.ratio + remainder)
                sizes[index] = int(size)
            break
    # Sizes now contains integers only
    return cast(List[int], sizes)
    """
    syntax = Syntax(code, "python", line_numbers=True)
    return syntax


class dashboard:
    def __init__(self, mode: str, urls: any, repeat: int) -> None:
        super().__init__()
        self.mode = mode
        self.urls = urls
        self.repeat = repeat
        self.setup_tasks()
        self.setup_tasks_layout()
        self.setup_layout(Header(), self.progress_table, make_config_display(
            self.mode, self.loop, self.urls), self.total_progress_table)

        self.run()

    def setup_tasks(self) -> None:
        self.response_values =  "task_id: , status:"
        self.job_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        self.responses = Text(
           self.response_values,
        )
        def add_task():
            return self.job_progress.add_task("{}".format(url))

        for i in range(self.repeat):
            for url in self.urls:
                self.x = add_task()


        self.tasktotal = sum(task.total for task in self.job_progress.tasks)
        self.overall_progress = Progress()

    def setup_tasks_layout(self) -> None:
        self.overall_task = self.overall_progress.add_task(
            "All Jobs", total=int(self.tasktotal))
        self.progress_table = Table.grid(expand=True)
        self.progress_table.add_row(
            Panel(self.job_progress, title="[b]Jobs",
                  border_style="red", padding=(1, 2)),
        )
        self.progress_table.add_row(
            Panel(self.responses, title="[b]Responses",
                  border_style="red", padding=(1, 2)),
        )
        self.total_progress_table = Table.grid(expand=True)
        self.total_progress_table.add_row(
            Panel(
                self.overall_progress,
                title="Overall Progress",
                border_style="red",
                padding=(2, 2),
            ),

            Panel(
                "0",
                title="Failed jobs",
                border_style="red",
                padding=(2, 2),
            ),
            Panel(
                "0",
                title="Succeeded jobs",
                border_style="red",
                padding=(2, 2),
            ),

            Panel(
                "0",
                title="Fallback attempts",
                border_style="red",
                padding=(2, 2),
            ),
        )

    def setup_layout(self, header, body, statusbox, footer) -> None:
        self.layout = make_layout()
        self.layout["header"].update(header)
        self.layout["body"].update(body)
        self.layout["box2"].update(
            Panel(make_syntax(), border_style="green"))
        self.layout["box2"].visible = False
        self.layout["statusbox"].update(Panel(statusbox, border_style="red"))
        self.layout["footer"].update(footer)

    def run(self):
        with Live(self.layout, refresh_per_second=10, screen=True):
            while not self.overall_progress.finished:
                sleep(0.1)
                for job in self.job_progress.tasks:
                    if not job.finished:
                        res =requests.get(job.description, stream=True)
                        if res.status_code:
                            self.responses.append_text(Text("\n" + str(job.id) + " " + res.text))
                            self.job_progress.advance(job.id, 100)
                        #else:
                        #    self.job_progress.stop(job.id)

                    completed = sum(
                        task.completed for task in self.job_progress.tasks)
                    self.overall_progress.update(
                        self.overall_task, completed=completed)
            sleep(1)


if __name__ == '__main__':
    x = dashboard('get', {'https://api.agify.io?name=apisim', 'https://api.agify.io?name=apisim', 'https://api.agify.io?name=apisim', 'https://api.agify.io?name=apisim'}, 5, False)
