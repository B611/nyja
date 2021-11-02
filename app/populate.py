import os
import sys


def next_startup():
    save = input("Do you want to be prompted again at next startup ? (y/n)\n")
    if save == "y":
        exit()
    elif save == "n":
        with open("/app/.nopopulateprompt", "w") as config:
            config.write("Delete me to be prompted for initial populate on startup")
    else:
        next_startup()


def populate_prompt():
    inp = input("Do you want to populate the database with the default nyja indexers ? (y/n)\n")
    if inp == 'y':
        populate()
    elif inp == 'n':
        next_startup()
    else:
        populate_prompt()


def populate():
    if os.path.isfile("nyja.py"):
        os.system("python nyja.py crawl /app/user_dir/indexers")
        os.system("python nyja.py metadata")
    else:
        os.system("nyja crawl /app/user_dir/indexers")
        os.system("nyja metadata")


def main():
    if len(sys.argv) == 2 and (sys.argv[1] == "--force" or sys.argv[1] == "-f"):  # CLI mode
        populate()
    else:
        try:
            with open("/app/.nopopulateprompt", "r") as config:
                exit()
        except FileNotFoundError:
            populate_prompt()


if __name__ == '__main__':
    main()
