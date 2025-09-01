from core.ftp_server import FTPServerThread, get_ip_addresses


class TUI:
    def __init__(self):
        self.ftp_thread = FTPServerThread(
        port=2121,
        username="user",
        password="password",
        ftp_directory="./ftp_root",
        log_file="./ftp_server.log"
    )


    def run(self):
        self.ftp_thread.start()
        print(f"FTP server started on port 2121")
        print(f"Connect using: ftp://user:password@localhost:2121")
    
        try:
            # Keep the server running until interrupted
            while self.ftp_thread.running:
                threading.Event().wait(1)
        except KeyboardInterrupt:
            print("Shutting down FTP server...")
            self.ftp_thread.stop()
            self.ftp_thread.join()
            print("FTP server stopped")



