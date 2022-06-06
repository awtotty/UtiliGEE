'''Various utility functions for cleaning file paths and managing files locally
and on Google Drive. 
'''


def trim_slash_from_path(path: str) -> str:
    """Utility function to remove ending slash from directory path."""
    if path.endswith('/'): 
        return path[0:-1]
    return path


def extract_file_name_root(path: str) -> str: 
    """Utility function to remove the parent directories and file extension
    from a file path.
    """
    name = path.split('/')[-1]
    return name[0:name.rindex('.')]


def download_file_from_drive(path: str, output_path: str = None): 
    fname = extract_file_name_root(path)

    if output_path is None: 
        output_path = f'raw/{fname}'
    
    raise NotImplementedError


def upload_file_to_drive(path: str, output_path: str = None): 
    raise NotImplementedError