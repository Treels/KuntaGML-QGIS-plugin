import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

from osgeo import gdal
from qgis.core import QgsVectorLayer

from .utils import logger
from .utils.constants import (ServiceProvider, KuntaGMLInvalidContentException,
                              WFS_NAMESPACE, INITIAL_SCHEMAS, DATA_DIR)
from .utils.network import fetch
from .utils.sql_utils import get_non_empty_tables
from .utils.utils import tr


class KuntaGML2Layers:

    def __init__(self, url: str, version_common: str, version_gml: str, version_wfs: str, srs=3067):
        """

        :param url: getCapabilities url
        :param version_common:
        :param version_gml:
        :param version_wfs:
        """
        self.url = url.split("?")[0]
        self.version_common = version_common
        self.version_gml = version_gml
        self.version_wfs = version_wfs
        self.srs = srs
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

    def convert_feature_types(self, feature_types: [str]) -> {str: [QgsVectorLayer]}:
        """

        :param feature_types:
        :return:
        """

        types = set(self.feature_types).intersection(set(feature_types))
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        layers = {}
        for f_type in types:
            layers[f_type] = self.convert_feature_type(f_type)

        return layers

    def convert_feature_type(self, feature_type: str):
        layers = []

        try:
            url = f'{self.url}?request=GetFeature&service=WFS&srsName={self.srs}&typeName={feature_type}&version={self.version_wfs}'
            content = fetch(url)
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
            logger.exception(tr("Uncaught error occurred"), error)
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
            logger.warning(tr("Could not create spatialite database"), error)
            return False

        return True

    @staticmethod
    def _fix_schemalocations(content: str) -> str:
        schemalocations = re.findall('xsi:schemaLocation="([^"]*)"', content)
        if len(schemalocations) != 1:
            raise KuntaGMLInvalidContentException(
                tr("Could not parse gml content: invalid occurences of schemalocations:"),
                len(schemalocations))
        original_locations = KuntaGML2Layers.filter_schemalocations(schemalocations)

        new_locations = original_locations + " " + "\n".join(
            [location for key, location in INITIAL_SCHEMAS.items() if key in content])
        logger.info(new_locations)
        print(ServiceProvider.paikkatietopalvelu.value)
        content = (content
                   .replace(schemalocations[0], new_locations)
                   .replace(ServiceProvider.kuntatietopalvelu.value, ServiceProvider.paikkatietopalvelu.value)
                   )

        return content

    @staticmethod
    def filter_schemalocations(schemalocations):
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
