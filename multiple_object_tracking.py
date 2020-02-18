from psychopy import core, visual, event, gui, data, sound
from random import randint, sample, choice, shuffle
from itertools import chain
import os, csv

#------ Define some utility functions ------
def display_instructions(window, message, size=1):
    """Display a message onscreen and wait for a keypress.
    
    Arguments:
        window -- the Psychopy window to draw to
        message -- the text to display
    """
    instructions = visual.TextStim(window, text=message, color='black', font='Helvetica', 
    units = 'deg', height=size, wrapWidth=100)
    instructions.draw(window)
    window.flip()
    event.waitKeys()

def write_data(filename, fieldnames, data):
    """Write data to a csv file with labelled columns.
    
    Arguments:
        filename -- string of the file name, including the extension
        fieldnames -- a list of column names
        data -- a list of lists; each sublist is one row in the csv file,
                and should be as long as the fieldnames
    """
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for datum in data:
            writer.writerow(dict([(fieldnames[i], datum[i]) for i in range(0, len(fieldnames))]))
    print('Data saved successfully.')

def get_count_response(window, question_text):
    """Accept numeric keyboard input.
    
    Arguments:
        window -- the window to draw to
        question_text -- a string to be displayed as the question
    """
    question = visual.TextStim(window, text=question_text, font='Helvetica', 
            units = 'deg', color='black', height=1, pos=(0, 5), wrapWidth = 50)
    question.setAutoDraw(True)
    response=''
    echo = visual.TextStim(window, text=response, color="red", units='deg', height = 1.5, wrapWidth = 12) 
    echo.setAutoDraw(True)
    window.flip()
    #until return pressed, listen for letter keys & add to text string
    while event.getKeys(keyList=['return'])==[] or len(response) == 0:
        letterlist=event.getKeys([str(i) for i in range(0, 10)] + ['backspace'])
        for l in letterlist:
            if l =='backspace' and len(response) > 0:
                response=response[:-1]
            else:
                response += l
        #continually redraw text onscreen until return pressed
        echo.setText(response)
        window.flip()
    echo.setAutoDraw(False)
    question.setAutoDraw(False)
    event.clearEvents()
    return int(response)
    
def get_afc_response(window, mouse, question_text, responses):
    """Generates an n-AFC question that a subject responds to by
    clicking a button. Returns the response.
    
    Arguments:
        window -- the Psychopy window to draw to
        mouse -- the mouse to monitor for input
        question_text -- a string for the question
        responses -- a list of strings, each of which is a possible answer
    """
    if len(responses) == 2:
        colors = [(229, 103, 103), (102, 151, 232)]
    else:
        colors = [(138, 125, 163)]*len(responses)
    buttonSize = (8, 4) #w, h
    separation = 10
    positions = [((i - (len(responses)/2 - .5))*separation , -5) for i in range(len(responses))]
    question = visual.TextStim(window, text=question_text, font='Helvetica', units = 'deg', height=1, 
    pos=(0,1), color='black', wrapWidth = 100)
    input = [(visual.Rect(window, width=buttonSize[0], height=buttonSize[1], 
                fillColor=colors[i], fillColorSpace='rgb255', pos=positions[i], units='deg'),
              visual.TextStim(window, text=responses[i], units = 'deg', height=.75, pos=positions[i], bold=True),
              responses[i]) for i in range(len(responses))]
    question.setAutoDraw(True)
    [(button[0].setAutoDraw(True), button[1].setAutoDraw(True)) for button in input]
    mouse.setVisible(1)
    window.flip()
    response = False
    while not response:
        buttons, last_click = mouse.getPressed(getTime=True)
        response = [input[i][2] for i in range(len(input)) if (mouse.isPressedIn(input[i][0]) and last_click[0])]
    question.setAutoDraw(False)
    [(button[0].setAutoDraw(False), button[1].setAutoDraw(False)) for button in input]
    mouse.setVisible(0)
    mouse.clickReset()
    return response[0]

#------ Define classes for experiment objects -------#

class motObject:
    """A class for the display objects.
    """
    def __init__(self, window, size, pos, bounds, color, shape):
        """Initialize a display object.
        
        Arguments:
            window -- the Psychopy window to draw to
            radius -- the radius of the object
            pos -- the starting position of the object
            bounds -- the x coordinates of the left and right edges of the display window,
                      and the y coordinates of the top and bottom edges of the display window
        """
        self.window = window
        self.pos = pos
        self.size = size
        self.color = color
        self.shape = shape
        self.velocity = [1.5*choice([-1, 1]), 1.5*choice([-1, 1])]
        self.bounds = [(bounds[0][0] + .5*self.size, bounds[0][1] - .5*self.size),
                        (bounds[1][0] - .5*self.size, bounds[1][1] + .5*self.size)]
        self.bounces = 0
    
    def create(self):
        pass
    
    def clear(self):
        """Clear the object from the screen.
        """
        self.obj.setAutoDraw(False)

    def checkCollision(self):
        """Evaluate the object's current position, compare to the bounds of the display,
        and change the object's velocity if it collided with an edge.
        """
        if self.pos[0] < self.bounds[0][0]: #left
            self.pos[0] = self.bounds[0][0]
            self.velocity[0] *= -1
            self.bounces += 1
        if self.pos[0] > self.bounds[0][1]:#right
            self.pos[0] = self.bounds[0][1]
            self.velocity[0] *= -1
            self.bounces += 1
        if self.pos[1] > self.bounds[1][0]: #top
            self.pos[1] = self.bounds[1][0]
            self.velocity[1] *= -1
            self.bounces += 1
        if self.pos[1] < self.bounds[1][1]: #bottom
            self.pos[1] = self.bounds[1][1]
            self.velocity[1] *= -1
            self.bounces += 1
    
    def update_velocity(self):
        """Draw a random number and update the object's velocity if
        the correct number is drawn.
        """
        change = randint(0, 200)
        if change == 50:
            self.velocity[0] += .5
            self.velocity[1] += .5
        elif change == 100:
            self.velocity[0] -= .5
            self.velocity[1] -= .5
        elif change == 150:
            self.velocity[0] -= .5
            self.velocity[1] += .5
        elif change == 200:
            self.velocity[0] += .5
            self.velocity[1] -= .5
        
        self.velocity[0] = 3 if self.velocity[0] > 3 else self.velocity[0]
        self.velocity[1] = 3 if self.velocity[1] > 3 else self.velocity[1]
     
    def move(self):
        """Check for collisions, check for a velocity update, and then
        update the object's position accordingly.
        """
        self.checkCollision()
        self.update_velocity()
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.obj.setPos((self.pos[0], self.pos[1]))

class motSquare(motObject):
    def __init__(self, window, size, pos, bounds, color, shape):
        super().__init__(window, size, pos, bounds, color, shape)
    
    def create(self):
        """Create a Psychopy square stimulus with the correct features.
        """
        self.obj = visual.Rect(self.window, height=self.size, width=self.size, pos=self.pos, lineColor=self.color, fillColor=self.color, units='pix')
        self.obj.setAutoDraw(True)

class motCircle(motObject):
    def __init__(self, window, size, pos, bounds, color, shape):
        super().__init__(window, size, pos, bounds, color, shape)
        self.radius = size*.75
        self.bounds = [(bounds[0][0] + self.radius, bounds[0][1] - self.radius),
                        (bounds[1][0] - self.radius, bounds[1][1] + self.radius)]
    
    def create(self):
        """Create a Psychopy circle stimulus with the correct features.
        """
        self.obj = visual.Circle(self.window, self.radius, pos=self.pos, lineColor=self.color, fillColor=self.color, units='pix')
        self.obj.setAutoDraw(True)

class unexObject(motObject):
    """A class for the unexpected object. A subclass of motObject
    with different attributes and a different movement method.
    """
    def __init__(self, window, size, bounds, color):
        """Initialize a solid-colored square.
        
        Arguments:
            window -- the Psychopy window to draw to
            size -- the length of the square's side
            bounds -- the y coordinates of the left and right edges of the
                      display
        """
        self.window = window
        self.side = size
        self.pos = [bounds[0][1] + self.side, 0]
        self.color = color
        self.velocity = [-2, 0]
    
    def create(self):
        """Create a visual stimulus at the desired position.
        """
        self.varm = visual.Rect(self.window, width=self.side*.25, height=self.side, pos=self.pos, 
        lineColor=self.color, fillColor=self.color, units='pix')
        self.harm = visual.Rect(self.window, width=self.side, height=self.side*.25, pos=self.pos, 
        lineColor=self.color, fillColor=self.color, units='pix')
        self.varm.setAutoDraw(True)
        self.harm.setAutoDraw(True)
        
    def move(self):
        """Update the object's position.
        """
        self.pos[0] += self.velocity[0]
        self.varm.setPos((self.pos[0], self.pos[1]))
        self.harm.setPos((self.pos[0], self.pos[1]))
        
    def clear(self):
        """Clear the object from the screen.
        """
        self.varm.setAutoDraw(False)
        self.harm.setAutoDraw(False)

class Trial:
    """A class to run and store attributes for a single trial."""
    def __init__(self, window, mouse, background_color, fixation_color, num_objects, object_colors, object_size, object_shapes, 
    trial_dur, attended_color, attended_shape, ib_color=None, ib_shape=None, is_ib=False):
        """Initializes a trial.
        
        Arguments:
            window -- the Psychopy window to draw to
            mouse -- the active mouse to monitor for input
            num_objects -- the number of objects to draw on the trial
            trial_dur -- the duration of the trial, in seconds
            is_ib -- whether this is an inattentional blindness trial with an unexpected object
    """
        self.window = window
        self.mouse = mouse
        self.background_color = background_color
        self.fixation_color = fixation_color
        self.num_objects = num_objects
        self.objects = []
        self.object_colors = object_colors
        self.object_size = object_size
        self.object_shapes = object_shapes
        self.trial_dur = trial_dur
        self.attended_color = attended_color
        self.attended_shape = attended_shape
        self.is_ib = is_ib
        self.ib_color = ib_color
        self.ib_shape = ib_shape
        self.ib_start = self.trial_dur/3 + 1
        self.background = visual.Rect(self.window, width=700, height=700, fillColor=self.background_color, units='pix')
        self.bounds=[(-self.background.width/2, self.background.width/2), (self.background.height/2, -self.background.height/2)]
        self.fixxvert = visual.Line(self.window, start = [0, 18], end = [0, -18], lineWidth=4, units= 'pix', lineColor=self.fixation_color)
        self.fixxhoriz = visual.Line(self.window, start = [-18, 0], end = [18, 0], lineWidth=4, units= 'pix', lineColor=self.fixation_color)
        self.blinder_r = visual.Rect(self.window, width = (self.window.size[0] - self.background.width)/2, height=self.window.size[1], 
                                            pos=(self.window.size[0]/2 - (self.window.size[0]/2-self.bounds[0][1])/2, 0), units='pix', 
                                            fillColor='white', lineColor='white')
        self.blinder_l = visual.Rect(self.window, width = (self.window.size[0] - self.background.width)/2, height=self.window.size[1], 
                                            pos=(-self.window.size[0]/2 + (self.window.size[0]/2-self.bounds[0][1])/2, 0), units='pix', 
                                            fillColor='white', lineColor='white')
        self.bounces = 0
        self.count = 0
        self.report_ib = None
        self.report_ib_color = None
        self.report_ib_shape = None
        self.object_maker = {'circle': motCircle, 'square':motSquare}
    
    def setup(self):
        """Set up the visuals for the trial and create all the objects."""
        self.background.setAutoDraw(True)
        self.objects += [self.object_maker[self.object_shapes[i]](self.window, self.object_size, 
        pos=[randint(-self.background.width/2 + 2*self.object_size, self.background.width/2 - 2*self.object_size), 
                   randint(-self.background.height/2 + 2*self.object_size, self.background.height/2 - 2*self.object_size)], 
                   bounds=self.bounds, color=self.object_colors[i], shape=self.object_shapes[i]) for i in range(self.num_objects)]
        if self.is_ib:
            self.objects.append(unexObject(self.window, self.object_size, self.bounds, self.ib_color))
        [object.create() for object in self.objects[::-1]]
        if self.is_ib:
            self.blinder_l.setAutoDraw(True)
            self.blinder_r.setAutoDraw(True)
        self.fixxvert.setAutoDraw(True)
        self.fixxhoriz.setAutoDraw(True)
        window.flip()
    
    def clear(self):
        """Clear the display."""
        self.background.setAutoDraw(False)
        self.fixxhoriz.setAutoDraw(False)
        self.fixxvert.setAutoDraw(False)
        self.blinder_l.setAutoDraw(False)
        self.blinder_r.setAutoDraw(False)
        [object.clear() for object in self.objects]
        self.window.flip()
    
    def run(self):
        """Start the animation for the trial."""
        self.timer = core.Clock()
        while self.timer.getTime() < self.trial_dur:
            if not self.is_ib or (self.is_ib and self.timer.getTime() >= self.ib_start):
                [object.move() for object in self.objects]
            elif self.is_ib:
                [object.move() for object in self.objects[:-1]]
            self.window.flip()
        self.clear()
        self.count = get_count_response(self.window, "How many times did the {0:s} {1:s} bounce?".format(self.attended_color, self.attended_shape))
        if self.is_ib:
            self.report_ib = get_afc_response(self.window, self.mouse, "Did you notice any new objects on that trial that weren't there before?", ('yes', 'no')) 
            self.report_ib_color = get_afc_response(self.window, self.mouse, "What shape was it? Guess if you don't know.", ('circle', 'triangle', self.ib_shape, 'square'))
            self.report_ib_shape = get_afc_response(self.window, self.mouse, "What color was it? Guess if you don't know.", ('tan', 'white', 'black', self.ib_color))
    
    def get_data(self):
        """Assemble the data for this trial and return it.
        
        Returns a list of the attended color, the number of objects, the color of the
        attended set, the color of the ignored set, the number of times the attended objects bounced,
        the subject's reported count, and, if it was an inattentional blindness trial, the shape of the
        ib object, the color of the ib object, whether the subject reported seeing it, what color they
        reported it being, and what shape they reported it being.
        """
        if self.is_ib:
            self.bounces = sum([object.bounces for object in self.objects[:-1] if object.color == self.attended_color])
        else:
            self.bounces = sum([object.bounces for object in self.objects if object.color == self.attended_color])

# ------ Set up the experiment parameters -------

expInfo = {'SubjID': ''}
expInfoDlg = gui.DlgFromDict(dictionary = expInfo, title='Experiment Log')
expInfo['Date'] = data.getDateStr()

window = visual.Window([1280, 800], allowGUI=True, monitor='testMonitor', color='white', fullscr=True)
mouse = event.Mouse(visible=False)
background_color = 'gray'
fixation_color = 'darkblue'
num_objects = 8
object_colors = ['white', 'black']*4
object_size = 40
object_shapes = ['circle']*4 + ['square']*4
trial_duration = 12
num_trials = 3
attended_color = choice(object_colors)
attended_shape = 'shapes'
ib_color = 'purple'
ib_shape = 'cross'
fieldnames = ['attended_color', 'attended_shape', 'ib_color', 'ib_shape'] \
+ list(chain(*[['bounces_'+ str(i), 'count_'+str(i)] for i in range(num_trials)])) \
+ ['reported_noticing', 'reported_color', 'reported_shape']
filename = expInfo['SubjID']+'_'+expInfo['Date']+'_ib_data.csv'

# ------ Run the experiment -------
display_instructions(window, "Please wait until the experimenter has cleared you to start.")

#run each trial
trial_data = [attended_color, attended_shape, ib_color, ib_shape]
for trial in range(num_trials):
    display_instructions(window, "Keep your eyes on the cross while you count how many times the {0:s} {1:s} bounce.\n\n"\
    "Press any key when you're ready to start.".format(attended_color, attended_shape))
    trial = Trial(window, mouse, background_color, fixation_color, num_objects, object_colors, object_size, object_shapes, 
    trial_duration, attended_color, attended_shape, ib_color=ib_color, ib_shape=ib_shape, is_ib=(trial == num_trials - 1))
    trial.setup()
    core.wait(1)
    trial.run()
    trial.clear()
    trial.get_data()
    trial_data += [trial.bounces, trial.count]
    if trial.is_ib:
        trial_data += [trial.report_ib, trial.report_ib_color, trial.report_ib_shape]

#output data
write_data(filename, fieldnames, [trial_data])

display_instructions(window, "Thank you for your participation. Please see the experimenter for your debriefing.")

window.close()
core.quit()