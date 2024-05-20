
import sys
sys.path.append('.')

import logging
import sys 

class InternalLogging():
    """ Internal logging class based on logging """
    
    LOG_FORMAT = '[%(levelname)s] - [%(asctime)s]: %(message)s'

    logging.basicConfig(
        level=logging.ERROR,
        format=LOG_FORMAT,
        stream=sys.stdout
    )
  
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def error(self, message):
        """ Error message """
        self.logger.error(message)
    