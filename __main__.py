
from core.args import get_arguments
if __name__ == '__main__':
    arguments = get_arguments()
    if "TUI" == arguments.mode:
        print("starting FTP server in TUI mode.")
        
        from tui.tui import TUI
        app = TUI()
        app.run()
    if "GUI" == arguments.mode:
        print("starting FTP server in GUI mode.")
