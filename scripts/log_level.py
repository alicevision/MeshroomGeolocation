import logging

def text_to_log_level(verbose_level):
    '''Convert text to log level'''
    if verbose_level == 'critical':
        return logging.CRITICAL
    if verbose_level == 'error':
        return logging.ERROR
    if verbose_level == 'warning':
        return logging.WARNING
    if verbose_level == 'info':
        return logging.INFO
    if verbose_level == 'debug':
        return logging.DEBUG
    
    return logging.NOTSET
