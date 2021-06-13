from components import Circuit
from display import Display
from demos import (
    bulb_demo, not_demo, and_demo, or_demo, xor_demo,
    sr_latch_demo, d_latch_demo, clock_demo, register_demo,
    alu_demo, decoder_demo, sram_demo, counter_demo,
    manual_controls_demo, controller_demo
)

if __name__ == '__main__':
    circuit = Circuit()
    display = Display()

    # bulb_demo(circuit, display)
    # not_demo(circuit, display)
    # and_demo(circuit, display)
    # or_demo(circuit, display)
    # xor_demo(circuit, display)
    # sr_latch_demo(circuit, display)
    # d_latch_demo(circuit, display)
    # clock_demo(circuit, display)
    # register_demo(circuit, display, nbits=8)
    # alu_demo(circuit, display, nbits=8)
    # decoder_demo(circuit, display, nbits=4)
    # sram_demo(circuit, display, nbytes=16)
    # counter_demo(circuit, display, nbits=4)
    # manual_controls_demo(circuit, display)
    controller_demo(circuit, display, show_full=True)

    circuit.initialize()
    display.update()

    while True:
        key = display.win.checkKey()
        if key == 'q':
            break
        if circuit.update(key):
            display.update()

    display.win.close()

