from typing import Optional, List


class Pitch:
    """
    Represents a musical pitch with a letter name and octave number.
    """

    def __init__(self, letter_name: Optional[str], octave_num: Optional[int]):
        self.letter_name = letter_name
        self.octave_num = octave_num

    def __repr__(self):
        return f"Pitch(LetterName={self.letter_name}, OctaveNum={self.octave_num})"

class ModernText:
    """
    Represents modern text elements like syllables for a note, with optional word endings.
    """
    def __init__(self, syllables: Optional[List[str]] = None, has_word_end: bool = False):
        self.syllables = syllables if syllables is not None else []
        self.has_word_end = has_word_end

    def __repr__(self):
        return f"ModernText(Syllables={self.syllables}, HasWordEnd={self.has_word_end})"


class Event:
    """
    Base class for all events.
    Each event has a type (e.g., 'Clef', 'Note', 'Dot', etc.).
    """
    def __init__(self, event_type: str):
        self.event_type = event_type

    def __repr__(self):
        return f"{self.__class__.__name__}(Type={self.event_type})"

class ClefEvent(Event):
    def __init__(self, appearance: Optional[str], staff_loc: Optional[int], pitch: Optional['Pitch'], colored: bool):
        super().__init__('Clef')
        self.appearance = appearance
        self.staff_loc = staff_loc
        self.pitch = pitch
        self.colored = colored

    def __repr__(self):
        return (f"ClefEvent(Appearance={self.appearance}, StaffLoc={self.staff_loc}, "
                f"Pitch={self.pitch}, Colored={self.colored})")

class NoteEvent(Event):
    def __init__(self, note_type: Optional[str], letter_name: Optional[str], octave_num: Optional[int],
                 lig: Optional[str], stem_dir: Optional[str], modern_text: Optional['ModernText']):
        super().__init__('Note')
        self.note_type = note_type
        self.letter_name = letter_name
        self.octave_num = octave_num
        self.lig = lig
        self.stem_dir = stem_dir
        self.modern_text = modern_text

    def __repr__(self):
        return (f"NoteEvent(Type={self.note_type}, LetterName={self.letter_name}, OctaveNum={self.octave_num}, "
                f"Lig={self.lig}, StemDir={self.stem_dir}, ModernText={self.modern_text})")

class DotEvent(Event):
    def __init__(self, pitch: Optional['Pitch']):
        super().__init__('Dot')
        self.pitch = pitch

    def __repr__(self):
        return f"DotEvent(Pitch={self.pitch})"

class MensurationEvent(Event):
    def __init__(self, main_symbol: Optional[str], strokes: Optional[int]):
        super().__init__('Mensuration')
        self.main_symbol = main_symbol
        self.strokes = strokes

    def __repr__(self):
        return f"MensurationEvent(MainSymbol={self.main_symbol}, Strokes={self.strokes})"

class OriginalTextEvent(Event):
    def __init__(self, phrase: Optional[str]):
        super().__init__('OriginalText')
        self.phrase = phrase

    def __repr__(self):
        return f"OriginalTextEvent(Phrase={self.phrase})"

class MiscItemEvent(Event):
    def __init__(self, num_lines: Optional[int]):
        super().__init__('MiscItem')
        self.num_lines = num_lines

    def __repr__(self):
        return f"MiscItemEvent(NumLines={self.num_lines})"

class RestEvent(Event):
    def __init__(self, rest_type, length_num, length_den, bottom_staff_line, num_spaces):
        super().__init__('Rest')
        self.rest_type = rest_type
        self.length_num = length_num
        self.length_den = length_den
        self.bottom_staff_line = bottom_staff_line
        self.num_spaces = num_spaces

    def __repr__(self):
        return f"RestEvent(Type={self.rest_type}, Length={self.length_num}/{self.length_den}, BottomStaffLine={self.bottom_staff_line}, NumSpaces={self.num_spaces})"

class ProportionEvent(Event):
    def __init__(self, proportion_num: Optional[int], proportion_den: Optional[int]):
        super().__init__('Proportion')
        self.proportion_num = proportion_num
        self.proportion_den = proportion_den

    def __repr__(self):
        return f"ProportionEvent(Proportion={self.proportion_num}/{self.proportion_den})"

class ColorChangeEvent(Event):
    def __init__(self, primary_color: Optional[str], secondary_color: Optional[str]):
        super().__init__('ColorChange')
        self.primary_color = primary_color
        self.secondary_color = secondary_color

    def __repr__(self):
        return f"ColorChangeEvent(PrimaryColor={self.primary_color}, SecondaryColor={self.secondary_color})"

class CustosEvent(Event):
    def __init__(self, letter_name: Optional[str], octave_num: Optional[int]):
        super().__init__('Custos')
        self.letter_name = letter_name
        self.octave_num = octave_num

    def __repr__(self):
        return f"CustosEvent(LetterName={self.letter_name}, OctaveNum={self.octave_num})"

class LineEndEvent(Event):
    def __init__(self, page_end: bool):
        super().__init__('LineEnd')
        self.page_end = page_end

    def __repr__(self):
        return f"LineEndEvent(PageEnd={self.page_end})"

class ModernKeySignatureEvent(Event):
    def __init__(self, accidental: Optional[str], pitch_class: Optional[str]):
        super().__init__('ModernKeySignature')
        self.accidental = accidental
        self.pitch_class = pitch_class

    def __repr__(self):
        return f"ModernKeySignatureEvent(Accidental={self.accidental}, PitchClass={self.pitch_class})"

class MultiEvent(Event):
    '''
        Composite pattern
    '''
    def __init__(self, events: List[Event]):
        super().__init__('MultiEvent')
        self.events = events

    def __repr__(self):
        return f"MultiEvent(Events={self.events})"
