#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Memory drawer.

Krusty/Benediction July 2016

Example file:

color yellow

bank C1 free to use
bank C2 free
bank C3 free to use


color orange

memory 0 0x0000 0x500 Demo System
memory 1 0x0000 0x1fff Demo system

color pink

memory 1 0x2000 0xbfff Music + player

color gray 
memory 1 0xc000 0xd000 Various things

"""

import argparse
import cairo

# http://blog.mathieu-leplatre.info/text-extents-with-python-cairo.html
def text_width(text, fontsize=14):
    try:
        import cairo
    except Exception, e:
        return len(str) * fontsize
    surface = cairo.PDFSurface('undefined.pdf', 1280, 200)
    cr = cairo.Context(surface)
    cr.select_font_face('Arial')
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
    return width


COLORS = [
        (255.0/255, 178.0/255, 70.0/255),
        (255.0/255, 41.0/255, 237.0/255),
        (75.0/255, 141.0/255, 255.0/255),
        (86.0/255, 255.0/255, 83.0/255)
        ]

class MemoryDraw(object):
    """MemoryDraw allow to create a png of Amstrad CPC memory from a description.
    It's purpose is only informative"""



    IMG_WIDTH = 1200
    IMG_HEIGHT = 1024

    BLOC_HEIGHT = 200
    BLOC_WIDTH = 400
    BLOC_SPACE = 200
    BLOC_BORDER = 2**2

    CORNER = (200, 200)


    def __init__(self, fname):
        self._surface = cairo.PDFSurface(fname, self.IMG_WIDTH, self.IMG_HEIGHT)
        self._ctx = cairo.Context(self._surface)
        self._draw_canvas()


    def _draw_canvas(self):
        """Draw an empty canvas. Things have to be added afterwhise"""


        def draw_bloc(x, y, address):
            # Outline rectangle
            self._ctx.set_source_rgb(0, 0, 0)
            self._ctx.set_line_width(self.BLOC_BORDER)

            self._ctx.rectangle(x, y, self.BLOC_WIDTH, self.BLOC_HEIGHT) 
            self._ctx.stroke()

            # Show memory
            self._ctx.set_font_size(20)
            self._ctx.select_font_face( "Arial")
            self._ctx.move_to( x - 80, y + self.BLOC_HEIGHT)
            self._ctx.set_source_rgb( 0, 0, 0)
            
            self._ctx.show_text("0x%.4x" % address)


        def draw_64k(x,y):
            for i in range(4):
                draw_bloc(x, y+ (self.BLOC_HEIGHT*i), 0x0000 + (3-i)*0x4000)


        

        draw_64k(self.CORNER[0], self.CORNER[1])
        draw_64k(self.CORNER[0]+self.BLOC_WIDTH + self.BLOC_SPACE, self.CORNER[1])


    def set_full_block_purpose(self, nb=0, delta=0, purpose="...", color=(0,1,0)):
        assert 0 <= nb < 4
        assert 0 <= delta <= 1

        x = self.CORNER[0] + (self.BLOC_WIDTH + self.BLOC_SPACE)* delta
        y = self.CORNER[1] + (3-nb) * self.BLOC_HEIGHT


        self._ctx.rectangle(x+self.BLOC_BORDER/2, y+self.BLOC_BORDER/2, self.BLOC_WIDTH-self.BLOC_BORDER, self.BLOC_HEIGHT-self.BLOC_BORDER) 
        self._ctx.set_source_rgb(color[0], color[1], color[2])
        self._ctx.fill()

        self._ctx.set_font_size(20)
        self._ctx.select_font_face( "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        xbearing, ybearing, width, height, xadvance, yadvance = self._ctx.text_extents(purpose)
        self._ctx.move_to( x + self.BLOC_WIDTH/2 -  width/2, y + self.BLOC_HEIGHT/2)
        self._ctx.set_source_rgb( 0, 0, 0)
        self._ctx.show_text(purpose)


    def set_parametrised_memory(self, start, end, delta, purpose, color=(1, 0, 1)):
        assert start >= 0x0000
        assert end <= 0xffff
        assert 0 <= delta <= 1

        def get_position(addr):
            bloc = addr / 0x4000
            relative = addr % 0x4000


            return (3-bloc+1) * self.BLOC_HEIGHT - relative*float(self.BLOC_HEIGHT)/0x4000


        posstart = get_position(start)
        posend = get_position(end)

        x = self.CORNER[0] + (self.BLOC_WIDTH + self.BLOC_SPACE)* delta
        y = self.CORNER[1] + posend
        bheight = abs(posend - posstart)

        self._ctx.set_source_rgb(0, 0, 0)
        self._ctx.set_line_width(2.5)
        self._ctx.rectangle(x + self.BLOC_BORDER/2, y + self.BLOC_BORDER/2, self.BLOC_WIDTH-self.BLOC_BORDER, bheight)
        self._ctx.stroke_preserve()

        self._ctx.set_source_rgb(color[0], color[1], color[2])
        self._ctx.fill()


        self._ctx.set_font_size(20)
        self._ctx.select_font_face( "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        xbearing, ybearing, width, height, xadvance, yadvance = self._ctx.text_extents(purpose)
        self._ctx.move_to( x + self.BLOC_WIDTH/2 -  width/2, y + bheight/2 + height/2)
        self._ctx.set_source_rgb( 0, 0, 0)
        self._ctx.show_text(purpose)


        self._ctx.set_font_size(20)
        self._ctx.select_font_face( "Arial")

        # end memory text
        text = "0x%.4x" % end
        xbearing, ybearing, width, height, xadvance, yadvance = self._ctx.text_extents(text)
        self._ctx.move_to( x+self.BLOC_WIDTH-width - self.BLOC_BORDER, y+height + self.BLOC_BORDER)
        self._ctx.set_source_rgb( 0, 0, 0)
        self._ctx.show_text(text)


        # start memory text
        text = "0x%.4x" % start
        xbearing, ybearing, width, height, xadvance, yadvance = self._ctx.text_extents(text)
        self._ctx.move_to( x+self.BLOC_BORDER, y+bheight)
        self._ctx.set_source_rgb( 0, 0, 0)
        self._ctx.show_text(text)



    def save(self):
        self._ctx.set_source_rgb( 0, 0, 0)
        self._ctx.select_font_face( "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        self._ctx.set_font_size(20)



        txt = "Main memory / CRTC accessible"
        xbearing, ybearing, width, height, xadvance, yadvance = self._ctx.text_extents(txt)
        
        self._ctx.move_to(self.CORNER[0] + (self.BLOC_WIDTH-width)/2, self.CORNER[1] - self.BLOC_BORDER)
        self._ctx.show_text(txt)


        txt = "Extra memory / NOT CRTC accessible"
        xbearing, ybearing, width, height, xadvance, yadvance = self._ctx.text_extents(txt)
        
        self._ctx.move_to(self.CORNER[0] + (self.BLOC_WIDTH-width)/2 + self.BLOC_WIDTH + self.BLOC_BORDER + self.BLOC_SPACE, self.CORNER[1] - self.BLOC_BORDER)
        self._ctx.show_text(txt)



        self._surface.finish()



class DescriptionParser(object):

    def __init__(self, f, outfname):
        self._drawer = MemoryDraw(outfname)
        self._color = (1,1,1)

        for line in f.readlines():
            self.executeLine(line)
        f.close()

        self._drawer.save()

    def executeLine(self, line):
        tokens = line.strip().split()

        if not tokens: return

        if tokens[0] == 'bank':
            self.executeBank(tokens[1:])
        elif tokens[0] == 'memory':
            self.executeMemory(tokens[1:])
        elif tokens[0] == 'color' :
            self.setColor(tokens[1])
        else:
            print tokens
            raise Exception("Parising error for " + line)


    def setColor(self, color):
        self._color = self.__getColor(color)

    def __getColor(self, name):
        return {
                'red': (1,0,0),
                'blue': (0,0,1),
                'green': (0,1,0),
                'white': (1,1,1),
                'black': (0,0,0),
                'orange': (1, 0.5, 0),
                'pink': (1, 0, 1),
                'yellow':(1,1,0),
                'gray':(0.5,.5,.5),
                }[name]

    def executeMemory(self, args):
        nb = int(args[0], 0)
        start = int(args[1], 0)
        end = int(args[2], 0)
        msg = " ".join(args[3:])

        self._drawer.set_parametrised_memory(
                start, 
                end, 
                nb, 
                msg,
                self._color)

    def executeBank(self, args):
        bank = args[0]
        nb, delta = {
                'C0': (0,0),
                'C1': (1,0),
                'C2': (2,0),
                'C3': (3,0),
                'C4': (0,1),
                'C5': (1,1),
                'C6': (2,1),
                'C7': (3,1),
        }[bank]


        text = " ".join(args[1:])
        
        self._drawer.set_full_block_purpose(
                nb, 
                delta,
                text,  
                self._color)


        

def main():
    parser = argparse.ArgumentParser(description="Document memory zones")
    parser.add_argument('input', type=open, help="Description file")
    parser.add_argument('output', help="PDF output file")
    args = parser.parse_args()

    DescriptionParser(args.input, args.output)

def test():
        drawer = MemoryDraw("/tmp/test.pdf")


        free = COLORS[2]
        music = COLORS[0]
        demosystem = COLORS[1]

        drawer.set_full_block_purpose(1, 0, "Free",  color=free)
        drawer.set_full_block_purpose(2, 0, "Free",  color=free)
        drawer.set_full_block_purpose(3, 0, "Free", color=free)


        drawer.set_parametrised_memory(0x2000 , 0x7fff, 1, "Music + player", music)
        drawer.set_parametrised_memory(0x0000 , 0x500, 0, "Demosystem", demosystem)
        drawer.set_parametrised_memory(0x0000 , 0x2000, 1, "Demosystem", demosystem)

        drawer.save()

if __name__ == "__main__":
    main()
