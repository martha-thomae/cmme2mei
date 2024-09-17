import xml.etree.ElementTree as ET
from cmme2mei import import_score
ET.register_namespace("", "http://www.music-encoding.org/ns/mei")
ns = {"":"http://www.music-encoding.org/ns/mei"}
currentScore = False
clefShapes = ["C", "F", "G", "Gamma", "Frnd", "MODERNC", "MODERNF","MODERNC", "MODERNC"]

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
def convertStaffLoc(cmmeStaffLoc):
	return str((int(cmmeStaffLoc) + 1) / 2)

def getVoiceNumber():
	return False

# ------------------ #
# STAFFDEF FUNCTIONS
# ------------------ #

# clef-related functions (MEI) #
# ---------------------------- #
def isClef(event):
	return (type(event).__name__ == "ClefEvent" 
		and event.appearance in clefShapes)

def convertClef(cmmeClef):
	meiClef = ET.Element('clef')
	meiClef.set('shape', cmmeClef.appearance)
	meiClef.set('line', convertStaffLoc(cmmeClef.staff_loc))
	return meiClef

def makeClefElement(staffDef, cmme_section, n):
	# makes <clef> or <keySig> from <Clef>
	# CMME uses <Clef> for clefs and signatures (having <Signature> as child)
	# Clef <Appearance>: C, G, Gamma, Frnd... maybe MODERNG|MODERNG8|MODERNF|MODERNC
	# Signature <Appearance>: Bmol, BmolDouble, Bqua, Diesis
	# What about Fis and Fsqr???
	# Clef
	voice_n = cmme_section.content.voices[n]
	# ASSUMPTION:
	# First element on the list of events of the voice # n
	# "will always be a clef"
	# or a variantlist with a set of clefs
	# if first element is a clef or variant list with a clef:
	cmmeClef = voice_n.event_list.events[0]
	if isClef(cmmeClef):
		return convertClef(cmmeClef)
	else:
		print("First element isn't a clef. We should probably do something")
	# else warn, but make staffdef without clef?


# clef-related functions (cmme) #
# ----------------------------- #
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
	# Search for the first clef in a CMME object given voice number
	for section in cmmetree.music_sections:
		for voice in section.content.voices:
			if voice.voice_num == voiceNum:
				return findClefInVoice(voice)

# key signature-related functions #
# ------------------------------- #
def makeSignatureElement(staffDef, cmme_section, n):
	# If there is signature at the beginning of this voice in the section, add it here
	return False

def convertSignatureOrAccidental(cmme_clef):
	return False

# mensuration-related functions #
# ----------------------------- #
def makeMensElement(staffDef, cmme_section, n):
	# If there is mensuration at the beginning of this voice in the section, add it here
	# Use MakeMensuration() for the conversion
	return False

# make staffDef functions #
# ----------------------- #
""" def makeStaffDefs(cmme_section, staffgrp):
	for i in range(cmme_section.content.num_voices):
		staffdef = ET.SubElement(staffgrp, 'staffDef')
		staffdef.set('lines', '5')
		# Should we use actual staff numbers rather than i?
		clef = makeClefElement(staffdef, cmme_section, i)
		if clef:
			staffdef.append(clef)
		mens = makeMensElement(staffdef, cmme_section, i)
		if mens:
			staffdef.append(mens)
		sig = makeSignatureElement(staffdef, cmme_section, i)
		if sig:
			staffdef.append(sig) """

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
		cmmeclef = findClefForVoiceNum(cmmetree, i)
		if cmmeclef:
			staffdef.append(convertClef(cmmeclef))
		## Do all this again for mens and sig

# ----------------------------------- #
# mdiv- and section-related functions #
# ----------------------------------- #
def makeSectionElement(cmme_musicsection):
	# Make MEI section for this section
	# If the section is 'plainchant', we need
	#  some invisible staves for tacet voices
	#  and probably a @type attribute. We
	#  do not use @notationtype, because in CMME
	#  this is still mensural notation - it's 
	#  just chant. 
	section = ET.Element('section',ns)
	if cmme_musicsection.content.section_type == "Plainchant":
		section.set("type", "Plainchant")
	return section
	


def makeMdivElement(cmme_musicsection, cmmetree):
	# mdiv -> score -> scoreDef -> staffGrp
	mdiv = ET.Element('mdiv')
	score = ET.SubElement(mdiv, 'score')
	currentScore = score
	scoredef = ET.SubElement(score, 'scoreDef')
	staffgrp = ET.SubElement(scoredef, 'staffGrp')
	makeGlobalStaffDef(cmmetree, staffgrp)
	# mdiv -> score -> section
	score.append(makeSectionElement(cmme_musicsection))
	return mdiv

def makeSections(meitree, cmmetree):
	# Since: a) we know the max number of voices b) we can have non-shown staves 
	# for inactive voices in a section c) the plainchant in CMME is really 
	# mensural transcription of chant, we don't need multiple MDivs
	meibody = meitree.find('.//body',ns)
	for cmme_musicsection in cmmetree.music_sections:
		if currentScore:
			currentScore.append(makeSectionElement(cmme_musicsection))
		else:
			# This should only happen for the first section
			meibody.append(makeMdivElement(cmme_musicsection, cmmetree))

""" def makeSections(meitree, cmmetree):
	# creates sections or mDivs from <MusicSection>
	# <section> if voice numbers stay identical, <mDiv> if voice number changes
	# children of <MusicSection> are either <Plainchant> or <MensuralMusic>
	# change @notationtype accordingly
	# Useful code: section.content.num_voices and section.content.section_tyoe
	# MusicSection --> Child: Plainchant | MensuralMusic --> child NumVoices
	prevSectionType, prevNumvoices = False
	meibody = meitree.find('.//body',ns)
	for cmme_musicsection in cmmetree.music_sections:
		sectiontype = cmme_musicsection.content.section_type
		numvoices = cmme_musicsection.content.num_voices
		if(not prevSectionType or sectiontype!= prevSectionType
			or not prevNumvoices or numvoices!=prevNumvoices):
			# Either this is the first section (so we need an mdiv) or there's a change of notation or voice count
			meibody.append(makeMdivElement(cmme_musicsection))
		else:
			#make new section
			if currentScore:
				currentScore.append(makeSectionElement(cmme_musicsection))
			else:
				# error
				print("Missing score element")
 """

def makeStaffs():
	# makes a <staff> element within <section> for each <Voice> descendant in <MusicSection>
	return False

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

# ----------------------- #
# event-related functions #
# ----------------------- #


def makeNote():
	# create <note> from <Note>
	# then converPitch()
	# convertDuration()
	# convertModernTexttoLyrics()
	return False

def convertPitch():
	# <LetterName>D</LetterName> -> @pname
    # <OctaveNum>3</OctaveNum> -> @oct
	# octave count differs in cmme, octave starts at a
	# a(4) & b(4) are identical in cmme and mei
	# if range(c:g) => oct = oct + 1

		return False
	
def convertDuration():

	# <Type> value="Semifusa|Fusa|Semiminima|Minima|Semibrevis|Brevis|Longa|Maxima"	# <Type> to @dur de-capitalize first letter, like Maxima -> maxima
	# <Length> containing <Num>/<Den> use 1/1 for	minima
	# everything smaller than minima is always binary, e.g. 1/2 for semiminima
	# cmme stores relative durations always in ever
	return False









# Get the CMME tree
cmmetree = import_score("Anonymous-CibavitEos-BrusBRIV922.cmme.xml")
meitree = createMEIDoc()
#### some code
addMetadata(meitree, cmmetree)
makeSections(meitree, cmmetree)
writeMEIDoc(meitree, "output.mei")
