__version__ = '0.6.0'

import logging
import multiprocessing

# Only warn in the main process, not again in every multiprocessing worker
if multiprocessing.parent_process() is None:
    logger = logging.getLogger(__name__)
    logger.warning(
        'Default WIMP parameters are changed in accordance with '
        'https://arxiv.org/abs/2105.00599 (github.com/JelleAalbers/wimprates/pull/14)')

from .utils import *
from .halo import *
from .elastic_nr import *
from .bremsstrahlung import *
from .migdal import *
from .electron import *
from .summary import *
from .data.migdal.Cox.cox_wrapper import *
