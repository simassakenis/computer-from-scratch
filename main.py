import graphics
from components import (
    Branch12, Branch21, Plus, Minus, Switch, Bulb, Transistor,
    NOT, AND, OR, DLatch,
    Circuit, Display
)


if __name__ == '__main__':
    # # basic demo
    # circuit = Circuit()
    # plus = circuit.add_plus()
    # minus = circuit.add_minus()
    # jungiklis = Switch(i=plus.o)
    # lempute = Bulb(i=jungiklis.o, o=minus.i)
    # display = Display([jungiklis, lempute], ['I', 'O'])

    # # NOT demo
    # circuit = Circuit()
    # plus = circuit.add_plus()
    # minus = circuit.add_minus()
    # jungiklis = Switch(i=plus.o)
    # lempute = Bulb(o=minus.i)
    # not_gate = NOT(circuit=circuit, i=jungiklis.o)
    # not_gate2 = NOT(circuit=circuit, i=not_gate.o)
    # not_gate3 = NOT(circuit=circuit, i=not_gate2.o)
    # not_gate4 = NOT(circuit=circuit, i=not_gate3.o)
    # not_gate5 = NOT(circuit=circuit, i=not_gate4.o, o=lempute.i)
    # display = Display([jungiklis, lempute], ['I', 'O'])

    # # AND demo
    # circuit = Circuit()
    # plus1 = circuit.add_plus()
    # plus2 = circuit.add_plus()
    # minus = circuit.add_minus()
    # jungiklis1 = Switch(i=plus1.o)
    # jungiklis2 = Switch(i=plus2.o)
    # and_gate = AND(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
    # lempute = Bulb(i=and_gate.o, o=minus.i)
    # display = Display([jungiklis1, jungiklis2, lempute], ['I1', 'I2', 'O'])

    # # OR demo
    # circuit = Circuit()
    # plus1 = circuit.add_plus()
    # plus2 = circuit.add_plus()
    # minus = circuit.add_minus()
    # jungiklis1 = Switch(i=plus1.o)
    # jungiklis2 = Switch(i=plus2.o)
    # or_gate = OR(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
    # lempute = Bulb(i=or_gate.o, o=minus.i)
    # display = Display([jungiklis1, jungiklis2, lempute], ['I1', 'I2', 'O'])

    # # XOR demo
    # circuit = Circuit()
    # plus1 = circuit.add_plus()
    # plus2 = circuit.add_plus()
    # minus = circuit.add_minus()
    # jungiklis1 = Switch(i=plus1.o)
    # jungiklis2 = Switch(i=plus2.o)
    # branch121 = Branch12(i=jungiklis1.o)
    # branch122 = Branch12(i=jungiklis2.o)
    # and_gate = AND(circuit=circuit, i1=branch121.o1, i2=branch122.o1)
    # not_gate = NOT(circuit=circuit, i=and_gate.o)
    # or_gate = OR(circuit=circuit, i1=branch121.o2, i2=branch122.o2)
    # and_gate2 = AND(circuit=circuit, i1=not_gate.o, i2=or_gate.o)
    # lempute = Bulb(i=and_gate2.o, o=minus.i)
    # display = Display([jungiklis1, jungiklis2, lempute], ['I1', 'I2', 'O'])

    # # OR loop demo
    # circuit = Circuit()
    # plus = circuit.add_plus()
    # minus = circuit.add_minus()
    # jungiklis = Switch(i=plus.o)
    # or_gate = OR(circuit=circuit, i1=jungiklis.o)
    # branch12 = Branch12(i=or_gate.o, o2=or_gate.i2)
    # lempute = Bulb(i=branch12.o1, o=minus.i)
    # display = Display([jungiklis, lempute], ['I', 'O'])

    # # SR latch demo
    # circuit = Circuit()
    # plus1 = circuit.add_plus()
    # plus2 = circuit.add_plus()
    # minus = circuit.add_minus()
    # jungiklis1 = Switch(i=plus1.o)
    # jungiklis2 = Switch(i=plus2.o)
    # or_gate = OR(circuit=circuit, i2=jungiklis1.o)
    # not_gate = NOT(circuit=circuit, i=jungiklis2.o)
    # and_gate = AND(circuit=circuit, i1=or_gate.o, i2=not_gate.o)
    # branch12 = Branch12(i=and_gate.o, o2=or_gate.i1)
    # lempute = Bulb(i=branch12.o1, o=minus.i)
    # display = Display([jungiklis1, jungiklis2, lempute], ['S', 'R', 'O'])

    # D latch demo
    circuit = Circuit()
    plus1 = circuit.add_plus()
    plus2 = circuit.add_plus()
    minus = circuit.add_minus()
    jungiklis1 = Switch(i=plus1.o)
    jungiklis2 = Switch(i=plus2.o)
    dlatch = DLatch(circuit=circuit, i1=jungiklis1.o, i2=jungiklis2.o)
    lempute = Bulb(i=dlatch.o, o=minus.i)
    display = Display([jungiklis1, jungiklis2, lempute], ['D', 'WE', 'O'])

    circuit.initialize()
    while True:
        control_keys = ['a', 's']
        key = display.win.getKey()
        if key == 'q':
            break
        elif key in control_keys:
            idx = control_keys.index(key)
            display.components[idx].toggle()
            display.update()

    display.win.close()

