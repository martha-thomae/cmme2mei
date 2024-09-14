from .events import Event
from .clef import ClefEvent
from .custos import CustosEvent
from .dot import DotEvent
from .key_signature import ModernKeySignatureEvent
from .line_end import LineEndEvent
from .mensuration import MensurationEvent
from .misc_item import MiscItemEvent
from .multievent import MultiEvent
from .note import NoteEvent
from .original_text import OriginalTextEvent
from .proportion_event import ProportionEvent
from .rest import RestEvent

class EventFactory:
    '''
    This class is responsible for creating events. It uses reflection. Note that for working, all event classes must be imported above
    '''
    @classmethod
    def create(cls, event_el):
        """
        Dynamically constructs the class name from the XML tag and calls its parse method.
        For each event type (e.g. 'Clef'), there is an associated class (e.g. Clef)

        Args:
            event_el: The XML element representing the event.

        Returns:
            An Event object if a corresponding class with a parse method is found, otherwise None.
        """
        # Extract the tag name and construct the class name dynamically
        tag_suffix = event_el.tag.split('}')[-1]  # Get the suffix part of the tag (after the namespace)
        class_name = f'{tag_suffix}Event'  # Dynamically construct the class name, e.g., 'ClefEvent'
        if class_name == 'MultiEventEvent':
            class_name = 'MultiEvent'

        # Attempt to find the class in the current global scope
        event_class = globals().get(class_name)

        if event_class is None:
            # Raise exception if the class is not found
            raise EventClassNotFoundException(class_name)

            # Check if the class has the 'parse' method
        parse_method = getattr(event_class, 'parse', None)
        if parse_method is None:
            # Raise exception if the 'parse' method is not found
            raise ParseMethodNotFoundException(class_name)

        # Call the parse method and return the result
        return parse_method(event_el)

class EventClassNotFoundException(Exception):
    """Exception raised when the event class is not found."""
    def __init__(self, class_name):
        super().__init__(f"Event class '{class_name}' not found.")


class ParseMethodNotFoundException(Exception):
    """Exception raised when the parse method is not found in the event class."""
    def __init__(self, class_name):
        super().__init__(f"Parse method not found in the event class '{class_name}'.")

