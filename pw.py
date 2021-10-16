class interval:
    def __init__(self, start, end):
        self.start = float(start)
        # self.start_inclusive = start_inclusive
        
        self.end = float(end)
        # self.end_inclusive = end_inclusive

    def contains(self, other):
        return self.start < other.start and self.end > other.end

    def overlaps(self, other):
        return self.start < other.start < self.end

    def __str__(self): 
        return f'({self.start}, {self.end})'

class piecewise:

    def __init__(self):
        self.pw = []

    def add_poly_with_domain(self, polynomial, domain=None):
        mk = [[polynomial, domain]]
        # domains = []
        for i, (func, vals) in enumerate(self.pw):
            if domain.contains(vals):
                self.pw[i] = None
            elif vals.contains(domain):
                mk += [
                    [func, interval(vals.start, domain.start)],
                    [func, interval(domain.end, vals.end)]
                ]
                self.pw[i] = None
            elif domain.overlaps(vals):
                mk += [ [func, interval(domain.end, vals.end)] ]
                self.pw[i] = None
            elif vals.overlaps(domain):
                mk += [ [func, interval(vals.start, domain.start)] ]
                self.pw[i] = None

        self.pw[:] = (e for e in self.pw if e is not None)
        self.pw += mk

    def add_poly_by_transform(self, polynomial):
        for i in range(len(self.pw)):
            self.pw[i][0] = self.pw[i][0].add_poly(polynomial)

    def add_poly(self, polynomial, domain=None):
        if domain is None:
            self.add_poly_by_transform(polynomial)
            return self
        else:
            self.add_poly_with_domain(polynomial, domain)

    def __neg__(self):
        pw = piecewise()
        
        for func, vals in self.pw:
            pw.add_poly_with_domain(-func, vals)

        return pw

    def __abs__(self):
        pw = piecewise()

        for func, vals in self.pw:
            funcs = abs(func)
            for f, v in funcs.pw: 
                pw.add_poly_with_domain(
                    f, 
                    interval(max(vals.start, v.start), min(vals.end, v.end))
                )

        return pw

    def __str__(self):
        return '\n'.join(f'{f} \left\{{{v.start}<x<{v.end}\\right\}}' for f, v in self.pw).replace('inf','\infty')
        # return ' , '.join(f'{{{f}, x in {v}}}' for f, v in self.pw)
