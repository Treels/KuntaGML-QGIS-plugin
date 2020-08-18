#  Gispo Ltd., hereby disclaims all copyright interest in the program KuntaGML-QGIS-plugin
#  Copyright (C) 2020 Gispo Ltd (https://www.gispo.fi/).
#
#
#  This file is part of KuntaGML-QGIS-plugin.
#
#  KuntaGML-QGIS-plugin is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  KuntaGML-QGIS-plugin is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with KuntaGML-QGIS-plugin.  If not, see <https://www.gnu.org/licenses/>.

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
