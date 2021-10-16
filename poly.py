from term import term
from pw import piecewise, interval

class poly:
    def __init__(self, *terms):
        self.order = -1 if len(terms) == 0 else max(term.order for term in terms)
        self.terms = {}

        for term in terms:
            self.add_term(term)

    def add_term(self, term): # mutates polynomial
        in_poly = term.order in self.terms

        # combine like terms if necessary
        if in_poly:
            new_term = self.terms[term.order].combine(term)
        else:
            new_term = term

        # if the new term's coeffecient is zero, ignore it 
        # and delete from poly if necessary
        if new_term.coeff == 0:
            if in_poly:
                del self.terms[term.order]
                if term.order == self.order:
                    try:              self.order = max(term.order for term in self.terms.values())
                    except Exception: self.order = -1
            return 

        # if new term isn't zeroed out, update it in the polynomial 
        # and update the polynomial's order if necessary
        if term.order > self.order: self.order = term.order
        self.terms[term.order] = new_term

    def add_poly(self, other): # creates new polynomial
        newpoly = poly()
        for term in self.terms.values():
            newpoly.add_term(term)

        for term in other.terms.values():
            newpoly.add_term(term)
        
        return newpoly

    def find_roots(self):
        ld = self.get_leading()
        if ld is None: 
            raise ValueError("cannot find roots of malformed polynomial")

        if ld.order == 0:
            all = float('inf') # represents being equal to the x-axis
            return [] if ld.coeff != 0 else all

        elif ld.order == 1:
            c = self.get_term(order=0)
            return [-c.coeff/ld.coeff]
        
        # higher orders shoudl return double roots to count multiplicty
        elif ld.order == 2:
            a = ld
            b = self.get_term(order=1)
            c = self.get_term(order=0)

            disc = b.coeff**2 - 4 * a.coeff * c.coeff
            if disc < 0: return []
            
            disc **= 0.5
            return [
                (-b.coeff + disc)/(2*a.coeff), 
                (-b.coeff - disc)/(2*a.coeff)
            ]

        else:
            raise ValueError(f"cannot find roots of {ld.order} polynomial yet")

    def get_term(self, order):
        return self.terms[order] if order in self.terms else term(0, order)

    def find_multiplicity(self, sorted=False):
        roots = self.find_roots()
        if sorted: roots.sort()
        counted = {}

        for root in roots:
            if root in counted: counted[root] += 1
            else:               counted[root] =  1

        return counted

    def find_signs(self):
        # store ranges in flat list
        signs = []

        # find end behavoir
        ld = self.get_leading()
        even = ld.order % 2 == 0
        sign = +1 if ld.coeff > 0 else -1

        signs += [(float('-inf'), sign if even else -sign)]
        
        # fill in around the roots
        roots = self.find_multiplicity(sorted=True)

        for root, mult in roots.items():
            last_sign = signs[-1][1]
            if mult%2==0: signs+=[(root, +last_sign)]
            else:         signs+=[(root, -last_sign)]

        # this one is not technically necessay
        signs += [(float('inf'), signs[-1][1])]
        return signs

    def get_leading(self):
        if self.order >= 0:
            return self.terms[self.order]

        return None

    def __neg__(self):
        np = poly()

        for t in self.terms.values():
            np.add_term(term(-t.coeff, t.order))

        return np
    
    def __abs__(self):
        ap = piecewise()
        signs = self.find_signs()

        for i in range(0, len(signs)-1):
            ap.add_poly(
                self if signs[i][1] > 0 else -self, 
                interval(signs[i][0], signs[i+1][0])
            )

        return ap

    def __str__(self):
        polyparts = (str(term) for term in self.terms.values())
        return ' + '.join(polyparts)