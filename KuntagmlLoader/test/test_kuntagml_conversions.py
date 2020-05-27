import logging
import unittest

from qgis.core import QgsProject

from .utilities import get_qgis_app
from ..core.kuntagml2layers import KuntaGML2Layers

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()
QGIS_INSTANCE = QgsProject.instance()

LOGGER = logging.getLogger('QGIS')


class KuntaGMLConversionTest(unittest.TestCase):
    """Test KuntaGML to Geopackage script """

    def setUp(self) -> None:
        """Runs before every test. """
        IFACE.newProject()

    def tearDown(self) -> None:
        super().tearDown()

    def test_turku_opaskartta(self):
        url = "https://opaskartta.turku.fi/TeklaOGCWeb/WFS.ashx"

        converter = KuntaGML2Layers(url, '2.1.6', '2.1.1', '1.1.0')
        converter.populate_features()
        self.assertEqual(83, len(converter.feature_types))
        layers = converter.convert_feature_types(['akaava:Kaava'])
        self.assertEqual(len(layers['akaava:Kaava']), 5)

    def test_riihimaki_opaskartta(self):
        url = "https://kartta.riihimaki.fi/teklaogcweb/WFS.ashx?request=GetCapabilities"

        converter = KuntaGML2Layers(url, '2.1.6', '2.1.1', '1.1.0')
        converter.populate_features()
        print(converter.feature_types)
        self.assertEqual(72, len(converter.feature_types))
        layers = converter.convert_feature_types(['kanta:Kevyenliikenteenvayla'])
        self.assertEqual(len(layers['kanta:Kevyenliikenteenvayla']), 3)

    @unittest.skip("Host requires authentication")
    def test_lahti_opaskartta(self):
        url = "https://kartta.lahti.fi/TeklaOGCWeb/WFS.ashx"

        converter = KuntaGML2Layers(url, '2.1.6', '2.1.1', '1.1.0')
        converter.populate_features()
        self.assertEqual(97, len(converter.feature_types))
        converter.convert_feature_types(['kanta:Kevyenliikenteenvayla'])

    @unittest.skip("Host requires authentication")
    def test_jkyla_opaskartta(self):
        url = "https://kartta.jkl.fi/TeklaOgcWeb/WFS.ashx?request=GetCapabilities"

        converter = KuntaGML2Layers(url, '2.1.6', '2.1.1', '1.1.0')
        converter.populate_features()
        self.assertEqual(88, len(converter.feature_types))
        print(converter.feature_types)
        converter.convert_feature_types(['kanta:Kevyenliikenteenvayla'])
