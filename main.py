import graphics
from components import (
    Branch12, Branch21, Plus, Minus, Switch, Bulb, Transistor,
    NOT, AND, OR, XOR, Branch1n, MultiSwitch, MultiBulbs, ManualSwitches,
    SRLatch, DLatch, Register, Decoder, Selector, SRAM, SRAMProgrammer,
    FullAdder, nBitAdder, ALU,
    Clock, ClockDivider, BinaryCounter, Bus, Circuit
)
from display import Display, red, green, blue, yellow, teal, indigo

import sys
sys.setrecursionlimit(1500)


if __name__ == '__main__':
    # # basic demo
    # circuit = Circuit()
    # jungiklis = Switch(circuit=circuit, i=circuit.add_plus().o, key='a')
    # lempute = Bulb(circuit=circuit, i=jungiklis.o, o=circuit.add_minus().i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box(components=[jungiklis, lempute], labels=['I', 'O'],
    #                  colors=[green, green], title='Basic')

    # # NOT demo
    # circuit = Circuit()
    # jungiklis = Switch(circuit=circuit, i=circuit.add_plus().o, key='a')
    # lempute = Bulb(circuit=circuit, o=circuit.add_minus().i)
    # not_gate = NOT(circuit=circuit, i=jungiklis.o)
    # not_gate2 = NOT(circuit=circuit, i=not_gate.o)
    # not_gate3 = NOT(circuit=circuit, i=not_gate2.o)
    # not_gate4 = NOT(circuit=circuit, i=not_gate3.o)
    # not_gate5 = NOT(circuit=circuit, i=not_gate4.o, o=lempute.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box(components=[jungiklis, lempute], labels=['I', 'O'],
    #                  colors=[green, green], title='NOT')

    # # AND demo
    # circuit = Circuit()
    # jungiklis1 = Switch(circuit=circuit, i=circuit.add_plus().o, key='a')
    # jungiklis2 = Switch(circuit=circuit, i=circuit.add_plus().o, key='s')
    # and_gate = AND(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
    # lempute = Bulb(circuit=circuit, i=and_gate.o, o=circuit.add_minus().i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box(components=[jungiklis1, jungiklis2, lempute],
    #                  labels=['I1', 'I2', 'O'], colors=[green, green, green],
    #                  title='AND')

    # # OR demo
    # circuit = Circuit()
    # jungiklis1 = Switch(circuit=circuit, i=circuit.add_plus().o, key='a')
    # jungiklis2 = Switch(circuit=circuit, i=circuit.add_plus().o, key='s')
    # or_gate = OR(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
    # lempute = Bulb(circuit=circuit, i=or_gate.o, o=circuit.add_minus().i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box(components=[jungiklis1, jungiklis2, lempute],
    #                  labels=['I1', 'I2', 'O'], colors=[green, green, green],
    #                  title='OR')

    # # XOR demo
    # circuit = Circuit()
    # jungiklis1 = Switch(circuit=circuit, i=circuit.add_plus().o, key='a')
    # jungiklis2 = Switch(circuit=circuit, i=circuit.add_plus().o, key='s')
    # or_gate = XOR(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
    # lempute = Bulb(circuit=circuit, i=or_gate.o, o=circuit.add_minus().i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box(components=[jungiklis1, jungiklis2, lempute],
    #                  labels=['I1', 'I2', 'O'], colors=[green, green, green],
    #                  title='XOR')

    # # OR loop demo
    # circuit = Circuit()
    # jungiklis = Switch(circuit=circuit, i=circuit.add_plus().o, key='a')
    # or_gate = OR(circuit=circuit, i1=jungiklis.o)
    # branch12 = Branch12(circuit=circuit, i=or_gate.o, o2=or_gate.i2)
    # lempute = Bulb(circuit=circuit, i=branch12.o1, o=circuit.add_minus().i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box(components=[jungiklis, lempute], labels=['I', 'O'],
    #                  colors=[green, green], title='OR loop')

    # # SR latch demo
    # circuit = Circuit()
    # jungiklis1 = Switch(circuit=circuit, i=circuit.add_plus().o, key='a')
    # jungiklis2 = Switch(circuit=circuit, i=circuit.add_plus().o, key='s')
    # sr_latch = SRLatch(circuit=circuit, s=jungiklis1.o, r=jungiklis2.o)
    # lempute = Bulb(circuit=circuit, i=sr_latch.o, o=circuit.add_minus().i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box(components=[jungiklis1, jungiklis2, lempute],
    #                  labels=['S', 'R', 'O'], colors=[green, green, green],
    #                  title='SR latch')

    # # D latch demo
    # circuit = Circuit()
    # jungiklis1 = Switch(circuit=circuit, i=circuit.add_plus().o, key='a')
    # jungiklis2 = Switch(circuit=circuit, i=circuit.add_plus().o, key='s')
    # dlatch = DLatch(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
    # lempute = Bulb(circuit=circuit, i=dlatch.o, o=circuit.add_minus().i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box(components=[jungiklis1, jungiklis2, lempute],
    #                  labels=['D', 'WE', 'O'], colors=[green, green, green],
    #                  title='D latch')

    # # clock demo
    # circuit = Circuit()
    # minus = Minus(circuit=circuit)
    # clock = Clock(circuit=circuit)
    # lempute = Bulb(circuit=circuit, i=clock.o1, o=minus.i)
    # circuit.initialize()
    # display = Display()
    # display.draw_box(components=[lempute], labels=['CLK'], colors=[blue],
    #                  title='Clock')

    # # 8-bit registers demo
    # n = 8

    # circuit = Circuit()
    # clock = Clock(circuit=circuit)
    # clock_branch = Branch12(circuit=circuit, i=clock.o2)
    # bus = Bus(circuit=circuit, n=n)

    # manual_switches = ManualSwitches(
    #     circuit=circuit, o=bus.add_write(),
    #     keys=['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'], we_key='e', n=n
    # )

    # regA_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='r')
    # regA = Register(circuit=circuit, i=bus.add_read(), re=regA_re_switch.o,
    #                 clk=clock_branch.o1, n=n)
    # regA_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='w')
    # regA_we = MultiSwitch(circuit=circuit, switch=regA_we_switch.o,
    #                       i=regA.o, o=bus.add_write(), n=n)

    # regB_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='y')
    # regB = Register(circuit=circuit, i=bus.add_read(), re=regB_re_switch.o,
    #                 clk=clock_branch.o2, n=n)
    # regB_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='t')
    # regB_we = MultiSwitch(circuit=circuit, switch=regB_we_switch.o,
    #                       i=regB.o, o=bus.add_write(), n=n)

    # circuit.initialize()
    # display = Display()
    # display.draw_box(
    #     components=[manual_switches.we_switch] + manual_switches.switches,
    #     labels=['WE'] + [f'I{j+1}' for j in range(n)],
    #     colors=[yellow] + [green for _ in range(n)],
    #     title='Manual inputs', yoffset=-180, sep_after=[1]
    # )
    # display.draw_box(
    #     components=bus.bulbs, labels=[f'B{j+1}' for j in range(n)],
    #     colors=[green for _ in range(n)], title='Bus', yoffset=-60
    # )
    # display.draw_box(
    #     components=[clock.bulb, regA_re_switch, regA_we_switch] + regA.bulbs,
    #     labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(n)],
    #     colors=[blue, yellow, yellow] + [green for _ in range(n)],
    #     title='Register A', yoffset=60, sep_after=[3]
    # )
    # display.draw_box(
    #     components=[clock.bulb, regB_re_switch, regB_we_switch] + regB.bulbs,
    #     labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(n)],
    #     colors=[blue, yellow, yellow] + [green for _ in range(n)],
    #     title='Register B', yoffset=180, sep_after=[3]
    # )

    # # 8-bit adder demo
    # n = 8
    # circuit = Circuit()

    # manualA_switches = ManualSwitches(
    #     circuit=circuit, keys=['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'],
    #     we_key='e', n=n
    # )

    # manualB_switches = ManualSwitches(
    #     circuit=circuit, keys=['z', 'x', 'c', 'v', 'b', 'n', 'm', 'comma'],
    #     we_key='r', n=n
    # )

    # ci_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='t')
    # nbit_adder = nBitAdder(circuit=circuit,
    #                        a=manualA_switches.o,
    #                        b=manualB_switches.o,
    #                        ci=ci_switch.o, n=n)
    # sum_bulbs = [Bulb(circuit=circuit, i=nbit_adder.s[j]) for j in range(n)]
    # sum_minuses = [Minus(circuit=circuit, i=sum_bulbs[j].o) for j in range(n)]
    # co_bulb = Bulb(circuit=circuit, i=nbit_adder.co)
    # co_minus = Minus(circuit=circuit, i=co_bulb.o)

    # circuit.initialize()
    # display = Display()
    # display.draw_box(
    #     components=[manualA_switches.we_switch] + manualA_switches.switches,
    #     labels=['WE'] + [f'I{j+1}' for j in range(n)],
    #     colors=[yellow] + [green for _ in range(n)],
    #     title='Manual inputs A', yoffset=-180, sep_after=[1]
    # )
    # display.draw_box(
    #     components=[manualB_switches.we_switch] + manualB_switches.switches,
    #     labels=['WE'] + [f'I{j+1}' for j in range(n)],
    #     colors=[yellow] + [green for _ in range(n)],
    #     title='Manual inputs B', yoffset=-60, sep_after=[1]
    # )
    # display.draw_box(
    #     components=[ci_switch] + sum_bulbs + [co_bulb],
    #     labels=['CI'] + [f'S{j+1}' for j in range(n)] + ['CO'],
    #     colors=[green] * (n+2), title='8-bit adder',
    #     yoffset=60, sep_after=[1, 9]
    # )

    # # 8-bit ALU demo
    # n = 8

    # circuit = Circuit()
    # clock = Clock(circuit=circuit)
    # clock_branch = Branch1n(circuit=circuit, i=[clock.o2], n=3)
    # bus = Bus(circuit=circuit, n=n)

    # manual_switches = ManualSwitches(
    #     circuit=circuit, o=bus.add_write(),
    #     keys=['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'][::-1],
    #     we_key='e', n=n
    # )

    # regA_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='r')
    # regA = Register(circuit=circuit, i=bus.add_read(), re=regA_re_switch.o,
    #                 clk=clock_branch.o[0], n=n)
    # regA_branches = [Branch12(circuit=circuit, i=regA.o[j]) for j in range(n)]
    # regA_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='w')
    # regA_we = MultiSwitch(circuit=circuit, switch=regA_we_switch.o,
    #                       i=[regA_branches[j].o1 for j in range(n)],
    #                       o=bus.add_write(), n=n)

    # regB_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='y')
    # regB = Register(circuit=circuit, i=bus.add_read(), re=regB_re_switch.o,
    #                 clk=clock_branch.o[1], n=n)
    # regB_branches = [Branch12(circuit=circuit, i=regB.o[j]) for j in range(n)]
    # regB_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='t')
    # regB_we = MultiSwitch(circuit=circuit, switch=regB_we_switch.o,
    #                       i=[regB_branches[j].o1 for j in range(n)],
    #                       o=bus.add_write(), n=n)

    # regC_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='i')
    # regC = Register(circuit=circuit, i=bus.add_read(), re=regC_re_switch.o,
    #                 clk=clock_branch.o[2], n=n)
    # regC_branches = [Branch12(circuit=circuit, i=regC.o[j]) for j in range(n)]
    # regC_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='u')
    # regC_we = MultiSwitch(circuit=circuit, switch=regC_we_switch.o,
    #                       i=[regC_branches[j].o1 for j in range(n)],
    #                       o=bus.add_write(), n=n)

    # alu_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='o')
    # alu_su_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='p')
    # alu = ALU(circuit=circuit,
    #           a=[regA_branches[j].o2 for j in range(n)],
    #           b=[regB_branches[j].o2 for j in range(n)],
    #           s=bus.add_write(),
    #           we=alu_we_switch.o,
    #           su=alu_su_switch.o,
    #           n=n)

    # circuit.initialize()
    # display = Display()
    # display.draw_box(
    #     components=[manual_switches.we_switch] + manual_switches.switches[::-1],
    #     labels=['WE'] + [f'I{j+1}' for j in range(n)][::-1],
    #     colors=[yellow] + [green for _ in range(n)],
    #     title='Manual inputs', yoffset=-300, sep_after=[1]
    # )
    # display.draw_box(
    #     components=bus.bulbs[::-1], labels=[f'B{j+1}' for j in range(n)][::-1],
    #     colors=[green for _ in range(n)], title='Bus', yoffset=-180
    # )
    # display.draw_box(
    #     components=([clock.bulb, regA_re_switch, regA_we_switch]
    #                 + regA.bulbs[::-1]),
    #     labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(n)][::-1],
    #     colors=[blue, yellow, yellow] + [green for _ in range(n)],
    #     title='Register A', yoffset=-60, sep_after=[3]
    # )
    # display.draw_box(
    #     components=([clock.bulb, regB_re_switch, regB_we_switch]
    #                 + regB.bulbs[::-1]),
    #     labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(n)],
    #     colors=[blue, yellow, yellow] + [green for _ in range(n)],
    #     title='Register B', yoffset=60, sep_after=[3]
    # )
    # display.draw_box(
    #     components=([clock.bulb, regC_re_switch, regC_we_switch]
    #                 + regC.bulbs[::-1]),
    #     labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(n)],
    #     colors=[blue, yellow, yellow] + [green for _ in range(n)],
    #     title='Register C', yoffset=180, sep_after=[3]
    # )
    # display.draw_box(
    #     components=[alu_we_switch, alu_su_switch] + alu.bulbs[::-1],
    #     labels=['WE', 'SU'] + [f'S{j+1}' for j in range(n)][::-1],
    #     colors=[yellow, yellow] + [green for _ in range(n)],
    #     title='ALU', yoffset=300, sep_after=[2]
    # )

    # # Decoder demo
    # n = 16
    # m = 4
    # circuit = Circuit()

    # manual_switches = ManualSwitches(
    #         circuit=circuit, keys=['u', 'i', 'o', 'p'][::-1],
    #     we_key='e', n=m
    # )
    # decoder = Decoder(circuit=circuit, i=manual_switches.o, n=n)
    # mbulbs = MultiBulbs(circuit=circuit, i=decoder.o, n=n)

    # circuit.initialize()
    # display = Display()
    # display.draw_box(
    #     components=[manual_switches.we_switch] + manual_switches.switches[::-1],
    #     labels=['WE'] + [f'I{j+1}' for j in range(m)][::-1],
    #     colors=[yellow] + [green for _ in range(m)],
    #     title='Manual inputs', yoffset=-180, sep_after=[1]
    # )
    # display.draw_box(
    #     components=mbulbs.bulbs, labels=[f'D{j}' for j in range(n)],
    #     colors=[green] * n, title='Decoder', yoffset=60
    # )

    # # SRAM demo
    # n = 16
    # m = 4

    # circuit = Circuit()
    # clock = Clock(circuit=circuit)
    # clock_branch = Branch1n(circuit=circuit, i=[clock.o2], n=2)
    # bus = Bus(circuit=circuit, n=8)

    # manualB_switches = ManualSwitches(
    #     circuit=circuit, o=bus.add_write(),
    #     keys=['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'][::-1],
    #     we_key='b', n=8
    # )

    # regM_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='n')
    # regM = Register(circuit=circuit, i=bus.add_read(), re=regM_re_switch.o,
    #                 clk=clock_branch.o[0], n=4)
    # regM_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='m')
    # regM_we = MultiSwitch(circuit=circuit, switch=regM_we_switch.o,
    #                       i=regM.o, o=bus.add_write(), n=4)

    # manualA_switches = ManualSwitches(
    #     circuit=circuit, keys=['u', 'i', 'o', 'p'][::-1],
    #     we_key='v', n=m
    # )
    # manualD_switches = ManualSwitches(
    #     circuit=circuit, keys=['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'][::-1],
    #     we_key='v', n=8
    # )

    # pm_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='v')
    # pm_branch = Branch1n(circuit=circuit, i=[pm_switch.o], n=2)
    # a_selector = Selector(circuit=circuit,
    #                       a=manualA_switches.o,
    #                       b=regM_we.o,
    #                       s=pm_branch.o[0],
    #                       n=4)
    # d_selector = Selector(circuit=circuit,
    #                       a=manualD_switches.o,
    #                       b=bus.add_read(),
    #                       s=pm_branch.o[1],
    #                       n=8)

    # sram_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='r')
    # sram_re_and = AND(circuit=circuit, i1=clock_branch.o[1],
    #                   i2=sram_re_switch.o)
    # sram_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='w')
    # sram = SRAM(circuit=circuit,
    #             a=a_selector.o,
    #             i=d_selector.o,
    #             re=sram_re_and.o,
    #             we=sram_we_switch.o,
    #             o=bus.add_write(),
    #             nbytes=n)

    # circuit.initialize()
    # display = Display()
    # display.draw_box(
    #     components=([manualB_switches.we_switch]
    #                 + manualB_switches.switches[::-1]),
    #     labels=['WE'] + [f'I{j+1}' for j in range(8)][::-1],
    #     colors=[yellow] + [green for _ in range(8)],
    #     title='Manual bus inputs', yoffset=-300, sep_after=[1]
    # )
    # display.draw_box(
    #     components=bus.bulbs[::-1], labels=[f'B{j+1}' for j in range(8)][::-1],
    #     colors=[green for _ in range(8)], title='Bus', yoffset=-180
    # )
    # display.draw_box(
    #     components=([clock.bulb, regM_re_switch, regM_we_switch]
    #                 + regM.bulbs[::-1]),
    #     labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(4)][::-1],
    #     colors=[blue, yellow, yellow] + [green for _ in range(4)],
    #     title='Address register', yoffset=-60, sep_after=[3]
    # )
    # display.draw_box(
    #     components=([manualD_switches.we_switch]
    #                 + manualD_switches.switches[::-1]),
    #     labels=['WE'] + [f'I{j+1}' for j in range(8)][::-1],
    #     colors=[red] + [green for _ in range(8)],
    #     title='Manual data inputs', yoffset=60, sep_after=[1]
    # )
    # display.draw_box(
    #     components=([manualA_switches.we_switch]
    #                 + manualA_switches.switches[::-1]),
    #     labels=['WE'] + [f'I{j+1}' for j in range(m)][::-1],
    #     colors=[red] + [green for _ in range(m)],
    #     title='Manual address inputs', yoffset=180, sep_after=[1]
    # )
    # display.draw_box(
    #     components=([sram_re_switch, sram_we_switch, pm_switch]
    #                 + sram.addr_bulbs[::-1]
    #                 + sram.bulbs[::-1]),
    #     labels=(['RE', 'WE', 'PM']
    #             + [f'A{j+1}' for j in range(4)][::-1]
    #             + [f'R{j+1}' for j in range(8)][::-1]),
    #     colors=[yellow, yellow, red] + [teal] * 4 + [green] * 8, title='SRAM',
    #     yoffset=300, sep_after=[2, 3, 7]
    # )

    # # Binary counter demo
    # n = 4
    # circuit = Circuit()
    # clock = Clock(circuit=circuit)
    # bus = Bus(circuit=circuit, n=8)
    # manualJ_switches = ManualSwitches(
    #     circuit=circuit, keys=['a', 's', 'd', 'f', 'g', 'h', 'j', 'k'][::-1],
    #     o=bus.add_write(), we_key='e', n=8
    # )
    # ce_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='u')
    # je_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='i')
    # co_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='o')
    # counter = BinaryCounter(circuit=circuit, clk=clock.o1,
    #                         i=bus.add_read(), o=bus.add_write(),
    #                         ce=ce_switch.o, je=je_switch.o, co=co_switch.o, n=n)

    # circuit.initialize()
    # display = Display()
    # display.draw_box(
    #     components=([manualJ_switches.we_switch]
    #                 + manualJ_switches.switches[::-1]),
    #     labels=['WE'] + [f'I{j+1}' for j in range(8)][::-1],
    #     colors=[yellow] + [green] * 8,
    #     title='Manual jump inputs', yoffset=-180, sep_after=[1]
    # )
    # display.draw_box(
    #     components=bus.bulbs[::-1], labels=[f'B{j+1}' for j in range(8)][::-1],
    #     colors=[green for _ in range(8)], title='Bus', yoffset=-60
    # )
    # display.draw_box(
    #     components=([clock.bulb, ce_switch, je_switch, co_switch]
    #                 + counter.bulbs[::-1]),
    #     labels=['CLK', 'CE', 'JE', 'CO'] + [f'O{j+1}' for j in range(n)][::-1],
    #     colors=[blue, yellow, yellow, yellow] + [green] * n,
    #     title='Binary counter', yoffset=60, sep_after=[1, 4]
    # )

    # Assembled components demo (manual controls)
    n = 16
    m = 4

    circuit = Circuit()
    clock = Clock(circuit=circuit)
    clock_branch = Branch1n(circuit=circuit, i=[clock.o2], n=6)
    bus = Bus(circuit=circuit, n=8)

    regM_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='n')
    regM = Register(circuit=circuit, i=bus.add_read(), re=regM_re_switch.o,
                    clk=clock_branch.o[0], n=4)
    regM_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='m')
    regM_we = MultiSwitch(circuit=circuit, switch=regM_we_switch.o,
                          i=regM.o, o=bus.add_write(), n=4)

    sram_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='r')
    sram_re_and = AND(circuit=circuit, i1=clock_branch.o[1],
                      i2=sram_re_switch.o)
    sram_prog = SRAMProgrammer(
        circuit=circuit, nbytes=256, pm_key='v', a_keys=['E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        d_keys = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K'], re_key='L',
        a=regM_we.o + [None] * 4, i=bus.add_read(), re=sram_re_and.o
    )
    sram_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='w')
    sram = SRAM(circuit=circuit, a=sram_prog.ao, i=sram_prog.io,
                re=sram_prog.reo, we=sram_we_switch.o, o=bus.add_write(),
                nbytes=256)

    regI_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='k')
    regI = Register(circuit=circuit, i=bus.add_read(), re=regI_re_switch.o,
                    clk=clock_branch.o[2], n=8)
    regI_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='l')
    regI_we = MultiSwitch(circuit=circuit, switch=regI_we_switch.o,
                          i=regI.o[:4], o=bus.add_write()[:4], n=4)

    ce_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='u')
    je_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='i')
    co_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='o')
    counter = BinaryCounter(circuit=circuit, clk=clock.o1,
                            i=bus.add_read(), o=bus.add_write(),
                            ce=ce_switch.o, je=je_switch.o, co=co_switch.o, n=4)

    regA_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='a')
    regA = Register(circuit=circuit, i=bus.add_read(), re=regA_re_switch.o,
                    clk=clock_branch.o[3], n=8)
    regA_branches = [Branch12(circuit=circuit, i=regA.o[j]) for j in range(8)]
    regA_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='s')
    regA_we = MultiSwitch(circuit=circuit, switch=regA_we_switch.o,
                          i=[regA_branches[j].o1 for j in range(8)],
                          o=bus.add_write(), n=8)

    regB_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='d')
    regB = Register(circuit=circuit, i=bus.add_read(), re=regB_re_switch.o,
                    clk=clock_branch.o[4], n=8)
    regB_branches = [Branch12(circuit=circuit, i=regB.o[j]) for j in range(8)]
    regB_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='f')
    regB_we = MultiSwitch(circuit=circuit, switch=regB_we_switch.o,
                          i=[regB_branches[j].o1 for j in range(8)],
                          o=bus.add_write(), n=8)

    regC_re_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='g')
    regC = Register(circuit=circuit, i=bus.add_read(), re=regC_re_switch.o,
                    clk=clock_branch.o[5], n=8)
    regC_branches = [Branch12(circuit=circuit, i=regC.o[j]) for j in range(8)]
    regC_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='h')
    regC_we = MultiSwitch(circuit=circuit, switch=regC_we_switch.o,
                          i=[regC_branches[j].o1 for j in range(8)],
                          o=bus.add_write(), n=8)

    alu_we_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='j')
    alu_su_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='p')
    alu = ALU(circuit=circuit,
              a=[regA_branches[j].o2 for j in range(8)],
              b=[regB_branches[j].o2 for j in range(8)],
              s=bus.add_write(),
              we=alu_we_switch.o,
              su=alu_su_switch.o,
              n=8)

    sram_prog.content = {
        '0000': '00011111',
        '0001': '00101110',
        '0010': '00111101',
        '1110': '00011100',
        '1111': '00001110',
    }

    print('******-')
    circuit.initialize()
    display = Display()
    display.draw_box(
        components=bus.bulbs[::-1], labels=[f'B{j+1}' for j in range(8)][::-1],
        colors=[green for _ in range(8)], title='Bus',
        xoffset=-400, yoffset=-300
    )
    display.draw_box(
        components=([clock.switch, regM_re_switch, regM_we_switch]
                    + regM.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(4)][::-1],
        colors=[blue, yellow, yellow] + [green for _ in range(4)],
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
        sep_after=[2, 3, 7], xoffset=-400, yoffset=60
    )
    display.draw_box(
        components=([clock.switch, regI_re_switch, regI_we_switch]
                    + regI.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
        colors=[blue, yellow, yellow] + [green for _ in range(8)],
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
        colors=[blue, yellow, yellow] + [green for _ in range(8)],
        title='Register A', sep_after=[3], xoffset=400, yoffset=-180
    )
    display.draw_box(
        components=[alu_we_switch, alu_su_switch] + alu.bulbs[::-1],
        labels=['WE', 'SU'] + [f'S{j+1}' for j in range(8)][::-1],
        colors=[yellow, yellow] + [green for _ in range(8)],
        title='ALU', sep_after=[2], xoffset=400, yoffset=-60
    )
    display.draw_box(
        components=([clock.switch, regB_re_switch, regB_we_switch]
                    + regB.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
        colors=[blue, yellow, yellow] + [green for _ in range(8)],
        title='Register B', sep_after=[3], xoffset=400, yoffset=60
    )
    display.draw_box(
        components=([clock.switch, regC_re_switch, regC_we_switch]
                    + regC.bulbs[::-1]),
        labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
        colors=[blue, yellow, yellow] + [green for _ in range(8)],
        title='Register C', sep_after=[3], xoffset=400, yoffset=180
    )

    # # Controller demo
    # n = 16
    # m = 4

    # circuit = Circuit()
    # hlt_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # clock = Clock(circuit=circuit, hlt=hlt_switch.o)
    # clock_branch = Branch1n(circuit=circuit, i=[clock.o2], n=8)
    # clk_full_branch = Branch1n(circuit=circuit, i=[clock.o1], n=4)
    # bus = Bus(circuit=circuit, n=8)

    # reset_switch = Switch(circuit=circuit, i=circuit.add_plus().o, key='Q')
    # reset_branch = Branch1n(circuit=circuit, i=[reset_switch.o], n=9)

    # regM_re_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # regM = Register(circuit=circuit, i=bus.add_read(), re=regM_re_switch.o,
    #                 clk=clock_branch.o[0], reset=reset_branch.o[0], n=4)

    # sram_re_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # sram_re_and = AND(circuit=circuit, i1=clock_branch.o[1],
    #                   i2=sram_re_switch.o)
    # sram_prog = SRAMProgrammer(
    #     circuit=circuit, nbytes=n, pm_key='v', a_keys=['U', 'I', 'O', 'P'],
    #     d_keys = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K'], re_key='L',
    #     a=regM.o, i=bus.add_read(), re=sram_re_and.o
    # )
    # sram_we_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # sram = SRAM(circuit=circuit, a=sram_prog.ao, i=sram_prog.io,
    #             re=sram_prog.reo, we=sram_we_switch.o, o=bus.add_write(),
    #             nbytes=n)

    # regI_re_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # regI = Register(circuit=circuit, i=bus.add_read(), re=regI_re_switch.o,
    #                 clk=clock_branch.o[2], reset=reset_branch.o[1], n=8)
    # regI_we_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # regI_we = MultiSwitch(circuit=circuit, switch=regI_we_switch.o,
    #                       i=regI.o[:4], o=bus.add_write()[:4], n=4)

    # ce_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # je_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # co_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # prog_ctr = BinaryCounter(circuit=circuit, clk=clk_full_branch.o[1],
    #                          i=bus.add_read(), o=bus.add_write(),
    #                          ce=ce_switch.o, je=je_switch.o, co=co_switch.o,
    #                          reset=reset_branch.o[2], n=4)

    # regA_re_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # regA = Register(circuit=circuit, i=bus.add_read(), re=regA_re_switch.o,
    #                 clk=clock_branch.o[3], reset=reset_branch.o[3], n=8)
    # regA_branches = [Branch12(circuit=circuit, i=regA.o[j]) for j in range(8)]
    # regA_we_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # regA_we = MultiSwitch(circuit=circuit, switch=regA_we_switch.o,
    #                       i=[regA_branches[j].o1 for j in range(8)],
    #                       o=bus.add_write(), n=8)

    # regB_re_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # regB = Register(circuit=circuit, i=bus.add_read(), re=regB_re_switch.o,
    #                 clk=clock_branch.o[4], n=8)
    # regB_branches = [Branch12(circuit=circuit, i=regB.o[j]) for j in range(8)]
    # regB_we_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # regB_we = MultiSwitch(circuit=circuit, switch=regB_we_switch.o,
    #                       i=[regB_branches[j].o1 for j in range(8)],
    #                       o=bus.add_write(), n=8)


    # regC_re_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # regC = Register(circuit=circuit, i=bus.add_read(), re=regC_re_switch.o,
    #                 clk=clock_branch.o[5], reset=reset_branch.o[5], n=8)
    # regC_we_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # regC_we = MultiSwitch(circuit=circuit, switch=regC_we_switch.o,
    #                       i=regC.o, o=bus.add_write(), n=8)

    # alu_we_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # alu_su_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # alu_fe_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # alu = ALU(circuit=circuit,
    #           a=[regA_branches[j].o2 for j in range(8)],
    #           b=regB.o,
    #           s=bus.add_write(),
    #           we=alu_we_switch.o,
    #           su=alu_su_switch.o,
    #           clk=clock_branch.o[6],
    #           fe=alu_fe_switch.o,
    #           freset=reset_branch.o[6],
    #           n=8)

    # regII_re_nots = [NOT(circuit=circuit, i=clk_full_branch.o[j])
    #                   for j in [0, 3]]
    # regII_re_and = AND(circuit=circuit, i1=regII_re_nots[0].o,
    #                     i2=regII_re_nots[1].o)
    # regII = Register(circuit=circuit, i=regI.o[4:] + alu.fo, re=regII_re_and.o,
    #                  clk=circuit.add_plus().o, n=6)

    # regO_re_switch = Transistor(circuit=circuit, i=circuit.add_plus().o)
    # regO = Register(circuit=circuit, i=bus.add_read(), re=regO_re_switch.o,
    #                 clk=clock_branch.o[7], reset=reset_branch.o[7], n=8)

    # clk_not = NOT(circuit=circuit, i=clk_full_branch.o[2])
    # step_ctr = BinaryCounter(circuit=circuit, n=3, clk=clk_not.o,
    #                          ce=circuit.add_plus().o, co=circuit.add_plus().o,
    #                          reset=reset_branch.o[8])

    # controls = [
    #     hlt_switch.switch,
    #     regM_re_switch.switch,
    #     sram_re_switch.switch,
    #     sram_we_switch.switch,
    #     regI_re_switch.switch,
    #     regI_we_switch.switch,
    #     regA_re_switch.switch,
    #     regA_we_switch.switch,
    #     alu_we_switch.switch,
    #     alu_su_switch.switch,
    #     regB_re_switch.switch,
    #     regB_we_switch.switch,
    #     regC_re_switch.switch,
    #     regC_we_switch.switch,
    #     regO_re_switch.switch,
    #     alu_fe_switch.switch,
    #     ce_switch.switch,
    #     je_switch.switch,
    #     co_switch.switch
    # ]
    # ctrl_labels = ['HLT', 'MI', 'RI', 'RO', 'II', 'IO', 'AI', 'AO',
    #                'SO', 'SU', 'BI', 'BO', 'CI', 'CO', 'OI', 'FE',
    #                'PCE', 'PCI', 'PCO']
    # nctrl_srams = (len(controls) // 8) + (len(controls) % 8 > 0)
    # step_o_branches = [Branch1n(circuit=circuit, i=[step_ctr.o[j]], n=nctrl_srams)
    #                    for j in range(3)]
    # regI_o_branches = [Branch1n(circuit=circuit, i=[regII.o[j]], n=nctrl_srams)
    #                    for j in range(6)]
    # ctrl_progs = [None] * nctrl_srams
    # ctrl_srams = [None] * nctrl_srams
    # for i in range(nctrl_srams):
    #     ctrl_progs[i] = SRAMProgrammer(
    #         circuit=circuit, nbytes=512, pm_key=f'c{i}',
    #         a_keys=['W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    #         d_keys = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K'], re_key='L',
    #         a=([step_o_branches[j].o[i] for j in range(3)]
    #            + [regI_o_branches[j].o[i] for j in range(6)]),
    #         i=[None] * 8,
    #         re=None,
    #         content={}
    #     )
    #     ctrl_srams[i] = SRAM(
    #         circuit=circuit, a=ctrl_progs[i].ao, i=ctrl_progs[i].io,
    #         o=(controls[8*i:8*(i+1)] + [None] * 8)[:8][::-1],
    #         re=ctrl_progs[i].reo, we=circuit.add_plus().o, nbytes=512
    #     )

    # instruction_set = {
    #     'NOP': ('0000', 'PCO MI, RO II PCE'),
    #     'LDA': ('0001', 'PCO MI, RO II PCE, IO MI, RO AI'),
    #     'ADD': ('0010', 'PCO MI, RO II PCE, IO MI, RO BI, SO CI FE, CO AI'),
    #     'SUB': ('0011', 'PCO MI, RO II PCE, IO MI, RO BI, SO CI SU FE, CO AI'),
    #     'STA': ('0100', 'PCO MI, RO II PCE, IO MI, AO RI'),
    #     'LDI': ('0101', 'PCO MI, RO II PCE, IO AI'),
    #     'JMP': ('0110', 'PCO MI, RO II PCE, IO PCI'),
    #     'JC' : ('0111', 'PCO MI, RO II PCE, IO PCI'), # if CF is set, else NOP
    #     'JZ' : ('1000', 'PCO MI, RO II PCE, IO PCI'), # if ZF is set, else NOP
    #     'OUT': ('1110', 'PCO MI, RO II PCE, AO OI'),
    #     'HLT': ('1111', 'PCO MI, RO II PCE, HLT'),
    # }

    # binstr = lambda x, w: bin(x)[2:].zfill(w)
    # for instr, (opcode, mucode) in instruction_set.items():
    #     for cf in ['1', '0']:
    #         for zf in ['0', '1']:
    #             store_nop = ((instr == 'JC' and cf != '1')
    #                          or (instr == 'JZ' and zf != '1'))
    #             for i, muinstr in enumerate(mucode.split(', ')):
    #                 if store_nop and i >= 2:
    #                     continue
    #                 addr = binstr(int(zf + cf + opcode + '000', 2) + i, 9)
    #                 active_idxs = [ctrl_labels.index(lab)
    #                                for lab in muinstr.split(' ')]
    #                 val = ''.join(['1' if j in active_idxs else '0'
    #                                for j in range(8*nctrl_srams)])
    #                 for k in range(nctrl_srams):
    #                     ctrl_progs[k].content[addr] = val[8*k:8*(k+1)]

    # sram_prog.content = {
    #     '0000': '01011111', # LDI 15
    #     '0001': '01001111', # STA 15
    #     '0010': '01010000', # LDI 0
    #     '0011': '11100000', # OUT
    #     '0100': '00101111', # ADD 15
    #     '0101': '01110111', # JC 7
    #     '0110': '01100011', # JMP 3
    #     '0111': '00111111', # SUB 15
    #     '1000': '11100000', # OUT
    #     '1001': '10000011', # JZ 3
    #     '1010': '01100111', # JMP 7
    #     '1110': '11111110',
    # }

    # circuit.initialize()
    # display = Display()
    # # display.draw_box(
    # #     components=bus.bulbs[::-1], labels=[f'B{j+1}' for j in range(8)][::-1],
    # #     colors=[green for _ in range(8)], title='Bus',
    # #     xoffset=-400, yoffset=-300
    # # )
    # # display.draw_box(
    # #     components=([clock.bulb, regM_re_switch]
    # #                 + regM.bulbs[::-1]),
    # #     labels=['CLK', 'RE'] + [f'D{j+1}' for j in range(4)][::-1],
    # #     colors=[blue, yellow] + [green for _ in range(4)],
    # #     title='Memory address register', sep_after=[2],
    # #     xoffset=-400, yoffset=-180
    # # )
    # # display.draw_box(
    # #     components=([sram_prog.pm_switch, sram_prog.re_switch]
    # #                 + sram_prog.a_switches.switches[::-1]
    # #                 + sram_prog.d_switches.switches[::-1]),
    # #     labels=(['PM', 'RE']
    # #             + [f'A{j+1}' for j in range(4)][::-1]
    # #             + [f'D{j+1}' for j in range(8)][::-1]),
    # #     colors=[red, yellow] + [teal] * 4 + [green] * 8,
    # #     title='SRAM programmer', sep_after=[1, 2, 6],
    # #     xoffset=-400, yoffset=-60
    # # )
    # # display.draw_box(
    # #     components=([sram_re_switch, sram_we_switch, sram_prog.pm_switch]
    # #                 + sram.addr_bulbs[::-1]
    # #                 + sram.bulbs[::-1]),
    # #     labels=(['RE', 'WE', 'PM']
    # #             + [f'A{j+1}' for j in range(4)][::-1]
    # #             + [f'R{j+1}' for j in range(8)][::-1]),
    # #     colors=[yellow, yellow, red] + [teal] * 4 + [green] * 8, title='SRAM',
    # #     sep_after=[2, 3, 7], xoffset=-400, yoffset=60
    # # )
    # # display.draw_box(
    # #     components=([clock.bulb, regI_re_switch, regI_we_switch]
    # #                 + regI.bulbs[::-1]),
    # #     labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
    # #     colors=[blue, yellow, yellow] + [green for _ in range(8)],
    # #     title='Instruction Register', sep_after=[3], xoffset=-400, yoffset=180
    # # )
    # # display.draw_box(
    # #     components=([clock.bulb, ce_switch, je_switch, co_switch]
    # #                 + prog_ctr.bulbs[::-1]),
    # #     labels=['CLK', 'CE', 'JE', 'CO'] + [f'O{j+1}' for j in range(4)][::-1],
    # #     colors=[blue, yellow, yellow, yellow] + [green] * 4,
    # #     title='Program counter', sep_after=[1, 4], xoffset=400, yoffset=-300
    # # )
    # # display.draw_box(
    # #     components=([clock.bulb, regA_re_switch, regA_we_switch]
    # #                 + regA.bulbs[::-1]),
    # #     labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)][::-1],
    # #     colors=[blue, yellow, yellow] + [green for _ in range(8)],
    # #     title='Register A', sep_after=[3], xoffset=400, yoffset=-180
    # # )
    # # display.draw_box(
    # #     components=([alu_we_switch, alu_su_switch]
    # #                 + alu.bulbs[::-1]
    # #                 + alu.fbulbs),
    # #     labels=(['WE', 'SU']
    # #             + [f'S{j+1}' for j in range(8)][::-1]
    # #             + ['CF', 'ZF']),
    # #     colors=[yellow, yellow] + [green for _ in range(8)] + [indigo] * 2,
    # #     title='ALU', sep_after=[2, 10], xoffset=400, yoffset=-60
    # # )
    # # display.draw_box(
    # #     components=([clock.bulb, regB_re_switch, regB_we_switch]
    # #                 + regB.bulbs[::-1]),
    # #     labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
    # #     colors=[blue, yellow, yellow] + [green for _ in range(8)],
    # #     title='Register B', sep_after=[3], xoffset=400, yoffset=60
    # # )
    # # display.draw_box(
    # #     components=([clock.bulb, regC_re_switch, regC_we_switch]
    # #                 + regC.bulbs[::-1]),
    # #     labels=['CLK', 'RE', 'WE'] + [f'D{j+1}' for j in range(8)],
    # #     colors=[blue, yellow, yellow] + [green for _ in range(8)],
    # #     title='Register C', sep_after=[3], xoffset=400, yoffset=180
    # # )
    # # display.draw_box(
    # #     components=regO.bulbs[::-1], title='Output',
    # #     xoffset=600, yoffset=300, decimal=True
    # # )
    # # display.draw_box(
    # #     components=([reset_switch]
    # #                 + ctrl_srams[0].addr_bulbs[::-1]
    # #                 + sum([ctrl_srams[i].bulbs[::-1]
    # #                        for i in range(nctrl_srams)], [])[:len(controls)]),
    # #     labels=(['RS']
    # #             + ['S1', 'S2', 'S3', 'I1', 'I2', 'I3', 'I4', 'CF', 'ZF'][::-1]
    # #             + ctrl_labels),
    # #     colors=([red]
    # #             + [teal] * len(ctrl_srams[0].addr_bulbs)
    # #             + [yellow] * len(controls)),
    # #     title='Controller', sep_after=[1, 10], xoffset=-120, yoffset=300
    # # )

    # display.draw_box(
    #     components=regO.bulbs[::-1], title='Output',
    #     xoffset=600, yoffset=300, decimal=True
    # )

    while True:
        key = display.win.checkKey()
        if key == 'q':
            break
        if circuit.update(key):
            display.update()

    display.win.close()

