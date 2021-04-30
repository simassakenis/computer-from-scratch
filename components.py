import graphics

# Color constants
lightGray = graphics.color_rgb(245, 245, 245)
green = graphics.color_rgb(76, 217, 100)
black = graphics.color_rgb(10, 10, 10)


# Lowest-level components


class Leg:
    def __init__(self, parent, c=None):
        self.parent = parent # component whose leg this leg is
        self.c = c # component that this leg is connected to
        self.val = 0 # value of this leg


class Branch12:
    def __init__(self, i=None, o1=None, o2=None):
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o1 = Leg(self, o1.parent if o1 is not None else None)
        if o1 is not None: o1.c = self
        self.o2 = Leg(self, o2.parent if o2 is not None else None)
        if o2 is not None: o2.c = self

    def update_right(self, c, val):
        if self.i.val != val:
            self.i.val = val
            self.o1.c.update_right(self, val)
            self.o2.c.update_right(self, val)

    def update_left(self, c, val):
        assert c == self.o1.c or c == self.o2.c
        if c == self.o1.c and self.o1.val != val:
            if self.o1.val == -1:
                self.o2.c.update_right(self, self.i.val)
            self.o1.val = val
            if val == -1:
                self.o2.c.update_right(self, 0)
            if self.o1.val == 0 or self.o2.val == 0:
                self.i.c.update_left(self, self.o1.val + self.o2.val)
            else:
                self.i.c.update_left(self, self.o1.val * self.o2.val)
        elif c == self.o2.c and self.o2.val != val:
            if self.o2.val == -1:
                self.o1.c.update_right(self, self.i.val)
            self.o2.val = val
            if val == -1:
                self.o1.c.update_right(self, 0)
            if self.o1.val == 0 or self.o2.val == 0:
                self.i.c.update_left(self, self.o1.val + self.o2.val)
            else:
                self.i.c.update_left(self, self.o1.val * self.o2.val)


class Branch21:
    def __init__(self, i1=None, i2=None, o=None):
        self.i1 = Leg(self, i1.parent if i1 is not None else None)
        if i1 is not None: i1.c = self
        self.i2 = Leg(self, i2.parent if i2 is not None else None)
        if i2 is not None: i2.c = self
        self.o = Leg(self, o.parent if o is not None else None)
        if o is not None: o.c = self

    def update_right(self, c, val):
        assert c == self.i1.c or c == self.i2.c
        if c == self.i1.c and self.i1.val != val:
            self.i1.val = val
            self.o.c.update_right(self, max(self.i1.val, self.i2.val))
        elif c == self.i2.c and self.i2.val != val:
            self.i2.val = val
            self.o.c.update_right(self, max(self.i1.val, self.i2.val))

    def update_left(self, c, val):
        if self.o.val != val:
            self.o.val = val
            self.i1.c.update_left(self, self.o.val)
            self.i2.c.update_left(self, self.o.val)


class Plus:
    def __init__(self):
        self.o = Leg(self)

    def update_right(self, c, val):
        self.o.c.update_right(self, 1)

    def update_left(self, c, val):
        pass


class Minus:
    def __init__(self):
        self.i = Leg(self)

    def update_right(self, c, val):
        self.i.c.update_left(self, -val)


class Switch:
    def __init__(self, i=None, o=None):
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o = Leg(self, o.parent if o is not None else None)
        if o is not None: o.c = self
        self.pos = 0

    def toggle(self):
        self.pos = abs(self.pos - 1)
        self.o.c.update_right(self, self.i.val * self.pos)

    def update_right(self, c, val):
        if self.i.val != val:
            self.i.val = val
            self.o.c.update_right(self, self.i.val * self.pos)

    def update_left(self, c, val):
        if self.o.val != val:
            self.o.val = val
            self.i.c.update_left(self, self.o.val * self.pos)

    def state(self):
        return abs(self.i.val * self.o.val * self.pos)


class Bulb:
    def __init__(self, i=None, o=None):
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o = Leg(self, o.parent if o is not None else None)
        if o is not None: o.c = self
        
    def update_right(self, c, val):
        if self.i.val != val:
            self.i.val = val
            self.o.c.update_right(self, val)

    def update_left(self, c, val):
        if self.o.val != val:
            self.o.val = val
            self.i.c.update_left(self, abs(val))

    def state(self):
        return abs(self.i.val * self.o.val)


class Transistor:
    def __init__(self, switch=None, i=None, o=None):
        self.switch = Leg(self, switch.parent if switch is not None else None)
        if switch is not None: switch.c = self
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o = Leg(self, o.parent if o is not None else None)
        if o is not None: o.c = self

    def update_right(self, c, val):
        assert c == self.i.c or c == self.switch.c
        if c == self.i.c and self.i.val != val:
            self.i.val = val
            self.o.c.update_right(self, self.i.val * self.switch.val)
        elif c == self.switch.c and self.switch.val != val:
            self.switch.val = val
            self.switch.c.update_left(self, 1)
            self.o.c.update_right(self, self.i.val * self.switch.val)

    def update_left(self, c, val):
        self.o.val = val
        self.i.c.update_left(self, self.o.val * self.switch.val)

    def state(self):
        return abs(self.i.val * self.o.val * self.switch.val)


# Derived components


class NOT:
    def __init__(self, circuit, i=None, o=None):
        plus = circuit.add_plus()
        minus = circuit.add_minus()
        branch = Branch12(i=plus.o)
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
        branch12 = Branch12(i=plus.o)
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


class DLatch:
    def __init__(self, circuit, i1=None, i2=None, o=None):
        branch121 = Branch12()
        branch122 = Branch12()
        and_gate1 = AND(circuit=circuit, i1=branch121.o1, i2=branch122.o1)
        not_gate1 = NOT(circuit=circuit, i=branch121.o2)
        and_gate2 = AND(circuit=circuit, i1=not_gate1.o, i2=branch122.o2)
        or_gate = OR(circuit=circuit, i2=and_gate1.o)
        not_gate2 = NOT(circuit=circuit, i=and_gate2.o)
        and_gate2 = AND(circuit=circuit, i1=or_gate.o, i2=not_gate2.o)
        branch123 = Branch12(i=and_gate2.o, o2=or_gate.i1)
        self.i1 = branch121.i
        if i1 is not None:
            self.i1.c = i1.parent
            i1.c = self.i1.parent
        self.i2 = branch122.i
        if i2 is not None:
            self.i2.c = i2.parent
            i2.c = self.i2.parent
        self.o = branch123.o1
        if o is not None:
            self.o.c = o.parent
            o.c = self.o.parent


# Circuit and display


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

    def initialize(self):
        for p in self.plusses:
            p.update_right(None, None)


class Display:
    def __init__(self, components, labels):
        self.win = graphics.GraphWin(title='Computer', width=1000, height=600)
        self.win.setBackground(lightGray)

        self.components = components
        self.labels = [None] * len(components)
        self.indicators = [None] * len(components)
        dist = 100
        left_most_x = (1000 / 2) - (len(components) - 1) * dist / 2
        for i, c in enumerate(components):
            self.labels[i] = graphics.Text(
                graphics.Point(left_most_x + i * dist, 240),
                labels[i]
            )
            self.labels[i].setFace('courier')
            self.labels[i].setSize(16)
            self.labels[i].draw(self.win)

            self.indicators[i] = graphics.Circle(
                graphics.Point(left_most_x + i * dist, 300),
                radius=12
            )
            self.indicators[i].setFill(black)
            self.indicators[i].setWidth(0)
            self.indicators[i].draw(self.win)

    def update(self):
        for i, c in enumerate(self.components):
            self.indicators[i].setFill(green if c.state() else black)

