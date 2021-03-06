
#**********************************************************************************
#                               PAWS Game Skeleton
#                      Written by Roger Plowman (c) 1998-2002
#
# This skeleton provides certain functions that because of Pythonic variable
# scoping rules have to be defined at a higher level than the rest of the game.
# It also handles importing your game library.
#
# Your game library can be called anything you like, the skeleton will load the
# name found as the second argument on the command line. Before trying to do this
# of course it will check to make sure there *is* a second argument on the command
# line!
#
# For example: Python play TQ
#
# TQ.py is the game file you wrote and what play will load.
#
#**********************************************************************************


#----------------------
# Import Needed Modules
#----------------------

# Since there's no repetition between PAWS and Universe, and since
# the Save/Restore game functions defined in this module need everything
# in those modules anyway, we import *everything* from both modules,
# instead of importing only a reference to the module.

from PAWS import *
from Universe import *


#--------------------
# Import Game Library
#--------------------

# Importing the game library is a little trickier since we have to read the line
# the player typed to start the game. To start Thief's Quest, for example, the 
# player should have typed:
#
# Python play TQ
#
# Thus TQ is the second argument on the command line.

#-----------------------------------------
# 2 or more arguments on the command line?
#-----------------------------------------

# sys.argv is the list that contains the command line arguments.The sys module 
# reference was imported as part of the PAWS module import.
#
# If there are more than 2 arguments (just in case the author wants to add some
# after the game's name) then we attempt to load the game, otherwise we complain
# with the proper syntax to run PAWS games.

#if len(sys.argv) >1:
    
    #--------------------------
    # Yes, Attempt To Load Game
    #--------------------------

    # Because of deep Pythonic variable scoping mysteries certain functions have to
    # be defined "above" the game, world library, and engine. That means this
    # module (play) has to be the one to import those modules.
    #
    # Since the player typed command line to start the game we have to check that
    # the player typed a valid game name. We do this by attempting to load the game
    # and seeing if an error (called an "exception" in Python) occurs.
    #
    # The TRY statement attempts to execute the EXEC statement. If an error
    # occurs ("an exception is raised", in Python-speak) the EXCEPT clause will
    # check to see if the error was "ImportError".
    #
    # If an import error did occur then we display an error to the player and shut
    # down Python, returning to the operating system.

try:
   #exec "from %s import *" % sys.argv[1]
   exec "from POTUS import *"
except ImportError:
   Say("Couldn't find that game. You might not have spelled it correctly.")
   sys.exit()

#else:
    
    #-------------
    # No, Complain
    #-------------

    # If there are less than 2 arguments on the command line we print the correct
    # game syntax for the player.

    #Say("To run a game type: Python play <name of game> ~n")
    #Say("For example: Python play TQ ~n")



#----------------------
# Play Module Functions
#----------------------

# These functions must be defined in the module that imports PAWS, Universe, and
# your game to work properly, this has to do with the way Python stores variables.


#----------------------
# Restore Game Function
#----------------------

# This function restores a game previously saved in the passed file name.

def Restore(FileName):
    """Restore previously saved game from disk"""
    
    #---------------------
    # Open Saved Game File
    #---------------------

    # We try and open the saved game, if we can't it's almost always
    # because the player hasn't saved one yet.

    try:
        SavedGame = open(FileName+".PSG","r")
    except:
        Say("You haven't saved a game yet.")
        return FAILURE

    
    #-----------------------
    # Retrieve Global Object
    #-----------------------

    # Because of the nature of pickled objects, we have to manually restore each
    # and every property of each and every object Global refers to. To do that
    # successfully we need SavedObject to be a temporary copy.

    SavedObject = pickle.load(SavedGame)

    
    #-------------------------------------------
    # Restore all properties & objects in Global
    #-------------------------------------------

    # SavedObject has a dictionary that contains each and every
    # property in Global. In addition, it contains a reference to
    # each and every property of each and every object Global
    # referenced when it was saved...
    #
    # Notice FOR uses 2 variables instead of the normal 1. This is ok because
    # the items() method returns a tuple (group) of 2 objects. These two
    # variables are the ones required by the setattr function. Convenient, yes?

    for attr,value in SavedObject.__dict__.items():
        setattr(Global,attr,value)
        DebugTrace("Restoring "+attr)
        
    
    #----------------------
    # Close Saved Game File
    #----------------------

    # Just good programming practice to close what you open.

    SavedGame.close()

    
    #--------------------------------
    # Inform Caller Restore Succeeded
    #--------------------------------

    return SUCCESS


#----------------------------------
# Assign Restore Function To Engine
#----------------------------------


# When PAWS wants to restore the game it won't call Restore() directly, instead
# it will call Engine.RestoreFunction(). The line below makes
# Engine.RestoreFunction an "alias" of Restore(). This alias can be used in
# PAWS, Universe, or TQLib equally well. It's nearly impossible to use
# Restore() directly in those modules because it hasn't been defined within
# them, but Engine.RestoreFunction() was defined by PAWS, which both Universe
# and TQLib know about.


Engine.RestoreFunction = Restore


#-------------------
# Save Game Function
#-------------------

# This function saves the entire game into the file passed to us in
# FileName.

def Save(FileName):
    """Save the game in progress to disk"""
    
    #-------------------------
    # Erase Old Save Game File
    #-------------------------

    # FileName contains the name of the file we're going to save our
    # game into, for exmple TQ.PSG.

    # Since the file may already exist we try and delete it (which is
    # what os.remove() does).
    #
    # If the file DOES NOT exist already the attempt fails and the
    # EXCEPT clause kicks in. The PASS statement does nothing, it's
    # just a "place holder" since there's got to be at least one
    # statement following the EXCEPT. PASS was designed for cases like
    # this!
    #
    # The bottom line is, erase the file if it exists and if it doesn't
    # then don't do anything.
    #
    # By the way, PSG stands for PAWS Save Game.

    try:
        os.remove(FileName + ".PSG")
    except:
        pass

    
    #----------
    # Open File
    #----------

    # We need to create a new file to save our game in. The name of the
    # file is in FileName, by default it will be <game>.PSG,
    # for example "TQ.PSG".
    #
    # SavedGame becomes a reference to the open file.

    SavedGame = open(FileName+".PSG","w")

    
    #-----------------
    # Create PickleJar
    #-----------------

    # PickleJar is just the object that does the pickling. We have to
    # tell it which file to dump the pickles into (SavedGame) and the
    # kind of pickling to use (Binary/Text).
    #
    # We're using Text pickling because it works, binary pickling has a bug that
    # causes it to fail. This is unfortunate because the binary version of the 
    # file is much smaller (and unreadable by players!).

    PickleJar = pickle.Pickler(SavedGame,TEXT_PICKLE)

    
    #-------------------
    # Save Global Object
    #-------------------

    # By dumping the Global object into PickleJar we're *also* pickling
    # any objects Global references, which would include every
    # object in the game.

    try:
        PickleJar.dump(Global)
    except:
        print "save error!"
    
    #----------------------
    # Close Saved Game File
    #----------------------

    # We're finished with the file, so now we have to make sure all
    # the information written to the file is actually on the hard
    # drive and not still in memory, this is what SavedGame.close()
    # REALLY does, in case you're curious.

    SavedGame.close()

    
    #--------------------------------
    # Inform Caller Restore Succeeded
    #--------------------------------

    return SUCCESS


#------------------------------------
# Assign This Save function to Engine
#------------------------------------


# When PAWS wants to save the game it won't call Save() directly, instead
# it will call Engine.SaveFunction(). The line below makes
# Engine.SaveFunction an "alias" of Save(). This alias can be used in
# PAWS, Universe, or TQLib equally well. It's nearly impossible to use Save()
# directly in those modules because it hasn't been defined within
# them, but Engine.SaveFunction() was defined by PAWS, which both Universe
# and TQLib know about.


Engine.SaveFunction = Save


#---------------------------------
# Translate Curly Brace Expression
#---------------------------------

# This function takes a string and translates any valid Python
# expression(s) enclosed within curly braces (the symbols { and })
# into strings and returns the resulting string to the caller.

def TranslateCBExpression(Text=""):
    """Translates {} Python expression into text"""
    
    #---------------------------
    # Convert Text If Wrong Type
    #---------------------------

    # Text might not be a text variable, if it isn't then convert it
    # into text. repr() returns the "representation" of the object,
    # in other words what you'd get at the Python prompt if you tried
    # to print it.

    if type(Text) <> type(""): Text = repr(Text)

    
    #-----------------------
    # Return Text If not CBE
    #-----------------------

    # If this isn't a CBE (Curly Brace Expression) we don't need to
    # translate it, return it as is.

    if "{" not in Text or "}" not in Text: return Text

    
    #-----------------------------------
    # Find { and } Positions Within Text
    #-----------------------------------

    # We need to find the position of the opening and closing curly
    # braces in Text. We'll use this information to replace only
    # that portion of the string with its translation.

    OpenBrace  = string.find(Text,"{")
    CloseBrace = string.find(Text,"}")

    
    #---------------------
    # Try To Translate CBE
    #---------------------

    # Because this is an arbitrary Python expression, and because this
    # function is part of the PAWS debugging system we have no
    # guarantee that the expression is valid. So we try to evaluate it
    # and if it works we then translate the result into a string.
    #
    # If it fails we set the result to "Invalid Curly Brace Expression,
    # Ignored" and continue on our merry way.

    try:
        Expr = eval(Text[OpenBrace+1:CloseBrace])
        if type(Expr) <> type(""): Expr = repr(Expr)
    except:
        Expr = "Invalid CBE '%s'" % Text[OpenBrace+1:CloseBrace]

    
    #------------------------
    # Replace CBE With Result
    #------------------------

    # Here's an interesting bit of slicing and dicing. If you look
    # carefully you'll see we're taking the front part of text (up to
    # but NOT including the open brace), appending the result and the
    # end of Text following the closing curly brace. This neatly snips
    # out the CBE and replaces it with the result of the expression.
    #
    # Since we don't want to disturb the original Text (which might be
    # from anywhere) we put the result in ReturnValue.

    ReturnValue = Text[:OpenBrace] + Expr + Text[CloseBrace + 1:]

    
    #------------------------------
    # Handle CBE Resulting From CBE
    #------------------------------

    # Although you can't nest CBE's (have one CBE inside another), you
    # CAN have one CBE end up evaluating to another. That's why we
    # use the return value as the argument and call THIS SAME FUNCTION
    # again. It's called "recursion".
    #
    #
    # Here's how it might work. Let's say your description contains the
    # CBE {Clock.SoundDesc()}. The CBE evaluates to:
    #
    # "{ClockBird.SoundDesc()}". Obviously you don't want your players
    # seeing that! So the call below would translate the CBE AGAIN.
    #
    # This can occur any number of times and will properly translate.
    # It's unlikely to happen more than once or twice for any given
    # CBE however!

    ReturnValue = TranslateCBExpression(ReturnValue)

    
    #----------------------
    # Return Translated CBE
    #----------------------

    return ReturnValue


#-------------------------------
# Assign This Function To Engine
#-------------------------------


# When PAWS wants to use this function it won't call it directly, instead
# it will call Engine.XLateCBEFunction(). The line below makes
# Engine.XlateCBEFunction an "alias" of this one. This alias can be used in
# PAWS, Universe, or TQLib equally well. It's nearly impossible to use
# TranslateCBEExpression() directly in those modules because it hasn't been
# defined within them, but Engine.XLateCBEFunction() was defined by PAWS,
# which both Universe and TQLib know about.


Engine.XlateCBEFunction = TranslateCBExpression



#-----------------------
# Store Game Module Name
#-----------------------

# sys.argv[1] contains the name of the game module, for instance "TQ". We need this
# for the save/restore file names, which will be <game>.PSG (for instance TQ.PSG).
#

Global.GameModule = "POTUS" # sys.argv[1]


#------------------------
# Set Play Module Version
#------------------------

# PlayModuleVersion is this module's version, which is valuable information since
# you pretty much want to keep the Engine, world library, and play module at the
# SAME version to avoid problems. While every effort is made to keep the three 
# programs backwardly compatible, it's not always possible to do so.

Global.PlayModuleVersion = "1.4"


#---------
# Run Game
#---------

# Engine.GameSkeleton() is the *entire* game! GameSkeleton() won't
# return a value like a normal Python function. Instead it exits
# directly to the operating system (Windows, or Linux, or Mac OS or
# whatever).
#
# Usually the only way to exit GameSkeleton() is for the player to
# type "quit", or to be killed and elect not to restart the game.

Engine.GameSkeleton()


#*********************************************************************************
#                             END OF GAME SKELETON
#*********************************************************************************
