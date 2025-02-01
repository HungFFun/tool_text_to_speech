from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

from src.gui.app import App


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
