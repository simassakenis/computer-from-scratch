import math
from components import (
    Branch12, Branch21, Plus, Minus, Switch, Bulb, Transistor,
    NOT, AND, OR, XOR, Branch1n, MultiSwitch, MultiBulbs, ManualSwitches,
    SRLatch, DLatch, Register, Decoder, Selector, SRAM, SRAMProgrammer,
    FullAdder, nBitAdder, ALU, Clock, ClockDivider, BinaryCounter, Bus
)
from display import red, green, blue, yellow, teal, indigo


def bulb_demo(circuit, display):
    switch = Switch(circuit=circuit, i=circuit.add_plus(), key='a')
    bulb = Bulb(circuit=circuit, i=switch.o, o=circuit.add_minus())
    display.draw_box(components=[switch, bulb], labels=['I', 'O'],
                     colors=[green, green], title='Bulb')


def not_demo(circuit, display):
    switch = Switch(circuit=circuit, i=circuit.add_plus(), key='a')
    not_gate = NOT(circuit=circuit, i=switch.o)
    bulb = Bulb(circuit=circuit, i=not_gate.o, o=circuit.add_minus())
    display.draw_box(components=[switch, bulb], labels=['I', 'O'],
                     colors=[green, green], title='NOT')


def and_demo(circuit, display):
    switch1 = Switch(circuit=circuit, i=circuit.add_plus(), key='a')
    switch2 = Switch(circuit=circuit, i=circuit.add_plus(), key='s')
    and_gate = AND(circuit=circuit, i1=switch1.o, i2=switch2.o)
    bulb = Bulb(circuit=circuit, i=and_gate.o, o=circuit.add_minus())
    display.draw_box(components=[switch1, switch2, bulb],
                     labels=['I1', 'I2', 'O'], colors=[green, green, green],
                     title='AND')


def or_demo(circuit, display):
    switch1 = Switch(circuit=circuit, i=circuit.add_plus(), key='a')
    switch2 = Switch(circuit=circuit, i=circuit.add_plus(), key='s')
    or_gate = OR(circuit=circuit, i1=switch1.o, i2=switch2.o)
    bulb = Bulb(circuit=circuit, i=or_gate.o, o=circuit.add_minus())
    display.draw_box(components=[switch1, switch2, bulb],
                     labels=['I1', 'I2', 'O'], colors=[green, green, green],
                     title='OR')


def xor_demo(circuit, display):
    switch1 = Switch(circuit=circuit, i=circuit.add_plus(), key='a')
    switch2 = Switch(circuit=circuit, i=circuit.add_plus(), key='s')
    xor_gate = XOR(circuit=circuit, i1=switch1.o, i2=switch2.o)
    bulb = Bulb(circuit=circuit, i=xor_gate.o, o=circuit.add_minus())
    display.draw_box(components=[switch1, switch2, bulb],
                     labels=['I1', 'I2', 'O'], colors=[green, green, green],
                     title='XOR')


def sr_latch_demo(circuit, display):
    switch1 = Switch(circuit=circuit, i=circuit.add_plus(), key='a')
    switch2 = Switch(circuit=circuit, i=circuit.add_plus(), key='s')
    sr_latch = SRLatch(circuit=circuit, s=switch1.o, r=switch2.o)
    bulb = Bulb(circuit=circuit, i=sr_latch.o, o=circuit.add_minus())
    display.draw_box(components=[switch1, switch2, bulb],
                     labels=['S', 'R', 'O'], colors=[green, green, green],
                     title='SR latch')


def d_latch_demo(circuit, display):
    switch1 = Switch(circuit=circuit, i=circuit.add_plus(), key='a')
    switch2 = Switch(circuit=circuit, i=circuit.add_plus(), key='s')
    d_latch = DLatch(circuit=circuit, i1=switch1.o, i2=switch2.o)
    bulb = Bulb(circuit=circuit, i=d_latch.o, o=circuit.add_minus())
    display.draw_box(components=[switch1, switch2, bulb],
                     labels=['D', 'WE', 'O'], colors=[green, green, green],
                     title='D latch')


def clock_demo(circuit, display):
    clock = Clock(circuit=circuit)
    bulb = Bulb(circuit=circuit, i=clock.o1, o=circuit.add_minus())
    display.draw_box(components=[bulb], labels=['CLK'], colors=[blue],
                     title='Clock')


def register_demo(circuit, display, nbits=8):
    assert nbits <= 8 # would need to add more keys to work with nbits > 8
    manual_keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'][:nbits]

    clock = Clock(circuit=circuit)
    clock_branch = Branch12(circuit=circuit, i=clock.o2)
    bus = Bus(circuit=circuit, n=nbits)

    manual_switches = ManualSwitches(circuit=circuit, o=bus.add_write(),
                                     keys=manual_keys, we_key='e', n=nbits)

    regA_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='r')
    regA = Register(circuit=circuit, i=bus.add_read(), re=regA_re_switch.o,
                    clk=clock_branch.o1, n=nbits)
    regA_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='w')
    regA_we = MultiSwitch(circuit=circuit, switch=regA_we_switch.o,
                          i=regA.o, o=bus.add_write(), n=nbits)

    regB_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='y')
    regB = Register(circuit=circuit, i=bus.add_read(), re=regB_re_switch.o,
                    clk=clock_branch.o2, n=nbits)
    regB_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='t')
    regB_we = MultiSwitch(circuit=circuit, switch=regB_we_switch.o,
                          i=regB.o, o=bus.add_write(), n=nbits)

    display.draw_box(
        components=[manual_switches.we_switch] + manual_switches.switches,
        labels=['WE'] + [f'I{j+1}' for j in range(nbits)],
        colors=[yellow] + [green] * nbits, title='Manual inputs',
        yoffset=-180, sep_after=[1]
    )
    display.draw_box(
        components=bus.bulbs, labels=[f'B{j+1}' for j in range(nbits)],
        colors=[green] * nbits, title='Bus', yoffset=-60
    )
    display.draw_box(
        components=[clock.bulb, regA_re_switch, regA_we_switch] + regA.bulbs,
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(nbits)],
        colors=[blue, yellow, yellow] + [green] * nbits,
        title='Register A', yoffset=60, sep_after=[3]
    )
    display.draw_box(
        components=[clock.bulb, regB_re_switch, regB_we_switch] + regB.bulbs,
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(nbits)],
        colors=[blue, yellow, yellow] + [green] * nbits,
        title='Register B', yoffset=180, sep_after=[3]
    )


def alu_demo(circuit, display, nbits=8):
    assert nbits <= 8 # would need to add more keys to work with nbits > 8
    manual_keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'][::-1][:nbits]

    clock = Clock(circuit=circuit)
    clock_branch = Branch1n(circuit=circuit, i=[clock.o2], n=3)
    bus = Bus(circuit=circuit, n=nbits)

    manual_switches = ManualSwitches(circuit=circuit, o=bus.add_write(),
                                     keys=manual_keys, we_key='e', n=nbits)

    regA_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='r')
    regA = Register(circuit=circuit, i=bus.add_read(), re=regA_re_switch.o,
                    clk=clock_branch.o[0], n=nbits)
    regA_branches = [Branch12(circuit=circuit, i=regA.o[j])
                     for j in range(nbits)]
    regA_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='w')
    regA_we = MultiSwitch(circuit=circuit, switch=regA_we_switch.o,
                          i=[regA_branches[j].o1 for j in range(nbits)],
                          o=bus.add_write(), n=nbits)

    regB_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='y')
    regB = Register(circuit=circuit, i=bus.add_read(), re=regB_re_switch.o,
                    clk=clock_branch.o[1], n=nbits)
    regB_branches = [Branch12(circuit=circuit, i=regB.o[j])
                     for j in range(nbits)]
    regB_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='t')
    regB_we = MultiSwitch(circuit=circuit, switch=regB_we_switch.o,
                          i=[regB_branches[j].o1 for j in range(nbits)],
                          o=bus.add_write(), n=nbits)

    regC_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='i')
    regC = Register(circuit=circuit, i=bus.add_read(), re=regC_re_switch.o,
                    clk=clock_branch.o[2], n=nbits)
    regC_branches = [Branch12(circuit=circuit, i=regC.o[j])
                     for j in range(nbits)]
    regC_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='u')
    regC_we = MultiSwitch(circuit=circuit, switch=regC_we_switch.o,
                          i=[regC_branches[j].o1 for j in range(nbits)],
                          o=bus.add_write(), n=nbits)

    alu_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='o')
    alu_su_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='p')
    alu = ALU(circuit=circuit,
              a=[regA_branches[j].o2 for j in range(nbits)],
              b=[regB_branches[j].o2 for j in range(nbits)],
              s=bus.add_write(),
              we=alu_we_switch.o,
              su=alu_su_switch.o,
              n=nbits)

    display.draw_box(
        components=[manual_switches.we_switch] + manual_switches.switches[::-1],
        labels=['WE'] + [f'I{j+1}' for j in range(nbits)][::-1],
        colors=[yellow] + [green] * nbits, title='Manual inputs',
        yoffset=-300, sep_after=[1]
    )
    display.draw_box(
        components=bus.bulbs[::-1],
        labels=[f'B{j+1}' for j in range(nbits)][::-1],
        colors=[green] * nbits, title='Bus', yoffset=-180
    )
    display.draw_box(
        components=([clock.bulb, regA_re_switch, regA_we_switch]
                    + regA.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(nbits)][::-1],
        colors=[blue, yellow, yellow] + [green] * nbits,
        title='Register A', yoffset=-60, sep_after=[3]
    )
    display.draw_box(
        components=([clock.bulb, regB_re_switch, regB_we_switch]
                    + regB.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(nbits)],
        colors=[blue, yellow, yellow] + [green] * nbits,
        title='Register B', yoffset=60, sep_after=[3]
    )
    display.draw_box(
        components=([clock.bulb, regC_re_switch, regC_we_switch]
                    + regC.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(nbits)],
        colors=[blue, yellow, yellow] + [green] * nbits,
        title='Register C', yoffset=180, sep_after=[3]
    )
    display.draw_box(
        components=[alu_we_switch, alu_su_switch] + alu.bulbs[::-1],
        labels=['WE', 'SU'] + [f'S{j+1}' for j in range(nbits)][::-1],
        colors=[yellow, yellow] + [green] * nbits,
        title='ALU', yoffset=300, sep_after=[2]
    )


def decoder_demo(circuit, display, nbits=4):
    assert nbits <= 8 # would need to add more keys to work with nbits > 8
    manual_keys = ['e', 'r', 't', 'y', 'u', 'i', 'o', 'p'][::-1][:nbits]
    ndec = 2 ** nbits

    manual_switches = ManualSwitches(circuit=circuit, keys=manual_keys,
                                     we_key='e', n=nbits)
    decoder = Decoder(circuit=circuit, i=manual_switches.o, n=ndec)
    mbulbs = MultiBulbs(circuit=circuit, i=decoder.o, n=ndec)

    display.draw_box(
        components=[manual_switches.we_switch] + manual_switches.switches[::-1],
        labels=['WE'] + [f'I{j+1}' for j in range(nbits)][::-1],
        colors=[yellow] + [green] * nbits, title='Manual inputs',
        yoffset=-60, sep_after=[1]
    )
    display.draw_box(
        components=mbulbs.bulbs, labels=[f'D{j}' for j in range(ndec)],
        colors=[green] * ndec, title='Decoder', yoffset=60
    )


def sram_demo(circuit, display, nbytes=16):
    m = int(math.log2(nbytes))
    assert m <= 8 # would need to add more keys to work with nbits > 8
    manual_keys = ['e', 'r', 't', 'y', 'u', 'i', 'o', 'p'][::-1][:m]

    clock = Clock(circuit=circuit)
    clock_branch = Branch1n(circuit=circuit, i=[clock.o2], n=2)
    bus = Bus(circuit=circuit, n=8)

    manualB_switches = ManualSwitches(
        circuit=circuit, o=bus.add_write(),
        keys=['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'][::-1],
        we_key='b', n=8
    )

    regM_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='n')
    regM = Register(circuit=circuit, i=bus.add_read(), re=regM_re_switch.o,
                    clk=clock_branch.o[0], n=m)
    regM_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='m')
    regM_we = MultiSwitch(circuit=circuit, switch=regM_we_switch.o,
                          i=regM.o, o=bus.add_write(), n=m)

    manualA_switches = ManualSwitches(
        circuit=circuit, keys=manual_keys,
        we_key='v', n=m
    )
    manualD_switches = ManualSwitches(
        circuit=circuit, keys=['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'][::-1],
        we_key='v', n=8
    )

    pm_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='v')
    pm_branch = Branch1n(circuit=circuit, i=[pm_switch.o], n=2)
    a_selector = Selector(circuit=circuit,
                          a=manualA_switches.o,
                          b=regM_we.o,
                          s=pm_branch.o[0],
                          n=m)
    d_selector = Selector(circuit=circuit,
                          a=manualD_switches.o,
                          b=bus.add_read(),
                          s=pm_branch.o[1],
                          n=m)

    sram_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='r')
    sram_re_and = AND(circuit=circuit, i1=clock_branch.o[1],
                      i2=sram_re_switch.o)
    sram_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='w')
    sram = SRAM(circuit=circuit,
                a=a_selector.o,
                i=d_selector.o,
                re=sram_re_and.o,
                we=sram_we_switch.o,
                o=bus.add_write(),
                nbytes=nbytes)

    display.draw_box(
        components=([manualB_switches.we_switch]
                    + manualB_switches.switches[::-1]),
        labels=['WE'] + [f'I{j+1}' for j in range(8)][::-1],
        colors=[yellow] + [green] * 8, title='Manual bus inputs',
        yoffset=-300, sep_after=[1]
    )
    display.draw_box(
        components=bus.bulbs[::-1], labels=[f'B{j+1}' for j in range(8)][::-1],
        colors=[green] * 8, title='Bus', yoffset=-180
    )
    display.draw_box(
        components=([clock.bulb, regM_re_switch, regM_we_switch]
                    + regM.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(m)][::-1],
        colors=[blue, yellow, yellow] + [green] * m,
        title='Address register', yoffset=-60, sep_after=[3]
    )
    display.draw_box(
        components=([manualD_switches.we_switch]
                    + manualD_switches.switches[::-1]),
        labels=['WE'] + [f'I{j+1}' for j in range(8)][::-1],
        colors=[red] + [green] * 8, title='Manual data inputs',
        yoffset=60, sep_after=[1]
    )
    display.draw_box(
        components=([manualA_switches.we_switch]
                    + manualA_switches.switches[::-1]),
        labels=['WE'] + [f'I{j+1}' for j in range(m)][::-1],
        colors=[red] + [green] * m, title='Manual address inputs',
        yoffset=180, sep_after=[1]
    )
    display.draw_box(
        components=([sram_re_switch, sram_we_switch, pm_switch]
                    + sram.addr_bulbs[::-1]
                    + sram.bulbs[::-1]),
        labels=(['RE', 'WE', 'PM']
                + [f'A{j+1}' for j in range(m)][::-1]
                + [f'R{j+1}' for j in range(8)][::-1]),
        colors=[yellow, yellow, red] + [teal] * m + [green] * 8, title='SRAM',
        yoffset=300, sep_after=[2, 3, 3+m]
    )


def counter_demo(circuit, display, nbits=4):
    clock = Clock(circuit=circuit)
    bus = Bus(circuit=circuit, n=8)
    manualJ_switches = ManualSwitches(
        circuit=circuit, keys=['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'][::-1],
        o=bus.add_write(), we_key='e', n=8
    )
    ce_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='u')
    je_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='i')
    co_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='o')
    counter = BinaryCounter(circuit=circuit, clk=clock.o1,
                            i=bus.add_read(), o=bus.add_write(),
                            ce=ce_switch.o, je=je_switch.o,
                            co=co_switch.o, n=nbits)

    display.draw_box(
        components=([manualJ_switches.we_switch]
                    + manualJ_switches.switches[::-1]),
        labels=['WE'] + [f'I{j+1}' for j in range(8)][::-1],
        colors=[yellow] + [green] * 8,
        title='Manual jump inputs', yoffset=-180, sep_after=[1]
    )
    display.draw_box(
        components=bus.bulbs[::-1], labels=[f'B{j+1}' for j in range(8)][::-1],
        colors=[green] * 8, title='Bus', yoffset=-60
    )
    display.draw_box(
        components=([clock.bulb, ce_switch, je_switch, co_switch]
                    + counter.bulbs[::-1]),
        labels=(['CLK', 'CE', 'JE', 'CO']
                + [f'O{j+1}' for j in range(nbits)][::-1]),
        colors=[blue, yellow, yellow, yellow] + [green] * nbits,
        title='Binary counter', yoffset=60, sep_after=[1, 4]
    )


def manual_controls_demo(circuit, display):
    nbytes = 16 # fixed by the architecture (4-bit opcodes, 4-bit addresses)

    clock = Clock(circuit=circuit)
    clock_branch = Branch1n(circuit=circuit, i=[clock.o2], n=6)
    bus = Bus(circuit=circuit, n=8)

    regM_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='n')
    regM = Register(circuit=circuit, i=bus.add_read(), re=regM_re_switch.o,
                    clk=clock_branch.o[0], n=4)
    regM_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='m')
    regM_we = MultiSwitch(circuit=circuit, switch=regM_we_switch.o,
                          i=regM.o, o=bus.add_write(), n=4)

    sram_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='r')
    sram_re_and = AND(circuit=circuit, i1=clock_branch.o[1],
                      i2=sram_re_switch.o)
    sram_prog = SRAMProgrammer(
        circuit=circuit, nbytes=nbytes, pm_key='v', a_keys=['U', 'I', 'O', 'P'],
        d_keys = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K'], re_key='L',
        a=regM_we.o, i=bus.add_read(), re=sram_re_and.o
    )
    sram_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='w')
    sram = SRAM(circuit=circuit, a=sram_prog.ao, i=sram_prog.io,
                re=sram_prog.reo, we=sram_we_switch.o, o=bus.add_write(),
                nbytes=nbytes)

    regI_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='k')
    regI = Register(circuit=circuit, i=bus.add_read(), re=regI_re_switch.o,
                    clk=clock_branch.o[2], n=8)
    regI_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='l')
    regI_we = MultiSwitch(circuit=circuit, switch=regI_we_switch.o,
                          i=regI.o[:4], o=bus.add_write()[:4], n=4)

    ce_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='u')
    je_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='i')
    co_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='o')
    counter = BinaryCounter(circuit=circuit, clk=clock.o1,
                            i=bus.add_read(), o=bus.add_write(),
                            ce=ce_switch.o, je=je_switch.o, co=co_switch.o, n=4)

    regA_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='a')
    regA = Register(circuit=circuit, i=bus.add_read(), re=regA_re_switch.o,
                    clk=clock_branch.o[3], n=8)
    regA_branches = [Branch12(circuit=circuit, i=regA.o[j]) for j in range(8)]
    regA_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='s')
    regA_we = MultiSwitch(circuit=circuit, switch=regA_we_switch.o,
                          i=[regA_branches[j].o1 for j in range(8)],
                          o=bus.add_write(), n=8)

    regB_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='d')
    regB = Register(circuit=circuit, i=bus.add_read(), re=regB_re_switch.o,
                    clk=clock_branch.o[4], n=8)
    regB_branches = [Branch12(circuit=circuit, i=regB.o[j]) for j in range(8)]
    regB_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='f')
    regB_we = MultiSwitch(circuit=circuit, switch=regB_we_switch.o,
                          i=[regB_branches[j].o1 for j in range(8)],
                          o=bus.add_write(), n=8)

    regC_re_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='g')
    regC = Register(circuit=circuit, i=bus.add_read(), re=regC_re_switch.o,
                    clk=clock_branch.o[5], n=8)
    regC_branches = [Branch12(circuit=circuit, i=regC.o[j]) for j in range(8)]
    regC_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='h')
    regC_we = MultiSwitch(circuit=circuit, switch=regC_we_switch.o,
                          i=[regC_branches[j].o1 for j in range(8)],
                          o=bus.add_write(), n=8)

    alu_we_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='j')
    alu_su_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='p')
    alu = ALU(circuit=circuit,
              a=[regA_branches[j].o2 for j in range(8)],
              b=[regB_branches[j].o2 for j in range(8)],
              s=bus.add_write(),
              we=alu_we_switch.o,
              su=alu_su_switch.o,
              n=8)

    display.draw_box(
        components=bus.bulbs[::-1], labels=[f'B{j+1}' for j in range(8)][::-1],
        colors=[green] * 8, title='Bus', xoffset=-400, yoffset=-300
    )
    display.draw_box(
        components=([clock.switch, regM_re_switch, regM_we_switch]
                    + regM.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(4)][::-1],
        colors=[blue, yellow, yellow] + [green] * 4,
        title='Memory address register', sep_after=[3],
        xoffset=-400, yoffset=-180
    )
    display.draw_box(
        components=([sram_prog.pm_switch, sram_prog.re_switch]
                    + sram_prog.a_switches.switches[::-1]
                    + sram_prog.d_switches.switches[::-1]),
        labels=(['PM', 'RE']
                + [f'A{j+1}' for j in range(4)][::-1]
                + [f'D{j+1}' for j in range(8)][::-1]),
        colors=[red, yellow] + [teal] * 4 + [green] * 8,
        title='SRAM programmer', sep_after=[1, 2, 6],
        xoffset=-400, yoffset=-60
    )
    display.draw_box(
        components=([sram_re_switch, sram_we_switch, sram_prog.pm_switch]
                    + sram.addr_bulbs[::-1]
                    + sram.bulbs[::-1]),
        labels=(['RE', 'WE', 'PM']
                + [f'A{j+1}' for j in range(4)][::-1]
                + [f'R{j+1}' for j in range(8)][::-1]),
        colors=[yellow, yellow, red] + [teal] * 4 + [green] * 8, title='SRAM',
        sep_after=[2, 3, 3+4], xoffset=-400, yoffset=60
    )
    display.draw_box(
        components=([clock.switch, regI_re_switch, regI_we_switch]
                    + regI.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
        colors=[blue, yellow, yellow] + [green] * 8,
        title='Instruction Register', sep_after=[3], xoffset=-400, yoffset=180
    )
    display.draw_box(
        components=([clock.switch, ce_switch, je_switch, co_switch]
                    + counter.bulbs[::-1]),
        labels=['CLK', 'CE', 'JE', 'CO'] + [f'O{j+1}' for j in range(4)][::-1],
        colors=[blue, yellow, yellow, yellow] + [green] * 4,
        title='Program counter', sep_after=[1, 4], xoffset=400, yoffset=-300
    )
    display.draw_box(
        components=([clock.switch, regA_re_switch, regA_we_switch]
                    + regA.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)][::-1],
        colors=[blue, yellow, yellow] + [green] * 8, title='Register A',
        sep_after=[3], xoffset=400, yoffset=-180
    )
    display.draw_box(
        components=[alu_we_switch, alu_su_switch] + alu.bulbs[::-1],
        labels=['WE', 'SU'] + [f'S{j+1}' for j in range(8)][::-1],
        colors=[yellow, yellow] + [green] * 8, title='ALU',
        sep_after=[2], xoffset=400, yoffset=-60
    )
    display.draw_box(
        components=([clock.switch, regB_re_switch, regB_we_switch]
                    + regB.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
        colors=[blue, yellow, yellow] + [green] * 8, title='Register B',
        sep_after=[3], xoffset=400, yoffset=60
    )
    display.draw_box(
        components=([clock.switch, regC_re_switch, regC_we_switch]
                    + regC.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
        colors=[blue, yellow, yellow] + [green] * 8, title='Register C',
        sep_after=[3], xoffset=400, yoffset=180
    )


def controller_demo(circuit, display, show_full=True):
    nbytes = 16 # fixed by the architecture (4-bit opcodes, 4-bit addresses)

    hlt_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    clock = Clock(circuit=circuit, hlt=hlt_switch.o)
    clock_branch = Branch1n(circuit=circuit, i=[clock.o2], n=8)
    clk_full_branch = Branch1n(circuit=circuit, i=[clock.o1], n=4)
    bus = Bus(circuit=circuit, n=8)

    reset_switch = Switch(circuit=circuit, i=circuit.add_plus(), key='Q')
    reset_branch = Branch1n(circuit=circuit, i=[reset_switch.o], n=9)

    regM_re_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    regM = Register(circuit=circuit, i=bus.add_read(), re=regM_re_switch.o,
                    clk=clock_branch.o[0], reset=reset_branch.o[0], n=4)

    sram_re_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    sram_re_and = AND(circuit=circuit, i1=clock_branch.o[1],
                      i2=sram_re_switch.o)
    sram_prog = SRAMProgrammer(
        circuit=circuit, nbytes=nbytes, pm_key='v', a_keys=['U', 'I', 'O', 'P'],
        d_keys = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K'], re_key='L',
        a=regM.o, i=bus.add_read(), re=sram_re_and.o
    )
    sram_we_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    sram = SRAM(circuit=circuit, a=sram_prog.ao, i=sram_prog.io,
                re=sram_prog.reo, we=sram_we_switch.o, o=bus.add_write(),
                nbytes=nbytes)

    regI_re_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    regI = Register(circuit=circuit, i=bus.add_read(), re=regI_re_switch.o,
                    clk=clock_branch.o[2], reset=reset_branch.o[1], n=8)
    regI_we_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    regI_we = MultiSwitch(circuit=circuit, switch=regI_we_switch.o,
                          i=regI.o[:4], o=bus.add_write()[:4], n=4)

    ce_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    je_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    co_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    prog_ctr = BinaryCounter(circuit=circuit, clk=clk_full_branch.o[1],
                             i=bus.add_read(), o=bus.add_write(),
                             ce=ce_switch.o, je=je_switch.o, co=co_switch.o,
                             reset=reset_branch.o[2], n=4)

    regA_re_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    regA = Register(circuit=circuit, i=bus.add_read(), re=regA_re_switch.o,
                    clk=clock_branch.o[3], reset=reset_branch.o[3], n=8)
    regA_branches = [Branch12(circuit=circuit, i=regA.o[j]) for j in range(8)]
    regA_we_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    regA_we = MultiSwitch(circuit=circuit, switch=regA_we_switch.o,
                          i=[regA_branches[j].o1 for j in range(8)],
                          o=bus.add_write(), n=8)

    regB_re_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    regB = Register(circuit=circuit, i=bus.add_read(), re=regB_re_switch.o,
                    clk=clock_branch.o[4], n=8)
    regB_branches = [Branch12(circuit=circuit, i=regB.o[j]) for j in range(8)]
    regB_we_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    regB_we = MultiSwitch(circuit=circuit, switch=regB_we_switch.o,
                          i=[regB_branches[j].o1 for j in range(8)],
                          o=bus.add_write(), n=8)


    regC_re_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    regC = Register(circuit=circuit, i=bus.add_read(), re=regC_re_switch.o,
                    clk=clock_branch.o[5], reset=reset_branch.o[5], n=8)
    regC_we_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    regC_we = MultiSwitch(circuit=circuit, switch=regC_we_switch.o,
                          i=regC.o, o=bus.add_write(), n=8)

    alu_we_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    alu_su_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    alu_fe_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    alu = ALU(circuit=circuit,
              a=[regA_branches[j].o2 for j in range(8)],
              b=regB.o,
              s=bus.add_write(),
              we=alu_we_switch.o,
              su=alu_su_switch.o,
              clk=clock_branch.o[6],
              fe=alu_fe_switch.o,
              freset=reset_branch.o[6],
              n=8)

    regII_re_nots = [NOT(circuit=circuit, i=clk_full_branch.o[j])
                      for j in [0, 3]]
    regII_re_and = AND(circuit=circuit, i1=regII_re_nots[0].o,
                        i2=regII_re_nots[1].o)
    regII = Register(circuit=circuit, i=regI.o[4:] + alu.fo, re=regII_re_and.o,
                     clk=circuit.add_plus(), n=6)

    regO_re_switch = Transistor(circuit=circuit, i=circuit.add_plus())
    regO = Register(circuit=circuit, i=bus.add_read(), re=regO_re_switch.o,
                    clk=clock_branch.o[7], reset=reset_branch.o[7], n=8)

    clk_not = NOT(circuit=circuit, i=clk_full_branch.o[2])
    step_ctr = BinaryCounter(circuit=circuit, n=3, clk=clk_not.o,
                             ce=circuit.add_plus(), co=circuit.add_plus(),
                             reset=reset_branch.o[8])

    controls = [
        hlt_switch.switch,
        regM_re_switch.switch,
        sram_re_switch.switch,
        sram_we_switch.switch,
        regI_re_switch.switch,
        regI_we_switch.switch,
        regA_re_switch.switch,
        regA_we_switch.switch,
        alu_we_switch.switch,
        alu_su_switch.switch,
        regB_re_switch.switch,
        regB_we_switch.switch,
        regC_re_switch.switch,
        regC_we_switch.switch,
        regO_re_switch.switch,
        alu_fe_switch.switch,
        ce_switch.switch,
        je_switch.switch,
        co_switch.switch
    ]
    ctrl_labels = ['HLT', 'MI', 'RI', 'RO', 'II', 'IO', 'AI', 'AO',
                   'SO', 'SU', 'BI', 'BO', 'CI', 'CO', 'OI', 'FE',
                   'PCE', 'PCI', 'PCO']
    nctrl_srams = (len(controls) // 8) + (len(controls) % 8 > 0)
    step_o_branches = [Branch1n(circuit=circuit, i=[step_ctr.o[j]], n=nctrl_srams)
                       for j in range(3)]
    regI_o_branches = [Branch1n(circuit=circuit, i=[regII.o[j]], n=nctrl_srams)
                       for j in range(6)]
    ctrl_progs = [None] * nctrl_srams
    ctrl_srams = [None] * nctrl_srams
    for i in range(nctrl_srams):
        ctrl_progs[i] = SRAMProgrammer(
            circuit=circuit, nbytes=512, pm_key=f'c{i}',
            a_keys=['W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            d_keys = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K'], re_key='L',
            a=([step_o_branches[j].o[i] for j in range(3)]
               + [regI_o_branches[j].o[i] for j in range(6)]),
            i=[None] * 8,
            re=None,
            content={}
        )
        ctrl_srams[i] = SRAM(
            circuit=circuit, a=ctrl_progs[i].ao, i=ctrl_progs[i].io,
            o=(controls[8*i:8*(i+1)] + [None] * 8)[:8][::-1],
            re=ctrl_progs[i].reo, we=circuit.add_plus(), nbytes=512
        )

    instruction_set = {
        'NOP': ('0000', 'PCO MI, RO II PCE'),
        'LDA': ('0001', 'PCO MI, RO II PCE, IO MI, RO AI'),
        'ADD': ('0010', 'PCO MI, RO II PCE, IO MI, RO BI, SO CI FE, CO AI'),
        'SUB': ('0011', 'PCO MI, RO II PCE, IO MI, RO BI, SO CI SU FE, CO AI'),
        'STA': ('0100', 'PCO MI, RO II PCE, IO MI, AO RI'),
        'LDI': ('0101', 'PCO MI, RO II PCE, IO AI'),
        'JMP': ('0110', 'PCO MI, RO II PCE, IO PCI'),
        'JC' : ('0111', 'PCO MI, RO II PCE, IO PCI'), # if CF is set, else NOP
        'JZ' : ('1000', 'PCO MI, RO II PCE, IO PCI'), # if ZF is set, else NOP
        'OUT': ('1110', 'PCO MI, RO II PCE, AO OI'),
        'HLT': ('1111', 'PCO MI, RO II PCE, HLT'),
    }

    binstr = lambda x, w: bin(x)[2:].zfill(w)
    for instr, (opcode, mucode) in instruction_set.items():
        for cf in ['1', '0']:
            for zf in ['0', '1']:
                store_nop = ((instr == 'JC' and cf != '1')
                             or (instr == 'JZ' and zf != '1'))
                for i, muinstr in enumerate(mucode.split(', ')):
                    if store_nop and i >= 2:
                        continue
                    addr = binstr(int(zf + cf + opcode + '000', 2) + i, 9)
                    active_idxs = [ctrl_labels.index(lab)
                                   for lab in muinstr.split(' ')]
                    val = ''.join(['1' if j in active_idxs else '0'
                                   for j in range(8*nctrl_srams)])
                    for k in range(nctrl_srams):
                        ctrl_progs[k].content[addr] = val[8*k:8*(k+1)]

    sram_prog.content = {
        '0000': '01011111', # LDI 15
        '0001': '01001111', # STA 15
        '0010': '01010000', # LDI 0
        '0011': '11100000', # OUT
        '0100': '00101111', # ADD 15
        '0101': '01110111', # JC 7
        '0110': '01100011', # JMP 3
        '0111': '00111111', # SUB 15
        '1000': '11100000', # OUT
        '1001': '10000011', # JZ 3
        '1010': '01100111', # JMP 7
        '1110': '11111110',
    }

    if show_full:
        display.draw_box(
            components=bus.bulbs[::-1],
            labels=[f'B{j+1}' for j in range(8)][::-1],
            colors=[green] * 8, title='Bus',
            xoffset=-400, yoffset=-300
        )
        display.draw_box(
            components=([clock.bulb, regM_re_switch]
                        + regM.bulbs[::-1]),
            labels=['CLK', 'RE'] + [f'D{j+1}' for j in range(4)][::-1],
            colors=[blue, yellow] + [green] * 4,
            title='Memory address register', sep_after=[2],
            xoffset=-400, yoffset=-180
        )
        display.draw_box(
            components=([sram_prog.pm_switch, sram_prog.re_switch]
                        + sram_prog.a_switches.switches[::-1]
                        + sram_prog.d_switches.switches[::-1]),
            labels=(['PM', 'RE']
                    + [f'A{j+1}' for j in range(4)][::-1]
                    + [f'D{j+1}' for j in range(8)][::-1]),
            colors=[red, yellow] + [teal] * 4 + [green] * 8,
            title='SRAM programmer', sep_after=[1, 2, 6],
            xoffset=-400, yoffset=-60
        )
        display.draw_box(
            components=([sram_re_switch, sram_we_switch, sram_prog.pm_switch]
                        + sram.addr_bulbs[::-1]
                        + sram.bulbs[::-1]),
            labels=(['RE', 'WE', 'PM']
                    + [f'A{j+1}' for j in range(4)][::-1]
                    + [f'R{j+1}' for j in range(8)][::-1]),
            colors=[yellow, yellow, red] + [teal] * 4 + [green] * 8,
            title='SRAM', sep_after=[2, 3, 7], xoffset=-400, yoffset=60
        )
        display.draw_box(
            components=([clock.bulb, regI_re_switch, regI_we_switch]
                        + regI.bulbs[::-1]),
            labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
            colors=[blue, yellow, yellow] + [green] * 8,
            title='Instruction Register', sep_after=[3],
            xoffset=-400, yoffset=180
        )
        display.draw_box(
            components=([clock.bulb, ce_switch, je_switch, co_switch]
                        + prog_ctr.bulbs[::-1]),
            labels=(['CLK', 'CE', 'JE', 'CO']
                    + [f'O{j+1}' for j in range(4)][::-1]),
            colors=[blue, yellow, yellow, yellow] + [green] * 4,
            title='Program counter', sep_after=[1, 4],
            xoffset=400, yoffset=-300
        )
        display.draw_box(
            components=([clock.bulb, regA_re_switch, regA_we_switch]
                        + regA.bulbs[::-1]),
            labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)][::-1],
            colors=[blue, yellow, yellow] + [green] * 8,
            title='Register A', sep_after=[3], xoffset=400, yoffset=-180
        )
        display.draw_box(
            components=([alu_we_switch, alu_su_switch]
                        + alu.bulbs[::-1]
                        + alu.fbulbs),
            labels=(['WE', 'SU']
                    + [f'S{j+1}' for j in range(8)][::-1]
                    + ['CF', 'ZF']),
            colors=[yellow, yellow] + [green] * 8 + [indigo] * 2,
            title='ALU', sep_after=[2, 10], xoffset=400, yoffset=-60
        )
        display.draw_box(
            components=([clock.bulb, regB_re_switch, regB_we_switch]
                        + regB.bulbs[::-1]),
            labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
            colors=[blue, yellow, yellow] + [green] * 8,
            title='Register B', sep_after=[3], xoffset=400, yoffset=60
        )
        display.draw_box(
            components=([clock.bulb, regC_re_switch, regC_we_switch]
                        + regC.bulbs[::-1]),
            labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
            colors=[blue, yellow, yellow] + [green] * 8,
            title='Register C', sep_after=[3], xoffset=400, yoffset=180
        )
        display.draw_box(
            components=regO.bulbs[::-1], title='Output',
            xoffset=600, yoffset=300, decimal=True
        )
        display.draw_box(
            components=([reset_switch]
                        + ctrl_srams[0].addr_bulbs[::-1]
                        + sum([ctrl_srams[i].bulbs[::-1]
                               for i in range(nctrl_srams)], [])[:len(controls)]),
            labels=(['RS']
                    + ['S1', 'S2', 'S3', 'I1', 'I2', 'I3', 'I4', 'CF', 'ZF'][::-1]
                    + ctrl_labels),
            colors=([red]
                    + [teal] * len(ctrl_srams[0].addr_bulbs)
                    + [yellow] * len(controls)),
            title='Controller', sep_after=[1, 10], xoffset=-120, yoffset=300
        )
    else:
        display.draw_box(components=regO.bulbs[::-1],
                         title='Output', decimal=True)

