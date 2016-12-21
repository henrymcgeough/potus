#*********************************************************************
#                      Python Adventure Writing System
#                                Game Engine
#                      Written by Roger Plowman (c) 1998-2001
#
# This module contains the constants and classes required to create
# the PAWS runtime system. This includes the game engine, parser,
# global variables, and a *very* basic "thing" object and verb object.
#
# It assumes some sort of library will be layered on top of it before
# games are developed. By default this library is Universe.
#
# Written By: Roger Plowman     
# Written On: 07/30/98
#
#*********************************************************************


#======================================================================
#                           Library Imports
#======================================================================

# We need some standard Python libraries. These aren't part of PAWS,
# rather they're supplied as part of Python. It's good programming
# practice not to "re-invent the wheel" when you don't have to, so
# always look for a pre-written library to do your work for you!

#----------------------
# PAWS/Universe Support
#----------------------

import os               # Operating System specific functions
import pickle           # picking functions (for save/restore)
import string           # String handling functions
import sys              # System related functions
import types            # variable type identifiers
import random           # Random # generator & functions

#------------------------
# Curses Terminal Support
#------------------------

#try:
import curses       # Basic Curses character terminal support
#except:
#    pass

#------------------------
# WConio Terminal Support
#------------------------

#try:
#import WConio       # Windows 32-bit Console
#except:
#    pass

#-----------------------------------------
# Tkinter Terminal Support (Nathan Barnes)
#-----------------------------------------

#try:
import thread       # Multithreading support
import Tkinter      # Tkinter interface API
import tkMessageBox # Tkinter message box object
import time         # Time function support
#except:
#    pass

     

#----------------------------
# Bootstrap Classes/Functions
#----------------------------

# To avoid some chicken-and-egg problems with terminal handling we define a 
# few classes now, such as ClassFundamental and ClassActiveIO.


#-------------
# Base Classes
#-------------

# This function takes a class and recursively returns a list of the class's base
# classes, starting with the object's immediate parent(s) and stepping upward
# through all the object's ancestors.

def BaseClasses(Class):
    """Returns a list of all the passed class's ancestor class objects"""

    #-------------------------
    # Create Empty Return List
    #-------------------------

    ReturnList = []

    #-------------------------------------------
    # Return [] If Class Wasn't Actually A Class
    #-------------------------------------------

    if type(Class)<>types.ClassType:
        return ReturnList

    ReturnList.append(Class)

    #---------------------------
    # Find Class's Base Class(s)
    #---------------------------

    ClassTuple = Class.__bases__

    #-----------------------
    # For Each Base Class...
    #-----------------------

    # The return list is the base classes of the base class plus the base class
    # itself. Mind bending, but true. This is a recursive call.

    for BaseClass in ClassTuple:
        ReturnList = Union(ReturnList,BaseClasses(BaseClass))

    #-----------------
    # Return To Caller
    #-----------------

    return ReturnList


#--------------------
# Object Base Classes
#--------------------

# This function takes an object and returns a list of the object's base classes,
# starting with the object's immediate parent(s) and stepping upward trhough all
# the object's ancestors.

def ObjectBaseClasses(object):
    """Returns a list of all object's ancestor class objects"""
    ReturnList = []

    if type(object)<>types.InstanceType:
        return ReturnList

    ReturnList.append(object.__class__)
    ReturnList = BaseClasses(object.__class__)

    return ReturnList


#-------------------
# Union of two lists
#-------------------

# Returns a list containing list1 and all items in list 2 that weren't
# already in list 1.

def Union(list1,list2):
    """Returns union of two lists"""
    ReturnList = list1[:]
    for x in list2:
        if not x in ReturnList: ReturnList.append(x)
    return ReturnList


#===========================================================================
#                                   Fundamental Class
#===========================================================================

# The Fundamental Class is intended to supply all classes defined in PAWS
# certain "plumbing" methods and functions that allow us certain liberties
# with the Python programming language.
#
# Certain constraints are built-in Python assumptions. Properties and methods
# have differing syntax, making them impossible to interchange freely. This
# has unfortunate implications, especially for game authors coming from
# TADS.
#
# This class helps alleviate some of the more annoying problems.

class ClassFundamental:
    """Root class of all PAWS classes. Provides additional Python 'plumbing'"""
    
    #---------------------------
    # Make (self) current object
    #---------------------------

    # Because "self" isn't really a variable in the global sense we use
    # this method to explicitly mark which object is "current".
    # Global.CurrentObject will always equal "self" and can safely
    # be used in place of self when creating services that need to
    # refer to self with {} expressions.

    def MakeCurrent(self): Global.CurrentObject = self

    
    #--------------
    # Get Attribute
    #--------------

    # Python has different syntax for returning the value of properties
    # versus the value of methods. Because we want to allow Location and
    # other attributes to be either a property OR a method we had to
    # develop this method.
    #
    # Note, only methods without arguments can be returned by this function.
    # "self" doesn't count as an argument.

    def Get(self,Attribute):
        """Get properties/methods you aren't certain exist."""
        if not hasattr(self,Attribute): return None

        if type(getattr(self,Attribute)) <> type(self.Get):
            return getattr(self,Attribute)
        else:
            return getattr(self,Attribute)()
            
    
    #------------------------
    # Set Instance Properties
    #------------------------

    
    # To make object __init__() functions more generic (because they're
    # involved and somewahat difficult to extend) we created this method
    # to actually define an object's properties when it is instantiated. All
    # you have to do is add the class and instance properties you want to set and
    # the code in this method will automatically run the SetMyProperties() method
    # for each ancestor class, starting with the descendant of ClassFundamental
    # and progressing through the generations until it has run all of them.
    #
    # For example, when this code is run for an object created with ClassRoom
    # it runs the following code automatically.
    #
    # ClassBaseObject.SetMyProperties()
    # ClassBasicThing.SetMyProperties()
    # ClassRoom.SetMyProperties()
    

    def InheritProperties(self):
        """Sets instance properties. Called by __init__()"""
        
        #----------------
        # Get Family Tree
        #----------------

        # The family tree is ordered by most RECENT ancestor first, so we need to
        # reverse the order to make the OLDEST ancestor first. This insures that
        # properties are overridden by descendant classes as they should be.

        Ancestors = ObjectBaseClasses(self)
        Ancestors.reverse()

        
        #------------------------------------
        # Remove Class Fundamental If Present
        #------------------------------------

        # ClassFundamental is the root class of all classes--but not services!
        # That's why we need to check to see if it's present. If so, we remove it
        # so a recursive infinite loop won't occur when this method tried to call
        # itself...

        if ClassFundamental in Ancestors:
            Ancestors.remove(ClassFundamental)

        
        #------------------
        # For Each Class...
        #------------------

        # For each ancestor we try to call SetMyProperties(). If an exception
        # occurs because the ancestor doesn't have SetMyProperties() defined we
        # simply ignore the exception.


        for Ancestor in Ancestors:

            try:
                Ancestor.SetMyProperties(self)
            except:
                pass







#===========================================================================
#                             Global Class
#===========================================================================

# This class defines the Global variables object. The global variables object
# is used to hold all the variables that you want to get to from every part
# of the program (such as the Game State).

class ClassActiveIO(ClassFundamental):
    """Holds ActiveIO variables/methods"""
        
    def __init__(self):
        """Sets default instance properties"""
        self.NamePhrase = "Global Object"
        ClassFundamental.InheritProperties(self)
        
    
    def SetMyProperties(self):
        """Set Terminal's Properties"""

        
        #----------
        # Active IO
        #----------

        # This variable (actually a property, but who's counting?) holds the
        # current IO object, the object used to input and output to the hardware. 
        # This allows for device independence, we can use the default text IO 
        # supplied by Python's raw_input() and print functions, or we can take
        # advantage of GLK or other GUI interfaces. We put this here so that
        # the chosen IO device can attach itself and the save/restore functions
        # will save the parser object properties (particularly vocabulary).

        self.ActiveIO = None
        
        



    def ActiveTerminal(self):
        """Returns ActiveIO.ActiveIO"""
        return self.ActiveIO

#------------------------------
# Instantiate ActiveIO/Terminal
#------------------------------

ActiveIO = ClassActiveIO()
Terminal = ActiveIO.ActiveTerminal()


#=================================================================================
#                             Default IO
#=================================================================================

# This class defines the default IO system used when no advanced GUI system
# is available. This class uses Python's raw_input() and print() functions
# to perform I/O with the player.
#
# It implements a "glass TTY", with the following abilities:
#
# Setting Screen dimensions (but not querying dimensions)
# Track Cursor Position by dead reckoning
# Move cursor to beginning of next line
# Screen Erase by printing # of screenline blanks
# Word Wrap
# Query IO Capabilities
#
# And that's *all*. No bold text, color, cursor control, etc. Literally a glass
# teletype machine.

class ClassDefaultIO(ClassFundamental):
    """Glass Teletype terminal"""
        
    def __init__(self):
        """Sets default instance properties"""
        self.NamePhrase = "Glass TTY"
        ClassFundamental.InheritProperties(self)
        
    
    def SetMyProperties(self):
        """Set I/O Properties"""
        
        #------------------
        # Screen Management
        #------------------

        # The properties here are related to screen management and the Say()
        # function.

        self.MaxScreenLines      = 24
        self.MaxScreenColumns    = 79
        self.CurrentScreenLine   = 0
        self.CurrentScreenColumn = 0
        
        
        #--------------------------
        # I/O Capability Properties
        #--------------------------
        
        self.BackColor = FALSE
        self.Bold = FALSE
        self.CrLf = TRUE
        self.CursorControl = FALSE
        self.Erase = TRUE
        self.Home = FALSE
        self.FontColor = FALSE
        self.FontPitch = FALSE
        self.FontFace = FALSE
        self.Italic = FALSE
        self.Underline = FALSE
        
        
        #---------------------
        # Attribute Properties
        #---------------------

        self.BLACK = 0
        self.BLUE = 0
        self.GREEN = 0
        self.CYAN = 0
        self.RED = 0
        self.MAGENTA = 0
        self.BROWN = 0
        self.LIGHTGRAY = 0
        self.DARKGRAY = 0
        self.LIGHTBLUE = 0
        self.LIGHTGREEN = 0
        self.LIGHTCYAN = 0
        self.LIGHTRED = 0
        self.LIGHTMAGENTA = 0
        self.YELLOW = 0
        self.WHITE = 0
        
        self.A_BOLD = 0
        self.A_UNDERLINE = 0
        self.A_STANDOUT = 0
        self.A_REVERSE = 0
        self.A_DIM = 0
        self.A_NORMAL = 0
        self.A_MORE = 0
        self.A_TITLE = 0
        
    
    
    #-------------------
    # Configure Terminal
    #-------------------
    
    def Configure(self):
        """Configure terminal colors"""
        Say("The Glass TTY can not be configured.")            
    
    #-------------
    # Clear Screen
    #-------------
    
    # This method clears the screen by printing a number of lines equal to the
    # number of screen lines.
    
    def ClearScreen(self):
        """Clear Screen"""
        for I in range(1,self.MaxScreenLines): self.Output(chr(13) + chr(10))
        self.HomeCursor()
        
    
    #---------------------------
    # Display Status Line Method
    #---------------------------
    
    # The Glass TTY doesn't have a status line...
    
    def DisplayStatusLine(self,DisplayString):
        """Display Status Line"""
        pass
        
    
    #------------
    # Home Cursor
    #------------
    
    # In the Glass TTY terminal HomeCursor() doesn't actually move the cursor.
    # Instead it resets the current line/column to 0,0 so that Say() will be 
    # fooled into thinking the screen is blank.

    def HomeCursor(self):
        """Return Cursor To Home Position"""        
        self.MoveCursor(0,0)
        
    
    #---------------
    # Input() method
    #---------------

    # This method returns what the player typed. It's inside a try statement 
    # because if the player typed Ctrl-Z an exception is raised (an error occurs) 
    # and we'll return a two-character string "^Z" to let the parser know that.

    def Input(self,PromptString):
        """Get player input, displaying PromptString."""
       
        try:
            self.NewParagraph()
            InputValue = raw_input(PromptString)

            if Global.Transcribe:
                Global.LogFile.write("\n\n"+PromptString+InputValue+"\n")
                if Global.Debug: Global.DebugFile.write("\n\n"+PromptString+InputValue+"\n")
                
            self.CurrentScreenColumn = 0
            self.CurrentScreenLine = max(self.CurrentScreenLine + 1, self.MaxScreenLines)
            return InputValue
        except:
            self.CurrentScreenColumn = 0
            self.CurrentScreenLine = max(self.CurrentScreenLine + 1, self.MaxScreenLines)            
            return "^Z"
    
    
    #--------------------
    # More Message Method
    #--------------------

    # For the glass TTY the [--More--] message is preceeded by a line break
    # (because of the Input() call). It also performs a "home cursor" which on the
    # glass TTY does nothing but reset the line/column counters to 0.
    
    def MoreMessage(self):
        """Dispays [--More--] Message On Screen for long messages"""
        self.Input("[--more--]")
        self.HomeCursor()
        
    
    #------------
    # Move Cursor
    #------------

    # This method does NOT move the cursor in the Glass TTY terminal, it simply
    # forces the current row/column coordiates to the passed values. This can be
    # very handy in the Say() function.
    
    def MoveCursor(self,Row,Column):
        """Move Cursor"""
        self.CurrentScreenLine = Row
        self.CurrentScreenColumn = Column
            
    
    #---------------
    # Newline Method
    #---------------
    
    def NewLine(self):
        self.Output(chr(13) + chr(10))
        self.CurrentScreenColumn = 0
        self.CurrentScreenLine = min(self.CurrentScreenLine + 1, self.MaxScreenLines)
                
    
    #---------------------
    # New Paragraph Method
    #---------------------

    # Creates a new paragraph by printing two newline characters.
    # This has the effect of ending the current line AND printing
    # a blank line.
    
    def NewParagraph(self):
        self.NewLine()
        self.NewLine()
        
    
    #----------------
    # Output() method
    #----------------

    # This method prints the contents of OutputString to the screen. Notice it
    # does NOT change the cursor coordinates, that will have been handled by Say().

    def Output(self,OutputString,Mode=None):
        """Get player input, displaying PromptString."""
        print OutputString,

        self.CurrentScreenColumn = self.CurrentScreenColumn + len(OutputString) + 1

        if self.CurrentScreenColumn > self.MaxScreenColumns - 1:
            self.CurrentScreenColumn = self.CurrentScreenColumn - self.MaxScreenColumns
            self.CurrentScreenLine = min(self.CurrentScreenLine,self.MaxScreenLines)

    
    #----------------
    # Output() method
    #----------------

    # This method prints the contents of OutputString to the screen. Notice it
    # does NOT change the cursor coordinates, that will have been handled by Say().

    def RawOutput(self,OutputString,Mode=None):
        """Output Text"""
        print OutputString,
        self.CurrentScreenColumn = self.CurrentScreenColumn + len(OutputString)

        if self.CurrentScreenColumn > self.MaxScreenColumns - 1:
            self.CurrentScreenColumn = self.CurrentScreenColumn - self.MaxScreenColumns
            self.CurrentScreenLine = min(self.CurrentScreenLine,self.MaxScreenLines)

    
    #-------------------
    # Terminate() method
    #-------------------

    # The Glass TTY doesn't require special end of session code.
    
    def Terminate(self):
        """End Session"""
        pass

    
ActiveIO.ActiveIO = ClassDefaultIO()


#=================================================================================
#                               Curses Terminal
#=================================================================================


# This class defines a character based terminal that's pretty much universally
# available. It's light-years ahead of the default IO system used when it insn't
# available, but not nearly as advanced as a GUI system, of course.
#
# Curses terminals have the following abilities:
#
# Querying Screen dimensions
# Query cursor position
# Move cursor to beginning of next line
# Homing cursor
# Full cursor control
# Screen Erase
# Screen attributes (bold, inverse video, blinking, etc)
# Independent status line at top of the screen
# Word Wrap
# Query IO Capabilities


class ClassCursesTerminal(ClassFundamental):
    """Curses Terminal"""
    
    #--------------------
    # INITIALIZE TERMINAL
    #--------------------
    
    # This routine is a little more complex than most. It names the terminal,
    # initializes it, creates two windows on the screen (the status line and the 
    # "Pane" (the main window), then makes the background of the status line 
    # reverse video. We make sure the terminal is in buffered mode, can scroll
    # and echos input. We then refresh the screen to reflect window changes and
    # finally call the standard InheritProperties() method.

    
    def __init__(self):
        """Sets default instance properties"""
        self.NamePhrase = "Curses Terminal"
        self.Screen = curses.initscr()
        self.Pane = curses.newwin(24,80,1,0)
        #curses.start_color()
        #curses.keypad(1)
        curses.noraw()
        curses.echo()
        self.StatusLine = curses.newwin(1,80,0,0)
        self.StatusLine.addstr(0,0,string.ljust(" ",79),curses.A_REVERSE)
        self.StatusLine.refresh()
        self.Pane.idlok(1)
        self.Pane.scrollok(1)
        self.Pane.refresh()
        ClassFundamental.InheritProperties(self)

    
    def SetMyProperties(self):
        """Set I/O Properties"""
        
        #------------------
        # Screen Management
        #------------------

        # The properties here are related to screen management and the Say()
        # function.
        self.MaxScreenLines,self.MaxScreenColumns = self.Pane.getmaxyx()
        self.CurrentScreenLine   = 0
        self.CurrentScreenColumn = 0
        
        
        #--------------------------
        # I/O Capability Properties
        #--------------------------
        
        self.BackColor = FALSE
        self.Bold = TRUE
        self.CrLf = TRUE
        self.CursorControl = TRUE
        self.Erase = TRUE
        self.Home = TRUE
        self.FontColor = FALSE
        self.FontPitch = FALSE
        self.FontFace = FALSE
        self.Italic = FALSE
        self.Underline = FALSE

        
        #---------------------
        # Attribute Properties
        #---------------------

        self.BLACK = curses.A_NORMAL
        self.BLUE = curses.A_NORMAL
        self.GREEN = curses.A_NORMAL
        self.CYAN = curses.A_NORMAL
        self.RED = curses.A_NORMAL
        self.MAGENTA = curses.A_NORMAL
        self.BROWN = curses.A_NORMAL
        self.LIGHTGRAY = curses.A_NORMAL
        self.DARKGRAY = curses.A_NORMAL
        self.LIGHTBLUE = curses.A_NORMAL
        self.LIGHTGREEN = curses.A_NORMAL
        self.LIGHTCYAN = curses.A_NORMAL
        self.LIGHTRED = curses.A_NORMAL
        self.LIGHTMAGENTA = curses.A_NORMAL
        self.YELLOW = curses.A_NORMAL
        self.WHITE = curses.A_BOLD
        
        self.A_BOLD = curses.A_BOLD
        self.A_UNDERLINE = curses.A_UNDERLINE
        self.A_STANDOUT = curses.A_BOLD
        self.A_REVERSE = curses.A_REVERSE
        self.A_DIM = curses.A_DIM
        self.A_NORMAL = curses.A_NORMAL
        self.A_MORE = self.A_REVERSE
        self.A_INPUT = curses.A_UNDERLINE + curses.A_BOLD
        self.A_TITLE = self.A_BOLD
        
        
    
    #-------------------
    # Configure Terminal
    #-------------------
    
    def Configure(self):
        """Configure terminal colors"""
        Say("The Curses Terminal can not be configured.")
                    
    
    #-------------
    # Clear Screen
    #-------------
        
    def ClearScreen(self):
        """Clear Screen"""
        self.Pane.erase()
        self.HomeCursor()
        self.Pane.refresh()
    
    #---------------------------
    # Display Status Line Method
    #---------------------------
    
    # Chop off any excess status line length
    
    def DisplayStatusLine(self,DisplayString):
        """Display Status Line"""
        DisplayString = DisplayString[:self.MaxScreenColumns - 1]
        self.StatusLine.addstr(0,0,DisplayString,curses.A_REVERSE)
        self.StatusLine.refresh()

    
    #------------
    # Home Cursor
    #------------
    
    # In the Glass TTY terminal HomeCursor() doesn't actually move the cursor.
    # Instead it resets the current line/column to 0,0 so that Say() will be 
    # fooled into thinking the screen is blank.

    def HomeCursor(self):
        """Return Cursor To Home Position"""        
        self.MoveCursor(0,0)
                
    
    #---------------
    # Input() method
    #---------------

    # This method returns what the player typed. This input method is a lot
    # fancier than the one in the Glass TTY although it does pretty much the 
    # same thing, it looks nicer!

    def Input(self,PromptString):
        """Get player input, displaying PromptString."""
        
        #----------------
        # Paragraph Break
        #----------------

        # This guarantees one blank line between the bottom of the output text and
        # the player's command, making it easier to read.
        
        self.NewParagraph()        
        
        #--------------------
        # Turn on "Blue" Text
        #--------------------
        
        # OK, this one's a cheat. :) In the version of curses available to Python
        # 1.5.2 (Curses 1.2) color really isn't supported. Of course neither is
        # underline--the "underline" is really blue text. Bolding it makes it
        # legible on the black background.
        
        self.Pane.attron(self.A_INPUT)
        self.Pane.refresh()
        
        
        #---------------------------
        # Display The Command Prompt
        #---------------------------        
                                    
        self.Output(PromptString)
        
        
        #-------------------
        # Get Player's Input
        #-------------------

        # The getstr() method echos output (including the CR/LF) back to the 
        # screen just like you'd expect it to.

        InputValue = self.Pane.getstr()

        if Global.Transcribe:
            Global.LogFile.write("\n\n"+PromptString+InputValue+"\n")
            if Global.Debug: Global.DebugFile.write("\n\n"+PromptString+InputValue+"\n")

        
        #---------------------
        # Turn Off "Blue" Text
        #---------------------
        
        self.Pane.attroff(self.A_INPUT)
        
        
        #---------------
        # Refresh Screen
        #---------------
        
        # When using "native" curses functions no output is reflected on the 
        # screen until refresh() is called.
                 
        self.Pane.refresh()
        
        
        #------------------------------
        # Return Player's Typed Command
        #------------------------------
       
        return InputValue
        
    
    
    #--------------------
    # More Message Method
    #--------------------

    # For the curses terminal we save the old cursor position, put [--more--] on
    # the screen in reverse video, and get the player's input (which we ignore).
    # Then we restore the cursor position to the row ABOVE (because it scrolled
    # when the player pressed ENTER) and clear to end of line, and refresh the 
    # pane.
    
    def MoreMessage(self):
        """Dispays [--More--] Message On Screen for long messages"""
        
        OldRow,OldColumn = self.Pane.getyx()
        self.Pane.addstr("[--more--]",self.A_MORE)
        self.Pane.getstr()
        self.MoveCursor(OldRow - 1,OldColumn)
        self.Pane.clrtoeol()         
        self.Pane.refresh()
                
    
    #------------
    # Move Cursor
    #------------

    # This method does NOT move the cursor in the Glass TTY terminal, it simply
    # forces the current row/column coordiates to the passed values. This can be
    # very handy in the Say() function.
    
    def MoveCursor(self,Row,Column):
        """Move Cursor"""
        self.Pane.move(Row,Column)
        self.CurrentScreenLine = Row
        self.CurrentScreenColumn = Column
        self.Pane.refresh()        
            
    
    #---------------
    # Newline Method
    #---------------
    
    def NewLine(self):
        self.Output("\n")
        self.CurrentScreenColumn, self.CurrentScreenLine = self.Pane.getyx()
                
    
    #---------------------
    # New Paragraph Method
    #---------------------

    # Creates a new paragraph by printing two newline characters.
    # This has the effect of ending the current line AND printing
    # a blank line.
    
    def NewParagraph(self):
        self.NewLine()
        self.NewLine()
        
    
    #----------------
    # Output() method
    #----------------

    # This method prints the contents of OutputString to the screen. Notice it
    # does NOT change the cursor coordinates, that will have been handled by Say().

    def Output(self,OutputString,Mode=None):
        """Display OutputString"""
        if Mode is None: Mode = curses.A_NORMAL
        if OutputString <> "\n": OutputString = OutputString + " "

        self.Pane.addstr(OutputString, Mode)
        self.CurrentScreenLine, self.CurrentScreenColumn = self.Pane.getyx()
        
    
    #----------------
    # Output() method
    #----------------

    # This method prints the contents of OutputString to the screen. Notice it
    # does NOT change the cursor coordinates, that will have been handled by Say().

    def RawOutput(self,OutputString,Mode=None):
        """Get player input, displaying PromptString."""
        if Mode is None: Mode = curses.A_NORMAL

        if Mode: 
            self.Pane.addstr(OutputString, Mode)
        else:
            self.Pane.addstr(OutputString)

        self.CurrentScreenLine, self.CurrentScreenColumn = self.Pane.getyx()
    
    
    #-------------------
    # Terminate() method
    #-------------------

    # The Curses terminal requires an endwin() function call to release resources.
    
    def Terminate(self):
        """End Session"""
        curses.endwin()
        
        

#=================================================================================
#                               WConio Terminal
#=================================================================================


# This class defines a character based terminal that's available for Windows 32-bit
# platforms (Windows 95 and later). It's better than the Curses terminal because
# it supports color as well as the other Curses functionality--at least in the
# Win9x/NT environment. It isn't available for other platforms.
#
# WConio terminals have the following abilities:
#
# Querying Screen dimensions
# Query cursor position
# Move cursor to beginning of next line
# Homing cursor
# Full cursor control
# Screen Erase
# Screen attributes (bold, inverse video, etc. Blinking is NOT supported)
# Screen Color (16 color foreground/16 color background)
# Independent status line at top of the screen
# Word Wrap
# Query IO Capabilities


class ClassWConioTerminal(ClassFundamental):
    """WConio Terminal"""
    
    #--------------------
    # INITIALIZE TERMINAL
    #--------------------
    
    # This routine is a little more complex than most. It names the terminal,
    # initializes it, creates two windows on the screen (the status line and the 
    # "Pane" (the main window), then makes the background of the status line 
    # reverse video. We make sure the terminal is in buffered mode, can scroll
    # and echos input. We then refresh the screen to reflect window changes and
    # finally call the standard InheritProperties() method.

    
    def __init__(self):
        """Sets default instance properties"""
        self.NamePhrase = "WConio Terminal"
        ClassFundamental.InheritProperties(self)
        WConio.textmode()
    
    def SetMyProperties(self):
        """Set I/O Properties"""
        
        #------------------
        # Screen Management
        #------------------

        # The properties here are related to screen management and the Say()
        # function.

        self.MaxScreenLines = WConio.gettextinfo()[7] - 1
        self.MaxScreenColumns = WConio.gettextinfo()[8] - 1
        self.CurrentScreenLine   = 0
        self.CurrentScreenColumn = 0

        
        #--------------------------
        # I/O Capability Properties
        #--------------------------
        
        self.BackColor = TRUE
        self.Bold = TRUE
        self.CrLf = TRUE
        self.CursorControl = TRUE
        self.Erase = TRUE
        self.Home = TRUE
        self.FontColor = TRUE
        self.FontPitch = FALSE
        self.FontFace = FALSE
        self.Italic = FALSE
        self.Underline = FALSE
        
        
        #---------------------
        # Attribute Properties
        #---------------------

        self.BLACK = WConio.BLACK
        self.BLUE = WConio.BLUE
        self.GREEN = WConio.GREEN
        self.CYAN = WConio.CYAN
        self.RED = WConio.RED
        self.MAGENTA = WConio.MAGENTA
        self.BROWN = WConio.BROWN
        self.LIGHTGRAY = WConio.LIGHTGRAY
        self.DARKGRAY = WConio.DARKGRAY
        self.LIGHTBLUE = WConio.LIGHTBLUE
        self.LIGHTGREEN = WConio.LIGHTGREEN
        self.LIGHTCYAN = WConio.LIGHTCYAN
        self.LIGHTRED = WConio.LIGHTRED
        self.LIGHTMAGENTA = WConio.LIGHTMAGENTA
        self.YELLOW = WConio.YELLOW
        self.WHITE = WConio.WHITE
        
        self.A_BOLD = self.WHITE              # Text isn't shifted
        self.A_UNDERLINE = self.LIGHTBLUE     # Text isn't shifted
        self.A_STANDOUT = self.YELLOW         # Text isn't shifted
        self.A_REVERSE = (self.MAGENTA << 4) + self.YELLOW
        self.A_DIM = self.LIGHTGRAY           # Text isn't shifted
        self.A_NORMAL = self.GREEN            # Text isn't shifted
        self.A_MORE = self.LIGHTGRAY << 4     # Background is shifted 4 bits
        self.A_INPUT = self.LIGHTBLUE         # Text isn't Shifted 
        self.A_TITLE = self.A_BOLD       
        
        
    
    #-------------------
    # Configure Terminal
    #-------------------
    
    def Configure(self):
        """Configure terminal colors"""
        self.ClearScreen()        

        AttrList = [["Bold (Text,Background)? ","", self.A_BOLD],
                    ["Dim (Text,Background)? ","",self.A_DIM],
                    ["Input (Text,Background)? ","",self.A_INPUT],
                    ["More (Text,Background)? ","",self.A_MORE],
                    ["Normal (Text,Background)? ","",self.A_NORMAL],
                    ["Reverse (Text,Background)? ","",self.A_REVERSE],
                    ["Standout (Text,Background)? ","",self.A_STANDOUT],
                    ["Underline (Text,Background)? ","",self.A_UNDERLINE]]
                    

        ColorPair = [2,0]

        self.Output("Configure Screen Colors:")
        
        for I in range(0,8):
            self.MoveCursor(I+2,0);self.Output(repr(I)+".",self.A_NORMAL)
            if I == 0:
                self.MoveCursor(I+2,3);self.Output("Color Of Text",7<<4)
            else:
                self.MoveCursor(I+2,3);self.Output("Color Of Text",I)

            self.MoveCursor(I+2,35);self.Output(string.rjust(repr(I+8),2)+".",self.A_NORMAL)
            self.MoveCursor(I+2,39);self.Output("Color Of Text",I+8)

        for I in range(0,8):
            self.MoveCursor(I+11,0)
            self.Output(AttrList[I][0],AttrList[I][2])
            AttrList[I][1] = WConio.cgets(10)
            List = string.split(AttrList[I][1],",")
            
            try:
                ColorPair[0] = string.atoi(List[0])
                ColorPair[1] = string.atoi(List[1])
                Attr = (ColorPair[1] << 4) + ColorPair[0]
            except:
                Attr = AttrList[I][2]
            
            if Attr == 0: Attr = 7
            
            AttrList[I][2] = Attr

        self.A_BOLD      = AttrList[0][2]
        self.A_DIM       = AttrList[1][2]
        self.A_INPUT     = AttrList[2][2]
        self.A_MORE      = AttrList[3][2]
        self.A_NORMAL    = AttrList[4][2]
        self.A_REVERSE   = AttrList[5][2]
        self.A_STANDOUT  = AttrList[6][2]
        self.A_UNDERLINE = AttrList[7][2]

        self.ClearScreen()
                    
    
    #-------------
    # Clear Screen
    #-------------
        
    def ClearScreen(self):
        """Clear Screen"""
        WConio.textattr(Terminal.A_NORMAL)
        WConio.clrscr()

    
    #---------------------------
    # Display Status Line Method
    #---------------------------
    
    # Chop off any excess status line length
    
    def DisplayStatusLine(self,DisplayString):
        """Display Status Line"""
        DisplayString = string.rjust(DisplayString[:self.MaxScreenColumns],self.MaxScreenColumns)
        OldRow = WConio.wherey()
        OldColumn = WConio.wherex()
        
        self.MoveCursor(0,0)
        WConio.textattr(self.A_REVERSE)
        WConio.cputs(DisplayString)
        self.MoveCursor(OldRow,OldColumn)
        WConio.textattr(self.A_NORMAL)

    
    #------------
    # Home Cursor
    #------------
    
    # In the Glass TTY terminal HomeCursor() doesn't actually move the cursor.
    # Instead it resets the current line/column to 0,0 so that Say() will be 
    # fooled into thinking the screen is blank.

    def HomeCursor(self):
        """Return Cursor To Home Position"""        
        self.MoveCursor(0,0)
                
    
    #---------------
    # Input() method
    #---------------

    # This method returns what the player typed. This input method is a lot
    # fancier than the one in the Glass TTY although it does pretty much the 
    # same thing, it looks nicer!

    def Input(self,PromptString):
        """Get player input, displaying PromptString."""
        
        #----------------
        # Paragraph Break
        #----------------

        # This guarantees one blank line between the bottom of the output text and
        # the player's command, making it easier to read.
        
        self.NewParagraph()
                
        
        #--------------------
        # Display Status Line
        #--------------------

        # Unlike Curses, WConio doesn't support multiple windows. Because of this
        # we have to display the status line just before the player types their
        # input so it's visible.

        self.DisplayStatusLine(Global.StatusLine)

        
        #---------------------------
        # Display The Command Prompt
        #---------------------------        
      
        self.Output(PromptString, self.A_INPUT)

        
        #-------------------------
        # Turn on Highlighted Text
        #-------------------------
        
        # OK, this one's a cheat. :) In the version of curses available to Python
        # 1.5.2 (Curses 1.2) color really isn't supported. Of course neither is
        # underline--the "underline" is really blue text. Bolding it makes it
        # legible on the black background.
        
        WConio.textattr(self.A_INPUT)
                
        
        #-------------------
        # Get Player's Input
        #-------------------

        # The getstr() method echos output (including the CR/LF) back to the 
        # screen just like you'd expect it to.

        InputValue = ""
        
        while len(InputValue)==0:
            try:
                InputValue = WConio.cgets(self.MaxScreenColumns - len(PromptString) - 1)

                if Global.Transcribe:
                    Global.LogFile.write("\n\n"+PromptString+InputValue+"\n")
                    if Global.Debug: Global.DebugFile.write("\n\n"+PromptString+InputValue+"\n")

            except:
                pass
                        
        
        #--------------
        # Force Newline
        #--------------

        # Unlike the Glass TTY and the Curses terminal, WConio's input function
        # doesn't echo the CR/LF. To keep the spacing consistant we have to 
        # force a new line to simulate what the other two terminals do.
         
        self.NewLine()

        
        #---------------------
        # Turn Off "Blue" Text
        #---------------------
        
        WConio.textattr(self.A_NORMAL)
        
        
        
        #------------------------------
        # Return Player's Typed Command
        #------------------------------
       
        return InputValue
        
    
    
    #--------------------
    # More Message Method
    #--------------------

    # For the curses terminal we save the old cursor position, put [--more--] on
    # the screen in reverse video, and get the player's input (which we ignore).
    # Then we restore the cursor position to the row ABOVE (because it scrolled
    # when the player pressed ENTER) and clear to end of line, and refresh the 
    # pane.
    
    def MoreMessage(self):
        """Dispays [--More--] Message On Screen for long messages"""
        
        OldRow = WConio.wherey()
        OldColumn = WConio.wherex()
        WConio.textattr(self.A_MORE)
        WConio.cputs("[--more--]")
        WConio.textattr(self.A_NORMAL)
        WConio.getch()
        self.MoveCursor(OldRow,OldColumn)
        WConio.clreol()         
        
    
    #------------
    # Move Cursor
    #------------

    # This method does NOT move the cursor in the Glass TTY terminal, it simply
    # forces the current row/column coordiates to the passed values. This can be
    # very handy in the Say() function.
    
    def MoveCursor(self,Row,Column):
        """Move Cursor"""
        WConio.gotoxy(Column,Row)
        self.CurrentScreenLine = Row
        self.CurrentScreenColumn = Column
            
    
    #---------------
    # Newline Method
    #---------------
    
    def NewLine(self):
        self.Output("\n")
        self.CurrentScreenColumn = WConio.wherey()
        self.CurrentScreenLine = WConio.wherex()
        
    
    #---------------------
    # New Paragraph Method
    #---------------------

    # Creates a new paragraph by printing two newline characters.
    # This has the effect of ending the current line AND printing
    # a blank line.
    
    def NewParagraph(self):
        self.NewLine()
        self.NewLine()
        
    
    #----------------
    # Output() method
    #----------------

    # This method prints the contents of OutputString to the screen. Notice it
    # does NOT change the cursor coordinates, that will have been handled by Say().

    def Output(self,OutputString,Mode=None):
        """Get player input, displaying PromptString."""
        if Mode is None: Mode = self.A_NORMAL
        if OutputString <> "\n": OutputString = OutputString + " "
        WConio.textattr(Mode)
        WConio.cputs(OutputString)        
        WConio.textattr(self.A_NORMAL)
        self.CurrentScreenLine = WConio.wherey()
        self.CurrentScreenColumn = WConio.wherex()

    
    #--------------------
    # Raw Output() method
    #--------------------

    # This method prints the contents of OutputString to the screen. Notice it
    # does NOT change the cursor coordinates, that will have been handled by Say().

    def RawOutput(self,OutputString,Mode=None):
        """Get player input, displaying PromptString."""
        if Mode: WConio.textattr(Mode)
        WConio.cputs(OutputString)        
        self.CurrentScreenLine = WConio.wherey()
        self.CurrentScreenColumn = WConio.wherex()

    
    #-------------------
    # Terminate() method
    #-------------------

    # The WConio terminal doesn't need any special ending code.
    
    def Terminate(self):
        """End Session"""
        pass
        

#=================================================================================
#                               Tkinter Terminal
#=================================================================================

# This is a Tkinter based GUI terminal capable of lights, colors, bells
# and whistles...at least, once those features are implemented.
#
# Tkinter terminals have (or will have) the following abilities:
#
# Querying Screen dimensions
# Query cursor position
# Move cursor to beginning of next line
# Homing cursor
# Full cursor control
# Screen Erase
# Screen attributes (bold, inverse video, etc. Blinking is omitted on ethical grounds)
# Screen Color (16 color foreground/16 color background)
# Independent status line at top of the screen
# Word Wrap
# Query IO Capabilities

class ClassTkinterTerminal(ClassFundamental):
    """Tkinter Terminal"""
    
    #--------------------
    # INITIALIZE TERMINAL
    #--------------------
    
    def __init__(self):
        """Sets default instance properties"""
        self.NamePhrase = "Tkinter Terminal"
        ClassFundamental.InheritProperties(self)
        self.StartTk()
        self.SetMyProperties()
    

    def SetMyProperties(self):
        """Set I/O Properties"""
        
        #------------------
        # Screen Management
        #------------------

        # These values are a bit arbitrary for the Tkinter interface.
        # Potentially, the user could resize the screen and make them
        # different.  For now, they are stuck with the defaults.

        self.MaxScreenLines      = 23
        self.MaxScreenColumns    = 79
        self.CurrentScreenLine   = 0
        self.CurrentScreenColumn = 0

        
        #--------------------------
        # I/O Capability Properties
        #--------------------------
        
        self.BackColor = TRUE
        self.Bold = TRUE
        self.CrLf = TRUE
        self.CursorControl = TRUE
        self.Erase = TRUE
        self.Home = TRUE
        self.FontColor = TRUE
        self.FontPitch = TRUE
        self.FontFace = TRUE
        self.Italic = TRUE
        self.Underline = TRUE
        
        
        #---------------------
        # Attribute Properties
        #---------------------

        # The mode contains a four byte value, expanding on the WConio-style
        # mode setting.  This allows the TkinterTerminal to integrate
        # properly with the PAWS engine while still providing a bit more
        # functionality than the WConio terminal (i.e. italic and bold text).

        # To provide more functionality in the future, it may be necessary
        # to eclipse PAWS.say() with a more specific say() function in this
        # class.

        # The bytes are laid out like this, with each byte containing two
        # values:
        # 
        #     # #  # #
        #     | |  | |
        #     | |  | forefround color
        #     | |  background color
        #     | style (bold, italic, etc.)
        #     font (helvetica, console, etc. - not implemented yet)

        self.BLACK        = 0x00
        self.BLUE         = 0x01
        self.GREEN        = 0x02
        self.CYAN         = 0x03
        self.RED          = 0x04
        self.MAGENTA      = 0x05
        self.BROWN        = 0x06
        self.LIGHTGRAY    = 0x07
        self.DARKGRAY     = 0x08
        self.LIGHTBLUE    = 0x09
        self.LIGHTGREEN   = 0x0a
        self.LIGHTCYAN    = 0x0b
        self.LIGHTRED     = 0x0c
        self.LIGHTMAGENTA = 0x0d
        self.YELLOW       = 0x0e
        self.WHITE        = 0x0f

        self.A_BOLD      = 0x100
        self.A_UNDERLINE = 0x200
        self.A_STANDOUT  = 0x300
        self.A_REVERSE   = 0x400
        self.A_TITLE     = 0x500        

        self.A_DIM       = self.LIGHTGRAY
        self.A_NORMAL    = self.GREEN | (self.BLACK << 4)
        self.A_MORE      = self.LIGHTGRAY
        self.A_INPUT     = self.LIGHTBLUE

        self.Pane.tag_config('foreground0',  foreground='black')
        self.Pane.tag_config('foreground1',  foreground='blue')
        self.Pane.tag_config('foreground2',  foreground='green')
        self.Pane.tag_config('foreground3',  foreground='cyan')
        self.Pane.tag_config('foreground4',  foreground='red')
        self.Pane.tag_config('foreground5',  foreground='magenta')
        self.Pane.tag_config('foreground6',  foreground='brown')
        self.Pane.tag_config('foreground7',  foreground='lightgray')
        self.Pane.tag_config('foreground8',  foreground='darkgray')
        self.Pane.tag_config('foreground9',  foreground='lightblue')
        self.Pane.tag_config('foregrounda',  foreground='lightgreen')
        self.Pane.tag_config('foregroundb',  foreground='lightcyan')
        self.Pane.tag_config('foregroundc',  foreground='pink') # light red
        self.Pane.tag_config('foregroundd',  foreground='#FFB8B7FFF') # light magenta
        self.Pane.tag_config('foregrounde',  foreground='yellow')
        self.Pane.tag_config('foregroundf',  foreground='white')

        self.Pane.tag_config('background0',  background='black')
        self.Pane.tag_config('background1',  background='blue')
        self.Pane.tag_config('background2',  background='green')
        self.Pane.tag_config('background3',  background='cyan')
        self.Pane.tag_config('background4',  background='red')
        self.Pane.tag_config('background5',  background='magenta')
        self.Pane.tag_config('background6',  background='brown')
        self.Pane.tag_config('background7',  background='lightgray')
        self.Pane.tag_config('background8',  background='darkgray')
        self.Pane.tag_config('background9',  background='lightblue')
        self.Pane.tag_config('backgrounda',  background='lightgreen')
        self.Pane.tag_config('backgroundb',  background='lightcyan')
        self.Pane.tag_config('backgroundc',  background='pink') # light red
        self.Pane.tag_config('backgroundd',  background='#FFB8B7FFF') # light magenta
        self.Pane.tag_config('backgrounde',  background='yellow')
        self.Pane.tag_config('backgroundf',  background='white')


        # For now, the styles must explicitly set the foreground and background
        # colors.  This is because the PAWS.Say() function sets the Mode equal
        # to the style rather than merging it onto the current mode, thus setting
        # the color set to the contents of the style's color byte rather than
        # just setting the style portion of the formatting byte.  It would
        # be necessary to override the default Say() to change this and it is
        # simpler to just do it this way.  On the down side, this means you
        # cannot produce underlined blue text, for example.

        self.Pane.tag_config('style100',font=(
                                            self.Pane.DefaultFontFamily,
                                            self.Pane.DefaultFontSize,
                                            'bold',
                                            self.Pane.DefaultFontSlant),
                                        foreground='green')      # bold

        self.Pane.tag_config('style200',underline=1,foreground='green')           # underline

        self.Pane.tag_config('style300',font=(
                                            self.Pane.DefaultFontFamily,
                                            self.Pane.DefaultFontSize,
                                            self.Pane.DefaultFontStyle,
                                            'italic'),
                                        foreground='green')   # standout

        self.Pane.tag_config('style400',foreground='black', background='green')   # reverse

        self.Pane.tag_config('style500',font=(
                                            'Helvetica',
                                            str(int(self.Pane.DefaultFontSize) + 4),
                                            'bold',
                                            self.Pane.DefaultFontSlant),
                                        foreground='white')      # Title
        

    # This starts the Tk process, initiating a thread to handle the main loop.
        
    def StartTk(self):
        self.mw = Tkinter.Tk()

        frame = Tkinter.Frame(self.mw)
        frame.pack(side=Tkinter.TOP, expand=Tkinter.YES, fill=Tkinter.BOTH)

        self.Status  = TkinterIOStatusBar(frame)
        self.Pane    = TkinterIOScrolledROText(frame)
        self.Reader  = TkinterIOSimpleReader(frame, self.Pane)
        self.TkinterIOMenuBar = TkinterIOMenuBar(self.mw, self.Status, self.Pane, self.Reader)

        self.Reader.entry.focus_force()

        thread.start_new_thread(self.mw.mainloop,())

    
    #-------------
    # Clear Screen
    #-------------

    # Maybe this should just scroll the visible screen down until it is blank
    # rather than clearing the whole text buffer.
        
    def ClearScreen(self):
        """Clear Screen"""
        self.Pane.Clear()

    
    #---------------------------
    # Display Status Line Method
    #---------------------------
    
    def DisplayStatusLine(self,DisplayString):
        """Display Status Line"""
        self.Status.SetStatus(DisplayString)

    
    #------------
    # Home Cursor
    #------------

    def HomeCursor(self):
        """Return Cursor To Home Position"""        
        self.Pane.mark_set('insert','%d.0' % RelativeTop(self))
                
    
    #---------------
    # Input() method
    #---------------

    def Input(self,PromptString):
        """Get player input."""
        
        #---------------------------
        # Display The Command Prompt
        #---------------------------        

        # Leave the prompt out for now, as it complicates input retrieval.
        # Save this for the future.
        self.Pane.RawOutput("\n\n" + PromptString)
        
        #-------------------
        # Get Player's Input
        #-------------------

        InputValue = self.Reader.RawInput()


        #---------------------------------------------
        # Echo the player's command in the Output pane
        #---------------------------------------------

        self.Pane.RawOutput(" " + InputValue + "\n\n")

        if Global.Transcribe:
            Global.LogFile.write("\n\n"+PromptString+InputValue+"\n")
            if Global.Debug: Global.DebugFile.write("\n\n"+PromptString+InputValue+"\n")

        if Global.Debug:
            Global.DebugFile.write("\n\n",PromptString+InputValue+"\n")
        
        #------------------------------
        # Return Player's Typed Command
        #------------------------------
       
        return InputValue
    
    #--------------------
    # More Message Method
    #--------------------

    def MoreMessage(self):
        """
        Insert a 'more' message, wait for '<Return>', then
        erase the 'more' message.
        """

        start_mark = self.Pane.index('insert')
        self.Output("--more--", self.A_MORE)
        end_mark = self.Pane.index('insert')
        self.Reader.ready = 0
        self.Reader.entry.delete(0,'end')
        while self.Reader.ready == 0:
            time.sleep(0.1)
        self.Pane.text.config(state=Tkinter.NORMAL)
        self.Pane.text.delete(start_mark,end_mark)
        self.Pane.text.config(state=Tkinter.DISABLED)
        self.Reader.entry.delete(0,'end')
        self.Reader.ready = 0

        
    
    #------------
    # Move Cursor
    #------------

    def MoveCursor(self,Row,Column):
        """Move Cursor"""
        self.Pane.mark_set('insert','%d.%d' % (Row,self.RelativeTop() + Column))
        self.CurrentScreenLine, self.CurrentScreenColumn = self.GetYX()
            
    
    #---------------
    # Newline Method
    #---------------
    
    def NewLine(self):
        self.Pane.RawOutput("\n")
        self.CurrentScreenLine, self.CurrentScreenColumn = self.GetYX()
        
    
    #---------------------
    # New Paragraph Method
    #---------------------

    # Creates a new paragraph by printing two newline characters.
    # This has the effect of ending the current line AND printing
    # a blank line.
    
    def NewParagraph(self):
        self.NewLine()
        self.NewLine()
        
    
    #----------------
    # Output() method
    #----------------

    # This method prints the contents of OutputString to the screen. Notice it
    # does NOT change the cursor coordinates, that will have been handled by Say().

    # The color and style settings are handled with Text widget tags.  The method
    # used here produces at least one tag for each word of a non-standard region.
    # This may have an effect on the memory or processor time used by the program.

    # Creating multiple-effect tags and extending existing tags to cover entire
    # regions rather than a separate tag for each word of a region may or may
    # not be beneficial, depending on how tags are handled in the Text widget.

    def Output(self,OutputString,Mode=None):
        """Display Output string to the Pane"""
        if Mode is None: Mode = self.A_NORMAL

        tag_start = self.Pane.index('insert')
        self.Pane.RawOutput(OutputString)
        tag_end   = self.Pane.index('insert')

        foreground =  Mode & 0x000f
        background = (Mode & 0x00f0) >> 4
        style      = (Mode & 0x0f00)
        font       = (Mode & 0xf000)

        if foreground != 0x02:
            self.Pane.tag_add('foreground%x'%(foreground),tag_start,tag_end)
        if background != 0x00:
            self.Pane.tag_add('background%x'%(background),tag_start,tag_end)
        if style != 0x00:
            self.Pane.tag_add('style%x'%(style),tag_start,tag_end)
        # Font is not implemented yet.

        if OutputString <> "\n": self.Pane.RawOutput(" ")

        self.CurrentScreenLine, self.CurrentScreenColumn = self.GetYX()


    #---------------
    # GetYX() method
    #---------------

    # This gets the absolute cursor position from the Pane, then translates
    # it into a position relative to the last screen-length lines in order
    # to emulate a terminal that lacks scrolling.

    def GetYX(self):
        y,x = self.Pane.GetYX()

        relative_y = y - self.RelativeTop()

        return y,x


    def RelativeTop(self):
        """Return the top of the 'screen' relative to the actual text buffer."""

        y,x = self.Pane.GetYX()
        last_y, last_x = string.split(self.Pane.text.index('end'),'.')
        last_y = int(last_y)
        relative_top = last_y - self.MaxScreenLines
        if relative_top < 0: relative_top = 0

        return relative_top


    def Terminate(self):
        """Close up the Tkinter widgets."""
        self.Pane.RawOutput("\n")
        self.MoreMessage()



################################
# Custom Widgets for TkinterIO #
################################


#------------------------
# TkinterIOMenuBar Widget
#------------------------

# The TkinterIOMenuBar handles the menus at the top of the screen and the
# functions tied to the various menu options.

class TkinterIOMenuBar:
    def __init__(self, mw, status, pane, reader):
        top  = Tkinter.Menu(mw)
        mw.config(menu=top)

        self.mw = mw
        self.Status = status
        self.Pane = pane
        self.Reader = reader

        game = Tkinter.Menu(top)
        game.add_command(label='Quit', command=self.QuitCallback, underline=0)
        top.add_cascade(label='Game', menu=game, underline=0)

        view = Tkinter.Menu(top)
#       view.add_command(label='Rotate Font', command=self.RotateFont, underline=0)
        view.add_command(label='Increase Font Size', command=self.IncreaseFontSize, underline=0)
        view.add_command(label='Decrease Font Size', command=self.DecreaseFontSize, underline=0)
        top.add_cascade(label='View', menu=view, underline=0)

        help = Tkinter.Menu(top)
        help.add_command(label='About PAWS', command=self.AboutPopup, underline=0)
        top.add_cascade(label='Help', menu=help, underline=0)


    def RotateFont(self):
        """Switch the font used in the Pane."""

        family = self.Pane.DefaultFontFamily
        if   family == 'Courier'  : self.Pane.DefaultFontFamily = 'Helvetica'
        elif family == 'Helvetica': self.Pane.DefaultFontFamily = 'Roman'
        elif family == 'Roman'    : self.Pane.DefaultFontFamily = 'Courier'
        print self.Pane.DefaultFontFamily
        self.UpdateScreenFonts()


    def IncreaseFontSize(self):
        """Increase the size of the standard font."""

        self.Pane.DefaultFontSize = str(int(self.Pane.DefaultFontSize) + 2)
        self.UpdateScreenFonts()


    def DecreaseFontSize(self):
        """Decrease the size of the standard font."""

        if int(self.Pane.DefaultFontSize) < 6: return

        self.Pane.DefaultFontSize = str(int(self.Pane.DefaultFontSize) - 2)
        self.UpdateScreenFonts()


    def UpdateScreenFonts(self):
        """Activate changes made to the default font sets."""

        self.Pane.text.config(font=(
                                self.Pane.DefaultFontFamily,
                                self.Pane.DefaultFontSize,
                                self.Pane.DefaultFontStyle,
                                self.Pane.DefaultFontSlant))

        self.Pane.tag_config('style100',font=(
                                            self.Pane.DefaultFontFamily,
                                            self.Pane.DefaultFontSize,
                                            'bold',
                                            self.Pane.DefaultFontSlant),
                                        foreground='green')      # bold

        self.Pane.tag_config('style300',font=(
                                            self.Pane.DefaultFontFamily,
                                            self.Pane.DefaultFontSize,
                                            self.Pane.DefaultFontStyle,
                                            'italic'),
                                        foreground='green')   # standout

        self.Pane.tag_config('style500',font=(
                                            'Helvetica',
                                            str(int(self.Pane.DefaultFontSize) + 4),
                                            'bold',
                                            self.Pane.DefaultFontSlant),
                                        foreground='white')      # Title

    def AboutPopup(self):
        tkMessageBox.showinfo(
            "About PAWS",
            """
            PAWS
            The Python Adventure Writing System is an interactive fiction authoring system produced by Roger Plowman.  Check the web page (http://w3.one.net/~wolf/PAWS.shtml) for updates and information.
            """)


    def QuitCallback(self):
        """Cause the game to quit via the normal channels."""

        self.Reader.Feed('quit')


#--------------------------
# TkinterIOStatusBar Widget
#--------------------------

# This handles the game's status display.  It is basically a read only Entry
# widget with a groove border.

class TkinterIOStatusBar(Tkinter.Entry):
    def __init__(self, parent=None):
        Tkinter.Entry.__init__(self,parent)
        self.config(
            state=Tkinter.DISABLED, relief=Tkinter.GROOVE, 
            cursor='arrow', font=('Courier','12','bold','roman'))
        self.pack(side=Tkinter.TOP, expand=Tkinter.NO, fill=Tkinter.X)

    def SetStatus(self, status):
        self.config(state=Tkinter.NORMAL)
        self.delete(0,Tkinter.END)
        self.insert(Tkinter.END, status)
        self.config(state=Tkinter.DISABLED)


#-----------------------------------------------------------
# TkinterIOScrolledROText - A Scrolled Read Only Text Widget
#-----------------------------------------------------------

# The text component's state is set to 'DISABLED' except when
# the class is writing to it.  This prevents the user from
# modifying the text area with the keyboard or the mouse
# (by pasting).

class TkinterIOScrolledROText(Tkinter.Frame):

    def __init__(self, parent):
        Tkinter.Frame.__init__(self,parent)
        self.pack(expand=Tkinter.YES, fill=Tkinter.BOTH)
        self.SetFonts()
        self.MakeWidgets()

    def SetFonts(self):
        self.DefaultFontFamily = 'Courier'
        self.DefaultFontSize   = '12'
        self.DefaultFontStyle  = 'normal'
        self.DefaultFontSlant  = 'roman'

    def MakeWidgets(self):
        sbar = Tkinter.Scrollbar(self)
        text = Tkinter.Text(self, wrap='none', relief=Tkinter.SUNKEN)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        text.pack(side=Tkinter.LEFT, expand=Tkinter.YES, fill=Tkinter.BOTH)
        text.config(foreground='green',background='black',
                    font=(
                        self.DefaultFontFamily, 
                        self.DefaultFontSize, 
                        self.DefaultFontStyle, 
                        self.DefaultFontSlant),
                    cursor='arrow')
        text.config(state=Tkinter.DISABLED)
        self.text = text
        self.mark_set = text.mark_set
        self.index = text.index
        self.insert = text.insert
        self.tag_config = text.tag_config
        self.tag_add = text.tag_add

    def Clear(self):
        self.text.config(state=Tkinter.NORMAL)
        self.text.delete('1.0', Tkinter.END)
        self.text.config(state=Tkinter.DISABLED)

    def RawOutput(self, text):
        self.text.config(state=Tkinter.NORMAL)
        self.text.insert('insert', text)
        self.text.see(self.text.index(Tkinter.END))
        self.text.config(state=Tkinter.DISABLED)

    def GetYX(self):
        """Return the row and column of the cursor in the Pane"""

        y,x = string.split(self.text.index('insert'),'.')
        return (int(y), int(x))


#-----------------------------------
# TkinterIOSimpleReader Input Widget
#-----------------------------------

# This is an Entry widget that is capable of returning its contents
# in a non-event-driven manner.

# It also supports command history and some readline key bindings.

# ctrl-f           -> forward 1 char
# ctrl-b           -> back 1 char
# ctrl-u           -> clear to start of line
# ctrl-k or ctrl-y -> clear to end of line
# ctrl-p           -> previous item in history
# ctrl-n           -> next item in history

class TkinterIOSimpleReader(Tkinter.Frame):

    def __init__(self, parent, pane):
        Tkinter.Frame.__init__(self,parent)
        self.parent = parent
        self.Pane = pane
        self.pack(expand=Tkinter.NO, fill=Tkinter.X)
        self.MakeWidgets()
        self.ready = 0
        self.contents = ''
        self.history = []
        self.history_pos = 0


    def MakeWidgets(self):
        entry = Tkinter.Entry(self, relief=Tkinter.SUNKEN)
        entry.pack(side=Tkinter.LEFT, expand=Tkinter.YES, fill=Tkinter.BOTH)
        self.entry = entry
        entry.bind('<Return>', self.Fetch)
        entry.bind('<Up>', self.HistoryPrev)
        entry.bind('<Control-p>', self.HistoryPrev)
        entry.bind('<Down>', self.HistoryNext)
        entry.bind('<Control-n>', self.HistoryNext)
        entry.bind('<Control-w>', self.DeletePrevWord)
        entry.bind('<Control-u>', self.DeleteToStart)
        entry.bind('<Control-y>', self.DeleteToEnd)
        entry.bind('<Prior>', self.ScreenUp)
        entry.bind('<Next>', self.ScreenDown)


    # This is sort of a dirty trick, but it will allow the program to
    # get information from the Tk interface without re-writing PAWS to
    # be Tk event-driven.
    #
    # The PAWS thread will pause here until input is available (enter has
    # been pressed) from the input object.  It will poll every tenth of a
    # second to see if new input is ready.  This should be a high enough 
    # rate to provide good responsiveness, but still low enough not to
    # occupy much processor time.
    #
    # The ready flag starts at 0.  When the input object recieves the 
    # enter key, it sets the ready flag to 1.  The class's input function
    # will wait until the ready flag is 1, then it will take the contents
    # of the entry field, clear the entry field, and set the ready flag
    # back to 0.
    #
    # The prompt is echoed to the Pane, but is not displayed in the
    # Input widget.

    def RawInput(self, prompt=''):
        self.entry.delete(0,Tkinter.END)

        while self.ready == 0:
            time.sleep(0.1)

        self.ready = 0

        if self.contents != '':
            return self.contents


    def Fetch(self, event):
        self.contents = self.entry.get()
        self.history.append(self.contents)
        if self.contents != '':
            self.history_pos = len(self.history)
        self.ready = 1


    def Feed(self, command):
        """Enter a command into the reader and execute it."""

        self.contents = command
        self.ready = 1


    # These callback methods power the command history and line editing 
    # features of the class.
    # 'event' is ignored, but must be present.

    def HistoryPrev(self, event):
        """Retrieve the previous history entry into the entry widget."""

        if self.history_pos == 0:
            return

        self.history_pos = self.history_pos - 1
        self.entry.delete(0,'end')
        self.entry.insert(0,self.history[self.history_pos])


    def HistoryNext(self, event):
        """Retrieve the next history entry into the entry widget."""

        if self.history_pos >= len(self.history) - 1:
            return

        self.history_pos = self.history_pos + 1
        self.entry.delete(0,'end')
        self.entry.insert(0,self.history[self.history_pos])


    def DeletePrevWord(self, event):
        """Delete the previous word in the entry widget."""

        pos = self.entry.index('insert')
        contents = self.entry.get()
        pos = pos - 1
        while pos > 0 and contents[pos] != ' ':
            pos = pos - 1
        self.entry.delete(pos,'insert')


    def DeleteToStart(self, event):
        """Delete all text from 'insert' to the start of the entry widget."""

        self.entry.delete(0,'insert')


    def DeleteToEnd(self, event):
        """Delete all text from 'insert' to the end of the entry widget."""

        self.entry.delete('insert','end')


    def ScreenUp(self, event):
        """Scroll the Pane up one screenful."""

        self.Pane.text.yview_scroll(-1,'page')

    def ScreenDown(self, event):
        """Scroll the Pane down one screenful."""

        self.Pane.text.yview_scroll(1,'page')


#===========================================================================
#                                PAWS Contants
#===========================================================================

# The following contants may be considered "global", that is, they are
# usable anywhere in your game.


#------------------
# Boolean Constants
#------------------

# Notice that TRUE and SUCCESS are synonymous, as are FALSE and FAILURE.
# The reason we use two different sets of words is to make the program
# easier to read.
#
# TRUE and FALSE are used to set variables or conditions. SUCCESS and
# FAILURE are used to test the success or failure of methods and
# functions.


TRUE = 1                # Test or condition is true
SUCCESS = TRUE          # Function was successful
TURN_ENDS = TRUE        # Verb Action causes turn to end

FALSE = 0               # Test or condition is not true (it's false)
FAILURE = FALSE         # Function was NOT successful, it failed
TURN_CONTINUES = FALSE  # Verb Action doesn't end current turn

TEXT_PICKLE = FALSE     # Argument for pickle.dump(), file is stored as text
BINARY_PICKLE = TRUE    # Argument for pickle.dump(), file is stored as binary

SHALLOW = TRUE          # Shallow refers to displaying only the first layer of
                        # a container's contents, regardless if nested containers
                        # are transparent or open.


#-----------------
# Daemon Constants
#-----------------

# This are used to identify which kind of automatically running program
# (daemon, fuse, or recurring fuse) is being examined. Used mainly by
# the RunDaemon() function.
#
# Daemons run every turn once activated, fuses delay for a given number of turns,
# run once, then don't run again. Recurring fuses happen every X turns.

DAEMON = 0
FUSE = 1
RECURRING_FUSE = -1


#---------------------
# Game State Constants
#---------------------

# These constants define the various states the game can enter. STARTING
# means the game is either starting for the first time or restarting to the
# very beginning (because the player typed "restart").
#
# RUNNING means the game is running normally, accepting input from the
# player and processing commands.
#
# FINISHED means the player is quitting the game. Any command that sets
# the game status to FINISHED should cause the TurnHandler to fail, which
# will immediately terminate the game loop and cause the PostGameWrapUp()
# method to execute, just prior to ending the game and shutting down Python.

STARTING = 1
RUNNING = 2
FINISHED = 3


#------------------
# Pronoun Constants
#------------------

# These constants are used as keys into the PronounDict dictionary. They make
# it easy to remember the numeric keys and make the code clearer.

IT = 0
THEM = 1
HIM = 2
HER = 3


#-------------------------
# Verb Allowance Constants
#-------------------------

# These constants are used to tell the verb object which "style" of
# direct/indirect objects to expect. By default the verb is in state 3
# which expects no direct or indirect objects. This is part of the
# disambiguation process.

ALLOW_NO_DOBJS = 1          # Allow No Direct Objects
ALLOW_NO_IOBJS = 2          # Allow No Indirect Objects
ALLOW_ONE_DOBJ = 4          # Allow 1 Direct Object
ALLOW_ONE_IOBJ = 8          # Allow 1 Indirect Object
ALLOW_MULTIPLE_DOBJS = 16   # Allow Multiple Direct Objects
ALLOW_MULTIPLE_IOBJS = 32   # Allow Multiple Indirect Objects
ALLOW_OPTIONAL_DOBJS = 64   # Allow Optional Direct Objects


#---------------------------------
# All asIF visual editor constants
#---------------------------------

# asIF is a visual editor for PAWS programs.

# We also define a constant, AsIf_TrueFalseType.  AsIF needs to distinguish
# between true/false values (which are presented with a checkbox) and
# numbers (which are presented with an entry field) -- but this is a
# distinction Python doesn't make on its own.  So we define the constant
# TrueFalseType with an arbitrary value, whose sole purpose is to tell
# AsIF to use a checkbox rather than an entry field.

AsIF_TrueFalseType = 1



#----------------
# Set Up Terminal
#----------------

# We want the best terminal available to us, so we're going to keep upping the 
# ante until we obtain the most powerful terminal possible. This means we try
# each terminal type in turn, from the least powerful curses character terminal 
# up to actual GUI terminal types like Tkinter. Since the terminal type
# isn't disturbed if the attempt fails this guarantees the last successful
# terminal type that loads is the most powerful.
#
# If *none* of these terminals are available we still have our trusty Glass
# TTY default, so we'll at least be able to play something.


#-------------------------
# Set Up And Save GlassTTY
#-------------------------

# Notice we're activating the Glass TTY without a try statement, since it will
# by definition always be available and always be the default if no other
# terminal is available.

ActiveIO.ActiveIO = ClassDefaultIO()
Terminal = ActiveIO.ActiveTerminal()
OldTerminal = Terminal


#------------------------------
# Try To Set Up Curses Terminal
#------------------------------

# Activate the curses terminal. If successful save it to OldTerminal so it
# becomes the default.

try:
    ActiveIO.ActiveIO = ClassCursesTerminal()
    Terminal = ActiveIO.ActiveTerminal()
except:
    Terminal = OldTerminal

OldTerminal = Terminal


#------------------------------
# Try To Set Up WConio Terminal
#------------------------------

# Activate the WConio terminal. If successful save it to OldTerminal so it
# becomes the default.
                     
#try:
#    ActiveIO.ActiveIO = ClassWConioTerminal()
#    Terminal = ActiveIO.ActiveTerminal()
#except:
#    Terminal = OldTerminal

#-------------------------------
# Try To Set Up Tkinter Terminal
#-------------------------------

# Activate the Tkinter GUI terminal. If successful save it to OldTerminal so
# it becomes the default. This is currently the most powerful terminal
# available, and should also be one of the most widespread.
                         
#try:
#    ActiveIO.ActiveIO = ClassTkinterTerminal()
#    Terminal = ActiveIO.ActiveTerminal()
#except:
#    Terminal = OldTerminal
    
#OldTerminal = None



#===========================================================================
#                       Utility Functions
#===========================================================================

# These functions are of general use for PAWS, Universe, and the game
# author themselves.


#-----------------------
# Append Dictionary List
#-----------------------


# This routine doesn't return a value, it appends a value to a dictionary
# of lists. A Dictionary List is just a dictionary who's values are
# actually lists. For example, the VerbsDict is a list dictionary, it
# might look like this:
#
# {'look': [LookVerb, LookIntoVerb, LookThroughVerb],
#  'quit': [QuitVerb],
#  'exit': [QuitVeb]
# }
#
# You supply the dictionary name, the key, and the value you want to
# append. The key must be a string, either a single value (without any
# commas) or multiple values seperated by commas. For instance:
#
# AppendDictList(NounsDict,"rock,stone",SmallRock)
#
# This would place SmallRock in the dictionary under two keys,
# "rock", and "stone".


def AppendDictList(Dict,Key,Value):
    """Appends value to a list dictionary"""

    
    #------------
    # Massage Key
    #------------

    # We have to massage the key to make it easier to work with. The
    # first thing we do is force the key strings to lower case
    # (string.lower), then split the comma delimited string into a
    # list of strings (string.split).
    #
    # Since this function is mainly used to add words to the verb, noun,
    # preposition and adjective dictionaries. We want to make sure
    # the developer doesn't have to worry about case sensitivity when
    # defining verbs and objects.

    WordList = string.split(string.lower(Key),",")


    #-----------------------------
    # For each word in the list...
    #-----------------------------

    # For each word in the wordlist (dictionary key) do the following...

    for word in WordList:

        #----------------------------
        # Word in dictionary already?
        #----------------------------

        
        # If the word is already in the dictionary we append the value
        # to the entry. This has the effect of adding Value to the
        # list of values already filed under the key.
        #
        # If the word ISN'T in the dictionary, we add the LIST of Value
        # to the dictionary. Notice how the Value is surrounded by
        # square brackets?
        #
        # This is a 'casting' trick. It forces value (which is generally
        # one item) to become a list of one item. This is important
        # because append only works with a list. If we didn't convert
        # Value to a list the second object added to the same key value
        # would cause the game to blow up with an error message.


        if Dict.has_key(word):
            Dict[word] = Union(Dict[word],[Value])
        else:
            Dict[word] = [Value]



#-------
# Choose
#-------

# This function is handy for use inside Curly Brace Expressions (CBE's).
# Decision must evaluate to true or false (0 or 1, empty or full, etc). If
# True then TrueChoice will be returned, else FalseChoice will be returned.

def Choose(Decision,TrueChoice,FalseChoice):
    """Ternary IIF operator, returns TrueChoice or FalseChoice based on Decision"""
    if Decision:
        return TrueChoice
    else:
        return FalseChoice


#=============
# Clear Screen
#=============

def ClearScreen():
    """Clears the screen)"""
    Terminal.ClearScreen()


#---------
# Complain
#---------

# Because the action of printing a message and returning FAILURE is so
# prevalent in the game (complaining) we write a simple function to make
# the complaining much simpler to read. Note that TURN_CONTINUES and FAILURE
# are actually the same value (0).

def Complain(Text=""):
    """Call Say(Text) and return TURN _CONTINUES"""
    Say(Text)
    return TURN_CONTINUES



#------------
# Debug Trace
#------------

# This function lets you put debug tracing into the system and turn it
# on or off with one switch, Global.Debug. Set it to TRUE or FALSE.

def DebugTrace(Text):
    if not Global.Debug: return
    print Text
    if Global.Transcribe: Global.DebugFile.write(Text+"\n")


#-------------------------
# Debug Direct Object List
#-------------------------

# This function is used to list the contents of the (parsed) list of
# direct objects associated with the current command. It's intended
# to help debug the parser and verbs that use direct objects.

def DebugDObjList():
    for Object in P.DOL():
        DebugTrace("-->" + Object.Get(SDesc))


#---------------------------
# Debug Indirect Object List
#---------------------------

# This function is used to list the contents of the (parsed) list of
# indirect objects associated with the current command. It's intended
# to help debug the parser and verbs that use indirect objects.

def DebugIObjList():
    for Object in P.IOL():
        DebugTrace("Debug-->" + Object.Get(SDesc))


#---------------------------
# Debug Passed Object List
#---------------------------

# This function is used to list the contents of the (passed) list of
# objects preceeded by Msg. It's intended to help debug the parser and verbs
# that use objects.

def DebugPassedObjList(Msg,ObjList):
    DebugTrace(Msg)
    for Object in ObjList:
        DebugTrace("-->" + Object.SDesc())
    return ""
    

#-----------------------
# Delete Dictionary List
#-----------------------

# This function deletes an object from a dictionary list (a dictionary who's
# values are lists) and replaces it.

def DeleteDictList(Dictionary,Object=None):
    """Delete Object From Dictionary List"""
    
    #-------------------------
    # Return if no real object
    #-------------------------

    # If Object is None then there's nothing to do.

    if Object == None: return

    
    #---------------------------
    # Return If Dictionary Empty
    #---------------------------

    # If the dictionary is empty there's nothing to do either.

    if len(Dictionary) == 0: return

    
    #------------------------------
    # For each key in dictionary...
    #------------------------------

    # For each key in the dictionary we retrieve the value, which should be
    # a list. If it isn't we skip this key.

    for key in Dictionary.keys():
        
        #------------------------------
        # Retrieve List From Dictionary
        #------------------------------

        # List is the value of the dictionary key. For example:
        # [LookVerb, LookIntoVerb, LookUnderVerb].

        List = Dictionary[key]

        
        #---------------------
        # Continue If Not List
        #---------------------

        # If this dictionary key isn't a list, we skip this key and continue
        # the for loop, getting the next key.

        if type(List) <> type([]): continue

        
        #-------------------------
        # Remove Object If In List
        #-------------------------

        # If object is in list, remove it. If the resulting list is 0 length the 
        # entire dictionary entry should be deleted, otherwise the current
        # dictionary entry will be replaced with the new List.

        if Object in List:
            List.remove(Object)
            if len(List) == 0:
                del Dictionary[key]
            else:
                Dictionary[key] = List




#------------------------------
# Delete Object From Vocabulary
#------------------------------

# PAWS requries the use of a pre-written library. This library (normally
# Universe) creates lots of objects, usually verbs, that sometimes need to be
# overridden. To do this you need to remove all references from the vocabulary
# dictionaries of the old objects (so Python can "garbage collect" them) before
# replacing them with your new definition.
#
# This function deletes the object from the Verb, Preposition, Noun and
# Adjective parser dictionaries so you can either disable the verb or replace
# it with your own. It also works for objects.


def DeleteObjectFromVocabulary(Object):
    """Deletes Passed Object From All Vocabulary Dictionaries"""
    DeleteDictList(P.AP().VerbsDict,Object)
    DeleteDictList(P.AP().PrepsDict,Object)
    DeleteDictList(P.AP().NounsDict,Object)
    DeleteDictList(P.AP().AdjsDict,Object)


#------------------
# Disambiguate List
#------------------


# This function actually figures out which object the player meant. It does
# so by testing the object with the passed TestMethod. If the result is true
# the object is kept, if false it's discarded.
#
# When all objects in the list have been discarded (because none of them
# return true) the function prints the ErrorMethod.
#
# This function returns either a single object (if it can be disambiguated),
# an empty list (if no objects pass the test), or a list of objects that
# do pass the test.


def DisambiguateList(List,TestMethod,ErrorMethod,Actor=None):
    """Actual Disambiguation routine"""
    
    #-------------------------
    # Return List Starts Empty
    #-------------------------

    # Our return list starts empty because we're going to be appending
    # to it.

    ReturnList = []
    
    #-----------------------
    # Set Last Tested Object
    #-----------------------

    # If ALL of the objects in List fail the test we need to use the last
    # object tested as error method argument. Unfortunately the Object
    # variable set in the FOR loop disappears when the loop is completed.
    #
    # LastTestedObject saves the last object tested by the loop. Under certain
    # circumstances, that object may be None, which would cause the ErrorMethod
    # to crash if used as an argument, which is why we have to test for it.
    #
    # Setting LastTestedObject to None now is good programming practice, it 
    # gives the variable existance now and sets it to a known value.

    LastTestedObject = None

    
    #---------------------------
    # For Each Object in List...
    #---------------------------

    # We're guaranteed that List will always be a list, since this function
    # is only called for ambiguous object lists.

    for Object in List[:]:

        #-----------------------
        # Set Last Tested Object
        #-----------------------

        LastTestedObject = Object

        #----------------
        # Actor involved?
        #----------------

        
        # Some test methods require an actor AND an object, while some dont.
        # IsReachable(), for example needs to calculate the path between two
        # objects. If an actor is needed for the test method, it will be
        # passed to DisambiguateListOfLists which in turn passes it to this
        # function.

        if Actor == None:
            TestResult = TestMethod(Object)
        else:
            TestResult = TestMethod(Object,Actor)

        #--------------------
        # Object passes test?
        #--------------------

        
        # If the object passes the test we append it to the ReturnList. If
        # it doesn't...
        #
        # In that case we delete it from the List. If the List loses EVERY
        # member we've eliminated all objects, so we say the error method
        # of the object we just eliminated.

        if TestResult == TRUE:
            ReturnList.append(Object)
            DebugTrace("    "+Object.SDesc() + " passed")
        else:
            List.remove(Object)
            DebugTrace("    "+Object.SDesc() + " failed")

    
    #------------------------
    # No Items in ReturnList?
    #------------------------

    # If there are no items in the return list we need to use the last object
    # tested and print the error condition, since every object failed! We then
    # return an empty list.

    if len(ReturnList) == 0:
        Say(ErrorMethod(LastTestedObject))
        return []

    
    #--------------------------------
    # Exactly One item in ReturnList?
    #--------------------------------

    # If there is exactly one item on the return list we're finished!
    # Instead of returning ReturnList we return just the 0'th (first) element
    # of ReturnList. This returns a single object instead of a list.
    #
    # If there are no objects in ReturnList or more than 1 we return the
    # entire list.

    if len(ReturnList) == 1:
        return ReturnList[0]
    else:
        return ReturnList[:]


#----------------------------
# Disambiguate Lists of Lists
#----------------------------


# This function performs "disambiguation" of the kinds of object lists
# created by the parser. In other words, it intelligently chooses which
# objects are intended when there's a choice.
#
# For instance, if the game contains three keys, a bone key, a brass key, and
# a silver key but only one rock and the player says "get key and rock" the
# resulting direct object list looks like:
#
# [ [BoneKey,BrassKey,SilverKey], [Rock] ]
#
# Notice the direct object list contains two other lists! Key could refer to
# any of the keys, at the time of parsing there's no way to know which is
# intended. Thus we say the key is ambiguous.
#
# Rock isn't of course, since there's only one rock in the game.
#
# The theory of disambiguation is complex and messy, so pay close attention.
# There are three major problems we have to deal with.
#
# First, we're starting off with  a list of lists. It's messy, but the only
# way we can handle ambiguous objects.
#
# The second problem is that of delegation. Since the PAWS engine is intended
# to be library independent we have to build an engine that can work with
# anyone's library. This means both the test method(s) and the error
# method(s) are supplied by the library, along with the specific
# disambiguation method itself.
#
# Which leads to our third problem. We have no way of predicting ahead of
# time which tests the library author will want to perform, or how many of
# them there will be. The implication is we have to be able to handle
# multiple disambiguation passes.
#
# There's another implication. If we handle multiple passes, then at some
# point part of the list will be single objects and part of the list will
# be lists!
#
# For example, let's say that there are two passes. The first tests to see
# if the objects are known. (Assume the player doesn't know a silver key
# exists in the game).
#
# The first pass yields: [ Rock, [BoneKey,BrassKey] ]
#
# Notice Rock is no longer a list, it's a single object. That's because
# the aim of disambiguation is to reduce our list of lists to a simple list
# of objects, if possible. Since the [Rock] list contains only one item we
# convert it to an object. We've eliminated the silver key, but key is
# still ambiguous.
#
# Second pass, are the items reachable? The bone key is in the basement,
# but both the rock and the brass key are in the kitchen with the player.
#
# Thus our second pass yeilds: [ Rock, BrassKey ] and our disambiguation is
# done.
#
# BUT there's a third pass, are all objects visible? Our third pass doesn't
# eliminate anything and yields: [ Rock, BrassKey ].
#
# And depending on the library you use there might be more passes yet. So
# we have to be able to handle all three states of the list.

def DisambiguateListOfLists(ListOfLists,TestMethod,ErrorMethod,Actor=None):
    """Break list of lists into multiple lists for DisambiguateList() function"""
    
    #------------------------------------
    # Empty list automatically successful
    #------------------------------------

    if len(ListOfLists) == 0:
        return SUCCESS

    
    #-------------------------
    # Return List Starts Empty
    #-------------------------

    # Our return list starts empty because we're going to be appending to it.

    ReturnList = []
    
    #--------------------------------
    # For Each item in ListOfLists...
    #--------------------------------

        # Each item in the list of lists might be a single object (unambiguous)
    # or it might be a list of objects (ambiguous). The purpose of this loop
    # is to either directly append an unambiguous object to the return list
    # or pass an ambigous object list to the DisambiguateList function to see
    # if it can be disambiguated and append the result.

    for List in ListOfLists:
        
        #---------------------
        # Is Object ambiguous?
        #---------------------

        
        # Remember, "List" will either be a single object (unambigous) or
        # a list of objects with the same noun (ambiguous). If it is an
        # ambiguous list we pass it to the disambiguate function, which
        # will either return a single object if it was able to narrow it
        # down to one or it will return a (hopefully smaller) list of
        # objects. In either case we simply append the result to the
        # ReturnList.
        #
        # If the object isn't ambiguous we just append the object to the
        # return list.

        if type(List) == type([]):
            WorkList = DisambiguateList(List,TestMethod,ErrorMethod,Actor)
            ReturnList.append(WorkList)
            continue

        
        #-----------------------
        # Not Ambiguous, test it
        #-----------------------

        if Actor == None:
            TestResult = TestMethod(List)
        else:
            TestResult = TestMethod(List,Actor)

        #--------------------
        # Object fails test?
        #--------------------

        
        # If the object passes the test we append it to the ReturnList. If
        # it doesn't...
        #
        # In that case we delete it from the List. If the List loses EVERY
        # member we've eliminated all objects, so we say the error method
        # of the object we just eliminated.

        if not TestResult:
            DebugTrace("    "+List.SDesc() + " Failed")
            ListOfLists.remove(List)
            Say(ErrorMethod(List))
            DebugTrace("    "+List.SDesc() + " unambiguous failure")
            continue

        DebugTrace("    "+List.SDesc() + " passed")
        ReturnList.append(List)


    #-------------------
    # Remove empty lists
    #-------------------

    # From time to time the DisambiguateList() function will eliminate EVERY
    # object in the list. For example, the player says "get rock" but the
    # rock isn't here. In that case the DisambiguateList function returns
    # an empty list -- []. You may have (depending on the situation) many
    # empty lists in your ListOfLists.
    #
    # The line below eliminates empty lists, leaving single items and
    # object lists untouched. How it does it is something of a Python
    # mystery, but rest assured it works.

    ReturnList = filter(None,ReturnList)
    #---------------------------
    # Return New "List Of Lists"
    #---------------------------

    # The result of this function is either a partially disambiguated list
    # or a completely disambiguated one. The list of lists may be run
    # through this function again with a different test method to further
    # disambiguate the list.

        # Notice the peculiar syntax we use to assign ListOfLists. The reason
    # we do this is extremely involved, but the short form is that Python
    # doesn't support "pass by reference".
    #
    # Instead it passes a copy of an object reference. ListOfLists isn't
    # a copy of Global.CurrenDIObjList, for instance, it *points* to it.
    #
    # But the statement "ListOfLists = ReturnList" means that instead of
    # assigning ReturnList to Global.DObjList as you might expect, it
    # actually changes where ListOfLists is *pointing* to!
    #
    # By putting [:] on the end, we change this from pointer assignment to
    # object reference. Since ListOfLists is still pointing to Global.DObjList
    # it does what we want it to (replace Global.DObjList with a copy of
    # ReturnList).

    ListOfLists[:] = ReturnList[:]

    if len(ReturnList) > 0:
        return SUCCESS
    else:
        return FAILURE



#------------------
# Do (execute) code
#------------------

# This function takes a string and tries to turn it into valid Python
# code, then execute it. Its main purpose is for use in debugging, to
# set variables and the like, but you can execute any valid Python
# code fragment with it. Be careful!

def DoIt(CodeString):
    """Takes CodeString and tries to execute it as a Python command"""
    try:
        eval(compile(CodeString,"<string>","exec"))
    except:
        Say("Syntax Error In CodeString")

    return "Code Execution Complete"



#------------
# Game Daemon
#------------

# This function is a DAEMON, a function that will be run automatically every turn
# by the game engine. All it does is increment the turn counter, but it
# demonstrates how to write a daemon.

def GameDaemon():
    """Daemon to handle standard game chores"""
    Global.CurrentTurn = Global.CurrentTurn + 1
    Terminal.DisplayStatusLine(Global.StatusLine)
 


#-------
# Indent
#-------

# This function merely creates a string of "\t" (tab) characters for each
# indent level passed in the argument. For example, Indent(3) returns 3 tab
# characters. NOTE: TAB CHARACTERS ARE 3 SPACES, NOT ASCII CODE 9!

def Indent(Level):
    """Returns Level # of ~t's"""
    RV = ""
    for x in range(0,Level): RV = RV + " ~t "
    return RV

#--------------------------
# Intersection of two lists
#--------------------------

# This function takes two lists and returns a list of items common to
# both lists.

def Intersect(list1,list2):
    """Returns intersection of two lists"""
    ReturnList = []

    for x in list1:
        if x in list2: ReturnList.append(x)

    return ReturnList

#--------------
# In Vocabulary
#--------------

# This function returns TRUE if the passed word is in the game's vocabulary,
# FALSE if it isn't.

def InVocabulary(Word):

    if P.AP().NounsDict.has_key(Word): return TRUE
    if P.AP().VerbsDict.has_key(Word): return TRUE
    if P.AP().AdverbsDict.has_key(Word): return TRUE
    if P.AP().AdjsDict.has_key(Word): return TRUE
    if P.AP().PrepsDict.has_key(Word): return TRUE
    if P.AP().PronounsListDict.has_key(Word): return TRUE
    if Word in P.AP().ArticlesList: return TRUE
    if Word in P.AP().ConjunctionsList: return TRUE
    if Word in P.AP().DisjunctionsList: return TRUE
    if Word in P.AP().CommandBreaksList: return TRUE

    return FALSE



#===============================
# Run Existing Daemons And Fuses
#===============================


# This function runs all daemons and fuses in Global.DaemonDict. It
# does all the scheduling for fuses and recurring fuses.


def RunDaemons():
    """Runs all daemons/fuses in Global.DaemonDict"""

    
    #---------------------
    # For Each Daemon/Fuse
    #---------------------

    
    # Global.DaemonDict.keys() returns a list of the keys in the
    # dictionary. Each key is a function reference so DaemonFuse,
    # in addition to being the dictionary key for this particular
    # entry in Global.DaemonDict is also an indirect reference to
    # a function. That means the expression DaemonFuse() will actually
    # run the appropriate function!


    for DaemonFuse in Global.DaemonDict.keys():

        
        #-------------------------
        # Get Original Fuse Length
        #-------------------------

        # Remember, the original fuse length will be a negative, 0, or
        # positive number. It's stored in the dictionary and is the
        # original fuse length. If negative the remaining turns will
        # be reset to the absolute value of this number.

        FuseLength = Global.DaemonDict[DaemonFuse][1]

        
        #-------------------
        # Get Remaining Time
        #-------------------

        # Get the remaining time. Note this is the time *before* the
        # fuse is reduced for the current turn. For example, if the
        # value was 1, then the fuse will execute THIS PASS, since
        # 1 minus 1 is 0. However, if the value were 2 it would
        # execute NEXT pass, since 2 - 1 is 1, not 0.

        RemainingTime = Global.DaemonDict[DaemonFuse][0]

        
        #---------------------
        # Identify Daemon Type
        #---------------------

        # Any function in Global.DaemonDict can be either a daemon,
        # a fuse, or a recurring fuse. A daemon runs every turn,
        # a fuse runs after X turns delay and is then removed from
        # DaemonDict, a recurring fuse runs after a delay of X turns
        # but is then reset to run in another X turns.


        if FuseLength < 0:  DaemonType = RECURRING_FUSE
        if FuseLength == 0: DaemonType = DAEMON
        if FuseLength > 0:  DaemonType = FUSE

        
        #-----------------
        # Handle If Daemon
        #-----------------

        # If the function we're examining is a daemon (has an
        # original fuse length of 0) then it's supposed to run every
        # turn. So we run it and continue, which skips the rest of
        # the FOR loop. Note we DO NOT return! If we returned then
        # only the first daemon/fuse in the dictionary would execute.

        if DaemonType == DAEMON:
            DaemonFuse()
            continue

        
        #----------------------
        # Reduce Remaining Time
        #----------------------

        # Since we know the function being examined is either a fuse
        # or a recurring fuse, we shorten the remaining time by 1. We
        # know we aren't dealing with a daemon because daemons are
        # handled above, we'd never have gotten here if it was a
        # daemon.
        #
        # Notice we reduce RemainingTime, then assign it back to the
        # dictionary. We use RemainingTime because it makes the code
        # easier to read and understand.

        RemainingTime = RemainingTime - 1
        Global.DaemonDict[DaemonFuse][0] = RemainingTime
        
        #-------------------------
        # Continue If Time Remains
        #-------------------------

        # If there's still remaining time (RemainingTime is more than
        # 0) then we need do nothing further for either fuses or
        # recurring fuses, since they haven't "gone off" yet.

        if RemainingTime > 0: continue

        
        #----------------------
        # Execute Fuse Function
        #----------------------

        # If we've gotten this far it means the Remaining Time has
        # been exhausted, it has reached 0. Remember than DaemonFuse
        # contains an indirect function reference. All we have to do
        # to execute the function is put parentheses after it, as we
        # do in the code below. If DaemonFuse contains a reference to
        # the ClearScreen function, for instance, then
        #
        # DaemonFuse()
        #
        # would be identical to:
        #
        # ClearScreen()

        DaemonFuse()

        
        #----------------------
        # Handle If Normal Fuse
        #----------------------

        # If we're dealing with a regular fuse we simply call
        # StopDaemon and pass it DaemonFuse, which is the indirect
        # reference to the function we just executed. This removes it
        # from Global.DaemonDict. Then we continue, to skip the rest
        # of the FOR loop.

        if DaemonType == FUSE:
            StopDaemon(DaemonFuse)
            continue

        
        #-------------------------
        # Handle If Recurring Fuse
        #-------------------------

        # If dealing with a recurring fuse (one that resets itself
        # after the function is executed) then we reset RemainingTime
        # to the absolute value of FuseLength. This turns the negative
        # FuseLength into a positive value for Remaining time.
        #
        # Then we set the 0'th (first) element of the dictionary to
        # the remaining time. Doing it this way makes the code easier
        # to understand than the equivalent single line:
        #
        # Global.DaemonDict[DaemonFuse][0] = abs(FuseLength)

        if DaemonType == RECURRING_FUSE:
            RemainingTime = abs(FuseLength)
            Global.DaemonDict[DaemonFuse][0] = RemainingTime
            continue


    #-----------------
    # Return To Caller
    #-----------------

    # Notice we're returning, but we aren't returning a value to
    # the caller. This is reasonable, since this function just runs
    # daemons, and really can't say much about their statuses.

    return



#----------------------
# Say print replacement
#----------------------


# Because the print statement isn't particularly intelligent when it comes to
# printing we'll have to create our own. This function makes sure that when
# a word is printed it doesn't "wrap" from the right edge of the screen to
# the left edge.
#
# In addition, if a single piece of text is printed that exceeds the number
# of screen lines available, a [--more--] capability allows all text to be
# read before it scrolls of the end of the screen.
#
# Note this function interprets no "\" characters (\n, \t, etc) but it does
# recognize two commands, ~n and ~m. These must be space seperated from
# the words around them.
#
# ~n causes a \n line break. ~m forces a "[-- more --]" message and the
# screen to pause. ~n lets you format text and ~m lets you pause the
# printing exactly where you want to.


def Say(Text="",Mode=None):
    """Replacement print statement"""
    
    #---------------
    # Make Shortcuts
    #---------------

    # These variables are just shortcuts to make the code shorter and easier
    # to read. LP means Lines Printed. If Lines printed for this piece of
    # text exceed Max screen lines - 1 then we pause printing to allow the
    # player to read the screen.

    MSL = Terminal.MaxScreenLines
    MSC = Terminal.MaxScreenColumns
    LP = 0
    LFAfter  = FALSE
    if Mode is None: Mode = Terminal.A_NORMAL
    
    
    #------------------
    # Ignore Empty Text
    #------------------

    # If Text is empty (nothing) then return without doing anything.

    if Text == "": return
    
    #--------------------------------
    # Translate {} Expressions And ~p
    #--------------------------------

    Text = Engine.XlateCBEFunction(Text)
    Text = string.replace(Text,"~p","~n ~n")
    
    
    #-----------------
    # Create Word List
    #-----------------

    # This will break the text into a list of words which we can then use
    # a FOR loop on.

    WordList = string.split(Text)

    
    #---------------------------
    # For each word in Word List
    #---------------------------

    for Word in WordList:
        
        #----------------------
        # Terminal Mode Changes
        #----------------------

        # Various special characters to control the terminal.

        if Word[0] == "~":
            if Word   == "~b":
                Mode = Terminal.A_BOLD;Word = ""
            elif Word == "~title":
                Mode = Terminal.A_TITLE;Word = ""
            elif Word == "~d":
                Mode = Terminal.A_DIM;Word = ""
            elif Word == "~e":
                Mode = Terminal.A_MORE;Word = ""
            elif Word == "~i":
                Mode = Terminal.A_INPUT;Word = ""
            elif Word == "~l":
                Mode = Terminal.A_NORMAL;Word = ""
            elif Word == "~r":
                Mode = Terminal.A_REVERSE;Word = ""
            elif Word == "~s":
                Mode = Terminal.A_STANDOUT;Word = ""
            elif Word == "~u":
                Mode = Terminal.A_UNDERLINE;Word = ""
            elif Word == "~bk":
                Mode = Terminal.BLACK;Word = ""
            elif Word == "~bl":
                Mode = Terminal.BLUE;Word = ""
            elif Word == "~gr":
                Mode = Terminal.GREEN;Word = ""
            elif Word == "~cy":
                Mode = Terminal.CYAN;Word = ""
            elif Word == "~rd":
                Mode = Terminal.RED;Word = ""
            elif Word == "~mg":
                Mode = Terminal.MAGENTA;Word = ""
            elif Word == "~br":
                Mode = Terminal.BROWN;Word = ""
            elif Word == "~gy":
                Mode = Terminal.LIGHTGRAY;Word = ""
            elif Word == "~lbk":
                Mode = Terminal.DARKGRAY;Word = ""
            elif Word == "~lbl":
                Mode = Terminal.LIGHTBLUE;Word = ""
            elif Word == "~lgr":
                Mode = Terminal.LIGHTGREEN;Word = ""
            elif Word == "~lcy":
                Mode = Terminal.LIGHTCYAN;Word = ""
            elif Word == "~lrd":
                Mode = Terminal.LIGHTRED;Word = ""
            elif Word == "~lmg":
                Mode = Terminal.LIGHTMAGENTA;Word = ""
            elif Word == "~lbr":
                Mode = Terminal.YELLOW;Word = ""
            elif Word == "~lgy":
                Mode = Terminal.WHITE;Word = ""
            elif Word == "~bbk":
                Mode = Mode + (Terminal.BLACK << 4);Word = ""
            elif Word == "~bbl":
                Mode = Mode + (Terminal.BLUE << 4);Word = ""
            elif Word == "~bgr":
                Mode = Mode + (Terminal.GREEN << 4);Word = ""
            elif Word == "~bcy":
                Mode = Mode + (Terminal.CYAN << 4);Word = ""
            elif Word == "~brd":
                Mode = Mode + (Terminal.RED << 4);Word = ""
            elif Word == "~bmg":
                Mode = Mode + (Terminal.MAGENTA << 4);Word = ""
            elif Word == "~bbr":
                Mode = Mode + (Terminal.BROWN << 4);Word = ""
            elif Word == "~bgy":
                Mode = Mode + (Terminal.LIGHTGRAY << 4);Word = ""
            elif Word == "~blbk":
                Mode = Mode + (Terminal.DARKGRAY << 4);Word = ""
            elif Word == "~blbl":
                Mode = Mode + (Terminal.LIGHTBLUE << 4);Word = ""
            elif Word == "~blgr":
                Mode = Mode + (Terminal.LIGHTGREEN << 4);Word = ""
            elif Word == "~blcy":
                Mode = Mode + (Terminal.LIGHTCYAN << 4);Word = ""
            elif Word == "~blrd":
                Mode = Mode + (Terminal.LIGHTRED << 4);Word = ""
            elif Word == "~blmg":
                Mode = Mode + (Terminal.LIGHTMAGENTA << 4);Word = ""
            elif Word == "~blbr":
                Mode = Mode + (Terminal.YELLOW << 4);Word = ""
            elif Word == "~blgy":
                Mode = Mode + (Terminal.WHITE << 4);Word = ""
        
        
        #-------------------
        # Replace ~n with \n
        #-------------------

        Word = string.replace(Word,"~n","\n")
        Word = string.replace(Word,"~t","  ")

        
        #-------------------------------
        # If it starts with a line break
        #-------------------------------

        # If the first two characters of Word are \n this means a newline
        # character will be printed, followed by the word.
        # Increment the current line # by one but don't exceed the screen
        # length, increment the number of lines printed and reset the
        # current screen column to 1.

        if Word == "\n":
            Terminal.NewLine()

            if Global.Transcribe:
                Global.LogFile.write("\n")
                if Global.Debug: Global.DebugFile.write("\n")

            LP = LP + 1
            Word = ""

        
        #------------------------
        # Screen Length Exceeded?
        #------------------------

        # If the lines printed are about to exceed screen length then
        # use the raw_input function to pause. Notice we don't assign the
        # return value to anything, it's discarded.
        #
        # Once the player presses Enter we set lines printed to 0.

        if LP > MSL - 2 or Word == "~m":
            LP = 0
            Terminal.MoreMessage()
            if Word <> "~m":
                Terminal.Output(Word,Mode)

            if Global.Transcribe:
                Global.LogFile.write(Word+" ")
                if Global.Debug: Global.DebugFile.write(Word+" ")
                
            continue

        
        #-------------------------
        # Will Word Fit on line?
        #-------------------------


        # If the word fits on the current line print it then increment the
        # current screen column by the length of the word and again by 1.
        # Each time a word is printed Python automatically puts a space after
        # it. Then of course the word is printed to the screen.
        #
        # If the word won't fit on the current line print a blank line,
        # print the word, then set the current screen column to 1, incremnt
        # the screen line (but don't let it go past the end of screen), and
        # increment the number of lines printed.

        if Terminal.CurrentScreenColumn + len(Word) < MSC - 2:
            if len(Word) > 0:
                Terminal.Output(Word,Mode)

                if Global.Transcribe:
                    Global.LogFile.write(Word+" ")
                    if Global.Debug: Global.DebugFile.write(Word+" ")

        else:
            Terminal.NewLine()
            Terminal.Output(Word,Mode)

            if Global.Transcribe:
                Global.LogFile.write("\n"+Word+" ")
                if Global.Debug: Global.DebugFile.write("\n"+Word+" ")

            LP = LP + 1




#--------------
# Sentence Case
#--------------

# This function acts like lower except it capitalizes the first letter of
# the passed argument.Note it ALSO strips leading whitespace before
# capitalizing the string!

def SCase(Sentence):
    """Returns argument with first character upper case & rest lower case."""

    if Sentence == None: return Sentence
    if type(Sentence) <> type(""): return Sentence

    NewSentence = string.lstrip(Sentence)
    return string.capitalize(NewSentence[0]) + NewSentence[1:]


#-------
# Self()
#-------


# Because "self" is actually only a method argument defined by
# classes it can't be used in curly-brace expressions (which are
# evaluated by a function). Therefore we store the "current object"
# (self, in other words) in Global.CurrentObject. Because that's such
# a long string, we define this function to make it easier to use.
#
# Therefore instead of saying something like:
#
# {Global.CurrentObject.TheDesc()}
#
# we can use the shorter:
#
# {Self().TheDesc()}
#
# They mean exactly the same thing, but Self() is a lot easier to
# read AND type!
#
# The complement to this function is the MakeCurrent() method which
# is called as part of the parsing process.


def Self(): return Global.CurrentObject


#------------------------
# Remove list2 from List1
#------------------------

# Returns a list containing list1 with items in list2 removed.

def SetRemove(list1,list2):
    """Returns list1 with list2 removed."""
    ReturnList = list1[:]
    for x in list2:
        if x in ReturnList: ReturnList.remove(x)
    return ReturnList

#=======================
# Start A Daemon Running
#=======================


# This function takes the function reference in DaemonFuse and adds it
# to Global.DaemonDict. It sets the Remaining Turns appropriately as
# well.
#
# Note FuseLength is optional, if not supplied it will default to 0,
# which means run the daemon every turn.
#
# This function returns SUCCESS unless DaemonFuse isn't a funciton,
# in which case it returns FAILURE.


def StartDaemon(DaemonFuse,FuseLength = 0):
    """Adds a daemon/fuse to Global.DaemonDict"""

    
    #------------------------------------
    # Fail If DaemonFuse isn't a function
    #------------------------------------

    # Daemons *must* be functions, they can't be methods, strings, or
    # anything else.

    if type(DaemonFuse) <> type(StartDaemon): return FAILURE

    
    #-------------------------
    # Append/Update DaemonDict
    #-------------------------

    # If DaemonFuse is already in Global.DaemonDict then the remaining
    # turns and fuse length will be *updated*. This lets you change a
    # daemon into a fuse or vice versa, or reset a fuse's activation
    # time.
    #
    # If DaemonFuse isn't in DaemonDict it will be added. Since both
    # cases are handled by a single simple line of code, you can 
    # appreciate just how powerful dictionaries are!

    Global.DaemonDict[DaemonFuse] = [abs(FuseLength), FuseLength]

    
    #---------------
    # Return SUCCESS
    #---------------

    return SUCCESS



#======================
# Stop A Daemon Running
#======================


# This function takes the function reference in DaemonFuse and removes
# it from Global.DaemonDict. Obviously, this will stop the daemon/fuse
# from running.
#
# This function returns SUCCESS unless DaemonFuse isn't a funciton,
# in which case it returns FAILURE. It will also return FAILURE if
# DaemonFuse isn't currently in the dictionary.


def StopDaemon(DaemonFuse):
    """Removes a daemon/fuse from Global.DaemonDict"""

    
    #------------------------------------
    # Fail If DaemonFuse isn't a function
    #------------------------------------

    # Daemons *must* be functions, they can't be methods, strings, or
    # anything else.

    if type(DaemonFuse) <> type(StartDaemon): return FAILURE

    #---------------------------------------
    # Fail If DaemonFuse Isn't In DaemonDict
    #---------------------------------------

    # Return FAILURE if DaemonFuse isn't on the list. This allows us
    # a silent but testable way to see if the daemon was removed, or
    # wasn't actually on the list.

    if not Global.DaemonDict.has_key(DaemonFuse): return FAILURE
    
    #-----------------------------------------
    # Remove DaemonFuse From Global.DaemonDict
    #-----------------------------------------

    del Global.DaemonDict[DaemonFuse]

    
    #---------------
    # Return SUCCESS
    #---------------

    return SUCCESS




#===========================================================================
#                      Default Handler Functions For Engine
#===========================================================================

# You'll probably replace most of these.


#---------------------------
# Default After Turn Handler
#---------------------------

# This routine is intended for actions (like daemons) that should occur
# after a given amount of time has elapsed, or after a successful
# player's turn, which is assumed to take a few minutes. Note this
# routine is only called when the Turn handler routine above returns
# SUCCESS.
#
# This allows you the ability to control which commands count as a turn
# and which ones do not.

def default_AfterTurnHandler():
    """Default routine for handling after turn stuff, like daemons"""
    Engine.BuildStatusLine()
    RunDaemons()
    
#--------------------------
# Default Build Status Line
#--------------------------

# This method is just a place holder for the library written method.

def default_BuildStatusLine():
    """Default build status line method."""
    pass

#*********************************************************************************
#                               PAWS Game Skeleton
#                      Written by Roger Plowman (c) 1998-2001
#
# This is the heart of the game. It calls your game and stays active until the game
# ends.
#*********************************************************************************

def default_GameSkeleton():
    """Default game logic loop"""

    
    #==========
    # Game Loop
    #==========

    # The basic logic in IF games is simple. Get a command from the player, 
    # figure it out, do it, then tell the player what happened. Repeat until
    # the player quits the game.

    while Global.GameState != FINISHED:

        #-----------------------
        # While Game is STARTING
        #-----------------------

        # The first time this loop executes GameState will be STARTING so we set
        # up the Game and set GameState to RUNNING.

        if Global.GameState == STARTING:
            Engine.SetUpGame()
            Global.GameState = RUNNING

        #----------------------
        # While Game is RUNNING
        #----------------------

        
        # While the game is running (which it will do until something
        # sets the GameState to FINISHED) we call the
        # pre-turn handler then the parser.
        #
        # If the parser executes successfully we then execute the
        # turn hanlder, and if *that* succeeds then we execute the
        # after turn handler.
        #
        # The implication is that if the parser returns FAILURE
        # (which it might do if the command wasn't understood, the
        # pre-turn handler will *still* execute. Another implication
        # is that you can deliberately cause the turn-handler to fail
        # and thus avoid running the after turn handler. This gives
        # you better control.

        if Global.GameState == RUNNING:
            Engine.PreTurnHandler()
            if P.AP().Parser():
                if Engine.TurnHandler(): Engine.AfterTurnHandler()

    
    #=============
    # Wrap Up Game
    #=============

    # Once the game is over (the loop ended because Global.GameState
    # was set to FINISHED) we call the PostGameWrapUp method to print
    # a closing message, or whatever's appropriate to your game.

    Engine.PostGameWrapUp()

    
    #===============
    # Shut down game
    #===============

    # Finally, we quit the Python interpreter, which shuts down the
    # game and returns us to the operating system.

    Terminal.Terminate()
    sys.exit()


#***************************************************************************
#                           END OF PAWS GAME SKELETON
#***************************************************************************



#--------------------------
# Default Post Game Wrap Up
#--------------------------

# The post game wrap up lets the developer print a message after the
# game is over, if they want. The default version below does absolutely
# nothing.

def default_PostGameWrapUp():
    """Default routine for printing end of game messages"""
    pass


#-------------------------
# Default Pre Turn Handler
#-------------------------

# Although the default pre-turn handler does nothing, the developer can
# replace it with one that handles "quick" actions, actions which should
# happen just before the player is allowed to type their command WHETHER
# OR NOT THE LAST COMMAND WAS SUCCESSFUL, OR EVEN UNDERSTOOD!
#
# Pre-turn handlers aren't normally required.

def default_PreTurnHandler():
        """Default routine for handling 'pre-turn' stuff"""
        pass


#-------------------
# Default Setup Game
#-------------------

# This method sets up the starting parameters for the game. It places
# objects, initialzies daemons, and all the rest. Note if the developer
# wants they can create their own

def default_SetUpGame():
    """Default routine for setting up the game"""
    pass


#---------------------
# Default Turn Handler
#---------------------

# The default turn handler doesn't actually do much, it simply returns
# the TURN_ENDS or TURN_CONTINUES value returned by the current verb's Execute
# method.
#
# In other words, if the player typed "look at rose" then all the
# turnhandler does is call LookAtVerb.Execute(). LookAtVerb.Execute()
# returns either TURN_ENDS or TURN_CONTINUES, which the TurnHandler returns to
# the gaming loop.

def default_TurnHandler():
        """Default routine for handling player commands"""
        return P.AP().CurrentVerb.Execute()


#------------------------
# Default User Setup Game
#------------------------

# This method is just a place holder for the user written User set up
# game method.

def default_UserSetUpGame():
    """Default USER routine for setting up the game"""
    pass



#=================================================================================
#                                     PAWS Classes
#=================================================================================

# These are the real basic, fundamental parts of PAWS (and thus Universe and
# any games written with them.
                              


#===========================================================================
#                             Global Class
#===========================================================================

# This class defines the Global variables object. The global variables object
# is used to hold all the variables that you want to get to from every part
# of the program (such as the Game State).

class ClassGlobal(ClassFundamental):
    """Holds Global Variables"""
        
    def __init__(self):
        """Sets default instance properties"""
        self.NamePhrase = "Global Object"
        ClassFundamental.InheritProperties(self)
        
    
    def SetMyProperties(self):
        """Set Global Properties"""
        
        #--------------
        # Active Parser
        #--------------

        # This variable (actually a property, but who's counting?) holds the
        # current parser object, the object used to translate the player's 
        # input into terms the engine can understand. We put this here so that
        # the parser can attach itself and the save/restore functions will save
        # the parser object properties (particularly vocabulary).

        self.ActiveParser = None
        

        
        #-----------------------------
        # Dictionary Of Active Daemons
        #-----------------------------

        
        # This "dictionary of lists" contains all the daemons and
        # fuses which are currently active (use StartDaemon() to add
        # daemons/fuses to the list and StopDaemon() to remove
        # them from the list).
        #
        # Use RunDaemon() to actually execute daemons in the list.
        #
        # The dictionary key is the indirect reference to the function
        # you want to run. It MUST be a function reference, an object
        # method won't work. In addition, you can't pass any arguments
        # to a daemon/fuse.

        # Each entry in the dictionary is a list. The elements of the
        # entry list is:
        #
        # 0 - Remaining Turns. How many turns remain before the daemon
        #     activates. For a daemon that runs every turn this value
        #     will be 0. For a fuse (function that runs once) this
        #     value will be the number of turns before the function
        #     is executed. Each turn this number is reduced by 1.
        #
        # 2 - Initial Fuse Length. When the daemon or fuse is added to
        #     Global.DaemonList by RunDaemon() the Remaining Turns
        #     value above is set to the ABSOLUTE VALUE of this number.
        #
        #     0  - If this number is 0 the function will be executed
        #          every turn. In other words, it's a daemon just like
        #          in TADS.
        #
        #     >0 - If this number is positive (5, say) then the
        #          remaining turns above will be set to 5 and the
        #          function will be run 5 turns later. It will run
        #          once and be removed from Global.DaemonList. In
        #          other words, this is like a fuse in TADS.
        #
        #     <0 - If this number is NEGATIVE (-5, say) then the
        #          remaining turns above will be set to 5 and the
        #          function will be run 5 turns later. However, once
        #          run instead of being removed the remaining turns
        #          count is RESET. Using a negative number is like
        #          running a daemon every X turns instead of every
        #          turn.


        self.DaemonDict = {}


        
        # The debug property is an easy way to embed (and leave) debugging trace code in your
        # program. In production it should be set to FALSE

        self.Debug = FALSE


        
        #-----------
        # Game State
        #-----------

        # This variable (actually a property, but who's counting?) holds the
        # current state of the game, which starts off as STARTING. This is
        # how the game logic loop knows when the game is starting or running
        # or finished.

        self.GameState = STARTING


        
        #----------------
        # Player "Object"
        #----------------

        # The player object is the one the player controls, it's usually
        # refered to as "me". When a player types a command it's usually
        # assumed the player object is the one that will do the command.
        #
        # Global.Player is set in the object library (Universe), but can be
        # easily be overridden in your game library.

        self.Player = None

        
        #---------------------------
        # Parts Of Speech Dictionary
        #---------------------------

        
        # Like the noun, verb, adjective and preposition dictionaries this
        # dictionary contains lists. Also like those dictionaries POSDict is keyed
        # on the vocabulary word.
        #
        # This dictionary identifies which of the 8 parts of speech the word
        # belongs to:
        #
        #   Noun (sword, ring, rock)
        #   Verb (take, run, hide)
        #   Adjective (blue, big, small, heavy)
        #   Limiting adjective (a, an, the, some, first)
        #   aDverb (quickly, slowly, carefully)
        #   pRonoun (him, her, them)
        #   Preposition (in, behind, of, about)
        #   Conjuctions (and, but, or, nor, after, if)
        #
        # The capitalized letter is what's put in the dictionary. For example,
        # here are two entries:
        #
        #   "take": ["V"]
        #   "gold": ["A", "N"]
        #
        # These entries tell us that "take" is a verb, and that "gold" is both an
        # adjective and a noun.
        #
        # A "Limiting" adjective is one used to identify a sub-group or one
        # particular item from a group of similar items "That rock", "a rock",
        # "some rocks", "the fifth rock", etc. We distinguish them from regular
        # adjectives to make the parser's job easier.


        self.POSDict = {}

        
        #----------------------
        # Game is in Production
        #----------------------

        # This variable allows you to enable/disable the Debug verb.
        # All you need to do to disable the Debug verb is set 
        # Production to TRUE instead of FALSE.
        #
        # The default TQ.py file comes with Production set to FALSE,
        # so that the Debug verb works.
        #
        # When your game is finished and completely tested, change the
        # line in your specially created UserSetUpGame() function
        # replacement to TRUE.
        #
        # IMPORTANT NOTE: Do *NOT* change the value here! Do it in
        # your game library's UserSetUpGame() function! For example,
        # in Thief's Quest the library is called TQLib.py and the
        # function is called TQUserSetUpGame(). THAT's where you
        # should change it, NOT HERE.

        self.Production = TRUE


        
        #------------
        # Status Line
        #------------
        
        self.StatusLine = " "

        
        # The Transcribe property turns the transcription log on and off. The log
        # records every bit of text produced by Say() and player input to one log,
        # (<gamename>.log) and debugging output to a second file (<gamename>.dbg).

        self.Transcribe = FALSE
        self.LogFile = 0
        self.DebugFile = 0
        


#-------------------
# Instantiate Global
#-------------------

Global = ClassGlobal()



#===========================================================================
#                           Parser Class
#===========================================================================

class ClassParser(ClassFundamental):
    """Defines all parser functionality"""

    
    #--------------------
    # Initialize function
    #--------------------

    # ClassFundamental.SetMyProperties() will automatically call SetMyProperties()
    # for every ancestor class of self that defined it, in the proper sequence.

    def __init__(self):
        """Create Instance Variables"""
        self.NamePhrase = "Parser Object"
        ClassFundamental.InheritProperties(self)

    
    #------------------------
    # Set Instance Properties
    #------------------------

    def SetMyProperties(self):
        """Sets default instance properties"""

        
        #--------------------------
        # Active Command Words List
        #--------------------------

        # The active command words list contains a list of words for the
        # command currently being processed.

        self.ActiveCommandList = []
        
        
        #----------------------
        # Adjectives Dictionary
        #----------------------

        # The AdjsDict dictionary holds all objects associated with a given
        # adjective, just like the NounsDict dictionary, for example:
        #
        # 'small': [SmallRock, Kitten, Phial, House]
        # 'glass': [CrystalBall, Window]
        # 'large': [Troll, Cliff, Diamond]

        self.AdjsDict = {}

        
        # The AdverbsDict 
        #
        # 'Look': [LookVerb, LookIntoVerb, LookUnderVerb]

        self.AdverbsDict = {}
        
        
        # Articles aren't used, they're discarded at the present time. It is possible future
        # enhancements of the parser will make use of these.

        self.ArticlesList = ["a","an","the"]


        
        # Items in this list seperate multiple commands entered on a single line.

        self.CommandBreaksList = ["then",
                                  ".",
                                  "?",
                                  "!"]
        
        #--------------
        # Commands List
        #--------------

        # This list holds the list of seperate commands that the player typed
        # on the same line, for instance "Go west then open door" is two
        # commands, not just one. The Commands List for this would look like
        # this:
        #
        #   [['go','west'],['open','door']]
        #
        # In other words CommandsList[0] is ['Go','west'].

        self.CommandsList = []
        
        # Conjunctions are currently ignored, but future enhancements to the parser
        # may make of them.

        self.ConjunctionsList = ["and",","]


        
        #----------------
        # Decoded Objects
        #----------------

        # Once the parser figures out which objects the player's command
        # indicated it puts them in these variables.
        #
        # CurrentActor and CurrentVerb are both single objects.
        #
        # CurrentPrepList is a list of strings, the preposition(s) used
        # with the verb. For instance, 'get book from under the bed' would
        # have 2 prepositions, 'from' and 'under.' You generally won't need
        # these but if you ever do you'll have them.
        #
        # CurrentDObjList is a list of the direct object(s) the player meant,
        # and CurrentIObjList is a list of indirect object(s) the player
        # meant.
        #
        # SaidText is literally the text the player typed in for the
        # ActiveCommandList. As in "Say "Hello". SaidText would be
        # "Hello" inside quotes.

        self.CurrentActor = None        # Object
        self.CurrentVerb = None         # Object
        self.PreviousVerb = None        # Object
        self.Again = None               # Object (again verb)
        self.CurrentObject = None       # Object (within CurrentDObjList)

        self.CurrentDObjList = []       # Objects
        self.CurrentIObjList = []       # Objects
        self.CurrentAdverbList = []     # Adverb objects

        self.CurrentVerbNoun = None     # Word
        self.CurrentPrepList = []       # WORDS
        self.SaidText = ""              # string

        
        # Disjunctions are currently ignored, but may be used in future enhancements to the
        # parser.

        self.DisjunctionsList = ["but","except"]


        
        #-----------------------
        # Noun/Verb Dictionaries
        #-----------------------

        # The actual heart of the parsing algorhythmn is based on these two
        # dictionaries, so understanding them is vital to understanding the
        # parser.
        #
        # Every discete 'thing' in the game (like a sword or a rock) has 1
        # (or more!) names associated with it. For example, let's say we
        # created an object we named SmallRock in the program. The player
        # can refer to SmallRock either with 'rock' or 'stone' or 'pebble'.
        #
        # Ok, fine. NounsDict will have 3 entries, 'rock', 'stone', and
        # 'pebble'. These are called the KEYS. But what value does each
        # key hold?
        #
        # You guessed it.
        #
        # 'rock': [SmallRock]
        # 'stone': [SmallRock]
        # 'pebble': [SmallRock]
        #

        # Now, let's say we created a second object called Boulder, that
        # the player can refer to as 'boulder', or 'rock', or 'stone'. Now
        # our dictionary looks like:
        #
        # 'rock': [SmallRock, Boulder]
        # 'stone': [SmallRock, Boulder]
        # 'pebble': [SmallRock]
        # 'boulder': [Boulder]
        #
        # Ok, now we know that 'rock; can be either SmallRock or Boulder. How
        # do we tell which one the player meant?
        #
        # If there's any doubt (for example both SmallRock and Boulder are
        # in the same room as the player) the parser will compare the
        # adjectives used. No two objects with the same name should ever
        # have exactly the same list of adjectives, otherwise the parser
        # will go off and sulk.

        self.NounsDict = {}
        
        
        #--------------
        # Parser Errors
        #--------------

        self.NoVerb = "There's no verb in that sentence."
        self.NoPreposition = "'%s' needs a preposition."
        self.NoPreviousCommand = "You haven't done anything yet!"
        self.NoSuchVerbPreposition = "I don't recognize that verb/preposition(s) combination"
        self.MultipleVerbPrepositions = "PROGRAMMING ERROR: Two or more verbs share this verb and preposition combination."
        self.MultipleActors = "You can only tell one thing at a time to do something."
        self.DObjsNotAllowed = "'%s' can't have any direct objects."
        self.IObjsNotAllowed = "'%s' can't have any indirect objects."
        self.NotInVocabulary = "I don't know the word '%s'."

        
        # The PrepsDict dictionary works like the AdjsDict dictionary but
        # holds lists of VERBS, not OBJECTS. For example:
        #
        # 'with': [DigWithVerb, AttackWithVerb]
        # 'from': [TakeFromVerb]
        # 'under': [LookUnderVerb, DigUnderVerb, SearchUnderVerb]
        #
        # The ObjPrepsDict holds the preposition of the object of
        # the verb, for instance "put chest on table into trunk".
        #
        # In this case "into" is the verb preposition, but "on"
        # is the object preposition.

        self.PrepsDict = {}

                #-------------------------
        # Pronouns Dictionary/List
        #-------------------------

        # Pronouns work a little differently. There are 4 kinds, gender
        # neutral singular, gender neutral plural, male, and female singular.
        #
        # The parser uses the PronounsList to search for words in the command

        # which it replaces with the objects from the program dictionary.
        #
        # For instance, let's say the player said "Get Book". The parser
        # (once it knows the player means BlueBook) assigns BlueBook to the
        # PronounsDict entry 'it' (since the book is gender neutral and
        # singular). If the player later says 'Read it', the parser knows
        # "it" refers to BlueBook.

        self.PronounsListDict = {"it": IT,
                                 "them": THEM,
                                 "all": THEM,
                                 "everything":THEM,
                                 "him":HIM,
                                 "her":HER}

        self.PronounsDict = {IT: None,
                             THEM: [],
                             HIM: None,
                             HER: None}


        
        # The VerbsDict works the same way, except we distinguish verbs by
        # the prepositions used with them. For example, 'Look', 'look into
        # mirror', and 'look under bed' are actually three distinct verbs,
        # just as Boulder and SmallRock were two distinct objects. So our
        # VerbDicts dictionary would contain:
        #
        # 'Look': [LookVerb, LookIntoVerb, LookUnderVerb]

        self.VerbsDict = {}

    
    
    #-----------------
    # Get Player Input
    #-----------------

    # This routine takes the player's typed line and turns it into a list
    # of commands which are placed in Global.CommandsList.

    def GetPlayerInput(self):
        """Get Player's command."""
        
        #-------------------
        # Get Player Command
        #-------------------

        # InputString holds the string the player typed. Notice the use of
        # the Prompt function inside the Input function.
        #
        # Next, translate the InputString into a list of words, and put
        # that list in TempWordList.

        InputString = Terminal.Input(self.Prompt(0))
        TempWordList = string.split(InputString)

        
        #-------------------------
        # Handle Punctuation Marks
        #-------------------------

        # So far the list we have contains words seperated by spaces, any
        # punctuation marks will be on the end of individual words. The
        # line below makes punctuation marks their own words.

        TempWordList = self.HandlePunctuation(TempWordList)
        
        
        #---------------------------------------
        # Break Word list into separate commands
        #---------------------------------------

        # Since the player can type muliple commands on a single line
        # (such as "go west then open door" or just "go west. open door")
        # we have to make sure we get all commands.

        #--------------------------------
        # For each word in Temp Word List
        #--------------------------------

        # The FOR loop says in English: "for each word in a COPY of
        # TempWordList do the following...
        #
        # We use a copy because in the course of the FOR loop we're going
        # to completely destroy the real TempWordList.

        for word in TempWordList[:]:
            
            #----------------------
            # Is Word a terminator?
            #----------------------

            # Is the current word in the Global.CommandBreaksList? This
            # list includes all valid ways to end a command. By default
            # this includes all the valid ending sentence punctuation and
            # the word "then" (as in "Go west then open door"). Ending
            # sentence punctuation is assumed to a period, exclamation
            # point, or question mark.

            if word in self.CommandBreaksList:
                
                #-----------------------------
                # Find word's current position
                #-----------------------------

                # We're constantly deleting words from TempWordList, so we
                # need to find the current position of word within the word
                # list. Item will contain the position of word.

                Item = TempWordList.index(word)
                
                #-------------------------------
                # Append Command To CommandsList
                #-------------------------------

                # The command to append to the commands list starts at the
                # beginning of TempWordList and runs up to position Item.
                # The line below will NOT include the actual terminating
                #word in the appended command. So "go west. Open door" will
                # append the command ["go","west"] to the command list, but
                # not include the period.

                self.CommandsList.append(TempWordList[:Item])

                
                #------------------------------
                # Delete command from word list
                #------------------------------

                # Since we no longer need the command we discard everything
                # from the beginning of TempWordList through (and including)
                # the terminating word.
                #
                # In English the code below reads: "Set TempWordList to
                # the remainder of TempWordList from the word after the
                # terminating word till then end of the temp word list.
                #
                # For instance: ["go","west",".","open","door"] becomes
                # ["open","door"].

                TempWordList = TempWordList[Item+1:]


        else:
            
            #-----------------------------------------
            # Remaining TempWordList has no terminator
            #-----------------------------------------

            # This code is part of the FOR/ELSE loop. If we actually
            # have reached this point it means the FOR loop has reached
            # the end of the COPY of TempWordList, but there may still be
            # an extra command in process. Let's examine our example "go
            # west. open door"
            #
            # The copy of TempWordList being processed by the FOR loop
            # ended without a terminator. Therefore the REAL TempWordList
            # still contains ["Open" "Door"]
            #
            # To handle this situation we just append the entire remaining
            # TempWordList (in this case ["open","door"] to the commands
            # list.

            self.CommandsList.append(TempWordList)


        
        #--------------------------------
        # Make Sure last command is valid
        #--------------------------------

        
            # Consider what Global.CommandList will look like if the player
            # types "go west." (ie ends with a period. This yields ["go",
            # "west"],[]] In other words, a bogus last command is introduced
            # into the list.
            #
            # Global.CommandList[-1] means "the last command in the list". If
            # the last command is [] (ie, nothing) then we want to get rid of
            # it. We do that by setting the command list to the command list
            # :-1.
            #
            # In English, :-1 means "from the beginning to the end -1. If the
            # list contained 5 commands, then :-1 would give us the first 4
            # commands.
            

        if self.CommandsList[-1] == []:
            self.CommandsList = self.CommandsList[:-1]

        
        #-------------------------
        # Tell caller we succeeded
        #-------------------------

        # We don't really need to indicate success or failure, since the
        # existing code doesn't check, but it's good programming practice
        # because a game author might rewrite the parser and need to know
        # if this routine succeeded or failed.

        return SUCCESS



    
    #-------------------
    # Handle Punctuation
    #-------------------

    
    # This function takes a list of words like:
    #
    #   ['Joe,','go','west.'] and turns it into:
    #
    #   ['Joe',',','go','west','.']
    #
    # In other words it takes punctuation at the end of a word and inserts
    # it into the list at the appropriate places. This makes single
    # punctuation marks into "words".
    #
    # We do this because from a syntax point of view punctuation marks really
    # *are* seperate words! They add meaning to the sentence, especially for
    # the computer.
    

    def HandlePunctuation(self,WordList):
        """
        Finds punctuation marks at the end of words in a list and inserts
        them as seperate entities in the appropriate part of the list.
        """

        
        #-------------------------
        # Define Punctuation Marks
        #-------------------------

        # These are the punctuation marks people are likely to use. We put
        # them in a single string for convenience, Punctuation could also
        # have stored a list.

        Punctuation = ":;!.,?"
        
        
        #----------------------
        # For Each Word in List
        #----------------------

        # This is a little complex, so pay attention. FOR is a loop, similar
        # to WHILE. But FOR acts differently. We know that WordList contains
        # a list of words. What the FOR loop is saying is: "For each word
        # in WordList put that word in Word (a variable), and do the
        # following..."
        #
        # A couple of cute (and extremely useful tricks). First, notice we
        # are actually using WordList[:] instead of simply WordList. What
        # this does is have FOR use a COPY of WordList, instead of WordList
        # itself. We need to do that because we're going to be changing
        # WordList, and we don't want to confuse Python. Got that? We're
        # changing WordList, we're giving FOR a COPY of WordList. (By the
        # way, WordList[:] means "WordList from the beginning to the end".

        for Word in WordList[:]:
            
            #---------------------------------
            # Word ends in a punctuation mark?
            #---------------------------------

            # You should be familiar with IF tests. This test says "If
            # the last character of Word is in Punctuation (a variable),
            # then do the following...
            #
            # Let's say the player typed "Joe, go west". The WordList will
            # be: ['Joe,','go','west']. The first time though the loop Word
            # will be 'Joe,'.
            #
            # To get a single letter of Word we follow it with the letter's
            # position, starting at 0. Word[0] is 'J', Word[1] is 'o', and
            # so on.
            #
            # But when you use a negative number you're counting from the
            # END of the string. So Word[-1] is ','. In other words Word[-1]
            # will ALWAYS be the last letter, no matter how long Word is!
            # This is the second cute trick I mentioned.

            if Word[-1] in Punctuation:
                
                #----------------------
                # Find Word in WordList
                #----------------------

                # We need to know where the word occurs in the list, so
                # we look it up. The line below sets Item equal to the Word's
                # position in WordList, starting at 0.

                Item = WordList.index(Word)

                
                #------------------------------------------
                # Insert the punctuation mark into the list
                #------------------------------------------

                # We insert the punctuation mark in front of the NEXT word's
                # position in the list. In our example 'Joe,' is word 0, so
                # we insert in front of word 1 ('go')

                WordList.insert(Item+1,Word[-1])
                
                
                #-----------------------------------------
                # Replace Word With Word minus punctuation
                #-----------------------------------------

                # Last cute trick. WordList[Item] is going to be 'Joe,'
                # (notice the ending comma). Word[:-1] means "Word up to
                # but not including the last character". So we replace
                # "Joe," with "Joe". Neat, huh?

                WordList[Item] = Word[:-1]
                

        
        #-------------------------
        # Return Altered Word List
        #-------------------------

        # Ok, we've altered the wordlist the way we want it, so now we
        # return it to the line that called this function.

        return WordList



    
   
    #--------------
    # Default Parser
    #---------------

    # This is the big cheese as far as most developers are concerned. It
    # handles translating the command the player typed into recognizable
    # objects so the parser can then hand off execution to the objects in
    # question.
    #
    # It's reasonably intelligent, it handles multiple commands on a single
    # line, has the ability to handle multiple direct and indirect objects,
    # can handle preparsing and a fair degree of disambiguation, ala TADS.
    #
    # The parser can return SUCCESS or FAILURE. If it returns FAILURE
    # it means the command wasn't understood, SUCCESS means the command
    # was understood and parsed into objects that TurnHandler() can deal
    # with.
    

    def Parser(self):
        """Parsing routine. Almost never overridden"""

        
        #--------------
        # Get a command
        #--------------

    
        # The first thing we have to do is get a command to parse. That
        # isn't as easy as it sounds, for two reasons. First, the player
        # can type multiple commands on a single line, such as
        # "East, then open door" This is two commands "East" and "Open door".
        #
        # Second, if the player does type multiple commands on a single
        # line then the *game loop* has no way to tell if the player typed
        # the commands on one line or several, so the parser has to deal
        # with it.
        #
        # Once the player types a string it is broken down into one or more
        # commands which are put in Global.CommandsList. If there aren't
        # any commands in CommandsList that means we need to go back to the
        # player for another string.

        while len(self.CommandsList) == 0: self.GetPlayerInput()


        
        #--------------------------
        # Get Active (next) command
        #--------------------------

        # The parser places the words from the first command in the list the
        # player typed (Global.CommandsList[0]) into the list the parser
        # actually uses to do the parsing (Global.ActiveCommandList).

        self.ActiveCommandList = self.CommandsList[0]

        
        #-----------------------------
        # Delete it from commands list
        #-----------------------------

        # Now that we've saved the command we're interested in, we delete
        # it from the CommandsList. Doing this does two things. First, it
        # lets us write simpler code (ALWAYS desirable) and it also allows
        # the parser to know when the CommandsList is empty so the parser
        # can ask the player to type in more.

        del self.CommandsList[0]

        
        #----------------------------
        # Delete Trailing Conjuctions
        #----------------------------

        # Because of the nature of English, it's very possible for the
        # player to type in "go west and then open door". This makes our
        # active command list ['go','west','and'], which doesn't make much
        # sense. So we need to make sure the last word isn't a conjunction.
        # To gracefully handle parser abuse (like "go west and and then
        # open door" we use a while loop which will whittle off as many
        # trailing conjunctions as might prove necessary.
        #
        # Translated, the while loop says "While the last word is a
        # conjunction, set the ActiveCommandList to the ActiveCommandList
        # up to but not including the last word."

        while self.ActiveCommandList[-1] in self.ConjunctionsList:
            self.ActiveCommandList = self.ActiveCommandList[:-1]

        
        #-----------------------------
        # Pre-parse the active command
        #-----------------------------

        # Now that we have winnowed a single command from the command list
        # we're ready to apply any pre-parsing rules to the command.

        if not self.PreParse(): return FAILURE

        
        #-------------------
        # Debug Parser Trace
        #-------------------

        # If debug is active then for each word in the active command list print it's
        # part of speech. If it's unrecognized, print "Not In Vocabulary".

        if Global.Debug:
            for Word in self.ActiveCommandList:
                if Global.POSDict.has_key(Word):
                    DebugTrace(Word + ": " + repr(Global.POSDict[Word]))
                else:
                    DebugTrace(Word+": Not In Vocabulary")

        
        #===================
        # Break Down Command
        #===================

        # English is a difficult language to parse. Fortunately, all we have
        # to parse are commands, which, while difficult, always follow a
        # consistant format.
        #
        # The format is:
        #
        # [Actor] VERB [direct object(s)] [preposition] [indirect object(s)]
        #
        # (We're going to ignore the inconvenient form "VERB [direct objects]
        # [Actor]" since it's too difficult to handle cleanly and most
        # people use the first form anyway...)
        #
        # All items in square brackets are optional, which means the only
        # item required in the command is a verb!
        #
        # This suggests the strategy the parser uses to break down the
        # command. First it scans the command for a verb. If it doesn't find
        # a verb, there's nothing more to be done, we complain and return
        # a FAILURE.
        #
        # Assuming we find a verb we save its location. The next thing we do
        # is try and find one or more prepositions, saving the location of
        # the first one we find.
        #
        # The locations of the verb and first preposition are landmarks in
        # the command.
        #
        # Consider the command: "John, dig the hole with the shovel." Since
        # "John" preceeds the verb, we know that John must be the actor,
        # you can't put anything else in front of a verb.
        #
        # Likewise we know "with" is a preposition. Therefore "the hole" is
        # a direct object.
        #
        # And "the shovel" is the indirect object. Translate those
        # (see below) and the parser's job is finished.
        #
        # There's one special case we need to look at. That's a command
        # where the preposition immediately follows the verb, which makes
        # the command's indirect object into the direct object.
        #
        # For example: "Look into chest"
        #
        # Left to itself, chest would become the command's indirect object.
        # However, all we have to do when the first preposition immediately
        # follows the verb is copy the indirect object list into the
        # direct object list and then zap the indirect object list. 

        
        #----------
        # Find Verb
        #----------

        
        # A command can only have one verb in it, so break out of the FOR
        # loop when we find it. If we don't find it complain and return
        # FAILURE.
        #
        # Now to translate the following code into English. First line:
        # "Set PotentialVerbList to an empty list (there aren't any).
        #
        # "For each word in Global.ActiveCommandList, do the following"
        #
        # "If the current word is a verb, then set VerbLocation to the
        # current word's position and then append the VERB'S OBJECT (NOT
        # the word!) to the PotentialVerbList. (We now have one verb
        # object). Since a command may only have one verb we break the
        # FOR loop immediately, stopping our scan.
        #
        # If none of the words in the ActiveCommandList are verbs then
        # we print a complaint ("That sentence doesn't contain a verb!")
        # and immediately return a FAILURE code. This causes the game loop
        # to call the parser again, so the next command can be processed.
        

        PotentialVerbList = []

        for word in self.ActiveCommandList:
            if self.VerbsDict.has_key(word):
                self.CurrentVerbNoun = word
                VerbLocation = self.ActiveCommandList.index(word)
                PotentialVerbList = Union(PotentialVerbList,self.VerbsDict[word])
                break
        else:
            #return Complain(self.NoVerb)
            if self.PreviousVerb is None: return Complain(self.NoVerb)
            self.CurrentVerbNoun = self.PreviousVerb.NamePhrase
            VerbLocation = 0
            PotentialVerbList.append(self.PreviousVerb)
            self.ActiveCommandList = [self.CurrentVerbNoun] + self.ActiveCommandList

        DebugPassedObjList("Potential Verbs",PotentialVerbList)
        
        
        #-----------------
        # Find Preposition
        #-----------------

        # If we get this far we found a verb, now we have to find its
        # prepositions (if any). We start at the verb's location and
        # move to the end of the active command list. If we don't find
        #
        # one the preposition location remains the verb's location.
        #
        # This code is similar to the verb code above, except as noted
        # below.
        #
        # In English: "Set PrepositionList to an empty list (there aren't
        # any). Set FirstPrepositionLocation to VerbLocation".
        #
        # "For each word in Global.ActiveCommandList (starting at the
        # Verb's location and continuing to the end of the list), do the
        # following:"
        #
        # "If the current word is a preposition, append it to
        # Global.CurrentPrepList, append all objects with this preposition
        # to the PrepositionList, then (if this is the first preposition),
        # reset the FirstPrepLocation to the current word's position."
        #
        # Unlike a verb, there can be multiple prepositions in the command,
        # so the FOR loop continues even after we find the first preposition.
        

        self.CurrentPrepList = []
        PrepositionList = []
        FirstPrepLocation = VerbLocation

        if len(self.ActiveCommandList) > 1:
            for word in self.ActiveCommandList[VerbLocation + 1:]:
                if self.PrepsDict.has_key(word):
                    self.CurrentPrepList.append(word)
                    PrepositionList = Union(PrepositionList,self.PrepsDict[word])
                    if FirstPrepLocation == VerbLocation:
                        FirstPrepLocation = self.ActiveCommandList.index(word)
        
        
        #--------------------------------------------
        # Player didn't use a preposition in command?
        #--------------------------------------------

        
        # If the player did NOT use a preposition in the command (like
        # "Take" or "look", then we have a problem. This is because if
        # you intersect any list with an empty list you get an empty
        # list.
        #
        # To solve the problem PAWS requires ALL verbs to have at least one
        # preposition. Verbs that don't normally have a preposition are
        # given the preposition "nopreposition".
        #
        # Let's use "look" as an example. Let's say we have 3 verbs named
        # look, "look", "look into", and "look under". Therefore our
        # potential verb list would be [LookVerb,LookIntoVerb,LookUnderVerb].
        #
        # Let's further assume the player typed "look". The preposition list
        # is empty ([]), but we can't intersect with an empty list, or we'll
        # just get an empty list.
        #
        # So if PrepositionList is empty, we append all the verbs in
        # the preposition dictionary with the name "nopreposition". This
        # makes the preposition list (for instance) [LookVerb, TakeVerb,
        # QuitVerb]. Intersection with our verb list yields exactly one
        # verb! (unless we screwed up and gave two different verbs the
        # same name and preposition(s)!)
       

        if len(PrepositionList) == 0:
            PrepositionList = Union(PrepositionList,self.PrepsDict["nopreposition"])

        DebugPassedObjList("Prepositions",PrepositionList)
       
        
        #============================
        # Positively Identify the Verb
        #=============================

        # It's time to narrow the verb to exactly one candidate. Be aware
        # it's a rule of PAWS that each verb must have a unique name and
        # set of prepositions. For example, you can only have one QuitVerb,
        # since Quit has no prepositions. You can have a look, look into,
        # and look under verb since each "look" verb has a different
        # preposition.
        #
        # There are 3 possible outcomes:
        #
        # 1) We eliminate everything. This means the player either used a
        #verb that doesn't have prepositions with prepositions
        #("quit from here") or used a verb that needed prepositions
        #without any (such as "dig"). We complain and fail.
        #
        # 2) We still have more than one possible verb. This generally
        #means a programming error (two verbs with the same verb
        #name and the same set of prepositions). We complain with a
        #bug report. Make one of the verbs use a different preposition
        #or give it a new name.
        #
        # 3) We only have one verb left. This is only way we continue.
 
        PotentialVerbList = Intersect(PotentialVerbList,PrepositionList)

        DebugPassedObjList("Winnowed Verb List",PotentialVerbList)
    
 
        
        #-------------------------------
        # No Verbs, no prepositions used
        #-------------------------------

        # Remember our VerbPosition and FirstPrepPosition variables?
        # If the player used no prepositions the two values will be
        # equal. If PotentialVerbList is empty and the two values are
        # equal, the player typed a verb that needed one but didn't
        # give us one (like typing "dig" and not saying "with".)

        if len(PotentialVerbList) == 0 and VerbLocation == FirstPrepLocation:
            return Complain(SCase(self.NoPreposition % P.CVN()))

        
        #----------------------------
        # No verbs, prepositions used
        #----------------------------

        # On the other hand, say the player used a preposition with a verb
        # that doesn't have one (like "Quit to DOS". In that case we don't
        # have any intersecting verbs, but since we did have a preposition
        # FirstPrepPosition will be at least one greater than the
        # VerbPosition. (In our example "Quit To DOS" VerbPosition is 0, and
        # FirstPrepPosition is 1.)

        if len(PotentialVerbList) == 0 and VerbLocation < FirstPrepLocation:
            return Complain(self.NoSuchVerbPreposition)

        
        #-------------------------
        # More than one verb left?
        #-------------------------

        # This only happens when the game developer (you) gives two different
        # verbs the same name and preposition. For instance you might have
        # LookInVerb and LookIntoVerb and mistakenly given them both "in"
        # when you really wanted one to have "in" and one to have "into".

        if len(PotentialVerbList) > 1:
            return Complain(self.MultipleVerbPrepositions)

        
        #====================
        # VERB IDENTIFIED!!!!
        #====================

        # By reaching this point we have successfully identified one and
        # only one verb. We also know where the verb is, and where the
        # first preposition is. Given this information we can now set
        # the self.CurrentVerb variable to the first element in
        # PotentialVerbList.

        self.CurrentVerb = PotentialVerbList[0]
        DebugTrace("Current Verb-->"+PotentialVerbList[0].SDesc())
        
        
        #---------------------------
        # Check to see if Again verb
        #---------------------------

        # If the player typed a verb meaning AGAIN, then (assuming they typed
        # a previous command) set the current verb to the previous verb. At this
        # point the direct and indirect object lists haven't been disturbed, so
        # the previous command should execute normally.

        if self.CurrentVerb == self.Again and self.Again <> None:
            DebugTrace("Verb is 'Again' ("+self.Again.SDesc()+")")
            if self.PreviousVerb == None: return Complain(self.NoPreviousCommand)
            self.CurrentVerb = self.PreviousVerb
            return SUCCESS

        
        #---------------------
        # Set Previous Command
        #---------------------

        # This will allow the above command to work when the *NEXT* command is
        # "again".

        self.PreviousVerb = self.CurrentVerb

        
        #===============
        # Identify Actor
        #===============

        
        # The current actor will always be the player's character unless
        # the player puts something in front of the verb. So we play a
        # small programming trick.
        #
        # We deliberately set the current actor to the player. Then we test
        # to see if the verb's position in the command was greater than 0.
        #
        # If not then the player didn't give us an actor. We don't have to
        # do anything else, because the current actor is already the
        # player's object! This is called "defaulting", it's a very useful
        # trick to keep code short and simple.
        #
        # If the verb's position is greater than 0 that means the player
        # typed the name of an actor in front of the verb.
        #
        # We have a special function called ParserIdentifyNoun() that will
        # identify objects in a command. You pass it the starting and
        # ending position within Global.ActiveCommandList and it returns
        # a list of corresponding objects.
        #
        # So we pass it 0 (the start of the command) and VerbPosition.
        #
        # In the command "John, Take the book" this means John is the
        # only word scanned. Thus the function returns [JohnActor] as
        # a single item list of lists.
        #
        # Unfortunately, everything that uses CurrentActor expects it to
        # be a single item, not a list. So we employ a trick called
        # "type conversion" to convert it from a list to a single item.
        # To do that we simply assign the first element of the first list
        # to CurrentActor, this converts it from a list to a single item.
        #
        # The IF test below tests the type of P.CA() against
        # the type of an empty list. If the currentActor is a list, the
        # parser gives up (rather than trying to weed out which object
        # is the actor), complains, and returns FALSE.


        self.CurrentActor = Global.Player

        if VerbLocation > 0:
            self.CurrentActor = self.ParserIdentifyNoun(0,VerbLocation)
            self.CurrentActor = self.CurrentActor[0]
            self.CurrentActor = self.CurrentActor[0]

            if type(self.CurrentActor) == type([]):
                self.CurrentActor = Global.Player
                return Complain(self.MultipleActors)
   
        
        
        #---------------------------
        # Clear Current Adverbs List
        #---------------------------

        # The current adverb list consists of objects that the parser identifies
        # as adverbs. By their nature adverbs will never be anything else, the 
        # word can't also be any other part of speech. 
        
        self.CurrentAdverbList = []
        
        
        
        #-------------------
        # Get Direct objects
        #-------------------

        # Direct objects are the objects the verb acts on. For example,
        # in the command "Take book", "book" is the direct object. The
        # parser uses a simple rule to identify direct objects, they're
        # everything that lie between the verb and the first preposition.
        #
        # There's a special case we need to handle, but that's actually a
        # special case of indirect objects (stay tuned). Notice we use our
        # defaulting trick again.

        self.CurrentDObjList = []

        if len(self.ActiveCommandList) > 1:
            self.CurrentDObjList = self.ParserIdentifyNoun(VerbLocation,FirstPrepLocation)
   
        
        #-----------------
        # Indirect Objects
        #-----------------

        # Indirect objects are those that follow a preposition. In the
        # command "dig hole with shovel", shovel is the indirect object.

        self.CurrentIObjList = []

        if len(self.ActiveCommandList) > FirstPrepLocation + 1:
            self.CurrentIObjList = self.ParserIdentifyNoun(FirstPrepLocation + 1,len(self.ActiveCommandList) + 1)

        
        #---------------------------
        # DIRECT OBJECT SPECIAL CASE
        #---------------------------

        # There is one special case for direct objects. This occurs when
        # the preposition immediately follows the verb. For instance,
        # in the command "Look into chest", "chest" is actually a direct
        # object, although the parser considers it an indirect object.
        #
        # The solution is simple. When the preposition immediately follows
        # a verb, copy the indirect object list to the direct object list,
        # then clear the indirect list.

        if (FirstPrepLocation - VerbLocation) <= 1:
            self.CurrentDObjList = self.CurrentIObjList[:]
            self.CurrentIObjList = []

        
        #------------------
        # That's All, Folks
        #------------------

        # The parser is finished. Notice it doesn't handle disambiguation of
        # objects, that's left to the verbs. You'll notice the BasicVerb
        # object is quite sophisticated, it handles default disambiguation
        # for most cases, you can override specific verbs on a case by case
        # basis.

        DebugTrace("Parsed Verb Is "+self.CurrentVerb.SDesc())
        return SUCCESS


    
    #--------------
    # Identify Noun
    #--------------

    
    # This function returns a list of objects identified by the word range
    # in Global.ActiveCommandList. Objects are identified by zero or more
    # adjectives preceeding a noun. Other parts of speech are ignored by
    # this search.
    #
    # It is very possible for this routine to return a list within a list.
    #
    # For example, let's say the phrase was "stone". This is a noun, and
    # could apply to any of three objects, a small grey stone, a boulder,
    # or a large blue rock. In this case our list is only 1 item long--but
    # that item is a list of 3 objects!
    #
    # Normally the player types something like "Get stone, lamp, and knife".
    # This would return (assuming there's only one knife and lamp object):
    #
    # [Knife,Lamp,[SmallRock,Boulder,BlueRock]]
    #
    # This is a list of 3 items, Knife, Lamp, and the list [SmallRock,
    # Boulder,BlueRock]. The fact we have a list means the verb itself may
    # have to disambiguate further. For example, it makes little sense to
    # try and dig a hole with a lamp, right?


    def ParserIdentifyNoun(self,StartPos,EndPos):
        """Returns a list of objects identified by nouns in Global.ActiveCommandList """

        
        #-------------------
        # Create Empty Lists
        #-------------------

        # We have to create lists for one object's adjectives and nouns. We
        # use a list for nouns (even though an object only has one) because
        # it's possible for more than one object to have the same noun.
        #
        # The Return list returns all objects found (the command list might
        # have listed multiple objects).

        AdjectiveList = []
        NounList = []
        ReturnList = []
        
        
        #----------------------------------
        # Loop through each word in command
        #----------------------------------

        # In English: "For each word in the Active command list from the
        # starting postion up to (but not including) the ending position,
        # do the following..."
        #
        # We take advantage of the fact that all non-verb/preposition words
        # in the command pass through this function eventually. The 
        
        for word in self.ActiveCommandList[StartPos:EndPos]:
            
            #-------------------
            # Word is adjective?
            #-------------------

            # If the word is an adjective, look up all objects that have
            # that adjective and append them to the adjective's list.

            if self.AdjsDict.has_key(word):
                AdjectiveList = Union(AdjectiveList,self.AdjsDict[word])
                DebugTrace(word + " is Adjective")

             
            #--------------
            # Is word noun?
            #--------------

            # When the word is a noun we basically append all objects that
            # have that noun, then (if there were adjectives) intersect the
            # noun and adjective list. Then we append all the objects in
            # the trimmed down NounList to the ReturnList (the list of
            # objects returned by this function).

            if self.NounsDict.has_key(word):
                DebugTrace(word + " is Noun")
                NounList = Union(NounList,self.NounsDict[word])

                if len(AdjectiveList) > 0:
                    NounList = Intersect(NounList,AdjectiveList)

                ReturnList.append(NounList)
                AdjectiveList = []
                NounList = []

            
            #----------------
            # Is Word Adverb?
            #----------------

            # If the word is in the adverbs dictionary append the entry(s) to the 
            # current adverb list. Normally an adverb will be only one object, but
            # it doesn't hurt to have more than one adverb object use the same
            # word.
            
            if self.AdverbsDict.has_key(word):
                self.CurrentAdverbList = Union(self.CurrentAdverbList,self.AdverbsDict[word])
                DebugTrace(word + " is Adverb")


        
        #--------------------------
        # Return Found Objects List
        #--------------------------

        # Now it's time to return the list of objects we parsed from the
        # section of the active command list. Note it's very possible for
        # this function to return an empty list.

        return ReturnList


    
    #--------------------------------------
    # Default Pre-Parse Active Command List
    #--------------------------------------

    # All this routine does by default is put the text of the active
    # command (the command about to be parsed) into the global string
    # variable SaidText, which is used by the "say" verb to Say() what
    # the player typed. This is usually just parroting the player, but
    # can also be used for debugging.

    def PreParse(self):
        """Default routine for pre-parsing a command"""
        
        
        #--------------------------------------------
        # Preserve exact command for debugging system
        #--------------------------------------------

        # notice the said text does not include the verb, it starts at word 1 which
        # excludes word 0 (the verb).

        self.SaidText = string.join(self.ActiveCommandList[1:])

        
        #-------------------------------------------------
        # Force Words In Active Command List To Lower Case
        #-------------------------------------------------

        #----------------------------------
        # Initialize LastWord & CurrentWord
        #----------------------------------

        
            # LastWord is the # of the last word in the active command list. Remember the
            # first word in the list is 0, not 1, which is why we subtract 1 from the
            # actual length of the active command list to find the last word #.
            #
            # This means in a 5 word command the last word is actually word #4
            #
            # Since we want work with one word in the list at a time we need a variable
            # to track which word # we're currently on. We set it to 0 since the first
            # word in the list is 0.


        LastWord    = len(self.ActiveCommandList) - 1
        CurrentWord = 0

        #---------------------
        # Lower Case Each Word
        #---------------------

        
            # We use the more complicated WHILE construct instead of FOR IN so we can
            # lower each list item "in place". This means we avoid having to create
            # a new list and transfer it.
            #
            # The variable Word is purely a coding convenience. We really didn't need to
            # use Word here, we could have used Global.ActiveCommandList[CurrentWord], but
            # Word is much shorter and easier to understand.
            #
            # Notice Word is also forced to lower case using the string.lower() function.
            # We actually want Word in lower case because all the vocabulary dictionaries
            # are in lower case. Since Python says that "WEST" is different than "west"
            # (because of case) we have to make sure to use the same case for everything.
            # PAWS uses lower.
            #
            # If Word is not in the game's vocabulary we complain. Remember that the
            # Complain() function does two things. It types our text on the screen, but it
            # also returns FALSE. That means when we return to the parser the parser will
            # know a problem occurred, and will go back to the player for new input.
            #
            # If we *did* find Word in the vocabulary, we change the current word in the
            # active command list to our lower cased version and then increment
            # CurrentWord by 1.
            #
            # Finally notice we exempt CBE's from being vocabulary checked, since CBE's
            # would *NEVER* be in the vocabulary.


        while CurrentWord <= LastWord:
            Word = string.lower(self.ActiveCommandList[CurrentWord])

            if not InVocabulary(Word) and Word[0]<>"{":
                return Complain(self.NotInVocabulary % Word)

            self.ActiveCommandList[CurrentWord] = Word
            CurrentWord = CurrentWord + 1

        
        #-------------------
        # Translate Pronouns
        #-------------------

        
        #------------------
        # Create Empty List
        #------------------

        # ReturnList will hold the new command, with it, him, her, or
        # them/all/everything translated to the appropriate object names.

        ReturnList = []

        
        #-------------------------
        # For Each Word In Command
        #-------------------------

        
        # The return list is the new command resulting from the translation of
        # pronouns.
        #
        # We look at each word in the active command list, and if it is NOT a
        # pronoun we simply append it to the return list unchanged. If it's a
        # singular pronoun (it/him/her) we get the object's short description
        # and save it.
        #
        # If it's a plural pronoun (them/all/everything) we loop through the
        # resulting list of objects, appending each object's short description
        # to a variable.
        #
        # In either case we then create a list from the resulting set of words
        # and append them to the return list.
        #
        # In the case of "Take it" (where it refers to a rock) the resulting
        # new command would be "take small gray rock". If the command was "Look at
        # them (and them referred to a ring and a sword) then the command would
        # be translated to "look at gold ring sharp sword" (this command will
        # parse correctly, for all it's horrible English).
    

        for word in self.ActiveCommandList:
            
            #-------------------
            # Empty Object Names
            #-------------------

            # This string variable holds one or more pronoun short descriptions.
            # For example if the command was "take it" where it was a ring, then
            # ObjectNames would eventually hold "gold ring".
            #
            # If the command was "take them" where them was a ring and sword then
            # ObjectNames would eventually hold "gold ring sharp sword".


            ObjectNames = ""

            
            #-------------------
            # Is Word A Pronoun?
            #-------------------

            # If the word is a pronoun it will be in the Global.PronounsListDict.
            # has_keys returns true if word is in the dictionary, false if it
            # isn't.

            if P.AP().PronounsListDict.has_key(word):
                

                #------------------
                # Word IS A Pronoun
                #------------------

                # By getting to this point we're convinced the word IS a pronoun
                # that needs to be translated.

                
                #-------------------
                # Get Pronoun Number
                #-------------------

                # There are 4 kinds of pronouns. They're numbered 0 to 3. The 
                # pronouns are listed below:
                #
                # 0 - it
                # 1 - them/all/everything
                # 2 - him
                # 3 - her
                #
                # Everything but pronoun #1 is singular--it can refer only to a
                # single object. Pronoun #1 is PLURAL, it can refer to more than
                # one object. We have to treat singular and plural pronouns very
                # differently, which is why we need to know the pronoun number.
                #
                # The PronounsListDict contains a list of pronouns and their 
                # corresponding numbers, keyed by word.

                PronounNumber = self.PronounsListDict[word]

                
                #-------------------------------
                # Is Pronoun Singular Or Plural?
                #-------------------------------

                # Any pronoun that isn't THEM is singular. Because pronoun numbers
                # are important, each has been given a constant. IT = 0, THEM = 1,
                # HIM = 2, and HER = 3.
                #
                # Thus the IF test below could have been written:
                #
                # if PronounNumber <> 1:
                #
                # We think this way is easier to understand!

                if PronounNumber <> THEM:
                    
                    #--------------------
                    # Pronoun Is SINGULAR
                    #--------------------

                    
                    # If the pronoun is singular we need to get it from the
                    # PronounsDict dictionary, using the Pronoun Number we looked
                    # up above as the key.
                    #
                    # Each time objects are described to the player the parser
                    # automatically sets the values in PronounsDict for you. The
                    # line below sets Object to whatever object the parser last
                    # described to the player for the pronoun in question (the
                    # parser can store 3 objects, one for it, one for him, and one
                    # for her.


                    Object = self.PronounsDict[PronounNumber]

                    #----------------------------
                    # Get words to add to command
                    #----------------------------
 
                    # ObjectNames will contain the words we're going to add to the
                    # command, in this case the object's short description (which,
                    # conveniently is made up of one or two adjectives and a single
                    # noun). Notice if there is no object stored in the pronoun
                    # dictionary we don't replace the pronouns with ANY words.

                    if Object <> None:
                        ObjectNames = Object.SDesc()

                else:
                    
                    #------------------
                    # Pronoun is PLURAL
                    #------------------

                    # If the pronoun used was them, all, or everything then we take
                    # the short description of EACH OBJECT and add it to
                    # ObjectNames. The next step will be to add the words in 
                    # ObjectNames to the command, replacing the plural pronoun.
                    # 
                    # Notice we do NOT add the current actor to the list!

                    ObjectList = self.PronounsDict[PronounNumber]

                    for Object in ObjectList:
                        if Object <> None and Object<> self.CurrentActor and not Object.IsScenery:
                            ObjectNames = ObjectNames + " " + Object.SDesc()



                
                #--------------------------------
                # Add Object Words To Return List
                #--------------------------------

                # ObjectNames contains all the words we want to add to the
                # command regardless of whether the pronoun was singular or
                # plural.

                
                #-------------------------
                # Strip leading whitespace
                #-------------------------

                # Strip off any leading spaces to make the conversion easier.

                ObjectNames = string.lstrip(ObjectNames)

                
                #-------------------------
                # Add Words To Return List
                #-------------------------

                # If ObjectNames has any words in it go ahead and convert the
                # string to a list, then append each word in the list to the
                # return list. Remember, the return list contains the translated
                # command.

                if len(ObjectNames)>0:
                    WordList = string.split(ObjectNames)
                    for word in WordList:
                        ReturnList.append(word)


            else:
                
                #----------------------
                # Word Is NOT A Pronoun
                #----------------------

                # If the word isn't a pronoun we don't need to translate it, so
                # just append it to the ReturnList untouched.

                ReturnList.append(word)

        
        #--------------------------
        # Record Translated Command
        #--------------------------
        
        self.ActiveCommandList = ReturnList

        return SUCCESS

    
    #---------------
    # Default Prompt
    #---------------

    # This function provides the player's prompting character. We define
    # it first because the parser needs it.

    def Prompt(self,PromptArg):
        """Default function to return player prompt"""
        return ">"

    
#--------------------------
# Instantiate Parser Object
#--------------------------

# We instantiate the parser object and immediately place it in the Global object
# so the save/restore routines (which save the Global object) will *also* save the
# parser object, primarily the vocabulary.

Global.ActiveParser = ClassParser()
ParserObject = Global.ActiveParser

#=================================================================================
# Parser Aliasing Object
#=================================================================================

# This object provides short aliases for some of the monster-length properties 
# otherwise required. If you swap out the parser you should create your own
# aliasing class and recreate the P instance with your class.
#
# Note this alias class is NOT based on ClassFundamental(), it's a "lightweight"
# class based directly on the Python's own base object.

class ClassParserAlias:
    """Provides short alias names for commonly used parser related properties"""

    def AP(self): return Global.ActiveParser
    def AVL(self): return Global.ActiveParser.CurrentAdverbList
    def CA(self): return Global.ActiveParser.CurrentActor
    def CV(self): return Global.ActiveParser.CurrentVerb
    def CVN(self): return Global.ActiveParser.CurrentVerbNoun
    def DOL(self): return Global.ActiveParser.CurrentDObjList
    def IOL(self): return Global.ActiveParser.CurrentIObjList
    
P = ClassParserAlias()



#===========================================================================
#                               Engine Class
#===========================================================================

# The class ClassEngine lays out the majority of the runtime system. Along
# with the Global above it makes up about 95% of the runtime system.

class ClassEngine(ClassFundamental):
    """All the game plumbing and wiring"""
    
    #--------------------
    # Initialize function
    #--------------------

    def __init__(self):
        """Sets default instance properties"""
        self.NamePhrase = "Engine Object"
        ClassFundamental.InheritProperties(self)

        
    
    def SetMyProperties(self):

        #----------------------
        # Assign method Aliases
        #----------------------

        
        # We want to set up aliases for the default game engine routines.
        # These aliases are the "functions" called by you the developer, not
        # the default function itself.

        # For example, Prompt is the alias to default_Prompt. Note we're not
        # instantiating an object here, we're assigning an alias. At this
        # point in the code Prompt() and default_Prompt() do exactly the
        # same thing.
        #
        # Why bother, you ask? Because the developer (the game author--you)
        # can replace the default prompt with your own function. Let's say
        # you create a really neat function called MyPrompt().
        #
        # At the end of your function all you have to say is:
        #
        #   Engine.Prompt = MyPrompt
        #
        # and the game engine will start using your prompt instead of the
        # default one! Pretty neat, eh? Notice you don't follow MyPrompt
        # with parentheses, you want to assign the address of your function
        # to Prompt, not the return value!


        self.AfterTurnHandler = default_AfterTurnHandler
        self.BuildStatusLine = default_BuildStatusLine
        self.GameSkeleton = default_GameSkeleton
        self.PreTurnHandler = default_PreTurnHandler
        self.PostGameWrapUp = default_PostGameWrapUp
        self.RestoreFunction = None
        self.SaveFunction = None
        self.SetUpGame = default_SetUpGame
        self.TurnHandler = default_TurnHandler
        self.UserSetUpGame = default_UserSetUpGame
        self.Version = "1.4"
        self.XlateCBEFunction = None


#-------------------
# Instantiate Engine
#-------------------

Engine = ClassEngine()


#===========================================================================
#                                   Base Object
#===========================================================================

# This class is used to extend all "thing" classes. It basically adds the
# current object's name(s) and adjectives to the parser dictionaries. It
# also provides minimal functionality to support the parser.

class ClassBaseObject(ClassFundamental):
    """Base class for all non-verb objects (things)"""
    
    #------------------
    # Instantiate Class
    #------------------

    
    # This method is called ONLY when an object is instantiated. For instance
    # if "rock" were being defined the instantiation would look like:
    #
    # SmallRock = ClassBaseObject("rock,stone","small,grey")
    #
    # This is the equivalent of saying:
    #
    # SmallRock = ClassBaseObject.__init__("rock,stone","small,grey")
    #
    # In other words, you're actually calling the __init__() method when you
    # instantiate a class.
    

    def __init__(self,Name = "",Adjs = "", PluralName = ""):
        """Adds object to appropriate Global lists and dicts"""
        
        #-------------------------------------------------
        # Append Object to Noun and Adjective Dictionaries
        #-------------------------------------------------

        AppendDictList(Global.ActiveParser.NounsDict,Name,self)
        AppendDictList(Global.ActiveParser.NounsDict,PluralName,self)
        AppendDictList(Global.ActiveParser.AdjsDict,Adjs,self)

        
        #--------------------------------------------------
        # Append Vocabulary To Part Of Speech To Dictionary
        #--------------------------------------------------

        AppendDictList(Global.POSDict,Name,"N")
        AppendDictList(Global.POSDict,PluralName,"N")
        AppendDictList(Global.POSDict,Adjs,"A")

        
        #---------------------------
        # Set KeyNoun And NamePhrase
        #---------------------------

        # The KeyNoun lets us find this object in the NounDict for
        # disambiguation purposes. Notice we also set the NamePhrase
        # to the KeyNoun, this allows us to avoid having to set it
        # explicitly.

        NounList = string.split(Name,",")

        if len(NounList) > 0:
            self.KeyNoun = NounList[0]
        else:
            self.KeyNoun = ""

        self.NamePhrase = self.KeyNoun

        
        #--------------------
        # Set AdjectivePhrase
        #--------------------

        AdjectiveList = string.split(Adjs,",")

        if len(AdjectiveList) > 0:
            self.AdjectivePhrase = AdjectiveList[0]
        else:
            self.AdjectivePhrase = ""

        
        #--------------------
        # Set self properties
        #--------------------

        ClassFundamental.InheritProperties(self)



#===========================================================================
#                               Base Verb Object
#===========================================================================

# This class is used to extend all verb classes. It basically adds the
# current verb's name(s) ("go","walk", etc) to the dictionary, along with
# the appropriate prepositions.

class ClassBaseVerbObject(ClassFundamental):
    """Base class for all verbs"""
    
    #------------------
    # Instantiate Class
    #------------------

    
    # This method is called ONLY when an object is instantiated. For instance
    # if "quit" were being defined the instantiation would look like:
    #
    # QuitVerb = ClassBaseVerb("quit")
    #
    # This is the equivalent of saying:
    #
    # QuitVerb = ClassBaseVerb.__init__("quit")
    #
    # In other words, you're actually calling the __init__() method when you
    # instantiate a class.
    #
    # Notice how we default the Preps argument? This way, a developer can
    # easily create verbs that have no prepositions ("quit", "save", etc).

    def __init__(self,Name = "",Preps = "nopreposition"):
        """Adds verb to appropriate Global dicts"""

        
        #-----------------------------------------
        # Append all verb names to verb dictionary
        #-----------------------------------------

        AppendDictList(P.AP().VerbsDict,Name,self)
        AppendDictList(P.AP().PrepsDict,Preps,self)
        
        
        #-----------------------------------------------
        # Append All Verbs To Parts Of Speech Dictionary
        #-----------------------------------------------

        AppendDictList(Global.POSDict,Name,"V")
        AppendDictList(Global.POSDict,Preps,"P")
        
        
        #---------------------------
        # Set KeyNoun And NamePhrase
        #---------------------------

        # The KeyNoun lets us find this object in the NounDict for
        # disambiguation purposes. Notice we also set the NamePhrase
        # to the KeyNoun, this allows us to avoid having to set it
        # explicitly.

        VerbList = string.split(Name,",")

        if len(VerbList) > 0:
            self.KeyNoun = VerbList[0]
        else:
            self.KeyNoun = ""

        self.NamePhrase = self.KeyNoun

        
        #--------------------
        # Set Self Properties
        #--------------------

        ClassFundamental.InheritProperties(self)
        


    
    #------------------------
    # Set Instance Properties
    #------------------------

    def SetMyProperties(self):
        """Sets default instance properties"""
        
        #----------------------------
        # Only Allowed Direct Objects
        #----------------------------

        # This is a "placeholder" list. If any objects are put in this
        # list, they become the only direct objects that can be used with
        # this verb, any other direct objects will cause the verb to fail.
        #
        # This allows a simple way to restrict verbs to certain direct
        # objects.

        self.OnlyAllowedDObjList = []
        
        #------------------------------
        # Only Allowed Indirect Objects
        #------------------------------

        # This is a "placeholder" list. If any objects are put in this
        # list, they become the only indirect objects that can be used with
        # this verb, any other indirect objects will cause the verb to fail.
        #
        # This allows a simple way to restrict verbs to certain objects.


        self.OnlyAllowedIObjList = []
        
        #-----------------
        # Object Allowance
        #-----------------

        # The object allowance property determines what the verb expects
        # in the way of direct and indirect objects. As you can see we
        # set the property by adding two of the object allowance constants
        # together, one for the direct and one for the indirect objects.

        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_ONE_IOBJ

        
        #-----------
        # OK In Dark
        #-----------

        # Set this value to TRUE if the verb can be used in the dark. The
        # default is FALSE.

        self.OkInDark = FALSE

    
    #---------------
    # Execute Method
    #---------------

    
    # The execute method is small, but very flexible. The first thing it
    # does is call the GenericDisambiguate method. The GenericDisambiguate
    # method elminates direct and indirect objects that don't make sense for
    # the verb. In addition, it verifies that verbs that don't allow direct
    # and indirect objects don't have any. If it should fail it returns
    # failure immediately.
    #
    # Then if the SanityCheck() fails we return failure immediately. The
    # SanityCheck allows us a way to test each verb, we replace it the same
    # way we do Action().
    #
    # Finally, if both the GenericDisambiguate() and SanityCheck() methods
    # are successful we return the value of Action() (which will be either
    # SUCCESS or FAILURE).

    def Execute(self):
        """Calls generic disambiguate and if successful, action."""

        if not self.GenericDisambiguate(): return FAILURE
        if not self.SanityCheck(): return FAILURE
        return self.Action()
    
    #---------------------
    # Generic Disambiguate
    #---------------------

    
    # Disambiguate means to remove ambiguity (uncertainty) from something.
    # In this case it means remove the direct and indirect objects that
    # don't make sense in the current context.
    #
    # For instance, this would include objects the current actor (usually
    # the player) hasn't yet encountered, or couldn't know about. In this
    # "generic" disambiguation, we handle situations that are common to
    # ANY game you might write.
    #
    # We also call a specific disambiguate routine at the end of our generic
    # one. This "layered" approach allows us to create a default behavior
    # (aborting disambiguation immediately if there are no objects, and
    # removing unknown objects) as well as library or game specific
    # disambiguation (object isn't here, isn't reachable, is invisible, is
    # locked, etc).

    def GenericDisambiguate(self):
        """Basic disambiguation. Handles no objects, unknown objects. Calls SpecificDisambiguate"""

        DebugTrace("Chosen Verb --> "+self.__class__.__name__)
        
        #-----------------------------------
        # Check for forbidden direct objects
        #-----------------------------------

        # If the verb doesn't allow direct objects, and direct objects were
        # used we complain and return failure. This insures the Execute()
        # method won't call the verb's action.

        if len(P.DOL()) <> 0 and (self.ObjectAllowance & ALLOW_NO_DOBJS > 0):
            return Complain(SCase(P.AP().DObjsNotAllowed % P.CVN()))

        
        #-------------------------------------
        # Check for forbidden indirect objects
        #-------------------------------------

        # If the verb doesn't allow indirect objects, and indirect objects
        # were used we complain and return failure. This insures the
        # Execute() method won't call the verb's action.

        if len(P.IOL()) <> 0 and (self.ObjectAllowance & ALLOW_NO_IOBJS > 0):
            return Complain(SCase(P.AP().IObjsNotAllowed % P.CVN()))

         
        #-----------------------------
        # Call Specific Disambiguation
        #-----------------------------

        # Verbs defined in the library must have a more specific
        # disambiguation routine defined. The library will override our
        # definition of the method with its own. If the disambiguation
        # fails for some reason we will abort the GenericDisambiguation
        # routine, and thus abort the command.

        if not self.SpecificDisambiguate(): return FAILURE

        return SUCCESS

    
    #----------------------
    # Specific Disambiguate
    #----------------------

    # Specific disambiguation handles removing objects specific to the
    # game. This routine will be overridden by the game library, or
    # even specific verbs within the game itself.

    def SpecificDisambiguate(self):
        """Specific disambiguation routine. Overridden by descendents"""
        return SUCCESS

    
    #--------------
    # Verb's Action
    #--------------

    # Although this method is a simple "placeholder" intended to be replaced
    # in every descendent class, the replacement methods are the ones
    # that actually "do" something.
    #
    # The Action() method must always return either SUCCESS or FAILURE,
    # SUCCESS if you want the AfterTurnHandler to run, FAILURE if you
    # don't.

    def Action(self):
        """The action taken by the verb. Overridden by descendants"""
        return FAILURE

    
    # This function is (optionally) implemented on a verb by verb basis
    # (maybe). It's a last ditch effort to make the action fail before
    # it's executed. Return SUCCESS if you want the action to execute,
    # FAILURE if you don't.

    def SanityCheck(self):
        """The sanity check performed by the verb before the action. Overridden by descendents"""
        return SUCCESS

    
    def SDesc(self):
        """Verb short description"""
        return self.NamePhrase
        

#===========================================================================
#                               Adverb Object
#===========================================================================

# This class is used to create adverb objects. An adverb object is basically 
# just the name of the adverb and a method to determine if the adverb was 
# used in the current command.

class ClassAdverb(ClassFundamental):
    """Base class for all adverbs"""
    
    #------------------
    # Instantiate Class
    #------------------

    
    # This method is called ONLY when an object is instantiated. For instance
    # if "quit" were being defined the instantiation would look like:
    #
    # QuitVerb = ClassBaseVerb("quit")
    #
    # This is the equivalent of saying:
    #
    # QuitVerb = ClassBaseVerb.__init__("quit")
    #
    # In other words, you're actually calling the __init__() method when you
    # instantiate a class.
    #
    # Notice how we default the Preps argument? This way, a developer can
    # easily create verbs that have no prepositions ("quit", "save", etc).

    def __init__(self,Name = "",Preps = "nopreposition"):
        """Adds adverb to appropriate Global dicts"""

        
        #---------------------------------------------
        # Append all adverb names to adverb dictionary
        #---------------------------------------------

        AppendDictList(P.AP().AdverbsDict,Name,self)
        
        
        #-----------------------------------------------
        # Append All Verbs To Parts Of Speech Dictionary
        #-----------------------------------------------

        AppendDictList(Global.POSDict,Name,"D")

        
        #---------------
        # Set NamePhrase
        #---------------

        # The KeyNoun lets us find this object in the NounDict for
        # disambiguation purposes. Notice we also set the NamePhrase
        # to the KeyNoun, this allows us to avoid having to set it
        # explicitly.

        AdverbList = string.split(Name,",")
        self.NamePhrase = AdverbList[0]

        
        #--------------------
        # Set Self Properties
        #--------------------

        ClassFundamental.InheritProperties(self)
        

    
    #------------------------
    # Set Instance Properties
    #------------------------

    def SetMyProperties(self):
        """Sets default instance properties"""
        pass
         


    #-----------------
    # Applies() method
    #-----------------
    
    # This method returns TRUE if this adverb was used in the current command,
    # FALSE if it wasn't.
    
    def Applies(self):
        """Has this adverb been used in the current command?"""        
        return (self in P.AVL())
                              


#*********************************************************************
#                          End of PAWS Module
#*********************************************************************
