import logging
import sys
import json
from datetime import datetime
from logging.handlers import SocketHandler
import os


class LogstashFormatter(logging.Formatter):
    """Custom formatter to output logs in JSON format for Logstash"""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": os.getenv("SERVICE_NAME", "unknown-service"),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "endpoint"):
            log_data["endpoint"] = record.endpoint
        if hasattr(record, "method"):
            log_data["method"] = record.method
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        
        return json.dumps(log_data)


def setup_logging(service_name: str | None = None):
    """
    Configure logging to send logs to both console and Logstash
    
    Args:
        service_name: Name of the microservice (e.g., 'auth-service')
    """
    if service_name:
        os.environ["SERVICE_NAME"] = service_name
    
    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler (for local development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Logstash handler (for production)
    try:
        logstash_host = os.getenv("LOGSTASH_HOST", "logstash")
        logstash_port = int(os.getenv("LOGSTASH_PORT", "5000"))
        
        logstash_handler = SocketHandler(logstash_host, logstash_port)
        logstash_handler.setFormatter(LogstashFormatter())
        logger.addHandler(logstash_handler)
        
        logger.info(f"Logstash handler configured: {logstash_host}:{logstash_port}")
    except Exception as e:
        logger.warning(f"Failed to configure Logstash handler: {e}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


# Custom log adapter for adding context
class ContextLogger(logging.LoggerAdapter):
    """Logger adapter that adds context to log messages"""
    
    def process(self, msg, kwargs):
        # Add context from extra dict
        if self.extra:
            for key, value in self.extra.items():
                if key not in kwargs.get('extra', {}):
                    kwargs.setdefault('extra', {})[key] = value
        return msg, kwargs