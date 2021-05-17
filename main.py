import graphics
from components import (
    Branch12, Branch21, Plus, Minus, Switch, Bulb, Transistor,
    NOT, AND, OR, DLatch, Clock,
    Circuit, Display
)


if __name__ == '__main__':
    # # basic demo
    # circuit = Circuit()
    # plus = Plus(circuit=circuit)
    # minus = Minus(circuit=circuit)
    # jungiklis = Switch(circuit=circuit, i=plus.o, key='a')
    # lempute = Bulb(circuit=circuit, i=jungiklis.o, o=minus.i)
    # circuit.initialize()
    # display = Display([jungiklis, lempute], ['I', 'O'])

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
    # display = Display([jungiklis, lempute], ['I', 'O'])

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
    # display = Display([jungiklis1, jungiklis2, lempute], ['I1', 'I2', 'O'])

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
    # display = Display([jungiklis1, jungiklis2, lempute], ['I1', 'I2', 'O'])

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
    # display = Display([jungiklis1, jungiklis2, lempute], ['I1', 'I2', 'O'])

    # # OR loop demo
    # circuit = Circuit()
    # plus = Plus(circuit=circuit)
    # minus = Minus(circuit=circuit)
    # jungiklis = Switch(circuit=circuit, i=plus.o, key='a')
    # or_gate = OR(circuit=circuit, i1=jungiklis.o)
    # branch12 = Branch12(circuit=circuit, i=or_gate.o, o2=or_gate.i2)
    # lempute = Bulb(circuit=circuit, i=branch12.o1, o=minus.i)
    # circuit.initialize()
    # display = Display([jungiklis, lempute], ['I', 'O'])

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
    # display = Display([jungiklis1, jungiklis2, lempute], ['S', 'R', 'O'])

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
    # display = Display([jungiklis1, jungiklis2, lempute], ['D', 'WE', 'O'])

    # # clock demo
    # circuit = Circuit()
    # minus = Minus(circuit=circuit)
    # clock = Clock(circuit=circuit)
    # lempute = Bulb(circuit=circuit, i=clock.o1, o=minus.i)
    # circuit.initialize()
    # display = Display([lempute], ['CLK'])

    # D latch with clock demo
    circuit = Circuit()
    plus1 = Plus(circuit=circuit)
    minus1 = Minus(circuit=circuit)
    minus2 = Minus(circuit=circuit)
    jungiklis = Switch(circuit=circuit, i=plus1.o, key='a')
    clock = Clock(circuit=circuit)
    lempute_pulse = Bulb(circuit=circuit, i=clock.o1, o=minus1.i)
    lempute_edge = Bulb(circuit=circuit, i=clock.o2)
    dlatch = DLatch(circuit=circuit, i1=jungiklis.o, i2=lempute_edge.o)
    lempute = Bulb(circuit=circuit, i=dlatch.o, o=minus2.i)
    circuit.initialize()
    display = Display([jungiklis, lempute_pulse, lempute_edge, lempute],
                      ['D', 'CLK', 'WE', 'O'])

    while True:
        key = display.win.checkKey()
        if key == 'q':
            break
        if circuit.update(key):
            display.update()

    display.win.close()

