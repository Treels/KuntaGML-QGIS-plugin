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

import logging
import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

from osgeo import gdal
from qgis.core import QgsVectorLayer, QgsSettings

from .exceptions import KuntaGMLInvalidContentException
from .utils.sql_utils import get_non_empty_tables
from ..definitions.constants import (ServiceProvider, WFS_NAMESPACE, INITIAL_SCHEMAS, DATA_DIR)
from ..qgis_plugin_tools.tools.i18n import tr
from ..qgis_plugin_tools.tools.network import fetch
from ..qgis_plugin_tools.tools.resources import plugin_name

LOGGER = logging.getLogger(plugin_name())


class LoadFromSettings:
    def __init__(self, by_substring: str = 'qgis/connections-wfs/', suffix: str = '/url') -> None:
        """Load settings by parsing QgsSettings keys

        :param by_substring: settings substring, defaults to 'qgis/connections-wfs/'
        :type by_substring: str, optional
        :param suffix: settings suffix to search for, defaults to '/url'
        :type suffix: str, optional
        """
        self.wfs_urls = {}
        self.authcfg_id = ''
        self.load_saved_urls(by_substring, suffix)

    def load_saved_urls(self, by_substring: str, suffix: str):
        settings = QgsSettings().allKeys()
        for setting in settings:
            if setting.find(by_substring) != -1 and setting.find(suffix) != -1:
                cleaned_name = setting.strip(by_substring).strip(suffix)
                self.wfs_urls[cleaned_name] = QgsSettings().value(setting)

    def load_authcfg_id(self, cleaned_name: str, suffix: str = '/authcfg'):
        self.authcfg_id = ''
        settings = QgsSettings().allKeys()
        for setting in settings:
            if setting.find(cleaned_name) != -1 and setting.find(suffix) != -1:
                self.authcfg_id = QgsSettings().value(setting)
        if self.authcfg_id:
            LOGGER.info("authcfg id found for selected item")
        else:
            LOGGER.info("no autcfg id found for selected item")


class KuntaGML2Layers:

    def __init__(self, url: str, version_common: str, version_gml: str, version_wfs: str, srs=3067, authcfg_id: str = ''):
        """

        :param url: getCapabilities url
        :param version_common:
        :param version_gml:
        :param version_wfs:
        :param srs:
        :param authcfg_id:
        """
        self.url = url.split("?")[0]
        self.version_common = version_common
        self.version_gml = version_gml
        self.version_wfs = version_wfs
        self.srs = srs
        self.authcfg_id = authcfg_id
        self.feature_types = []

    @property
    def domain(self):
        uri = urlparse(self.url)
        return uri.netloc.replace(".", "-")

    @property
    def data_dir(self):
        return os.path.join(DATA_DIR, self.domain)

    def populate_features(self) -> None:
        """
        Populate feature types based on capabilities document
        """
        content = fetch(f'{self.url}?request=GetCapabilities&service=WFS&version={self.version_wfs}')
        d = ET.ElementTree(ET.fromstring(content))
        r = d.getroot()
        feature_types = r.findall('{%s}FeatureTypeList' % WFS_NAMESPACE)[0].findall(
            '{%s}FeatureType' % WFS_NAMESPACE)
        self.feature_types = [f_type.find('{%s}Name' % WFS_NAMESPACE).text for f_type in feature_types]

    def convert_feature_types(self, feature_types: [str], max_features=100) -> {str: [QgsVectorLayer]}:
        """

        :param feature_types:
        :param max_features:
        :return:
        """

        types = set(self.feature_types).intersection(set(feature_types))
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        layers = {}
        for f_type in types:
            layers[f_type] = self.convert_feature_type(f_type, max_features)

        return layers

    def convert_feature_type(self, feature_type: str, max_features: int):
        layers = []

        try:
            max_fs = f'maxFeatures={max_features}' if int(self.version_wfs[0]) < 2 else f'count={max_features}'
            url = f'{self.url}?request=GetFeature&service=WFS&srsName={self.srs}&typeName={feature_type}&version={self.version_wfs}&{max_fs}'
            content = fetch(url, authcfg_id=self.authcfg_id)
            content = self._fix_schemalocations(content)
            gml = os.path.join(self.data_dir, f'{feature_type.replace(":", "_")}.gml')
            with open(gml, "w") as f:
                f.write(content)
            db_name = os.path.join(self.data_dir, f'{feature_type.replace(":", "_")}.sqlite')
            succeeded = self._convert_to_spatialite(gml, db_name)
            if succeeded:
                tables = get_non_empty_tables(db_name)
                for table in tables:
                    layer = QgsVectorLayer(table.uri, table.name, 'spatialite')
                    if layer.isValid():
                        layers.append(layer)
        except Exception as error:
            LOGGER.exception(tr("Uncaught error occurred"), error)
        finally:
            return layers

    def _convert_to_spatialite(self, gml_file: str, spatialite_file: str) -> bool:
        ogr2ogr_convert_params = [
            "-dim", "XY",
            "-a_srs", f"EPSG:{self.srs}",
            "-nlt", "convert_to_linear",
            "-oo", "REMOVE_UNUSED_LAYERS=YES",
            "-oo", "REMOVE_UNUSED_FIELDS=YES",
            "-oo", "EXPOSE_METADATA_LAYERS=YES",
            "-forceNullable"
        ]

        try:
            gdal.VectorTranslate(
                spatialite_file, f'gmlas:{gml_file}',
                options='-f SQLite -dsco SPATIALITE=YES ' + ' '.join(ogr2ogr_convert_params)
            )
        except Exception as error:
            LOGGER.warning(tr("Could not create spatialite database"), error)
            return False

        return True

    @staticmethod
    def _fix_schemalocations(content: str) -> str:
        schemalocations = re.findall('xsi:schemaLocation="([^"]*)"', content)
        if len(schemalocations) != 1:
            raise KuntaGMLInvalidContentException(
                tr("Could not parse gml content: invalid occurences of schemalocations:"),
                len(schemalocations))
        original_locations = KuntaGML2Layers._filter_schemalocations(schemalocations)

        new_locations = original_locations + " " + "\n".join(
            [location for key, location in INITIAL_SCHEMAS.items() if key in content])
        LOGGER.info(new_locations)
        print(ServiceProvider.paikkatietopalvelu.value)
        content = (content
                   .replace(schemalocations[0], new_locations)
                   .replace(ServiceProvider.kuntatietopalvelu.value, ServiceProvider.paikkatietopalvelu.value)
                   )

        return content

    @staticmethod
    def _filter_schemalocations(schemalocations: [str]) -> [str]:
        original_locations = schemalocations[0]
        parts = original_locations.split()
        filtered_locations = []
        i = 0
        while i < len(parts):
            s_location = parts[i].strip()
            if "tekla" in s_location:
                i += 1
            else:
                filtered_locations.append(s_location)
            i += 1
        original_locations = "\n".join(filtered_locations)
        return original_locations
