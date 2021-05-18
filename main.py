import graphics
from components import (
    Branch12, Branch21, Plus, Minus, Switch, Bulb, Transistor,
    NOT, AND, OR, Branch1n, MultiSwitch, DLatch, Register, Clock, Bus,
    Circuit
)
from display import Display, green, blue, yellow


if __name__ == '__main__':
    # # basic demo
    # circuit = Circuit()
    # plus = Plus(circuit=circuit)
    # minus = Minus(circuit=circuit)
    # jungiklis = Switch(circuit=circuit, i=plus.o, key='a')
    # lempute = Bulb(circuit=circuit, i=jungiklis.o, o=minus.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box([jungiklis, lempute], ['I', 'O'], [green, green], 'Basic')

    # # NOT demo
    # circuit = Circuit()
    # plus = Plus(circuit=circuit)
    # minus = Minus(circuit=circuit)
    # jungiklis = Switch(circuit=circuit, i=plus.o, key='a')
    # lempute = Bulb(circuit=circuit, o=minus.i)
    # not_gate = NOT(circuit=circuit, i=jungiklis.o)
    # not_gate2 = NOT(circuit=circuit, i=not_gate.o)
    # not_gate3 = NOT(circuit=circuit, i=not_gate2.o)
    # not_gate4 = NOT(circuit=circuit, i=not_gate3.o)
    # not_gate5 = NOT(circuit=circuit, i=not_gate4.o, o=lempute.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box([jungiklis, lempute], ['I', 'O'], [green, green], 'NOT')

    # # AND demo
    # circuit = Circuit()
    # plus1 = Plus(circuit=circuit)
    # plus2 = Plus(circuit=circuit)
    # minus = Minus(circuit=circuit)
    # jungiklis1 = Switch(circuit=circuit, i=plus1.o, key='a')
    # jungiklis2 = Switch(circuit=circuit, i=plus2.o, key='s')
    # and_gate = AND(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
    # lempute = Bulb(circuit=circuit, i=and_gate.o, o=minus.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box([jungiklis1, jungiklis2, lempute], ['I1', 'I2', 'O'],
    #                  [green, green, green], 'AND')

    # # OR demo
    # circuit = Circuit()
    # plus1 = Plus(circuit=circuit)
    # plus2 = Plus(circuit=circuit)
    # minus = Minus(circuit=circuit)
    # jungiklis1 = Switch(circuit=circuit, i=plus1.o, key='a')
    # jungiklis2 = Switch(circuit=circuit, i=plus2.o, key='s')
    # or_gate = OR(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
    # lempute = Bulb(circuit=circuit, i=or_gate.o, o=minus.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box([jungiklis1, jungiklis2, lempute], ['I1', 'I2', 'O'],
    #                  [green, green, green], 'OR')

    # # XOR demo
    # circuit = Circuit()
    # plus1 = Plus(circuit=circuit)
    # plus2 = Plus(circuit=circuit)
    # minus = Minus(circuit=circuit)
    # jungiklis1 = Switch(circuit=circuit, i=plus1.o, key='a')
    # jungiklis2 = Switch(circuit=circuit, i=plus2.o, key='s')
    # branch121 = Branch12(circuit=circuit, i=jungiklis1.o)
    # branch122 = Branch12(circuit=circuit, i=jungiklis2.o)
    # and_gate = AND(circuit=circuit, i1=branch121.o1, i2=branch122.o1)
    # not_gate = NOT(circuit=circuit, i=and_gate.o)
    # or_gate = OR(circuit=circuit, i1=branch121.o2, i2=branch122.o2)
    # and_gate2 = AND(circuit=circuit, i1=not_gate.o, i2=or_gate.o)
    # lempute = Bulb(circuit=circuit, i=and_gate2.o, o=minus.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box([jungiklis1, jungiklis2, lempute], ['I1', 'I2', 'O'],
    #                  [green, green, green], 'XOR')

    # # OR loop demo
    # circuit = Circuit()
    # plus = Plus(circuit=circuit)
    # minus = Minus(circuit=circuit)
    # jungiklis = Switch(circuit=circuit, i=plus.o, key='a')
    # or_gate = OR(circuit=circuit, i1=jungiklis.o)
    # branch12 = Branch12(circuit=circuit, i=or_gate.o, o2=or_gate.i2)
    # lempute = Bulb(circuit=circuit, i=branch12.o1, o=minus.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box([jungiklis, lempute], ['I', 'O'],
    #                  [green, green], 'OR loop')

    # # SR latch demo
    # circuit = Circuit()
    # plus1 = Plus(circuit=circuit)
    # plus2 = Plus(circuit=circuit)
    # minus = Minus(circuit=circuit)
    # jungiklis1 = Switch(circuit=circuit, i=plus1.o, key='a')
    # jungiklis2 = Switch(circuit=circuit, i=plus2.o, key='s')
    # or_gate = OR(circuit=circuit, i2=jungiklis1.o)
    # not_gate = NOT(circuit=circuit, i=jungiklis2.o)
    # and_gate = AND(circuit=circuit, i1=or_gate.o, i2=not_gate.o)
    # branch12 = Branch12(circuit=circuit, i=and_gate.o, o2=or_gate.i1)
    # lempute = Bulb(circuit=circuit, i=branch12.o1, o=minus.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box([jungiklis1, jungiklis2, lempute], ['S', 'R', 'O'],
    #                  [green, green, green], 'SR latch')

    # # D latch demo
    # circuit = Circuit()
    # plus1 = Plus(circuit=circuit)
    # plus2 = Plus(circuit=circuit)
    # minus = Minus(circuit=circuit)
    # jungiklis1 = Switch(circuit=circuit, i=plus1.o, key='a')
    # jungiklis2 = Switch(circuit=circuit, i=plus2.o, key='s')
    # dlatch = DLatch(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
    # lempute = Bulb(circuit=circuit, i=dlatch.o, o=minus.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box([jungiklis1, jungiklis2, lempute], ['D', 'WE', 'O'],
    #                  [green, green, green], 'D latch')

    # # clock demo
    # circuit = Circuit()
    # minus = Minus(circuit=circuit)
    # clock = Clock(circuit=circuit)
    # lempute = Bulb(circuit=circuit, i=clock.o1, o=minus.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box([lempute], ['CLK'], [blue], 'Clock')

    # 8-bit registers demo
    n = 8
    keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k']

    circuit = Circuit()
    clock = Clock(circuit=circuit)
    clock_branch = Branch12(circuit=circuit, i=clock.o2)
    bus = Bus(circuit=circuit, n=n)
    bus_write_manual = bus.add_write()

    manual_plus = Plus(circuit=circuit)
    manual_enable = Switch(circuit=circuit, i=manual_plus.o, key='e')
    manual_branch = Branch1n(circuit=circuit, i=[manual_enable.o], n=n)
    manual_switches = [Switch(circuit=circuit,
                              i=manual_branch.o[j],
                              o=bus_write_manual[j],
                              key=keys[j])
                       for j in range(n)]

    regA_re_plus = Plus(circuit=circuit)
    regA_re_switch = Switch(circuit=circuit, i=regA_re_plus.o, key='r')
    regA_re_and = AND(circuit=circuit, i1=clock_branch.o1, i2=regA_re_switch.o)
    regA = Register(circuit=circuit, we=regA_re_and.o, i=bus.add_read(), n=n)
    regA_out_branches = [Branch12(circuit=circuit, i=regA.o[j])
                         for j in range(n)]
    regA_bulbs = [Bulb(circuit=circuit, i=regA_out_branches[j].o1)
                  for j in range(n)]
    regA_minuses = [Minus(circuit=circuit, i=regA_bulbs[j].o) for j in range(n)]
    regA_we_plus = Plus(circuit=circuit)
    regA_we_switch = Switch(circuit=circuit, i=regA_we_plus.o, key='w')
    regA_we_mswitch = MultiSwitch(
        circuit=circuit, switch=regA_we_switch.o,
        i=[regA_out_branches[j].o2 for j in range(n)], o=bus.add_write(), n=n
    )

    regB_re_plus = Plus(circuit=circuit)
    regB_re_switch = Switch(circuit=circuit, i=regB_re_plus.o, key='y')
    regB_re_and = AND(circuit=circuit, i1=clock_branch.o2, i2=regB_re_switch.o)
    regB = Register(circuit=circuit, we=regB_re_and.o, i=bus.add_read(), n=n)
    regB_out_branches = [Branch12(circuit=circuit, i=regB.o[j])
                         for j in range(n)]
    regB_bulbs = [Bulb(circuit=circuit, i=regB_out_branches[j].o1)
                  for j in range(n)]
    regB_minuses = [Minus(circuit=circuit, i=regB_bulbs[j].o) for j in range(n)]
    regB_we_plus = Plus(circuit=circuit)
    regB_we_switch = Switch(circuit=circuit, i=regB_we_plus.o, key='t')
    regB_we_mswitch = MultiSwitch(
        circuit=circuit, switch=regB_we_switch.o,
        i=[regB_out_branches[j].o2 for j in range(n)], o=bus.add_write(), n=n
    )

    circuit.initialize()
    display = Display()
    display.draw_box(
        components=[manual_enable] + manual_switches,
        labels=['WE'] + [f'I{j+1}' for j in range(n)],
        colors=[yellow] + [green for _ in range(n)],
        title='Manual inputs', yoffset=-180, sep_after=[1]
    )
    display.draw_box(
        components=bus.bulbs, labels=[f'B{j+1}' for j in range(n)],
        colors=[green for _ in range(n)], title='Bus', yoffset=-60
    )
    display.draw_box(
        components=[clock.switch, regA_re_switch, regA_we_switch] + regA_bulbs,
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(n)],
        colors=[blue, yellow, yellow] + [green for _ in range(n)],
        title='Register A', yoffset=60, sep_after=[3]
    )
    display.draw_box(
        components=[clock.switch, regB_re_switch, regB_we_switch] + regB_bulbs,
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(n)],
        colors=[blue, yellow, yellow] + [green for _ in range(n)],
        title='Register B', yoffset=180, sep_after=[3]
    )

    while True:
        key = display.win.checkKey()
        if key == 'q':
            break
        if circuit.update(key):
            display.update()

    display.win.close()

