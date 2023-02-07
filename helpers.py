def get_commands(commands: []) -> str:
    message = "Hello customer!\nLooking for list commands:"
    for command in commands:
        message = message + "\n" + command
    return message
