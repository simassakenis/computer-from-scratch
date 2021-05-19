import time


# Lowest-level components


class Leg:
    def __init__(self, parent, c=None):
        self.parent = parent # component whose leg this leg is
        self.c = c # component that this leg is connected to
        self.val = 0 # value of this leg


class Branch12:
    def __init__(self, circuit, i=None, o1=None, o2=None):
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o1 = Leg(self, o1.parent if o1 is not None else None)
        if o1 is not None: o1.c = self
        self.o2 = Leg(self, o2.parent if o2 is not None else None)
        if o2 is not None: o2.c = self

    def update_right(self, c, val):
        if self.i.val != val:
            self.i.val = val
            if self.o1.c is not None:
                self.o1.c.update_right(self, val)
            if self.o2.c is not None:
                self.o2.c.update_right(self, val)

    def update_left(self, c, val):
        assert c == self.o1.c or c == self.o2.c
        if c == self.o1.c and self.o1.val != val:
            if self.o1.val == -1:
                if self.o2.c is not None:
                    self.o2.c.update_right(self, self.i.val)
            self.o1.val = val
            if val == -1:
                if self.o2.c is not None:
                    self.o2.c.update_right(self, 0)
            if self.o1.val == 0 or self.o2.val == 0:
                if self.i.c is not None:
                    self.i.c.update_left(self, self.o1.val + self.o2.val)
            else:
                if self.i.c is not None:
                    self.i.c.update_left(self, self.o1.val * self.o2.val)
        elif c == self.o2.c and self.o2.val != val:
            if self.o2.val == -1:
                self.o1.c.update_right(self, self.i.val)
            self.o2.val = val
            if val == -1:
                self.o1.c.update_right(self, 0)
            if self.o1.val == 0 or self.o2.val == 0:
                if self.i.c is not None:
                    self.i.c.update_left(self, self.o1.val + self.o2.val)
            else:
                if self.i.c is not None:
                    self.i.c.update_left(self, self.o1.val * self.o2.val)


class Branch21:
    def __init__(self, circuit, i1=None, i2=None, o=None):
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
            if self.o.c is not None:
                self.o.c.update_right(self, max(self.i1.val, self.i2.val))
        elif c == self.i2.c and self.i2.val != val:
            self.i2.val = val
            if self.o.c is not None:
                self.o.c.update_right(self, max(self.i1.val, self.i2.val))

    def update_left(self, c, val):
        if self.o.val != val:
            self.o.val = val
            if self.i1.c is not None:
                self.i1.c.update_left(self, self.o.val)
            if self.i2.c is not None:
                self.i2.c.update_left(self, self.o.val)


class Plus:
    def __init__(self, circuit):
        self.o = Leg(self)
        circuit.plusses.append(self)

    def update_right(self, c, val):
        if self.o.c is not None:
            self.o.c.update_right(self, 1)

    def update_left(self, c, val):
        pass


class Minus:
    def __init__(self, circuit, i=None):
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self

    def update_right(self, c, val):
        if self.i.c is not None:
            self.i.c.update_left(self, -val)


class Switch:
    def __init__(self, circuit, i=None, o=None, key=None):
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o = Leg(self, o.parent if o is not None else None)
        if o is not None: o.c = self
        self.key = key
        self.pos = 0
        circuit.interactive.append(self)

    def toggle(self):
        self.pos = abs(self.pos - 1)
        if self.o.c is not None:
            self.o.c.update_right(self, self.i.val * self.pos)

    def update_right(self, c, val):
        if self.i.val != val:
            self.i.val = val
            if self.o.c is not None:
                self.o.c.update_right(self, self.i.val * self.pos)

    def update_left(self, c, val):
        if self.o.val != val:
            self.o.val = val
            if self.i.c is not None:
                self.i.c.update_left(self, self.o.val * self.pos)

    def state(self):
        return self.pos

    def update(self, key):
        if key == self.key:
            self.toggle()
            return True
        return False


class Bulb:
    def __init__(self, circuit, i=None, o=None):
        self.i = Leg(self, i.parent if i is not None else None)
        if i is not None: i.c = self
        self.o = Leg(self, o.parent if o is not None else None)
        if o is not None: o.c = self
        
    def update_right(self, c, val):
        if self.i.val != val:
            self.i.val = val
            if self.o.c is not None:
                self.o.c.update_right(self, val)

    def update_left(self, c, val):
        if self.o.val != val:
            self.o.val = val
            if self.i.c is not None:
                self.i.c.update_left(self, abs(val))

    def state(self):
        return abs(self.i.val * self.o.val)


class Transistor:
    def __init__(self, circuit, switch=None, i=None, o=None):
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
            if self.o.c is not None:
                self.o.c.update_right(self, self.i.val * self.switch.val)
        elif c == self.switch.c and self.switch.val != val:
            self.switch.val = val
            if self.switch.c is not None:
                self.switch.c.update_left(self, 1)
            if self.o.c is not None:
                self.o.c.update_right(self, self.i.val * self.switch.val)

    def update_left(self, c, val):
        self.o.val = val
        if self.i.c is not None:
            self.i.c.update_left(self, self.o.val * self.switch.val)

    def state(self):
        return abs(self.i.val * self.o.val * self.switch.val)


# Derived components


class NOT:
    def __init__(self, circuit, i=None, o=None):
        branch = Branch12(circuit=circuit, i=circuit.add_plus().o)
        self.transistor = Transistor(circuit=circuit, i=branch.o2,
                                     o=circuit.add_minus().i)
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
        transistor1 = Transistor(circuit=circuit, i=circuit.add_plus().o)
        transistor2 = Transistor(circuit=circuit, i=transistor1.o)
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
        branch12 = Branch12(circuit=circuit, i=circuit.add_plus().o)
        branch21 = Branch21(circuit=circuit)
        self.transistor1 = Transistor(circuit=circuit, i=branch12.o1, o=branch21.i1)
        self.transistor2 = Transistor(circuit=circuit, i=branch12.o2, o=branch21.i2)
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


class XOR:
    def __init__(self, circuit, i1=None, i2=None, o=None):
        branch121 = Branch12(circuit=circuit)
        branch122 = Branch12(circuit=circuit)
        and_gate = AND(circuit=circuit, i1=branch121.o1, i2=branch122.o1)
        not_gate = NOT(circuit=circuit, i=and_gate.o)
        or_gate = OR(circuit=circuit, i1=branch121.o2, i2=branch122.o2)
        and_gate2 = AND(circuit=circuit, i1=not_gate.o, i2=or_gate.o)
        self.i1 = branch121.i
        if i1 is not None:
            self.i1.c = i1.parent
            i1.c = self.i1.parent
        self.i2 = branch122.i
        if i2 is not None:
            self.i2.c = i2.parent
            i2.c = self.i2.parent
        self.o = and_gate2.o
        if o is not None:
            self.o.c = o.parent
            o.c = self.o.parent


class Branch1n:
    def __init__(self, circuit, n, i=None, o=None):
        branch = Branch12(circuit=circuit)
        self.i = [branch.i]
        self.o = [branch.o1]
        assert n >= 2
        for _ in range(n - 2):
            branch = Branch12(circuit=circuit, i=branch.o2)
            self.o.append(branch.o1)
        self.o.append(branch.o2)
        for j in range(len(self.i)):
            if i is not None and len(i) > j and i[j] is not None:
                self.i[j].c = i[j].parent
                i[j].c = self.i[j].parent
        for j in range(len(self.o)):
            if o is not None and len(o) > j and o[j] is not None:
                self.o[j].c = o[j].parent
                o[j].c = self.o[j].parent


class MultiSwitch:
    def __init__(self, circuit, n, switch=None, i=None, o=None):
        branch = Branch1n(circuit=circuit, n=n)
        transistors = [Transistor(circuit=circuit, switch=branch.o[j])
                       for j in range(n)]
        self.switch = branch.i[0]
        if switch is not None:
            self.switch.c = switch.parent
            switch.c = self.switch.parent
        self.i = [transistors[j].i for j in range(n)]
        for j in range(len(self.i)):
            if i is not None and len(i) > j and i[j] is not None:
                self.i[j].c = i[j].parent
                i[j].c = self.i[j].parent
        self.o = [transistors[j].o for j in range(n)]
        for j in range(len(self.o)):
            if o is not None and len(o) > j and o[j] is not None:
                self.o[j].c = o[j].parent
                o[j].c = self.o[j].parent


class MultiBulbs:
    def __init__(self, circuit, n, i=None, o=None):
        branches = [Branch12(circuit=circuit) for j in range(n)]
        self.bulbs = [Bulb(circuit=circuit,
                           i=branches[j].o1,
                           o=circuit.add_minus().i)
                      for j in range(n)]
        self.i = [branches[j].i for j in range(n)]
        for j in range(len(self.i)):
            if i is not None and len(i) > j and i[j] is not None:
                self.i[j].c = i[j].parent
                i[j].c = self.i[j].parent
        self.o = [branches[j].o2 for j in range(n)]
        for j in range(len(self.o)):
            if o is not None and len(o) > j and o[j] is not None:
                self.o[j].c = o[j].parent
                o[j].c = self.o[j].parent


class ManualSwitches:
    def __init__(self, circuit, n, keys, we_key, o=None):
        self.switches = [Switch(circuit=circuit,
                                i=circuit.add_plus().o,
                                key=keys[j])
                         for j in range(n)]
        self.we_switch = Switch(circuit=circuit, i=circuit.add_plus().o,
                                key=we_key)
        we = MultiSwitch(circuit=circuit, switch=self.we_switch.o,
                         i=[self.switches[j].o for j in range(n)], n=n)
        self.o = we.o
        for j in range(len(self.o)):
            if o is not None and len(o) > j and o[j] is not None:
                self.o[j].c = o[j].parent
                o[j].c = self.o[j].parent


class DLatch:
    def __init__(self, circuit, i1=None, i2=None, o=None):
        branch121 = Branch12(circuit=circuit)
        branch122 = Branch12(circuit=circuit)
        and_gate1 = AND(circuit=circuit, i1=branch121.o1, i2=branch122.o1)
        not_gate1 = NOT(circuit=circuit, i=branch121.o2)
        and_gate2 = AND(circuit=circuit, i1=not_gate1.o, i2=branch122.o2)
        or_gate = OR(circuit=circuit, i2=and_gate1.o)
        not_gate2 = NOT(circuit=circuit, i=and_gate2.o)
        and_gate2 = AND(circuit=circuit, i1=or_gate.o, i2=not_gate2.o)
        branch123 = Branch12(circuit=circuit, i=and_gate2.o, o2=or_gate.i1)
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


class Register:
    def __init__(self, circuit, n, i=None, o=None, re=None, clk=None):
        re_and = AND(circuit=circuit)
        re_branch = Branch1n(circuit=circuit, i=[re_and.o], n=n)
        dlatches = [DLatch(circuit=circuit, i2=re_branch.o[j])
                    for j in range(n)]
        mbulbs = MultiBulbs(circuit=circuit,
                            i=[dlatches[j].o for j in range(n)], n=n)
        self.bulbs = mbulbs.bulbs
        self.i = [dlatches[j].i1 for j in range(n)]
        for j in range(len(self.i)):
            if i is not None and len(i) > j and i[j] is not None:
                self.i[j].c = i[j].parent
                i[j].c = self.i[j].parent
        self.o = mbulbs.o
        for j in range(len(self.o)):
            if o is not None and len(o) > j and o[j] is not None:
                self.o[j].c = o[j].parent
                o[j].c = self.o[j].parent
        self.re = re_and.i1
        if re is not None:
            self.re.c = re.parent
            re.c = self.re.parent
        self.clk = re_and.i2
        if clk is not None:
            self.clk.c = clk.parent
            clk.c = self.clk.parent


class FullAdder:
    def __init__(self, circuit, a=None, b=None, ci=None, s=None, co=None):
        branch12a = Branch12(circuit=circuit)
        branch12b = Branch12(circuit=circuit)
        xor_gate1 = XOR(circuit=circuit, i1=branch12a.o1, i2=branch12b.o1)
        branch12xor = Branch12(circuit=circuit, i=xor_gate1.o)
        branch12c = Branch12(circuit=circuit)
        xor_gate2 = XOR(circuit=circuit, i1=branch12xor.o1, i2=branch12c.o1)
        and_gate1 = AND(circuit=circuit, i1=branch12a.o2, i2=branch12b.o2)
        and_gate2 = AND(circuit=circuit, i1=branch12xor.o2, i2=branch12c.o2)
        or_gate = OR(circuit=circuit, i1=and_gate1.o, i2=and_gate2.o)
        self.a = branch12a.i
        if a is not None:
            self.a.c = a.parent
            a.c = self.a.parent
        self.b = branch12b.i
        if b is not None:
            self.b.c = b.parent
            b.c = self.b.parent
        self.ci = branch12c.i
        if ci is not None:
            self.ci.c = ci.parent
            ci.c = self.ci.parent
        self.s = xor_gate2.o
        if s is not None:
            self.s.c = s.parent
            s.c = self.s.parent
        self.co = or_gate.o
        if co is not None:
            self.co.c = co.parent
            co.c = self.co.parent


class nBitAdder:
    def __init__(self, circuit, n, a=None, b=None, ci=None, s=None, co=None):
        adders = []
        for j in range(n):
            adder = FullAdder(circuit=circuit,
                              ci=None if j == 0 else adders[-1].co)
            adders.append(adder)
        self.a = [adders[j].a for j in range(n)]
        for j in range(len(self.a)):
            if a is not None and len(a) > j and a[j] is not None:
                self.a[j].c = a[j].parent
                a[j].c = self.a[j].parent
        self.b = [adders[j].b for j in range(n)]
        for j in range(len(self.b)):
            if b is not None and len(b) > j and b[j] is not None:
                self.b[j].c = b[j].parent
                b[j].c = self.b[j].parent
        self.ci = adders[0].ci
        if ci is not None:
            self.ci.c = ci.parent
            ci.c = self.ci.parent
        self.s = [adders[j].s for j in range(n)]
        for j in range(len(self.s)):
            if s is not None and len(s) > j and s[j] is not None:
                self.s[j].c = s[j].parent
                s[j].c = self.s[j].parent
        self.co = adders[-1].co
        if co is not None:
            self.co.c = co.parent
            co.c = self.co.parent


class ALU:
    def __init__(self, circuit, n, a=None, b=None, s=None, we=None, su=None):
        su_branches = Branch1n(circuit=circuit, n=n+1)
        su_xors = [XOR(circuit=circuit, i1=su_branches.o[j]) for j in range(n)]
        adder = nBitAdder(circuit=circuit, b=[su_xors[j].o for j in range(n)],
                          ci=su_branches.o[-1], n=n)
        mbulbs = MultiBulbs(circuit=circuit, i=adder.s, n=n)
        self.bulbs = mbulbs.bulbs
        we_mswitch = MultiSwitch(circuit=circuit, i=mbulbs.o, n=n)
        self.a = adder.a
        for j in range(len(self.a)):
            if a is not None and len(a) > j and a[j] is not None:
                self.a[j].c = a[j].parent
                a[j].c = self.a[j].parent
        self.b = [su_xors[j].i2 for j in range(n)]
        for j in range(len(self.b)):
            if b is not None and len(b) > j and b[j] is not None:
                self.b[j].c = b[j].parent
                b[j].c = self.b[j].parent
        self.s = we_mswitch.o
        for j in range(len(self.s)):
            if s is not None and len(s) > j and s[j] is not None:
                self.s[j].c = s[j].parent
                s[j].c = self.s[j].parent
        self.we = we_mswitch.switch
        if we is not None:
            self.we.c = we.parent
            we.c = self.we.parent
        self.su = su_branches.i[0]
        if su is not None:
            self.su.c = su.parent
            su.c = self.su.parent


class Clock:
    def __init__(self, circuit, o1=None, o2=None):
        self.manual_mode = False
        self.speed = 0.5 # in Hertz
        self.delta = 0.5 # in Hertz
        self.t = time.time()
        self.switch = Switch(circuit=circuit, i=circuit.add_plus().o)
        self.edge_switch = Switch(circuit=circuit, i=circuit.add_plus().o)
        self.o1 = self.switch.o
        if o1 is not None:
            self.o1.c = o1.parent
            o1.c = self.o1.parent
        self.o2 = self.edge_switch.o
        if o2 is not None:
            self.o2.c = o2.parent
            o2.c = self.o2.parent
        circuit.interactive.append(self)

    def update(self, key):
        if key in ['minus', 'equal']:
            self.speed += self.delta * (1 if key == 'equal' else -1)
            if self.speed <= 0:
                print('minimum clock speed reached')
                self.speed = self.delta
            print(f'clock speed: {self.speed} Hz')
        elif key == 'x':
            self.manual_mode = not self.manual_mode
            print(f'clock mode: {"manual" if self.manual_mode else "automatic"}')

        tock = time.time() - self.t >= 1 / (self.speed * 2)
        if ((tock and self.switch.pos)
            or (tock and not self.manual_mode)
            or (key == 'c' and self.manual_mode and not self.switch.pos)):
            self.t = time.time()
            self.switch.toggle()
            if self.switch.pos:
                self.edge_switch.toggle()
                self.edge_switch.toggle()
            return True
        return False


class Bus:
    def __init__(self, circuit, n):
        self.n = n
        self.circuit = circuit
        self.minuses = [Minus(circuit=circuit) for _ in range(self.n)]
        self.bulbs = [Bulb(circuit=circuit, o=self.minuses[j].i)
                      for j in range(self.n)]
        self.pins_in = [bulb.i for bulb in self.bulbs]
        self.pins_out = [bulb.o for bulb in self.bulbs]

    def add_read(self):
        branches = [Branch12(circuit=self.circuit,
                             i=self.pins_out[j],
                             o1=self.minuses[j].i)
                    for j in range(self.n)]
        self.pins_out = [branch.o1 for branch in branches]
        return [branch.o2 for branch in branches]

    def add_write(self):
        branches = [Branch21(circuit=self.circuit, o=self.pins_in[j])
                    for j in range(self.n)]
        self.pins_in = [branch.i1 for branch in branches]
        return [branch.i2 for branch in branches]


# Circuit


class Circuit:
    def __init__(self):
        self.plusses = []
        self.interactive = []

    def initialize(self):
        for p in self.plusses:
            p.update_right(None, None)

    def add_plus(self):
        plus = Plus(circuit=self)
        self.plusses.append(plus)
        return plus

    def add_minus(self):
        return Minus(circuit=self)

    def update(self, key):
        return sum(c.update(key) for c in self.interactive) > 0


