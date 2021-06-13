import time
import math


# Lowest-level components


class Leg:
    def __init__(self, parent, c=None):
        self.parent = parent # component whose leg this leg is
        self.c = c # component that this leg is connected to
        self.val = 0 # value of this leg


def init_legs(component, locals_dict, leg_names):
    for key, value in locals_dict.items():
        if key in leg_names:
            if value is None:
                setattr(component, key, Leg(component))
            else:
                setattr(component, key, Leg(component, value.parent))
                value.c = component


def connect_legs(component, locals_dict, leg_names):
    for key, value in locals_dict.items():
        if key in leg_names and value is not None:
            leg = getattr(component, key)
            if isinstance(leg, list):
                for j in range(len(leg)):
                    if len(value) > j and value[j] is not None:
                        leg[j].c = value[j].parent
                        value[j].c = leg[j].parent
            else:
                leg.c = value.parent
                value.c = leg.parent


class Branch12:
    def __init__(self, circuit, i=None, o1=None, o2=None):
        init_legs(self, locals(), ['i', 'o1', 'o2'])

    def update_right(self, c, val):
        if self.i.val != val:
            self.i.val = val
            return [(self.o2.c, 'r', self, val), (self.o1.c, 'r', self, val)]
        return []

    def update_left(self, c, val):
        assert c == self.o1.c or c == self.o2.c
        ret = []
        if c == self.o1.c and self.o1.val != val:
            if self.o1.val == -1:
                ret.append((self.o2.c, 'r', self, self.i.val))
            self.o1.val = val
            if val == -1:
                ret.append((self.o2.c, 'r', self, 0))
            if self.o1.val == 0 or self.o2.val == 0:
                ret.append((self.i.c, 'l', self, self.o1.val + self.o2.val))
            else:
                ret.append((self.i.c, 'l', self, self.o1.val * self.o2.val))
        elif c == self.o2.c and self.o2.val != val:
            if self.o2.val == -1:
                ret.append((self.o1.c, 'r', self, self.i.val))
            self.o2.val = val
            if val == -1:
                ret.append((self.o1.c, 'r', self, 0))
            if self.o1.val == 0 or self.o2.val == 0:
                ret.append((self.i.c, 'l', self, self.o1.val + self.o2.val))
            else:
                ret.append((self.i.c, 'l', self, self.o1.val * self.o2.val))
        return ret[::-1]


class Branch21:
    def __init__(self, circuit, i1=None, i2=None, o=None):
        init_legs(self, locals(), ['i1', 'i2', 'o'])

    def update_right(self, c, val):
        assert c == self.i1.c or c == self.i2.c
        if c == self.i1.c and self.i1.val != val:
            self.i1.val = val
            return [(self.o.c, 'r', self, max(self.i1.val, self.i2.val))]
        elif c == self.i2.c and self.i2.val != val:
            self.i2.val = val
            return [(self.o.c, 'r', self, max(self.i1.val, self.i2.val))]
        return []

    def update_left(self, c, val):
        if self.o.val != val:
            self.o.val = val
            return [(self.i2.c, 'l', self, val), (self.i1.c, 'l', self, val)]
        return []


class Plus:
    def __init__(self, circuit, o=None):
        init_legs(self, locals(), ['o'])
        circuit.plusses.append(self)

    def update_right(self, c, val):
        return [(self.o.c, 'r', self, 1)]

    def update_left(self, c, val):
        return []


class Minus:
    def __init__(self, circuit, i=None):
        init_legs(self, locals(), ['i'])

    def update_right(self, c, val):
        return [(self.i.c, 'l', self, -val)]


class Switch:
    def __init__(self, circuit, i=None, o=None, key=None):
        init_legs(self, locals(), ['i', 'o'])
        self.key = key
        self.pos = 0
        self.circuit = circuit
        circuit.switches.append(self)

    def toggle(self):
        self.pos = abs(self.pos - 1)
        self.circuit.update_loop([(self.o.c, 'r', self, self.i.val * self.pos)])

    def update_right(self, c, val):
        if self.i.val != val:
            self.i.val = val
            return [(self.o.c, 'r', self, self.i.val * self.pos)]
        return[]

    def update_left(self, c, val):
        if self.o.val != val:
            self.o.val = val
            return [(self.i.c, 'l', self, self.o.val * self.pos)]
        return[]

    def state(self):
        return self.pos

    def update(self, key):
        if key == self.key:
            self.toggle()
            return True
        return False


class Bulb:
    def __init__(self, circuit, i=None, o=None):
        init_legs(self, locals(), ['i', 'o'])
        
    def update_right(self, c, val):
        if self.i.val != val:
            self.i.val = val
            return [(self.o.c, 'r', self, val)]
        return[]

    def update_left(self, c, val):
        if self.o.val != val:
            self.o.val = val
            return [(self.i.c, 'l', self, abs(val))]
        return[]

    def state(self):
        return abs(self.i.val * self.o.val)


class Transistor:
    def __init__(self, circuit, switch=None, i=None, o=None):
        init_legs(self, locals(), ['switch', 'i', 'o'])

    def update_right(self, c, val):
        assert c == self.i.c or c == self.switch.c
        if c == self.i.c and self.i.val != val:
            self.i.val = val
            return [(self.o.c, 'r', self, self.i.val * self.switch.val)]
        elif c == self.switch.c and self.switch.val != val:
            self.switch.val = val
            return [(self.o.c, 'r', self, self.i.val * self.switch.val),
                    (self.switch.c, 'l', self, 1)]
        return []

    def update_left(self, c, val):
        self.o.val = val
        return [(self.i.c, 'l', self, self.o.val * self.switch.val)]

    def state(self):
        return abs(self.i.val * self.o.val * self.switch.val)


# Derived components


class NOT:
    def __init__(self, circuit, i=None, o=None):
        branch = Branch12(circuit=circuit, i=circuit.add_plus().o)
        transistor = Transistor(circuit=circuit, i=branch.o2,
                                o=circuit.add_minus().i)
        self.i = transistor.switch
        self.o = branch.o1
        connect_legs(self, locals(), ['i', 'o'])


class AND:
    def __init__(self, circuit, i1=None, i2=None, o=None):
        transistor1 = Transistor(circuit=circuit, i=circuit.add_plus().o)
        transistor2 = Transistor(circuit=circuit, i=transistor1.o)
        self.i1 = transistor1.switch
        self.i2 = transistor2.switch
        self.o = transistor2.o
        connect_legs(self, locals(), ['i1', 'i2', 'o'])


class OR:
    def __init__(self, circuit, i1=None, i2=None, o=None):
        branch12 = Branch12(circuit=circuit, i=circuit.add_plus().o)
        branch21 = Branch21(circuit=circuit)
        self.transistor1 = Transistor(circuit=circuit, i=branch12.o1, o=branch21.i1)
        self.transistor2 = Transistor(circuit=circuit, i=branch12.o2, o=branch21.i2)
        self.i1 = self.transistor1.switch
        self.i2 = self.transistor2.switch
        self.o = branch21.o
        connect_legs(self, locals(), ['i1', 'i2', 'o'])


class XOR:
    def __init__(self, circuit, i1=None, i2=None, o=None):
        branch121 = Branch12(circuit=circuit)
        branch122 = Branch12(circuit=circuit)
        and_gate = AND(circuit=circuit, i1=branch121.o1, i2=branch122.o1)
        not_gate = NOT(circuit=circuit, i=and_gate.o)
        or_gate = OR(circuit=circuit, i1=branch121.o2, i2=branch122.o2)
        and_gate2 = AND(circuit=circuit, i1=not_gate.o, i2=or_gate.o)
        self.i1 = branch121.i
        self.i2 = branch122.i
        self.o = and_gate2.o
        connect_legs(self, locals(), ['i1', 'i2', 'o'])


class Branch1n:
    def __init__(self, circuit, n, i=None, o=None):
        n = max(n, 2)
        branch = Branch12(circuit=circuit)
        self.i = [branch.i]
        self.o = [branch.o1]
        for _ in range(n - 2):
            branch = Branch12(circuit=circuit, i=branch.o2)
            self.o.append(branch.o1)
        self.o.append(branch.o2)
        connect_legs(self, locals(), ['i', 'o'])


class Branchn1:
    def __init__(self, circuit, n, i=None, o=None):
        n = max(n, 2)
        branch = Branch21(circuit=circuit)
        self.i = [branch.i1]
        self.o = [branch.o]
        for _ in range(n - 2):
            branch = Branch21(circuit=circuit, o=branch.i2)
            self.i.append(branch.i1)
        self.i.append(branch.i2)
        connect_legs(self, locals(), ['i', 'o'])


class MultiSwitch:
    def __init__(self, circuit, n, switch=None, i=None, o=None):
        branch = Branch1n(circuit=circuit, n=n)
        transistors = [Transistor(circuit=circuit, switch=branch.o[j])
                       for j in range(n)]
        self.switch = branch.i[0]
        self.i = [transistors[j].i for j in range(n)]
        self.o = [transistors[j].o for j in range(n)]
        connect_legs(self, locals(), ['switch', 'i', 'o'])


class MultiBulbs:
    def __init__(self, circuit, n, i=None, o=None):
        branches = [Branch12(circuit=circuit) for j in range(n)]
        self.bulbs = [Bulb(circuit=circuit,
                           i=branches[j].o1,
                           o=circuit.add_minus().i)
                      for j in range(n)]
        self.i = [branches[j].i for j in range(n)]
        self.o = [branches[j].o2 for j in range(n)]
        connect_legs(self, locals(), ['i', 'o'])


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
        connect_legs(self, locals(), ['o'])


class SRLatch:
    def __init__(self, circuit, s=None, r=None, o=None):
        or_gate = OR(circuit=circuit)
        not_gate = NOT(circuit=circuit)
        and_gate = AND(circuit=circuit, i1=or_gate.o, i2=not_gate.o)
        branch = Branch12(circuit=circuit, i=and_gate.o, o2=or_gate.i1)
        self.s = or_gate.i2
        self.r = not_gate.i
        self.o = branch.o1
        connect_legs(self, locals(), ['s', 'r', 'o'])


class DLatch:
    def __init__(self, circuit, i1=None, i2=None, o=None, reset=None):
        reset_branch = Branch12(circuit=circuit)
        reset_not = NOT(circuit=circuit, i=reset_branch.o1)
        reset_transistor = Transistor(circuit=circuit, switch=reset_not.o)
        branch121 = Branch12(circuit=circuit, i=reset_transistor.o)
        we_or_gate = OR(circuit=circuit, i2=reset_branch.o2)
        branch122 = Branch12(circuit=circuit, i=we_or_gate.o)
        and_gate1 = AND(circuit=circuit, i1=branch121.o1, i2=branch122.o1)
        not_gate1 = NOT(circuit=circuit, i=branch121.o2)
        and_gate2 = AND(circuit=circuit, i1=not_gate1.o, i2=branch122.o2)
        or_gate = OR(circuit=circuit, i2=and_gate1.o)
        not_gate2 = NOT(circuit=circuit, i=and_gate2.o)
        and_gate2 = AND(circuit=circuit, i1=or_gate.o, i2=not_gate2.o)
        branch123 = Branch12(circuit=circuit, i=and_gate2.o, o2=or_gate.i1)
        self.i1 = reset_transistor.i
        self.i2 = we_or_gate.i1
        self.o = branch123.o1
        self.reset = reset_branch.i
        connect_legs(self, locals(), ['i1', 'i2', 'o', 'reset'])


class Register:
    def __init__(self, circuit, n, i=None, o=None,
                 re=None, clk=None, reset=None):
        re_and = AND(circuit=circuit)
        re_branch = Branch1n(circuit=circuit, i=[re_and.o], n=n)
        reset_branch = Branch1n(circuit=circuit, n=n)
        dlatches = [DLatch(circuit=circuit, i2=re_branch.o[j],
                           reset=reset_branch.o[j])
                    for j in range(n)]
        mbulbs = MultiBulbs(circuit=circuit,
                            i=[dlatches[j].o for j in range(n)], n=n)
        self.bulbs = mbulbs.bulbs
        self.i = [dlatches[j].i1 for j in range(n)]
        self.o = mbulbs.o
        self.re = re_and.i1
        self.clk = re_and.i2
        self.reset = reset_branch.i[0]
        connect_legs(self, locals(), ['i', 'o', 're', 'clk', 'reset'])


class Decoder:
    def __init__(self, circuit, n, i=None, o=None):
        m = int(math.log2(n))
        assert n >= 2 and m == math.log2(n)
        if m == 1:
            branch = Branch12(circuit=circuit)
            not_gate = NOT(circuit=circuit, i=branch.o1)
            self.i = [branch.i]
            self.o = [not_gate.o, branch.o2]
        else:
            branches = [Branch12(circuit=circuit) for _ in range(m)]
            not_gate = NOT(circuit=circuit, i=branches[-1].o1)
            decoder_low = Decoder(circuit=circuit,
                                  i=[branches[j].o1 for j in range(m-1)],
                                  n=n//2)
            mswitch_low = MultiSwitch(circuit=circuit, i=decoder_low.o,
                                      switch=not_gate.o, n=n//2)
            decoder_high = Decoder(circuit=circuit,
                                   i=[branches[j].o2 for j in range(m-1)],
                                   n=n//2)
            mswitch_high = MultiSwitch(circuit=circuit, i=decoder_high.o,
                                       switch=branches[-1].o2, n=n//2)
            self.i = [branches[j].i for j in range(m)]
            self.o = mswitch_low.o + mswitch_high.o
        connect_legs(self, locals(), ['i', 'o'])


class Selector:
    def __init__(self, circuit, n, a=None, b=None, o=None, s=None):
        s_branch = Branch1n(circuit=circuit, n=4)
        s_nots = [NOT(circuit=circuit, i=s_branch.o[j]) for j in [2, 3]]
        a_mswitch = MultiSwitch(circuit=circuit, switch=s_branch.o[1], n=n)
        b_mswitch = MultiSwitch(circuit=circuit, switch=s_nots[0].o, n=n)
        o_branches = [Branch21(circuit=circuit, i1=a_mswitch.o[j],
                               i2=b_mswitch.o[j])
                      for j in range(n)]
        we_xor = XOR(circuit=circuit, i1=s_branch.o[0], i2=s_nots[1].o)
        we_branch = Branch1n(circuit=circuit, i=[we_xor.o], n=n)
        dlatches = [DLatch(circuit=circuit, i1=o_branches[j].o,
                           i2=we_branch.o[j])
                    for j in range(n)]
        self.a = a_mswitch.i
        self.b = b_mswitch.i
        self.o = [dlatches[j].o for j in range(n)]
        self.s = s_branch.i[0]
        connect_legs(self, locals(), ['a', 'b', 'o', 's'])


class SRAM:
    def __init__(self, circuit, nbytes, a=None, i=None, o=None,
                 re=None, we=None):
        addr_bulbs = MultiBulbs(circuit=circuit, n=int(math.log2(nbytes)))
        self.addr_bulbs = addr_bulbs.bulbs
        decoder = Decoder(circuit=circuit, i=addr_bulbs.o, n=nbytes)
        dec_mbulbs = MultiBulbs(circuit=circuit, i=decoder.o, n=nbytes)
        self.dec_bulbs = dec_mbulbs.bulbs
        a_branches = [Branch12(circuit=circuit, i=dec_mbulbs.o[k])
                      for k in range(nbytes)]
        re_mswitch = MultiSwitch(circuit=circuit,
                                 i=[a_branches[k].o1 for k in range(nbytes)],
                                 n=nbytes)
        re_branches = [Branch1n(circuit=circuit, i=[re_mswitch.o[k]], n=8)
                       for k in range(nbytes)]
        d_branches = [Branch1n(circuit=circuit, n=nbytes) for j in range(8)]
        dlatches = [[DLatch(circuit=circuit, i1=d_branches[j].o[k],
                            i2=re_branches[k].o[j])
                     for j in range(8)]
                    for k in range(nbytes)]
        o_mswitches = [MultiSwitch(circuit=circuit,
                                   i=[dlatches[k][j].o for j in range(8)],
                                   switch=a_branches[k].o2, n=8)
                       for k in range(nbytes)]
        o_branches = [Branchn1(circuit=circuit,
                               i=[o_mswitches[k].o[j] for k in range(nbytes)],
                               n=nbytes)
                      for j in range(8)]
        o_mbulbs = MultiBulbs(circuit=circuit,
                              i=[o_branches[j].o[0] for j in range(8)], n=8)
        self.bulbs = o_mbulbs.bulbs
        we_mswitch = MultiSwitch(circuit=circuit, i=o_mbulbs.o, n=8)
        self.a = addr_bulbs.i
        self.i = [d_branches[j].i[0] for j in range(8)]
        self.o = we_mswitch.o
        self.re = re_mswitch.switch
        self.we = we_mswitch.switch
        connect_legs(self, locals(), ['a', 'i', 'o', 're', 'we'])


class SRAMProgrammer:
    def __init__(self, circuit, nbytes, pm_key, a_keys, d_keys, re_key,
                 a, i, re, ao=None, io=None, reo=None,
                 content=None):
        m = int(math.log2(nbytes))
        assert m == math.log2(nbytes)
        assert len(a_keys) == m and len(d_keys) == 8

        self.a_switches = ManualSwitches(circuit=circuit, keys=a_keys[::-1],
                                         we_key=pm_key, n=m)
        self.d_switches = ManualSwitches(circuit=circuit, keys=d_keys[::-1],
                                         we_key=pm_key, n=8)
        self.re_switch = Switch(circuit=circuit, i=circuit.add_plus().o,
                                key=re_key)
        self.pm_switch = Switch(circuit=circuit, i=circuit.add_plus().o,
                                key=pm_key)
        selector = Selector(
            circuit=circuit,
            a=self.a_switches.o + self.d_switches.o + [self.re_switch.o],
            b=a + i + [re],
            s=self.pm_switch.o,
            n=m + 8 + 1
        )
        self.ao = selector.o[:m]
        self.io = selector.o[m:m+8]
        self.reo = selector.o[-1]
        connect_legs(self, locals(), ['ao', 'io', 'reo'])

        self.pm_key = pm_key
        self.a_keys = a_keys
        self.d_keys = d_keys
        self.re_key = re_key
        self.content = content
        circuit.sram_programmers.append(self)


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
        self.b = branch12b.i
        self.ci = branch12c.i
        self.s = xor_gate2.o
        self.co = or_gate.o
        connect_legs(self, locals(), ['a', 'b', 'ci', 's', 'co'])


class nBitAdder:
    def __init__(self, circuit, n, a=None, b=None, ci=None, s=None, co=None):
        adders = []
        for j in range(n):
            adder = FullAdder(circuit=circuit,
                              ci=None if j == 0 else adders[-1].co)
            adders.append(adder)
        self.a = [adders[j].a for j in range(n)]
        self.b = [adders[j].b for j in range(n)]
        self.ci = adders[0].ci
        self.s = [adders[j].s for j in range(n)]
        self.co = adders[-1].co
        connect_legs(self, locals(), ['a', 'b', 'ci', 's', 'co'])


class ALU:
    def __init__(self, circuit, n, a=None, b=None, s=None, we=None,
                 su=None, clk=None, fe=None, fo=None, freset=None):
        su_branches = Branch1n(circuit=circuit, n=n+1)
        su_xors = [XOR(circuit=circuit, i1=su_branches.o[j]) for j in range(n)]
        adder = nBitAdder(circuit=circuit, b=[su_xors[j].o for j in range(n)],
                          ci=su_branches.o[-1], n=n)
        mbulbs = MultiBulbs(circuit=circuit, i=adder.s, n=n)
        self.bulbs = mbulbs.bulbs
        o_branches = [Branch12(circuit=circuit, i=mbulbs.o[j])
                      for j in range(n)]
        zf_nots = [NOT(circuit=circuit, i=o_branches[j].o2) for j in range(n)]
        zf_ands = [AND(circuit=circuit, i1=zf_nots[0].o, i2=zf_nots[1].o)]
        for j in range(2, n):
            zf_ands.append(AND(circuit=circuit, i1=zf_nots[j].o,
                               i2=zf_ands[-1].o))
        flags_reg = Register(circuit=circuit, i=[adder.co, zf_ands[-1].o], n=2)
        flags_bulbs = MultiBulbs(circuit=circuit, i=flags_reg.o, n=2)
        self.fbulbs = flags_bulbs.bulbs
        we_mswitch = MultiSwitch(circuit=circuit,
                                 i=[o_branches[j].o1 for j in range(n)], n=n)
        self.a = adder.a
        self.b = [su_xors[j].i2 for j in range(n)]
        self.s = we_mswitch.o
        self.we = we_mswitch.switch
        self.su = su_branches.i[0]
        self.clk = flags_reg.clk
        self.fe = flags_reg.re
        self.fo = flags_bulbs.o
        self.freset = flags_reg.reset
        connect_legs(self, locals(),
                     ['a', 'b', 's', 'we', 'su', 'clk', 'fe', 'fo', 'freset'])


class Clock:
    def __init__(self, circuit, hlt=None, o1=None, o2=None):
        self.manual_mode = True
        self.speed = 0.5 # in Hertz
        self.delta = 0.5 # in Hertz
        self.t = time.time()

        hlt_not = NOT(circuit=circuit)
        transistor = Transistor(circuit=circuit, i=circuit.add_plus().o,
                                switch=hlt_not.o)
        tr_branch = Branch12(circuit=circuit, i=transistor.o)
        self.switch = Switch(circuit=circuit, i=tr_branch.o1)
        self.edge_switch = Switch(circuit=circuit, i=tr_branch.o2)
        mbulbs = MultiBulbs(circuit=circuit,
                            i=[self.switch.o, self.edge_switch.o], n=2)
        self.bulb = mbulbs.bulbs[0]
        self.hlt = hlt_not.i
        self.o1 = mbulbs.o[0]
        self.o2 = mbulbs.o[1]
        connect_legs(self, locals(), ['hlt', 'o1', 'o2'])
        circuit.clocks.append(self)

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


class ClockDivider:
    def __init__(self, circuit, clk=None, i=None, o=None, je=None, we=None):
        je_branch = Branch1n(circuit=circuit, n=3)
        we_branch = Branch12(circuit=circuit)
        clk_branch = Branch1n(circuit=circuit, n=4)
        clk_nots = [NOT(circuit=circuit, i=clk_branch.o[j]) for j in [1, 3]]
        we1_clk = AND(circuit=circuit, i1=clk_branch.o[0], i2=clk_branch.o[2])
        we1_we = AND(circuit=circuit, i1=we1_clk.o, i2=we_branch.o1)
        we1_je = OR(circuit=circuit, i1=we1_we.o, i2=je_branch.o[0])
        d1_selector = Selector(circuit=circuit, s=je_branch.o[1], n=1)
        dlatch1 = DLatch(circuit=circuit, i1=d1_selector.o[0], i2=we1_je.o)
        we2_clk = AND(circuit=circuit, i1=clk_nots[0].o, i2=clk_nots[1].o)
        we2_we = AND(circuit=circuit, i1=we2_clk.o, i2=we_branch.o2)
        d2_selector = Selector(circuit=circuit, b=[dlatch1.o],
                               s=je_branch.o[2], n=1)
        dlatch2 = DLatch(circuit=circuit, i1=d2_selector.o[0], i2=we2_we.o)
        o2_branch = Branch1n(circuit=circuit, i=[dlatch2.o],
                             o=[None, None, d1_selector.a[0]], n=3)
        o2_not = NOT(circuit=circuit, i=o2_branch.o[1], o=d1_selector.b[0])
        self.clk = clk_branch.i[0]
        self.i = d2_selector.a[0]
        self.o = o2_branch.o[0]
        self.je = je_branch.i[0]
        self.we = we_branch.i
        connect_legs(self, locals(), ['clk', 'i', 'o', 'je', 'we'])


class BinaryCounter:
    def __init__(self, circuit, n, clk=None, i=None, o=None,
                 ce=None, je=None, co=None, reset=None):
        reset_branch = Branch1n(circuit=circuit, n=3)
        reset_je_or = OR(circuit=circuit, i2=reset_branch.o[1])
        je_branch = Branch1n(circuit=circuit, i=[reset_je_or.o], n=4+n)
        ce_or = OR(circuit=circuit, i2=je_branch.o[1])
        reset_clk_or = OR(circuit=circuit, i2=reset_branch.o[0])
        ce_transistor = Transistor(circuit=circuit, i=reset_clk_or.o,
                                   switch=ce_or.o)
        clk_inv = NOT(circuit=circuit, i=ce_transistor.o)
        clk_branch = Branch1n(circuit=circuit, i=[clk_inv.o], n=1+n)
        clk_sel = Selector(circuit=circuit,
                           a=clk_branch.o[1:],
                           b=[clk_branch.o[0]] + [None] * (n - 1),
                           s=je_branch.o[2], n=n)
        reset_not = NOT(circuit=circuit, i=reset_branch.o[2])
        reset_i_mswitch = MultiSwitch(circuit=circuit, switch=reset_not.o, n=n)
        div_we_xor = XOR(circuit=circuit, i1=je_branch.o[0], i2=je_branch.o[-1])
        div_we_not = NOT(circuit=circuit, i=div_we_xor.o)
        div_we_branch = Branch1n(circuit=circuit, i=[div_we_not.o], n=n)
        divs = [ClockDivider(circuit=circuit,
                             clk=clk_sel.o[j],
                             i=reset_i_mswitch.o[j],
                             je=je_branch.o[3+j],
                             we=div_we_branch.o[j])
                for j in range(n)]
        o_branches = [Branch12(circuit=circuit, i=divs[j].o,
                               o1=clk_sel.b[j+1] if j+1 < n else None)
                      for j in range(n)]
        o_bulbs = MultiBulbs(circuit=circuit,
                             i=[o_branches[j].o2 for j in range(n)], n=n)
        self.bulbs = o_bulbs.bulbs
        co_mswitch = MultiSwitch(circuit=circuit, i=o_bulbs.o, n=n)
        self.clk = reset_clk_or.i1
        self.i = reset_i_mswitch.i
        self.o = co_mswitch.o
        self.ce = ce_or.i1
        self.je = reset_je_or.i1
        self.co = co_mswitch.switch
        self.reset = reset_branch.i[0]
        connect_legs(self, locals(),
                     ['clk', 'i', 'o', 'ce', 'je', 'co', 'reset'])


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
        self.switches = []
        self.clocks = []
        self.sram_programmers = []
        self.update_stack = []

    def initialize(self):
        # initialize circuit
        self.update_loop([(p, 'r', None, None) for p in self.plusses[::-1]])
        # program SRAMs if requested
        for sp in self.sram_programmers:
            if sp.content is None:
                continue
            seq = [sp.pm_key]
            for a, v in sp.content.items():
                a = [int(bit_str) for bit_str in a]
                v = [int(bit_str) for bit_str in v]
                a_seq = sum([[sp.a_keys[j]] * a[j] for j in range(len(a))], [])
                v_seq = sum([[sp.d_keys[j]] * v[j] for j in range(len(v))], [])
                seq += a_seq + v_seq + [sp.re_key] * 2 + a_seq + v_seq
            seq += [sp.pm_key]
            for key in seq:
                self.update(key)

    def add_plus(self):
        plus = Plus(circuit=self)
        self.plusses.append(plus)
        return plus

    def add_minus(self):
        return Minus(circuit=self)

    def update(self, key):
        if key == '':
            return sum(c.update(key) for c in self.clocks) > 0
        else:
            return sum(c.update(key) for c in self.switches + self.clocks) > 0

    def update_loop(self, updates=[]):
        assert len(self.update_stack) == 0
        self.update_stack.extend(updates)
        while len(self.update_stack) > 0:
            component, mode, sender, value = self.update_stack.pop()
            if component is None:
                continue
            assert mode == 'r' or mode == 'l'
            self.update_stack.extend(
                component.update_right(sender, value) if mode == 'r' else
                component.update_left(sender, value)
            )

