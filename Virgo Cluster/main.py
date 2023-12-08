# use interactive backend

## Import necessary modules:
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

import numpy as np
import os
import pandas as pd

from astropy.io import fits
from io import StringIO

import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import display, HTML, Javascript

## Create a button to show or hide all the code cells within the notebook:

javascript_functions = {False: "hide()", True: "show()"}
button_descriptions = {False: "Show code", True: "Hide code"}


def toggle_code(state):
    """
    Toggles the JavaScript show()/hide() function
    on the div.input element.
    """

    output_string = "<script>$(\"div.input\").{}</script>"
    output_args = (javascript_functions[state],)
    output = output_string.format(*output_args)

    display(HTML(output))


def button_action(value):
    """
    Calls the toggle_code function and updates the button description.
    """

    state = value.new

    toggle_code(state)

    value.owner.description = button_descriptions[state]

    # Save widget state:
    display(
        HTML('<script>Jupyter.menubar.actions._actions["widgets:save-with-widgets"].handler()</script>'))


state = False
toggle_code(state)

## Define and activate button:
toggle_button = widgets.ToggleButton(state, description=button_descriptions[state])
toggle_button.observe(button_action, "value")

## Define variables to change widget visibility:
layout_hidden = widgets.Layout(visibility='hidden')
layout_visible = widgets.Layout(visibility='visible')

## Define output widgets (they allow greater control over the display):
out0 = widgets.Output(layout={'border': '1px solid black'})
out = widgets.Output(layout={'border': '1px solid black'})

## Define widgets to allow the user to change the aperture parameters:

# Radius of the aperture:
ApertureRadius = widgets.BoundedIntText(
    value=3,
    min=0,
    max=10,
    step=1,
    description='Radius of the aperture (in pixels):',
    style={'description_width': '195px'},
    layout={'width': '300px'},
    disabled=False,
    continuous_update=True
)

# Inner annulus multiplier:
InnerAnnulus = widgets.BoundedFloatText(
    value=2,
    min=0,
    max=5,
    step=0.5,
    description='Inner annulus multiplier (in radii):',
    style={'description_width': '195px'},
    layout={'width': '300px'},
    disabled=False,
    continuous_update=True
)

# Outer annulus multiplier:
OuterAnnulus = widgets.BoundedFloatText(
    value=3,
    min=0,
    max=5,
    step=0.5,
    description='Outer annulus multiplier (in radii):',
    style={'description_width': '195px'},
    layout={'width': '300px'},
    disabled=False,
    continuous_update=True
)

## Define widgets to allow the user to change the image viewing options:

# Lower percentile (of the image maximum):
LowLim = widgets.IntSlider(
    value=0,
    min=0,
    max=100,
    step=1,
    description='Lower percentile:',
    style={'description_width': '100px'},
    layout={'width': '350px'},
    disabled=False,
    continuous_update=True,
    orientation='horizontal',
    readout=True,
    readout_format='d'
)

# Upper percentile (of the image maximum):
HiLim = widgets.IntSlider(
    value=40,
    min=0,
    max=100,
    step=1,
    description='Upper percentile:',
    style={'description_width': '100px'},
    layout={'width': '350px'},
    disabled=False,
    continuous_update=True,
    orientation='horizontal',
    readout=True,
    readout_format='d'
)

# Colour map:
Cmap = widgets.Dropdown(
    options=[('Blue-green', 'viridis'), ('Gray', 'gray'), ('Orange', 'afmhot')],  # shows the first one, but
    # takes the value of the second
    value='gray',
    description='Colour map:'
)

## Define global variables for these parameters (they will change throughout the program):

R = 3  # aperture radius
inner_annulus = 2  # inner annulus multiplier
outer_annulus = 3  # outer annulus multiplier

low_lim = 0  # lower percentile
hi_lim = 40  # upper percentile
cmap_value = 'gray'  # colour map


## Check if these values are correct:

def check_values():
    """
    Verifies whether the set of aperture parameters and image viewing values are correct. Prevents the cases
    in which errors would be raised when plotting or doing aperture photometry.

    """

    if R == 0:  # aperture radius cannot be zero
        with out:
            print("Please select a value for the aperture radius.\n")
        return 0

    elif inner_annulus <= 1:  # inner annulus radius must be larger than aperture radius
        with out:
            print("Please make sure that the inner annulus multiplier is larger than one.\n")
        return 0

    elif outer_annulus <= 1:  # outer annulus radius must be larger than aperture radius
        with out:
            print("Please make sure that the outer annulus multiplier is larger than one.\n")
        return 0

    elif inner_annulus >= outer_annulus:  # outer annulus must be larger than inner annulus
        with out:
            print("Please make sure that the outer annulus multiplier is bigger than the inner annulus multiplier.\n")
        return 0

    elif low_lim >= hi_lim:  # the upper percentile must be larger than the lower percentile
        with out:
            print("Please make sure that the lower percentile is smaller than the upper percentile.\n")
        return 0

    else:
        return 1


## Store all 72 Cepheid images in a table:

# Save them as a 2D string:
testdata = StringIO("""Apr 23,May 04,May 06,May 09,May 12,May 16,May 20,May 26,May 31,Jun 07,Jun 17,Jun 19
Cepheid 4,c4apr23.fits,c4may04.fits,c4may06.fits,c4may09.fits,c4may12.fits,c4may16.fits,c4may20.fits,c4may26.fits,c4may31.fits,c4jun07.fits,c4jun17.fits,c4jun19.fits
Cepheid 5,c5apr23.fits,c5may04.fits,c5may06.fits,c5may09.fits,c5may12.fits,c5may16.fits,c5may20.fits,c5may26.fits,c5may31.fits,c5jun07.fits,c5jun17.fits,c5jun19.fits
Cepheid 10,c10apr23.fits,c10may04.fits,c10may06.fits,c10may09.fits,c10may12.fits,c10may16.fits,c10may20.fits,c10may26.fits,c10may31.fits,c10jun07.fits,c10jun17.fits,c10jun19.fits
Cepheid 18,c18apr23.fits,c18may04.fits,c18may06.fits,c18may09.fits,c18may12.fits,c18may16.fits,c18may20.fits,c18may26.fits,c18may31.fits,c18jun07.fits,c18jun17.fits,c18jun19.fits
Cepheid 32,c32apr23.fits,c32may04.fits,c32may06.fits,c32may09.fits,c32may12.fits,c32may16.fits,c32may20.fits,c32may26.fits,c32may31.fits,c32jun07.fits,c32jun17.fits,c32jun19.fits
Cepheid 56,c56apr23.fits,c56may04.fits,c56may06.fits,c56may09.fits,c56may12.fits,c56may16.fits,c56may20.fits,c56may26.fits,c56may31.fits,c56jun07.fits,c56jun17.fits,c56jun19.fits
""")

# Convert the string to a table (rows = cepheids, columns = dates):
df = pd.read_csv(testdata, sep=",")

## Define dropdown lists for image selection:

# List of the Cepheids:
dropdown = widgets.Dropdown(
    options=['Cepheid 4', 'Cepheid 5', 'Cepheid 10', 'Cepheid 18', 'Cepheid 32', 'Cepheid 56'],
    value='Cepheid 4',
    description='Cepheid:',
)

# List of the dates:
dropdown2 = widgets.Dropdown(
    options=['Apr 23', 'May 04', 'May 06', 'May 09', 'May 12', 'May 16', 'May 20', 'May 26', 'May 31',
             'Jun 07', 'Jun 17', 'Jun 19'],
    value='Apr 23',
    description='Date:',
)


## Function to get the image frm the dropdown lists:

def Dropdown_Menu(value1, value2):
    """
    Finds the selected image in the table created above by going to the row and column corresponding to the
    selected Cepheid and date from the dropdowns. Reads the fits file and stores it in a variable.
    """

    # Get the image from the table:
    fits_image_filename = './fits_for_astropy/' + str(df.loc[value1, value2])

    # Read the fits file:
    HDUlist = fits.open(fits_image_filename)
    large = HDUlist[0].data

    # Store the file in an array:
    global img
    img = large

    # Get the size of the array:
    global x_size
    x_size = img.shape[0]
    global y_size
    y_size = img.shape[1]

    # Save widget state:
    display(
        HTML('<script>Jupyter.menubar.actions._actions["widgets:save-with-widgets"].handler()</script>'))


## Function which will make interactive matplotlib qt windows pop up in front of the notebook, instead of
## hiding behind it:

def show_plot(figure_id=None):
    if figure_id is None:
        fig = plt.gcf()
    else:
        # do this even if figure_id == 0
        fig = plt.figure(num=figure_id)

    plt.show()
    plt.pause(1e-9)
    fig.canvas.manager.window.activateWindow()
    fig.canvas.manager.window.raise_()


## Function to draw a circle (useful for aperture and annuli);

def circle(R, x, y, color_string):
    '''
    This function creates a circle of radius R centred at the point (x,y). The color of the circle must
    also be specified.
    '''
    theta = np.linspace(0, 2 * np.pi, 100)

    a = x + R * np.cos(theta)
    b = y + R * np.sin(theta)

    plt.plot(a, b, color=color_string)


## Define the x and y-positions of the mouse click. Start off with them outside the image so that no apertures
## are plotted at the beginning. Will repeatedly be reset to -1 when the apertures already drawn need to disappear.
x_center = -1
y_center = -1


## Function which calculates the signal and mean sky background within an aperture and concentric annuli centred
## on the position of the mouse click.

def Run():
    """
    Calculates the signal within an aperture and the mean sky background in a ring of concentric annuli centred
    on the position of the mouse click. Uses global variables which determine the radius of the aperture and
    annuli.
    """
    global signal, sky_bckg

    if check_values() == 1:  # only proceed if the parameters are correct

        w = np.where(img != None)  # all indices in the img array

        # Calculate the distance (in pixels) from all pixels to the star's centre:
        dist = np.sqrt((w[0] - y_center) ** 2 + (w[1] - x_center) ** 2)  # popt[0]=cenx and popt[1]=ceny;
        # w[0] gives y coords., w[1] gives x coords.
        dist = dist.reshape(x_size, y_size)  # reshape to the shape of the image

        # Find all pixels within the aperture radius:
        ww = np.where(dist < R)

        # Calculate the no. of pixels within the circular aperture:
        no_pixels = np.array(ww).shape[1]

        # Calculate the total signal within the aperture:
        total_signal = np.sum(img[ww])

        # Find all pixels within the background ring:
        m = np.where((dist > inner_annulus * R) & (dist < outer_annulus * R))

        # Calculate the total sky background:
        total_sky_bckg = np.sum(img[m])

        # Divide by no. of pixels within ring to get the mean background per pixel:
        sky_bckg = total_sky_bckg / np.array(m).shape[1]
        plt.text(0.9, 1.1, "Sky: %.4f" % (sky_bckg,), transform=ax.transAxes, \
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        # display this value on the canvas

        # Find the total signal from the star (after background subtraction from each pixel):
        signal = np.sum(img[ww] - sky_bckg)
        plt.text(0.9, 1.03, "Star: %.4f" % (signal,), transform=ax.transAxes, \
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        # display this value on the canvas

        # Show the x and y- positions of the click on the canvas:
        plt.text(0.95, -0.02, "x = %.1f" % (x_center,), transform=ax.transAxes, \
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.text(0.95, -0.09, "y = %.1f" % (y_center,), transform=ax.transAxes, \
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.draw()



    else:  # if the parameters are incorrect, prevent from calculating
        with out:
            print("Try again.\n")


## Function which draws the aperture and measures the photometric signal:

def aperture_photom(R, inner_annulus, outer_annulus):
    """
    Draws the aperture and the background ring centred on the position of the mouse click.
    Calls Run() to measure the photometric signal and mean sky per pixel within these.
    """
    ## Display the circular aperture around the star and the ring that contains the sky background:
    C1 = circle(R, x_center, y_center, 'red')
    C2 = circle(inner_annulus * R, x_center, y_center, 'orange')
    C3 = circle(outer_annulus * R, x_center, y_center, 'orange')

    ## Measure the signal and the sky background:
    Run()


## The next is the main function of the program. It is called whenever there is a mouse click anywhere on the
## canvas. It deals with all sorts of clicks and situations (i.e. left-click, right-click, zoom/pan etc.).

def on_press(event):
    """
    Main function of the program. If the user left-clicks on the image, aperture photometry is done at the
    location of the click. A right click within the image does nothing, but keeps the apertures already drawn in
    place. A click outside of the image resets everything.
    """

    if check_values() == 1:  # only proceed if the parameters are correct

        plt.clf()  # clear what was previously drawn
        plt.title(dropdown.value + '\n' + dropdown2.value + ', 1994')  # add the right title to the image

        # Display the image with the updated viewing options:
        plt.imshow(img, origin='lower', cmap=cmap_value, vmin=low_lim / 100 * np.max(img), \
                   vmax=hi_lim / 100 * np.max(img), animated=True)
        plt.draw()

        if fig.canvas.cursor().shape() == 0:  # simple click (not zoom/pan) --> 0 is the arrow click

            if ((event.xdata != None and event.ydata != None) and (event.xdata >= 0 and event.ydata >= 0) \
                    and (event.xdata <= x_size and event.ydata <= y_size)):
                # if you click inside the image

                if event.button == 1:  # left click

                    ## Centre the aperture and annuli on the position of the click:
                    global x_center, y_center
                    x_center = event.xdata
                    y_center = event.ydata

                    ## Do photometry:
                    aperture_photom(R, inner_annulus, outer_annulus)


                elif event.button == 3:  # right click

                    ## Do photometry only if there is an aperture already drawn:
                    if x_center >= 0 and y_center >= 0:
                        aperture_photom(R, inner_annulus, outer_annulus)


            else:  # if you click outside the img  or button

                x_center = -1  # reset the centre of the aperture
                y_center = -1



        else:  # i.e. fig.canvas.cursor().shape() != 0 (if you zoom/pan)

            ## Do photometry only if there is an aperture already drawn:
            if x_center >= 0 and y_center >= 0:
                aperture_photom(R, inner_annulus, outer_annulus)

    else:  # prevent the program if the initial parameters are incorrect
        with out:
            print("Try again.\n")


## Function to update the values of the aperture and image viewing parameters:

def update_values():
    """
    Reads the values of the widgets and stores them in global variables for later use.
    """
    global R
    global inner_annulus
    global outer_annulus
    global low_lim
    global hi_lim
    global cmap_value
    R = ApertureRadius.value
    inner_annulus = InnerAnnulus.value
    outer_annulus = OuterAnnulus.value
    low_lim = LowLim.value
    hi_lim = HiLim.value
    cmap_value = Cmap.value
    # Save widget state:
    display(
        HTML('<script>Jupyter.menubar.actions._actions["widgets:save-with-widgets"].handler()</script>'))


## Define a button which displays the image selected from the dropdown lists:
button1 = widgets.Button(description="Display image")
button1.style.button_color = 'lightblue'

## Define a button which updates the image corresponding to the newly set widgets:
button2 = widgets.Button(description="Update values")
button2.style.button_color = 'wheat'


## Function which sets the functionality of the 'Update values' button.
def on_update_values_button_clicked(b):
    """
    Calls update_values() to read the values of the aperture and image viewing widgets.
    Updates the image depending on these new values.
    """
    out.clear_output()
    update_values()

    if check_values() == 1:  # only proceed if the values are correct

        plt.clf()  # clear everything drawn before
        plt.title(dropdown.value + '\n' + dropdown2.value + ', 1994')  # set the right title

        ## Display the image with the new parameters:
        plt.imshow(img, origin='lower', cmap=cmap_value, vmin=low_lim / 100 * np.max(img), \
                   vmax=hi_lim / 100 * np.max(img), animated=True)
        show_plot()  # make the interactive window pop up

        ## If an aperture was previously drawn somewhere on the image, redraw it and do photometry there.
        if x_center >= 0 and y_center >= 0:
            aperture_photom(R, inner_annulus, outer_annulus)

    else:  # prevent plotting the image if the values are incorrect
        with out:
            print("Try again.\n")

    # Save widget state:
    display(
        HTML('<script>Jupyter.menubar.actions._actions["widgets:save-with-widgets"].handler()</script>'))


## Function to hide the existing widgets whenever the image tab is closed:

def on_close(event):
    """
    When the interactive plot window is closed, hide all aperture and image viewing widgets, so that they cannot
    be changed when there is no active image.
    """

    # Reset the centre of the aperture:
    global x_center
    global y_center
    x_center = -1
    y_center = -1

    # Hide the widgets and the 'Update values' button:
    out0.layout = layout_hidden
    ApertureRadius.layout = layout_hidden
    InnerAnnulus.layout = layout_hidden
    OuterAnnulus.layout = layout_hidden
    LowLim.layout = layout_hidden
    HiLim.layout = layout_hidden
    Cmap.layout = layout_hidden
    button2.layout = layout_hidden  # hide 'update values' button
    out.layout = layout_hidden

    out.clear_output()


## Activate the interactive dropdown lists and show the 'Display image' button:
widgets.interact(Dropdown_Menu, value1=dropdown, value2=dropdown2)
display(button1)

## Define what the 'Display image' button does:

# Initialise a click counter. Depending on the number of times the button has already been clicked,
# the button does different things:
click_count = 0


def on_display_img_button_clicked(b):
    """
    Defines what the 'Display image' button does. Upon clicking, erase any images plotted before, show the current
    image and display or make the image viewing widgets visible.
    """

    ## Delete the previous output:
    out.clear_output()
    plt.close()

    ## Reset the centre of the aperture:
    global x_center, y_center

    x_center = -1
    y_center = -1

    ## Show the current image:
    global fig
    global ax
    fig, ax = plt.subplots()
    plt.clf()  # clear anything plotted before
    plt.title(dropdown.value + '\n' + dropdown2.value + ', 1994')  # set the right title
    plt.imshow(img, origin='lower', cmap=cmap_value, vmin=low_lim / 100 * np.max(img), \
               vmax=hi_lim / 100 * np.max(img), animated=True)  # display the image
    show_plot()  # make the interactive window pop up

    global click_count

    if click_count == 0:  # if this is the first time the button has been clicked

        display(out0)  # display the widgets for the first time
        display(ApertureRadius)  # (doing this on a subsequent clicking would display these widgets
        display(InnerAnnulus)  # again and again)
        display(OuterAnnulus)
        display(LowLim)
        display(HiLim)
        display(Cmap)
        display(button2)  # display the 'Update values' button only after an image is shown
        display(out)

        ## Activate the 'Update values' button only after an image is shown:
        button2.on_click(on_update_values_button_clicked)


    else:  # if the button has been clicked before

        out0.layout = {'border': '1px solid black'}  # only make these widgets visible
        ApertureRadius.layout = layout_visible  # (do not display them again, or you will get duplicates)
        InnerAnnulus.layout = layout_visible
        OuterAnnulus.layout = layout_visible
        LowLim.layout = layout_visible
        HiLim.layout = layout_visible
        Cmap.layout = layout_visible
        button2.layout = layout_visible  # show the 'Update values' button only after an image is shown
        out.layout = {'border': '1px solid black'}

        ## Activate the 'Update values' button only after an image is shown:
        button2.on_click(on_update_values_button_clicked)

    click_count = click_count + 1  # increase the no. of click counts

    fig.canvas.mpl_connect('button_press_event', on_press)  # activate the canvas to the mouse-click fct.

    fig.canvas.mpl_connect('close_event', on_close)  # activate the canvas to the closing fct.

    # Save widget state:
    display(
        HTML('<script>Jupyter.menubar.actions._actions["widgets:save-with-widgets"].handler()</script>'))


## Activate the 'Display image' button:
button1.on_click(on_display_img_button_clicked)

plt.show()
