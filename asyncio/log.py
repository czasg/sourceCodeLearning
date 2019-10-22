"""Logging configuration."""

import logging

# Name the logger after the package.
logger = logging.getLogger(__package__)

if __name__ == '__main__':
    logger.error(__package__)
