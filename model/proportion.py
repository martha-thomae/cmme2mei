from xml.etree.ElementTree import Element

class Proportion:
    """
    Represents a proportion with a numerator and denominator.
    """
    def __init__(self, num: int, den: int):
        self.num = num
        self.den = den

    @classmethod
    def parse(cls, element: Element) -> 'Proportion':
        # Implement the parsing logic for a proportion (numerator and denominator)
        num = int(element.find('{http://www.cmme.org}Num').text)
        den = int(element.find('{http://www.cmme.org}Den').text)
        return cls(num, den)

    def __eq__(self, other):
        if isinstance(other, Proportion):
            return self.num == other.num and self.den == other.den
        return False

    def __repr__(self):
        return f"Proportion(Num={self.num}, Den={self.den})"

