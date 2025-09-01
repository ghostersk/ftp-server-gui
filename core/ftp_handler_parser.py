def extract_ftp_handler_info(handler):
    """
    Extract information directly from an FTPHandler object.
    
    Args:
        handler: The FTPHandler object
        
    Returns:
        dict: Extracted information in a structured format
    """
    info = {
        "session_id": str(id(handler)),
        "client_address": f"{handler.remote_ip}:{handler.remote_port}",
        "user": handler.username if hasattr(handler, 'username') else "Not authenticated",
        "current_file": getattr(handler, 'current_file', 'None'),
        "bytes_transferred": getattr(handler, 'bytes_transferred', 0),
        "status": "Active"
    }
    
    # Check if currently transferring a file
    if hasattr(handler, 'file_obj') and handler.file_obj:
        info['status'] = "Transfer in progress"
        info['current_file'] = getattr(handler.file_obj, 'name', 'Unknown file')
    
    return info

def format_handler_info(handler_info):
    """
    Format handler information into a human-readable string.
    
    Args:
        handler_info (dict): Information about the FTP handler
        
    Returns:
        str: Formatted human-readable information
    """
    output = [
        "FTP Session Details:",
        f"  Session ID: {handler_info['session_id']}",
        f"  Client: {handler_info['client_address']}",
        f"  User: {handler_info['user']}",
        f"  Current File: {handler_info['current_file']}",
        f"  Bytes Transferred: {handler_info['bytes_transferred']} bytes",
        f"  Status: {handler_info['status']}"
    ]
    
    return "\n".join(output)
