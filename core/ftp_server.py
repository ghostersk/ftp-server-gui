import os
import logging
import socket
import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from core.ftp_handler_parser import format_handler_info, extract_ftp_handler_info

class FTPServerThread(threading.Thread):
    def __init__(self, port, username, password, ftp_directory, log_file, log_callback=None):
        super(FTPServerThread, self).__init__()
        self.port = port
        self.username = username
        self.password = password
        self.ftp_directory = ftp_directory
        self.log_file = log_file
        self.log_callback = log_callback
        self.server = None
        self.running = False
        self.daemon = False  # Thread will exit when main program exits
        self.setup_logger()
        self.last_message = None

    def setup_logger(self):
        """Setup logger to log to file and optionally to a callback function."""
        self.logger = logging.getLogger(f"FTPServer_{self.port}")
        self.logger.setLevel(logging.INFO)

        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        self.logger.addHandler(file_handler)

    def run(self):
        if not os.path.exists(self.ftp_directory):
            os.makedirs(self.ftp_directory)

        print("FTP directory:{}".format(self.ftp_directory))

        # Set up authorizer with user authentication
        authorizer = DummyAuthorizer()
        authorizer.add_user(self.username, self.password, self.ftp_directory, perm="elradfmw")

        # Set up FTP handler
        handler = FTPHandler
        handler.authorizer = authorizer

        # Override handler log method to connect to our logger
        original_log = handler.log
        def custom_log(message, *args,**kwargs):
            self.log_message(message)
            print(message)
            #_message = extract_ftp_handler_info(message)
            #print(format_handler_info(_message))
        handler.log = custom_log

        # Create FTP server
        self.server = FTPServer(("0.0.0.0", self.port), handler)
        self.running = True
        self.log_message(f"FTP server starting on port {self.port}")
        try:
            self.server.serve_forever()
        except Exception as e:
            self.log_message(f"Server error: {str(e)}")
            print(str(e))
        finally:
            self.running = False
            self.log_message("FTP server stopped")

    def log_message(self, message):
        """Log message to file and optionally to callback function."""
        self.logger.info(message)
        if self.log_callback:
            self.log_callback(message)

    def stop(self):
        """Stop the FTP server."""
        if self.server and self.running:
            self.log_message("Stopping FTP server...")
            self.server.close_all()
            self.running = False

def get_ip_addresses():
    """Get all non-local IP addresses of the current machine."""
    ip_list = []
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if not ip.startswith("127."):
            ip_list.append(ip)
    return ip_list
