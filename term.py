class term:
    def __init__(self, coeff, order):
        self.coeff = float(coeff)
        self.order = float(order)

        if self.order < 0:
            raise ValueError("value of a term must be greater than 0")

    def combine(self, other):
        if other.order != self.order:
            raise ValueError("these terms are not like terms")

        return term(
            self.coeff + other.coeff, 
            self.order
        )

    def __str__(self):
        if self.order == 0: return f'{self.coeff}'
        
        coeff = '' if self.coeff == 1 else f'{self.coeff}*'
        if self.order == 1: return f'{coeff}x' 
        
        return f"{coeff}x^{self.order}"