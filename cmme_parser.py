from cmme_model import SourceInfo, VariantVersion, GeneralData, Voice, VoiceData, MusicSection, Piece, Plainchant, \
    TextSection, MensuralMusic, EventList, BaseColoration, ColorationData, ColorAndFillData, SingleVoiceData, TacetData, \
    Event
import xml.etree.ElementTree as ET
from typing import List, Optional

from cmme_model_events import Pitch, MiscItemEvent, DotEvent, NoteEvent, MensurationEvent, OriginalTextEvent, ClefEvent, \
    ModernText, RestEvent, ProportionEvent, ColorChangeEvent, CustosEvent, LineEndEvent, ModernKeySignatureEvent, \
    MultiEvent, EventAttributes, Proportion


class PieceParser:
    # .................. GENERAL DATA ............................
    def parse_source_info(self, element) -> Optional[SourceInfo]:
        if element is None:
            return None
        name_el = element.find('{http://www.cmme.org}Name')
        id_el = element.find('{http://www.cmme.org}ID')
        name = name_el.text if name_el is not None else None
        id_ = int(id_el.text) if id_el is not None else None
        return SourceInfo(name, id_)

    def parse_variant_version(self, element) -> VariantVersion:
        id_el = element.find('{http://www.cmme.org}ID')
        id_ = id_el.text if id_el is not None else None

        source_el = element.find('{http://www.cmme.org}Source')
        source = self.parse_source_info(source_el) if source_el is not None else None

        description_el = element.find('{http://www.cmme.org}Description')
        description = description_el.text if description_el is not None else None

        missing_voices_el = element.find('{http://www.cmme.org}MissingVoices')
        missing_voices = []
        if missing_voices_el is not None:
            voice_num_els = missing_voices_el.findall('{http://www.cmme.org}VoiceNum')
            missing_voices = [voice_num_el.text for voice_num_el in voice_num_els if voice_num_el.text is not None]

        return VariantVersion(id_, source, description, missing_voices)

    def parse_color_and_fill_data(self, element) -> ColorAndFillData:
        if element is None:
            return ColorAndFillData()

        # Parse the Color element (optional)
        color_el = element.find('{http://www.cmme.org}Color')
        color = color_el.text if color_el is not None else None

        # Parse the Fill element (optional)
        fill_el = element.find('{http://www.cmme.org}Fill')
        fill = fill_el.text if fill_el is not None else None

        return ColorAndFillData(color, fill)

    def parse_base_coloration(self, element) -> Optional[BaseColoration]:
        if element is None:
            return None

        # Parse the primary color (required)
        primary_color_el = element.find('{http://www.cmme.org}PrimaryColor')
        primary_color_data = self.parse_color_and_fill_data(primary_color_el)

        # Parse the secondary color (optional)
        secondary_color_el = element.find('{http://www.cmme.org}SecondaryColor')
        secondary_color_data = self.parse_color_and_fill_data(secondary_color_el)

        # Create the ColorationData object
        coloration_data = ColorationData(primary_color_data, secondary_color_data)

        # Return the BaseColoration object
        return BaseColoration(coloration_data)

    def parse_general_data(self, element) -> GeneralData:
        if element is None:
            raise ValueError("GeneralData element is missing")

        incipit_el = element.find('{http://www.cmme.org}Incipit')
        incipit = incipit_el.text if incipit_el is not None else None

        title_el = element.find('{http://www.cmme.org}Title')
        title = title_el.text if title_el is not None else None

        section_el = element.find('{http://www.cmme.org}Section')
        section = section_el.text if section_el is not None else None

        composer_el = element.find('{http://www.cmme.org}Composer')
        composer = composer_el.text if composer_el is not None else None

        editor_el = element.find('{http://www.cmme.org}Editor')
        editor = editor_el.text if editor_el is not None else None

        publicNotes_el = element.find('{http://www.cmme.org}PublicNotes')
        publicNotes = publicNotes_el.text if publicNotes_el is not None else None

        notes_el = element.find('{http://www.cmme.org}Notes')
        notes = notes_el.text if notes_el is not None else None

        # Parse BaseColoration
        base_coloration_el = element.find('{http://www.cmme.org}BaseColoration')
        base_coloration = self.parse_base_coloration(base_coloration_el)

        # Handle 0..* (unbounded) cardinality for VariantVersion
        variant_versions = [self.parse_variant_version(var_ver_el) for var_ver_el in
                            element.findall('{http://www.cmme.org}VariantVersion')]

        return GeneralData(incipit, title, section, composer, editor, publicNotes, notes, variant_versions, base_coloration)

    # .................. VOICE DATA ............................
    def parse_single_voice_data(self, element) -> SingleVoiceData:
        name_el = element.find('{http://www.cmme.org}Name')
        name = name_el.text if name_el is not None else None

        editorial_el = element.find('{http://www.cmme.org}Editorial')
        editorial = editorial_el.text if editorial_el is not None else None

        # Only used in mensural music, not in plainchant. As it's optional, it can be added here
        canon_resolutio_el = element.find('{http://www.cmme.org}CanonResolutio')
        canon_resolutio = canon_resolutio_el.text if canon_resolutio_el is not None else None

        suggested_modern_clef_el = element.find('{http://www.cmme.org}SuggestedModernClef')
        suggested_modern_clef = suggested_modern_clef_el.text if suggested_modern_clef_el is not None else None

        return SingleVoiceData(name, editorial, canon_resolutio, suggested_modern_clef)

    def parse_voice_data(self, element) -> VoiceData:
        # Parse NumVoices (required)
        num_voices_el = element.find('{http://www.cmme.org}NumVoices')
        num_voices = int(num_voices_el.text) if num_voices_el is not None else 0

        # Parse the list of Voice elements
        voices = []
        voice_elements = element.findall('{http://www.cmme.org}Voice')
        for voice_el in voice_elements:
            single_voice_data = self.parse_single_voice_data(voice_el)
            voices.append(single_voice_data)

        return VoiceData(num_voices, voices)


    # .................. MUSIC SECTION ............................
    def parse_tacet_data(self, element) -> TacetData:
        # Parse the VoiceNum element (unsigned integer)
        voice_num_el = element.find('{http://www.cmme.org}VoiceNum')
        voice_num = int(voice_num_el.text) if voice_num_el is not None else None

        # Parse the TacetText element (string)
        tacet_text_el = element.find('{http://www.cmme.org}TacetText')
        tacet_text = tacet_text_el.text if tacet_text_el is not None else None

        # Return a TacetData object
        return TacetData(voice_num, tacet_text)

    """
        Used for plainchant and mensural notation
    """
    def parse_music_data(self, element):
        # Parse NumVoices (required)
        num_voices_el = element.find('{http://www.cmme.org}NumVoices')
        num_voices = int(num_voices_el.text) if num_voices_el is not None else 0

        # Parse BaseColoration (optional)
        base_coloration_el = element.find('{http://www.cmme.org}BaseColoration')
        base_coloration = self.parse_base_coloration(base_coloration_el) if base_coloration_el is not None else None

        # Parse TacetInstruction elements (optional, can occur multiple times)
        tacet_instructions = []
        tacet_instruction_els = element.findall('{http://www.cmme.org}TacetInstruction')
        for tacet_instruction_el in tacet_instruction_els:
            tacet_instructions.append(self.parse_tacet_data(tacet_instruction_el))

        # Parse Voice elements (must occur at least once)
        voices = [self.parse_voice(voice_el) for voice_el in element.findall('{http://www.cmme.org}Voice')]

        # Return all common data
        return num_voices, base_coloration, tacet_instructions, voices


    def parse_mensural_music(self, element) -> MensuralMusic:
        num_voices, base_coloration, tacet_instructions, voices = self.parse_music_data(element)
        return MensuralMusic(num_voices, base_coloration, tacet_instructions, voices)

    def parse_plainchant(self, element) -> Plainchant:
        num_voices, base_coloration, tacet_instructions, voices = self.parse_music_data(element)
        return Plainchant(num_voices, base_coloration, tacet_instructions, voices)

    def parse_text_section(self, element) -> TextSection:
        # Parse the Content element
        content_elements = element.findall('{http://www.cmme.org}Content')
        contents = [content_el.text for content_el in content_elements if content_el.text is not None]

        # Return the TextSection object with the parsed contents
        return TextSection(contents)

    def parse_music_section(self, element) -> MusicSection:
        # Try to find the MensuralMusic element
        mensural_music_el = element.find('{http://www.cmme.org}MensuralMusic')
        if mensural_music_el is not None:
            content = self.parse_mensural_music(mensural_music_el)
            return MusicSection(content)

        # Try to find the Plainchant element
        plainchant_el = element.find('{http://www.cmme.org}Plainchant')
        if plainchant_el is not None:
            content = self.parse_plainchant(plainchant_el)
            return MusicSection(content)

        # Try to find the Text element
        text_el = element.find('{http://www.cmme.org}Text')
        if text_el is not None:
            content = self.parse_text_section(text_el)
            return MusicSection(content)

        # If no known content type is found, raise an error
        raise ValueError("Unsupported section type in MusicSection")




    # .................. PIECE ............................
    def parse_piece(self, xml_string: str) -> Piece:
        root = ET.fromstring(xml_string)

        cmme_version = root.attrib.get('CMMEversion')

        # Parse GeneralData (required)
        general_data_el = root.find('{http://www.cmme.org}GeneralData')
        general_data = self.parse_general_data(general_data_el)

        # Parse VoiceData (required)
        voice_data_el = root.find('{http://www.cmme.org}VoiceData')
        voice_data = self.parse_voice_data(voice_data_el)

        # Parse MusicSection (1..unbounded)
        music_sections = [self.parse_music_section(ms_el) for ms_el in
                          root.findall('{http://www.cmme.org}MusicSection')]

        return Piece(cmme_version, general_data, voice_data, music_sections)


    def parse_event_list(self, element) -> EventList:
        events = []

        # Parse all standard events and other structures in EventListData
        for event_el in element:
            if event_el.tag.endswith('VariantReadings'):
                variant_reading = self.parse_variant_readings(event_el)
                events.append(variant_reading)
            elif event_el.tag.endswith('EditorialData'):
                editorial_data = self.parse_editorial_data(event_el)
                events.append(editorial_data)
            else:
                # For standard events handled by SingleOrMultiEventData
                event = self.parse_single_or_multi_event_data(event_el)
                events.append(event)

        return EventList(events)

    def parse_variant_readings(self, element):
        readings = []
        for reading_el in element.findall('{http://www.cmme.org}Reading'):
            variant_version_ids = [vv_el.text for vv_el in reading_el.findall('{http://www.cmme.org}VariantVersionID')]
            preferred_reading = reading_el.find('{http://www.cmme.org}PreferredReading')
            error = reading_el.find('{http://www.cmme.org}Error')
            lacuna = reading_el.find('{http://www.cmme.org}Lacuna')

            # If there's a Music element, it might have SingleOrMultiEventData inside
            music_el = reading_el.find('{http://www.cmme.org}Music')
            music_events = []
            if music_el is not None:
                music_events = [self.parse_single_or_multi_event_data(me_el) for me_el in music_el.findall('{http://www.cmme.org}Event')]

            readings.append({
                'variant_version_ids': variant_version_ids,
                'preferred_reading': preferred_reading.text if preferred_reading is not None else None,
                'error': error.text if error is not None else None,
                'lacuna': lacuna is not None,
                'music_events': music_events
            })

        return {'type': 'VariantReadings', 'readings': readings}

    def parse_editorial_data(self, element):
        new_reading = element.find('{http://www.cmme.org}NewReading')
        original_reading = element.find('{http://www.cmme.org}OriginalReading')

        new_events = []
        if new_reading is not None:
            new_events = [self.parse_single_or_multi_event_data(ne_el) for ne_el in new_reading.findall('{http://www.cmme.org}Event')]

        original_events = []
        if original_reading is not None:
            lacuna_el = original_reading.find('{http://www.cmme.org}Lacuna')
            error_el = original_reading.find('{http://www.cmme.org}Error')
            if lacuna_el is not None:
                original_events.append({'type': 'Lacuna'})
            if error_el is not None:
                error_events = [self.parse_single_or_multi_event_data(ee_el) for ee_el in error_el.findall('{http://www.cmme.org}Event')]
                original_events.append({'type': 'Error', 'events': error_events})

        return {'type': 'EditorialData', 'new_reading': new_events, 'original_reading': original_events}


    def parse_voice(self, element) -> Voice:
        # Parse the VoiceNum (required)
        voice_num_el = element.find('{http://www.cmme.org}VoiceNum')
        voice_num = int(voice_num_el.text) if voice_num_el is not None else None

        # Parse MissingVersionID (optional, can occur multiple times)
        missing_version_ids = [mv_el.text for mv_el in element.findall('{http://www.cmme.org}MissingVersionID')]

        # Parse EventList (required)
        event_list_el = element.find('{http://www.cmme.org}EventList')
        event_list = self.parse_event_list(event_list_el) if event_list_el is not None else None

        return Voice(voice_num, missing_version_ids, event_list)

    def parse_single_event(self, event_el):
        # Check the tag name and call the appropriate parsing method
        if event_el.tag.endswith('MultiEvent'):
            return self.parse_multi_event(event_el)
        elif event_el.tag.endswith('Clef'):
            return self.parse_clef(event_el)
        elif event_el.tag.endswith('Mensuration'):
            return self.parse_mensuration(event_el)
        elif event_el.tag.endswith('Rest'):
            return self.parse_rest(event_el)
        elif event_el.tag.endswith('Note'):
            return self.parse_note(event_el)
        elif event_el.tag.endswith('Dot'):
            return self.parse_dot(event_el)
        elif event_el.tag.endswith('OriginalText'):
            return self.parse_original_text(event_el)
        elif event_el.tag.endswith('Proportion'):
            return self.parse_proportion(event_el)
        elif event_el.tag.endswith('ColorChange'):
            return self.parse_color_change(event_el)
        elif event_el.tag.endswith('Custos'):
            return self.parse_custos(event_el)
        elif event_el.tag.endswith('LineEnd'):
            return self.parse_line_end(event_el)
        elif event_el.tag.endswith('MiscItem'):
            return self.parse_misc_item(event_el)
        elif event_el.tag.endswith('ModernKeySignature'):
            return self.parse_modern_key_signature(event_el)
        else:
            return None


    def parse_multi_event(self, element) -> MultiEvent:
        multi_events = []

        # Iterate over each child element inside MultiEvent and use helper method
        for sub_event_el in element:
            event = self.parse_single_event(sub_event_el)
            if event is not None:
                multi_events.append(event)

        return MultiEvent(multi_events)

    def parse_event_list(self, element) -> EventList:
        events = []

        # Iterate over child elements in EventList and use helper method
        for event_el in element:
            event = self.parse_single_event(event_el)
            if event is not None:
                events.append(event)

        return EventList(events)

    def parse_event_attributes(self, element) -> EventAttributes:
        """
        Parse the EventAttributes group, which includes optional elements:
        Colored, Ambiguous, Editorial, Error, and EditorialCommentary.
        """
        # Parse Colored (True if present)
        colored = element.find('{http://www.cmme.org}Colored') is not None

        # Parse Ambiguous (True if present)
        ambiguous = element.find('{http://www.cmme.org}Ambiguous') is not None

        # Parse Editorial (True if present)
        editorial = element.find('{http://www.cmme.org}Editorial') is not None

        # Parse Error (True if present)
        error = element.find('{http://www.cmme.org}Error') is not None

        # Parse EditorialCommentary (if present)
        editorial_commentary_element = element.find('{http://www.cmme.org}EditorialCommentary')
        editorial_commentary = editorial_commentary_element.text if editorial_commentary_element is not None else None

        # Create and return EventAttributes object
        return EventAttributes(colored, ambiguous, editorial, error, editorial_commentary)




    def parse_clef(self, element) -> ClefEvent:
        # Parse Appearance
        appearance = element.find('{http://www.cmme.org}Appearance').text if element.find('{http://www.cmme.org}Appearance') is not None else None

        # Parse StaffLoc as an integer
        staff_loc = int(element.find('{http://www.cmme.org}StaffLoc').text) if element.find('{http://www.cmme.org}StaffLoc') is not None else None

        # Parse Pitch (which uses the Locus group)
        pitch_element = element.find('{http://www.cmme.org}Pitch')
        if pitch_element is not None:
            letter_name = pitch_element.find('{http://www.cmme.org}LetterName').text if pitch_element.find('{http://www.cmme.org}LetterName') is not None else None
            octave_num = int(pitch_element.find('{http://www.cmme.org}OctaveNum').text) if pitch_element.find('{http://www.cmme.org}OctaveNum') is not None else None
            pitch = Pitch(letter_name, octave_num)
        else:
            pitch = None

        # Parse Signature (optional)
        signature = element.find('{http://www.cmme.org}Signature') is not None

        # Parse EventAttributes (referenced group)
        event_attributes = self.parse_event_attributes(element)

        return ClefEvent(appearance, staff_loc, pitch, event_attributes, signature)


    def parse_modern_text(self, element) -> ModernText:
        if element is None:
            return None

        syllables = []
        has_word_end = False

        # Parse Syllable elements
        for syllable_el in element.findall('{http://www.cmme.org}Syllable'):
            syllables.append(syllable_el.text)

        # Check if WordEnd is present
        word_end_el = element.find('{http://www.cmme.org}WordEnd')
        if word_end_el is not None:
            has_word_end = True

        return ModernText(syllables, has_word_end)


    def parse_original_text(self, element):
        phrase = element.find('{http://www.cmme.org}Phrase').text if element.find('{http://www.cmme.org}Phrase') is not None else None
        return OriginalTextEvent(phrase)

    def parse_mensuration(self, element) -> MensurationEvent:
        main_symbol = None
        orientation = None
        strokes = None
        dot = False
        number = None

        # Handle Sign element
        sign_el = element.find('{http://www.cmme.org}Sign')
        if sign_el is not None:
            main_symbol_el = sign_el.find('{http://www.cmme.org}MainSymbol')
            main_symbol = main_symbol_el.text if main_symbol_el is not None else None

            orientation_el = sign_el.find('{http://www.cmme.org}Orientation')
            orientation = orientation_el.text if orientation_el is not None else None

            strokes_el = sign_el.find('{http://www.cmme.org}Strokes')
            strokes = int(strokes_el.text) if strokes_el is not None else None

            dot = sign_el.find('{http://www.cmme.org}Dot') is not None

        # Handle Number element (Proportion group)
        number_el = element.find('{http://www.cmme.org}Number')
        if number_el is not None:
            number = self.parse_proportion(number_el)

        # Parse optional StaffLoc
        staff_loc_el = element.find('{http://www.cmme.org}StaffLoc')
        staff_loc = int(staff_loc_el.text) if staff_loc_el is not None else None

        # Parse MensInfo (if present)
        mens_info = {}
        mens_info_el = element.find('{http://www.cmme.org}MensInfo')
        if mens_info_el is not None:
            mens_info['prolatio'] = mens_info_el.find('{http://www.cmme.org}Prolatio').text if mens_info_el.find('{http://www.cmme.org}Prolatio') is not None else None
            mens_info['tempus'] = mens_info_el.find('{http://www.cmme.org}Tempus').text if mens_info_el.find('{http://www.cmme.org}Tempus') is not None else None
            mens_info['modus_minor'] = mens_info_el.find('{http://www.cmme.org}ModusMinor').text if mens_info_el.find('{http://www.cmme.org}ModusMinor') is not None else None
            mens_info['modus_maior'] = mens_info_el.find('{http://www.cmme.org}ModusMaior').text if mens_info_el.find('{http://www.cmme.org}ModusMaior') is not None else None

            tempo_change_el = mens_info_el.find('{http://www.cmme.org}TempoChange')
            if tempo_change_el is not None:
                mens_info['tempo_change'] = self.parse_proportion(tempo_change_el)

        # Parse NoScoreEffect (True if present)
        no_score_effect = element.find('{http://www.cmme.org}NoScoreEffect') is not None

        # Parse EventAttributes
        event_attributes = self.parse_event_attributes(element)

        # Return the parsed MensurationEvent object
        return MensurationEvent(main_symbol, orientation, strokes, dot, number, staff_loc, mens_info, no_score_effect, event_attributes)

    def parse_note(self, element):
        note_type = element.find('{http://www.cmme.org}Type').text if element.find('{http://www.cmme.org}Type') is not None else None
        letter_name = element.find('{http://www.cmme.org}LetterName').text if element.find('{http://www.cmme.org}LetterName') is not None else None
        octave_num = int(element.find('{http://www.cmme.org}OctaveNum').text) if element.find('{http://www.cmme.org}OctaveNum') is not None else None
        lig = element.find('{http://www.cmme.org}Lig').text if element.find('{http://www.cmme.org}Lig') is not None else None
        stem_dir = element.find('{http://www.cmme.org}Stem/Dir').text if element.find('{http://www.cmme.org}Stem/Dir') is not None else None
        modern_text = self.parse_modern_text(element.find('{http://www.cmme.org}ModernText'))

        return NoteEvent(note_type, letter_name, octave_num, lig, stem_dir, modern_text)

    def parse_dot(self, element):
        pitch = self.parse_pitch(element.find('{http://www.cmme.org}Pitch'))
        return DotEvent(pitch)

    def parse_misc_item(self, element):
        barline_el = element.find('{http://www.cmme.org}Barline')
        if barline_el is not None:
            num_lines = barline_el.find('{http://www.cmme.org}NumLines').text if barline_el.find('{http://www.cmme.org}NumLines') is not None else None
            return MiscItemEvent(num_lines)
        return None

    def parse_pitch(self, element):
        if element is None:
            return None
        letter_name = element.find('{http://www.cmme.org}LetterName').text if element.find('{http://www.cmme.org}LetterName') is not None else None
        octave_num = int(element.find('{http://www.cmme.org}OctaveNum').text) if element.find('{http://www.cmme.org}OctaveNum') is not None else None
        return Pitch(letter_name, octave_num)


    def parse_rest(self, element):
        rest_type = element.find('{http://www.cmme.org}Type').text if element.find('{http://www.cmme.org}Type') is not None else None
        length_num = element.find('{http://www.cmme.org}Length/Num').text if element.find('{http://www.cmme.org}Length/Num') is not None else None
        length_den = element.find('{http://www.cmme.org}Length/Den').text if element.find('{http://www.cmme.org}Length/Den') is not None else None
        bottom_staff_line = element.find('{http://www.cmme.org}BottomStaffLine').text if element.find('{http://www.cmme.org}BottomStaffLine') is not None else None
        num_spaces = element.find('{http://www.cmme.org}NumSpaces').text if element.find('{http://www.cmme.org}NumSpaces') is not None else None

        return RestEvent(rest_type, length_num, length_den, bottom_staff_line, num_spaces)

    def parse_proportion(self, element) -> ProportionEvent:
        num_el = element.find('{http://www.cmme.org}Num')
        den_el = element.find('{http://www.cmme.org}Den')

        num = int(num_el.text) if num_el is not None else 1  # Default to 1 if missing
        den = int(den_el.text) if den_el is not None else 1  # Default to 1 if missing

        proportion = Proportion(num, den)
        return ProportionEvent(proportion)

    def parse_color_change(self, element):
        primary_color = element.find('{http://www.cmme.org}PrimaryColor').text if element.find('{http://www.cmme.org}PrimaryColor') is not None else None
        secondary_color = element.find('{http://www.cmme.org}SecondaryColor').text if element.find('{http://www.cmme.org}SecondaryColor') is not None else None

        return ColorChangeEvent(primary_color, secondary_color)

    def parse_custos(self, element):
        letter_name = element.find('{http://www.cmme.org}LetterName').text if element.find('{http://www.cmme.org}LetterName') is not None else None
        octave_num = element.find('{http://www.cmme.org}OctaveNum').text if element.find('{http://www.cmme.org}OctaveNum') is not None else None

        return CustosEvent(letter_name, octave_num)

    def parse_line_end(self, element):
        page_end = element.find('{http://www.cmme.org}PageEnd') is not None

        return LineEndEvent(page_end)

    def parse_modern_key_signature(self, element):
        accidental = element.find('{http://www.cmme.org}Accidental').text if element.find('{http://www.cmme.org}Accidental') is not None else None
        pitch_class = element.find('{http://www.cmme.org}PitchClass').text if element.find('{http://www.cmme.org}PitchClass') is not None else None

        return ModernKeySignatureEvent(accidental, pitch_class)
