import logging

def textToLogLevel(verboseLevel):
    if verboseLevel == 'critical':
        return logging.CRITICAL
    elif verboseLevel == 'error':
        return logging.ERROR
    elif verboseLevel == 'warning':
        return logging.WARNING
    elif verboseLevel == 'info':
        return logging.INFO
    elif verboseLevel == 'debug':
        return logging.DEBUG
    else:
        return logging.NOTSET