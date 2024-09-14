from xml.etree.ElementTree import Element


class LineEndEvent:
    """
    Represents a line end event in musical notation, which may indicate the end of a page.
    """
    def __init__(self, page_end: bool):
        self.page_end = page_end

    @classmethod
    def parse(cls, element: Element) -> 'LineEndEvent':
        """
        Parses a LineEndEvent from an XML element.

        Args:
            element: The XML element containing LineEndEvent data.

        Returns:
            A LineEndEvent object.
        """
        # Check if PageEnd is present
        page_end = element.find('{http://www.cmme.org}PageEnd') is not None

        return cls(page_end)

    def __eq__(self, other):
        if isinstance(other, LineEndEvent):
            return self.page_end == other.page_end
        return False

    def __repr__(self):
        return f"LineEndEvent(PageEnd={self.page_end})"
