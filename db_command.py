from aozora import update

def main():
    commands = ['select * from books']
    for command in commands:
        update(command)


if __name__ == "__main__":
    main()