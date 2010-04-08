#! /usr/bin/env python
"""
fetchBuilds.py is used to get the primary nightly builds from ftp.mozilla.org, record
the build information and provide that information through the Crash Reporter website.

This script is expected to be run once per day.
"""

import logging
import logging.handlers

try:
  import config.buildsconfig as config
except ImportError:
  import buildsconfig as config

import socorro.cron.builds as builds
import socorro.lib.ConfigurationManager as configurationManager

config = configurationManager.newConfiguration(configurationModule = config, applicationName='startBuilds.py')
assert "databaseHost" in config, "databaseHost is missing from the configuration"
assert "databaseName" in config, "databaseName is missing from the configuration"
assert "databaseUserName" in config, "databaseUserName is missing from the configuration"
assert "databasePassword" in config, "databasePassword is missing from the configuration"
assert "base_url" in config, "base_url is missing from the configuration"
assert "platforms" in config, "platforms is missing from the configuration"
assert "versions" in config, "versions is missing from the configuration"

logger = logging.getLogger("builds")
logger.setLevel(logging.DEBUG)

stderrLog = logging.StreamHandler()
stderrLog.setLevel(config.stderrErrorLoggingLevel)
stderrLogFormatter = logging.Formatter(config.stderrLineFormatString)
stderrLog.setFormatter(stderrLogFormatter)
logger.addHandler(stderrLog)

rotatingFileLog = logging.handlers.RotatingFileHandler(config.logFilePathname, "a", config.logFileMaximumSize, config.logFileMaximumBackupHistory)
rotatingFileLog.setLevel(config.logFileErrorLoggingLevel)
rotatingFileLogFormatter = logging.Formatter(config.logFileLineFormatString)
rotatingFileLog.setFormatter(rotatingFileLogFormatter)
logger.addHandler(rotatingFileLog)

config.logger = logger 
logger.info("current configuration\n%s", str(config))

try:
  builds.recordNightlyBuilds(config)
finally:
  logger.info("Done.")
  rotatingFileLog.flush()
  rotatingFileLog.close()