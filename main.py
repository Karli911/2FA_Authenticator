from gui.main_gui import main
from utils.logger import setup_logger

if __name__ == "__main__":
    log_file = 'logs/app.log'
    logger = setup_logger(log_file)
    try:
        main()
    except Exception as e:
        logger.exception("Unhandled exception occurred.")