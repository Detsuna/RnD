import math


class ExponentNotation() :
    Scientific = 1
    Engineering = 3

    def __init__(self, value, decimalPlaces=3, notation=Engineering, spacing=False, plusForPositive=False) : 
        self.value = value
        if decimalPlaces<0 : raise ValueError("not possible to have decimal places below 0 ")
        else : self.decimalPlaces = decimalPlaces
        self.notation = notation
        self.spacing = spacing
        self.plusForPositive = plusForPositive
    def __str__(self) : 
        exponent = pow(10, self.notation)
        mag = int(math.log(abs(self.value)) // math.log(exponent))
        return "".join([
            "-" if self.value<0 else "",
            f"{abs(self.value)/pow(exponent, mag):.{self.decimalPlaces}f}".rstrip("0").rstrip("."),
            f"""{" " if self.spacing else ""}{"E" if mag!=0 else ""}{"+" if mag>0 and self.plusForPositive else ""}{mag*self.notation if mag!=0 else ""}"""
        ])

class ReadableSize() : 
    SI = pow(10, 3)
    IEC = pow(2, 10)
    Symbols = {
        -8: " y",
        -7: " z",
        -6: " a",
        -5: " f",
        -4: " p",
        -3: " n",
        -2: " μ",
        -1: " m",
        0: " ",
        1: " K",
        2: " M",
        3: " G",
        4: " T",
        5: " P",
        6: " E",
        7: " Z",
        8: " Y"
    }
    def __init__(self, value, format=SI) : 
        self.value = value
        self.format = format
    def __str__(self) : 
        mag = math.log(abs(self.value)) // math.log(self.format)
        return "".join([
            "-" if self.value<0 else "",
            f"""{abs(self.value)/pow(self.format, mag):.2f}""",
            f"""{ReadableSize.Symbols[mag]}{"i" if self.format == ReadableSize.IEC else ""}"""
        ])
