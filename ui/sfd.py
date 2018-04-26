import Tkinter as tk
import tkFileDialog
import tkMessageBox
import ttk
from PIL import Image, ImageTk, ImageDraw
import matplotlib as mpl
import matplotlib.pyplot as pp

from process.narrowbox import find_scuff

import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Scuff Finder Desktop

# Authors:
#   Nick Bond and Gabe Waksman

# Version:
#   0.3.1

# Written for Shaw Industries Group, Inc. Plant RP Quality Control
# Part of a Georgia Tech 2018 MSE Capstone II project

class Application_SFD(tk.Frame):
    im_before = None
    im_after  = None

    photo_before = None
    photo_after  = None

    real_before = ''
    real_after  = ''

    size  = (240, 180)
    ti = 'Scuff Finder Desktop'

    export_path = ''

    help_docs = '''
    Scuff Finder Desktop Help
        1. Click on the current image to bring up the file selection dialog.
        2. Select the resolution of the scuff map using the slider.
        3. After selecting both images and a grain size, click the Test
            button to analyze the images.
'''

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master.title(self.ti)
        self.set_export_path()
        self.grid()
        self.populate()

    def populate(self):
        tabs = ttk.Notebook(self)
        tab_indiv = tk.Frame(self)
        tab_stats = tk.Frame(self)
        tab_help  = tk.Frame(self)

        tabs.add(tab_indiv, text = 'Individual Samples')
        # tabs.add(tab_stats, text = 'Scuff Statistics')
        tabs.add(tab_help, text = 'Help')

        tabs.grid(row = 0, column = 0, sticky = tk.N)

        ##### individual images

        frame_before  = tk.Frame(tab_indiv)
        frame_after   = tk.Frame(tab_indiv)
        frame_grain   = tk.Frame(tab_indiv)
        # frame_arrow   = tk.Frame(tab_indiv)
        frame_buttons = tk.Frame(tab_indiv)

        ###

        label_before = tk.Label(frame_before, text = 'Pre-Scuff Image')
        label_before.grid(row = 0, pady = 5, sticky = tk.N)

        back = Image.new('L', self.size)

        back_draw = ImageDraw.Draw(back)
        back_draw.multiline_text(
            (self.size[0] / 2 - 55, self.size[1] / 2 - 5),
            'Click to add image...',
            fill  = 255,
            align = 'center'
        )

        photo_background = ImageTk.PhotoImage(back)

        back_before = tk.Label(frame_before, image = photo_background)
        back_before.image = photo_background

        back_before.bind('<Button-1>', self.get_before_image)
        back_before.grid(row = 1, pady = 5, sticky = tk.S)

        self.image_before = tk.Label(frame_before, image = photo_background)

        self.image_before.bind('<Button-1>', self.get_before_image)
        self.image_before.grid(row = 1, pady = 5)

        ###

        label_after = tk.Label(frame_after, text = 'Scuffed Image')
        label_after.grid(row = 0, pady = 5, sticky = tk.N)

        back_after = tk.Label(frame_after, image = photo_background)
        back_after.image = photo_background

        back_after.bind('<Button-1>', self.get_after_image)
        back_after.grid(row = 1, pady = 5, sticky = tk.S)

        self.image_after = tk.Label(frame_after, image = photo_background)

        self.image_after.bind('<Button-1>', self.get_after_image)
        self.image_after.grid(row = 1, pady = 5)

        ###

        label_grain = tk.Label(frame_grain, text = 'Resolution')
        label_grain.grid(row = 0, column = 0, padx = 25, pady = 0, sticky = tk.E)

        self.grain   = tk.IntVar()
        self.grain.set(10)
        slider_grain = tk.Scale(
            frame_grain,
            from_        = 2,
            to           = 50,
            orient       = tk.HORIZONTAL,
            length       = 200,
            variable     = self.grain
        )
        slider_grain.grid(row = 0, column = 1, pady = 0, sticky = tk.E)

        ###

        button_indiv_test = tk.Button(
            frame_buttons,
            text    = 'Test',
            command = self.indiv_test
        )

        button_indiv_quit = tk.Button(
            frame_buttons,
            text    = 'Quit',
            command = self.quit
        )

        button_indiv_test.grid(row = 0, column = 0, padx = 100, pady = 10, sticky = tk.W)
        button_indiv_quit.grid(row = 0, column = 1, padx = 100, pady = 10, sticky = tk.E)

        frame_before.grid(
            row = 0,
            column = 0,
            padx = 5,
            pady = 5,
            sticky = tk.W
        )

        frame_after.grid(
            row = 0,
            column = 2,
            padx = 5,
            pady = 5,
            sticky = tk.E
        )

        # frame_arrow.grid(
        #     row = 0,
        #     column = 1,
        #     padx = 5,
        #     pady = 100
        # )

        frame_grain.grid(
            row = 1,
            column = 0,
            columnspan = 3,
            padx = 5,
            pady = 5,
            sticky = tk.S
        )

        frame_buttons.grid(
            row = 2,
            column = 0,
            columnspan = 3,
            padx = 5,
            pady = 5,
            sticky = tk.S
        )

        # frame_before.grid_propagate(0)
        # frame_after.grid_propagate(0)

        ##### Help

        frame_help = tk.Frame(tab_help)

        label_help = tk.Label(
            frame_help,
            text = self.help_docs,
            justify = tk.LEFT
        )

        label_help.grid(row = 0, pady = 5, sticky = tk.W)

        frame_help.grid(
            row = 0,
            column = 2,
            padx = 5,
            pady = 5,
            sticky = tk.E
        )

    def get_before_image(self, event):
        im_file = tkFileDialog.askopenfile()
        try:
            self.im_before = Image.open(im_file.name)
            self.im_before.thumbnail(self.size)

            self.real_before = im_file.name
            im_file.close()
        except AttributeError:
            return None

        self.photo_before = ImageTk.PhotoImage(self.im_before)
        self.image_before.config(image = self.photo_before)
        self.image_before.image = self.photo_before

    def get_after_image(self, event):
        im_file = tkFileDialog.askopenfile()
        try:
            self.im_after = Image.open(im_file.name)
            self.im_after.thumbnail(self.size)

            self.real_after = im_file.name
            im_file.close()
        except AttributeError:
            return None

        self.photo_after = ImageTk.PhotoImage(self.im_after)
        self.image_after.config(image = self.photo_after)
        self.image_after.image = self.photo_after

    def indiv_test(self):
        try:
            before = Image.open(self.real_before)
            print 'before path: \"%s\"' % self.real_before
        except AttributeError:
            before = Image.new('L', self.size)
            tkMessageBox.showwarning(self.ti, 'Before image required.')
            print 'no before image found.'
            return None

        try:
            after = Image.open(self.real_after)
            print 'after path: \"%s\"' % self.real_after
        except AttributeError:
            after = Image.new('L', self.size)
            tkMessageBox.showwarning(self.ti, 'After image required.')
            print 'no after image found.'
            return None

        print 'grain: %d' % self.grain.get()

        try:
            data = find_scuff(before, after, self.grain.get())
            try:
                wg = tk.Toplevel(self)
                ws = tk.Toplevel(self)

                graph = Window_Graph(wg)
                graph.set_data(data)

                stats = Window_Stats(ws)

                tile_name = self.real_before.split('/')[-1].split('.')[0]
                stats.set_data(data, tile_name)
                stats.set_export_path(self.export_path)

                # pp.figure(1)
                # pp.pcolormesh(data['data']['rd'])
                # pp.show()
            except AttributeError:
                print 'find_scuff failure.'
                return None
        except NameError:
            print 'narrowbox not installed.'
            return None

    def set_export_path(self):
        try:
            ex = open('./.config.txt', 'w')
            line = ex.readline().strip()
            self.export_path = line
            ex.close()
        except IOError:
            self.export_path = ''

class Window_Graph(tk.Frame):
    ti   = 'Scuff Finder Desktop'
    data = None

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master.title(self.ti)
        self.grid()
        self.populate()

    def populate(self):
        self.canv = tk.Canvas(self, width = 480, height = 320)
        self.canv.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tk.N)

        button_quit = tk.Button(
            self,
            text    = 'OK',
            command = self.master.destroy
        )

        button_quit.grid(row = 1, column = 0, padx = 50, pady = 10, sticky = tk.E)

    # from matplotlib docs:
    #      https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_canvas_sgskip.html
    def draw_figure(self, figure, loc=(0, 0)):
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tk.PhotoImage(master=self.canv, width=figure_w, height=figure_h)

        self.canv.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        return photo

    def set_data(self, data):
        self.data = data

        fig = mpl.figure.Figure(figsize = (6, 4))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.pcolormesh(data['x'], data['y'], data['data']['rd'])
        # print 'nice'
        ax.set_xlabel('x (inches)')
        ax.set_ylabel('y (inches)')
        # print 'nicer'

        self.fig_x, self.fig_y = 5, 5
        self.fig_photo = self.draw_figure(fig, loc=(self.fig_x, self.fig_y))
        self.fig_w, self.fig_h = self.fig_photo.width(), self.fig_photo.height()

class Window_Stats(tk.Frame):
    ti          = 'Scuff Statistics'
    data        = None
    sample      = ''
    export_path = ''

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master.title(self.ti)
        # self.export_path = '/Users/nickbond/Desktop/test.csv'
        self.grid()
        self.populate()

    def populate(self):
        self.data_stringvar = tk.StringVar()

        frame_stats   = tk.Frame(self)
        frame_buttons = tk.Frame(self)

        ###

        label_data = tk.Label(
            frame_stats,
            justify      = 'left',
            textvariable = self.data_stringvar
        )

        label_data.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.W)

        ###

        button_export = tk.Button(
            frame_buttons,
            text    = 'Export',
            command = self.export
        )

        button_quit = tk.Button(
            frame_buttons,
            text    = 'OK',
            command = self.master.destroy
        )

        button_export.grid(row = 0, column = 1, padx = 50, pady = 10, sticky = tk.E)
        button_quit.grid(row = 0, column = 0, padx = 50, pady = 10, sticky = tk.E)

        frame_stats.grid(
            row = 0,
            column = 0,
            padx = 5,
            pady = 5,
            sticky = tk.W
        )

        frame_buttons.grid(
            row = 2,
            column = 0,
            columnspan = 3,
            padx = 5,
            pady = 5,
            sticky = tk.S
        )

    def set_data(self, data, sample):
        self.data   = data
        self.sample = sample

        data_string = '\n'

        try:
            # data_string += 'Extrema:\n'
            if not self.data['extrema']:
                raise TypeError()
            else:
                data_string += 'Maximum intensity (normalized): %0.4f\n' % (
                    self.data['extrema']['max_rd'] / (255.0 - self.data['extrema']['min_rd']))
                # data_string += 'Minimum intensity (normalized): %0.4f\n' % (self.data['extrema']['min_rd'] / 255.0)
        except TypeError:
            data_string += 'No extrema found.'
        except KeyError:
            data_string += 'No <extrema> key found.'

        data_string += '\n'

        try:
            data_string += 'Image width: %0.2f inches\n' % self.data['real_width']
        except KeyError:
            print 'No <real_width> key found.'

        try:
            data_string += 'Image height: %0.2f inches\n' % self.data['real_height']
        except KeyError:
            print 'No <real_height> key found.'

        data_string += '\n'

        try:
            data_string += 'Scuff width: %0.2f inches\n' % self.data['scuff_width']
        except KeyError:
            print 'No <scuff_width> key found.'

        try:
            data_string += 'Scuff height: %0.2f inches\n' % self.data['scuff_height']
        except KeyError:
            print 'No <scuff_height> key found.'

        try:
            data_string += 'Scuff area: %0.2f square inches' % self.data['scuff_area']
        except KeyError:
            print 'No <scuff_area> key found.'

        # try:
        #     bbox = self.data['boundingbox']
        #     data_string += 'Scuff size:\n%d pixels' % bbox.get_area()
        # except AttributeError:
        #     print bbox

        # data_string += '\n\n'
        #
        # try:
        #     grain = self.data['grain']
        #     data_string += 'Resolution:\n%d pixels' % grain
        # except AttributeError:
        #     print grain

        self.data_stringvar.set(data_string)

    def set_export_path(self, path):
        self.export_path = path

    def export(self):
        with_or_against = '' #for now, this has to be set manually
        # if ord(self.sample.split(' ')[-1]) > ord('E'):
        #     with_or_against = 'against'

        try:
            f = open(self.export_path, 'a')
            f.write('%s, %d, %0.4f, %0.2f, %s\n' % (
                self.sample,
                self.data['grain'],
                (self.data['extrema']['max_rd'] / (255.0 - self.data['extrema']['min_rd'])),
                self.data['scuff_area'],
                with_or_against
            ))
            f.close()
        except IOError:
            pass


if __name__ == '__main__':
    app = Application_SFD()
    app.mainloop()
