"""Shared CLI-TUI rendering and prompt helpers for CustomRallyDash tools."""

from __future__ import annotations

import io
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Iterator, Sequence

try:
    import questionary
except ImportError:  # pragma: no cover - optional fallback before install
    questionary = None  # type: ignore[assignment]

try:
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.rule import Rule
    from rich.table import Table
    from rich.text import Text
except ImportError:  # pragma: no cover - optional fallback before install
    box = None  # type: ignore[assignment]
    Console = None  # type: ignore[assignment,misc]
    Panel = None  # type: ignore[assignment,misc]
    Rule = None  # type: ignore[assignment,misc]
    Table = None  # type: ignore[assignment,misc]
    Text = None  # type: ignore[assignment,misc]

InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], Any]

ACCENT_STYLE = "bright_cyan"

STATUS_MAP: dict[str, tuple[str, str]] = {
    "ok": ("[OK]", "green"),
    "warn": ("[!]", "yellow"),
    "err": ("[X]", "red"),
    "info": ("[*]", ACCENT_STYLE),
}

_QUESTIONARY_STYLE = (
    questionary.Style(
        [
            ("qmark", "fg:ansibrightcyan bold"),
            ("question", "bold"),
            ("answer", "fg:ansibrightcyan bold"),
            ("pointer", "fg:ansibrightcyan bold"),
            ("highlighted", "fg:ansibrightcyan bold"),
            ("selected", "fg:ansibrightcyan"),
            ("instruction", "fg:ansibrightblack"),
        ]
    )
    if questionary is not None
    else None
)


class UserCancelled(Exception):
    """Raised when the user cancels an interactive terminal prompt."""


@dataclass(frozen=True)
class ChoiceItem:
    """Single choice entry pairing an internal value with display text."""

    value: str
    label: str
    aliases: tuple[str, ...] = ()


class CliUI:
    """Thin terminal UI facade with Rich styling, arrow-key prompts, and fallback."""

    def __init__(
        self,
        input_fn: InputFunction = input,
        output_fn: OutputFunction = print,
    ) -> None:
        self.input_fn = input_fn
        self.output_fn = output_fn
        self._is_stdout = output_fn is print
        self._has_rich = Console is not None
        self._stdout_console = (
            Console(highlight=False)
            if (self._is_stdout and Console is not None)
            else None
        )

    @property
    def interactive(self) -> bool:
        """Return True when running attached to an interactive TTY."""
        return (
            self.input_fn is input
            and self._is_stdout
            and sys.stdin.isatty()
            and sys.stdout.isatty()
        )

    @property
    def has_arrow_menus(self) -> bool:
        """Return True when questionary arrow-key menus can be used safely."""
        return self.interactive and questionary is not None

    def _emit(self, renderable: Any, fallback_lines: Sequence[str] = ()) -> None:
        """Print a Rich renderable to stdout or render plain text to output_fn."""
        if self._stdout_console is not None:
            self._stdout_console.print(renderable)
            return

        if Console is not None:
            buffer = io.StringIO()
            plain_console = Console(
                file=buffer,
                no_color=True,
                highlight=False,
                width=120,
                legacy_windows=False,
            )
            plain_console.print(renderable)
            for line in buffer.getvalue().rstrip("\n").splitlines():
                self.output_fn(line)
            return

        for line in fallback_lines:
            self.output_fn(line)

    def blank(self) -> None:
        """Emit an empty line."""
        if self._stdout_console is not None:
            self._stdout_console.print()
        else:
            self.output_fn("")

    def banner(self, title: str, warning: str | None = None) -> None:
        """Render a sharp single-line header box with an optional warning line."""
        clean_warning = warning.strip() if warning else None
        fallback = [title] + ([f"[!] {clean_warning}"] if clean_warning else [])
        if Panel is None or Text is None or box is None:
            for line in fallback:
                self.output_fn(line)
            return

        body = Text(title, style=f"bold {ACCENT_STYLE}")
        if clean_warning:
            body.append("\n")
            body.append("[!] ", style="yellow bold")
            body.append(clean_warning, style="yellow")

        self.blank()
        self._emit(
            Panel(
                body,
                box=box.SQUARE,
                border_style="dim",
                expand=False,
                padding=(0, 2),
            ),
            fallback,
        )

    def header_line(self, title: str, meta: str | None = None) -> None:
        """Render a compact single-line header followed by a subtle divider."""
        fallback = [f"{title}  ({meta})" if meta else title, "-" * 70]
        if Text is None or Rule is None:
            for line in fallback:
                self.output_fn(line)
            return

        line = Text(title, style=f"bold {ACCENT_STYLE}")
        if meta:
            line.append(f"  ({meta})", style="dim")
        self._emit(line)
        self._emit(Rule(style="dim"))

    def step(self, current: int, total: int, label: str) -> None:
        """Render a compact numbered section rule like [1/4] Network."""
        fallback = [f"\n[{current}/{total}] {label}"]
        if Rule is None:
            self.output_fn(fallback[0])
            return

        self.blank()
        self._emit(
            Rule(
                title=f"[{ACCENT_STYLE}][{current}/{total}][/{ACCENT_STYLE}] "
                f"[bold]{label}[/bold]",
                align="left",
                style="dim",
            ),
            fallback,
        )

    def table(
        self,
        title: str | None,
        headers: Sequence[str],
        rows: Sequence[Sequence[Any]],
        col_styles: Sequence[str] | None = None,
    ) -> None:
        """Render a clean borderless horizontal-header table."""
        if Table is None or box is None:
            if title:
                self.output_fn(title)
            for row in rows:
                self.output_fn(" | ".join(str(cell) for cell in row))
            return

        tbl = Table(
            title=Text(title, style="bold") if title and Text is not None else title,
            title_justify="left",
            box=box.SIMPLE_HEAD,
            show_header=bool(headers),
            header_style="bold",
            border_style="dim",
            padding=(0, 2, 0, 0),
        )
        for idx, header in enumerate(headers):
            style = col_styles[idx] if col_styles and idx < len(col_styles) else ""
            tbl.add_column(header, style=style, no_wrap=(idx == 0))

        for row in rows:
            tbl.add_row(*row)
        self._emit(tbl)

    def status(self, kind: str, message: str, detail: str | None = None) -> None:
        """Print a status line prefixed with [OK], [!], [X], or [*]."""
        tag, color = STATUS_MAP.get(kind, ("[*]", ACCENT_STYLE))
        plain = f"{tag} {message}" + (f" ({detail})" if detail else "")
        if Text is None:
            self.output_fn(plain)
            return

        text = Text.assemble((f"{tag} ", f"bold {color}"), (message, ""))
        if detail:
            text.append(f" ({detail})", style="dim")
        self._emit(text, [plain])

    def bullet(self, text: str, style: str = "dim") -> None:
        """Print an indented bullet line."""
        if Text is None:
            self.output_fn(f"    - {text}")
            return
        self._emit(Text(f"    - {text}", style=style))

    def command_hint(self, label: str, command: str) -> None:
        """Print a labelled command with bright_cyan command highlighting."""
        if Text is None:
            self.output_fn(f"  {label}: {command}")
            return
        self._emit(
            Text.assemble(("  ", ""), (f"{label} ", "dim"), (command, ACCENT_STYLE))
        )

    @contextmanager
    def wait_status(self, message: str) -> Iterator[None]:
        """Display an ASCII spinner on TTY stdout, or log once in non-TTY mode."""
        if (
            self._stdout_console is not None
            and sys.stdout.isatty()
            and self.output_fn is print
        ):
            with self._stdout_console.status(
                f"[{ACCENT_STYLE}]{message}[/{ACCENT_STYLE}]",
                spinner="line",
            ):
                yield
            return

        self.status("info", message)
        yield

    def ask_text(self, prompt: str, default: str | None = None) -> str:
        """Read a line of text using styled console input when interactive."""
        suffix = f" [{default}]" if default is not None else ""
        plain_prompt = f"{prompt}{suffix}: "
        if self.interactive and self._stdout_console is not None and Text is not None:
            styled = Text.assemble(
                ("? ", f"bold {ACCENT_STYLE}"),
                (prompt, "bold"),
                (suffix, "dim") if suffix else ("", ""),
                (": ", ""),
            )
            try:
                return self._stdout_console.input(styled)
            except (EOFError, KeyboardInterrupt) as error:
                raise UserCancelled from error

        try:
            return self.input_fn(plain_prompt)
        except (EOFError, KeyboardInterrupt) as error:
            raise UserCancelled from error

    def ask_select(
        self,
        prompt: str,
        choices: Sequence[ChoiceItem],
        default: str,
        invalid_message: str,
        instruction: str = "(↑/↓, Enter)",
        allow_empty_default: bool = True,
        fallback_prompt: str | None = None,
    ) -> str:
        """Select one option with arrow keys on TTY or fallback input loop."""
        if self.has_arrow_menus:
            q_choices = [
                questionary.Choice(title=item.label, value=item.value) for item in choices
            ]
            default_choice = next(
                (item for item in q_choices if item.value == default),
                q_choices[0] if q_choices else None,
            )
            answer = questionary.select(
                prompt,
                choices=q_choices,
                default=default_choice,
                qmark="?",
                pointer=">",
                style=_QUESTIONARY_STYLE,
                instruction=instruction,
            ).ask()
            if answer is None:
                raise UserCancelled
            return str(answer)

        if fallback_prompt is not None:
            prompt_text = fallback_prompt
        else:
            choice_keys = "/".join(item.value for item in choices)
            prompt_text = f"{prompt} ({choice_keys}) [{default}]: "

        while True:
            try:
                raw = self.input_fn(prompt_text).strip().lower()
            except (EOFError, KeyboardInterrupt) as error:
                raise UserCancelled from error

            if not raw and allow_empty_default:
                return default

            for item in choices:
                valid = {item.value.lower(), *(alias.lower() for alias in item.aliases)}
                if raw in valid:
                    return item.value

            self.status("err", invalid_message)

    def ask_yes_no(
        self,
        prompt: str,
        default: bool,
        yes_label: str,
        no_label: str,
        yes_short: str,
        no_short: str,
        invalid_message: str,
        instruction: str = "(↑/↓, Enter)",
    ) -> bool:
        """Ask a yes/no confirmation with arrow keys on TTY or Y/N text fallback."""
        if self.has_arrow_menus:
            yes_choice = questionary.Choice(title=yes_label, value="yes")
            no_choice = questionary.Choice(title=no_label, value="no")
            answer = questionary.select(
                prompt,
                choices=[yes_choice, no_choice],
                default=yes_choice if default else no_choice,
                qmark="?",
                pointer=">",
                style=_QUESTIONARY_STYLE,
                instruction=instruction,
            ).ask()
            if answer is None:
                raise UserCancelled
            return answer == "yes"

        default_text = yes_short if default else no_short
        prompt_text = f"{prompt} ({yes_short}/{no_short}) [{default_text}]: "
        while True:
            try:
                answer = self.input_fn(prompt_text).strip().lower()
            except (EOFError, KeyboardInterrupt) as error:
                raise UserCancelled from error

            if not answer:
                return default
            if answer in {"y", "yes", "e", "evet", "1", "true"}:
                return True
            if answer in {"n", "no", "h", "hayır", "hayir", "0", "false"}:
                return False
            self.status("err", invalid_message)
