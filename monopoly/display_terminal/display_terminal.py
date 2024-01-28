"""the module for displaying the game on the terminal."""


def query_yes_no(question: str, default: str = "yes") -> bool:
    """
    Return True if the user answers yes, False otherwise.

    Args:
    ----
        question (str): question to ask the user
        default (str, optional): the presumed answer
                                if the user just hits <Enter>. Defaults to "yes".

    Raises:
    ------
        ValueError: if the default is not yes or no

    Returns:
    -------
        bool: True for yes, False for no
    """
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        error_msg = f"invalid default answer: '{default}'"
        raise ValueError(error_msg)

    while True:
        print(question + prompt)
        choice = input().lower()
        if "yes".startswith(choice):
            return True
        if "no".startswith(choice):
            return False
        print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
