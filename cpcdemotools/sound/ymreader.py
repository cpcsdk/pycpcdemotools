#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""YM reader.

Read an YM file in order to graphically analyse the content of the register.
"""

# imports
import struct
import sys

# code

class YMReader(object):
    """YMReader.
    
    Read YM file according to http://leonard.oxg.free.fr/ymformat.html"""

    def __init__(self, fname):
        super(YMReader, self).__init__()
        self._fname = fname

        self.extract_information()

    def are_data_interleaved(self):
        """Return true if the data are interleaved"""
        return (self._song_attributes & 1) == 1

    def extract_information(self):
        """Extract the data from the YM file"""

        f = open(self._fname)

        def extract_header():
            """Extract header information"""

            header = struct.unpack('>4s8siiHiHiH', f.read(34))
            assert header[0] == 'YM6!', 'Error, %s is not an YM6 file!'

            self._nb_frames = header[2]
            self._song_attributes = header[3]
            self._nb_digidrums = header[4]
            self._ym_clock = header[5]
            self._original_player_frame = header[6]
            self._loop_frame = header[7]
            self._size_additional = header[8]


            assert self._nb_digidrums == 0, 'Error, we do not treat digidrums'

        def extract_string():
            """Extract a string (until is 0 is met)"""
            string = []

            while True:

                char = f.read(1)
                if char != '\0':
                    string += char
                else:
                    break
            return "".join(string)

        def extract_values():
            """Extract the values of each registers"""

            if self.are_data_interleaved():
                # Loop among all registers
                self._registers = []
                for R in range(16):
                    self._registers.append([ord(_) for _ in f.read(self._nb_frames)])
            else:
                assert False, "You need to use an interleaved YM"


        # Get the informations from the file
        extract_header()
        self._song_name = extract_string()
        self._author_name = extract_string()
        self._song_comment = extract_string()
        extract_values()

        assert "End!" == f.read(), 'Error while reading the YM file'
        f.close()
        

    def __str__(self):
        string = """
        %s

        Nb frames:\t%d
        Attributes:\t%d (Interleaved=%i)
        Nb digidrums:\t%d
        YM clock:\t%d
        Original player frame:\t%d
        Loop frame:\t%d
        Additional:\t%d

        Song name:\t %s
        Author name:\t %s
        Song comment:\t %s
        """ % (self._fname,
               self._nb_frames ,
               self._song_attributes ,
               self.are_data_interleaved(),
               self._nb_digidrums ,
               self._ym_clock ,
               self._original_player_frame ,
               self._loop_frame ,
               self._size_additional ,
               self._song_name,
               self._author_name,
               self._song_comment,
              )

        return string


    def graph(self):
        """Graph registers contents"""
        def frame_nb_to_hour(nb):
            nb_totseconds = nb/50
            nb_seconds = nb_totseconds%60
            nb_totminutes = nb_totseconds/60
            return "%d'%d''" % (nb_totminutes, nb_seconds)

        import matplotlib.pyplot as plt
        for R in range(len(self._registers)):
            plt.figure()
            plt.suptitle('R%d - %d distinct values' % (R, len(set(self._registers[R]))))

            plt.subplot(1,2,1)
            plt.title('Register values')
            plt.plot(self._registers[R], '.')
            nums, labels = plt.xticks()
            plt.xticks(nums, [frame_nb_to_hour(nb) for nb in nums])

            
            # Specific code to show when R12 has several values
            # because Hicks player is not able to manage such tunes
            if R == 12 and len(set(self._registers[R]))!=1:
                first = self._registers[R][0]
                for i in range(len(self._registers[R])):
                    if self._registers[R][i] != first:
                        plt.annotate(frame_nb_to_hour(i), (i,self._registers[R][i]), 
                        horizontalalignment='center', verticalalignment='center')
                        print 'R12 different at frame %d : %s' % (i, frame_nb_to_hour(i))

            plt.subplot(1,2,2)
            plt.title('Histogram of values')
            plt.hist(self._registers[R])
        plt.show()

if __name__ == '__main__':
    ym = YMReader(sys.argv[1])
    print ym

    ym.graph()
# metadata
__author__ = 'Krusty/Benediction'
__copyright__ = 'Copyright 2012, Benediction'
__credits__ = ['Krusty/Benediction']
__licence__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Krusty/Benediction'
__email__ = 'krusty@cpcscene.com'
__status__ = 'Prototype'

