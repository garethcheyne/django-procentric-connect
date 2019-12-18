import xmlschema

xsd = xmlschema.XMLSchema('../bin/pms-data-schema.xsd')

xsd.validate('../bin/sample-pms-xml.xml')