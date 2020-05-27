import logging

from qgis.core import QgsMessageLog, Qgis

IDENTIFIER = "KuntaGMLLoader"

LOGGER = logging.getLogger('QGIS')




def info(msg: str, *args, **kwargs) -> None:
    print(msg)
    QgsMessageLog.logMessage(msg, IDENTIFIER, Qgis.Info)
    LOGGER.info(msg, args, kwargs)

def exception(msg: str, *args, **kwargs) -> None:
    print(msg, args, kwargs)
    QgsMessageLog.logMessage(msg, IDENTIFIER, Qgis.Warning)
    LOGGER.exception(str)

def debug(msg: str, *args, **kwargs) -> None:
    print(msg)
    LOGGER.debug(msg, *args, **kwargs)


def warning(msg:str, *args, **kwargs):
    print(msg, args, kwargs)
    LOGGER.warning(msg, args, kwargs)
