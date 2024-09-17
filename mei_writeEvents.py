
# ----------------------- #
# event-related functions #
# ----------------------- #


def makeNote():
	# create <note> from <Note>
	# then converPitch()
	# convertDuration()
	# convertModernTexttoLyrics()
	# if <Colored/> -> @colored="true"
	return None

def convertPitch():
	# <LetterName>D</LetterName> -> @pname
    # <OctaveNum>3</OctaveNum> -> @oct
	# octave count differs in cmme, octave starts at a
	# a(4) & b(4) are identical in cmme and mei
	# if range(c:g) => oct = oct + 1

	return None
	
def convertDuration():

	# <Type> value="Semifusa|Fusa|Semiminima|Minima|Semibrevis|Brevis|Longa|Maxima"	# <Type> to @dur de-capitalize first letter, like Maxima -> maxima
	# <Length> containing <Num>/<Den> use 1/1 for	minima
	# everything smaller than minima is always binary, e.g. 1/2 for semiminima
	# cmme stores relative durations always in every note/rest, one can figure out mensuration from that
	# -> Convert <Num> to @num && <Den> to @numbase
	return None 


def convertModernTexttoLyrics():
	# <ModernText><Syllable></ModernText> (child of <Note>) to <verse><syl></verse>
	# <WordEnd> to @wordpos="t" (cmme doesn't distinguish i & m)
    # !<WordEnd> -
	# 	@con="d"d"
    # remember if last <ModernText> had <Wordend>
	#		if lastText.wordend == True
	#			@wordpos="i"
    #       else
    #           @wordpos="m"
	return None