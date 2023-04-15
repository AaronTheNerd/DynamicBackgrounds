def progress_bar(t: float, width: int = 30) -> None:
    full = round(t * width)
    print(f" |{full * '▮'}{(width - full) * ' '}| {round(t * 100, 1)}%", end="\r")
