import logging
import io
import os
import sys
import warnings
import utils.colored_formatter as cf

class Logger:
    """Manage logging"""
    _logger_level = None
    _format = "[%(asctime)s] %(levelname)-10s %(message)s"
    _formatter =  logging.Formatter(_format)   
    _log_contents = io.StringIO()
    _current_log_file_path = "info.log"
    _output = ""  # intercepted output from stdout and stderr
    string_handler = None
    file_handler = None
    console_handler = None
    logger = None
    
    @staticmethod
    def debug(data: str, hl = False):
        if Logger.logger is None:
            Logger.init()
            
        if hl:
            data = cf.format_bold(cf.format_green(data))  
             
        Logger.logger.debug(data)
    
    @staticmethod
    def info(data: str, hl = False):
        if Logger.logger is None:
            Logger.init()
            
        if hl:
            data = cf.format_bold(cf.format_green(data)) 
            
        Logger.logger.info(data)

    @staticmethod
    def warning(data: str, hl = False):
        if Logger.logger is None:
            Logger.init()
            
        if hl:
            data = cf.format_bold(cf.format_green(data)) 
            
        Logger.logger.warning(data)

    @staticmethod
    def error(data: str, hl = False):
        if Logger.logger is None:
            Logger.init()
            
        if hl:
            data = cf.format_bold(cf.format_red(data)) 
            
        Logger.logger.error(data)
    
    @staticmethod
    def init(lvl = logging.DEBUG, colored_console = True):
        """
        Setup logger for StringIO, console and file handler
        """
        Logger._logger_level = lvl
        
        if colored_console:
            print("colored_console used")
            Logger._formatter = cf.colored_formatter(Logger._format)
 
        if Logger.logger is not None:
            Logger.logger.warning("logger was setup already, deleting all previously existing handlers")
            for hdlr in Logger.logger.handlers[:]:  # remove all old handlers
                Logger.logger.removeHandler(hdlr)

        # Create the logger
        Logger.logger = logging.getLogger("botty")
        for hdlr in Logger.logger.handlers:
            Logger.logger.removeHandler(hdlr)
        Logger.logger.setLevel(Logger._logger_level)
        Logger.logger.propagate = False

        # Setup the StringIO handler
        Logger._log_contents = io.StringIO()
        Logger.string_handler = logging.StreamHandler(Logger._log_contents)
        Logger.string_handler.setLevel(Logger._logger_level)

        # Setup the console handler
        Logger.console_handler = logging.StreamHandler(sys.stdout)
        Logger.console_handler.setLevel(Logger._logger_level)

        # Setup the file handler
        Logger.file_handler = logging.FileHandler(Logger._current_log_file_path, 'a')
        Logger.file_handler.setLevel(Logger._logger_level)

        # Optionally add a formatter
        Logger.string_handler.setFormatter(Logger._formatter)
        Logger.console_handler.setFormatter(cf.colored_formatter(Logger._format))
        Logger.file_handler.setFormatter(Logger._formatter)

        # Add the handler to the logger
        Logger.logger.addHandler(Logger.string_handler)
        Logger.logger.addHandler(Logger.console_handler)
        Logger.logger.addHandler(Logger.file_handler)
        
        # redirect stderr & stdout to logger, e.g. print("...")
        # would have to implement all the std func such as write() flush() etc.
        # sys.stderr = Logger
        # sys.stdout = Logger

    @staticmethod
    def remove_file_logger(delete_current_log: bool = False):
        """
        Remove the file logger to not write output to a log file
        """
        Logger.logger.removeHandler(Logger.file_handler)
        if delete_current_log and os.path.exists(Logger._current_log_file_path):
            try:
                os.remove(Logger._current_log_file_path)
            except PermissionError:
                warnings.warn("Could not remove info.log, permission denied")
