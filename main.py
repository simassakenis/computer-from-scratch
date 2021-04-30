import time
import keyboard
from termcolor import colored


class Leg:
    def __init__(self, parent, c=None):
        self.parent = parent
        self.c = c


class Branch:
    def __init__(self, i=None, o1=None, o2=None):
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o1 = Leg(self, o1.parent if o1 is not None else None)
        if o1 is not None: o1.c = self
        self.o2 = Leg(self, o2.parent if o2 is not None else None)
        if o2 is not None: o2.c = self
        self.val = 0
        self.one_received = False

    def zero_out(self):
        self.val = 0
        self.o1.c.zero_out()
        self.o2.c.zero_out()

    def update(self):
        if self.one_received:
            self.val = min(self.o1.c.val, self.o2.c.val)
            if self.val == -1:
                if self.o1.c.val != -1: self.o1.c.zero_out()
                if self.o2.c.val != -1: self.o2.c.zero_out()
            else:
                self.val = max(self.o1.c.val, self.o2.c.val)
            self.i.c.update()
            self.val = abs(self.i.c.val) * self.val
            if self.val == 0:
                self.o1.c.zero_out()
                self.o2.c.zero_out()
            self.one_received = False
        else:
            self.val = 1
            self.one_received = True


class Branch21:
    def __init__(self, i1=None, i2=None, o=None):
        self.i1 = Leg(self, i1.parent if i1 is not None else None)
        if i1 is not None: i1.c = self
        self.i2 = Leg(self, i2.parent if i2 is not None else None)
        if i2 is not None: i2.c = self
        self.o = Leg(self, o.parent if o is not None else None)
        if o is not None: o.c = self
        self.val = 0

    def zero_out(self):
        self.val = max(abs(self.i1.c.val), abs(self.i2.c.val)) * self.val
        if self.val == 0: self.o.c.zero_out()

    def update(self):
        self.val = self.o.c.val
        self.i1.c.update()
        self.i2.c.update()
        self.val = max(abs(self.i1.c.val), abs(self.i2.c.val)) * self.val


class Plus:
    def __init__(self):
        self.o = Leg(self)
        self.val = 1

    def update(self):
        pass


class Minus:
    def __init__(self):
        self.i = Leg(self)
        self.val = -1

    def zero_out(self):
        pass

    def update(self):
        self.val = -1
        self.i.c.update()
        self.val = abs(self.i.c.val) * self.val


class Switch:
    def __init__(self, i=None, o=None):
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o = Leg(self, o.parent if o is not None else None)
        if o is not None: o.c = self
        self.val = 0
        self.pos = 0

    def zero_out(self):
        self.val = 0
        self.o.c.zero_out()

    def update(self):
        self.val = self.o.c.val * self.pos
        self.i.c.update()
        self.val = self.i.c.val * self.val

    def toggle(self):
        self.pos = abs(self.pos - 1)


class Bulb:
    def __init__(self, i=None, o=None):
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o = Leg(self, o.parent if o is not None else None)
        if o is not None: o.c = self
        self.val = 0
        
    def zero_out(self):
        self.val = 0
        self.o.c.zero_out()

    def update(self):
        self.val = abs(self.o.c.val)
        self.i.c.update()
        self.val = self.i.c.val * self.val


class Transistor:
    def __init__(self, switch=None, i=None, o=None):
        self.switch = Leg(self, switch.parent if switch is not None else None)
        if switch is not None: switch.c = self
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o = Leg(self, o.parent if o is not None else None)
        if o is not None: o.c = self
        self.val = 0

    def zero_out(self):
        self.val = 0
        self.o.c.zero_out()

    def update(self):
        self.val = 1
        self.switch.c.update()
        self.val = abs(self.switch.c.val) * self.o.c.val * self.val
        self.i.c.update()
        self.val = abs(self.i.c.val) * self.val


class Circuit:
    def __init__(self):
        self.plusses = []
        self.minuses = []

    def add_plus(self):
        plus = Plus()
        self.plusses.append(plus)
        return plus

    def add_minus(self):
        minus = Minus()
        self.minuses.append(minus)
        return minus

    def update(self):
        for m in self.minuses: m.update()

    def display(self, gadgets):
        indicators = ''
        for gadget in gadgets:
            indicators += colored('● ', 'green' if gadget.val else 'grey')
        print('\t' + indicators, end='\r')


class NOT:
    def __init__(self, circuit, i=None, o=None):
        plus = circuit.add_plus()
        minus = circuit.add_minus()
        branch = Branch(i=plus.o)
        self.transistor = Transistor(i=branch.o2, o=minus.i)
        self.i = self.transistor.switch
        if i is not None:
            self.i.c = i.parent
            i.c = self.i.parent
        self.o = branch.o1
        if o is not None:
            self.o.c = o.parent
            o.c = self.o.parent


class AND:
    def __init__(self, circuit, i1=None, i2=None, o=None):
        plus = circuit.add_plus()
        transistor1 = Transistor(i=plus.o)
        transistor2 = Transistor(i=transistor1.o)
        self.i1 = transistor1.switch
        if i1 is not None:
            self.i1.c = i1.parent
            i1.c = self.i1.parent
        self.i2 = transistor2.switch
        if i2 is not None:
            self.i2.c = i2.parent
            i2.c = self.i2.parent
        self.o = transistor2.o
        if o is not None:
            self.o.c = o.parent
            o.c = self.o.parent


class OR:
    def __init__(self, circuit, i1=None, i2=None, o=None):
        plus = circuit.add_plus()
        branch12 = Branch(i=plus.o)
        branch21 = Branch21()
        self.transistor1 = Transistor(i=branch12.o1, o=branch21.i1)
        self.transistor2 = Transistor(i=branch12.o2, o=branch21.i2)
        self.i1 = self.transistor1.switch
        if i1 is not None:
            self.i1.c = i1.parent
            i1.c = self.i1.parent
        self.i2 = self.transistor2.switch
        if i2 is not None:
            self.i2.c = i2.parent
            i2.c = self.i2.parent
        self.o = branch21.o
        if o is not None:
            self.o.c = o.parent
            o.c = self.o.parent


def user_pressed(jungiklis, circuit, gadgets):
    jungiklis.toggle()
    circuit.update()
    circuit.display(gadgets)


if __name__ == '__main__':
    print()

#     # basic demo
#     circuit = Circuit()
#     plus = circuit.add_plus()
#     minus = circuit.add_minus()
#     jungiklis = Switch(i=plus.o)
#     lempute = Bulb(i=jungiklis.o, o=minus.i)

#     # NOT demo
#     circuit = Circuit()
#     plus = circuit.add_plus()
#     minus = circuit.add_minus()
#     jungiklis = Switch(i=plus.o)
#     lempute = Bulb(o=minus.i)
#     not_gate = NOT(circuit=circuit, i=jungiklis.o)
#     not_gate2 = NOT(circuit=circuit, i=not_gate.o)
#     not_gate3 = NOT(circuit=circuit, i=not_gate2.o)
#     not_gate4 = NOT(circuit=circuit, i=not_gate3.o, o=lempute.i)

#     # AND demo
#     circuit = Circuit()
#     plus1 = circuit.add_plus()
#     plus2 = circuit.add_plus()
#     minus = circuit.add_minus()
#     jungiklis1 = Switch(i=plus1.o)
#     jungiklis2 = Switch(i=plus2.o)
#     and_gate = AND(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
#     lempute = Bulb(i=and_gate.o, o=minus.i)

#     # OR demo
#     circuit = Circuit()
#     plus1 = circuit.add_plus()
#     plus2 = circuit.add_plus()
#     minus = circuit.add_minus()
#     jungiklis1 = Switch(i=plus1.o)
#     jungiklis2 = Switch(i=plus2.o)
#     or_gate = OR(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
#     lempute = Bulb(i=or_gate.o, o=minus.i)

    # XOR demo
    circuit = Circuit()
    plus1 = circuit.add_plus()
    plus2 = circuit.add_plus()
    minus = circuit.add_minus()
    jungiklis1 = Switch(i=plus1.o)
    jungiklis2 = Switch(i=plus2.o)
    branch121 = Branch(i=jungiklis1.o)
    branch122 = Branch(i=jungiklis2.o)
    and_gate = AND(circuit=circuit, i1=branch121.o1, i2=branch122.o1)
    not_gate = NOT(circuit=circuit, i=and_gate.o)
    or_gate = OR(circuit=circuit, i1=branch121.o2, i2=branch122.o2)
    and_gate2 = AND(circuit=circuit, i1=not_gate.o, i2=or_gate.o)
    lempute = Bulb(i=and_gate2.o, o=minus.i)

    user_pressed(jungiklis1, circuit, [jungiklis1, jungiklis2, lempute])
    user_pressed(jungiklis2, circuit, [jungiklis1, jungiklis2, lempute])

    keyboard.on_press_key('a', lambda _: user_pressed(jungiklis1, circuit, [jungiklis1, jungiklis2, lempute]))
    keyboard.on_press_key('s', lambda _: user_pressed(jungiklis2, circuit, [jungiklis1, jungiklis2, lempute]))

    while True:
        time.sleep(60)

