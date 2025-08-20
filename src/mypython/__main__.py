"""Main entry point for the mypython package."""


def main() -> str:
    """Return a greeting message.

    Returns:
        str: A greeting message from mypython.
    """
    return "Hello from mypython!"


if __name__ == "__main__":
    s = main()
    print(s)
