import xml.etree.ElementTree as ET
from cmme2mei import import_score

# Get the CMME tree
cmmetree = import_score("Anonymous-CibavitEos-BrusBRIV922.cmme.xml")

# Get the MEI tree (with the right name space)
meitree = ET.parse("./MEI-mensural-skeleton.mei")
ET.register_namespace("", "http://www.music-encoding.org/ns/mei")
ns = {"":"http://www.music-encoding.org/ns/mei"}

# Start modifying the MEI tree with the information from CMME

# Element: title
title = meitree.findall('//title', ns)[0]
title.text = cmmetree.general_data.title

# Element: staffDef
staffgrp = meitree.findall('//staffGrp', ns)[0]
section1 = cmmetree.music_sections[1]

for i in range(section1.content.num_voices):
	staffdef = ET.SubElement(staffgrp, 'staffDef')
	staffdef.set('lines', '5')
	staffdef.set('n', str(i+1))
	# # Clef
	# clef
	# staffdef.set('clef.line', '')
	# staffdef.set('clef.shape', '')
	# # Mensuration


# Write output MEI file
meitree.write('output11.xml','utf-8', xml_declaration=True)
