import os
import logging
import socket
import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

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
        self.daemon = True  # Thread will exit when main program exits
        self.setup_logger()

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

        # Set up authorizer with user authentication
        authorizer = DummyAuthorizer()
        authorizer.add_user(self.username, self.password, self.ftp_directory, perm="elradfmw")

        # Set up FTP handler
        handler = FTPHandler
        handler.authorizer = authorizer

        # Override handler log method to connect to our logger
        original_log = handler.log
        def custom_log(message, logfun=None):
            original_log(message, logfun)
            self.log_message(message)
        handler.log = custom_log

        # Create FTP server
        self.server = FTPServer(("0.0.0.0", self.port), handler)
        self.running = True
        self.log_message(f"FTP server starting on port {self.port}")
        try:
            self.server.serve_forever()
        except Exception as e:
            self.log_message(f"Server error: {str(e)}")
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

# Example usage
"""
if __name__ == "__main__":
    def print_log(message):
        print(f"FTP Log: {message}")
    
    # Create and start FTP server
    ftp_thread = FTPServerThread(
        port=2121,
        username="user",
        password="password",
        ftp_directory="./ftp_root",
        log_file="./ftp_server.log",
        log_callback=print_log
    )
    
    ftp_thread.start()
    print(f"FTP server started on port 2121")
    print(f"Connect using: ftp://user:password@localhost:2121")
    
    try:
        # Keep the server running until interrupted
        while ftp_thread.running:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("Shutting down FTP server...")
        ftp_thread.stop()
        ftp_thread.join()
        print("FTP server stopped")
"""
