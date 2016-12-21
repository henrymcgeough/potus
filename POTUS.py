#*********************************************************************
#                          POTUS
#
#                      Henry McGeough (c) 2016
#
# You're the President Of The United States (POTUS)
# Can you last 100 days in office without blowing up the Planet?
# We knew you would...
#*********************************************************************


#
# The comments are intended for game authors who've never programmed before,
# they may be a bit long-winded for experienced programmers.
#
# One final note: Python is CASE SENSITIVE, which means not only do you have to
# spell everything correctly, you also have to capitalize it correctly! Almost
# all the truly frustrating problems a beginner will have come from problems
# with capitalization.


#=====================================================================
# Color Codes
#
# This source code is best read with a color coding editor, preferably
# ScopeEdit. I developed using the "Lucinda Console" font, in Bold,
# sized at 15 points in 1280x1024 resolution (large fonts).
#
# The following colors were used:
#
# White Background
# ----------------
#
# Black         - Local Variables, symbols, most Verb Classes
# Grey          - Comments
# Orange        - Quoted Text
#
# Light Blue    - Python & PAWS Module names
# Bright Blue   - Python keywords
# Rose          - Python functions/Object Methods
#
# Purple        - PAWS Constants, numbers
# Pink          - PAWS/POTUS Object Instances
# Red           - PAWS/POTUS Object Methods
# Dark Green    - PAWS/POTUS Object Properties
# Brown         - PAWS/POTUS Classes (excluding most verb classes)
#
# Color Background
# ~~~~~~~~~~~~~~~~
#
# Black On Pink   - Click to zoom into text "fold". Sort of like
#                   a URL on the web, except it shows you the code
#                   labeled by the fold you clicked.
#
#==================================================================

#==================================================================
# A color-coding editor (like ScopeEdit) also helps you keep the
# capitalization of stuff right. If a word doesn't change color you
# either mis-spelled it or didn't capitalize correctly. This helps,
# A LOT!
#
# The color coding editor I used in the creation of this code is
# called ScopeEdit version 1.8. It's shareware and costs $79.00 U.S.,
# but it's worth every penny for 3 reasons. 1) It color codes your
# game so that spelling and capitalization mistakes are easy to catch
# and 2) it has very good basic editing features. It folows Windows
# conventions very closely. (Sorry, ScopeEdit is Windows only).
#
# And 3) it does text folding (aka code nesting). This lets you create
# an outline of your program, one that you can expand or collapse as
# you need to.
#
# PAWS, Universe, and POTUS have all been written with this
# idea in mind. No single part of the code is more than a screenfull
# long. For instance, even though the Universe library is over 5,000
# lines of code, the collapsed outline (using ScopeEdit) fits on a
# single screen!
#
# This simple yet incredibly powerful feature means that you can
# concentrate on a single part of the program, and not be distracted
# by the rest of it.
#
# I've included the ScopeEdit document "Edit Shell.SE" so you can
# look at PAWS with folding if you own a copy of ScopeEdit. I've also
# included the highlighting file "Python.SEO" so you can see the color
# coding.
#
# To download a demo of ScopeEdit off the Web, go to:
#
#   www.loginov.com
#
# If you like it you can register it online with a credit card and
# download the full version immediately.
#
# By the way, I didn't write ScopeEdit, but it's so good I'm willing
# to plug it!
#
# You might also try Origami Gold, a $20 shareware editor (Windows
# only) which not only supports color-coding (limited to 255 keywords
# alas, and it doesn't highlight text) which also does "folding".
# Origami is much cruder than ScopeEdit, and be warned it has a few
# rough edges, but then it's 1/4 the price of ScopeEdit as well.
#
#===========================================================================


#===============================
# Import game engine & libraries
#===============================


# Python doesn't know where any of the other pieces of our game are, so
# we have to tell it. To do this we have to "import" them.
#
# The two most important pieces are the "game engine" and the "world
# library".

# 1. The game engine is the part of the program that does all the "dirty
#    work". For instance it asks the player to enter commands and
#    translates those commands into verbs and objects for you. It handles
#    saving and restoring games, it handles the initial game set up and so
#    forth. The game engine is stored in PAWS.py (source code) and
#    PAWS.pyc (compiled code). Don't change these files! (Unless you
#    REALLY know what you're doing! :))
#
# 2. The world library is the part of the program that builds the
#    underpinnings of the game universe, it defines what a room is, what
#    an actor is, what a door is, and so on. The object library is
#    contained in Universe.py (source code) and Universe.pyc (compiled
#    code) Don't change these files!
#
# Since each of these modules is used in its entirity we import everything,
# that is, we import all objects in these files. This is frowned upon in
# "official" Python circles, but it makes writing the game a LOT easier!


from PAWS import *
from Universe import *

#********************************************************************
#            Natural Language NLTK 3.0
#********************************************************************

#import nltk
import aiml
import os

#********************************************************************
#                          G A M E   D A T A
#********************************************************************

# Here we "fill in the blanks" of Game instance.

Game.Author    = "Harry McGeough"
Game.Copyright = "2016-2017"
Game.Name      = "POTUS: 100 Days"
Game.Version   = "1.0.1 Alpha"


#-----------------------
# Game Introductory Text
#-----------------------


# Python allows you to mark strings with single or double quotes like
# other programming languages you may have used, but it has a new feature
# not available to most: the *TRIPLE* quote.
#
# A triple quote lets you start a string that runs until you end it with
# another triple quote. You can include as many lines of text as you like.
#
# You needn't worry about formatting, either! Since PAWS and Universe
# use the Say() function instead of Python's "print" command PAWS handles
# the formatting.
#
# This means you can make the text attractive in your source code and
# still have it display correctly when the game is played. VERY handy!
#
# Notice how we used the ~n symbol (which causes Say() to line break) in
# combination with the real line breaks? This lets us have the best of
# both worlds, attractive source code and a clear idea of where line
# breaks will occur when the text is said.


Game.IntroText = """
                 After a big party last night following the Presidential Inauguration Ceremony, 
                 this is your first day of being President Of The United States (POTUS). Everyone 
                 thinks you will be the worst President ever, but you plan on proving them wrong.
                 In fact you have managed to finish a secret plan to defeat ISIS, after looking 
                 them up on Google... and it's in your desk draw. You need to go and meet with 
                 The Joint Chiefs who are waiting for you in the Situation Room and start making 
                 America Great Again. ~p
                 """


#********************************************************************************
#                               Adverbs
#
# Adverbs modify verbs, words like "quickly", "slowly", "carefully", etc. They are
# recognizable but don't do anything by default, the Action() method of a verb
# has to specifically modify its action.
#********************************************************************************

CarefullyAdverb = ClassAdverb("carefully")
CloselyAdverb = ClassAdverb("closely")


#***************************************************************************
#                                F U N C T I O N S
#***************************************************************************


#-------------------------------
# POTUS User Set Up Game
#-------------------------------


# This function is essential in any game you write. First, it sets the
# player's character's starting location and second it tells the parser
# who the current actor is before the player types their first command.
#
# When you define this function you also have to tell the Engine to use it
# in place of the PAWS default.
#
# You can probably just copy this function to your own game library and
# rename it from POTUSUserSetUpGame to MyUserSetUpGame or something, then
# change the starting location to your own game's first room.


def POTUSUserSetUpGame():
    """Code required for user game set up"""
    
    #--------------------
    # Is Game Production?
    #--------------------

    # When you create your own game, in your xxUserSetUpGame() function,
    # change Global.Production from FALSE to TRUE when your game is
    # finished. This will disable the Debug verb so players can't
    # cheat by turning on the debugger.

    Global.Production = FALSE

    
    #------------
    # First Actor
    #------------

    # The parser needs to be told who the current actor is because it
    # doesn't know until the player types in their first command. And the
    # first room is entered before that happens...


    P.AP().CurrentActor = Global.Player

    
    #-------------------------------------
    # Player Character's Starting Location
    #-------------------------------------

    # In POTUS (and Universe) the player's character is always
    # referred to as P.CA(). The starting location is the first
    # room the player sees when the game starts. In our case it's the
    # Start Room, the Room with the word START carved on it. :)

    P.CA().StartingLocation = OvalOffice

    
    #---------------------------------
    # Ask About Additional Conventions
    #---------------------------------
    
    Answer = Terminal.Input("This game uses additional conventions most IF doesn't. View them (Y/N)? ")

    if len(Answer)==0: Answer="No"

    if string.lower(Answer[0]) == "y":
        Say("""
            ~n POTUS is a game involving great subtlety--by design. To aid
            you in doing both quick scanning of a scene and detailed analysis POTUS
            uses ~b adverbs. ~l Thus to make a cursory examination of an object
            you'd type 'examine rock' or 'x rock'. To really inspect an item with
            a fine tooth comb you might type 'x rock closely' or 'inspect rock
            carefully'. ~p
            Likewise, if you want to be more precise in other commands you might
            say things like 'take rock carefully', 'move east slowly', etc.~p
            You have to last 100 days to win the game but... in this game a day goes by in an hour.~p          
            The player's character has been forced into a
            situation not of their own choosing where nothing is as it seems and
            paranoia is just common sense. Trust nothing, examine everything,
            believe no one...~p ~m
            """)
    
#--------------------------------------------------
# Replace Engine's default_UserSetUpGame() function
#--------------------------------------------------

Engine.UserSetUpGame = POTUSUserSetUpGame



#*************************************************************************
#                   F O U N D A T I O N   C L A S S E S
#*************************************************************************

# The classes in POTUS deals almost exclusively with room
# extensions, letting us have an Outside and a Office and a Lit Office and
# a Pine Forest and so forth...


#=====================================================================
#                               POTUS Room Class
#=====================================================================


# This room is defined simply to make all rooms have a set of universal
# properties in addition to those supplied by Universe. This allows us
# to test properties without worrying about whether they exist or not.
#
# Notice we're also using the Dictionary description service, this
# replaces the normal sensory descriptions in the room with ones from
# the Descriptions dictionary. This means that all POTUSRooms have
# default sensory description dictionaries.


class ClassPOTUSRoom(ServiceDictDescription,ClassRoom):
    
    #------------------------
    # Set Class's Default Map
    #------------------------

    # The default map is the complaint given when a player moves in a
    # direction the game author didn't set explicitly in the room map. In this
    # case there is *no* default map.

    DefaultMap = {}

    
    #------------------
    # Set My Properties
    #------------------

    # Please note that we call all SetMyProperties() methods (one per
    # service used) before the instance properties, but AFTER the base class
    # SetMyProperties. This allows service-defined properties to be defaulted,
    # yet still overridden by the class being defined.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.HasBeechTree = FALSE
        self.RoomMessageIsVisible = FALSE
        self.HasRoom = FALSE
        self.HasForest = FALSE
        self.HasForestPath = FALSE
        self.HasMound = FALSE
        self.HasPineTree = FALSE
        self.HasStream = FALSE
        self.IsOutside = TRUE

    
    #-----------------
    # Feel Description
    #-----------------

    # The FeelDesc() method supplied by ServiceDictDescription is inappropriate
    # for rooms, so we override it, basically calling ClassRoom's FeelDesc 
    # method.

    def FeelDesc(self): return ClassRoom.FeelDesc(self)


#---------------
# POTUS Class Actor
#---------------

# Just like the regular actor, except it has the Alerted property.

class ClassPOTUSActor(ClassActor):

    def SetMyProperties(self):
        self.Alerted = FALSE
        

#====================================================================
#                               Outside Class
#====================================================================

# This class defines a basic room that has the IsOutside property set
# to TRUE. It's used to handle things like "look at sky", because Sky
# is a floating object who's WHERE() method reports the current
# actor's location when IsOutside is true. Likewise Wall is a
# floating location that reports None when IsOutside is true. (Thus
# "get wall" when outside responds "There's no wall here."

class ClassOutside(ClassPOTUSRoom):
    """Class for a basic outdoors 'room'."""

    #------------
    # Default map
    #------------

    
    # Ok, this is new. DefaultMap is not a normal (instance) property
    # like IsLit or Map, it's a CLASS property.
    #
    # Instance properties are unique to each instance of a class. For
    # example the IsLit property for Clearing can be different than the
    # property for Deep Cave, even though both were created with ClassRoom.
    #
    # This is because IsLit is an instance property. It's unique each and
    # every instance of a class.
    #
    # DefaultMap, on the other hand is the SAME for EVERY instace created
    # from this class.
    #
    # Say you made a Clearing, and a Forest. Both would share the same
    # default map. You can tell the difference between a Class property and
    # an instance property because an instance property definition inside
    # a class always has the word "self." in front of it, where a class
    # property doesn't.

    
    DefaultMap = {North:      "You can't go that way.",
                  Northeast:  "You can't go that way.",
                  East:       "You can't go that way.",
                  Southeast:  "You can't go that way.",
                  South:      "You can't go that way.",
                  Southwest:  "You can't go that way.",
                  West:       "You can't go that way.",
                  Northwest:  "You can't go that way.",
                  Up:         "There's nothing climbable here.",
                  Down:       "There's no way down.",
                  Upstream:   "There's no stream here.",
                  Downstream: "There's no stream here.",
                  In:         "There's nothing here to enter.",
                  Out:        "There's nothing here to exit."}


    def SetMyProperties(self):
        """Sets default instance properties"""
        self.HasWall = FALSE
        self.SetDesc("Odor","All I can smell is fresh air.")


#===========================================================================
#                               Office Class
#===========================================================================

# This is the class for dark Offices. As you can see the default map is
# different, and IsLit is false. (ClassRoom's default is true). The
# DefaultMap Office also has different messages.

class ClassOffice(ClassPOTUSRoom):
    """Class for a basic Office 'room'."""

    
    DefaultMap = {North:      "There is a wall there.",
                  Northeast:  "There is a wall there.",
                  East:       "There is a wall there.",
                  Southeast:  "There is a wall there.",
                  South:      "There is a wall there.",
                  Southwest:  "There is a wall there.",
                  West:       "There is a wall there.",
                  Northwest:  "There is a wall there.",
                  Up:         "Climbing the walls already? Tisk.",
                  Down:       "The floor is in the way.",
                  Upstream:   "There's no stream here.",
                  Downstream: "There's no stream here.",
                  In:         "There's nothing here to enter.",
                  Out:        "There's nothing here to exit."}


    def SetMyProperties(self):
        """Sets default instance properties"""
        self.IsLit = TRUE
        self.IsOutside = FALSE
        self.RoomMessageIsVisible = TRUE
        self.NamePhrase = "Office"
        self.SetDesc("Odor","The air is very fresh, but carries no odors.")
        self.SetDesc("Sound","I can't hear anything.  The silence is deafening.")
        self.SetDesc("Sky","The ceiling is the painted white.")
        self.SetDesc("Ground","The floor is thick carpet.")
        self.HasWall = TRUE
        



#***************************************************************************
#                R O O M S    ( L E V E L   0 - S u r f a c e )
#***************************************************************************


# Rooms are places for the player to visit. Unlike most of what we've seen
# so far, instantiation plays a larger role in distinguishing rooms,
# especially maps.
#
# Rooms are first arranged by level (dungeon level), and within level
# alphabetically by name. The one exception is that the room StartRoom
# (the starting location) is defined first, to make it easy to find.
#
# It doesn't matter what order you define your rooms in, but we have so
# many in POTUS we chose this method to make rooms easier to find.



#===========================================================================
#                           Oval Office (Room #1)
#===========================================================================

# This is the first room the player will see. The game takes place in The
# White House. This President can also use a Limo to visit places in Washington
# reason for the player not to be able to leave the valley.
# or go to Air Force One to fly to other locations. Marine One on the south Lawn
# can be used to visit Camp David.

OvalOffice = ClassOffice()

OvalOffice.NamePhrase = "Oval Office"

OvalOffice.SetDesc("L","""
                       The room features three large south-facing windows behind the president's desk, and a
                       fireplace at the north end. It has four doors: the east door opens to the Rose Garden;
                       the west door leads to a private study and dining room; the northwest door opens onto
                       the main corridor of the West Wing; and the northeast door opens to the office of the
                       President's Secretary. It is the official office of the President of the United States.
                       """)

OvalOffice.SetDesc("Odor","There's a faint whiff of pine needles.")

OvalOffice.SetDesc("Sound","""
                           {SCase(You())} can hear faint buzz of people working.
                           """)

OvalOffice.SetDesc("Ground","""
                            There is a large oval carpet with an American Eagle in the center.
                            """)


#===========================================================================
#                            President's Secretary Office (Room #8)
#===========================================================================

# An easy room, however there's a subtle twist. To get here you travel
# south from the 4 way intersection, but to get back there you have to go
# *west*...
#


Secretary = ClassOffice()

Secretary.NamePhrase = "President's Secretary Office"

Secretary.SetDesc("L","""
                      The Secretary to the President was a former 19th and early 20th century
                      White House position that carried out all the tasks now spread throughout
                      the modern White House Office. The Secretary would act as a buffer between
                      the President and the public, keeping the President's schedules and
                      appointments, managing his correspondence, managing the staff, communicating
                      to the press as well as being a close aide and advisor to the President in a
                      manner that often required great skill and discretion. In terms of rank it is
                      a precursor to the modern White House Chief of Staff.
                      """)



#===========================================================================
#                       Oval Office Fireplace (Room #2)
#===========================================================================

# Just another T in the path.

Fireplace = ClassOffice()

Fireplace.NamePhrase = "Oval Office Fireplace"

Fireplace.SetDesc("L","""
                       There are couches and chairs and a burning fire in the fireplace.
                       Other notable furnishings in the Oval Office are the two paintings
                       that flank the south windows. The Avenue in the Rain by Childe Hassam,
                       1917, depicts Fifth Avenue in New York City adorned with flags and
                       banners in support of the Allied war effort during World War I. The
                       Statue of Liberty by Norman Rockwell was prepared for the cover of
                       The Saturday Evening Post to commemorate the Fourth of July in 1946.
                       """)


#===========================================================================
#                             Corridor (Room #4)
#===========================================================================

# This is the main corridor it leads north to the stairs and is northwest of
# the Oval Office. The Roosevelt Room is northwest and the West wing is west.

Corridor = ClassOffice()

Corridor.NamePhrase = "Corridor"

Corridor.SetDesc("L","""
                      The Corridor leads west into the West Wing offices.
                      The Oval Office is southeast and The Roosevelt is northwest.
                      There is a staircase leading down in the north.
                      """)


#===========================================================================
#                                Roosevelt Room (Room #10)
#===========================================================================

# Nothing special here, but it does contain the only tree in the whole
# forest the player can climb. If they dare...

Roosevelt = ClassOffice()

Roosevelt.NamePhrase = "Roosevelt Room"

Roosevelt.SetDesc("L","""
                       The Roosevelt Room occupies the original location of President Theodore
                       Roosevelt\'s office when the West Wing was built in 1902. This room was
                       once called the Fish Room because President Franklin D. Roosevelt used
                       it to display an aquarium and his fishing mementos. In 1969, President
                       Nixon named the room in honor of Theodore Roosevelt for building the
                       West Wing and Franklin D. Roosevelt for its expansion.

                       On the southeast wall hangs President Theodore Roosevelt\'s Congressional
                       Medal of Honor awarded posthumously on January 16, 2001 to honor his
                       heroism in the Spanish-American War in 1898. To the left of the fireplace
                       hangs President Theodore Roosevelt\'s Nobel Peace Prize, awarded in 1906,
                       for his mediation of the Russo-Japanese War peace settlement. This was the
                       first Nobel Prize awarded to an American.
                       """)


#===========================================================================
#                            White House Rose Garden (Room #16)
#===========================================================================

# The White House Rose Garden is just outside of the Oval Office, an important place.
# The President passes it on his way from the residence to start his day.

RoseGarden = ClassOutside()
RoseGarden.NamePhrase = "White House Rose Garden"

RoseGarden.SetDesc("L","""
                       The White House Rose Garden is a garden bordering the Oval Office and the
                       West Wing of the White House in Washington, D.C., United States. The garden
                       is approximately 125 feet long and 60 feet wide. It balances the Jacqueline
                       Kennedy Garden on the east side of the White House Complex.

                       The West colonnade is north, the South Lawn is south and the Kennedy Garden
                       is east.
                       """)

RoseGarden.SetDesc("Odor","""
                          You can smell pine in the air, like rare
                          perfume.
                          """)

RoseGarden.SetDesc("Sound","""
                           You hear birdsong of surpassing loveliness. Tears
                           spring to your eyes, you feel like bursting into 
                           song yourself.
                           """)

RoseGarden.SetDesc("Sky","""
                         This sky is cloudy and overcast, it looks like it might rain
                         or there may be a storm coming.
                         """)
                         
RoseGarden.SetDesc("Ground","""
                            You are on a stone path but you can see lawns and flowers
                            all around.
                            """)

#===========================================================================
#                            Jacqueline Kennedy Garden (Room #16)
#===========================================================================

# The Jacqueline Kennedy Garden is just outside of the East Wing of the White House.


KennedyGarden = ClassOutside()
KennedyGarden.NamePhrase = "Jacqueline Kennedy Garden"

KennedyGarden.SetDesc("L","""
                       The Jacqueline Kennedy Garden is located at the White House south
                       of the East Colonnade. The garden balances the Rose Garden on the
                       west side of the White House Complex.
                       """)

KennedyGarden.SetDesc("Odor","""
                          You can smell pine in the air, like rare
                          perfume.
                          """)

KennedyGarden.SetDesc("Sound","""
                           You hear birdsong of surpassing loveliness. Tears
                           spring to your eyes, you feel like bursting into
                           song yourself.
                           """)

KennedyGarden.SetDesc("Sky","""
                         This sky is cloudy and overcast, it looks like it might rain
                         or there may be a storm coming.
                         """)

KennedyGarden.SetDesc("Ground","""
                         You are on a stone path but you can see lawns and flowers
                         all around.
                         """)

#===========================================================================
#                            South Lawn (Room #16)
#===========================================================================

# The is used by Marine One Helicopter to fly to Camp David.


SouthLawn = ClassOutside()
SouthLawn.NamePhrase = "South Lawn"

SouthLawn.SetDesc("L","""
                       The South Lawn is the site of the President\'s Marine One arrivals
                       and departures and includes the White House tennis court, putting
                       green, and, as of March 2009, a kitchen garden. The White House
                       Kitchen Garden includes over 50 kinds of vegetables, as well as
                       berries, herbs, and a beehive.

                       Marine One Helicopter is ready to take off in the south.
                       """)

SouthLawn.SetDesc("Odor","""
                          You can smell pine in the air, like rare
                          perfume.
                          """)

SouthLawn.SetDesc("Sound","""
                           You hear birdsong of surpassing loveliness. Tears
                           spring to your eyes, you feel like bursting into
                           song yourself.
                           """)

SouthLawn.SetDesc("Sky","""
                         This sky is cloudy and overcast, it looks like it might rain
                         or there may be a storm coming.
                         """)

SouthLawn.SetDesc("Ground","""
                         You are on a stone path but you can see lawns and flowers
                         all around.
                         """)

#===========================================================================
#                            Marine One Helicopter (Room #36)
#===========================================================================

# An open invitation to a few hours of restful rock climbing...

MarineOne = ClassOffice()

MarineOne.HasMound = TRUE
MarineOne.NamePhrase = "Marine One Helicopter"

MarineOne.SetDesc("L","""
                          Marine One is the call sign of any United States Marine Corps
                          aircraft carrying the President of the United States. The
                          Helicopter is ready to take off. The south lawn is north.
                          """)

MarineOne.SetDesc("Sound","You can hear the wind roaring above you.")

#===========================================================================
#                            West Colonnade (Room #16)
#===========================================================================

# The White House Rose Garden is just outside of the Oval Office, an important place.
# The President passes it on his way from the residence to start his day.

WestColonade = ClassOutside()
WestColonade.NamePhrase = "West Colonnade"

WestColonade.SetDesc("L","""
                       Also known as the '45 second commute,' the West Colonnade was built for
                       Thomas Jefferson to run alongside service spaces underneath the West
                       Terrace, such as the ice house and storage rooms for coal and wood.
                       The open columned walkway is now used by the President and his staff to
                       travel between the West Wing and the Executive Residence.
                       """)

WestColonade.SetDesc("Odor","""
                          You can smell pine in the air, like rare
                          perfume.
                          """)

WestColonade.SetDesc("Sound","""
                           You hear birdsong of surpassing loveliness. Tears
                           spring to your eyes, you feel like bursting into
                           song yourself.
                           """)

WestColonade.SetDesc("Sky","""
                         This sky is cloudy and overcast, it looks like it might rain
                         or there may be a storm coming.
                         """)

WestColonade.SetDesc("Ground","""
                            You are on a stone path but you can see lawns and flowers
                            all around.
                            """)

#===========================================================================
#                            Palm Room(Room #9)
#===========================================================================

# The Palm Room acts as almost a visitor's foyer in the West Wing.

PalmRoom = ClassOffice()

PalmRoom.NamePhrase = "Palm Room"

PalmRoom.SetDesc("L","""
                   The Palm Room acts as almost a visitor's foyer in the West Wing.
                   This room provides access to and from the Rose Garden.
                   """)


#===========================================================================
#                            First Floor Staircase (Room #9)
#===========================================================================

# The staircase leads down to the ground floor.

FirstStaircase = ClassOffice()

FirstStaircase.HasRoom = TRUE
FirstStaircase.NamePhrase = "First Floor Staircase"

FirstStaircase.SetDesc("L","""
                   The staircase leads down to the ground floor. There are exits
                   north leads to Press Room, west to Press Secretary Office, east
                   leads to Cabinet Room and south leads back to a corridor.
                   """)

#===========================================================================
#                            Ground Floor Staircase (Room #9)
#===========================================================================

# The staircase leads up to the first floor.

GroundStaircase = ClassOffice()

GroundStaircase.HasRoom = TRUE
GroundStaircase.NamePhrase = "Ground Floor Staircase"

GroundStaircase.SetDesc("L","""
                   The staircase leads up to the first floor. There are exits southwest
                   to the Situation Room, west leads to the Photo Office and south leads
                   to a Navy Mess.
                   """)

#===========================================================================
#                              The Situation Room (Room #20)
#===========================================================================

# The front porch to the hermit's cave.

Situation = ClassOffice()

Situation.NamePhrase = "The Situation Room "

Situation.SetDesc("L","""
                     Months after being sworn into office, President John F. Kennedy was
                     confronted with the Bay of Pigs Invasion in Cuba and insisted that
                     intelligence information feed directly into the White House.
                     The Situation Room was established in 1961 to meet President Kennedy\'s
                     request.

                     The current Sit Room is a 5,000-square-foot complex of rooms that is
                     staffed 24 hours a day, seven days a week to monitor national and
                     world intelligence information. Televisions for secure video conferences
                     and technology can link the President to generals and world leaders
                     around the globe.
                     """)

Situation.SetDesc("Odor","""
                        Now that you concentrate you can smell the faintest whiff
                        of freshly baked cookies!
                        """)

Situation.SetDesc("Sound","You can hear the sound of deep military thinking.")


#===========================================================================
#                            The Navy Mess (Room 22)
#===========================================================================

# The Navy Mess provides food for te Commander in Chief.

NavyMess = ClassOffice()
NavyMess.NamePhrase = "Navy Mess"

NavyMess.SetDesc("L","""
                            Navy Stewards have provided food service to the Commander in Chief
                            since 1880. The modern White House Navy Mess was established under
                            President Harry S. Truman in 1951. The Navy\'s culinary specialists
                            prepare and serve fine foods in the West Wing. The Staircase leading
                            up is in north and the Situation Room is west.
                            """)

NavyMess.SetDesc("Odor","You smell hot metal and dust.")
NavyMess.SetDesc("Sound","You can hear a faint sound behind the door.")


#===========================================================================
#                            West Wing Entrance (Room #38)
#===========================================================================

# The ledge provides a tease to make the player think it might be a way out.

WestWingEntrance = ClassOffice()
WestWingEntrance.NamePhrase = "West Wing Entrance"

WestWingEntrance.NoExit = """
                   I wouldn't leave here without a security team as there are many assassins.
                   """

WestWingEntrance.SetDesc("L","""
                      This is the entrance to the West Wing. When the President is working in
                      the West Wing, a single U.S. Marine stands sentry outside the north
                      entrance. Working in 30 minute shifts, the Marine Corps members make a
                      strong first impression on the dignitaries, leaders and everyday people
                      who visit the West Wing. The reception room is for visitors of the
                      President, Vice President, and White House staff. The current lobby was
                      renovated by Richard Nixon in 1970 to provide a smaller, more intimate
                      receiving space.

                      The large gilt clock was likely created from assembled parts to imitate
                      an early nineteenth century clock, similar to those used in churches and
                      other public buildings. The artist inscribed the name 'Simon Willard,' an
                      important clock maker at the turn of the nineteenth century.

                      The English-made mahogany bookcase (c.1770) is one of the oldest pieces of
                      furniture in the White House collection.
                      """)

WestWingEntrance.SetDesc("Sound","Just the wind moaning mournfully. Suits your mood perfectly.")
WestWingEntrance.SetDesc("Odor","Nothing in particular assaults your olfactory sense at the moment.")


#===========================================================================
#                        Chief of Staff Office (Room #25)
#===========================================================================

# Just a trick to get the player's hopes up...

ChiefOfStaff = ClassOffice()
ChiefOfStaff.NamePhrase = "Chief of Staff Office"

ChiefOfStaff.SetDesc("L","""
                           The White House chief of staff is the highest ranking employee
                           of the White House. The position is a modern successor to the
                           earlier role of the president's private secretary. The role was
                           formalized as the assistant to the president in 1946 and acquired
                           its current name in 1961.
                           """)

ChiefOfStaff.SetDesc("Sound","You can hear a faint but spine chilling whistling noise.")


#===========================================================================
#                     Vice Presidents Office (Room #13)
#===========================================================================

# The Vice President doesn't do much unless the President dies.

VicePresident = ClassOffice()
VicePresident.NamePhrase = "Vice Presidents Office"


VicePresident.SetDesc("L","""
                           The Office of the Vice President includes personnel who directly
                           support or advise the Vice President of the United States. The
                           Office is headed by the Chief of Staff to the Vice President of
                           the United States, currently Steve Ricchetti. The Office also
                           provides staffing and support to the Second Lady of the United
                           States. It is primarily housed in the Eisenhower Executive Office
                           Building, with offices for the Vice President also in the West Wing,
                           the U.S. Capitol and in the Vice President's official residence.
                           """)

VicePresident.SetDesc("Sound","""
                               You can still hear birds chirping, and the wind in the leaves,
                               but there's also another sound, coming from the trunk, a sort
                               of creaking noise, it's especially loud if you make a sudden
                               movement, and then you can also hear a kind of popping sound.
                               """)


#===========================================================================
#                            Study (Room #31)
#===========================================================================

# Presidents private Study

Study = ClassOffice()
Study.NamePhrase = "Study"

Study.SetDesc("L","""
                       Immediately off the Oval Office, across from the president\'s private
                       lavatory and a small kitchenette, is a very small room used in many
                       administrations as the president's private study."
                       """)

Study.SetDesc("Odor","The air reeks with the smell of old books.")


#===========================================================================
#                         Oval Office Dining Room (Room #32)
#===========================================================================

# Here's the first example of a real cave.

DiningRoom = ClassOffice()
DiningRoom.NamePhrase = "Oval Office Dining Room"

DiningRoom.SetDesc("L","""
                          Just off the Oval Office, through a small corridor past the president\'s
                          private study is the President's West Wing study and dining room, some
                          presidents use a smaller office next door as their private study. In this
                          room, the president may have casual meals alone or with staff and catch
                          the news on television or discuss White House policy. Because this room
                          is usually furnished with a small television, it is often here that the
                          president first sees news events being reported from around the world.
                          """)

DiningRoom.SetDesc("Odor","""
                             The smell of cooked breakfast lingers in the air.
                             """)


#===========================================================================
#                            Lobby (Room #33)
#===========================================================================

# This is where the player's hoard is located

Lobby = ClassOffice()
Lobby.NamePhrase = "Lobby"

Lobby.SetDesc("L","""
                       Before the creation of the Press Briefing Room and offices for journalists, the
                       West Wing Lobby was the location that much news was passed to men from the press.
                       The contemporary lobby is considerably smaller than the 1934 Roosevelt lobby. Its
                       northern section has been walled off to create additional West Wing staff offices
                       and the room has been converted into of a waiting room. A small vestibule provides
                       a formal entry to the space. And there are restrooms off the short corridor between
                       the vestibule and the lobby proper.
                       """)


#===========================================================================
#                                Cabinet Room (Room #17)
#===========================================================================

# Where the President meets his Cabinet to make policies to run the free
# world and make America Great again...

Cabinet = ClassOffice()
Cabinet.NamePhrase = "Cabinet Room"

Cabinet.SetDesc("L","""
                 In the Cabinet Room, the President meets with the Cabinet Secretaries, members of Congress,
                 the National Security Council, and foreign Heads of State on topics ranging from energy
                 efficiency to national security.

                 When the President meets around the large mahogany table with the Cabinet Secretaries, each
                 is assigned a chair based on the date their department was established with the oldest
                 Cabinet departments seated closest to the center. The President sits at the center of the
                 table with his back to the Rose Garden doors and opposite the Vice President.
                 """)

Cabinet.SetDesc("Sound","""
                     You can hear water tinkling faintly in the stream that feeds the pool
                     below you.
                     """)


#===========================================================================
#                                Office of the Press Secretary (Room #6)
#===========================================================================

# Like many of the non-forest rooms this one has most of its properties
# defined directly.

PressSecretary = ClassOffice()

PressSecretary.NamePhrase = "Office of the Press Secretary"

PressSecretary.SetDesc("L","""
                       The White House Office of the Press Secretary, or the Press Office, is responsible for
                       gathering and disseminating information to three principal groups: the President, the
                       White House staff, and the media. The Office is headed by the White House Press Secretary
                       and is part of the White House Office. The Press Office is responsible for providing
                       support and information to the national and international media regarding the President's
                       beliefs, activities and actions.
                       """)

PressSecretary.SetDesc("Odor","""
                          You can smell damp newspapers.  The air is cool like fall and a
                          crispness tickles your nose.
                          """)

PressSecretary.SetDesc("Sound","You can hear the sound of crickets chirping.")


#===========================================================================
#                                Press Briefing Room  (Room #12)
#===========================================================================

# The Press briefing Room is used to brief the Worlds Press on what is giong on
# in the White House.

PressBriefing  = ClassOffice()
PressBriefing.NamePhrase = "Press Briefing Room "


PressBriefing.SetDesc("L","""
                        During the Nixon Administration, more space was required to accommodate the
                        growing press corps. Therefore, in 1970, the briefing room was constructed on
                        top of the emptied pool that was installed for President Franklin D. Roosevelt\'s
                        physical therapy.

                        In 2000, the James S. Brady Press Briefing Room was named in honor of former
                        Press Secretary James Brady. He was shot and disabled during a 1981 assassination
                        attempt on President Ronald Reagan. Today, the current White House press corps is
                        made up of about 200 members. With just 49 chairs (arranged 7 by 7), it is up to
                        the White House Correspondents Association to decide who gets these coveted seats.
                        A plaque on each seat displays the name of the news organization to which it is
                        assigned.
                    """)

PressBriefing.SetDesc("Sound","""
                        You can hear cameras and sound equipment whiring and the clothes rustling.
                        It's quite a soothing sound, almost enough to make you want to go to
                        sleep.
                        """)

#===========================================================================
#                                Press Corps Offices (Room #6)
#===========================================================================

# Press use this room as their offices at the WhiteH House.

PressCorps = ClassOffice()

PressCorps.NamePhrase = "Press Corps Offices"

PressCorps.SetDesc("L","""
                       The White House press corps is the group of journalists or correspondents usually
                       stationed at the White House in Washington, D.C., to cover the President of the
                       United States, White House events, and news briefings. Their offices are located
                       in the West Wing.
                       """)

PressCorps.SetDesc("Odor","""
                          You can smell damp newspapers.  The air is cool like fall and a
                          crispness tickles your nose.
                          """)

PressCorps.SetDesc("Sound","You can hear the sound of crickets chirping.")



#===========================================================================
#                                White House Entrance
#===========================================================================

# entrance to White House has limousine waiting for President


WhiteHouseEntrance = ClassOffice()

WhiteHouseEntrance.NamePhrase = "White House Entrance"

WhiteHouseEntrance.SetDesc("L","""
                       The White House West Wing Entrance, there is a parkerd Presidential Limousine
                       adorned with small American Flags. There are also several Black SUV\'s with
                       darkened windows used by the secret service to guard the President.
                       """)

WhiteHouseEntrance.SetDesc("Odor","""
                          You can smell damp gunpowder.  The air is cool like fall and a
                          crispness tickles your nose.
                          """)

WhiteHouseEntrance.SetDesc("Sound","You can hear the sound of assassins cocking high powered rifles.")

#===========================================================================
#                            Presidential State Car (United States)
#===========================================================================

# The United States presidential state car (nicknamed "The Beast", "Cadillac One", "First Car";
# code named "Stagecoach") is the official state car of the President of the United States.

Limousine = ClassOffice()

Limousine.NamePhrase = "Presidential State Car"

Limousine.SetDesc("L","""
                          The United States presidential state car (nicknamed "The Beast",
                          "Cadillac One", "First Car"; code named "Stagecoach") is the official
                          state car of the President of the United States. The
                          limousine is ready to leave. The White House Entrance is south.
                          """)

Limousine.SetDesc("Sound","You can hear the sound of comfort.")



#*********************************************************************
#                              T H I N G S
#*********************************************************************

# Things, like rooms, are actually objects in the programming sense.
# They are either tools, treasures, or scenery. These objects are ones
# the player will interact with directly.
#
# A tree, an acorn, a person, a sword, a ring--these are all things.




#=====================================================================
#                                   Druid
#=====================================================================

# The druid is another cameo actor, and a non-combatant.  If spoken to
# he will give the player the mandala and instructions on its use. He
# then disappears forever.

class ClassDruid(ClassPOTUSActor):
    """Druid Cameo Actor"""
    
    #------
    # ADesc
    #------

    def ADesc(self): return "him"
    
    #-----------
    # FeelDesc()
    #-----------

    def FeelDesc(self):
        return """
               He doesn't look as though he'd appreciate your pawing
               him.
               """
    
    #-----------
    # HereDesc()
    #-----------

    def HereDesc(self):
        return """
               A robed man stands observing you. A cowl hides his
               face. His hands are hidden in the robe's sleeves.
               """
    
    #------------
    # HelloDesc()
    #------------

    def HelloDesc(self):

        #------------------
        # Make Druid Vanish
        #------------------

        # Move the druid into None and give the player the mandala

        self.MoveInto(None)
        Global.Player.Enter(phone)

        #--------------
        # Give the Clue
        #--------------

        return """
               The man bows to you, and says: "I am Amak, keeper of
               the ancient places.  Welcome, bold adventurer.  Behold
               the Apple iPhone, the sacred phone of the druids.  Take it,
               and let it be your shield and your sword in the places
               of the dark.  To summon its aid, cry aloud the word
               'Siri', but do so only in dire need, for the iPhone 7
               is a sacred object, and not for profane use."  He hands
               you a mobile phone, made from dark metal. Bowing the man 
               turns and disappears into a dark portal.
               """

    
    #--------
    # LDesc()
    #--------

    def LDesc(self):
        return """
               There's not much to see, just an average size man in a
               brown cowled robe. You can't see his face, hands or
               feet.
               """

        
    #-----------
    # OdorDesc()
    #-----------

    def OdorDesc(self):
        return """
               Other than the fact that he's long overdue for a bath,
               you smell nothing unusual about him.
               """
    
    #------------
    # SoundDesc()
    #------------

    def SoundDesc(self): return "He's standing quietly."
    
    #-------
    # Take()
    #-------

    def Take(self,Multiple=FALSE):
        Complain(self.TakeDesc())
    
    #-----------
    # TakeDesc()
    #-----------

    def TakeDesc(self):
        return """
               The man strikes you suddenly, with enough force to
               knock you back. You aren't injured, but the warning is
               obvious.
               """
    
    #------------
    # TasteDesc()
    #------------

    def TasteDesc(self): return "I don't think so!!!!!"
    
    #----------
    # TheDesc()
    #----------

    def TheDesc(self): return "him"


Druid = ClassDruid("man,druid,monk,iPhone salesman","robed,brown,cowled,holy")

Druid.IsHim = TRUE
Druid.StartingLocation = OvalOffice


#=====================================================================
#                                   Chief
#=====================================================================

# The Chief of Staff is another cameo actor, and a non-combatant.
# If spoken to he will give the player the secret plan. He
# then waits for you with joint chiefs in the Situation Room.

class ClassChief(ClassPOTUSActor):
    """Chief of Staff"""

    #------
    # ADesc
    #------

    def ADesc(self): return "him"

    #-----------
    # FeelDesc()
    #-----------

    def FeelDesc(self):
        return """
               He doesn't look as though he'd appreciate your pawing
               him.
               """

    #-----------
    # HereDesc()
    #-----------

    def HereDesc(self):
        return """
               The Chief of Staff, worried looking man in a dark suit.
               """

    #------------
    # HelloDesc()
    #------------

    def HelloDesc(self):

        # Move the Chief Of Staff into Situation Room and give the player the Secret Plan

        self.MoveInto(Situation)
        Global.Player.Enter(plan)

        #--------------
        # Give the Clue
        #--------------

        return """
               The Chief of Staff hands you a manila folder with Top Secert
               written on it. 'Mr. President I've read your plan and written
               some comments on it, the Joint Chiefs are waiting in the
               Situation Room to discuss what we should do about it. I will
               meet you there as I need to brief my staff on the possible
               consequences' the Chief leaves the Oval Office looking even
               more worried.
               """

    #--------
    # LDesc()
    #--------

    def LDesc(self):
        return """
               There's not much to see, just an average size man in a
               dark suit. He looks very worried about something.
               """

    #-----------
    # OdorDesc()
    #-----------

    def OdorDesc(self):
        return """
               You can smell fear and loathing coming in waves.
               """

    #------------
    # SoundDesc()
    #------------

    def SoundDesc(self): return "He's standing quietly."

    #-------
    # Take()
    #-------

    def Take(self,Multiple=FALSE):
        Complain(self.TakeDesc())

    #-----------
    # TakeDesc()
    #-----------

    def TakeDesc(self):
        return """
               The man strikes you suddenly, with enough force to
               knock you back. You aren't injured, but the warning is
               obvious.
               """

    #------------
    # TasteDesc()
    #------------

    def TasteDesc(self): return "I don't think so!!!!!"

    #----------
    # TheDesc()
    #----------

    def TheDesc(self): return "him"


Chief = ClassChief("chief, chief of staff","dark,suit,worried")

Chief.IsHim = TRUE
Chief.StartingLocation = OvalOffice

#=====================================================================
#                                   Secretary
#=====================================================================

# The Chief of Staff is another cameo actor, and a non-combatant.
# If spoken to he will give the player the secret plan. He
# then waits for you with joint chiefs in the Situation Room.

class ClassSecretary(ClassPOTUSActor):
    """Secretary"""

    #------
    # ADesc
    #------

    def ADesc(self): return "her"

    #-----------
    # FeelDesc()
    #-----------

    def FeelDesc(self):
        return """
               She doesn't look as though she'd appreciate your pawing
               her.
               """

    #-----------
    # HereDesc()
    #-----------

    def HereDesc(self):
        return """
               The President\'s Secretary is very busy dealing with the Presidents appointments and schedule.
               """

    #------------
    # HelloDesc()
    #------------

    def HelloDesc(self):

        # Move the Chief Of Staff into Situation Room and give the player the Secret Plan

        #self.MoveInto(Situation)
        Global.Player.Enter(mail)

        #--------------
        # Give the Clue
        #--------------

        return """
               The President\'s Secretary hands you a stack of junk mail
               'Mr. President these are your most pressing messages.
               The chef wanted to know what you wanted for lunch.' the
               Secretary carries on typing at a Computer terminal
               on her desk. Occassionaly answering the phone that seems
               to be constantly flashing.
               """

    #--------
    # LDesc()
    #--------

    def LDesc(self):
        return """
               There's not much to see, just an average size woman in a
               dark business suit with a pecil skirt. She looks very
               worried about something but is incedibly busy.
               """

    #-----------
    # OdorDesc()
    #-----------

    def OdorDesc(self):
        return """
               You can smell hope and optimism coming in waves.
               """

    #------------
    # SoundDesc()
    #------------

    def SoundDesc(self): return "She's sitting at her desk quietly."

    #-------
    # Take()
    #-------

    def Take(self,Multiple=FALSE):
        Complain(self.TakeDesc())

    #-----------
    # TakeDesc()
    #-----------

    def TakeDesc(self):
        return """
               The woman strikes you suddenly, with enough force to
               knock you back. You aren't injured, but the warning is
               obvious.
               """

    #------------
    # TasteDesc()
    #------------

    def TasteDesc(self): return "I don't think so!!!!!"

    #----------
    # TheDesc()
    #----------

    def TheDesc(self): return "her"


PresidentSecretary = ClassSecretary("secretary, Presidents Secretary","dark dress,busy")

PresidentSecretary.IsHim = TRUE
PresidentSecretary.StartingLocation = Secretary

#=====================================================================
#                          Secretary Of State
#=====================================================================

# The Chief of Staff is another cameo actor, and a non-combatant.
# If spoken to he will give the player the secret plan. He
# then waits for you with joint chiefs in the Situation Room.

class ClassSecretaryState(ClassPOTUSActor):
    """Secretary Of State"""

    #------
    # ADesc
    #------

    def ADesc(self): return "her"

    #-----------
    # FeelDesc()
    #-----------

    def FeelDesc(self):
        return """
               She doesn't look as though she'd appreciate your pawing
               her.
               """

    #-----------
    # HereDesc()
    #-----------

    def HereDesc(self):
        return """
               The Secretary Of State looks secretive like she knows something.
               """

    #------------
    # HelloDesc()
    #------------

    def HelloDesc(self):

        # Move the Chief Of Staff into Situation Room and give the player the Secret Plan

        #self.MoveInto(Situation)
        Global.Player.Enter(report)

        #--------------
        # Give the Clue
        #--------------

        return """
               The Secretary Of State hands you a manila folder with images
               from a satellite drone strike and background information
               on ISIS 'Mr. President these are images on the latest drone
               strike against ISIS and current latest strategic information.'
               The Secretary Of State then sits down at the table waiting for
               you to read the information.
               """

    #--------
    # LDesc()
    #--------

    def LDesc(self):
        return """
               There's not much to see, just an average size woman in a
               dark business suit with a pencil skirt. She looks very
               worried about something but is incedibly busy.
               """

    #-----------
    # OdorDesc()
    #-----------

    def OdorDesc(self):
        return """
               You can smell hope and optimism coming in waves.
               """

    #------------
    # SoundDesc()
    #------------

    def SoundDesc(self): return "She's hardly noticable, quite as a mouse."

    #-------
    # Take()
    #-------

    def Take(self,Multiple=FALSE):
        Complain(self.TakeDesc())

    #-----------
    # TakeDesc()
    #-----------

    def TakeDesc(self):
        return """
               The woman strikes you suddenly, with enough force to
               knock you back. You aren't injured, but the warning is
               obvious.
               """

    #------------
    # TasteDesc()
    #------------

    def TasteDesc(self): return "I don't think so!!!!!"

    #----------
    # TheDesc()
    #----------

    def TheDesc(self): return "her"


SecretaryState = ClassSecretaryState("state, 'Secretary of State'","dark leather dress,sexy")

SecretaryState.IsHim = TRUE
SecretaryState.StartingLocation = Situation

#=====================================================================
#                          Joint Chiefs
#=====================================================================

# The Chief of Staff is another cameo actor, and a non-combatant.
# If spoken to he will give the player the secret plan. He
# then waits for you with joint chiefs in the Situation Room.

class ClassJointChiefs(ClassPOTUSActor):
    """Joiunt Chiefs"""

    #------
    # ADesc
    #------

    def ADesc(self): return "them"

    #-----------
    # FeelDesc()
    #-----------

    def FeelDesc(self):
        return """
               They don't look as though she'd appreciate your pawing
               her.
               """

    #-----------
    # HereDesc()
    #-----------

    def HereDesc(self):
        return """
               The Joint Chiefs look a very serious secretive bunch of Generals and
               Admirals who need a strong Commander-in-Chief.
               """

    #------------
    # HelloDesc()
    #------------

    def HelloDesc(self):

        # Move the Chief Of Staff into Situation Room and give the player the Secret Plan

        #self.MoveInto(Situation)
        Global.Player.Enter(report)

        #--------------
        # Give the Clue
        #--------------

        return """
               The Chairman of the Joint Chiefs hands you a manila folder
               with images from a satellite drone strike and background
               information on ISIS 'Mr. President these are images on the
               latest drone strike against ISIS and current latest strategic
               information.' The Chairman then sits down at the table waiting
               for you to read the information.
               """

    #--------
    # LDesc()
    #--------

    def LDesc(self):
        return """
               There's not much to see, just an average size bunch of
               Generals and Admirals, wearing Military uniforms. They look
               worried about nothing and very scary.
               """

    #-----------
    # OdorDesc()
    #-----------

    def OdorDesc(self):
        return """
               You can smell victory, hope and optimism coming in waves.
               """

    #------------
    # SoundDesc()
    #------------

    def SoundDesc(self): return "It's like you hear faint marching music."

    #-------
    # Take()
    #-------

    def Take(self,Multiple=FALSE):
        Complain(self.TakeDesc())

    #-----------
    # TakeDesc()
    #-----------

    def TakeDesc(self):
        return """
               A General strikes you suddenly, with enough force to
               knock you back. You aren't injured, but the warning is
               obvious.
               """

    #------------
    # TasteDesc()
    #------------

    def TasteDesc(self): return "I don't think so!!!!!"

    #----------
    # TheDesc()
    #----------

    def TheDesc(self): return "them"


JointChiefs = ClassJointChiefs("chiefs, joint, 'Joint Chiefs'","military, uniforms, scary")

JointChiefs.IsHim = TRUE
JointChiefs.StartingLocation = Situation


#===========================================================================
#                          POTUS Player
#===========================================================================

# This class extends the Player class from Universe, mainly adding sensory
# descriptions.

class ClassPOTUSPlayer(ClassPlayer):

    
    #----------
    # Feel Desc
    #----------

    def FeelDesc(self): return """
                               You are Mr. President, leader of the Free World...
                               """
    
    #-----------
    # OdorDesc()
    #-----------

    def OdorDesc(self): return """
                               You smell great, just like the US Economy. . .
                               """
    #------------
    # SoundDesc()
    #------------

    def SoundDesc(self): return """
                                You are silently thinking of a plan to make America Great again because... you're smart.
                                """
    #------------
    # TasteDesc()
    #------------

    def TasteDesc(self): return """
                                You (perhaps wisely) decide against trying to
                                taste yourself.
                                """

#------------
# Redefine Me
#------------

POTUSMe = ClassPOTUSPlayer("me,myself, 'Mr. President'")
POTUSMe.Alerted = FALSE

Global.Player = POTUSMe




#----------------------------------------------------------------------
#                               Apple iPhone 7
#----------------------------------------------------------------------

phone = ClassItem("iPhone,phone,mobile")

phone.Bulk = 1
phone.StartingLocation = None
phone.Value = 60
phone.Weight = 1

phone.SetDesc("Feel","""
                       The Apple iPhone is cool and smooth to the touch,it weighs
                       a few ounces but has a curiously solid feel to it.
                       """)

phone.SetDesc("L","""
                    The Apple iPhone 7 is a state of the art smartphone with a
                    digital assistant called Siri. It's very beautiful and
                    obviously valuable as well.
                    """)


phone.SetDesc("Odor","The phone has no odor.")
phone.SetDesc("Taste","The phone doesn't have a taste.")

#----------------------------------------------------------------------
#                               Secret Plan
#----------------------------------------------------------------------

plan = ClassItem("plan, secret")

plan.Bulk = 1
plan.StartingLocation = None
plan.Value = 60
plan.Weight = 1

plan.SetDesc("Feel","""
                       The secret plan feels flimsy.
                       """)

plan.SetDesc("L","""
                    The secret plan is in a manila folder with 'Top
                    Secret' stamped in red. The plan basically talks
                    about Nuking ISIS with a cruise misile from a US
                    Navy ship in the Mediterranean. It goes on to say
                    there would be little fallout and most of this
                    would be political.
                    """)


plan.SetDesc("Odor","The plan really stinks.")
plan.SetDesc("Taste","The plan has a very bad taste.")

#----------------------------------------------------------------------
#                               Nuclear Football
#----------------------------------------------------------------------

football = ClassItem("football, nuclear football, briefcase")

football.Bulk = 1
football.StartingLocation = Secretary
football.Value = 60
football.Weight = 1

football.SetDesc("Feel","""
                    The nuclear football feels solid as a rock.
                       """)

football.SetDesc("L","""
                    The nuclear football is a black briefcase with an
                    lcd activation panel that is activated by the presidents
                    handprint. Once opened the president launch codes are
                    needed to fire nuclear weapons.
                    """)


football.SetDesc("Odor","The nuclear football smells of new leather.")
football.SetDesc("Taste","The football has a very bad taste.")

#----------------------------------------------------------------------
#                               Nuclear Codes
#----------------------------------------------------------------------

codes = ClassItem("Codes, nuclear codes, black wallet")

codes.Bulk = 1
codes.StartingLocation = OvalOffice
codes.Value = 60
codes.Weight = 1

codes.SetDesc("Feel","""
                    The nuclear codes feel extremly dangerous.
                       """)

codes.SetDesc("L","""
                    The nuclear codes is a small black wallet with the
                    president launch codes needed to fire nuclear weapons.
                    The main launch all code seems to be 1234, I think this
                    may be a test code and not actually work.
                    """)


codes.SetDesc("Odor","The nuclear code wallet smells of new leather.")
codes.SetDesc("Taste","The football has an extremly bad taste.")

#----------------------------------------------------------------------
#                               Secret Plan
#----------------------------------------------------------------------

report = ClassItem("report")

report.Bulk = 1
report.StartingLocation = None
report.Value = 60
report.Weight = 1

report.SetDesc("Feel","""
                       The report feels conclusive.
                       """)

report.SetDesc("L","""
                    The report is in a manila folder with 'Above Top
                    Secret' stamped in green. The report basically talks
                    about ISIS, including their known hideouts and current
                    CIA operations.
                    """)


report.SetDesc("Odor","The report smells like victory or naplam.")
report.SetDesc("Taste","The plan has a taste like agent orange.")

#----------------------------------------------------------------------
#                               Junk Mail
#----------------------------------------------------------------------

mail = ClassItem("junk mail, junk, mail")

mail.Bulk = 1
mail.StartingLocation = None
mail.Value = 60
mail.Weight = 1

mail.SetDesc("Feel","""
                       The junk mail feels like a waste of time.
                       """)

mail.SetDesc("L","""
                    The junk mail is in a folder with 'Not
                    Secret' stamped in blue on it. The mail contains
                    unpaid bills, business corrospndance, a post card
                    from Hilary Clinton and a letter from the US Tax office
                    asking about an overdue tax return.
                    """)


mail.SetDesc("Odor","The plan smells fishy.")
mail.SetDesc("Taste","The junk mail has a very bland taste.")


#=====================================================================
#                                    Computer
#=====================================================================


# This computer serves two purposes, one for the player and one for the
# game author.
#
# Since this is the first item players see, they're going to think
# it's important, especially since it emits a green flash when taken.
#
# It actually does contain a cryptic, creepy clue but is otherwise a red herring,
# doing absolutely nothing. You can throw it but it isn't a weapon, nor will it
# damage anything.
#
# For the developer it shows how to define a minimal object. Notice
# we haven't defined any of the major descriptions. This is to show
# you what happens when the default values are used.


Computer = ClassItem("computer,latop,mac","small,silver,metal,illegible,tiny,scratched")
Computer.StartingLocation = Study
Computer.Bulk = 5
Computer.Weight = 10

Computer.SetDesc("Feel","""
                    It weighs about a pound, and is smooth polished metal. It's a typical Apple product.
                    """)

Computer.SetDesc("Take","""
                    The Computer emits a bright flash when you pick it up
                    and the screen turns on when you touch the keyboard or touchpad.
                    """)

Computer.SetDesc("Taste","""
                     It would be tasteless to try and taste it.
                     """)

Computer.SetDesc("Read","""
                    In tiny, almost illegible, scratched letters the words read:
                    'Apple MacBook'
                    """)

Computer.SetDesc("L","""
                 Upon cursory examination the Computer appears to be turned on,
                 with a browser window open to Google waiting for input.
                 """)




#=====================================================================
#                                    Desk
#=====================================================================

# The Desk is just a scenery prop, it does nothing except show news and current affairs shows

desk = ClassScenery("Desk,Resolute","large,huge,enormous,big")
desk.StartingLocation = OvalOffice
desk.Article = "desk"

desk.SetDesc("L","""
                     Resolute Desk is a large, nineteenth-century partners desk mostly chosen
                     by presidents of the United States for use in the White House Oval Office
                     as the Oval Office desk. It was a gift from Queen Victoria to President
                     Rutherford B. Hayes in 1880 and was built from the timbers of the British
                     Arctic exploration ship Resolute.
               """)
desk.SetDesc("Feel","""
                     It weighs about a 500 pounds but except for its large size and weight feels
                     like a normal dark carved victorian desk.
                     """)

desk.SetDesc("Odor","It smells like any other old desk.")

desk.SetDesc("Take","""
                     The Desk is remarkable but it is far to big to carry around.
                     """)

desk.SetDesc("Taste","""
                      The Desk is way too tough to bite thru, and licking it merely
                      leaves a slightly bitter woody taste in your mouth.
                      """)

Global.desk = desk

#=====================================================================
#                                    TV
#=====================================================================

# The TV is just a scenery prop, it does nothing except show news and current affairs shows

tv = ClassScenery("TV,flat screen","large,huge,enormous,big")
tv.StartingLocation = OvalOffice
tv.Article = "tv"

tv.SetDesc("L","The TV\'s are large flat screens, but otherwise unremarkable.")

tv.SetDesc("Feel","""
                     It weighs about a 10 pounds but except for its large size and weight feels
                     like a normal black flat screen TV.
                     """)

tv.SetDesc("Odor","It smells like any other TV")

tv.SetDesc("Take","""
                     The TV\'s are unremarkable, except in size. After examining one you
                     realize its uselessness and drop it.
                     """)

tv.SetDesc("Taste","""
                      The TV\'s is way too tough to bite thru, and licking it merely
                      leaves a slightly bitter plastic taste in your mouth.
                      """)

Global.tv = tv



#===========================================================================
#                                Birds
#===========================================================================

Bird = ClassScenery("bird,birds","singing")
Bird.StartingLocation = RoseGarden

Bird.SetDesc("Feel","""
                         The birds are hidden in the trees, you can't see them,
                         much less touch them. (As if a bird would willingly 
                         let you touch it anyway)
                         """)

Bird.SetDesc("L","""
                      You can't see the birds, only hear them.
                      """)

Bird.SetDesc("Odor","The birds are hidden in the trees, you can't smell them.")

Bird.SetDesc("Sound","""
                          "The birdsong is cheerful, although you can't identify the kinds of
                          birds singing."
                          """)

Bird.SetDesc("Take","""
                         There aren't any birds in sight, only in hearing.
                         """)

Bird.SetDesc("Taste","""
                          You want to lick a bird? Ycch. Besides, all the
                          birds are hidden in the trees, you can see any. Of
                          course no bird would let you get that close anyway.
                          """)


#***************************************************************************
#                                M A P S
#***************************************************************************

# Here's another work around. Because of Python's interpreted nature,
# every object placed in a map dictionary must already be defined.
# Thus we have to add maps AFTER all the rooms they refer to have
# been defined.
#
# It's annoying, but not impossible.


OvalOffice.Map = {North:     Fireplace,
                  Northeast: Secretary,
                  Northwest: Corridor,
                  West:      Study,
                  East:      RoseGarden}

Fireplace.Map = {Northeast: Secretary,
                 East:      RoseGarden,
                 South:     OvalOffice,
                 West:      Study,
                 Northwest: Corridor}

Corridor.Map =  {North:     FirstStaircase,
                 Northwest: Roosevelt,
                 Southeast: OvalOffice,
                 West:      ChiefOfStaff}

Roosevelt.Map = {North:     PressSecretary,
                 Northeast: PressBriefing,
                 East:      FirstStaircase,
                 Southeast: Corridor,
                 South:     DiningRoom,
                 West:      Lobby}

RoseGarden.Map = {North:    WestColonade,
                 Northeast: PalmRoom,
                 Northwest: Cabinet,
                 East:      KennedyGarden,
                 Southeast: SouthLawn,
                 West:      OvalOffice}

KennedyGarden.Map = {Southwest: SouthLawn,
                  West:      RoseGarden}

SouthLawn.Map = {Northeast: KennedyGarden,
                  South:     MarineOne,
                  Northwest: RoseGarden,
                  Up:        "There are no climbable trees here.",
                  Down:      "You can not go down."}

MarineOne.Map = {North:     SouthLawn,
                 Up:        OvalOffice,
                 Down:      SouthLawn}

WestColonade.Map = {North:     PressCorps,
              East:      PalmRoom,
              Southeast: KennedyGarden,
              South:     RoseGarden,
              Southwest: OvalOffice,
              West:      Cabinet,
              Northwest: PressBriefing}

PalmRoom.Map = {Southwest: RoseGarden,
                West:      WestColonade,
                Northwest: PressCorps}

FirstStaircase.Map = {North:     PressBriefing,
                  Northeast: PressSecretary,
                  East:      Cabinet,
                  South:     Corridor,
                  West:      Roosevelt,
                  Down:      GroundStaircase}

GroundStaircase.Map = {South: NavyMess,
                   Southwest: Situation,
                   West:      WestWingEntrance,
                   Up:        FirstStaircase}

NavyMess.Map =    {North:     GroundStaircase,
                   South:     NavyMess,
                   West:      Situation,
                   Northwest: WestWingEntrance}

WestWingEntrance.Map = {North:  WhiteHouseEntrance,
                        East:   GroundStaircase,
                   Southeast:   NavyMess,
                       South:   Situation}

WhiteHouseEntrance.Map = {North: Limousine,
                          South: WestWingEntrance}

Limousine.Map = {South:     WhiteHouseEntrance}

Situation.Map =   {North:     WestWingEntrance,
                   Northeast: GroundStaircase,
                   East:      NavyMess}

ChiefOfStaff.Map = {North:    VicePresident,
                   Northeast: Lobby,
                   East:      DiningRoom}

VicePresident.Map = {East:      Lobby,
                     Southeast: DiningRoom,
                     South:     ChiefOfStaff}

Lobby.Map =           {East:      Roosevelt,
                       Northeast: PressSecretary,
                       South:     DiningRoom,
                       Southwest: ChiefOfStaff,
                       West:      VicePresident}

Cabinet.Map =   {South:     Secretary,
                 East:      RoseGarden,
                 West:      FirstStaircase,
                 Northwest: PressBriefing}

Secretary.Map =  {North:     Cabinet,
                  East:      RoseGarden,
                  Southwest: OvalOffice,
                  West:      FirstStaircase}

Study.Map =          {North:     Corridor,
                      East:      OvalOffice,
                      West:      DiningRoom}

DiningRoom.Map =     {North:     Roosevelt,
                      Northeast: Corridor,
                      East:      Study,
                      West:      ChiefOfStaff}

PressSecretary.Map = {Northeast: PressBriefing,
                      East:      FirstStaircase,
                      South:     Roosevelt,
                      Southwest: Lobby}

PressBriefing.Map = {East: PressCorps,
                     South: WestColonade,
                     Southwest: PressSecretary}

PressCorps.Map = {Northeast:    PalmRoom,
                     South:     WestColonade,
                     West:      PressBriefing}

#*********************************************************************
#                   End of POTUS Game Library
#*********************************************************************
