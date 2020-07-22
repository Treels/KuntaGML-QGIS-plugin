from enum import Enum

from ..qgis_plugin_tools.tools.resources import resources_path


class ServiceProvider(Enum):
    """Service provider of the schema """
    kuntatietopalvelu = 'http://www.kuntatietopalvelu.fi'
    paikkatietopalvelu = 'http://www.paikkatietopalvelu.fi'


ENCODING = "utf-8"
WFS_NAMESPACE = 'http://www.opengis.net/wfs'

INITIAL_SCHEMAS = {
    'gml/kantakartta': 'http://www.paikkatietopalvelu.fi/gml/kantakartta http://s3.eu-central-1.amazonaws.com/gispogdalkuntagml/kantakartta_2.1.1.xsd',
    'gml/osoitteet': 'http://www.paikkatietopalvelu.fi/gml/osoitteet http://s3.eu-central-1.amazonaws.com/gispogdalkuntagml/osoitteet_2.1.1.xsd',
    'gml/asemakaava': 'http://www.paikkatietopalvelu.fi/gml/asemakaava http://s3.eu-central-1.amazonaws.com/gispogdalkuntagml/asemakaava_2.1.1.xsd',
    'gml/rakennusvalvonta': 'http://www.paikkatietopalvelu.fi/gml/rakennusvalvonta http://s3.eu-central-1.amazonaws.com/gispogdalkuntagml/rakennusvalvonta_2.2.0.xsd'
}

DATA_DIR = resources_path('data')
