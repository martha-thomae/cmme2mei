import xml.etree.ElementTree as ET
from cmme2mei import import_score

# Get the CMME tree
cmmetree = import_score("Anonymous-CibavitEos-BrusBRIV922.cmme.xml")

# Get the MEI tree (with the right name space)
meitree = ET.parse("./MEI-mensural-skeleton.mei")
ET.register_namespace("", "http://www.music-encoding.org/ns/mei")
ns = {"":"http://www.music-encoding.org/ns/mei"}

# Start modifying the MEI tree with the information from CMME
title = meitree.findall('//title', ns)[0]
title.text = cmmetree.general_data.title

# Write output MEI file
meitree.write('output7.xml','utf-8', xml_declaration=True)
