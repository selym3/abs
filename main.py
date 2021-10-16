from poly import poly
from term import term

def question_1():
    # Construct |3 - |2-|1-x||

    a = poly(term(-1, 1), term(1, 0)) # 1-x
    a = -abs(a)                       # -|1-x|  
    a.add_poly(poly(term(2, 0)))      # 2 - |1-x|
    a = -abs(a)                       # -|2 - |1-x||
    a.add_poly(poly(term(3, 0)))      # 3 - |2 - |1-x|
    a = abs(a)                        # |3 - |2 - |1-x||
    
    return "\left\|3 - \left\|2-|1-x||", a

def question_2():
    # Construct |x^2 + |5x+6||

    a = poly(term(5, 1), term(6, 0)) # 5x + 6
    a = abs(a)                       # |5x + 6|
    a.add_poly(poly(term(1, 1)))     # x^2 + |5x+6|
    a = abs(a)                       # |x^2 + |5x + 6||

    return "|x^2 + |5x+6||", a

if __name__ == "__main__":
    tag, exp = question_2()
    
    print(tag)
    print()
    print(exp)