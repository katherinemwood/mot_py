This script runs a simple multiple-object-tracking task, with an unexpected object on the final trial.

## Quick Customization

The following variables can be changed to immediately alter the appearance or behavior of the script:

`background_color` (line 364): This sets the background color for the actual trials. You can replace this with [any of the color names on this list](https://htmlcolorcodes.com/color-names/).  
`fixation_color` (line 365): This sets the color for the fixation cross. You can replace it with any valid color name to change it.  
`num_objects` (line 366): How many objects total in the task. Should be a multiple of the number of distinct object groups you want.  
`object_colors` (line 367): The colors for the objects. Can be any valid color name. You need to have as many colors as you have objects, but you can use as many colors as you like.  
`object_size` (line 368): The size of each object, in pixels. For square objects this is the length of a side; for circles, they'll have a radius 75% as large.
`object_shapes` (line 369): The shape of each object. You need as many shapes as you have objects. Currently only circles and squares are supported.
`trial_duration` (line 370): The length of each trial, in seconds.
`num_trials` (line 371): The number of trials. The unexpected object will appear on the last trial.
`attended_color` (line 372): The color of object a participant should attend to. Right now it chooses randomly between white and black, but you can set it equal to a string (e.g. 'black') to specify a color in particular.
`attended_shape` (line 373): The shape a participant should attend to. Right now one isn't specified, so it's just "shapes."
`ib_color` (line 374): The color of the unexpected object. Any valid color name works here.
`ib_shape` (line 375): The shape of the unexpected object. Right now only a cross is supported.
