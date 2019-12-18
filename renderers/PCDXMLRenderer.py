"""
Provides XML rendering support for ProCentric.
"""
from __future__ import unicode_literals
from django.conf import settings
from django.utils import six
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six import StringIO
from django.utils.encoding import force_text
from rest_framework.renderers import BaseRenderer
from datetime import datetime
from datetime import timezone
import pytz
import xmlschema


class PCDXML(BaseRenderer):
    """
    Renderer which serializes to XML.
    """
    last_update = str(datetime.now(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%dT%H:%M:%S%z'))
    last_update = last_update[:22] + ':' + last_update[22:]
    media_type = 'application/xml'
    format = 'xml'
    charset = 'UTF-8'
    item_tag_name = 'item'
    root_tag_name = 'PMSData lastUpdate="' + last_update + '"'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        xml.startElement(self.root_tag_name, {})

        self._to_xml(xml, data)

        xml.endElement(self.root_tag_name.split(' ', 1)[0])
        xml.endDocument()
        print(stream.getvalue())

        xsd = xmlschema.XMLSchema('procentric_connect/bin/pms-data-schema.xsd')
        xsd.validate(stream.getvalue())

        return stream.getvalue()

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):

            for item in data:
                # Check for Messages
                print(item)
                if 'messageTitle' in item:
                    xml.startElement('message', {})
                    self._to_xml(xml, item)
                    xml.endElement('message')
                else:
                    xml.startElement(self.item_tag_name, {})
                    self._to_xml(xml, item)
                    xml.endElement(self.item_tag_name.split(' ', 1)[0])

        elif isinstance(data, dict):
            for key, value in six.iteritems(data):
                xml.startElement(key.split('temp', 1)[0], {})
                self._to_xml(xml, value)
                xml.endElement(key.split(' ', 1)[0])

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(force_text(data))
