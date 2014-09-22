#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AUTHOR Krusty/Benediction <krusty@cpcscene.com>

Help for coding CRTC transitions and so on.
Big thanks to Grimmy for its documentation here: http://www.grimware.org/doku.php/documentations/devices/crtc
"""

import sys
import argparse

class SimpleGA(object):
    """Very minimilistic GA implementation.
    YOU MUST CALL EXECUTE AT EACH NOP (BEFORE CRTC WORK)
    """

    def __init__(self):
        self._nop_counter = 0
        self._interupt_counter = 0
        self._int_raised = False
        self._vsync_occured_counter = -1


    def is_int_raised(self):
        """Return true if we just raised an int"""
        return self._int_raised

    def execute(self):
        self._nop_counter = self._nop_counter + 1
        self._int_raised = False

    def hsync_fall(self):
        """CRTC just stop an hsync signal."""
        self._interupt_counter = (self._interupt_counter + 1) & 0b00111111

        if self._interupt_counter == 52:
            self._interupt_counter = 0
            self._int_raised = True

        # Manage the two hsync wait
        if self._vsync_occured_counter != -1:
            self._vsync_occured_counter = self._vsync_occured_counter - 1

            if self._vsync_occured_counter == 0:
                self._vsync_occured_counter == 0

                if self._interupt_counter >= 32:
                    self._interupt_counter = 0
                else:
                    self._interupt_counter = 0
                    self._int_raised = True


    def vsync_occurs(self):
        """A vsync just occured"""
        self._vsync_occured_counter = 2

class SimpleCRTC(object):
    """Simple implementation of CRTC.
    Contains the minimum to work with R7 and R2 transitions
    """

    def __init__(self):
        """Initialise CRTC register values"""

        # Set initial values of registers
        self._registers = [63, 40, 46, 0x8e,
                           38, 0, 25, 30, 0,
                           7, 0, 0, 0x20, 0x00, 0]

        self.rest_internal_counters()

    def rest_internal_counters(self):
        """Reset various CRTC internal counters"""
        self._HCC = 0       # Character counter in a line
        self._VCC = 0       # Vertical Character Counter
        self._VLC = 0       # Vertical line counter
        self._VSyncCounter = 0
        self._HSyncCounter = 0
        self._nop_counter = 0

        self._ga = SimpleGA()

    def R0(self):
        return self._registers[0]
    def R1(self):
        return self._registers[1]
    def R2(self):
        return self._registers[2]
    def R3(self):
        return self._registers[3]
    def R4(self):
        return self._registers[4]
    def R5(self):
        return self._registers[5]
    def R6(self):
        return self._registers[6]
    def R7(self):
        return self._registers[7]
    def R8(self):
        return self._registers[8]
    def R9(self):
        return self._registers[9]
    def R10(self):
        return self._registers[10]
    def R11(self):
        return self._registers[11]
    def R12(self):
        return self._registers[12]
    def R13(self):
        return self._registers[13]





    def set_register(self, register, value):
        """Modify the value of the register"""
        assert register<len(self._registers) and register >= 0

        self._registers[register] = value


    def get_HCC(self):
        """Return Horizontal Char Counter value (HCC).
        Goes from 0 to R0
        """
        return self._HCC

    def get_VCC(self):
        """Return Vertical Char Counter value (VCC).
        Goes from 0 to R4
        """
        return self._VCC

    def get_VLC(self):
        """Return Vertical Line Counter value (VLC).
        Goes from 0 to R0
        """
        return self._VLC


    def get_VSync_width(self):
        """Return the VSynch width.
        It is stored in high quartet of register 3
        """
        return 16
        val = (self._registers[3] & 0b11110000) >> 4
        if val == 0:
            return 16
        else:
            return val

    def get_HSync_width(self):
        """Return the HSynch width.
        It is stored in low quartet of register 3
        """
        return self._registers[3] & 0b1111


    def is_VSync(self):
        """Test if we are in vsync."""
        return self._VSyncCounter != 0

    def is_HSync(self):
        """Test if we are in hsync."""
        return self._HSyncCounter != 0

    def _decrease_HSyncCounter(self):
        """Decrease HSYNC counter and increment GA one if needed."""

        self._HSyncCounter = self._HSyncCounter - 1

        if self._HSyncCounter == 0:
            self._ga.hsync_fall()

    def is_border(self):
        """Test if we are in border.
        Warning can be both in border and hsync or vsync
        """
        horizontal = self._HCC >= self._registers[1]
        vertical = self._VCC >= self._registers[6]

        return horizontal | vertical


    def get_nops(self):
        return self._nop_counter

    def reset_nops(self):
        self._nop_counter = 0

    def execute_n_nops(self, n, verbose):
        """Execute the CRTC during n NOPS.
        It allows to simulate the execution of a Z80 command.

        Parameters
        ----------
            - n : int
                Number of nop to execute
            - verbose : bool
                Do we print on screen ?
        """

        for i in range(n):
            if verbose:
              self.print_state_per_char_line()
            self.execute()

    def execute(self):
        """Do all the things during the life of the CRTC during one nop"""
        self._ga.execute()
        self._nop_counter = self._nop_counter + 1

        # Increment horizontal counter
        self._HCC = self._HCC + 1
        if self._HSyncCounter != 0:
            self._decrease_HSyncCounter()

        if self._HCC == self._registers[2]:
            self._HSyncCounter = self.get_HSync_width()

        # New line ?
        if self._HCC > self._registers[0]:
            self._HCC = 0

            # Increment vertical line counter
            if self._VSyncCounter != 0:
                self._VSyncCounter = self._VSyncCounter -1

            self._VLC = self._VLC + 1
            if self._VLC > self._registers[9]:
                self._VLC = 0

                # Increment vertical char counter
                self._VCC = self._VCC + 1

                if (self._VCC == self._registers[7]) and (self._VSyncCounter == 0):
                    self._VSyncCounter = self.get_VSync_width()
                    self._ga.vsync_occurs()

                # Verify looping of VCC
                if self._VCC > self._registers[4]:
                    self._VCC = 0

           


    def print_state_per_char_line(self):
        """Print CRTC state per each char_line"""
  #      if self._ga.is_int_raised():
  #          sys.stdout.write(' Int (line %d/%d) at %d nops' % \
  #              (self.get_VCC(),self.get_VLC(), self.get_nops()))

        if self.get_VLC() != 0:
            return

        self.print_state()

    def print_state(self):
        """Print CRTC state on screen"""

       
        if self._HCC == 0:
            if self._VCC == self._registers[6]:
                sys.stdout.write(' R6')
            elif self._VCC == self._registers[7]:
                sys.stdout.write(' R7')

            sys.stdout.write("\n%02d " % self._VCC)

        if self.is_HSync():
            sys.stdout.write("H")
        elif self.is_VSync():
            sys.stdout.write('V')
        elif self.is_border():
            sys.stdout.write('B')
        else:
            sys.stdout.write('C')

    def run_until_next_vsync(self, _print=False):
        """Launch CRTC emulation, and stop when a vbl is reatched

        Parameters
        ----------
            - _print: boolean
                if True, print CRTC info on screen
        """

        #Leave current vbl if we are inside
        while self.is_VSync():
            if _print:
                self.print_state_per_char_line()
            self.execute()

        #Loop until we reach vbl
        while not self.is_VSync():
            if _print:
                self.print_state_per_char_line()
            self.execute()

        if _print:
            sys.stdout.write("\n")

    def print_horizontal_top_rule(self):
        """Print the horinzonal rule"""
        sys.stdout.write('   ')
        for i in range(64):
            sys.stdout.write("%d" % (i/10))
        sys.stdout.write("\n")
        sys.stdout.write('   ')
        for i in range(64):
            sys.stdout.write("%d" % (i%10))

    def print_horizontal_bottom_rule(self):
        """Print the horinzonal rule"""
        sys.stdout.write('   ')
        for i in range(64):
            if i == self._registers[1]:
                sys.stdout.write('R')
            elif i == self._registers[2]:
                sys.stdout.write('R')
            elif i == self._registers[2] + self.get_HSync_width():
                sys.stdout.write('R')
            else:
                sys.stdout.write(" ")

        sys.stdout.write("\n")
        sys.stdout.write('   ')
        for i in range(64):
            if i == self._registers[1]:
                sys.stdout.write('1')
            elif i == self._registers[2]:
                sys.stdout.write('2')
            elif i == self._registers[2] + self.get_HSync_width():
                sys.stdout.write('3')
            else:
                sys.stdout.write(" ")

        sys.stdout.write("\n")


    def print_configuration(self):
        """Print CRTC configuration on screen"""
        self.run_until_next_vsync(_print=False)

        self.reset_nops()
        self.print_horizontal_top_rule()
        self.run_until_next_vsync(_print=True)
        self.print_horizontal_bottom_rule()

        self.print_registers()

        print ('%d nops' % self.get_nops())

    def print_registers(self):
        """Print register values"""

        print 'Register values'
        vals = [ "R%d:0x%x" % (crtc, value) for crtc, value in enumerate(self._registers)]
        sys.stdout.write("\n".join(vals))
        sys.stdout.write("\n")



class TransitionHelper(object):
    """Build and validate CRTC transitions."""

    def __init__(self):
        self._crtc = SimpleCRTC()

        self._reset_source_code()

    def _reset_source_code(self):
        self._source_code =  " ; Generated source by crtc_transition_helper.py\n"
        self._source_code += " ; (Krusty/Benediction (c) 2011\n\n"

    def set_crtc_register_value_as_slow_as_a_z80(self, register, value,
            verbose=True):
        """Change a CRTC register value, and execute the crtc tp reach the
        number of nops to do

        ld bc, 0xbc00 + register    ;4
        out (c), c                  ;5
        ld bc, 0xbd00 + value       ;4
        out (c), c                  ;5


        Parameters
        ----------
            - register: int
                Number of CRTC register
            - value: int
                Value to put in the register
            - verbose: bool
                Do we print on screen ?
        """

        self._crtc.execute_n_nops(4+5+4+5, verbose)
        self._crtc.set_register(register, value)

        self._source_code += """
    ld bc, 0xbc00 + %d
    out (c), c
    ld bc, 0xbd00 + %d
    out (c), c
""" % (register, value)


    def compute_r2_transition(self, start, stop):
        """Compute and validate a R2 transition.
        Assert transition is tested after an halt
        """

        self._crtc.set_register(6, 39)
        # Configure start
        if start != self._crtc.R2():
            self._crtc.set_register(2, start)
            self._crtc.rest_internal_counters()

        if start == stop:
            print 'Ugh?!'
        elif stop < start:
            success= False
            for delta in range(65):
                try:
                    self._compute_r2_transition_decrease(start, stop, delta)
                    success = True
                    break
                except:
                    pass

            if not success:
                    print "Problem not solved :("


        else:
            success= False
            for delta in range(65):
                try:
                    self._compute_r2_transition_increase(start, stop, delta)
                    success = True
                    break
                except:
                    pass

            if not success:
                    print "Problem not solved :("

    def _compute_r2_transition_increase(self, start, stop, delta = 0):
        """Compute the transition"""
        self._source_code += """
 ; Transition from R2=%d to R2=%d
""" % (start, stop)


        # Wait until being at a hsync (always the same vertical position)
        self._crtc.print_horizontal_top_rule()
        self._crtc.run_until_next_vsync(_print=False)
        self._crtc.reset_nops()

        while not self._crtc._ga.is_int_raised():
                self._crtc.execute()
        self._crtc._ga._int_raised = False

        # Print some lines of information to cleanup vars
        for i in range(64*10 + delta):
            self._crtc.print_state()
            self._crtc.execute()

        self._source_code += """
    defs %d
""" % delta

        R2_DIFF = stop - start
        self._source_code += """
    ld bc, 0xbc00      ; 3
    out (c), c         ; 4
    inc b              ; 1
    ld a, 63 - %d      ; 3
    out (c), a         ; 4
""" % R2_DIFF
        self._crtc.execute_n_nops(3+4+1+3+4, verbose=True)
        self._crtc.set_register(0, 63-R2_DIFF)

        NB_WAIT = 25 #TODO Need to be computed ?
        self._source_code += """
    defs %d            ; %d
""" % (NB_WAIT, NB_WAIT)
        self._crtc.execute_n_nops(NB_WAIT, verbose=True)

        self._source_code += """
    ld bc, 0xbc02      ; 3
    out (c), c         ; 4
    ld a, %d           ; 2
    inc b              ; 1
    out (c), a         ; 4
""" % stop
        self._crtc.execute_n_nops(3+4+2+1+4, verbose=True)
        self._crtc.set_register(2, stop)

        self._source_code += """
    ld bc, 0xbc00      ; 3
    out (c), c         ; 4
    inc b              ; 1
    ld a, 63           ; 2
    out (c), a         ; 4
"""
        self._crtc.execute_n_nops(3+4+1+2+4, verbose=True)
        self._crtc.set_register(0, 63)


        #Display screen after
        for i in range(64*10):
            self._crtc.print_state()
            self._crtc.execute()

        # Wait end of screen
        self._crtc.run_until_next_vsync(_print=False)
        print 'Transition done in %d nops' % self._crtc.get_nops()
        print self._source_code
        assert self._crtc.get_nops() == 64*39*8




    def _compute_r2_transition_decrease(self, start, stop, delta):
        """Compute the transition"""
        self._source_code += """
 ; Transition from R2=%d to R2=%d
""" % (start, stop)


        # Wait until being at a hsync (always the same vertical position)
        self._crtc.print_horizontal_top_rule()
        self._crtc.run_until_next_vsync(_print=False)
        self._crtc.reset_nops()

        while not self._crtc._ga.is_int_raised():
                self._crtc.execute()
        self._crtc._ga._int_raised = False

        # Print some lines of information to cleanup vars
        for i in range(64*10 + delta):
            self._crtc.print_state()
            self._crtc.execute()
        self._source_code += """
    defs %d
""" % delta


        R2_DIFF = start - stop
        self._source_code += """
    ld bc, 0xbc00      ; 3
    out (c), c         ; 4
    inc b              ; 1
    ld a, 63 + %d      ; 3
    out (c), a         ; 4
""" % R2_DIFF
        self._crtc.execute_n_nops(3+4+1+3+4, verbose=True)
        self._crtc.set_register(0, 63+R2_DIFF)

        NB_WAIT = 25 #TODO Need to be computed ?
        self._source_code += """
    defs %d            ; %d
""" % (NB_WAIT, NB_WAIT)
        self._crtc.execute_n_nops(NB_WAIT, verbose=True)

        self._source_code += """
    ld bc, 0xbc02      ; 3
    out (c), c         ; 4
    ld a, %d           ; 2
    inc b              ; 1
    out (c), a         ; 4
"""
        self._crtc.execute_n_nops(3+4+2+1+4, verbose=True)
        self._crtc.set_register(2, stop)

        self._source_code += """
    ld bc, 0xbc00      ; 3
    out (c), c         ; 4
    inc b              ; 1
    ld a, 63           ; 2
    out (c), a         ; 4
"""
        self._crtc.execute_n_nops(3+4+1+2+4, verbose=True)
        self._crtc.set_register(0, 63)


        #Display screen after
        for i in range(64*10):
            self._crtc.print_state()
            self._crtc.execute()

        # Wait end of screen
        self._crtc.run_until_next_vsync(_print=False)
        assert self._crtc.get_nops() == 64*39*8
        print 'Transition done in %d nops' % self._crtc.get_nops()


        print self._source_code

    def compute_r7_transition(self, start, stop):
        """Compute the way of doing a R7 transition and validate it"""

        # Configure start
        if start != self._crtc._registers[7]:
            self._crtc.set_register(7, start)
            self._crtc.rest_internal_counters()

        if stop > start:
            self._compute_r7_transition_increase( start, stop)
        elif stop < start:
            self._compute_r7_transition_decrease( start, stop)
        else:
            "Ugh?"

    def _compute_r7_transition_decrease(self, start, stop):
        """Compute transition when we increase R7 value"""

        print 'Screen during transition'

        self._source_code += """
 ; Transition from R7=%d to R7=%d
""" % (start, stop)

        # Wait frame
        self._crtc.print_horizontal_top_rule()
        self._crtc.run_until_next_vsync(_print=False)
        self._crtc.reset_nops()

        self._source_code += """
    call secure_wait_vsync

 ; Halt which can be removed with the secure wait
"""


        R4_DIFF = start - stop
        # Change R4 value
        self.set_crtc_register_value_as_slow_as_a_z80(4, 38 + R4_DIFF)
        self.set_crtc_register_value_as_slow_as_a_z80(7, stop )

        nb_halts_to_wait = 2
        for i in range(nb_halts_to_wait):
            self._source_code += """
    halt
"""

            while not self._crtc._ga.is_int_raised():
                self._crtc.print_state_per_char_line()
                self._crtc.execute()
            self._crtc._ga._int_raised = False


        self._crtc.run_until_next_vsync(_print=True)
        self._source_code += """
    call secure_wait_vsync
"""

        assert self._crtc.get_nops() == 64*39*8
        print 'Transition done in %d nops' % self._crtc.get_nops()


        # Reset R4
        self.set_crtc_register_value_as_slow_as_a_z80(4, 38)
        # Change R7 value



        print 'Screen after transition'
        self._crtc.print_configuration()

        print 'Source code'
        print self._source_code





    def _compute_r7_transition_increase(self, start, stop):
        """Compute transition when we decrease R7 value"""

        print 'Screen during transition'

        self._source_code += """
 ; Transition from R7=%d to R7=%d
""" % (start, stop)

        # Wait frame
        self._crtc.print_horizontal_top_rule()
        self._crtc.run_until_next_vsync(_print=False)
        self._crtc.reset_nops()

        self._source_code += """
    call secure_wait_vsync
"""


        R4_DIFF = stop - start
        # Change R4 value
        self.set_crtc_register_value_as_slow_as_a_z80(4, 38 - R4_DIFF)


        nb_halts_to_wait = R4_DIFF*8/52

        #
        for i in range(nb_halts_to_wait+1):
            self._source_code += """
    halt
"""

            while not self._crtc._ga.is_int_raised():
                self._crtc.print_state_per_char_line()
                self._crtc.execute()
            self._crtc._ga._int_raised = False


        # Reset R4
        self.set_crtc_register_value_as_slow_as_a_z80(4, 38)
        # Change R7 value
        self.set_crtc_register_value_as_slow_as_a_z80(7, stop )


        self._crtc.run_until_next_vsync(_print=True)
        self._crtc.print_horizontal_bottom_rule()

        print 'Transition done in %d nops' % self._crtc.get_nops()
        assert self._crtc.get_nops() == 64*39*8

        print 'Screen after transition'
        self._crtc.print_configuration()

        print 'Source code'
        print self._source_code




def test_crtc():
    crtc = SimpleCRTC()
    crtc.print_configuration()


def test_transition1():
    """Test a transition with increasing R7"""
    print """Test a transition with increasing R7"""
    helper = TransitionHelper()
    helper.compute_r7_transition(30, 35)

def test_transition2():
    """Test a transition with decreasing R7"""
    print """Test a transition with decreasing R7"""
    helper = TransitionHelper()
    helper.compute_r7_transition(35, 10)

def test_transitiona():
    """Test a transition with decreasing R2"""
    print """Test a transition with decreasing R2"""

    for start in range(10,64):
        for stop in range(10,64):
            helper = TransitionHelper()
            helper.compute_r2_transition(start, stop)



if __name__ == "__main__":
    #test_transition1()
    #test_transition2()
    #test_transitiona()

    parser = argparse.ArgumentParser(description='Compute CRTC transitions.')
    parser.add_argument('--begin', '-b', type=int, required=True,
                   help='Initial value for the register')
    parser.add_argument('--end', '-e', type=int,required=True,
                   help='Final value for the register')

    parser.add_argument('--register', '-r', type=int, choices=(2,7),required=True,
                   help='Register to treat (7 or 2)')

    args = parser.parse_args()

    helper = TransitionHelper()
    if args.register == 7:
        helper.compute_r7_transition(args.begin, args.end)
    elif args.register == 2:
        helper.compute_r2_transition(args.begin, args.end)
    else:
        print args
