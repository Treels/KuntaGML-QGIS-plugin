from PyQt5.QtCore import QSettings, QUrl
from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply
from qgis._core import Qgis, QgsBlockingNetworkRequest

from . import logger
from .constants import KuntaGMLNetworkException, ENCODING
from .utils import tr


def fetch(url: str) -> str:
    # http://osgeo-org.1560.x6.nabble.com/QGIS-Developer-Do-we-have-a-User-Agent-string-for-QGIS-td5360740.html
    user_agent = QSettings().value("/qgis/networkAndProxy/userAgent", "Mozilla/5.0")
    user_agent += " " if len(user_agent) else ""
    user_agent += f"QGIS/{Qgis.QGIS_VERSION_INT}"
    user_agent += " KuntaGMLLoader-plugin"
    logger.info(url)
    wfs_request = QNetworkRequest(QUrl(url))
    # https://www.riverbankcomputing.com/pipermail/pyqt/2016-May/037514.html
    wfs_request.setRawHeader(b"User-Agent", bytes(user_agent, "utf-8"))
    request_blocking = QgsBlockingNetworkRequest()
    _ = request_blocking.get(wfs_request)
    reply = request_blocking.reply()
    reply_error = reply.error()
    if reply_error != QNetworkReply.NoError:
        raise KuntaGMLNetworkException(tr('Request failed') + ':\n\n' + reply.errorString())

    return bytes(reply.content()).decode(ENCODING)
