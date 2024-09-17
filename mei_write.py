import xml.etree.ElementTree as ET
from cmme2mei import import_score
ET.register_namespace("", "http://www.music-encoding.org/ns/mei")
ns = {"":"http://www.music-encoding.org/ns/mei"}
currentScore = False

# ------------------------------ #
# MEI document-related functions #
# ------------------------------ #
def createMEIDoc():
	# Get the MEI tree (with the right name space)
	meitree = ET.parse("./MEI-mensural-skeleton.mei")
	return meitree

def writeMEI(meitree, filename):
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
	return str(int(cmmeStaffLoc) - 1)

def getVoiceNumber():

# ------------------ #
# STAFFDEF FUNCTIONS
# ------------------ #

# clef-related functions #
# ---------------------- #
def isClef(cmmeClef):
	return (type(cmmeClef).__name__ == "ClefEvent" 
		and cmmeClef.appearance in ["C", "F", "G", "Gamma", "Frnd", "MODERNC", "MODERNF","MODERNC", "MODERNC"])

def convertClef(cmmeClef):
	meiClef = ET.Element('clef',ns)
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
def makeStaffDefs(cmme_section, staffgrp):
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
			staffdef.append(sig)

# ----------------------------------- #
# mdiv- and section-related functions #
# ----------------------------------- #
def makeSectionElement(cmme_musicsection):
	


def makeMdivElement(cmme_musicsection):
	# mdiv -> score -> scoreDef -> staffGrp
	mdiv = ET.Element('mdiv',ns)
	score = ET.SubElement(mdiv, 'score')
	currentScore = score
	scoredef = ET.SubElement(score, 'scoreDef')
	staffgrp = ET.SubElement(scoredef, 'staffGrp')
	makeStaffDefs(cmme_musicsection, staffgrp)
	# mdiv -> score -> section
	score.append(makeSectionElement(cmme_musicsection))
	return mdiv


def makeSections(meitree, cmmetree):
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


def makeStaffs():
	# makes a <staff> element within <section> for each <Voice> descendant in <MusicSection>


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

# ----------------------- #
# event-related functions #
# ----------------------- #


def makeNote():
	# create <note> from <Note>
	# <T
pe> value="Semifusa|Fusa|Semiminima|Minima|Semibrevis|Brevis|Longa|Maxima"
	# <Length> containing <Num>/<Den>

def convertPitch():
	# <LetterName>D</LetterName> -> @pname
    # <OctaveNum>3</OctaveNum> -> @oct
	# octave count differs in cmme, octave starts at a
	# a(4) & b(4) are identical in cmme and mei
	# if range(c:g) => oct = oct + 1

def convertDuration():
	# <Type> to @dur de-capitalize first letter, like Maxima -> maxima
	# <Length> containing <Num>/<Den> use 1/1 for	minima
	# everything smaller than minima is always binary, e.g. 1/2 for semiminima
	# cmme stores relative durations always in every note/rest, one can figure out mensuration from that
	# 


# Get the CMME tree
cmmetree = import_score("Anonymous-CibavitEos-BrusBRIV922.cmme.xml")
meitree = createMEIDoc()
#### some code
writeMEI(meitree, "output.mei")
