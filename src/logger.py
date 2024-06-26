import glob
import logging
import multiprocessing as mp
import os
from datetime import datetime


def get_logger():
    current_process_name = mp.current_process().name
    logger = logging.getLogger(current_process_name)

    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(_get_formatter())
        logger.addHandler(stream_handler)

        if current_process_name == "BotProcess":
            file_handler = logging.FileHandler(
                os.path.join(get_session_log_folder_path(), f"{current_process_name}_{_get_timestamp()}.log") 
            )
        else:
            file_handler = logging.FileHandler(
                os.path.join(get_session_log_folder_path(), f"{current_process_name}.log")
            )
        file_handler.setFormatter(_get_formatter())
        logger.addHandler(file_handler)
            
    return logger


def get_session_log_folder_path():
    session_file_name = _get_session_file_name()
    name_parts = session_file_name.split(".")
    session_file_name = f"{name_parts[1]}_{name_parts[0]}"
    return os.path.join(MASTER_LOGS_DIR_PATH, session_file_name) 


def _get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]


def _get_formatter():
    return logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def _get_session_file_name():
    """Get the name of the newest session file and delete the rest.""" 
    session_files = glob.glob(os.path.join(MASTER_LOGS_DIR_PATH, '*.session'))
    if not session_files:
        raise FileNotFoundError(f"No session file in: {MASTER_LOGS_DIR_PATH}")
    session_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    for session_file in session_files[1:]:
        os.remove(session_file)
    return os.path.basename(session_files[0])

# ----------------------------

MASTER_LOGS_DIR_PATH = os.path.join(os.getcwd(), "logs")
if not os.path.exists(MASTER_LOGS_DIR_PATH):
    os.mkdir(MASTER_LOGS_DIR_PATH)

if mp.current_process().name == "MainProcess":
    # Create a new session file.
    with open(os.path.join(MASTER_LOGS_DIR_PATH, _get_timestamp() + ".session"), "w") as f:
        pass
    # Create a new session log folder.
    folder_path = get_session_log_folder_path()
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

# ----------------------------

if __name__ == "__main__":
    log = get_logger()
    log.info("Hello World!")
