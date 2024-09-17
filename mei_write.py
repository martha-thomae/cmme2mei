import xml.etree.ElementTree as ET
from cmme2mei import import_score


ET.register_namespace("", "http://www.music-encoding.org/ns/mei")
ns = {"":"http://www.music-encoding.org/ns/mei"}
currentScore = False
clefShapes = ["C", "F", "G", "Gamma", "Frnd", "MODERNC", "MODERNF","MODERNC", "MODERNC"]
signatureShapes = ["Bmol", "BmolDouble", "Bqua", "Diesis"]

# ------------------------------ #
# MEI document-related functions #
# ------------------------------ #
def createMEIDoc():
	# Get the MEI tree (with the right name space)
	meitree = ET.parse("./MEI-mensural-skeleton.mei")
	return meitree

def writeMEIDoc(meitree, filename):
	# Write output MEI file
	# FIXME: no schema attributes
	meitree.write(filename,'utf-8', xml_declaration=True)


# -------------------------- #
# metadata-related functions #
# -------------------------- #
def addMetadata(meitree, cmmeObject):
	# Element: title
	# Get title from CMME metadata and add to mei skeleton
	# FIXME: crude and incomplete
	title = meitree.findall('//title', ns)[0]
	title.text = cmmeObject.general_data.title


# ------------------- #
# auxiliary functions #
# ------------------- #
def convertStaffLocToLine(cmmeStaffLoc):
	return str(int((int(cmmeStaffLoc) + 1) / 2))

def convertStaffLocToLoc(cmmeStaffLoc):
	return str(int(cmmeStaffLoc) - 1)

def getVoiceNumber():
	return False

# ------------------ #
# STAFFDEF FUNCTIONS
# ------------------ #

# clef-related functions (MEI) #
# ---------------------------- #

def convertClef(cmmeClef):
	meiClef = ET.Element('clef')
	meiClef.set('shape', cmmeClef.appearance)
	meiClef.set('line', convertStaffLocToLine(cmmeClef.staff_loc))
	return meiClef

# clef-related functions (cmme) #
# ----------------------------- #
def isClef(event):
	return (type(event).__name__ == "ClefEvent" 
		and event.appearance in clefShapes)

def findClefInVoice(cmmeVoice):
	# If this voice part begins with a clef, return it
	for event in cmmeVoice.event_list.events:
		if isClef(event):
			return event
		elif type(event).__name__ == "VariantReadings":
			# If we have a default/preferred variant, check it for a clef
			defaultReading = getDefaultReading(event)
			if defaultReading:
				for readingEvent in defaultReading.music_events:
					# Is the first event a clef?
					if isClef(readingEvent):
						return readingEvent
					elif type(event).__name__ in ['NoteEvent', 'RestEvent']:
						return False
				return False
			return False
		elif type(event).__name__ in ['NoteEvent', 'RestEvent']:
			return False
	return False

def getDefaultReading(variantReadings):
	for reading in variantReadings:
		if reading.preferred_reading or "DEFAULT" in reading.variant_version_ids:
			return reading
	# If we reach here, there is no default. Should we just the return one, or just return false?
	return False


def findClefForVoiceNum(cmmetree, voiceNum):
	# Search for the first CMME voice matching voice num (across sections) and then look to
	# see if there's a clef before any musical content (i.e. notes and rests). This
	# is so it can be included in staffDef
	for section in cmmetree.music_sections:
		for voice in section.content.voices:
			if voice.voice_num == voiceNum:
				return findClefInVoice(voice)

# key signature-related functions #
# ------------------------------- #
def convertSignatureOrAccidental(cmmeSignature):
	# cmme Signature is now a sequence of Clef Elements
	meiSig = ET.Element('keySig')
	for element in cmmeSignature:
		sign = ET.SubElement(meiSig, 'keyAccid')
		sign.set('loc', convertStaffLocToLoc(element.staff_loc))
		sign.set('accid', convertAppearanceToAccid(element.appearance))
	return meiSig


def isSignature(event):
	labelledAsSignature = (type(event).__name__ == "ClefEvent" 
		and event.signature)
	if labelledAsSignature:
		if event.appearance in signatureShapes:
			return True
		else:
			print("Warning: Ignoring signature label on a:", event.appearance)
			return False
	else:
		return False

def isSignatureLike(event):
	return (type(event).__name__ == "ClefEvent" 
		and event.appearance in signatureShapes)

def convertAppearanceToAccid(appearance):
	if appearance == 'Bmol':
		return 'f'
	elif appearance == 'Bqua':
		return 'n'
	elif appearance == 'Diesis':
		return 's'
	elif appearance == 'BmolDouble':
		print('WARNING: BmolDouble has been treated as Bmol')
		return 'f'
	else:
		print("WARNING: Encountered unrecognised signature:". appearance)
		return ''

def findSigInEventList(events):
	# If this voice part begins with a signature, return it
	sig = False
	for event in events:
		if isSignature(event):
			# We track sig because it's possible to have a sequence of sig elements
			if sig:
				sig.append(event)
			else:
				sig = [event]
		elif sig:
			# If we've had a signature element, assume that if we get a non-sig, that's it
			return sig
		elif isSignatureLike(event):
			print("WARNING: Voice begins with a clef that looks like a signature")
			print("WARNING: This will be treated as an `accidental', but you might wish to check")
			return False
		elif type(event).__name__ == "VariantReadings":
			# If we have a default/preferred variant, check it for a clef
			defaultReading = getDefaultReading(event)
			if defaultReading:
				readingSig = False
				return findSigInEventList(defaultReading.music_events)
			return False
		elif type(event).__name__  == "MultiEvent":
			# Multiple signature elements may be grouped as a MultiEvent
			if(isSignature(event.events[0])):
				return event.events
		elif type(event).__name__ in ['NoteEvent', 'RestEvent']:
			return False
	return False

def findSignatureInVoice(cmmeVoice):
	# If this voice part begins with a signature, return it
	return findSigInEventList(cmmeVoice.event_list.events)

def findSigForVoiceNum(cmmetree, voiceNum):
	# Search for the first CMME voice matching voice num (across sections) and then look to
	# see if there's a signature-like object before any musical content (i.e. notes and rests). This
	# is so it can be included in staffDef
	for section in cmmetree.music_sections:
		for voice in section.content.voices:
			if voice.voice_num == voiceNum:
				return findSignatureInVoice(voice)

def makeSignatureElement(staffDef, cmme_section, n):
	# If there is signature at the beginning of this voice in the section, add it here
	return False

# mensuration-related functions #
# ----------------------------- #
def makeMensElement(staffDef, cmme_section, n):
	# If there is mensuration at the beginning of this voice in the section, add it here
	# Use MakeMensuration() for the conversion
	return False

# make staffDef functions #
# ----------------------- #
def makeGlobalStaffDef(cmmetree, staffgrp):
	# A global list of voices (rather than one per section)
	for i in range(cmmetree.voice_data.num_voices):
		staffdef = ET.SubElement(staffgrp, 'staffDef')
		# CMME can't represent other numbers of stafflines
		staffdef.set('lines', '5')
		voice = cmmetree.voice_data.voices[i]
		if voice.name:
			label = ET.SubElement(staffdef, 'label')
			label.text = voice.name
		# Clef
		cmmeclef = findClefForVoiceNum(cmmetree, i + 1)
		if cmmeclef:
			staffdef.append(convertClef(cmmeclef))
		## Do all this again for mens and sig
		# sig
		cmmeSig = findSigForVoiceNum(cmmetree, i + 1)
		if cmmeSig:
			staffdef.append(convertSignatureOrAccidental(cmmeSig))

# ----------------------------------- #
# mdiv- and section-related functions #
# ----------------------------------- #
def addStaffElements(cmme_musicsection, mei_section_element, maxvoices):
	# Find the numbers of the voices present in this MusicSection
	# makes a <staff> element within <section> for each <Voice> descendant in <MusicSection>
	cmme_voice_numbers_array = []
	for cmmevoice in cmme_musicsection.content.voices:
		cmme_voice_numbers_array.append(cmmevoice.voice_num)

	# Add a <staff> and its @n to the <section> for each <staffDef> element 
	# (so for the total number of voices in the piece)
	for n in range(1, maxvoices + 1):
		staff = ET.Element('staff')
		mei_section_element.append(staff)
		staff.set('n', str(n))
		# Use @visible = false for the <staff> elements that are actually not present in the MusicSection
		if n not in cmme_voice_numbers_array:
			staff.set('visible', 'false')
		# Add a <layer> to each <staff>
		ET.SubElement(staff, 'layer')


def makeSectionElement(cmme_musicsection, cmmetree):
	# Make MEI section for this section
	# If the section is 'plainchant', we need
	#  some invisible staves for tacet voices
	#  and probably a @type attribute. We
	#  do not use @notationtype, because in CMME
	#  this is still mensural notation - it's 
	#  just chant. 
	mei_section_element = ET.Element('section')
	if cmme_musicsection.content.section_type == "Plainchant":
		mei_section_element.set("type", "Plainchant")
	
	maxvoices = cmmetree.voice_data.num_voices
	addStaffElements(cmme_musicsection, mei_section_element, maxvoices)
	return mei_section_element
	


def makeMdivElement(cmme_musicsection, cmmetree):
	global currentScore
	# mdiv -> score -> scoreDef -> staffGrp
	mdiv = ET.Element('mdiv')
	score = ET.SubElement(mdiv, 'score')
	currentScore = score
	scoredef = ET.SubElement(score, 'scoreDef')
	staffgrp = ET.SubElement(scoredef, 'staffGrp')
	makeGlobalStaffDef(cmmetree, staffgrp)
	# mdiv -> score -> section
	score.append(makeSectionElement(cmme_musicsection, cmmetree))
	return mdiv

def makeSections(meitree, cmmetree):
	# Since: a) we know the max number of voices b) we can have non-shown staves 
	# for inactive voices in a section c) the plainchant in CMME is really 
	# mensural transcription of chant, we don't need multiple MDivs
	global currentScore
	meibody = meitree.find('.//body',ns)
	for cmme_musicsection in cmmetree.music_sections:
		if currentScore:
			currentScore.append(makeSectionElement(cmme_musicsection, cmmetree))
		else:
			# This should only happen for the first section
			meibody.append(makeMdivElement(cmme_musicsection, cmmetree))

def makeMensuration():
	# creates a <mensur> element from <Mensuration>
	# <Mensuration> contains a <Sign>, <Number> and <MensInfo>
	# Sign can contain <MainSymbol> "O|C", 
	# 	<Orientation> "Reversed|90CW|90CCW": mei @orient = "reversed|90CW|90CCW" (90CW and 90CCW seem to not be available in the cmme editor)
	# 	<Strokes> contains unsignedInt, and <Dot> (no content)
	# <Number> contains <Num> and <Den> with integers
	# <MensInfo> contains <Prolatio>, <Tempus>, <ModusMinor>, <ModusMaior> always 2 or 3
	#	and <TempoChange> containing <Num> & <Den>
	# <Mensuration> contains <MensInfo> only if you add it explicitly in the editor
	# 	CMME assumes a binary default: add @tempus/@prolatio/@modusminor/@modusminor="2" if there is nothing else
	# 	Infer from <Sign> O|C -> @tempus 3/2 && <Dot/>|!<Dot/> -> 3/2
	# 	Read then from <MensInfo> 
	return False


# Get the CMME tree
cmmetree = import_score("Anonymous-CibavitEos-BrusBRIV922.cmme.xml")
meitree = createMEIDoc()
#### some code
addMetadata(meitree, cmmetree)
makeSections(meitree, cmmetree)
writeMEIDoc(meitree, "outputLastChanges22.mei")
