import sys
import traceback
from typing import Any, Optional, Union

class CustomException(Exception):
    """Base custom exception for the Loan Prediction pipeline."""
    def __init__(self, error_message: Union[Exception, str], error_detail: Optional[Any] = sys) -> None:
        super().__init__(str(error_message))
        self.original_error = error_message
        self.file_name = "unknown"
        self.line_number = 0
        
        # Automatically extract file name and line number if an exception is active
        _, _, exc_tb = error_detail.exc_info() if hasattr(error_detail, "exc_info") else (None, None, sys.exc_info()[2])
        if exc_tb:
            # Extract the actual failure line from the end of the traceback
            summary = traceback.extract_tb(exc_tb)[-1]
            self.file_name, self.line_number = summary.filename, summary.lineno

        self.error_message = f"Error in [{self.file_name}] line [{self.line_number}]: {error_message}"

    def log(self, logger: Optional[Any] = None) -> "CustomException":
        """Logs the exception and returns self for chaining."""
        if logger is None:
            try:
                from src.logger import get_logger
            except ModuleNotFoundError:
                from logger import get_logger
            logger = get_logger(self.__class__.__name__)
        logger.error(self.error_message)
        return self

    def __str__(self) -> str: return self.error_message
    def __repr__(self) -> str: return f"{self.__class__.__name__}(file={self.file_name!r}, line={self.line_number})"

# Backward compatibility alias
CustomExceptions = CustomException

# Pipeline-specific exceptions
class DataIngestionException(CustomException): pass
class DataValidationException(CustomException): pass
class DataTransformationException(CustomException): pass
class ModelTrainerException(CustomException): pass
class ModelEvaluationException(CustomException): pass
class PredictionException(CustomException): pass
class ConfigurationException(CustomException): pass
