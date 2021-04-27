from colorama import Fore, Style

__all__ = [
    "green",
    "greenb",
    "magenta",
    "magentab",
    "blue",
    "blueb",
    "bright",
    "white",
    "whiteb",
    "red",
    "redb",
    "yellow",
    "yellowb",
    "cyan",
    "cyanb",
]


def green(text: str) -> str:
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def greenb(text: str) -> str:
    return f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def magenta(text: str) -> str:
    return f"{Fore.MAGENTA}{text}{Style.RESET_ALL}"


def magentab(text: str) -> str:
    return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def blue(text: str) -> str:
    return f"{Fore.BLUE}{text}{Style.RESET_ALL}"


def blueb(text: str) -> str:
    return f"{Fore.BLUE}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def bright(text: str) -> str:
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"


def white(text: str) -> str:
    return f"{Fore.WHITE}{text}{Style.RESET_ALL}"


def whiteb(text: str) -> str:
    return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def red(text: str) -> str:
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def redb(text: str) -> str:
    return f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def yellow(text: str) -> str:
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"


def yellowb(text: str) -> str:
    return f"{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def cyan(text: str) -> str:
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"


def cyanb(text: str) -> str:
    return f"{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}"
