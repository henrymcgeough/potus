
#*********************************************************************
#                 Universe Object Library For PAWS Engine
#          Written by Roger Plowman & Kevin Russell (c) 1998-2001
#
# This library supplies the basic "laws of nature" for the PAWS engine.
# It provides the basic functionality a game author expects. This is
# the layer most people will think of when they think of PAWS.
#
# Written By: Roger Plowman
# Written On: 08/27/98
#
# Portions By: Kevin Russell
# Written On:  09/14/99
#
#*********************************************************************

#===============================================================================
#                               Contributors
#
# Although I created Universe and wrote most of it, others have contributed 
# significant portions to the whole. Here's a list of who contributed what:
#
# Contributor     Contribution
# -----------     ------------
#
# Kevin Russel    ServiceActivation, ServiceOpenable, 
#                 ServiceContain In/On/Under/Behind, ServiceFollow, 
#                 ServiceOpenable, ServiceLockable, ServiceRevealWhenTaken,
#                 ClassDoor, ClassLockableDoor, ClassUnder/BehindHiderItem,
#                 Insert() method, all verbs to make the above work,
#                 Functions: Agree(), Be(), Have(), Do(), Go(), FollowerDaemon()
#
# Atholbrose      Verbose/Tense Verbs
#
#===============================================================================

#======================================================================
#                            Import needed Modules
#======================================================================

# By importing (a reference) to everything in PAWS.py we gain two 
# benefits. First, we can refer to *anything* in the PAWS module
# without putting "PAWS." in front of it. For example instead of saying
# PAWS.Engine we can just say Engine.
#
# Second, we don't have to perform any imports for the standard modules
# PAWS already imported, which is convenient. Keep in mind, when it
# comes to programming *LAZY IS GOOD*. In this case we save memory
# by not having 2 copies of the same thing, and we also save on typing!

from PAWS import *


#======================================================================
#                        Universe Data & Functions
#======================================================================

# This section contains functions and variables that can be referenced by
# your game library, assuming you include "from Universe import *" in your
# game library.


#-------------------
# Universe Copyright
#-------------------

# Don't change this!

UniverseCopyright = "Copyright (c) 1998 - 2001 by Roger Plowman and Kevin Russell"


#-----------------
# Universe Version
#-----------------

# Do not change this!

UniverseVersion = "1.4"


#---------------------------------------------------------------------------
#                                Universe Banner
#---------------------------------------------------------------------------

# Don't touch this, it must appear in all games (Universe is free, but I want
# people to know who wrote it! <grin> Having this said in all your games is
# the "price" you pay for using Universe.

def UniverseBanner():
    """Says Universe copyright information. Required in all games using Universe!"""

    Text = """
           ~n This game uses Universe version %s, a PAWS class library. ~n %s. ~n Displayed on 
           terminal ~s {Terminal.NamePhrase}. ~l
           ~p
           """

    Text = Text % (UniverseVersion,UniverseCopyright)

    return Text


#---------------------------------------
# Universe Build Status Line replacement
#---------------------------------------

# This function replaces the Engine method that builds the status line to display.
# It puts the score and turn count on the right side of the status line and the 
# game name on the left.

def Universe_BuildStatusLine():
    """Engine.BuildStatusLine replacement"""

    RightSide = " Score: " + repr(Global.CurrentScore) + \
                " Turn: " + repr(Global.CurrentTurn) + "  " 

    SLL = Terminal.MaxScreenColumns
    RSL = len(RightSide)   
    LeftSide = string.ljust(" " + Game.Name[:SLL], SLL)
    Global.StatusLine = LeftSide[:-RSL] + RightSide
    
#-------------------------------
# Replace Engine BuildStatusLine
#-------------------------------

Engine.BuildStatusLine = Universe_BuildStatusLine
    

#---------------------------------------------------------------------------
# Universe SetUpGame replacement
#---------------------------------------------------------------------------

# This function replaces the Engine method of the called at the start of your game. It sets up fuses,
# daemons, and other game mechanics required before the game can begin. It
# also calls UserGameSetup() as the first thing it does.

def Universe_SetUpGame():
    """Engine.SetUpGame replacement"""
    
    #--------------------
    # Clear Contents List
    #--------------------

    # Clear contents lists. This is part of initial set up AND it happens
    # during a restart as well.

    for Object in Global.AllObjectsList: Object.Contents=[]
    
    #--------------
    # Object Set Up
    #--------------

    # In English: For all objects in the AllObjectsList (all "things"), do
    # the following...

    for Object in Global.AllObjectsList:
        
        #--------------------
        # Set Object Location
        #--------------------

        # If the object's starting location is not None (meaning it has no
        # location) then call the object's MoveInto method to move it into
        # the starting location. Notice we don't set the object's location
        # directly!
        #
        # The location of an object is actually stored in two places. First,
        # it's stored in the object's Location property, second it's stored
        # in the contents list of Object's Location.
        #
        # The Location property holds either None or the object that contains
        # the object. (In this case a room is considered a "container",
        # although a special kind of one).
        #
        # Floating objects are special, but the Where() method will tell you
        # the location of any object, floating or not.

        if Object.StartingLocation <> None:
            Object.MoveInto(Object.StartingLocation)
        
        #------------------------
        # Increment Maximum Score
        #------------------------

        # Since the loop we're in runs through all objects, all we need to do is
        # add the object's value (if it has one) to the maximum score.

        if hasattr(Object,"Value"):
            Global.MaxScore = Global.MaxScore + Object.Value

        
        #---------------------------
        # Append Actor To Actor List
        #---------------------------

        # If this object is an actor then we append it to the Actor list.
        # This lets us find it very quickly later if we want to look just
        # for an actor...

        if Object.IsActor: Global.ActorList.append(Object)
        
        
        #---------------------------------
        # Append to Floating Location List
        #---------------------------------

        # If this object has a floating location, then we append it to the
        # floating location object list. This allows us to easily deal with
        # floating objects in the future as a group.

        if Object.HasFloatingLocation: Global.FloatingLocationList.append(Object)

        
        #----------------------------
        # Append To Light Source List
        #----------------------------

        # If this object is a potential light source, append it to the
        # light source list.

        if Object.IsLightSource: Global.LightSourceList.append(Object) 
        
        #-------------------------
        # Append Item To Item List
        #-------------------------

        # If this object is not scenery, then it's takable. then we append it to
        # the Item list.
        # This lets us find it very quickly later if we want to look just
        # for an item...

        if ServiceTakeableItem in ObjectBaseClasses(Object):
            Global.ItemList.append(Object)

        #-------------------------
        # Append Item To Item List
        #-------------------------

        # If this object is not scenery, then it's takable. then we append it to
        # the Item list.
        # This lets us find it very quickly later if we want to look just
        # for an item...

        if Object.IsScenery: Global.SceneryList.append(Object)

    
    #---------------------------
    # Add "Everything" and "All"
    #---------------------------

    # We want to be able to say "Get all" or "Drop everything". In order to
    # do that we simply add two nouns to the NounsDict with values of
    # Global.AllObjectsList. Like so:

    P.AP().NounsDict["everything"] = Global.ItemList
    P.AP().NounsDict["all"]        = Global.ItemList
    
    
    #----------------------
    # Call User Set Up Game
    #----------------------

    # The UserSetUpGame method lets us set information specific to our game,
    # such as some of the Game object properties like Game.Name,
    # Game.Version, etc.

    Engine.UserSetUpGame()
    
    #----------------
    # Call Game Intro
    #----------------

    Game.PrintGameIntroduction()
    
    
    #------------------
    # Start Game Daemon
    #------------------

    # The statement below starts the GameDaemon function running. At the end of
    # each turn the function GameDaemon() will run automatically.

    StartDaemon(GameDaemon)

    
    #----------------------
    # Memorize Ground & Sky
    #----------------------

    # By this time we've already run the UserSetUpGame routine, meaning we know
    # who the current actor is. We need to memorize ground and sky so the
    # player's character knows what they are.

    P.CA().Memorize(Sky)
    P.CA().Memorize(Ground)
    P.CA().Memorize(Wall)
    P.CA().Memorize(NoWall)
    
    
    #-------------------
    # Memorize Inventory
    #-------------------

    # The player already knows about anything he's carrying, so we need to have
    # the player's character memorize it.
    
    for Object in Global.Player.Contents:
        Global.Player.Memorize(Object)


#-------------------------------
# Replace Engine SetUpGameMethod
#-------------------------------

Engine.SetUpGame = Universe_SetUpGame



#--------------------------------------
# Verb Agreement with Subject Functions
#--------------------------------------


#  The arguments of the Agree() function are:
#  Verb:      This is the verb whose format is to be decided.
#  Subject:   This is the Actor whose "you/he/she/they" status the verb
#             should agree with.  If none is given, the verb will agree
#             with the status of the current player.
#  Contract:  if true, Agree() will return a contracted form of the verbs
#             "be" or "have".  contract=1 has no effect on other verbs.
#
#  Some examples of use:
#    """{Global.Player.FormatYou} {Agree('put')} the coin into the slot."""
#
#    """{Fred.FormatYou} {Agree('be',Fred)}n't going anywhere without
#    {Fred.FormatYour} security blanket."""
#
#    """Surprise, {Global.Player.FormatYou}{agree('be',contract=1)} dead."""


def Agree(Verb, Subject=None, Contract=FALSE):
    """Returns proper verb to agree with subject, allows contraction"""

    
    #----------------------------
    # Setting the default subject
    #----------------------------

    # If Agree() wasn't called with a specific subject (in which case
    # the Subject parameter will contain the special None value given
    # to it above in the function header), then we want to set the
    # subject to the current actor.

    if not Subject: Subject = P.CA()

    
    #----------------------------------
    # Strip Leading/Trailing Whitespace
    #----------------------------------

    # Get rid of any leading or trailing whitespace (not that there
    # should be any, of course). This is just adding robustness to
    # the function, 99 times out of 100 it won't make any difference,
    # but that 100'th time...

    Verb = string.strip(Verb)

    
    #---------------------
    # Use Contracted Form?
    #---------------------

    # If the author wants a contraction we have to physically add
    # the word "contracted" for "be" and "have", so we can find it
    # in the VerbAgreementDict. VerbAgreementDict holds exceptions to
    # the general rules of verb agreement (which both "be" and "have"
    # are.

    if Contract and Verb in ["be","have"]: Verb = "contracted" + Verb

    
    #-------------------
    # Is Verb Irregular?
    #-------------------

    # If the verb has irregular forms of subject agreement it will be
    # in VerbAgreementDict. VerbAgreementDict stores a LIST of entries,
    # the first is the plural/you form, the second is the singular
    # form.
    #
    # Note if this IF test is true, the function returns a value and
    # doesn't continue.

    if Global.VerbAgreementDict.has_key(Verb):
        if Subject.FormatYou == "you" or Subject.IsPlural:
            return Global.VerbAgreementDict[Verb][0]
        else:
            return Global.VerbAgreementDict[Verb][1]

    
    #------------------------------------
    # Verb Is Regular. Is Subject Plural?
    #------------------------------------

    # Getting this far means the verb wasn't in VerbAgreementDict so
    # it wasn't an irregular verb.
    #
    # If the subject is "you" or the subject is plural (like "they")
    # then just return the verb you were sent and the function stops
    # here.

    if Subject.FormatYou == "you" or Subject.IsPlural: return Verb

    
    #-------------------------------------
    # Verb Is Regular, Subject is Singular
    #-------------------------------------

    # We"re dealing with a third person singular.
    # First handle the case where the Verb ends in "y": if the
    # second last letter is not a vowel, the "y" should be
    # replaced with "ies", otherwise just add "s"

    if Verb[-1] == "y" and Verb[-2] not in "aeiou":
        return Verb[:-1]+"ies"
    else:
        return Verb+"s"



#-----------------------------------------
# Four Specialized Forms Of Verb Agreement
#-----------------------------------------

#  Four convenient abbreviations for agree().
#  These will let you write a statement like:
#     """{Global.Player.FormatYou} {be()} now dead."""
#  rather than:
#     """{Global.Player.FormatYou} {agree("be")} now dead."""

def Be(Subject = P.CA(), Contract=FALSE):
    return Agree("be", Subject, Contract)

def Have(Subject = P.CA(), Contract=FALSE):
    return Agree("have", Subject, Contract)

def Do(Subject = P.CA(), Contract=FALSE):
    return Agree("do", Subject, Contract)

def Go(Subject = P.CA(), Contract=FALSE):
    return Agree("go", Subject, Contract)


#----------------
# Follower Daemon
#----------------

# This function is a DAEMON, a function that will be run automatically every turn
# by the game engine (when started with the StartDaemon function)

def FollowerDaemon():
    """Daemon to have things follow player"""

    for actor in Global.ActorList:
        if not actor.Get("Follow") == None: actor.FollowPlayer()


#---------------------------------------------------------------------------
# Increment Score
#---------------------------------------------------------------------------

# This function increments the player's score, and lets the player know when
# it happens. Use this function with a negative Amount to reduce the player's
# score.

def IncrementScore(Amount,Silent=FALSE):
    """Increments player's score and tells them."""

    
    #-----------------------
    # Adjust Score By Amount
    #-----------------------

    Global.CurrentScore = Global.CurrentScore + Amount
    
    #---------------------------------
    # Determine proper word for Change
    #---------------------------------

    # We want to say decreased for a negative amount, increased for a
    # positive one, and nothing at all for a 0 amount.

    ChangeWord = ""
    if Amount < 0: ChangeWord = "decreased"
    if Amount > 0: ChangeWord = "increased"
    
    #--------
    # Plural?
    #--------

    # It's 1 point, but otherwise 0 points, 2 points, etc...

    PluralWord = "points"
    if abs(Amount) == 1: PluralWord = "point"
    
    #--------------
    # Build Comment
    #--------------

    Comment = "[Your score just %s by %d %s.] ~p" % (ChangeWord,Amount,PluralWord)
    
    #------------------------
    # Say it if score changed
    #------------------------

    # If the score changed and Silent is false (not TRUE is FALSE) then
    # say comment, otherwise don't. Silent score changes can be handy
    # if you don't want the player to know when their score changes.

    if Amount <> 0 and not Silent:
        Say(Comment)
        Terminal.DisplayStatusLine(Global.StatusLine)


#--------------------------------------
# Shortcuts For Curly Brace Expressions
#--------------------------------------

# These expressions are shortcuts for the longer expressions they 
# return. They're intended to be used inside CBE's, for instance:
#
# "{Me()}"
#
# Instead of the longer:
#
# "{Global.Player.FormatMe}"

def Me(): return P.CA().FormatMe
def You(): return P.CA().FormatYou
def Your(): return P.CA().FormatYour
def Youm(): return P.CA().FormatYoum





#======================================================================
#                         Additional Parser Errors
#======================================================================

# In this section we append new properties to the ParserError object, which
# we can freely use just as though they were added in the PAWS.py module.
# This hides the internal workings of ParserError from the game author (you)
# so you don't have to worry which parts are from PAWS and which parts are
# from Universe.

P.AP().Nonsense = "That doesn't make sense."
P.AP().NotADirection = "{You()} can't go that way!"
P.AP().NotAnActor = "You have lost your mind."
P.AP().ObjectNotHere = "There's no %s here."
P.AP().OnlyOneDObj = "You can only use one direct object with this verb."
P.AP().OnlyOneIObj = "You can only use one indirect object with this verb."
P.AP().TooDark = "It's too dark to see how."


#======================================================================
#                           Additional Global Variables
#======================================================================

# In this section we append new properties to the Global object, which, like
# our additions to ParserObject above, the game author can use freely without
# having to worry if they're PAWS stuff or Universe stuff.


#-----------
# Actor List
#-----------

# This list is constructed by the Engine.PreInit() method. It contains a
# list of all objects that have Actor as a class. It's a quick way to limit
# your search to just actors.

Global.ActorList = []

#-----------------
# All Objects List
#-----------------

# Lists all Thing objects. Useful for scanning all objects or setting
# up the game locations.

Global.AllObjectsList = []


#--------------
# Current Score
#--------------

# You guessed it, the player's current score. This is the value displayed
# on the status line.

Global.CurrentScore = 0

#------------
# Curent Turn
#------------

# This is the turn count displayed on the status line, it controls fuses,
# daemons, etc.

Global.CurrentTurn = 0


#------------------------------
# Floating Location Object List
#------------------------------

# This list is constructed by the SetUpGame() method. It contains a
# list of all "floating location" objects. A floating location object is one
# that has no fixed location, it can move with the player.
#
# Floating objects are handy for creating floors, ceilings, walls, etc.
# They're a kind of like Scenery for the Me object, invisible but always
# around so the player can say things like "Climb walls".

Global.FloatingLocationList = []

#----------
# Item List
#----------

# Lists all Item (takeable) objects. Useful for the "take/drop all" pronoun.


Global.ItemList = []


#------------------
# Light Source List
#------------------

# This list is constructed by the PreInit() function. It contains a list
# of all objects that have a true IsLightSource property. This list is
# used anywhere we need to scan a list of light sources.

Global.LightSourceList = []

#----------------
# Lit Parent List
#----------------

# This list is maintained by the AfterTurnHandler, it contains a list of
# all parent objects (containers or rooms) that are illuminated by a light
# source--excluding naturally lit rooms like the outdoors, or a room with
# a window to the outdoors.

Global.LitParentList = []


#--------------
# Maximum Score
#--------------

# You guessed it, the player's maximum (winning) score.

Global.MaxScore = 0


#-----------------
# Restarting Game?
#-----------------

# This is either true or false, it's used by certain commands to know
# whether or not the game should be restarted.

Global.Restarting = FALSE


#-------------
# Scenery List
#-------------

# Lists all scenery (non-takable) objects.

Global.SceneryList = []
             

#--------
# Verbose
#--------

# Verbose is either TRUE or FALSE. If true then room long descriptions will
# always be said whether or not the player has already been in the room.
# The default is FALSE, so the long description is only said # the first
# time the player vists a room, or types "look".

Global.Verbose = FALSE


#----------------------------------------------
# Verb Agreement Dictionary For Irregular Verbs
#----------------------------------------------

# VerbAgreementTable is a dictionary of the verb forms that can't be
# predicted by the general rule and have to be listed.  The agree()
# procedure will first check to see if the verb it's dealing with is
# in VerbAgreementTable and will only apply the regular rule if it's
# not.

Global.VerbAgreementDict = {"be":             ["are", "is"],
                            "do":             ["do", "does"],
                            "go":             ["go", "goes"],
                            "have":           ["have", "has"],
                            "contractedbe":   ["'re", "'s"],
                            "contractedhave": ["'ve", "'s"]}



#======================================================================
#                              Game Specific Object
#======================================================================

# This object lets us set all the properties for the game itself (author,
# version, copyright, etc).

class ClassGameObject(ClassFundamental):
    """Game specific information"""
    
    def __init__(self):
        """ Initialize game specific info"""
        self.SetMyProperties()

    
    def SetMyProperties(self):
        
        #------------
        # Game Author
        #------------

        # This property holds your name. It's usually set in your replacement
        # Engine.UserInit() or Engine.UserPreInit() function. By default this
        # property is said as part of the game banner.

        self.Author = "Put your name here"
        
        #----------
        # Copyright
        #----------

        # This property hold your copyright, for instance:
        #
        # "(c) 1998-2001 by Roger Plowman"

        self.Copyright = "Your copyright here"
        
        #------------------
        # Game Introduction
        #------------------

        # The game introduction text can be quite long, just look at Thief's
        # Quest (the sample game that comes with Universe). It says after
        # the banner and gives the player an introduction to the game. Who
        # they are, what they're doing in the game, etc.

        self.IntroText = "Your Game's Introductory Text Goes Here"
        
        #----------
        # Game Name
        #----------

        # This is the name of your game, as it will appear to the player. By
        # default it appears as the first text said on the screen once
        # your game is run.
        #

        self.Name = "Your Game's Name Goes Here"
        
        #-------------
        # Game Version
        #-------------

        # The version of your name, you should include only the number, such
        # as "1.0" since the game banner automatically says the word
        # Version.

        self.Version = "Your Game Version (1.0) Here"
    
    #------------
    # Game Banner
    #------------

    # By default this text is said at the beginning of your game.
    # Don't alter this property unless you make sure you include the
    # UniverseBanner property in it, that's a copyright requirement!
    #
    # It's unlikly you'll need to alter the game banner anyway.

    def Banner(self):
        """Method to say game banner at game start"""

        Text = "~title %s ~l version %s ~n Copyright (c) %s by %s ~n "
        Text = Text % (self.Name,self.Version,self.Copyright,self.Author)

        Text = Text + UniverseBanner()

        return Text
    
    #------------------------
    # Say Game Introduction
    #------------------------

    # This function says the game introduction, including the banners for
    # the game and Universe.

    def PrintGameIntroduction(self):
        """Says game introduction"""

        
        #--------------------------
        # Abort Intro If Restarting
        #--------------------------

        # If the global restarting flag isn't nil then we simply return from the
        # function immediately, doing nothing.

        if Global.Restarting: return
        
        #---------------------
        # Say Introductory Text
        #----------------------

        # Notice that all the introductory text is being said by the two lines
        # below. The game banner contains all the information about your name
        # that normally says at the start of a game, such as it's name, your
        # name and copyright, the Universe banner, and so forth.

        # The Game Intro contains all the other text you want to say just
        # before the first room's description. For example, in Thief's Quest
        # the game intro is a full screen of text!

        ClearScreen()
        Say(Game.Banner() + Game.IntroText)
        Global.Player.StartingLocation.Enter(Global.Player)

#------------------------
# Instantiate Game Object
#------------------------

Game = ClassGameObject()

#**********************************************************************
#                    U N I V E R S E     S E R V I C E S
#**********************************************************************

# A SERVICE is just a "mini" class used to add abilities to the base
# classes. For example, an actor by themselves isn't much use. But add a
# combat service and you have a monster. Add a Patrol service and you have
# a wandering monster.
#
# Take a room and add a Patrol service and you have a moving room! Services
# are carefully designed so any service can be used with any class.



#=====================================================================
#                 Activation Service
#=====================================================================


# This service allows devices to be activated and deactivated. This is
# generally used for light sources but can be used for any device that
# is switched on or off, with or without a tool.


class ServiceActivation:

    
    #-----------------------
    # Set Service Properties
    #-----------------------

    
    # This service is particularly involved, having lots of possible
    # complaints and options. Therefore each property below gets its
    # own lengthy explanation. Note this service is designed primarily
    # for lightsources (like flashlights, torches, candles, etc) but
    # can easily accomodate any device with a simple on/off function
    # just by changing the wording of the various properties.

    def SetMyProperties(self):

        
        #------------------------------------
        # Activate Spontaneous/Passive Phrase
        #------------------------------------

        
        # These two properties are used by the ActivateDesc() method
        # to describe the activation to the player. The word
        # "spontaneous" in this context means "active", as in "active
        # voice" and Passive means "passive voice". By default
        # Spontaneous is false, so passive voice will be used.
        #
        # Spontaneous would be "You light the lamp." while passive
        # would be "The lamp lights up." Notice we use curly brace
        # expressions so the strings will always reflect the object
        # in question.
        #
        # You'll also notice the use of the function "Self()." instead
        # of the more familiar "self.". This is due to a design issue
        # in Python. "self" is actually a variable that only exists
        # inside the class definition of the object. Self(), on the
        # other hand can safely be used in place of "self" in curly
        # brace expressions.

        self.ActivatePassivePhrase = """
                                     {SCase(You())} light
                                     {Self().TheDesc()}.
                                     """

        self.ActivateSpontaneousPhrase = """
                                         {SCase(Self().TheDesc())}
                                         lights up.
                                         """
        
        #--------------------
        # Activation Property
        #--------------------

        # This is the TRUE/FALSE property that is manipulated by the
        # Activate()/Deactivate() methods. You'll note it's a string,
        # by default it's the IsLit property.
        #
        # So activating a light source device makes self.IsLit TRUE
        # and deactivating it makes self.IsLit FALSE.
        #
        # Of course if self isn't a light source you could use a
        # different property, including those of your own creation,
        # perhaps IsOn, or IsRunning.

        self.ActivationProperty = "IsLit"

        
        #-------------------------------------
        # Already Activated/Deactivated Phrase
        #-------------------------------------

        # This pair of properties is returned by the
        # AlreadyActivated/DeactivatedDesc() methods. They say
        # "The lamp is already lit" and "The lamp is already out."
        #
        # Obviously the wording is skewed toward light source devices
        # and can easily be changed for other things. For instance
        # change "lit" to "running" or "already out" to "isn't running"
        # if you're dealing with an electric water pump.

        self.AlreadyActivatedPhrase = """
                                      {Self().TheDesc()} {Be(Self())}
                                      already lit.
                                      """

        self.AlreadyDeactivatedPhrase = """
                                      {Self().TheDesc()} {Be(Self())}
                                      already out.
                                      """

        
        #------------------------------------
        # Activate Spontaneous/Passive Phrase
        #------------------------------------

        
        # These two properties are used by the DeactivateDesc() method
        # to describe the deactivation to the player. The word
        # "spontaneous" in this context means "active", as in "active
        # voice" and Passive means "passive voice". By default
        # Spontaneous is false, so passive voice will be used.
        #
        # Spontaneous would be "You douse the lamp." while passive
        # would be "The lamp is now out." Notice we use curly brace
        # expressions so the strings will always reflect the object
        # in question.
        #
        # You'll also notice the use of the function "Self()." instead
        # of the more familiar "self.". This is due to a design issue
        # in Python. "self" is actually a variable that only exists
        # inside the class definition of the object. Self(), on the
        # other hand can safely be used in place of "self" in curly
        # brace expressions.



        self.DeactivatePassivePhrase = """
                                       {You()} douse
                                       {Self().TheDesc()}
                                       """

        self.DeactivateSpontaneousPhrase = "{Self().TheDesc()} goes out."

        
        #-------------------------
        # Required Activation Tool
        #-------------------------

        # Certain devices require a tool to turn them on, for example
        # a candle needs a match to light it, a bonfire might need a
        # torch, a fire hydrant might need a wrench, and so on.
        #
        # This property is set to the object needed to activate self.
        # If set to None (as it is by default) then no tool is needed
        # to activate self.

        self.RequiredActivationTool = None

        
        #---------------------------
        # Required Deactivation Tool
        #---------------------------

        # This is the tool required to deactivate self. It can be None
        # if no tool is required (like a flashlight), it can be the
        # same tool used to activate self (like a fire hydrant) or it
        # can be a different tool (such as a candle snuffer).

        self.RequiredDeactivationTool = None

        
        #------------------
        # Maximum Life Span
        #------------------

        # The maximum number of turns this device can operate before
        # being refueled/recharged/battery replacement. This value is
        # also used when a device is recharged, to return the 
        # RemainingLifeSpan property to the value of this property.
        #
        # By default we set this value to 32,000 turns. Obviously you
        # should lower this for devices you create!

        self.MaxLifeSpan = 32000

        
        #--------------------
        # Remaining Life Span
        #--------------------

        # This is the number of turns of fuel/power the device has
        # left to run.

        self.RemainingLifeSpan = self.MaxLifeSpan


    
    #--------------
    # Activate Self
    #--------------

    # This function activates self, if self were a flashlight for
    # example this function would turn it on.
    #
    # The following arguments are available but may not be used in
    # this default method.
    #
    # Multiple - Not used, allows the method to detect when self is
    #            part of a multiple list of objects. Defaults to
    #            false. This argument can be handy to say something
    #            different when self is part of a list than when it's
    #            by itself.
    #
    # Spontaneous - In this context TRUE means "active voice" and
    #               FALSE means "passive voice". Active voice would
    #               be "You light the lamp". Passive voice would be
    #               "The lamp lights up."
    #
    # Silent - If TRUE then the ActivateDesc() method is skipped, if
    #          FALSE the ActivateDesc() method is called.

    def Activate(self, Multiple=FALSE, Spontaneous=FALSE, Silent=FALSE):
        """Activate the device"""

        
        #------------------------------
        # Complain If No Life Span Left
        #------------------------------

        if not self.RemainingLifeSpan:
            return Complain("Nothing happens.")

        
        #------------------------------
        # Complain if already activated
        #------------------------------

        # Let's assume self is a flashlight. Let's further assume we
        # didn't change self.Activation property from "IsLit".
        # Therefore the if test below translates into English "if the
        # flashlight is lit then..."

        if self.Get(self.ActivationProperty):
            return Complain(self.AlreadyActivatedDesc())

        
        #------------------------------
        # Get Tool Needed And Tool Used
        #------------------------------

        # ToolNeeded is the tool needed to activate the device,
        # which can be None (for example, a flashlight). ToolUsed is
        # assumed to be None, unless there's an indirect object in the
        # list. This would only happen where the player said "Light
        # torch with..." or some such. If they just said "light lamp"
        # then ToolUsed remains None.

        ToolNeeded = self.RequiredActivationTool

        ToolUsed = None

        if len(P.IOL()) > 0:
            ToolUsed = P.IOL()[0]

        
        #----------------------------
        # If Tool Used But Not Needed
        #----------------------------

        # For example, if they tried to light the flashlight with a 
        # match...

        if ToolUsed and not ToolNeeded:
            return Complain("%s can't do that." % You())

        
        #----------------------------
        # If Tool Needed and Not Used
        #----------------------------

        # For example "light candle" instead of "light candle with match".

        if ToolNeeded and not ToolUsed:
            return Complain(self.RequiresToolDesc())

        
        #----------------------------
        # Complain If Wrong Tool Used
        #----------------------------

        # This test is a bit of elegant short-cutting. ToolNeeded will
        # either contain None or some object. If None then testing
        # ToolNeeded returns false. If ToolNeeded is any object, then
        # testing ToolNeeded returns true.
        #
        # You could also write the IF test this way:
        #
        # if ToolNeeded <> None and ToolNeeded <> ToolUsed:
        #
        # But I think this way is easier to read and understand.

        if ToolNeeded and ToolNeeded <> ToolUsed:
            return Complain(self.WrongToolDesc())

        
        #--------------------------------
        # Set Activation Property To TRUE
        #--------------------------------

        # The setattr() function lets you use a string to name the
        # property you want to set. This is exactly what we need to
        # set any property we care to put in the ActivationProperty
        # property.

        setattr(self, self.ActivationProperty, TRUE)

        
        #--------------------------
        # Tell Player Unless Silent
        #--------------------------

        # If Silent is FALSE then tell the player the device activated.

        if not Silent: Say(self.ActivateDesc(Multiple, Spontaneous))

        
        #---------------
        # Return Success
        #---------------

        return SUCCESS


    
    #----------------
    # Deactivate Self
    #----------------

    
    # This function deactivates self, if self were a flashlight for
    # example this function would turn it off.
    #
    # The following arguments are available but may not be used in
    # this default method.
    #
    # Multiple - Not used, allows the method to detect when self is
    #            part of a multiple list of objects. Defaults to
    #            false. This argument can be handy to say something
    #            different when self is part of a list than when it's
    #            by itself.
    #
    # Spontaneous - In this context TRUE means "active voice" and
    #               FALSE means "passive voice". Active voice would
    #               be "You douse the lamp". Passive voice would be
    #               "The lamp turns off."
    #
    # Silent - If TRUE then the DeactivateDesc() method is skipped, if
    #          FALSE the DeactivateDesc() method is called.


    def Deactivate(self, Multiple=FALSE, Spontaneous=FALSE, Silent=FALSE):
        """Deactivate the Device"""

        
        #------------------------------
        # Complain if already activated
        #------------------------------

        # Let's assume self is a flashlight. Let's further assume we
        # didn't change self.Activation property from "IsLit".
        # Therefore the if test below translates into English "if the
        # flashlight is not lit then..."

        if not self.Get(ActivationProperty):
            return Complain(self.AlreadyDeactivatedDesc())

        
        #------------------------------
        # Get Tool Needed And Tool Used
        #------------------------------

        # ToolNeeded is the tool needed to activate the device,
        # which can be None (for example, a flashlight). ToolUsed is
        # assumed to be None, unless there's an indirect object in the
        # list. This would only happen where the player said "Light
        # torch with..." or some such. If they just said "light lamp"
        # then ToolUsed remains None.

        ToolNeeded = self.RequiredDeactivationTool

        ToolNeeded = None

        if len(P.IOL()) > 0:
            ToolUsed = P.IOL()[0]

        
        #----------------------------
        # If Tool Used But Not Needed
        #----------------------------

        # For example, if they tried to light the flashlight with a 
        # match...

        if ToolUsed and not ToolNeeded:
            return Complain("%s can't do that." % You())

        
        #----------------------------
        # If Tool Needed and Not Used
        #----------------------------

        # For example "light candle" instead of "light candle with match".

        if ToolNeeded and not ToolUsed:
            return Complain(self.RequiresToolDesc())

        
        #----------------------------
        # Complain If Wrong Tool Used
        #----------------------------

        # This test is a bit of elegant short-cutting. ToolNeeded will
        # either contain None or some object. If None then testing
        # ToolNeeded returns false. If ToolNeeded is any object, then
        # testing ToolNeeded returns true.
        #
        # You could also write the IF test this way:
        #
        # if ToolNeeded <> None and ToolNeeded <> ToolUsed:
        #
        # But I think this way is easier to read and understand.

        if ToolNeeded and ToolNeeded <> ToolUsed:
            return Complain(self.WrongToolDesc())

        
        #---------------------------------
        # Set Activation Property To FALSE
        #---------------------------------

        # The setattr() function lets you use a string to name the
        # property you want to set. This is exactly what we need to
        # set any property we care to put in the ActivationProperty
        # property.

        setattr(self, self.ActivationProperty, FALSE)

        
        #--------------------------
        # Tell Player Unless Silent
        #--------------------------

        # If Silent is FALSE then tell the player the device activated.

        if not Silent: Say(self.DeactivateDesc(Multiple, Spontaneous))

        
        #---------------
        # Return Success
        #---------------

        return SUCCESS



    
    #---------------------
    # Activate Description
    #---------------------

    # This method returns the description of the device activation, in
    # either active (Spontaneous=TRUE) or passive (Spontaneous=FALSE) 
    # voice.

    def ActivateDesc(self, Multiple=FALSE, Spontaneous=FALSE):
        if Spontaneous:
            return self.ActivateSpontaneousPhrase
        else:
            return self.ActivatePassivePhrase

    
    #-----------------------
    # Deactivate Description
    #-----------------------

    # Returns the description of what happens when self is turned off.
    # If Spontaneous is FALSE returns "The lamp goes out." or "You put
    # the lamp out" if Spontaneous is true.

    def DeactivateDesc(self, Multiple=FALSE, Spontaneous=FALSE):

        if Spontaneous:
            return SCase(self.DeactivateSpontaneousPhrase)
        else:
            return SCase(self.DeactivatePassivePhrase)

    
    #-----------
    # Drain Life
    #-----------

    # This method reduces self's remaining life span by 1. When life
    # reaches 0, the device automatically deactivates.

    def DrainLife(self):
        self.RemainingLifeSpan = self.RemainingLifeSpan - 1
        if not self.RemainingLifeSpan: self.Deactivate()

    
    #------------------------------
    # Already Activated Description
    #------------------------------

    # Returns the already activated complaint. (The lamp is already on)

    def AlreadyActivatedDesc(self):
        return SCase(self.AlreadyActivatedPhrase)
        
    
    #--------------------------------
    # Already Deactivated Description
    #--------------------------------

    # This method returns the already deactivated complaint (The pump
    # isn't running!)

    def AlreadyDeactivatedDesc(self):
        return SCase(self.AlreadyDeactivatedPhrase)

    
    #---------------
    # Life Remaining
    #---------------

    # Most devices have a limited lifespan (number of turns) they can
    # remain active before running out of fuel or power. Flashlights
    # are a perfect example. This function returns the
    # RemainingLifeSpan property by default, but a more complex device
    # (such as a battery powered flashlight) could override (replace)
    # this method with one that returned the RemainingLifeSpan property
    # of the *batteries* (for example).

    def LifeRemaining(self): return self.RemainingLifeSpan

    
    #--------------------------
    # Requires Tool Description
    #--------------------------

    # Returns the complaint if you try to activate a device without
    # the required tool. (You'll need something to do that with.)

    def RequiresToolDesc(self):
        return SCase("%s'll need something to do that with." % You())

    
    #-----------------------
    # Wrong Tool Description
    #-----------------------

    # Returns the Wrong Tool complaint if you try to activate self
    # with the wrong tool. (You can't do that with a crowbar.)

    def WrongToolDesc(self,ToolUsed):
        return "%s can't do that with %s." % (You(),ToolUsed.ADesc())



#------------------------------------
# ServiceContainer In/On/Under/Behind
#------------------------------------

# These 4 services allow any class to act as a container. Note you must still set
# the container's actual MaxBulk property, these services automatically set the 
# MaxWeight property to 32000 (weight isn't usually an issue in containment).


#-----------------
# ServiceContainIn
#-----------------

# Most of the containment requirements are already met by ClassBasicThing, so
# adding this service to either ClassItem, ClassScenery, or their descendents only
# needs to change a couple of properties, everything else is already set properly
# for objects that contain other objects "inside" themselves.

class ServiceContainIn:

    def SetMyProperties(self):
        self.MaxBulk = 1
        self.MaxWeight = 32000
        self.IsOpen = TRUE
        self.CantLookInside = FALSE


#-----------------
# ServiceContainOn
#-----------------

# Most of the containment requirements are already met by ClassBasicThing, so
# adding this service to either ClassItem, ClassScenery, or their descendents only
# needs to change a few properties, everything else is already set properly
# for objects that contain other objects "on" themselves.

class ServiceContainOn:

    def SetMyProperties(self):
        self.MaxBulk = 1
        self.MaxWeight = 32000
        self.IsOpen = TRUE
        self.IsTransparent = TRUE
        self.ContainerPrepositionDynamic = "on"
        self.ContainerPrepositionStatic = "on"


#--------------------
# ServiceContainUnder
#--------------------

# Most of the containment requirements are already met by ClassBasicThing, so
# adding this service to either ClassItem, ClassScenery, or their descendents only
# needs to change a few properties, everything else is already set properly
# for objects that contain other objects "under" themselves. This service is also
# usually combined with ServiceRevealWhenTaken.

class ServiceContainUnder:

    def SetMyProperties(self):
        self.MaxBulk = 1
        self.MaxWeight = 32000
        self.IsOpen = TRUE
        self.ContainerPrepositionDynamic = "under"
        self.ContainerPrepositionStatic = "under"


#--------------------
# ServiceContainUnder
#--------------------

# Most of the containment requirements are already met by ClassBasicThing, so
# adding this service to either ClassItem, ClassScenery, or their descendents only
# needs to change a few properties, everything else is already set properly
# for objects that contain other objects "behind" themselves. This service is also
# usually combined with ServiceRevealWhenTaken.

class ServiceContainBehind:

    def SetMyProperties(self):
        self.MaxBulk = 1
        self.MaxWeight = 32000
        self.IsOpen = TRUE
        self.ContainerPrepositionDynamic = "behind"
        self.ContainerPrepositionStatic = "behind"



#-------------------------------
# Dictionary Description Service
#-------------------------------

# This service replaces the "sensory" description methods with ones that read their description
# from the Descriptions dictionary. This service makes it easier to define the long, odor,
# sound, taste and touch descriptions. This service may be used by BasicThings and Rooms as
# desired.

class ServiceDictDescription:

    def SetMyProperties(self):
        """Sets service properties"""
        self.DefaultDescriptions()

    
    def DefaultDescriptions(self):
        self.Descriptions = {
            "HereDesc": "There is {Self().ADesc()} here.",
            "LDesc": """
                     {SCase(Self().PronounDesc())} looks like an
                     ordinary {Self().NamePhrase} to {Me()}.
                     """,
            "OdorDesc": """
                        {SCase(Self().PronounDesc())} smells like an
                        ordinary {Self().NamePhrase} to {Me()}.
                        """,
            "SoundDesc": """
                         {SCase(Self().TheDesc())} isn't making any
                         noise.
                         """,
            "ReadDesc":  "{You()} can't read {self().ADesc()}.",
            "TasteDesc": """
                         {SCase(Self().PronounDesc())} tastes like an
                         ordinary {Self().NamePhrase} to {Me()}.
                         """,
            "FeelDesc": """
                        {SCase(Self().PronounDesc())} feels like an
                        ordinary {Self().NamePhrase} to {Me()}.
                        """,
            "GroundDesc": "The ground looks completely ordinary to {Me()}.",
            "SkyDesc": "The sky looks completely ordinary to {Me()}.",
            "TakeDesc": "{You()} can't take that!}",
            "WallDesc": "The wall looks completely ordinary to {Me()}."}


    def LDesc(self): return self.Descriptions["LDesc"]
    def OdorDesc(self): return self.Descriptions["OdorDesc"]
    def ReadDesc(self): return self.Descriptions["ReadDesc"]
    def SoundDesc(self): return self.Descriptions["SoundDesc"]
    def TasteDesc(self): return self.Descriptions["TasteDesc"]
    def FeelDesc(self): return self.Descriptions["FeelDesc"]
    def GroundDesc(self): return self.Descriptions["GroundDesc"]
    def SkyDesc(self): return self.Descriptions["SkyDesc"]
    def WallDesc(self): return self.Descriptions["WallDesc"]

    
    #----------------
    # Set Description
    #----------------

    # This function takes the key, adds "Desc" to it, and uses that to put Value in the
    # Descriptions dictionary. For example Rock.SetDesc("L","It looks like an ordinary rock.")
    # would create a key of LDesc (L + Desc) and place "It looks like an ordinary rock" in
    # the descriptions dictionary. This is a shortcut for the longer (but functionally identical
    #
    # Rock.Descriptions["LDesc"] = "It looks like an ordinary rock".
    #
    # Note the string.join(string.split(Value)). This reduces all white
    # spaces to 1 space. For example, many triple quoted strings are
    # "formatted" in the source code using multiple spaces. The
    # join/split combination changes multiple spaces into a single
    # space, this *seriously* reduces memory requirements!

    def SetDesc(self,Key,Value):
       self.Descriptions[Key + "Desc"] = string.join(string.split(Value))

    

#=====================================================================
#                           Follow Service
#=====================================================================

# This service allows things to follow the player.

class ServiceFollow:

    def SetMyProperties(self):
        """Sets service properties"""
        self.Follow = FALSE

    #--------------
    # Follow Player
    #--------------

    # If the Follow property is true, set this item's location to the player's 
    # location.

    def FollowPlayer(self):
        """Follow Player around"""
        if self.Follow:
            self.Location = Global.Player.Where()


#=====================================================================~~KR
#                           Openable Service
#=====================================================================

# This service allows things to be opened and closed.

class ServiceOpenable:

    def SetMyProperties(self):
        """Sets service properties"""
        pass

    
    #---------------------------
    # Already Closed Description
    #---------------------------

    # This method is called when the player tries to close an object
    # that's already closed. It says something like "The door is already
    # closed."

    def AlreadyClosedDesc(self):
        return SCase("%s %s already closed." % (self.TheDesc(), Be(self)))

    
    #-------------------------
    # Already Open Description
    #-------------------------

    # This method is called if the player tries to open an object that's
    # already open. It says "The door is already open." or whatever.

    def AlreadyOpenDesc(self):
        return SCase("%s %s already open." % (self.TheDesc(), Be(self)))


    
    #-----------
    # Close self
    #-----------

    # This method is called by the CloseVerb object when the player
    # attempts to close an object.
    #
    # If self isn't openable the method complains, if it's already open
    # the method complains, and if we don't want the closing to be
    # silent we print the close description. Then we set self's IsOpen
    # property to false and return SUCCESS.
    #
    # The Spontaneous argument should be FALSE when the character
    # closes the door directly, and TRUE if the character pushes a
    # button or something that closes the object.

    def Close(self, Multiple=FALSE, Silent=FALSE, Spontaneous=FALSE):
        """Close the object"""

        if not self.IsOpenable: return Complain(self.UnopenableDesc())
        if not self.IsOpen: return Complain(self.AlreadyClosedDesc())
        if not Silent: Say(self.CloseDesc(Multiple, Spontaneous))
        self.IsOpen = FALSE
        return SUCCESS

    
    #------------------
    # Close Description
    #------------------

    # The description printed when the player closes the object.
    # Multiple will almost certainly be false. If Spontaneous is true
    # the description will be "The door closes.". This would be used
    # in cases where the object isn't directly closed by the actor.
    #
    # When Spontaneous is false the description is "You close the
    # door" (or whatever it is the player closed).

    def CloseDesc(self, Multiple=FALSE, Spontaneous=FALSE):

        if Spontaneous:
            return SCase(self.TheDesc())+ " " + Agree("close", self)
        else:
            return SCase("%s %s %s." % (You(), Agree("close"), self.TheDesc()))


    
    #--------------
    # Open <object>
    #--------------

    # This method is called when an object is opened. Silent is true
    # if you don't want to say anything when the object opens,
    # Spontaneous means the player didn't directly open the object.
    #
    # Only show the opening description if the Silent parameter
    # is FALSE.  (Setting Silent to TRUE is useful, for example, in
    # opening a door: the Open command is passed to both sides of the
    # door in both rooms, but you don't want to see two messages.)
    #
    # The method will complain if the object isn't openable or if
    # it's already open. If Silent is FALSE then we call OpenDesc()
    # to say something like "You open the door."

    def Open(self, Multiple=FALSE, Silent=FALSE, Spontaneous=FALSE):
        """Open the object"""

        if not self.IsOpenable: return Complain(self.UnopenableDesc())
        if self.IsOpen: return Complain(self.AlreadyOpenDesc())
        if not Silent: Say(self.OpenDesc(Multiple, Spontaneous))

        self.IsOpen = TRUE

        return SUCCESS

    
    #-----------------
    # Open Description
    #-----------------

    # This method is called to describe the object opening. If
    # Spontaneous is FALSE it returns "You open the door." (or whatever).
    # If Spontaneous is false it says "The door opens."

    def OpenDesc(self, Multiple=FALSE, Spontaneous=FALSE):

        if Spontaneous:
            return SCase(self.TheDesc())+ " " + Agree("open", self)
        else:
            return SCase("%s %s %s." %
                         (You(), Agree("open"), self.TheDesc()))


    
    #-----------------------
    # Unopenable Description
    #-----------------------

    # This method is called by Open() and Close() when the object
    # being opened isn't openable, say for example a rock or a tree.

    def UnopenableDesc(self):
        return SCase("%s can't %s %s." % (You(),
                                          self.TheDesc(),
                                          P.CVN()))



#-----------------
# Lockable Service
#-----------------

# This service allows things to be opened and closed and locked.

class ServiceLockable(ServiceOpenable):

    def SetMyProperties(self):
        """Sets service properties"""
        self.IsLocked = FALSE
        self.LocksWithoutKey = TRUE

    
    #---------------------------
    # Already Locked Description
    #---------------------------

    # This method is called when the object being unlocked is already
    # unlocked.

    def AlreadyLockedDesc(self):
        return SCase("%s %s already locked." % (self.TheDesc(), Be(self)))

    
    #-----------------------------
    # Already Unlocked Description
    #-----------------------------

    # This method is called when the object being unlocked is already
    # unlocked.

    def AlreadyUnlockedDesc(self):
        return SCase("%s %s already unlocked." % (self.TheDesc(), Be(self)))

    
    #------------
    # Lock Object
    #------------

    # This method is called to lock an object. It complains if the
    # object is already locked, or if it needs a key and none was
    # provided or the wrong key was provided.
    #
    # If Silent is FALSE a description of the object being locked is
    # said and the IsLocked property is set to TRUE.

    def Lock(self, key=None, Silent=FALSE, Spontaneous=FALSE):
        """Lock the object"""

        if self.IsLocked: return Complain(self.AlreadyLockedDesc())

        if not self.LocksWithoutKey and not key:
            return Complain(self.NeedAKeyDesc())

        if not self.LocksWithoutKey and key <> self.Key:
            return Complain(self.WrongKeyDesc(key))

        if not Silent: Say(self.LockDesc(Spontaneous))

        self.IsLocked = TRUE

        return TURN_CONTINUES

    
    #-----------------
    # Lock Description
    #-----------------

    # This description is called when the object is locked. It says
    # either "The door locks." or "You lock the door." depending on
    # whether Spontaneous was True or not.

    def LockDesc(self, Spontaneous=FALSE):
        if Spontaneous:
            return SCase(self.TheDesc())+ " " + Agree("lock", self) + "."
        else:
            return SCase("%s %s %s." % (You(), Agree("lock"), self.TheDesc())) + "."

    
    #-----------------------
    # Need A Key Description
    #-----------------------

    # This method is called when the object being locked/unlocked needs
    # a key and no key was given.

    def NeedAKeyDesc(self):
        return SCase("%s %s some kind of key to do that." %
                     (You(), Agree("need")))

    
    #--------------
    # Unlock Object
    #--------------

    # This method is called to unlock an object. It complains if the
    # object is already unlocked, or if it needs a key and none was
    # provided or the wrong key was provided.
    #
    # If Silent is FALSE a description of the object being unlocked is
    # said and the IsLocked property is set to FALSE.

    def Unlock(self, key=None, Multiple=FALSE, Silent=FALSE,
               Spontaneous=FALSE):
        """Unlock the object"""

        if not self.IsLocked:
            return Complain(self.AlreadyUnlockedDesc())

        if not key and not self.UnlocksWithoutKey:
            return Complain(self.NeedAKeyDesc())

        if key <> self.Key and not self.UnlocksWithoutKey:
            return Complain(self.WrongKeyDesc(key))

        if not Silent:
            Say(self.UnlockDesc(Spontaneous))

        # change the IsOpen property of the object
        self.IsLocked = FALSE

        return TURN_CONTINUES

    
    #-------------------
    # Unlock Description
    #-------------------

    # This description is called when the object is locked. It says
    # either "The door unlocks." or "You unlock the door." depending on
    # whether Spontaneous was True or not.

    def UnlockDesc(self, Multiple=FALSE, Spontaneous=FALSE):

        if Spontaneous:
            return SCase(self.TheDesc())+ " " + Agree("unlock", self) + "."
        else:
            return SCase("%s %s %s." %
                         (You(), Agree("unlock"), self.TheDesc()))
    
    #----------------------
    # Wrong Key Description
    #----------------------

    # Called when the wrong key is used to lock/unlock objects that
    # need a specific key. It returns "This key doesn't work with the
    # door."

    def WrongKeyDesc(self, key):
        return SCase("This %s doesn't work with %s." %
                     (key.NamePhrase, self.TheDesc())) + "."



#=====================================================================
#                     Reveal When Taken
#=====================================================================


# If you take a rock, the things that are hiding under/behind the rock
# should normally be left behind.  This service overrides the usual
# Take method of ServiceTakeableThing so that the contents of the
# hider will be moved to the hider's old location.
#
# Note this service only makes sense when used with objects that store
# their contents behind or under, rather than in or on top. After all,
# it would defeat the purpose of a box to have it dump its contents on
# the ground when taken!


class ServiceRevealWhenTaken:

    def Take(self):

        
        #------------------
        # Save Old Location
        #------------------

        # self's current location is where we want to return any
        # items hidden by self.

        OldLocation = self.Location

        
        #------------------------------
        # Fail If Actor Can't Take Self
        #------------------------------

        if not P.CA().Enter(self): return FAILURE

        
        #----------------------------
        # Succeed If No Hidden Things
        #----------------------------

        
        # Desc contains self's normal take description (usually
        # "Taken"). HiddenThings contains self.Contents, a list of
        # all objects contained by self.
        #
        # If there are no hidden things we say Desc and return SUCCESS,
        # which of course ends the method immediately.
        #
        # A note about the IF test. The syntax "if not HiddenThings:"
        # is exactly the same as saying if len(HiddenThings) == 0:"
        # but it's a lot more like English!

        Desc = self.TakeDesc()
        HiddenThings = self.Contents

        if not HiddenThings:
            Say(Desc)
            return SUCCESS

        #------------------------
        # Describe Revealed Items
        #------------------------

        Desc = Desc + " " + self.LookDeepDesc()
        Say(Desc)
        #-----------------------------------------
        # Move Hidden Items to Self's Old Location
        #-----------------------------------------

        for Thing in HiddenThings: Thing.MoveInto(OldLocation)
        #---------------
        # Return Success
        #---------------

        return SUCCESS


#===========================================================================
#                          Takeable/Fixed Item Services
#===========================================================================

# These two services are mutually exclusive. They allow easily changed
# descriptions to be returned.


#----------------------
# Takeable Item Service
#----------------------

# This service allows an item to be taken. Notice it uses the ENTER method,
# so the BasicThing ENTER method has to be satisfied as well.

class ServiceTakeableItem:

    def SetMyProperties(self):
        """Sets service properties"""
        pass

    
    #----------
    # Drop Self
    #----------

    # This is the method called by the Drop verb.

    def Drop(self,Multiple=FALSE):
        """Drop self into current actor's location"""

        #---------------------
        # Actor Carrying Self?
        #---------------------

        # If the actor isn't carrying Self, then complain. Remember Complain returns FAILURE, so
        # when you return a Complain() function, you are returning FAILURE.

        if not self in P.CA().Contents: return Complain(self.NotCarryingDesc())

        #-----------------------
        # Will Room accept item?
        #-----------------------

        
        # Notice we're letting the room decide whether the object can enter
        # or not, which means (in a normal room) it will check to see if
        # there's enough bulk and weight left. If so, we say the DropDesc
        # property, if not we let the room do the complaining.

        if P.CA().Where().Enter(self):
            Say(self.DropDesc(Multiple) + " ~n")

    
    #-----------------
    # Drop Description
    #-----------------

    # This function returns either "Dropped" (if the object is the only one currently being
    # dropped) or "Rock: Dropped" if this object is one of many objects being dropped at the
    # same time.

    def DropDesc(self,Multiple=FALSE):
        """Drop Description"""

        ReturnValue = ""

        #----------------------------
        # Part of multiple item drop?
        #----------------------------

        # If Mutiple is true the actor is dropping multiple objects so we have to prepend the
        # Short Description the object uses when part of a multiple object description.

        if Multiple: ReturnValue = self.MultiSDesc()+": "

        #---------------
        # Return Message
        #---------------

        return ReturnValue + "Dropped."
    
    #-------------------------
    # Not Carrying Description
    #-------------------------

    # This is the message returned when the player tries to drop something they aren't carrying.
    # It says "You aren't carrying that." or "Fred isn't carrying that."

    def NotCarryingDesc(self):
        """Description said when actor not carrying self"""

        #--------------
        # Set Complaint
        #--------------

        # The code below says Complaint is going to be equal to the
        # string with the two %s's replaced by You() and Be(). You()
        # is the word that's appropriate for the "you" part of "You
        # aren't carrying that". Be() is the word for "is" or
        # "are".

        Complaint = "%s %sn't carrying that." % (You(), Be())

        return SCase(Complaint)

    
    #----------
    # Take Self
    #----------

    # This is the method invoked by the Take command. It basically says if self can enter the
    # current actor then say the take description. If it can't, the Enter() method of the actor
    # takes care of any complaints.

    def Take(self,Multiple=FALSE):
        """Current Actor take self"""

        if self in P.CA().Contents:
            Say("{SCase(You())}{Be(Contract=TRUE)} already carrying it.")
            return

        if P.CA().Enter(self):
            Say(self.TakeDesc(Multiple))

    
    #-----------------
    # Take Description
    #-----------------

    # Like the DropDesc method, the TakeDesc method returns either "Taken" or "Rock: Taken".

    def TakeDesc(self,Multiple=FALSE):
        """Take description"""
        ReturnValue = ""

        if hasattr(self,"Descriptions"):
            ReturnValue = self.Descriptions["TakeDesc"]
        else:
            ReturnValue = "Taken."

        if Multiple: ReturnValue = self.MultiSDesc()+": "
        return ReturnValue



#-------------------
# Fixed Item Service
#-------------------

# This service prevents an item from being taken. It complains appropriately
# if the player tries to take or drop self.

class ServiceFixedItem:

    def SetMyProperties(self):
        """Sets service properties"""
        pass

    
    #----------
    # Drop Self
    #----------

    # This is the method called by the Drop verb.

    def Drop(self,Multiple=FALSE):
        """Complain with drop description."""
        return Complain(self.DropDesc())
    
    #-----------------
    # Drop Description
    #-----------------

    def DropDesc(self):
        """Drop complaint"""
        Complaint = "%s %sn't carrying that!" % (You(), Be())

        if hasattr(self,"Descriptions"): Complaint = self.Descriptions["DropDesc"]

        return Complaint

    
    #----------
    # Take Self
    #----------

    def Take(self,Multiple=FALSE):
        """Take self"""
        Complain(self.TakeDesc())
    
    #---------------
    # Take Complaint
    #---------------

    def TakeDesc(self,Multiple=FALSE):
        """Take complaint"""
        Complaint = "%s can't take that!" % You()

        if hasattr(self,"Descriptions"):
            Complaint = self.Descriptions["TakeDesc"]

        return SCase(Complaint)




#**********************************************************************
#                        U N I V E R S E     C L A S S E S
#**********************************************************************

# There are only a handful of major classes, all objects are made from
# these. Where additional functionality is required we use SERVICES.

#=====================================================================
#                               Class Basic Thing
#=====================================================================


# ClassBasicThing is the root for all "real" objects (like a rock),
# or rooms. It is descended from ClassBaseObject. Basic Things have some
# fundamental attributes such as weight and bulk, the ability to provide
# basic descriptions of themselves (such as an ldesc, sdesc, adesc, etc.)
#
# In addition, certain fundamental functions (like checking for light) are
# also supplied here. In short, if an ability is required by *ALL* objects
# you'll likely find it here.
#
# In the examples we're going to use two objects, a rock for physical
# objects, and a forest for room objects. (It's much easier to talk about
# "a rock" than "an object", right?)

class ClassBasicThing(ClassBaseObject):
    """Root class of all physical objects or rooms"""
    
    def SetMyProperties(self):
        """Sets default instance properties"""

        
        #---------------------------
        # Append To All Objects list
        #---------------------------

        # Now we've done everything our ancestor did, it's time to ALSO
        # append this object to a list of all Thing objects. The
        # AllObjectsList must contain all "thing" objects, but it doesn't
        # contain verb objects.

        Global.AllObjectsList.append(self)
        
        #--------
        # Article
        #--------

        # This is the indefinite article used with the object. In English
        # there are two articles, "a", or "an", depending on the word the
        # article is describing. You have to be careful when choosing the
        # correct article, make sure it agrees with the object's short
        # description. Adjectives are a problem here.
        #
        # For example, it's "AN umbrella", but also "A red umbrella". By
        # default basic things use 'a' as their article. To decide which
        # article to use try saying "a", followed by the short description.
        # If it sounds ok, then use "a", otherwise use "an".

        self.Article = "a"

        
        #-----
        # Bulk
        #-----

        # Bulk is measured in completely arbitrary units--there is no
        # equivalent unit of measurement in the real world. The closest
        # concept comes from the world of RPG's, with "encumberance".
        #
        # The idea of bulk is how hard something is to carry. A pound of
        # feathers only weighs a pound but it's awkwardness makes up for
        # that. So we measure an item's weight AND it's bulk.

        self.Bulk = 0

        
        #-------------------------------
        # Can't Look Behind/Inside/Under
        #-------------------------------

        # These defaults assume a solid object that can be moved (like
        # a rock) that isn't openable. Change them appropriately if
        # you need to.

        self.CantLookBehind = FALSE
        self.CantLookInside = TRUE
        self.CantLookUnder  = FALSE
        self.CantLookOn     = FALSE

        
        #---------
        # Contents
        #---------

        # This list contains every object the room (or container) contains.

        self.Contents = []
        
        #--------------------------------
        # Container Preposition (dynamic)
        #--------------------------------

        # Preposition used when putting object in/under/behind/on
        # another object. The "active" preposition.

        self.ContainerPrepositionDynamic = "inside"

        #-------------------------------
        # Container Preposition (static)
        #--------------------------------

        # Preposition used when describing how an object holds its
        # contents.

        self.ContainerPrepositionStatic  = "inside"


        
        #--------------------
        # Format Descriptions
        #--------------------

        # These are the parts of speech that say "is/are" or "do/does"
        # when dealing with objects generically. FormatYou being blank
        # makes the Agree() function (and its siblings) consider this
        # object singular by default (which is generally correct).

        self.FormatYou = ""


        
        #-----------
        # Has Ground
        #-----------

        # True only for rooms, used to handle commands like "Examine Ground" in
        # a fairly automatic way.

        self.HasGround = FALSE
        
        
        #----------------------
        # Has Floating Location
        #----------------------

        # If true then this object can change its location when another
        # object does. Currently this functionality is only implemented
        # for the "me" object and ClassLandmark objects.

        self.HasFloatingLocation = FALSE

        
        #--------
        # Has Sky
        #--------

        # Only true for room objects, lets the room deal with the sky/ceiling
        # in a fairly automatic way.

        self.HasSky = FALSE
        
        
        #-----------
        # Has Ground
        #-----------

        # True only for rooms, used to handle commands like "Examine Wall" in
        # a fairly automatic way.

        self.HasWall = FALSE


        
        #-----------
        # Is Active?
        #-----------

        # True if device is activated, valuse if not.

        self.IsActivated = FALSE

        
        #----------
        # Is Actor?
        #----------

        # Is this object an actor? Determines whether or not this object
        # is placed in the Global.ActorList.

        self.IsActor = FALSE

        
        #-------------
        # Blatant Odor
        #-------------

        # By default this value is FALSE, set it to TRUE if the odor of the
        # object is so intrusive it should always be noticed, this is used
        # by the SmartDescribeSelf method to see if the odor should be
        # included as part of the description or not.

        self.IsBlatantOdor = FALSE

        
        #--------------
        # Blatant Sound
        #--------------

        # By default this value is nil, set it to true if the sound the
        # object makes is so intrusive it should always be noticed, this is
        # used by the SmartDescribeSelf method to see if the sound should be
        # included as part of the description or not.

        self.IsBlatantSound = FALSE

        
        #-------
        # Broken
        #-------

        # This property should return TRUE or FALSE, it's intended to handle
        # breakable objects--a mirror, for instance.

        self.IsBroken = FALSE

        
        #-----------------
        # Is Object Female
        #-----------------

        # To properly handle pronouns the parser has to know if an object is
        # male, female, or neuter. Setting IsHer lets the parser know that
        # "her" is the appropriate pronoun for this object. Note if you have
        # an androgynous object you can set both IsHer and IsHim true!

        # If neither IsHim or IsHer is set to true the parser will use "it"
        # as the object's pronoun.

        self.IsHer = FALSE

        
        #---------------
        # Is Object Male
        #---------------

        self.IsHim = FALSE

        
        #-----------------
        # Is Light Source?
        #-----------------

        # True if this object is capable of producing light. More to the
        # point, any object with a true IsLightSource will be included in
        # the Global.LightSourceList.

        self.IsLightSource = FALSE

         
        #-----------
        # Is Liquid?
        #-----------

        # Returns true if the object is liquid, false if not.

        self.IsLiquid = FALSE

        
        #-------
        # IsLit?
        #-------

        # Returns true if the object is *ACTUALLY* producing light at the
        # moment, false if not.

        self.IsLit = FALSE

        
        #-------------------------------------
        # Is Object Referred to in the plural?
        #-------------------------------------

        self.IsPlural = FALSE

        
        #-----
        # Open
        #-----

        # Return true if the object is open, false if it is closed or open
        # isn't applicable.

        self.IsOpen = FALSE

        
        #---------
        # Openable
        #---------

        # By default most objects are not openable.

        self.IsOpenable = FALSE

        
        #----------
        # Poisonous
        #----------

        # Returns true if the object is poisonous if eaten, drunk, or (in
        # the case of actors) bitten by.

        self.IsPoisonous = FALSE

        
        #--------
        # Potable
        #--------

        # Returns true if this is a foodstuff or (if liquid) a thirst
        # quencher.

        self.IsPotable = FALSE

        
        #------------
        # Is Scenery?
        #------------

        # Scenery isn't described unless you examine it explicitly.

        self.IsScenery = FALSE

        
        #------------
        # Transparent
        #------------

        # Returns true if the object is transparent (will pass vision),
        # false if not.

        self.IsTransparent = FALSE


        
        #---------
        # Location
        #---------

        # Location is a property. It holds self's parent. A parent is merely
        # the object that contains self. Note rooms don't ordinarily have a
        # Location, but everything else does.
        #
        # Also note you should use the Where() method to get an object's
        # location, since floating objects don't use a Location property
        # (it's always set None, Where() will return the object's "true"
        # location.
        #
        # To set an object's location always use the MoveInto() method
        # instead of setting the location variable directly. This is required
        # because you also have to set the LOCATION'S CONTENTS property!

        self.Location = None


        
        #-------------
        # Maximum Bulk
        #-------------

        # This is the maximum number of "bulk units" the object can contain.
        # The default is 0 (it can't contain anything).

        self.MaxBulk = 0
        
        #---------------
        # Maximum Weight
        #---------------

        # The maximum amount of weight an object can "carry". Notice that we
        # make a distinction between "carry" and "contain". A container can
        # contain maxbulk units, but any amount of weight. An actor, however,
        # has both a maximum bulk AND a maximum weight they can "contain".

        self.MaxWeight = 0
        
        #--------------
        # Object Memory
        #--------------

        # This list contains all objects this object has encountered. It is
        # used with the MEMORIZE() and REMEMBERS() functions to determine what
        # objects this particular object has encountered before.
        #
        # You may have guessed this is part of an actor's "memory", to
        # determine what an actor knows or doesn't know. It's placed here so
        # that any object can be "read" for objects it has encountred or
        # knows about.

        self.Memory = []

                #--------------
        # Parser Favors
        #--------------
        
        # Mark this property TRUE only for objects that will appear in the same
        # room, when you want one object to be always used and the other 
        # eliminated. This applies mainly to ClassLandmark objects, usually
        # walls when you want your wall to override the existing wall object.

        self.ParserFavors = FALSE
        

        
        #------------------
        # Starting Location
        #------------------

        # The starting location lets the author indicate where objects are
        # ORIGINALLY located, this value is used when the game restarts to
        # let the object be returned to its inital location. It's also used
        # by the SetUpGame method to put the object where it belongs in the
        # first place.

        self.StartingLocation = None


        
        #------
        # Value
        #------

        # The value of an object is generally what it adds to the score. For
        # a room the value is the number of points given for discovering it.

        self.Value = 0

        
        #-------
        # Weight
        #-------

        # The weight of an object. This is measured in arbitrary units (we
        # suggest 1 unit = 1/10 of a pound) but be consistant! For example
        # don't use a weight of 10 to mean 1 pound of nails but 10 tons of
        # explosives!

        self.Weight = 0


    
    #----------------------------------
    # Allowed By Verb As Direct Object?
    #----------------------------------

    # This method is used by the SpecificDisambiguation() method as a test
    # method when disambiguating direct objects.

    def AllowedByVerbAsDObj(self):
        """True if verb allows this object to be a direct object"""

        
        #-------------------------------------
        # Verb's allowed object list is empty?
        #-------------------------------------

        # If the verb's allowed direct object list is empty, then the verb
        # allows all objects as direct objects.

        if len(P.CV().OnlyAllowedDObjList) == 0:
            return SUCCESS


        #----------------------
        # self on allowed list?
        #----------------------

        # If self is on the allowed list return success, otherwise failure.

        if self in P.CV().OnlyAllowedDObjList:
            return SUCCESS
        else:
            return FAILURE

    
    #------------------------------------
    # Allowed By Verb As indirect Object?
    #------------------------------------

    # This method is used by the SpecificDisambiguation() method as a test
    # method when disambiguating indirect objects.

    def AllowedByVerbAsIObj(self):
        """True if verb allows this object to be an indirect object"""

        
        #-------------------------------------
        # Verb's allowed object list is empty?
        #-------------------------------------

        # If the verb's allowed indirect object list is empty, then the verb
        # allows all objects as indirect objects.

        if len(P.CV().OnlyAllowedIObjList) == 0: return SUCCESS


        #----------------------
        # self on allowed list?
        #----------------------

        # If self is on the allowed list return success, otherwise failure.

        if self in P.CV().OnlyAllowedIObjList:
            return SUCCESS
        else:
            return FAILURE


    
    #------------
    # Check Actor
    #------------

    
    # The parser calls this method for the object the player addressed as an
    # actor as part of the specific disambiguation of the command. If the
    # object is NOT an actor, say an error message and return FAILURE. This
    # will abort the player's command.
    #
    # If the object IS an actor (something that can be commanded, like a
    # person or a robot or an animal that understands commands) simply
    # return SUCCESS.
    #
    # By default all classes EXCEPT ClassActor and its descendants use this
    # method to say "You are out of your mind" and return FAILURE. You may
    # want to override this method to have a variety of snide comments for
    # players who command the landscape to do things...

    def CheckActor(self):
        """Returns true if object is an actor, says an error and returns false if not."""

        #----------
        # Is Actor?
        #----------

        # If this object is an actor, return success.

        if self.IsActor: return SUCCESS

        #-----------
        # NOT ACTOR!
        #-----------

        # This object isn't an actor, or we wouldn't have gotten this far.
        # Complain (which returns FAILURE).

        return Complain(P.AP().NotAnActor)

    
    #-----------------
    # Bulk of Contents
    #-----------------

    # This method returns the total bulk of an object's contents BUT DOES NOT
    # COUNT THE OBJECT's BULK!

    def ContentBulk(self):
        """Returns Total bulk of CONTENTS, excludes self.Bulk."""
        TotalBulk = 0
        for Obj in self.Contents: TotalBulk = TotalBulk + Obj.CurrentBulk()
        return TotalBulk
    
    #--------------
    # ContentWeight
    #--------------

    # Unlike the bulk of a rigid container vs a soft-sided container the
    # WEIGHT of an object will always be the weight of the object plus all
    # objects within it.
    #
    # You can, of course create things like anti-gravity pallets or bags of
    # holding that always have a fixed weight, but in general the above
    # statement holds true.

    def ContentWeight(self):
        """Returns weight of self's contents EXCLUDING self.Weight"""
        TotalWeight = 0
        for Obj in self.Contents: TotalWeight = TotalWeight + Obj.CurrentWeight()
        return (TotalWeight)
    
    #-------------
    # Current Bulk
    #-------------

    # The CURRENT bulk of an object is the bulk of the object itself PLUS the
    # bulk of its contents. Since we have a method that returns the contents
    # bulk it becomes trival to return an object's current bulk.
    #
    # Consider a sack. Folded up neatly the sack may have a bulk of 1 or even
    # 0. But as you put objects in the sack its bulk increases.
    #
    # This means you'll have to change the definition of this method for a
    # container with rigid sides--a box always has the same bulk (not
    # weight!) no matter what goes into it--unless the box is open and you
    # allow stuff to stick out, in that case it's ok to use this method.

    def CurrentBulk(self):
        """Returns current bulk (self.bulk + self.ContentsBulk()"""
        return self.Bulk + self.ContentBulk()

    
    #-----------------------------------
    # Is interior Currently Illuminated?
    #-----------------------------------

    # CurrentlyIlluminated is related to IsLit, but is superior to that
    # property because it also looks for Self in the Global.LitParentList.
    #
    # Primarily, it's intended for checking to see if light is present in
    # rooms, but like everything else in Universe we made it as generic as
    # we could.

    def CurrentlyIlluminated(self):
        """Returns TRUE if self is currently illuminated"""
        return (self.IsLit or (self in Global.LitParentList))

    
    #---------------
    # Current Weight
    #---------------

    # An object's current weight is the weight of the object itself plus
    # the weight of its contents. Unless you're creating an anti-gravity
    # device or bag of holding this method needn't be messed with, unlike
    # the CurrentBulk method, which differs for rigid and expandable objects
    # (boxes and sacks, for instance).

    def CurrentWeight(self):
        """Returns self.weight + self.Contents.Weight"""
        return self.Weight + self.ContentWeight()


    
    #--------------
    # Describe Self
    #--------------

    
    # The describe self method takes one argument, the type of description
    # desired. Unlike the various "Desc" methods, this function actually
    # says something.
    #
    # A  - A Description
    # Adj    - Adjective description (adjective phrase)
    # Here   - Here Description
    # Long   - Long Description
    # MultiShort - Multi short Description (unneeded but for consistancy...)
    # Name   - Name description (name phrase)
    # Read   - Read Description
    # Self   - Calls SmartDescribeSelf() (See below)
    # Short  - Short Description
    # The    - The Description

    def DescribeSelf(self,DescriptionArgument="Long"):
        """Says object description based on passed argument"""

        #-------------------------------
        # Translate Description Argument
        #-------------------------------

        # A short cut for the many IF tests below. UCDA stands for Upper
        # Case Description Argument. We translate it to upper case so that
        # the game author (you) has a safety margin for spelling arguments
        # in any case preferred.

        UCDA=string.upper(DescriptionArgument)

        #----------------------------
        # Say Appropriate Description
        #----------------------------

        if UCDA == "SMART":  self.SmartDescribeSelf();return
        if UCDA == "SHORT":  Say(self.SDesc());return
        if UCDA == "LONG":   Say(self.LDesc());return
        if UCDA == "A":      Say(self.ADesc());return
        if UCDA == "THE":    Say(self.TheDesc());return
        if UCDA == "HELLO":  Say(self.HelloDesc());return
        if UCDA == "HERE":   Say(self.HereDesc());return
        if UCDA == "CONTENT":Say(self.ContentDesc());return
        if UCDA == "NAME":   Say(self.NamePhrase);return
        if UCDA == "ADJ":    Say(self.AdjectivePhrase);return
        if UCDA == "READ":   Say(self.ReadDesc());return
        if UCDA == "MULTISHORT": Say(self.MultiSDesc());return
        if UCDA == "PLURAL": Say(self.PluralDesc());return
        if UCDA == "SOUND":  Say(self.SoundDesc());return
        if UCDA == "ODOR":   Say(self.OdorDesc());return
        if UCDA == "TASTE":  Say(self.TasteDesc());return
        if UCDA == "FEEL":   Say(self.FeelDesc());return
        if UCDA == "TAKE":   Say(self.TakeDesc());return
        if UCDA == "DROP":   Say(self.DropDesc());return


    
    #-------------
    # Enter Object
    #-------------

     
    # This method implements the ability for one object to enter another. If
    # entry is forbidden, then the method complains, returns false, and does
    # not move the object.
    #
    # By default this method returns true when:

    # A) Self is an actor and Obj.Bulk+self.ContentBulk<=self.MaxBulk AND
    #     Obj.Weight+self.ContentWeight<=self.MaxWeight.
    #
    # B) Self is not an actor and Obj.Bulk+self.ContentBulk<=self.MaxBulk.
    #
    # In other words, an actor has to be able to *LIFT* the object as well
    # as have room to carry it.

    def Enter(self,Object):
        """Returns true if object able to enter self, false and says complaint if not"""

        
        #------------------
        # Self is Openable?
        #------------------

        # If Self isn't openable, then obviously you won't be able to put the
        # object into self.

        if not self.IsOpen:
            Complaint = You() + " can't fit " + \
                        Object.TheDesc() + " into " + self.TheDesc() + "."
            return Complain(SCase(Complaint))
        
        #--------------
        # Self is Open?
        #--------------

        # If self isn't open you can't put an object in it either, but you
        # should give a different complaint. Notice we're using the
        # "$thedesc" macro here
        # to replace the more cumbersome "DescribeSelf('THE')"

        if not self.IsOpen:
            Complaint = SCase(self.TheDesc() + " is closed.")
            return Complain(Complaint)

        
        #--------------------------
        # Is Object too big to fit?
        #--------------------------

        if Object.Bulk + self.ContentBulk() > self.MaxBulk:
            Complaint = Object.TheDesc() + " won't fit."
            return Complain(Complaint)
        
        #------------
        # Move Object
        #------------

        # We've passed the tests, now it's time to actually move the
        # object into self. Note when you move an object into another
        # ALWAYS use the object's MoveInto method, it takes care of
        # all the messy details. See the MoveInto method definition to
        # see how hard moving an object really is!

        Object.MoveInto(self);


        return SUCCESS


    
    #------------------------------
    # Returns Parser Favored Status
    #------------------------------

    # This method returns the ParserFavors property. This is used as the final
    # step in the disambiguation process. It works like this. If, after all 
    # other disambiguation occurs, there are still multiple objects the parser
    # checks to see if one or more are favored (self.Favored is TRUE).
    #
    # If so it keeps only favored objects, eliminating unfavored ones. If
    # no objects in the final list are favored, then nothing happens and all
    # unfavored objects are kept.

    def Favored(self):
        return self.ParserFavors


    
    #------------------------
    # Insert self into Object
    #------------------------

    # Method called by InsertVerb objects to put self (Rock) into another
    # object (Box).

    def Insert(self, Object, Multiple=FALSE, Silent=FALSE, Spontaneous=FALSE):
        """Place an object into/onto/under/behind the container."""

        
        #-------------------------
        # Get Expected Preposition
        #-------------------------

        Preposition = self.VerbPreposition()

        
        #-----------------------------------
        # Complain If Wrong Preposition Used
        #-----------------------------------

        if Preposition <> Object.ContainerPrepositionDynamic:
            return Complain(self.WrongPrepositionDesc(Object,Spontaneous))
        
        #----------------------
        # Fail if Enter() fails
        #----------------------

        if not Object.Enter(self): return FAILURE

                
        #-------------------------------------
        # Say Insert Description Unless Silent
        #-------------------------------------

        if not Silent: Say(self.InsertedDesc(Object, Spontaneous))

        
        #---------------
        # Return Success
        #---------------

        return SUCCESS


    
    #--------------------------
    # Is Reachable From object?
    #--------------------------

    
    # This method answers the question "Does the object passed to me have an
    # unobstructed path to reach me?" To return true both objects must share
    # the same ParentOpen().
    #
    # An unobstructed path exists for an object (either obj or self) when
    # they are directly contained by the ParentRoom, or every container
    # between them is open.
    #
    # For instance, let's take an example. The player comes upon a gem inside
    # a (closed but transparent) bottle inside an (open) box in the forest.
    # If we call Gem.IsReachable(Me) would it return true?
    #
    # No, it wouldn't. Player.ParentOpen() is Forest, but Gem.ParentOpen()
    # is bottle, they do not match. If the bottle were open, Gem.ParentOpen()
    # would be Forest, and an unobstructed path would exist.
    #
    # Note that an unobstructed path can exist in the dark (compare
    # IsVisible below).

    def IsReachable(self,Object):
        """Returns true if self can reach object, false otherwise"""

        #----------------------
        # Get Reachable Parents
        #----------------------

        # Get the REACHABLE parents of both Self and the passed objects.

        SelfParent = self.ParentReachable()
        ObjectParent  = Object.ParentReachable()

        #--------------------
        # Valid and the same?
        #--------------------

        
        # The IF test below is somewhat bizarre. You might think a simple
        # SelfParent = ActParent would work--and it would except for one
        # thing. The ParentReachable() method can return None.
        #
        # So? you ask. They won't match if one returns None, so what's the
        # problem?
        #
        # But what if they BOTH return None? That means NEITHER Self nor
        # Object has a reachable parent, which means they obviously can't
        # reach each other!
        #
        # It's a simple enough trick. In order to succeed all three parts
        # of the test have to be true. That means if either OR BOTH Self and
        # Object have no reachable parent (are, in effect, either a room or
        # have a nil location) the function will automatically fail.

        if SelfParent and ObjectParent and SelfParent == ObjectParent: return SUCCESS

        #-----
        # Fail
        #-----

        return FAILURE

    
    #---------------------------
    # Is Self Visible to object?
    #---------------------------

    
    # This method answers the question "Can the object passed to me see me?"
    # To return true both objects must share the same ParentVisible().
    #
    # A clear line of sight exists for an object (either obj or self) when
    # they are directly contained by the parentroom, or every container
    # between them is either open or transparent.
    #
    # For instance, let's take an example. The player comes upon a gem inside
    # a (closed but transparent) bottle inside an (open) box in the forest.
    # If we call Gem.IsVisible(Me) would it return true?
    #
    # Yes it would. Player.ParentLit() is Forest, so is Gem.ParentLit().
    # Forest is lit, the line of sight from gem goes through the bottle
    # (it's closed but transparent) and through the box (since the box is
    # open) to the Forest.


    def IsVisible(self,Object):
        """Returns TRUE if self can see object"""

        #--------------------
        # Get Visible Parents
        #--------------------

        # Get the VISIBLE parents of both Self and the passed objects.

        SelfParent = self.ParentVisible()
        ObjParent  = Object.ParentVisible()

        #--------------------
        # Valid and the same?
        #--------------------

        
        # The IF test below is somewhat bizarre. You might think a simple
        # SelfParent = ObjParent would work--and it would except for one thing.
        # The ParentVisible method can return None.
        #
        # So? you ask. They won't match if one returns None, so what's the
        # problem?
        #
        # But what if they BOTH return None? That means NEITHER Self nor Object
        # has a visible parent, which means they obviously can't see each other!
        #
        # It's a simple enough trick. In order to succeed all three parts
        # of the test have to be true. That means if either OR BOTH Self and
        # Object are in the dark the function will automatically fail.

        if SelfParent and ObjParent and SelfParent == ObjParent:
            return SUCCESS

        #----------------------------------
        # Check to see if Object is carried
        #----------------------------------
        
        
        #------------------------------
        # Why Count Carried As visible?
        #------------------------------

        # You might wonder why we want to count objects the player is carrying as
        # visible. Think about it. If you were carrying something, a rock say, and
        # you wanted to drop it in a dark room you should be able to.
        #
        # If we didn't count carried objects as visible actions that would be 
        # reasonable would be forbidden because the object literally couldn't be
        # seen.
        


        if self in P.CA().Contents:
            return SUCCESS

        #-----
        # Fail
        #-----

        return FAILURE


    
    #-------------
    # Leave Object
    #-------------

    # This method implements the ability for one object to leave another. If
    # departure is forbidden, then the method complains, returns false, and
    # does not move the object.
    #
    # By default this method returns true. Note that self.Leave(Obj) is
    # intended purely as a check method, unlike Enter which does a great
    # deal more.

    def Leave(self,Object):
        """Return SUCCESS if able to leave object, FAILURE if can't"""
        return SUCCESS

    
    #----------
    # Look Deep
    #----------

    
    # This function is called to print a message when a player looks
    # behind, under, or inside an object. Usually it will return one
    # of the following (whichever is appropriate):
    #
    # You don't see anything interesting under the rock.
    # You don't see anything interesting behind the rock.
    # It is impossible to look inside a rock.
    #
    # There are 3 properties which affect how the object responds
    # either with disinterest or impossibility scolds). These are:
    #
    # self.CantLookInside (defaults to TRUE)
    # self.CantLookUnder  (defaults to FALSE)
    # self.CantLookBehind (defaults to FALSE)
    # self.CantLookOn     (defaults to FALSE)


    def LookDeep(self):
        """
        Returns FAILURE and complains appropriately if it can't look
        inside/under/behind/on object, or SUCCESS and prints a shallow
        contents of the object.
        """

        
        #----------------------------------------
        # Determine Appropriate CantLook Property
        #----------------------------------------

        
        # We need to pick which of the four CantLook properties to
        # use (CantLookInside, CantLookBehind, CantLookOn or
        # CantLookUnder). The first step is to call
        # self.VerbPreposition() and place the result in Attr. This
        # method will either return the current verb's
        # ExpectedPreposition property or "inside" if the current
        # verb doesn't have an ExpectedPreposition property.
        #
        # self.VerbPreposition() is just a "shorthand" method. If you
        # look at the method you'll see it's really just two lines of
        # code. However, because we call it in lots of different
        # places it's easier and less confusing to make a method call
        # rather than repeat those two lines of code each time.
        #
        # Another advantage of using a method here instead of the
        # actual code is called ABSTRACTION. Abstraction allows us to
        # put the details of getting the verb's preposition in one
        # place instead of several places. If we later change our
        # minds about how to get the verb's preposition (perhaps
        # adding additional code) we only have to do it one place
        # instead of half a dozen! This is a cornerstone of good
        # programming design. It saves you time, effort, and
        # eliminates a particularly frustrating kind of bug, caused by
        # forgetting to change the code in one place when you've
        # changed it everywhere else.
        #
        # In other words, abstraction is all gain, and no pain!

        Attr = self.VerbPreposition()

        #-----------------------
        # Assemble property name
        #-----------------------

        # Attr contains either "inside" or "under" or "behind" (unless
        # the author screwed up the spelling when they created the
        # verb of course!).
        #
        # This line changes "inside"/"behind"/"under" to
        # "CantLookInside"/"CantLookBehind"/"CantLookUnder"
        #
        # Notice the capitalization of the expected pronoun, it
        # won't work otherwise!

        Attr = "CantLook" + string.capitalize(Attr)

        
        #------------
        # Can't Look?
        #------------

        # Attr contains "CantLookInside", "CantLookBehind", or some
        # other appropriate CantLook property. So self.Get(Attr) is
        # actually saying something like:
        #
        # self.CantLookInside
        #
        # or whatever CantLook property is appropriate. If the CantLook
        # property is true, then we complain with the CantLookDesc()
        # method.

        if self.Get(Attr):
            return Complain(self.CantLookDesc())

        #----------------
        # Nothing to see?
        #----------------

        # If there are no items in the object, we just say there's
        # nothing interesting to see.

        if len(self.Contents) == 0:
            return Complain(self.DontSeeInterestingDesc())
        
        #--------------------------
        # Describe Shallow Contents
        #--------------------------

        # If we've gotten this far there's something to see, so we
        # list it.

        Say(self.LookDeepDesc())


        return SUCCESS


    
    #-------------
    # Mark Pronoun
    #-------------

    # This method is generally called by the HereDesc() method, it records this
    # object into the pronoun dictionary. There are 4 pronoun types, this
    # routine only sets the singlular ones.
    #
    # If the object is male (IsHim) put self in the HIM slot, if IsHer put it
    # in the HER slot, if neither put it in the IT slot. Notice this code
    # DELIBERATELY written to handle cases where an object is BOTH male and
    # female. This can be handy for actors who's gender is in question or not
    # immediately known.

    def MarkPronoun(self):
        """Places object in P.AP().PronounDict dictionary"""

        if self.IsHim: P.AP().PronounsDict[HIM] = self
        if self.IsHer: P.AP().PronounsDict[HER] = self
        if not self.IsHim and not self.IsHer: P.AP().PronounsDict[IT] = self


    
    #----------------
    # Memorize Object
    #----------------

    # This method lets Self memorize another object. It uses both the
    # REMEMBER method and the MEMORY list property.

    def Memorize(self,Object):
        """Memorizes the passed object (puts in self.Memory list)"""

        #------------------------
        # Do we already remember?
        #------------------------

        # If we already remember Object it's in MEMORY, so we do nothing
        # except return immediately.

        if self.Remembers(Object): return

        #------------
        # Memorize it
        #------------

        # Memorization is easy, we simply append OBJ to MEMORY. Notice we
        # also have the object memorize self. This allows us a reciprocal
        # memory, useful for disambiguation.

        self.Memory.append(Object)
        Object.Memorize(self)

        return

    
    #---------
    # MoveInto
    #---------

    
    # MoveInto Is used to move an object from one room (or container,
    # they're very similar) into another. Note this is a "primative",
    # it does nothing in the way of checking to see if the move is 
    # valid, that's up to the objects initiating the move.


    def MoveInto(self,Container):
        """Move self into container"""

        #----------------------------
        # Is Self currently anywhere?
        #----------------------------

        
        # Ok, Self is the object we're moving into a container (could be a
        # room, could be a box, could be an actor...)
        #
        # However, self.Location (where self is currently) might be None--in
        # other words self isn't anywhere! (Don't laugh, None locations are
        # not only legal, they're handy for tucking stuff away so the player
        # can't stumble across it).
        #
        # if Self IS somewhere, it's in the Contents list of it's
        # location--so the first thing we do is remove it from its location's
        # contents list.

        if self.Location <> None: self.Location.Contents.remove(self)

        #----------------------
        # Add Self to Container
        #----------------------

        # Next we add Self to the container's Content list--if Container
        # isn't None!

        if Container <> None: Container.Contents.append(self)

        #-----------------------------
        # Inform  Self of New Location
        #-----------------------------

        
        # Adding Self to the location's content list is only half the battle.
        # By doing so you tell the LOCATION it has a new object in it, but
        # you haven't told SELF it's in a new place!
        #
        # That's what the line of code below does.

        self.Location = Container

        return


    
    #-----------
    # Parent Lit
    #-----------

    
    # This method returns the outermost container that Self could illuminate
    # if lit. If SelfMustBeLit is true this function returns nil if self's
    # IsLit property is nil.
    #
    # In other words, if SelfMustBeLit is false we're just checking the
    # last parent self COULD light if it was lit, if SelfMustBeLit is true
    # we're checking to see the last parent self IS lighting...


    def ParentLit(self,SelfMustBeLit):
        """Determines outermost parent that either is lit or could be lit"""

        #---------------------
        # Check If Self Is Lit
        #---------------------

        # First check to see if Self must be lit, if it isn't it obviously
        # won't illuminate it's container, much less a room!

        if SelfMustBeLit and not self.IsLit: return None

        #---------------------
        # Find Last Lit Parent
        #---------------------

        
        # This loop is the heart of the beast. Object is going to be our test
        # variable, we start by assigning self to it. We set LastObject to
        # nil because we haven't examined the first object yet. (The reason
        # we need LastObject is explained in "Safety Net" below.)
        #
        # Let's use an example. We have a lit lamp in a glass bottle in an
        # open box in the forest. What is the last object it will illuminate?
        #
        # Obviously the forest, since there's an unobstructed path for the
        # light to reach the forest.
        #
        # Here's a breakdown. Obj starts off as Lamp. Lamp's location is
        # Bottle, so we test Lamp.Bottle.IsOpen, which is false (the bottle is
        # closed). Next we test Lamp.Bottle.IsTransparent, which is true. Since
        # the And connecting the tests requires both be true, the IF fails,
        # so we make LastObject = Lamp and Object = Bottle.
        #
        # The second time through the loop Bottle.Box.Open is true, so the IF
        # fails again and we make LastObject = Bottle and Object = Box.
        #
        # The third time through the loop Box.Forest.Open is false (by
        # default rooms are closed, only nested rooms are open) AND
        # Box.Forest.Transparent is false so the IF test works and we return
        # Forest.
        #
        # Had the box been CLOSED the function would have returned Box, had
        # the bottle been opaque the function would have returned Bottle.

        Object = self
        LastObject = None

        while Object.Where() <> None and Object.Where() <> SpaceTime:
            if not Object.Where().IsOpen and not Object.Where().IsTransparent:
                return Object.Where()
            LastObject = Object
            Object = Object.Where()

        #-----------
        # Safety Net
        #-----------

        
        # The above loop works fine when rooms are declared as not open and
        # not transparent. But what happens if for some reason you defined
        # a room as either open or transparent?
        #
        # In our example above let's assume you made Forest Open for some
        # reason. In that case the IF test would have failed and Obj would
        # have become Forest. Forest.Location is None, so the loop would
        # terminate BUT WOULD NOT HAVE RETURNED ANYTHING!
        #
        # This obviously isn't what you want. To cover yourself ALWAYS assume
        # the worst. In this case we return LastObject checked (Forest),
        # which means the function will work regardless of Forest's Open and
        # transparent properties. In other words, it will tolerate mistakes
        # on your part without failing and making a bug that's probably going
        # to take you days to find!
        #
        # This "safety net" has several names in the programming community,
        # ranging from the formal "proactive debugging" or "assertion
        # checking" to the slightly risque "CYA".

        return Object
    
    #-----------------
    # Parent Reachable
    #-----------------

    
    # This method returns the outermost container that Self could travel to
    # physically
    #
    # For example, if we have a gem in an (open) bottle in a (closed) box in
    # the forest, then this function would return box. If the box were open
    # it would return forest.

    def ParentReachable(self):
        """Outermost parent reachable by self"""

        #----------------------
        # Find Last Open Parent
        #----------------------

        
        # This loop is the heart of the beast. Object is going to be our test
        # variable, we start by assigning it to self. We set LastObject to None
        # because we haven't examined the first object yet. (The reason we
        # need LastObject is explained in "Safety Net" below.)
        #
        # Let's use an example. We have a gem in an (open) glass bottle in an
        # open box in the forest. Is there an unobstructed path between gem
        # and forest?
        #
        # Yes, since both box and bottle are open.
        #
        # Here's a breakdown. Object starts off as Gem. Gem's location is
        # Bottle, so we test Gem.Bottle.Open, which is true (the bottle is
        # open). The IF fails, so we make LastObj = Gem and Obj = Bottle.
        #
        # The second time through the loop Bottle.Box.Open is true, so the IF
        # fails again and we make LastObj = Bottle and Obj = Box.
        #
        # The third time through the loop Box.Forest.Open is false (by default
        # rooms are closed, only nested rooms are open) so the IF test works
        # and we return Forest.
        #
        # Had the box been CLOSED the function would have returned Box, had
        # the bottle been closed the function would have returned Bottle.

        Object = self
        LastObject = None

        while Object.Where() <> None and Object.Where() <> SpaceTime:
            if not Object.Where().IsOpen: return Object.Where()
            LastObject = Object
            Object = Object.Where()

        #-----------
        # Safety Net
        #-----------

         
        # The above loop works fine when rooms are declared as not open.
        # But what happens if for some reason you defined a room as open?
        #
        # In our example above let's assume you made Forest Open for some
        # reason. In that case the IF test would have failed and Obj would
        # have become Forest. Forest.Location is nil, so the loop would
        # terminate BUT WOULD NOT HAVE RETURNED ANYTHING!
        #
        # This obviously isn't what you want. To cover yourself ALWAYS assume
        # the worst. In this case we return LastObj (Forest), which means the
        # function will work regardless of Forest's Open property. In other
        # words, it will tolerate mistakes on your part without failing and
        # making a bug that's probably going to take you days to find!
        #
        # This "safety net" has several names in the programming community,
        # ranging from the formal "proactive debugging" or "assertion checking"
        # to the slightly risque "CYA".

        return Object

    
    #------------
    # Parent Room
    #------------

    # This method returns the outermost room that holds this object. It
    # does so by looping through each parent object until a None
    # location is returned, at which point we know we've reached the
    # outermost room.

        # The heart of the routine is the while loop. Let's take this example.
    # Suppose we have the player carrying rock in a box in a forest.
    # Obviously, Me.ParentRoom(), Box.ParentRoom(), and Rock.ParentRoom()
    # should all return Forest, but how?
    #
    # Let's take the rock as our example. We start off by setting the
    # variable Obj to Rock.
    #

    # Each time we hit the loop we have to test Object.Location to see if it
    # has one. Rock does, so we set the object to the rock's location which
    # is Box. Remember, the Location property holds the object that
    # contains this object.
    #
    # The second time through the loop Object.Location is Forest, so we set
    # Object to Forest.
    #
    # This time, however, Forest.Location is None, so we ignore the loop and
    # return Object (Forest) as our parent room.
    #
    # Basicly, locations form a "tree" that you can follow back to the root.
    # The root will always be a room for all objects that exist in the
    # game's "physical" universe. You can play games by setting an object's
    # location to None, which effectively removes the object from existance
    # (along with all contents). You should be very careful doing so,
    # however.
    #
    # By the way, Forest.ParentRoom() returns Forest!

    def ParentRoom(self):
        """Returns room self is in, no matter how many containers self is in."""
        Object = self
        while Object.Where()<>None and Object.Where()<>SpaceTime:
            Object = Object.Where()
        return Object
    
    #---------------
    # Parent Visible
    #---------------

    # This method returns the outermost container that Self can "see".
    # Light must be present for this function to return an object.
    # Therefore if a rock were in a closed opaque box (with no light
    # source) this function would return None, since no parent is
    # visible.
    #
    # This function employs some programming tricks explained below.

    def ParentVisible(self):
        """Returns first visible parent of self"""

        
        #-----------------------------------------
        # Determine parent potentially illuminated
        #-----------------------------------------

        
        # The ParentLit(FALSE) method returns the outermost parent self would
        # illuminate IF self were producing light. (We don't care if self is
        # actually producing light or not, we just want a "line of sight" to
        # the last object self can "see".
        #
        # By the way, the trick is using ParentLit(None). If we tried to use
        # ParentLit(TRUE) it wouldn't work. ParentLit(TRUE) would return None
        # unless self actually were lit.
        #
        # NOTE: You might be wondering why we stored self.ParentLit(None) in
        #   a variable since we turn around and use it in the very next
        #   line of code.
        #
        # If you look closely you'll notice that Parent is actually used
        # 3 times in the if test. ParentLit(None) is "expensive", that
        # means it takes a significant (to the computer) amount of time
        # to run.
        #
        # If we used it directly we'd triple the time required for this
        # method to run! ParentVisible is used a LOT, so we want to
        # optimize the performance as much as possible.
        #
        # Always pay attention to the amount of work your code does. The
        # more work, the longer it will take, and the slower your game
        # will run. Sometimes you can afford slow code, sometimes you
        # can't.
        #
        # The more often a function or method is called, the more vital
        # it is that it run quickly.

        Parent = self.ParentLit(FALSE)
        
        #----------------
        # Is Parent None?
        #----------------

        # If Parent is None we return None, since nilspace is unlit by
        # fiat. This test prevents an interesting and subtle bug from
        # occuring.
        #
        # I discovered that when a player sees an object and that
        # object then vanishes (location becomes None) and the player
        # then says "look at <vanished object> the next IF test below
        # fails, and PAWS produces an error message.
        #
        # It turns out that methods MUST have an object, None.IsLit
        # (for example) generates an error, since None has no 
        # properties or methods.

        if Parent == None: return None

        
        #---------------------
        # See if there's light
        #---------------------

        # Parent might be a lit room, for example if the rock were in the
        # (lit) forest then the forest would be visible. On the other hand it
        # might be in a cavern that's illuminated by the player's lantern. In
        # that case Parent.IsLit is None, however one of the elements in the
        # Global list LitParentList will be Cavern so you're free and clear.

        if Parent.IsLit or Parent in Global.LitParentList: return Parent
        
        #----------
        # No Light?
        #----------

        # If there's no light then the parent isn't visible, return
        # None.

        return None



    
    #----------
    # Remembers
    #----------

    # This method allows an object to recall whether or not it has
    # encountered the passed object before. It uses the MEMORY property
    # to do this, if an object is in the MEMORY list property the
    # object will remember it, if not, it won't.

    def Remembers(self,Object):
        """Returns True if self remembers object"""

        #-----------------
        # Remember object?
        #-----------------

        
        # This test is very straightforward. IN is the built-in Python
        # function that returns TRUE if object is in self.Memory. If the
        # object isn't in MEMORY, then IN returns FALSE (and we fail)
        # otherwise it returns TRUE and we pass.

        if Object in self.Memory or \
           Object.__class__ == ClassDirection or \
           self.__class__ == ClassDirection:
            return SUCCESS
        else:
            return FAILURE


    
    #--------------------------
    # Smart Description Of Self
    #--------------------------

    
    # This is the method called by other classes and services when they
    # want the object to describe itself in the most typical way. Note
    # this method actually says text on the screen, unlike the DESC
    # methods below.
    #
    # For example, self.Enter might call self.SmartDescribeSelf (in a
    # room) so the room would describe itself via short and long
    # descriptions, and also list the room's contents, etc. (Objects
    # in a list would most likely be described by calling 
    # Obj.SmartDescribeSelf!)
    #
    # By default this function says the long description of an object
    # and any blatant sound or smell the object is putting off.

    def SmartDescribeSelf(self):
        """Say most typical description of self"""
        P.CA().Memorize(self)
        self.DescribeSelf("HERE")
        if self.IsTransparent and self.Contents: Say(self.LookDeepDesc())
        if self.IsBlatantSound: self.DescribeSelf("SOUND")
        if self.IsBlatantOdor:  self.DescribeSelf("ODOR")

    
    #-----------------
    # Verb Preposition
    #-----------------

    # This method returns the preposition used with the verb. It's
    # intended to make various methods easier to understand, such
    # as LookDeep(), WrongPreposition(), and Insert()
    #
    # What it does is return the ExpectedPreposition property of the 
    # current verb, the verb used in the player's command. If there
    # is no ExpectedPreposition property in the verb's command then
    # "inside" is assumed. Note we use the Get() method to retrieve
    # ExpectedPreposition to protect ourselves from crashing the 
    # program if ExpectedPreposition hasn't been defined.

    def VerbPreposition(self):
        Preposition = P.CV().Get("ExpectedPreposition")
        if Preposition == None: Preposition = "inside"
        return Preposition


    
    #-----------------
    # Where Is Object?
    #-----------------

    # Call this function when you want to know where an object is
    # instead of calling on Location. Floating objects will override
    # this method with one that returns the current actor's location.
    #
    # See also the comments on MoveInto() and Location.

    def Where(self):
        """Returns Object's Location. Overridden for floating objects"""
        return self.Location


    
    #-----------------------------------------------------------------
    #                           "Descriptions"
    #-----------------------------------------------------------------

    # Descriptions are ways an object (for example, a rock) can describe
    # itself in various parts of speech. Descriptions are the building
    # blocks for the more complex DescribeSelf method.
    #
    # Every Description is a method, never a property, and it always returns
    # a string, never saying anything.

    
    #--------------
    # A Description
    #--------------

    # The ADesc by default is the object's article, a space, and the object's
    # short description. For example "a small grey rock" or "an elephant".
    #
    # It's used whenever you want to use the object and the correct article
    # in a sentence.

    def ADesc(self):
        """Returns 'a small grey rock'"""
        return "%s %s" % (self.ArticleDesc(),self.SDesc())
    
    #--------------------
    # Amnesia Description
    #--------------------

    # Used when the Me object doesn't remember an object.

    def AmnesiaDesc(self):
        """Returns 'I don't remember ever seeing a rock around here"""

        return "I don't remember ever seeing %s %s around here." % \
               (self.ArticleDesc(),self.NamePhrase)
    
    #--------------------
    # Article Description
    #--------------------

    # The article description is used to say the article. There are
    # cases where the two might not match, for example "umbrella" can
    # use either "a" or "an" depending on the adjective used, or IF
    # an adjective is used.

    def ArticleDesc(self):
        """Returns 'a' or 'an'"""
        return self.Article

    
    #-----------------------
    # Can't Look Description
    #-----------------------

    # This function return "It's impossible to look under/behind/inside
    # the rock. The appropriate word is supplied by the current verb's
    # ExpectedPreposition property. If the current verb has no
    # ExpectedPreposition property then "inside" is used.

    def CantLookDesc(self):
        """Can't look behind/under/in the object"""

        Preposition = P.CV().Get("ExpectedPreposition")
        if not Preposition: Preposition = "inside"

        return "It's impossible to look %s %s." % (Preposition,self.TheDesc())

    
    #------------------------
    # Can't Reach Description
    #------------------------

    # If the actor (generally Me) can see but not reach the object in
    # question, AND the verb used doesn't have a CantReach method of its
    # own, this one is used.

    def CantReachDesc(self):
        """Returns 'You can't reach the rock.'"""

        
        #---------------------------
        # Does self have a location?
        #---------------------------

        # If self does NOT have a location, return an empty string.

        if self.Where() == None: return ""
        
        #--------------------------------
        # Assemble first part of sentence
        #--------------------------------

        # The sentence will normally read "You can't reach the rock." Notice
        # we're using the FormatYou property from Actor, and the TheDesc
        # method from self (the rock).

        Sentence = SCase("%s can't reach %s." % (You(),self.TheDesc()))
        
        #-------------------------
        # Is Self's Location Open?
        #-------------------------

        # If the rock is in the open that's all there is to it, so we return
        # the sentence as is.

        if self.Where().IsOpen: return Sentence
        
        #-----------------
        # Add open warning
        #-----------------

        # However, if the rock is inside a closed container (say a closed
        # glass box) then we add "You'll have to open the glass box first."
        #
        # Notice we're using the TheDesc method from self.LOCATION, not
        # self! In other words, if self's location is GlassBox, we're
        # using GlassBox.TheDesc, not Rock.TheDesc.

        Sentence = Sentence + " %s'll have to open %s first." % \
            (You(),self.Where().TheDesc())
        
        #--------------------------------
        # Return fully assembled sentence
        #--------------------------------

        return Sentence
    
    #----------------------
    # Can't See Description
    #----------------------

    # Used as an error method on the SpecialDisambiguation routine.

    def CantSeeDesc(self):
        """You can't see any rock here."""

        Sentence = "%s can't see any %s here." % (You(),self.NamePhrase)

        return SCase(Sentence)

    
    #---------------------------
    # Choose Article Description
    #---------------------------

    # This method will return either TheDesc() or ADesc(), as appropriate.
    # If the current actor has met this object before, we use TheDesc().
    # Otherwise, if the object is a new one, we use ADesc()

    def ChooseArticleDesc(self):
        """TheDesc() or ADesc() depending on if the object is known."""
        if self.Remembers(P.CA()):
            return self.TheDesc()
        else:
            return self.ADesc()

    
    #--------------------
    # Content Description
    #--------------------

    # This method allows an object to describe its contents. This assumes a
    # standard object, special objects should override this method.

    def ContentDesc(self,Level = None,Shallow = FALSE):
        """
        Returns string describing object's contents in an indented
        outline style
        """

        
        #-------------------
        # Find Current Level
        #-------------------

        # When the first call is made, it's always made with no arguments.
        # This test lets us make the current level 0, which allows us to add
        # 1 to the level for self's contents.

        if Level == None:
            CurrentLevel = 0
        else:
            CurrentLevel = Level
        
        #----------------
        # Properly Indent
        #----------------

        # We want all new objects to say their contents indented on a new
        # line so we start with a line break (~n), then indent by the
        # current level's number of tabs (~t).

        Sentence = " ~n " + Indent(CurrentLevel)

        
        #-----------------------
        # Get the object's Adesc
        #-----------------------

        # The description used when the player types 'Inventory' or
        # 'Look into <object>' is "a rock", "an elephant", etc.

        if self <> Global.Player: Sentence = Sentence + self.ADesc()
        
        #--------------------------------------
        # Check if shallow, open or transparent
        #--------------------------------------

        # If doing a shallow (non-recursive) contents description, or
        # if the object is neither open nor transparent we want to fail
        # silently, that is, we want to do nothing. This allows us to
        # use the ContentDesc method recursively, that is, letting an
        # object call it, then objects referenced by it call their own
        # ContentDesc, and so forth.

        if Shallow: return Sentence
        if not (self.IsOpen or self.IsTransparent or self == Global.Player): return Sentence

        
        #--------------
        # Has contents?
        #--------------

        # An object's contents are stored in the Contents list. If the
        # length of this list is 0 the object is empty, if not it has
        # something in it.
        #
        # Notice we assign Prefix one of two strings based on whether
        # there's contents or not. We then indent on a new line and set
        # the prefix. This says basically either "The box is empty" or
        # "The box contains:".

        LC = len(self.Contents)

        if LC == 0:
            Prefix = self.EmptyDesc()
        else:
            Prefix = self.ContentsPrefixDesc()

        Sentence = Sentence + Choose(CurrentLevel==0,""," ~n ") + Indent(CurrentLevel) + Prefix
        
        
        #--------------------------------------
        # Recursive Call To Content Description
        #--------------------------------------

        
        # Recursion simply means call the same method for another object.
        # Let's take the simple example of the player carrying some keys,
        # a rock, a box, and in the box a bottle of water and a ring.
        #
        # We would like the (open) box to list its contents as well. So we
        # want to see:

        # You are carrying:
        #    some keys
        #    a rock
        #    a box
        #       The box contains:
        #  a bottle
        #  The bottle contains:
        #     some water
        #  a ring
        #
        # Here's how it works. The keys and rock are closed and opaque, so a
        # call to both keys.DescribeSelf('Content') and
        # rock.DescribeSelf('Content') produces no output. (Look at the
        # first IF test in this method).
        #
        # But Box.DescribeSelf('Content') fires the loop below for the box,
        # which obediently lists the bottle, which fires the loop below,
        # which then lists the bottle's contents. Since the water isn't open
        # it fails silently, making no more calls. That ends
        # Bottle.DescribeSelf('Content'), returning to
        # Box.DescribeSelf('Content') which then lists the ring, which is
        # opaque.

        for Obj in self.Contents:
            Sentence = Sentence + Obj.ContentDesc(CurrentLevel + 1)
        
        #----------------
        # Return Sentence
        #----------------

        # Now we've got a monster string, so we can return with it.

        return Sentence

    
    #----------------------------
    # Contents Prefix Description
    #----------------------------

    # This method is used when a container has contents.

    def ContentsPrefixDesc(self):
        """returns 'The treasure chest contains:'"""
        return SCase(self.TheDesc() + " contains:")
    
    #-----------------------------
    # Contents Shallow Description
    #-----------------------------

    # Unlike ContentsDesc() which lists self's contents, and then
    # for any open or transparent items lists THEIR contents as well
    # in an indented outline style list, this function only does a
    # "shallow" list, ie it lists self's immediate contents, but not
    # the contents of open or transparent items in self.
    #
    # For example, assume we look in a bag. The bag contains a bell,
    # a book, a candle, and a glass box. Further since the glass box
    # is transparent we can see it contains a ball.
    #
    # Here's what ContentsDesc() would display:
    #
    # The bag contains:
    #   a bell
    #   a book
    #   a candle
    #   a glass box
    #       The glass box contains:
    #           a ball
    #
    # Here's what ContentsShallowDesc() would display, assuming the
    # player had never seen any of the items before.
    #
    # The bag contains a bell, a book, a candle, and a glass box.

    def ContentsShallowDesc(self):
        """
        returns a flat list of the objects immediate contents, e.g.:
        "a gold coin, the wand, the old book, and a toothbrush"
        """

        
        #----------------------
        # Init Needed Variables
        #----------------------

        # TempList holds the intermediate results of calling
        # ChooseArticleDesc() for each object in self.Contents.
        # ListCount tells us how many objects are in self.Contents.

        TempList = []
        ListCount = len(self.Contents)
        
        #--------------------------
        # 0 or 1 Items in Contents?
        #--------------------------

        # If there are no contents, return "nothing". If there's
        # just one return it's ChooseArticleDesc(). In either case
        # these tests simplify the coding for contents of more than
        # one object.

        if ListCount == 0: return "nothing"
        if ListCount == 1: return self.Contents[0].ChooseArticleDesc()

        
        #-----------------------------
        # 2 or more items in Contents?
        #-----------------------------

        
        # If there are two or more items in Contents then we first
        # obtain a list of strings that are the ChooseArticleDesc()
        # results for each item. ChooseArticleDesc() returns either
        # ADesc() ("a rock") if the player hasn't seen it before or
        # TheDesc() ("the rock") if they have.
        #
        # Then we use string.join to join all but the last item in
        # Templist together with ", " (a comma and a space), add the
        # word "and", and finally add the last item in TempList.
        #
        # So if self.Contents contained [Bell, Book, Candle], Result
        # would become (assuming he'd seen none of the three before)
        # "a bell, a book and a candle".


        for Obj in Contents: TempList.append(Obj.ChooseArticleDesc())
        Result = string.join(TempList[:-1],", ") + " and " + TempList[-1]

        #--------------
        # Return Result
        #--------------

        return Result


    
    #----------------------------------
    # Don't See Interesting Description
    #----------------------------------

    # This function return "You t's impossible to look under/behind/inside
    # the rock. The appropriate word is supplied by the current verb's
    # ExpectedPreposition property. If the current verb has no
    # ExpectedPreposition property then "inside" is used.

    def DontSeeInterestingDesc(self):
        """
        You don't see anything interesting under/behind/inside the
        object.
        """
        Preposition = P.CV().Get("ExpectedPreposition")
        if not Preposition: Preposition = "inside"

        return SCase("%s %sn't see anything interesting %s %s." % (You(),
                                                             Do(),
                                                             Preposition,
                                                             self.TheDesc()))

    
    #------------------
    # Empty Description
    #------------------

    # This description is used when a container is empty.

    def EmptyDesc(self):
        """Returns 'The treasure chest is empty.'"""
        return SCase(self.TheDesc()+" is empty.")

    
    #-----------------
    # Feel Description
    #-----------------

    # All objects have a feel to them, silk is soft, granite is rough and
    # hard, etc.

    def FeelDesc(self):
        """Returns 'It feels like an ordinary rock to me'"""

        Phrase = "%s feels like an ordinary %s to %s." % \
         (self.PronounDesc(),self.NamePhrase,Me())

        return SCase(Phrase)
    
    #-------------------
    # Ground Description
    #-------------------

    def GroundDesc(self):
        """Returns 'The ground looks ordinary to me.'"""
        Phrase = "The ground looks ordinary to %s." % Me()
        return SCase(Phrase)
        
    
    #------------------
    # Hello Description
    #------------------

    def HelloDesc(self):
        """Returns 'Did you really expect a rock to speak?'"""

        Phrase = "Did you really expect %s to speak?" % self.ADesc()

        return SCase(Phrase)
    
    #-----------------
    # Here Description
    #-----------------

    
    # The HereDesc contains the description of the object when being
    # described by a room. By default it isn't very useful, you'll probably
    # want to override it in your object definitions.

    def HereDesc(self):
        """Returns the description of self as a room would describe it"""
        
        #------------------------
        # Record Correct Prounoun
        #------------------------

        # This records the object to the appropriate pronoun. For example:
        # "There is a rock here." Since rock is an "it" we need to record
        # the rock as "it". Then when the player says "get it" we know what
        # "it" refers to. This also works for "him" and "her". "Them", "all",
        # and "everything" is handled differently.

        self.MarkPronoun()

        
        #-----------------
        # Set Descriptions
        #-----------------

        # Here_Description is used if the object is NOT scenery, No_Description
        # is used if it is.
        #
        # Notice we override the default Here_Description if the
        # Descriptions dictionary is present and has a "Here" key.
        # This allows the option of using the ServiceDictDescription
        # with this function and not having to override it. Very
        # handy for objects of ClassItem.

        Here_Description = "There's %s here." % self.ADesc()

        if hasattr(self,"Descriptions"):
            if self.Descriptions.has_key("HereDesc"):
                Here_Description = self.Descriptions["HereDesc"]

        No_Description = ""

        
        #------------
        # Is Scenery?
        #------------

        # If Self is scenery (a useless prop to add atmosphere) we return no
        # description, else we return the Here description.

        if self.IsScenery:
            return No_Description
        else:
            return Here_Description


    
    #---------------------
    # Inserted Description
    #---------------------

    # Returns the description when one item is inserted into another,
    # for instance "The rock goes inside the bag." or "You put the
    # rock inside the bag."

    def InsertedDesc(self, Object, Spontaneous=FALSE):

        
        #----------------
        # Get Preposition
        #----------------

        # The preposition we want to use is self's dynamic one. 

        Preposition = P.IOL()[0].ContainerPrepositionDynamic

        
        #-------------------
        # Construct Sentence
        #-------------------

        # If Spontaneous is true says "The rock goes inside the bag."
        # Otherwise it says "You put the rock inside the bag."

        if Spontaneous:
            Sentence = "%s %s %s %s." % (self.TheDesc(),
                                          Agree("go", Object),
                                          Preposition,
                                          Object.TheDesc())
        else:
            Sentence = "%s %s %s %s %s." % (You(),
                                            Agree("put"),
                                            self.TheDesc(),
                                            Preposition,
                                            Object.TheDesc())

        
        #--------------------------------
        # Return Sentence Correctly Cased
        #--------------------------------

        # We make sure the first letter in the sentence is capitalized.

        return SCase(Sentence)

    
    #-----------------
    # Long Description
    #-----------------

    
    # The LDesc is the object's long description. For an object this is the
    # description provided by looking at the object, not the description
    # provided as part of a room.
    #
    # For instance, the rock is described as "a small grey rock" in general,
    # or "There is a small rock here." when described as part of the room's
    # contents. But when looked at closely it might say "The rock is oblong,
    # rough, and about the right size to fit comfortably in your hand."
    #
    # In a room, the LDesc is the room's visual description.

    # By default the long description isn't very helpful. Notice we use
    # NamePhrase instead of SDesc.

    def LDesc(self):
        """Returns 'It looks like an ordinary rock to me'."""

        BrokenDescription = ""
        if self.IsBroken: BrokenDescription = "(but broken) "

        RV = "%s looks like an ordinary %s to %s."

        RV = RV % (self.PronounDesc(),self.NamePhrase,Me())
        return SCase(RV)
    
    #---------------
    # Look Deep Desc
    #---------------

    # This function returns the string for looking in/behind/on/under
    # an object. It is only called when there are actually objects 
    # to be described.

    def LookDeepDesc(self):
        """
        return a string such as:  "In the box you see a key and an
        envelope."
        """

        return "%s %s %s %s %s. " % (SCase(self.ContainerPrepositionStatic),
                                     self.TheDesc(),
                                     You(),
                                     Agree("see"),
                                     self.ContentsShallowDesc())

    
    #--------------------------
    # Short Description In List
    #--------------------------

    # The MultiSDesc is used by the parser when running commands with
    # multiple direct objects, for example "Take All". The parser says
    # the MultiSDesc followed by a colon and the text for that object. This
    # lets you change the description of an object when it's part of a list.

    def MultiSDesc(self):
        """Returns 'small gray rock:'"""
        return self.SDesc() + ":"
    
    #---------------
    # No Description
    #---------------

    # Returns an empty string. For those times when you want to say nothing
    # at all.

    def NoDesc(self):
        """Returns ''"""
        return ""

    
    #----------------------------------
    # Not Allowed with verb description
    #----------------------------------

    # Error condition for SpecialDisambiguation when object not allowed with
    # verb.

    def NotWithVerbDesc(self):
        """Returns 'That doesn't make sense'"""
        return P.AP().Nonsense

    
    #-----------------
    # Odor Description
    #-----------------

    def OdorDesc(self):
        """Returns 'It smells like an ordinary small grey rock to me.'"""

        Phrase = "%s smells like an ordinary %s to %s." % \
                 (self.PronounDesc(),self.NamePhrase,Me())

        return SCase(Phrase)
        
    
    #--------------------
    # Pronoun Description
    #--------------------

    # The pronoun varies based on the IsHim/IsHer properties. If neither are
    # set the pronoun is 'it', otherwise the pronoun is 'him' or 'her'
    # respectively.

    def PronounDesc(self):
        """Returns 'he', 'she', or 'it'"""

        if self.IsHim: return "him"
        if self.IsHer: return "her"
        return "it"
    
    #-------------------
    # Plural Description
    #-------------------

    # Used to describe the object in plural, for example "coins". By
    # default this is the SDesc followed by an S. Plural forms in English
    # are lamentably unpredictable however. There's "es" (Indexes), word
    # shift (Hippotomous to Hippottomi), etc.

    def PluralDesc(self):
        """Returns 'small gray rocks'"""

        return self.SDesc() + "s"
        
    
    #--------------------
    # Reading Description
    #--------------------

    # The description of an item when read. By default it complains you
    # can't read the ADesc.

    def ReadDesc(self):
        """Returns 'You can't read a small grey rock.'"""

        Phrase = "%s can't read %s." % (You(),self.ADesc())

        return  SCase(Phrase)
    
    #------------------
    # Short Description
    #------------------

    # SDesc is the short description. As you can see a short description
    # isn't exactly easy to come by! The basic idea is to assemble the
    # description from the AdjectivePhrase and NamePhraseDesc. However,
    # if the item gets broken somehow we want to put the word broken in
    # front of the NamePhrase.

    def SDesc(self):
        """Returns 'small grey rock'"""

        RV = ""
        if len(self.AdjectivePhrase) > 0: RV = self.AdjectivePhrase + " "
        if self.IsBroken: RV = RV + "broken "
        RV = RV + self.NamePhrase
        return RV
        
    
    #----------------
    # Sky Description
    #----------------

    def SkyDesc(self):
        """Returns 'The sky looks ordinary to me.'"""
        Phrase = "The sky looks ordinary to %s." % Me()
        return SCase(Phrase)

    
    #------------------
    # Sound Description
    #------------------

    # This is the sound the object is making. By default most objects don't
    # make a sound, so we say "the <whatever> isn't making any noise."

    def SoundDesc(self):
        """Returns 'The rock isn't making any noise.'"""
        return SCase(self.TheDesc() + " isn't making any noise.")
    
    #------------------
    # Taste Description
    #------------------

    # Most objects have some sort of taste but it's seldom overpowering.

    def TasteDesc(self):
        """Returns 'It tastes like an ordinary rock to me.'"""

        Phrase = "%s tastes like an ordinary %s to %s." % \
                 (self.PronounDesc(),self.NamePhrase,Me())

        return SCase(Phrase)
    
    #----------------
    # The Description
    #----------------

    # There's only one definite article in English, so the default
    # TheDesc is simply the word "the" followed by a space and the
    # object's short description.

    def TheDesc(self):
        """Returns 'the small grey rock'"""
        return "the " + self.SDesc()
    
    #-------------------
    # Ground Description
    #-------------------

    def WallDesc(self):
        """Returns 'The wall looks normal to me.'"""
        Phrase = "The wall looks normal to %s." % Me()
        return SCase(Phrase)

    
    #------------------------------
    # Wrong Preposition Description
    #------------------------------

    # Called when verb had one preposition (like "under") and the
    # object had another (like "inside").
    #
    # Returns "The rock can't go inside the table." if Spontaneous is
    # TRUE or "You can't put the rock in the table." if Spontaneous is
    # FALSE. Spontaneous defaults to FALSE.

    def WrongPrepositionDesc(self, Object, Spontaneous=FALSE):

        
        #----------------------------
        # Get Preposition Player Used
        #----------------------------

        Preposition = self.VerbPreposition()
        
        #-------------------
        # Construct Sentence
        #-------------------

        # If Spontaneous is TRUE the sentence should read "The rock
        # can't go inside the table.". If Spontaneous is FALSE the
        # sentence should read "You can't put the rock inside the
        # table.".

        if Spontaneous:
            Sentence = "%s can't go %s %s. " % (self.TheDesc(),
                                                Preposition,
                                                Object.TheDesc())
        else:
            Sentence = "%s can't put %s %s %s. " % (You(),
                                                    self.TheDesc(),
                                                    Preposition,
                                                    Object.TheDesc())

        
        #---------------------------------
        # Return Sentence In Sentence Case
        #---------------------------------

        # Make sure the first letter of the sentence is capitalized.

        return SCase(Sentence)






#===========================================================================
#                               ClassActor
#===========================================================================

# An actor is an object capable of executing commands. Me is an actor, with
# additional capabilities. By default an actor is simply a BasicThing that
# that returns true for the IsActor property. Anything declared as an Actor
# (or having Actor for an ancestor) will be placed on the actor list.
#
# In addition, many parts of speech that relate to actors are defined here.
#
# Note by default the actor class is intended to create the player's
# character (Me).

class ClassActor(ServiceFixedItem,ClassBasicThing):
    """Class used to create Actors"""
    
    #--------------------
    # Initialize Instance
    #--------------------

    # Notice we're extending ClassBasicThing's init behavior. This is
    # necessary because we're adding (and changing) default valued instance
    # properties.

    def SetMyProperties(self):
        """Sets default instance properties"""
         
        self.IsActor    = TRUE
        self.Bulk       = 24    # 24 cubic feet (6' x 2' x 2')
        self.MaxBulk    = 10    # can carry 10 cubic feet
        self.MaxWeight  = 500   # can carry 50 pounds
        self.IsOpen     = TRUE  # actors must be open (inventory)
        self.Weight     = 1750  # 175 pounds
        
        #--------------------
        # Format Descriptions
        #--------------------

        # These are the parts of speech that are part of subject/verb
        # agreement.

        self.FormatMe      = "me"
        self.FormatYou     = "you"
        self.FormatYoum    = "you"
        self.FormatYour    = "your"

    
    def ADesc(self): return "yourself"
    
    #-------------------
    # Enter (Take Check)
    #-------------------

    # The only differences between this method and the standard (BasicThing)
    # method is the wording of the complaints.

    def Enter(self,Object):
        """Handles object entering self"""
        
        #------------------
        # Self is Openable?
        #------------------

        # If Self (the actor) isn't openable, then obviously they won't be
        # able to carry anything because they aren't openable. The PLAYER is
        # openable because of his inventory.

        if not self.IsOpenable:
            Complaint = "%s can't carry %s!" % (You(),Object.TheDesc())
            return Complain(SCase(Complaint))
            
        
        #--------------------------
        # Is Object too big to fit?
        #--------------------------

        if Object.Bulk + self.ContentBulk() > self.MaxBulk:
            Complaint = "%s can't manage to carry anything else." % You()
            return Complain(SCase(Complaint))

        
        #---------------------
        # Is object too heavy?
        #---------------------

        if Object.Weight > self.MaxWeight:
            Complaint = "%s can't even lift it, much less carry it!" % You()
            return Complain(SCase(Complaint))
            
        
        #-------------------
        # Is load too heavy?
        #-------------------

        if Object.Weight + self.ContentWeight() > self.MaxWeight:
            return Complain(SCase("%s load is too heavy." % Your()))

        
        #------------
        # OK to enter
        #------------

        Object.MoveInto(self);
        self.Memorize(Object)
        return TURN_ENDS
        
    
    def LDesc(self):
        Message = "%s %s about the same as always." % (You(),Agree('look'))
        return Message

    
    def TheDesc(self): return "yourself"
    
    #-------
    # Travel
    #-------

    # This method allows the actor to travel along the map just like the
    # player's character. Specific actors can override this method and any
    # class that needs to travel should also override it (ie a vehicle).
    #
    # This method checks for the indicated travel direction in 3 places,
    # the actor's location's Map, DefaultMap, or Global.DefaultMap in
    # that order. If direction's in none of those it complains with
    # P.AP().NotADirection.

    def Travel(self,Vector):
        """Have self travel in Vector direction"""
        
        #--------------------------------
        # Direction in My location's map?
        #--------------------------------

        # Map is a dictionary, so the has_key method tests to see if the
        # instance's Vector is in the map.

        if self.Where().Map.has_key(Vector):

            #----------------------------
            # Direction IS in map, get it
            #----------------------------

            
            # If direction is a string, it MUST be a complaint, so say it
            # and return FAILURE.
            #
            # If direction is an object first check and see if the room allows
            # the current actor to leave, if it does not return FAILURE (Leave()
            # will say the complaint).
            #
            # If it does allow exit, call the Direction's (a room's) Enter
            # method and return the result.

            Direction = self.Where().Map[Vector]
            if type(Direction) == type(""): return Complain(Direction)
            if not self.Where().Leave(self): return TURN_CONTINUES
            return Direction.Enter(self)
            
        
        #---------------------------------
        # Direction in Room's Default Map?
        #---------------------------------

        if self.Where().DefaultMap.has_key(Vector):

            #---------------------------------
            # Direction in room's default map?
            #---------------------------------

            
            # If the direction isn't in the default map either, complain.
            #
            # Otherwise, Direction will be the direction Who wants to go.
            # If Direction is a string, complain. If not, try to make Who
            # leave MyLocation. If it fails return FAILURE. (Leave() will
            # complain).
            #
            # Otherwise, simply return the Direction's Enter() method's
            # result (SUCCESS or FAILURE). Enter() will move Who into itself
            # or say the complaint.

            Direction = self.Where().DefaultMap[Vector]
            if type(Direction) == type(""): return Complain(Direction)
            if not self.Where().Leave(Who): return FAILURE
            return Direction.Enter(P.CA())
        
        #---------------------------------
        # Direction in Global default map?
        #---------------------------------

        # If the direction isn't in the default map either, complain.
        #
        # Otherwise, Direction will be the direction Who wants to go.
        # If Direction is a string, complain. If not, try to make Who
        # leave MyLocation. If it fails return FAILURE. (Leave() will
        # complain).
        #
        # Otherwise, simply return the Direction's Enter() method's
        # result (SUCCESS or FAILURE). Enter() will move Who into itself
        # or say the complaint.

        if not Global.DefaultMap.has_key(Vector): return Complain(P.AP().NotADirection)
        
        
        Direction = Global.DefaultMap[Vector]
        if type(Direction) == type(""): return Complain(Direction)
        if not self.Where().Leave(self): return FAILURE
        return Direction.Enter(self)



#=====================================================================
#                               Class Direction
#=====================================================================

# Directions are OBJECTS in PAWS, not prepositions like in TADS. This
# takes some getting used to if you're used to TADS. All normal
# directions are instantiated here. Some, like "tree" (climb tree)
# are handled as part of the class definition for those objects.

class ClassDirection(ClassBasicThing):

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.AdjectivePhrase = ""
        self.Location = None

    
    def Where(self): return P.CA().Location

    
    def TheDesc(self): return self.SDesc()
    #-----------------
    # Long Description
    #-----------------

    def LDesc(self):        
        return P.CA().Where().LDesc()



#------------------
# Direction Objects
#------------------

North = ClassDirection("north,n")
Northeast = ClassDirection("northeast,ne")
East = ClassDirection("east,e")
Southeast = ClassDirection("southeast,se")
South = ClassDirection("south,s")
Southwest = ClassDirection("southwest,sw")
West = ClassDirection("west,w")
Northwest = ClassDirection("northwest,nw")
Up = ClassDirection("up,u")
Down = ClassDirection("down,d")
Upstream = ClassDirection("upstream,us")
Downstream = ClassDirection("downstream,ds")
In = ClassDirection("in,inside")
Out = ClassDirection("out,outside")


#-----------------------
# Compass Direction List
#-----------------------


# This list contains 8 directions. These directions are actually the
# objects defined above. They represent the 8 horizontal compass
# points, and are used mainly to set the DefaultMap horizontal
# directions to the same error message (see DefaultMap below).
#
# Notice directions are listed starting with north and continuing in a
# clockwise circle. Thus North is always 0, Northwest is always 7).
#
# Finally, notice we're adding this to the Global object. This lets us
# easily access it.

Global.CompassList = [North,
                      Northeast,
                      East,
                      Southeast,
                      South,
                      Southwest,
                      West,
                      Northwest]

#------------
# Default Map
#------------


# The default map is used when a room's map doesn't contain a given direction. For example,
# when North is undefined in the room map then North is searched for in the default map.
#
# The default map is intended to reduce the game author's work load. You can define a class
# that changes the default map to have all eight horizontal directions say "There is a wall
# there." instead of "You can't go that way."
#
# The default map primarily allows a way for you to set up a default error message for a
# given direction, without having to fill each room's map over and over again.
#
# Notice we add this property to the global object.

Global.DefaultMap = {North:      "You can't go that way.",
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


#=====================================================================
#                               ClassRoom
#=====================================================================

# Rooms are locations where a player can go to and look around. Many of
# their methods and properties are inherited from their direct ancestor,
# BasicThing.

class ClassRoom(ClassBasicThing):
    """Class used to create Rooms"""
    
    #------------
    # Default Map
    #------------

    # If no map is specified, this one is used. This particular default map
    # doesn't let you go anywhere, but at least each direction will give a
    # reasonable response.

    DefaultMap = {North:      "You can't go that way.",
                  Northeast:  "You can't go that way.",
                  East:       "You can't go that way.",
                  Southeast:  "You can't go that way.",
                  South:      "You can't go that way.",
                  Southwest:  "You can't go that way.",
                  West:       "You can't go that way.",
                  Northwest:  "You can't go that way.",
                  Up:         "There's no way up from here.",
                  Down:       "There's no way down from here.",
                  Upstream:   "There's no stream here.",
                  Downstream: "There's no stream here.",
                  In:         "There's nothing here to enter.",
                  Out:        "You're not in anything at the moment."}
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.AdjectivePhrase = ""
        self.HasGround = TRUE
        self.HasSky = TRUE
        self.HasWall = TRUE
        self.IsLit = TRUE
        self.IsOpen = TRUE
        self.IsOpenable = TRUE
        self.IsOutside = FALSE
        self.IsTransparent = FALSE
        self.Location = SpaceTime
        self.MaxBulk = 32000
        self.MaxWeight = 32000
        self.Visited = FALSE
        self.Map = {}

    
    #------
    # Enter
    #------

    
    # The room's Enter method overrides its immediate ancestor (BasicThing)
    # because we want to do more than BasicThing's enter method provides for.
    #
    # Notice that ANY object can enter a room! This includes the player, of
    # course, but it also includes other actors (not too surprizing) AND it
    # includes literally any object!
    #
    # This is because we use the room's Enter method when an actor drops an
    # object to perform the basic checks and (only if the object entering is
    # the current actor) describe the object's location.
    #
    # This might seen confusing, but it's code re-use at its best. If you
    # think about it, anything that enters a room (enters the room's Contents
    # list) should do so with the same rules as the player, except that the
    # object won't describe its new location on the screen. (Remote
    # controlled objects with cameras (like a space probe) aren't handled by
    # this routine very well, I'm afraid.

    def Enter(self,Visitor):
        """Room entry/item dropped method"""
        
        #---------------------
        # Use Inherited Method
        #---------------------

        # This line of code looks tricky but it really isn't. It's saying if
        # BasicThing's ENTER method returns false, then we fail. If you take
        # the time to look at BasicThing's Enter method you'll see that it
        # handles the ability for self (the room) to restrict the bulk of the
        # object entering. It also checks for open and openable properties,
        # so those have to be set to true in this class (since BasicThings by
        # default aren't openable or open). Finally, it does the actual
        # movement of the Visitor into the room. Notice the Visitor doesn't
        # actually have to be an actor, it could be any object, since this
        # routine is also used when dropping objects.

        if not ClassBasicThing.Enter(self,Visitor): return FAILURE

        
        #-----------------------------------
        # Make sure it's the player entering
        #-----------------------------------

        # The only time we want a description of the room is when it's the
        # player entering the room. Other objects should move but not
        # describe their surroundings.
        #
        # Notice we return success, because the object entered the room
        # successfully, whether or not it was Me.

        if id(Visitor) <>  id(Global.Player): return SUCCESS

        
        #-----------------------
        # Call SmartDescribeSelf
        #-----------------------

        # The SmartDescribeSelf method lists the room's description and
        # contents.

        self.SmartDescribeSelf()
        #---------------
        # Return Success
        #---------------

        return SUCCESS

    
    #-----------------
    # Feel Description
    #-----------------

    def FeelDesc(self):
        """Feeling Description"""

        Complaint = "Scrabbling around with %s hands uncovers nothing useful."
        return Complaint % Your()

    
    #-------------------
    # First View Of Room
    #-------------------

    # The first view of a room happens only once. By default we use this
    # method to increment the player's score when a room is found that
    # has a value. We also mark the room as visited.

    def FirstView(self):
        """Increments score & marks room as visited"""

        IncrementScore(self.Value)
        self.Visited = TRUE
        return ""

    
    #------------
    # Room's Odor
    #------------

    
    # If you looked at the code below you're probably scratching your head
    # trying to figure it out.
    #
    # This function (and many other DESC functions) take advantage of
    # Python's FORMAT operator -- %.
    #
    # It's really quit simple. The %s's in Complaint are there as place
    # holders. They're replaced by the variables in the parentheses following
    # the %. You can read the % sign as "replace with",
    #
    # You() = "you"
    # Do()  = "do"
    #
    # Thus "%s %sn't smell anything." becomes: "You don't smell anything."
    #
    # But assume it's Fred (the player's sidekick):
    #
    # You() = "he"
    # Do()  = "does"
    #
    # Making it: "HE DOESn't smell anything."


    def OdorDesc(self):
        """Default odor of room"""
        Complaint ="%s %sn't smell anything." % (You(),Do())
        return SCase(Complaint)

    
    #--------------------
    # Smart Describe Self
    #--------------------

    # This method replaces the one inherited from BasicThing, and compared
    # to that method is exceptionally "smart". Basically it describes the
    # room appropriately, including visible contents, blatant sounds and
    # smells, surroundings, etc. It also handles scoring, an optional first
    # view, and more.

    def SmartDescribeSelf(self):
        """Have room describe itself appropriately"""
        
        #--------------------
        # Determine Verbosity
        #--------------------

        # Verbosity is the level of detail. If Global.Verbose is true then
        # the player has selected verbosity, which means the full room
        # descriptions say all the time, otherwise they only say the
        # first time the player sees the room, or when they type look.

        Verbosity = FALSE
        if self.Visited == FALSE or Global.Verbose == TRUE: Verbosity = TRUE
        
        
        #-------------
        # Is Room Lit?
        #-------------

        # If the room isn't lit, there isn't a lot to describe, so fail and
        # that's that. Notice we do check for blatant noise or odor

        if self.CurrentlyIlluminated() == FALSE:
            Say("It's too dark to see anything.")

            if self.IsBlatantSound or self.IsBlatantOdor:
                Say("But darkness doesn't stop your other senses...")
                if self.IsBlatantSound == TRUE: self.DescribeSelf("SOUND")
                if self.IsBlatantOdor == TRUE:  self.DescribeSelf("ODOR")

            return FAILURE

        
        #-------------------------------
        # Display Room Short Description
        #-------------------------------

        # Display the room's short description, followed by a blank line.

        Terminal.NewLine()
        Say(self.SDesc(),Terminal.A_TITLE)

        if Verbosity == TRUE: Terminal.NewLine()

        Engine.BuildStatusLine()
        Terminal.DisplayStatusLine(Global.StatusLine)

        
        #--------------------
        # Describe First View
        #--------------------

        # The room must be lit since if it wasn't we wouldn't have gotten
        # this far, so if it hasn't been seen before, you can call the
        # FirstView method to do something special. FirstView can give an
        # extra comment, or do something that only happens the first time
        # the player sees the room.

        if not self.Visited == TRUE: Say(self.FirstView())
        
         
        #--------------------------
        # Say Long Room Description
        #--------------------------

        if Verbosity == TRUE: self.DescribeSelf("LONG")
        if self.IsBlatantSound: self.DescribeSelf("SOUND")
        if self.IsBlatantOdor:  self.DescribeSelf("ODOR")
        
        
        #-----------------
        # Set THEM Pronoun
        #-----------------

        # If the player refers to "them", "all", or "everything" then the
        # parser's going to assume they mean the contents of the current room.

        P.AP().PronounsDict[THEM] = self.Contents

        
        #------------------
        # Say Room Contents
        #------------------

        # Here's an illustration of a very powerful concept, encapsulation.
        # Basically, we simply tell Object to describe itself appropriately
        # and it does! All our hard work is beginning to pay off.
        #
        # This concept let us elegently express in 5 short easy to read
        # lines what would take a page of ugly code in another language.

        for Object in self.Contents:
            Global.Player.Memorize(Object)
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.SmartDescribeSelf()
            if Object.IsBlatantSound == TRUE: Object.DescribeSelf("SOUND")
            if Object.IsBlatantOdor == TRUE:  Object.DescribeSelf("ODOR")

        
    
    #----------
    # SoundDesc
    #----------

    
    # By default most rooms are silent. You're probably gagging over the
    # complex syntax. While intimidating it's very straightforward (really!)
    #
    # Who is just a shortcut for Global.LastActor (the actor who's been given
    # the command). Normally Who would be "Me" (the player's actor).
    #
    # SCase is the single-quoted equivalent of Caps(). It capitalizes
    # Who.Pronoun, which for any Player class object is "you". Who.FormatDo is
    # "do", Who.FormatES is "", so the actual returned value is:
    #
    # 'You don't hear anything.'
    #
    # It's assembled as:
    #
    # SCase('you')+' '+'do'+''+'n\'t hear anything.'
    #
    # Which translates to:
    #
    # "You"+" "+"do"+"n't hear anything."

    def SoundDesc(self):
        """Sound Description of room"""

        Who = P.CA();
        Complaint = "%s %sn't hear anything." % (You(), Do())
        return SCase(Complaint)

    


#===========================================================================
#                               Class Monster
#===========================================================================

# A monster is just an actor with the combat service. Notice how the
# combat service preceeds the class? This is to make sure any combat
# routines take precedence over the same methods in Actor Class.

class ClassMonster(ClassActor):
    def SetMyProperties(self):
        """Sets default instance properties"""
        pass


#===========================================================================
#                               Class Player
#===========================================================================

# Notice that Me is the instantiated object for the player, and that
# Me is immediately stored in Global.Player. Global.Player is used 
#throughout the system to refer to the player object.

class ClassPlayer(ClassMonster):
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.IsPlural = TRUE
        self.IsScenery = TRUE
        self.Location = None
        self.IsOpenable = TRUE

    def ContentsPrefixDesc(self): return "You are carrying:"
    def EmptyDesc(self): return "You are empty handed."
    def HereDesc(self): return ""
    def OdorDesc(self): return "You're a bit ripe, about two months overdue for your yearly bath. . ."
    def SmartDescribeSelf(self): pass
    def SoundDesc(self): return "You aren't making any noise."
    def TasteDesc(self): return "You decide against trying to taste yourself."

UniverseMe = ClassPlayer("me,myself")
Global.Player = UniverseMe



#===========================================================================
#                            Class Scenery
#===========================================================================

# This class is used to create otherwise useless props to add atmosphere.
# For example, if you mention a hairbrush in a room's description you might
# use this class so when a player tries to take it you say "The hairbrush
# is worthless" or some such.

class ClassScenery(ServiceFixedItem,ServiceDictDescription,ClassBasicThing):
    """Makes objects to use as scenery. (Unimportant fluff)"""

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.IsScenery = TRUE


#---------------
# Class Landmark
#---------------


# This class is used to give a special Where() method to scenery objects that
# are placed with "landmarks". A landmark is a special property of objects
# created with this class. The Landmark property contains the suffix of the
# "Has" property that acts as the landmark.
#
# For example, you might have a series of forests with different kinds of
# trees. For each forest room you create a "Has" property, for example
# HasPineTree and set it to TRUE.
#
# To create an object that is only present in rooms with the HasPineTree
# property, you'd set the Landmark property of the object to "PineTree". Thus
# the Where() method will look to see if the current room possesses
# a HasPineTree property.
#
# This class is *extremely* useful for creating objects that must appear in
# multiple rooms. All you have to do is set the appropriate Has property to
# True in the rooms you want
#
# This class is otherwise normal scenery.


class ClassLandmark(ClassScenery):

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.HasFloatingLocation = TRUE
        self.Landmark = ""

    def Where(self):
        if P.CA().Where().Get("Has"+self.Landmark):
            Global.Player.Memorize(self)
            return P.CA().Where()
        else:
            return None


#-----------------------
# Class Landmark Missing
#-----------------------


# This method is identical to ClassLandmark except for one crucial difference.
# This class's Where() method returns the current actor's location if the
# landmark is MISSING.
#
# For example, take the NoWall object, created with this class. The NoWall
# object appears in rooms where HasWall is FALSE--the exact opposite of the
# Wall object (created with ClassLandmark) which appears in rooms where
# HasWall is TRUE.
#
# In fact this class was created specifically to create the NoWall object--but
# it can be used for all sorts of objects that must appear if a landmark is
# missing.


class ClassLandmarkMissing(ClassLandmark):

    def Where(self):
        if not P.CA().Where().Get("Has"+self.Landmark):
            return P.CA().Where()
        else:
            return None
            


#===========================================================================
#                            Class Item
#===========================================================================

# Items are simply objects that can be taken. This means they have the
# Takeable Item service added to the BasicThing class.

class ClassItem(ServiceTakeableItem,ServiceDictDescription,ClassBasicThing):
    """Makes normal items for player to take, drop, etc."""

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.Descriptions["TakeDesc"]="Taken."




#===========================================================================~~KR
#                            Class Door
#===========================================================================


# Doors may be opened and closed. Doors may stand in as exits for a
# room.  If the player succeeds in entering a door (i.e., if it's
# open and they'll fit through), they will automatically be forwarded
# to the door's destination room.
#
# Note that doors that let you walk through in both directions are
# always implemented as pairs--one door object in each room. This has
# the advantage of letting doors connect ANY two rooms, thus making
# magical teleportals very easy to create.


class ClassDoor(ServiceOpenable, ClassScenery):

    
    def SetMyProperties(self):
        """Sets default instance properties"""

        #---------------
        # Automatic Open
        #---------------

        # Setting the AutomaticOpen option to TRUE allows a player to
        # go through a closed but unlocked door with just "east"
        # rather than "open door; east". It's a courtesy to the
        # player, not a door that opens by itself.

        self.AutomaticOpen = FALSE

        self.Destination = None
        self.IsLockable = FALSE
        self.IsLocked = FALSE
        self.IsOpen = TRUE
        self.IsOpenable = TRUE
        self.IsTransparent = FALSE
        self.Key = None
        self.Location = None
        self.MaxBulk = 32000
        self.MaxWeight = 32000
        self.NamePhrase = 'door'

        #-----------
        # Other Side
        #-----------

        # All doors are really made of two door objects, one in each
        # room the door connects. For example if there's a door
        # between the living room and the kitchen you'd have to make
        # one door object and put it in the living room, and make a
        # second door object for the kitchen. This property lets you
        # identify which door object is the twin to self.

        self.OtherSide = None

    
    #------
    # Close
    #------

    # Action called by CloseVerb.

    def Close(self, IsSecondTime=FALSE):
        """Close the door"""

        
        #------------------------------
        # Fail If This Door Won't Close
        #------------------------------

        # We call the ServiceOpenable Close method to actually close 
        # the door. If the door won't close (for whatever reason)
        # any complaints will already have been made, so we exit the
        # method immediately, returning failure.

        if not ServiceOpenable.Close(self, Silent=IsSecondTime):
            return FAILURE

        
        #---------------------------
        # Close Other Side If Needed
        #---------------------------

        # This gets a bit complex. Let's assume we have two doors
        # objects (remember it takes two door objects to make a door)
        # called LivingRoomDoor and KitchenDoor that make up the door
        # between the living room and the kitchen.
        #
        # Let's further assume that the player closes the
        # LivingRoomDoor. That means that the following statement
        # (eventually) get's executed.
        #
        # LivingRoomDoor.Close(FALSE)
        #
        # Then the IF test would be true and this would happen:
        #
        # KitchenDoor.Close(TRUE)
        #
        # Now, this is known as a recursive call, the method is in
        # effect calling itself. If we'd used FALSE on the kitchen
        # door instead of TRUE then the KitchenDoor would call the
        # LivingRoomDoor's Close which would call the KitchenDoor's
        # close...I'm sure you get the point. The IF test makes sure
        # both doors execute the Close() method exactly once
        #
        # By the way, the IF test says "if there's another door
        # object defined and this isn't the second time we've called
        # Close() then..."
        #
        # The IF test prevents an author's mistake from crashing the
        # program if they forget to define the other door.

        if self.OtherSide and not IsSecondTime:
            self.OtherSide.Close(TRUE)

        
        #---------------
        # Return Success
        #---------------

        return SUCCESS

    
    def Enter(self, Visitor):
        """
        Enter the door. This will complain if the door is closed or
        doesn't lead anywhere.  Otherwise, it passes the entry request
        to the destination room.
        """

        #-------------------------------
        # Door closed and not auto open?
        #-------------------------------

        # You can't go through if the door is closed.

        if not self.IsOpen:
            if not self.AutomaticOpen: return Complain("The door isn't open.")
            self.Open()

        #----------------
        # No Destination?
        #----------------

        # You can't go through if the Destination property isn't set.

        if not self.Destination:
            return Complain("The door doesn't lead anywhere.")

        #-----------------------
        # Too big to go through?
        #-----------------------

        # You can't go through if you're too fat :-).

        if Visitor.Bulk > self.MaxBulk:
            Complaint = Visitor.TheDesc() + " won't fit through the door."
            return Complain(Complaint)


        #-----------------------------------------
        # Pass Enter() request to destination room
        #-----------------------------------------

        # Pass the movement request to the destination room.
        # You can't go through if the room at the other end won't let
        # you in.

        return self.Destination.Enter(Visitor)

    
    def Open(self, IsSecondTime=FALSE):
        """Open the door"""
        # IsSecondTime will be false if this is the side of the door
        # the actor is on.  It will be true for the Open command
        # that is passed to the other side of the door.

        # First open this side of the door
        if ServiceOpenable.Open(self, Silent=IsSecondTime):
            # Now, if the door's other side exists and still needs to
            # be opened, open it too.
            if not IsSecondTime and self.OtherSide:
                self.OtherSide.Open(IsSecondTime=TRUE)
            return SUCCESS
        else:
            return FAILURE


    #---------------------
    # See Thru Description
    #---------------------

    # The response to "Look thru door" when the door is open.

    def SeeThruDesc(self): return ""


#======================================================================
#                         Class Lockable Door
#======================================================================

# A combination of ClassDoor with ServiceLockableThing.  Doors of this
# class can be locked and unlocked, as well as opened and closed. 
# Remeber that doors are always defined in pairs, one door object for
# each side of the door!

class ClassLockableDoor(ServiceLockable, ClassDoor):

    
    def SetMyProperties(self):
        self.IsLockable = TRUE
        self.IsLocked   = TRUE
        self.IsOpen = FALSE
        self.IsOpenable = TRUE
        self.LockOnClosing = FALSE
        self.LocksWithoutKey = FALSE

        #---------------------------
        # Transmit Locking/Unlocking
        #---------------------------

        # TransmitLocking and TrasmitUnlocking control whether locking
        # and unlocking events are automatically transmitted to the
        # other side of the door.  For example, if you lock the door
        # to my house from the inside, it automatically becomes locked
        # on the outside as well.  But if you lock an emergency exit
        # from the outside, it would still be unlocked from the inside
        # (so TransmitLocking should be FALSE). TransmitUnlocking
        # does the same thing for unlocking the door.

        self.TransmitLocking = TRUE
        self.TransmitUnlocking = TRUE

        self.UnlocksWithoutKey = FALSE

    
    def Open(self, IsSecondTime=FALSE):
        """Open the door"""
        # IsSecondTime will be false if this is the side of the door
        # the actor is on.  It will be true for the Open command
        # that is passed to the other side of the door.

        if self.IsLocked:
            return Complain(self.DoorIsLockedDesc())
        else:
            return ClassDoor.Open(self, IsSecondTime)

    
    #------
    # Close
    #------

    # This method basically calls the ClassDoor method and (if 
    # LockOnClosing is TRUE) calls the Lock() method.

    def Close(self, IsSecondTime=FALSE):
        """Close the door"""

        # Pass the closing request on to the superclass.  If you succeed
        # in closing the door, and if the door is supposed to lock
        # automatically, then lock it too.

        if not ClassDoor.Close(self, IsSecondTime): return FALSE

        if self.LockOnClosing:
            self.Lock(key=self.Key, IsSecondTime=IsSecondTime)

        return SUCCESS

    
    def Lock(self, key=None, IsSecondTime=FALSE):
        # Try to lock this side of the door
        if ServiceLockable.Lock(self, key, Silent=IsSecondTime):
            # If appropriate, try to lock the other side of the door.
            # Cheat and use whatever key is necessary.
            if self.TransmitLocking and not IsSecondTime and \
               isinstance(self.OtherSide, ServiceLockable):
                self.OtherSide.Lock(self.OtherSide.Key, IsSecondTime=TRUE)
            return SUCCESS

    
    #-------
    # Unlock
    #-------

    def Unlock(self, key=None, IsSecondTime=FALSE):

        
        #---------------------------------
        # Fail If This Side Doesn't Unlock
        #---------------------------------

        if not ServiceLockable.Unlock(self, key, Silent=IsSecondTime):
            return FALSE

        
        #----------------------------
        # Unlock Other Side If Needed
        #----------------------------

        if self.TransmitUnlocking and not IsSecondTime and isinstance(self.OtherSide, ServiceLockable):
           self.OtherSide.Unlock(self.OtherSide.Key, IsSecondTime=TRUE)

        #---------------
        # Return Success
        #---------------

        return SUCCESS

    
    #---------------------------
    # Door Is Locked Description
    #---------------------------

    def DoorIsLockedDesc(self):
        return self.TheDesc() + " is locked."




#======================================================================
#                           Class Under Hider Item
#======================================================================

# This class is used to create takeable items that reveal other items
# under them when taken. You'll note how simple the class is, we 
# basically just set properties. This class is just a standard
# ClassItem with a service called ServiceRevealWhenTaken

class ClassUnderHiderItem (ServiceRevealWhenTaken, ClassItem):

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ContainerPrepositionStatic = "under"
        self.ContainerPrepositionDynamic = "under"


#======================================================================
#                            ClassBehindHiderItem
#======================================================================

# This class reveals objects hiden behind it when taken. Like the
# ClassUnderHiderItem it's just a standard ClassItem with the 
# ServiceRevealWhenTaken. The only difference between this class and
# the ClassUnderHiderItem is the setting of the ContainerPreposition
# properties.

class ClassBehindHiderItem (ServiceRevealWhenTaken,ClassItem):
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ContainerPrepositionStatic = "behind"
        self.ContainerPrepositionDynamic = "behind"


#====================================================================
#                      ClassActivatableItem
#====================================================================

# This class is used to create items that can be activated/deactivated,
# (such as light sources, electrical devices, etc). It allows limited
# life devices and automatic deactivation of devices that run out of
# power/fuel.
#
# As is, the class is skewed toward light sources such as torches,
# candles, light sources, etc, but simply rewording a couple of string
# properties allow it to be used for all sorts of devices.
#
# Note this class exists primarily to combine the Activation service with the
# ClassItem class, as such it has no properties or methods so to satisfy the needs
# of the Python interpreter we create a SetMyProperties() method that simply
# executes a pass command (which does absolutely nothing).

class ClassActivatableItem(ServiceActivation, ClassItem):

    def SetMyProperties(self):
        """Sets default instance properties"""
        pass


#====================================================================
#                      ClassOpenableItem
#====================================================================

# This class is used to create items that can be opened/closed
# (such as boxes). Although all items can potentially contain other items
# openable items are complex enough to be interesting.
#
# Note this class exists primarily to combine the Openable service with the
# ClassItem class, as such it has no properties or methods so to satisfy the needs
# of the Python interpreter we create a SetMyProperties() method that simply
# executes a pass command (which does absolutely nothing).

class ClassOpenableItem(ServiceOpenable, ClassItem):

    def SetMyProperties(self):
        """Sets default instance properties"""
        pass


#================================================================================
#                                Class Shelf
#================================================================================

# Shelves are objects on which other objects can be placed. Objects on a shelf
# are automatically visible when the shelf is described.

class ClassShelf(ServiceContainOn,ClassScenery):
    def SetMyProperties(self):
        """Sets default instance properties"""
        pass
        

#================================================================================
#                                Class Container
#================================================================================

# Containers are objects into which other objects can be placed. Objects in a 
# container are NOT automatically visible when the container is described, only
# when it's looked into.

class ClassContainer(ServiceContainIn,ClassItem):

    def SetMyProperties(self):
        """Sets default instance properties"""
        pass



#*********************************************************************
#                        U N I V E R S E     V E R B S
#*********************************************************************

# All verbs are arranged alphabetically to make them easier to find,
# however major verb classes (ClassBasicVerb, ClassSystemVerb, etc)
# are arranged first, hierarchically.
#
# In addition, all verbs have two parts, the class and the Instance.
# The class defines the verb's replacement Action() method, the
# instance allows specific aspects of the general verb class to
# be changed (like the verb, preposition, and OkInDark property.


#=====================================================================
#                               Class Basic Verb
#=====================================================================

# This class extends PAWS ClassBaseVerbObject. It handles specific
# disambiguation for most verbs, although some verbs might override
# it.

class ClassBasicVerb(ClassBaseVerbObject):
    """Basic verb for Universe. All verbs descend from this class."""

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ExpectedPreposition = "inside"

    
    #--------------------------------
    # Default Specific Disambiguation
    #--------------------------------

    
    # This is where the rubber hits the road when it comes to figuring out
    # what objects are acceptable to a verb and which aren't. This default
    # method may be overridden or extended by different verbs.

    # Basically it performs the following checks:
    #
    # 1) Is the actor actually an actor?
    # 2) Is a given object allowed with the verb?
    # 3) Is it remembered (actor knows about it)?
    # 4) Is it visible?
    # 5) Is it reachable?
    #
    # If any of these checks fail for a specific object, that object is
    # discarded. If all ambiguous objects for a given noun are discarded
    # the ErrorMethod for those objects is said.
    #
    # Once the disambiguation is completed, any ambiguous objects still
    # remaining are merged into the non-ambiguous object list. For instance,
    # if the bone and brass keys are both present, visible, and reachable
    # and the player says "get key", then BOTH keys will be taken. If the
    # player wants to deal with a specific key they can type "get brass key"
    # instead of just "get key".


    def SpecificDisambiguate(self):
        """Default specific disambiguation for most verbs"""
        
        #----------------------
        # Create Actor Shortcut
        #----------------------

        # The actor is needed in several pieces of code, so we create a
        # shortcut.

        Actor = P.CA()

        
        #--------------------
        # Perform Actor Check
        #--------------------

        # If the object being addressed as an actor (the object the player
        # is telling to do something) isn't really an actor then return
        # a failure code, which aborts the command.

        if not Actor.CheckActor():
            return FAILURE

        
        #-----------------------------------------
        # Remove Unallowed Direct/Indirect Objects
        #-----------------------------------------

        # Notice how we placed the arguments on several lines? This is legal
        # because Python ignores whitespace between the parentheses of a
        # tuple. (A tuple is any group of comma seperated things between
        # parentheses).


        DebugTrace("Testing Allowed Objects")

        if not DisambiguateListOfLists(P.DOL(),
               ClassBasicThing.AllowedByVerbAsDObj,
               ClassBasicThing.NotWithVerbDesc):
            return FAILURE

        if not DisambiguateListOfLists(P.IOL(),
               ClassBasicThing.AllowedByVerbAsIObj,
               ClassBasicThing.NotWithVerbDesc):
            return FAILURE

        
        #-----------------------------------------
        # Remove Invisible Direct/Indirect Objects
        #-----------------------------------------

        DebugTrace("Testing Visible Objects")

        if not DisambiguateListOfLists(P.DOL(),
               ClassBasicThing.IsVisible,
               ClassBasicThing.CantSeeDesc,
               Actor):
            return FAILURE

        if not DisambiguateListOfLists(P.IOL(),
               ClassBasicThing.IsVisible,
               ClassBasicThing.CantSeeDesc,
               Actor):
           return FAILURE

        
        #-------------------------------------------
        # Remove Unreachable Direct/Indirect Objects
        #-------------------------------------------

        DebugTrace("Testing Reachable Objects")

        if not DisambiguateListOfLists(P.DOL(),
               ClassBasicThing.IsReachable,
               ClassBasicThing.CantReachDesc,
               Actor):
           return FAILURE

        if not DisambiguateListOfLists(P.IOL(),
                ClassBasicThing.IsReachable,
                ClassBasicThing.CantReachDesc,
                Actor):
           return FAILURE

        
        #---------------------------------------
        # Remove Unknown Direct/Indirect Objects
        #---------------------------------------

        DebugTrace("Testing Known Objects")

        if not DisambiguateListOfLists(P.DOL(),
                ClassBasicThing.Remembers,
                ClassBasicThing.AmnesiaDesc,
                Actor):
            return FAILURE

        if not DisambiguateListOfLists(P.IOL(),
               ClassBasicThing.Remembers,
               ClassBasicThing.AmnesiaDesc,
               Actor):
            return FAILURE

        
        #-------------------------------------
        # Gather Parser Favored Objects If Any
        #-------------------------------------

        DebugTrace("Testing Favored Objects")
        List = P.DOL()[:]

        if DisambiguateListOfLists(List,
               ClassBasicThing.Favored,
               ClassBasicThing.NoDesc):
           P.AP().CurrentDObjList = List[:]


        List = P.IOL()[:]

        if DisambiguateListOfLists(List,
                ClassBasicThing.Favored,
                ClassBasicThing.NoDesc):
           P.AP().CurrentIObjList = List[:]

        
        #----------------------------------
        # Merge remaining ambiguous objects
        #----------------------------------

        # If any objects are still ambiguous, give it up. Merge them into
        # the unambiguous list. Basically we create a list, using Union if
        # the list item is a list, or append if it's a single object. We
        # then copy our resulting list back to the original list.

        #---------------------
        # Merge Direct Objects
        #---------------------

        List = []
        for Object in P.DOL():
            if type(Object) == type([]):
                List = Union(List,Object)
            else:
                List.append(Object)

        Global.CurrentDObjList = List

        #-----------------------
        # Merge Indirect Objects
        #-----------------------

        List = []
        for Object in P.IOL():
            if type(Object) == type([]):
                List = Union(List,Object)
            else:
                List.append(Object)

        Global.CurrentIObjList = List

        
        #----------------------------
        # Check for ONE direct object
        #----------------------------

        # If the verb allows one direct object, and either no direct direct objects were
        # used or more than 1 direct object is left we complain and return failure. This
        # insures the Execute() method won't call the verb's action.

        if len(P.DOL()) > 1 and (self.ObjectAllowance & ALLOW_ONE_DOBJ > 0):
            return Complain(P.AP().OnlyOneDObj)
            
        
        #------------------------------
        # Check for ONE indirect object
        #------------------------------

        # If the verb allows one direct object, and either no direct direct objects were
        # used we complain and return failure. This insures the Execute()
        # method won't call the verb's action.

        if len(P.IOL()) > 1 and (self.ObjectAllowance & ALLOW_ONE_IOBJ > 0):
            return Complain(P.AP().OnlyOneIObj)
        
        #----------------------------
        # Check for NO direct object
        #----------------------------

        # If no direct objects are left but one or more was expected, say
        # a complaint (Dig what? Take what?) and return FAILURE.

        if len(P.DOL())==0 and not \
           (self.ObjectAllowance & ALLOW_OPTIONAL_DOBJS):
            if not (self.ObjectAllowance & ALLOW_NO_DOBJS):
                if len(P.AP().CurrentPrepList) == 0:
                    return Complain(SCase("what would you like to " + P.CVN() + "?"))
                else:
                    return Complain(SCase("what would you like to " +P.CVN() + " " + \
                                          string.join(P.AP().CurrentPrepList) + "?"))

        
        #-----------------------------
        # Check for NO indirect object
        #-----------------------------

        # If no indirect objects are left but one or more was expected, say
        # a complaint (Dig what? Take what?) and return FAILURE.

        if len(P.IOL()) == 0:
            if not (self.ObjectAllowance & ALLOW_NO_IOBJS):
                return Complain(SCase(P.CVN() + " " + \
                                      P.DOL()[0].NamePhrase + " " + \
                                      string.join(P.AP().CurrentPrepList) + \
                                      " what?"))

        
        #-----------------
        # Congratulations!
        #-----------------

        # If you got this far you've got a disambiguated list of direct and
        # indirect objects and can now perform a sanity check.

        return SUCCESS


    
    #-------------
    # Sanity Check
    #-------------

    # By default the sanity check is simply if the verb can be performed in
    # the dark, or if the current actor's location has light. Otherwise we
    # complain and return FALSE.

    def SanityCheck(self):
        """Return Success if room is lit OR verb is OK in dark"""

        
        #--------------------
        # Twilight Zone Check
        #--------------------

        # If, for whatever reason the current actor is in the twilight
        # zone (Location == None) return SUCCESS, since the twilight
        # zone should have light.
        #
        # P.S. Don't ask. This test is from the very early development
        # days and handles truly bizarre coding by the game author...

        if P.CA() == None: return SUCCESS
        if P.CA().Where() == None: return SUCCESS
 
        
        #----------------
        # Check for light
        #----------------

        LightHere = P.CA().Where().CurrentlyIlluminated()

        if LightHere or self.OkInDark:
            return SUCCESS
        else:
            return Complain(P.AP().TooDark)




#======================================================================
#                               Class System Verb
#======================================================================

# System verbs are just basic verbs that are OK to use in the dark. We
# set up a special class simply to save us the effort of setting each
# and every system verb's OkInDark property to true.

class ClassSystemVerb(ClassBasicVerb):
    """Class used to create verbs for system commands."""

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.OkInDark = TRUE
        self.ObjectAllowance = ALLOW_NO_DOBJS + ALLOW_NO_IOBJS


#=====================================================================
#                               Class Travel Verb
#=====================================================================

# Travel verbs are: up, down, north, etc. This verb's action basically
# finds the room or string in the current actor's location map and
# either enters the room or (if a string) says it and returns FAILURE.

class ClassTravelVerb(ClassBasicVerb):

    
    #---------------
    # Set Properties
    #---------------

    # We add a new property, TravelDirection, and reset the ObjectAllowmance
    # so that travel verbs can't have either direct or indirect objects.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.TravelDirection = None
        self.ObjectAllowance = ALLOW_NO_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    
    #-------
    # Action
    #-------

    def Action(self):

        if P.CA().Where() == None: return TURN_ENDS
        return P.CA().Travel(self.TravelDirection)
        


#----------------------
# Travel Verb Instances
#----------------------

# These are the actual verbs that the parser will use when the player
# types the one word travel commands (north, down, etc).

NorthVerb = ClassTravelVerb("north,n")
NorthVerb.TravelDirection = North

NortheastVerb = ClassTravelVerb("northeast,ne")
NortheastVerb.TravelDirection = Northeast

EastVerb = ClassTravelVerb("east,e")
EastVerb.TravelDirection = East

SoutheastVerb = ClassTravelVerb("southeast,se")
SoutheastVerb.TravelDirection = Southeast

SouthVerb = ClassTravelVerb("south,s")
SouthVerb.TravelDirection = South

SouthwestVerb = ClassTravelVerb("southwest,sw")
SouthwestVerb.TravelDirection = Southwest

WestVerb = ClassTravelVerb("west,w")
WestVerb.TravelDirection = West

NorthwestVerb = ClassTravelVerb("northwest,nw")
NorthwestVerb.TravelDirection = Northwest

UpVerb = ClassTravelVerb("up,u,ascend")
UpVerb.TravelDirection = Up

DownVerb = ClassTravelVerb("down,d,descend")
DownVerb.TravelDirection = Down

UpstreamVerb = ClassTravelVerb("upstream,us")
UpstreamVerb.TravelDirection = Upstream

DownstreamVerb = ClassTravelVerb("downstream,ds")
DownstreamVerb.TravelDirection = Downstream

InVerb = ClassTravelVerb("in,enter,ingress")
InVerb.TravelDirection = In

OutVerb = ClassTravelVerb("out,outside,exit")
OutVerb.TravelDirection = Out



#=====================================================================
#                          Activate Verb
#=====================================================================

# This verb allows the player to activate an object (usually a light
# source). The way we define LightWithVerb below is interesting,
# notice the change to ObjectAllowance. LightWithVerb otherwise uses
# the standard ClassActivateVerb.

class ClassActivateVerb(ClassBasicVerb):
    """Defines a verb to light a lightsource."""

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE   # most definitely!

    
    def Action(self):
        Multiple = len(P.DOL()) > 1

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            if hasattr(Object, self.ActivationProperty): Object.Activate(Multiple)

        return TURN_CONTINUES


LightVerb = ClassActivateVerb("light,activate")
LightVerb.ActivationProperty = "IsLit"

TurnOnVerb = ClassActivateVerb("turn","on")
TurnOnVerb.ActivationProperty = "IsActivated"

LightWithVerb = ClassActivateVerb("light","with")
LightWithVerb.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_ONE_IOBJ
LightWithVerb.ActivationProperty = "IsLit"


#======================================================================
#                               Again Verb
#======================================================================

# This verb quits the game and returns to the operating system.

AgainVerb = ClassSystemVerb("g,again")
P.AP().Again = AgainVerb



#=====================================================================~~KR
#                               Close Verb
#=====================================================================

class ClassCloseVerb (ClassBasicVerb):
    """Defines a verb to close an object."""

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    
    def Action(self):

        Multiple = (len(P.DOL()) > 1)

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()

            if not hasattr(Object, "Close"):
                return Complain("I don't know how to close %s." % Object.ADesc())

            Object.Close(Multiple)

        return TURN_CONTINUES


CloseVerb = ClassCloseVerb("close,shut")



#===========================================================================
#                         Configure Terminal Verb
#===========================================================================

# This verb configures the terminal colors, including .

class ClassConfigureTerminalVerb(ClassSystemVerb):
    """Configure Terminal verb"""
    #-----------------
    # Quit Verb Action
    #-----------------

    # This replaces the default action

    def Action(self):
        """Action performed for Configure Terminal"""

        #------------------------------
        # Change Game State To Finished
        #------------------------------

        # If you examine the game loop code you notice the WHILE loop runs
        # until the game's state changes to FINISHED. This is the code that
        # changes the game state to finished.

        Terminal.Configure()

        #---------------
        # Return TURN_CONTINUES
        #---------------

        return TURN_CONTINUES


ConfigureTerminalVerb = ClassConfigureTerminalVerb("configure","terminal")



#=====================================================================
#                             Deactivate Verb
#=====================================================================

# This verb allows the player to deactivate an object (usually a light
# source). Note how we create Extinguish with by merely changing the
# verb's ObjectAllowance property.

class ClassDeactivateVerb (ClassBasicVerb):
    """Defines a verb to deactivate an object."""

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE   # inconceivable, but might as well allow it
    
    def Action(self):

        Multiple = len(P.DOL()) > 1

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            if hasattr(Object, "Extinguish"): Object.Deactivate(Multiple)

        return TURN_CONTINUES


ExtinguishVerb = ClassDeactivateVerb("deactivate,extinguish,douse")
PutOutVerb = ClassDeactivateVerb("put","out")
TurnOffVerb = ClassDeactivateVerb("turn","off")

ExtinguishWithVerb = ClassDeactivateVerb("extinguish,douse","with")
ExtinguishWithVerb.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_ONE_IOBJ


class ClassDebugVerb(ClassSystemVerb):
    
    #--------------
    # Debug Action
    #--------------

    # Toggle the debug variable True/False

    def Action(self):
        """Say action"""

        if Global.Production:
            return Complain("Debug is only active in TEST versions of this game.")
        else:
            Say("Debug verb is active")

        Global.Debug = not Global.Debug

        if Global.Debug:
            Say("Debug is ON")
        else:
            Say("Debug is OFF")

        return TURN_CONTINUES


DebugVerb = ClassDebugVerb("debug")

#===========================================================================
#                               Drop Verb
#===========================================================================

# This verb allows actors to drop things they're carrying. Notice how this
# verb has synonyms, "drop/release" or "set down/throw down". To do this
# we instantiated a second verb with the ClassDropVerb class to handle
# the "down" preposition.

class ClassDropVerb(ClassBasicVerb):
    """Defines verb to drop an object."""
    
    #---------------
    # Set Properties
    #---------------

    # Notice drop (and take!) allow one or more direct objects, but do NOT
    # allow ANY indirect ones.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    
    #------------
    # Drop Action
    #------------

    # This action does a great deal without appearing to. Let's examine
    # the coding tricks used.

    def Action(self):
        """Drop action"""

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        
        # If the player drops a rock the computer will say "Dropped". But
        # if the player drops a rock and a coin the computer will say:
        #
        # Rock: Dropped.
        # Coin: Dropped.
        #
        # The secret lies in the Multiple argument passed to the object's
        # Drop method. We use an "implied if" coding trick to make the code
        # 1 line instead of 5!
        #
        # If you examine the expression you see it's the same one you'd
        # put on an if test. The expression evaluates to 1 or 0, in other
        # words, TRUE or FALSE

        Multiple = (len(P.DOL()) > 1)

        #----------------------------------
        # For each direct object in command
        #----------------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            if hasattr(Object,"Drop"): Object.Drop(Multiple)

        return TURN_CONTINUES

    
    #--------------------
    # Sanity Check Method
    #--------------------
    
    def SanityCheck(self):
        """Sanity declares drop all would be actor's contents"""    

        #------------------------
        # Reassign "Them" Pronoun
        #------------------------
    
        # Normally "Them" refers to the ROOM'S contents. However, if you're dropping
        # something then "Them" (aka "all" or "everything") should refer to the
        # CURRENT ACTOR'S contents.

        P.AP().PronounsDict[THEM] = P.CA().Contents

        #-------------------------------
        # Call The "normal" Sanity Check
        #-------------------------------
    
        # The normal check for sanity is found in ClassBasicVerb, so return the
        # result of that sanity check. This insures that sanity runs in the 
        # family... :)

        return ClassBasicVerb.SanityCheck(self)
    


DropVerb = ClassDropVerb("drop,release")
DropDownVerb = ClassDropVerb("put,set,throw","down")



#=====================================================================
#                               Feel Verb
#=====================================================================

# This verb allows actors to feel things or their location if they don't
# supply a direct object.

class ClassFeelVerb(ClassBasicVerb):
    """Defines verb for feeling objects and environment"""
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS

    
    #------------
    # Feel Action
    #------------

    # This allows the player to type "feel" or "feel rock".

    def Action(self):

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0:
            P.CA().Where().DescribeSelf("FEEL")
            return TURN_ENDS

        #----------------------------
        # One or more direct objects?
        #----------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("FEEL")

        return TURN_ENDS


FeelVerb = ClassFeelVerb("feel,touch")
FeelAroundVerb = ClassFeelVerb("feel","around")



#=====================================================================
#                               Go Verb
#=====================================================================

# This verb allows actors to taste things. If they don't supply a
# direct object it will complain.

class ClassGoVerb(ClassBasicVerb):
    """Creates verb for go/walk/run/climb command."""
    
    #---------------
    # Set Properties
    #---------------

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    
    #----------
    # Go Action
    #----------

    # This verb can respond appropriately to "go" or "go east west" or
    # "go east" (complaining in the first two instances).

    def Action(self):
        """Go action"""

        #----------------------------------
        # No direction/multiple directions?
        #----------------------------------

        if len(P.DOL()) == 0: return Complain("Which way?")
        if len(P.DOL()) > 1:  return Complain("Make up your mind!")

        #--------------------
        # Travel in direction
        #--------------------

        return P.CA().Travel(Global.CurrentDObjList[0])


GoVerb = ClassGoVerb("go,walk,run,move")
GoToVerb = ClassGoVerb("go,walk,run,move","to")
GoTowardVerb = ClassGoVerb("go,walk,run,move","toward")
ClimbVerb = ClassGoVerb("climb")



#====================================================================
#                               Hello Verb
#====================================================================

class ClassHelloVerb(ClassBasicVerb):
    """Creates verb to handle Hello."""
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS + ALLOW_OPTIONAL_DOBJS
        self.OkInDark = TRUE
    
    def Action(self):
        """Hello Action"""

        if len(P.DOL()) == 0:
            if P.CA() == Global.Player:
                return Complain("Taking to yourself?")
            else:
                Say(P.CA().HelloDesc())
                return TURN_ENDS

        #----------------------------
        # One or more direct objects?
        #----------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("HELLO")

        return TURN_ENDS


HelloVerb = ClassHelloVerb("hello,hi")
HelloThereVerb = ClassHelloVerb("hello,hi","there")

AskAboutVerb = ClassHelloVerb("ask","about")
SpeakVerb = ClassHelloVerb("speak","to")
TalkVerb = ClassHelloVerb("talk","to")


#=====================================================================
#                        Insert Verb
#=====================================================================

class ClassInsertVerb (ClassBasicVerb):
    """Defines a verb to put an object into a container."""

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_ONE_IOBJ
        self.OkInDark = TRUE
        self.ExpectedPreposition = "inside"
    
    def Action(self):
        Multiple = len(P.DOL()) > 1
        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.Insert(P.IOL()[0],Multiple)

        return TURN_CONTINUES



PutInVerb = ClassInsertVerb("put,place,insert,set","in,into,inside")
PutOntoVerb = ClassInsertVerb("put,place,pile,stack,set","on,onto")
HangOnVerb = ClassInsertVerb("hang","on")
PutBehindVerb = ClassInsertVerb("put,place,hide,set", "behind")
PutUnderVerb = ClassInsertVerb("put,place,hide,set","under,underneath,beneath")

PutOntoVerb.ExpectedPreposition = "on"
HangOnVerb.ExpectedPreposition = "on"
PutBehindVerb.ExpectedPreposition = "behind"
PutUnderVerb.ExpectedPreposition = "under"


#=====================================================================
#                               Inventory Verb
#=====================================================================

# This verb allows actors to take inventory.

class ClassInventoryVerb(ClassBasicVerb):

    
    #---------------
    # Set Properties
    #---------------

    # Notice drop (and take!) allow one or more direct objects, but do NOT
    # allow ANY indirect ones.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_NO_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    
    #-----------------
    # Inventory Action
    #-----------------

    # This action does a great deal without appearing to. Let's examine
    # the coding tricks used.

    def Action(self):
        """Take inventory"""
        P.CA().DescribeSelf("CONTENT")
        return TURN_CONTINUES


InventoryVerb = ClassInventoryVerb("inventory,inven,i")
TakeInventoryVerb = ClassInventoryVerb("take","inventory")
TakeStockVerb = ClassInventoryVerb("take","stock")


#===========================================================================
#                               Listen Verb
#===========================================================================

# This verb allows actors to listen to their location. A different verb
# (ListenToVerb) is used to listen to objects.

class ClassListenVerb(ClassBasicVerb):

    
    #---------------
    # Set Properties
    #---------------

    # Notice drop (and take!) allow one or more direct objects, but do NOT
    # allow ANY indirect ones.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_NO_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    
    #--------------
    # Listen Action
    #--------------

    # This action does a great deal without appearing to. Let's examine
    # the coding tricks used.

    def Action(self):
        """Listen (to location) action"""

        P.CA().Where().DescribeSelf("SOUND")
        return TURN_ENDS


ListenVerb = ClassListenVerb("listen")

#=====================================================================
#                               ListenTo Verb
#=====================================================================

# This verb allows actors to listen to things (but NOT their location, see
# ListenVerb above).

class ClassListenToVerb(ClassBasicVerb):
    """Verb to handle Listen To Rock"""
    
    #---------------
    # Set Properties
    #---------------

    # Notice drop (and take!) allow one or more direct objects, but do NOT
    # allow ANY indirect ones.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

        #-------------------
    # Listen TO Objects?
    #-------------------

    # This action does a great deal without appearing to. Let's examine
    # the coding tricks used.

    def Action(self):
        """Listen To action"""

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0: return Complain("Listen to what?")

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("SOUND")

        return TURN_ENDS


ListenToVerb = ClassListenToVerb("listen","to")


#=====================================================================~~KR
#                               Lock Verb
#=====================================================================

class ClassLockVerb(ClassBasicVerb):
    """Defines a verb to lock an object (that doesn't require a key."""

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_ONE_DOBJ + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    
    def Action(self):
        DirectObject = P.DOL()[0]
        DirectObject.MakeCurrent()
        Object.MarkPronoun()

        if not hasattr(DirectObject, "Lock"):
            return Complain("I don't know how to lock " + DirectObject.ADesc())

        return DirectObject.Lock(None)



LockVerb = ClassLockVerb("lock,latch,hook")


#=====================================================================~~KR
#                               Lock With Verb
#=====================================================================

class ClassLockWithVerb(ClassBasicVerb):
    """Defines a verb to lock an object (that requires a key)."""

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_ONE_DOBJ + ALLOW_ONE_IOBJ
        self.OkInDark = TRUE

    
    def Action(self):
        DirectObject = P.DOL()[0]
        IndirectObject = P.IOL()[0]
        DirectObject.MakeCurrent()
        Object.MarkPronoun()

        if not hasattr(DirectObject, "Lock"):
            return Complain("I don't know how to lock " + DirectObject.ADesc())

        return DirectObject.Lock(IndirectObject)



LockWithVerb = ClassLockWithVerb("lock","with")


#=====================================================================
#                               Look Verb
#=====================================================================

# This verb allows actors to look at their location. A different verb
# (LookAtVerb) is used to listen to objects.

class ClassLookVerb(ClassBasicVerb):
    """Handles Look command"""
    
    #---------------
    # Set Properties
    #---------------

    # Notice drop (and take!) allow one or more direct objects, but do NOT
    # allow ANY indirect ones.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_NO_DOBJS + ALLOW_NO_IOBJS

    
    #------------
    # Look Action
    #------------

    # This action does a great deal without appearing to. Let's examine
    # the coding tricks used.

    def Action(self):
        """Look (at location) action"""
        
        #--------------------------
        # Force Temporary Verbosity
        #--------------------------

        # The look command says the FULL room description, regardless of
        # the current verbosity (or visited status) of the room. However, we
        # can't simply turn on the verbosity flag, that might contradict
        # the player's desire (always rude!)
        #
        # So we save the old verbosity setting before turning verbosity on.

        OldVerbosity = Global.Verbose
        Global.Verbose = TRUE

        
        #----------------------
        # Call Room Description
        #----------------------

        # The SmartDescribeSelf method for a room describes the room
        # completely, it's the method called by Enter().

        P.CA().Where().SmartDescribeSelf()
        
        #----------------------
        # Restore Old Verbosity
        #----------------------

        # Now that we are done it's time to put away our toys. We restore
        # the global verbosity flag to the value it was before we turned
        # it on.
        #
        # This brings up an important point. If you plan to change a global
        # setting (like Global.Verbose) it's a good idea to save the orignal
        # setting so you can restore it when you're finished. This is
        # espcially important if your change is temporary.

        Global.Verbose = OldVerbosity

        return TURN_ENDS



LookVerb = ClassLookVerb("look,gaze,l")
LookAroundVerb = ClassLookVerb("look,l","around")


#=====================================================================
#                               LookAt Verb
#=====================================================================

# This verb allows actors to look at things (but NOT their location, see
# LookVerb above).

class ClassLookAtVerb(ClassBasicVerb):

    
    #---------------
    # Set Properties
    #---------------

    # Notice drop (and take!) allow one or more direct objects, but do NOT
    # allow ANY indirect ones.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS

        #---------------
    # Look At Action
    #---------------

    # This action does a great deal without appearing to. Let's examine
    # the coding tricks used.

    def Action(self):
        """Look At action"""

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0: return Complain("Look at what?")

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("LONG")

        return TURN_ENDS


LookAtVerb = ClassLookAtVerb("look,l","at")
ExamineVerb = ClassLookAtVerb("examine,inspect,x")

#=====================================================================
#                        Look Deep Verb
#=====================================================================

class ClassLookDeepVerb(ClassBasicVerb):

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_ONE_DOBJ + ALLOW_NO_IOBJS
        self.OkInDark = FALSE
        self.ExpectedPreposition = "inside"

    
    def Action(self):
        Multiple = len(P.DOL()) > 1

        #-----------------------
        # For Each Direct Object
        #-----------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.LookDeep()

        return TURN_ENDS


LookUnderVerb = ClassLookDeepVerb("look,search","under,underneath,beneath")
LookInsideVerb = ClassLookDeepVerb("look,search","in,inside,into")
LookBehindVerb = ClassLookDeepVerb("look,search","behind")
LookOnVerb = ClassLookDeepVerb("look,search","on")

LookUnderVerb.ExpectedPreposition = "under"
LookBehindVerb.ExpectedPreposition = "behind"
LookOnVerb.ExpectedPreposition = "on"



#===========================================================================
#                               Quit Verb
#===========================================================================

# This verb quits the game and returns to the operating system.

class ClassQuitVerb(ClassSystemVerb):
    """Quit verb"""
        #-----------------
    # Quit Verb Action
    #-----------------

    # This replaces the default action

    def Action(self):
        """Action performed for Quit"""

        #------------------------------
        # Change Game State To Finished
        #------------------------------

        # If you examine the game loop code you notice the WHILE loop runs
        # until the game's state changes to FINISHED. This is the code that
        # changes the game state to finished.

        Global.GameState = FINISHED

        #---------------
        # Return FAILURE
        #---------------

        
        # Why failure? Why not success?
        #
        # Remember, the Action method returns whatever you want TurnHandler
        # to return. If the TurnHandler fails, the AfterTurnHandler won't
        # run.
        #
        # If we're quitting the game we want to quit RIGHT NOW, we don't want
        # any additional turn handling to occur. This is true of any game
        # controlling verb (quit, save, restore, etc).


        return TURN_CONTINUES


QuitVerb = ClassQuitVerb("quit")



#=====================================================================~~KR
#                               Open Verb
#=====================================================================

class ClassOpenVerb (ClassBasicVerb):
    """Defines a verb to open an object."""

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    
    def Action(self):

        Multiple = (len(P.DOL()) > 1)

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()

            if not hasattr(Object, "Open"):
                return Complain("I don't know how to open " + Object.ADesc())

            Object.Open(Multiple)

        return TURN_CONTINUES


OpenVerb = ClassOpenVerb("open")



#===========================================================================
#                                   Read Verb
#===========================================================================

# This verb allows actors to read things. If they don't supply a direct
# object it will complain.

class ClassReadVerb(ClassBasicVerb):

    
    #---------------
    # Set Properties
    #---------------

    # Notice drop (and take!) allow one or more direct objects, but do NOT
    # allow ANY indirect ones.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS

    
    #------------
    # Read Action
    #------------

    # This action does a great deal without appearing to. Let's examine
    # the coding tricks used.

    def Action(self):
        """Read action"""

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0: return Complain("Read what?")

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("READ")

        return TURN_ENDS


ReadVerb = ClassReadVerb("read")


#===========================================================================
#                               Restore Verb
#===========================================================================

# This verb restores the game and returns to the operating system.

class ClassRestoreVerb(ClassSystemVerb):
    """Restore verb"""
    
    #--------------------
    # Restore Verb Action
    #--------------------

    # This replaces the default action

    def Action(self):
        """Action performed for Restore"""

        #---------------
        # Restore Global
        #---------------
        
        # Toggle the transcribe property (which controls logging). If it was 
        # saved as TRUE set it to FALSE, if it was FALSE set it to TRUE. Then call
        # the Transcribe verb action, just as if the player had typed TRANSCRIBE.
        # That will *re*-toggle the transcription. The end result will be if the 
        # game was saved with logging turned on, logging will be turned on, and
        # if the game was saved with logging turned off, then logging will be
        # turned off.

        if Engine.RestoreFunction(Global.GameModule):
            Global.Transcribe = not Global.Transcribe
            TranscribeVerb.Action()
            Say("Restored")
                                        
        #---------------
        # Return FAILURE
        #---------------

        return TURN_CONTINUES


RestoreVerb = ClassRestoreVerb("restore")



#===========================================================================
#                               Save Verb
#===========================================================================

# This verb saves the game and returns to the operating system.

class ClassSaveVerb(ClassSystemVerb):
    """Save verb"""
    
    #-----------------
    # Save Verb Action
    #-----------------

    # This replaces the default action

    def Action(self):
        """Action performed for Save"""

        if Engine.SaveFunction(Global.GameModule):
            Say("Saved")

        #---------------
        # Return FAILURE
        #---------------

        return TURN_CONTINUES


SaveVerb = ClassSaveVerb("save")


class ClassSayVerb(ClassBasicVerb):

    
    #---------------
    # Set Properties
    #---------------

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS + ALLOW_OPTIONAL_DOBJS
        self.OkInDark = TRUE

    
    #-----------
    # Say Action
    #-----------

    # This function will translate { and } into [ and ] respectively
    # when debug is turned off. This prevents players from cheating.
    # The Debug verb is disabled when Global.Production is true.

    def Action(self):
        """Say action"""

        if not Global.Debug:
            P.AP().SaidText = string.replace(P.AP().SaidText,"{","[")
            P.AP().SaidText = string.replace(P.AP().SaidText,"}","]")

        Say(P.AP().SaidText)
        return TURN_CONTINUES


SayVerb = ClassSayVerb("say")

#===========================================================================
#                               Score Verb
#===========================================================================

# This verb returns the player's score.

class ClassScoreVerb(ClassSystemVerb):
    """Scoring verb"""
    
    #------------------
    # Score Verb Action
    #------------------

    # This is a simple minded scoring routine that simply prints the current
    # score. You can override this verb in your game library.


    def Action(self):
        """Action performed for Score"""

        #------------------------
        # Display Score To Player
        #------------------------

        # Notice we use the str() function to convert the numeric score into a
        # string that the % function can handle properly.

        Say("Your score is %s points out of a possible %s." % \
           (str(Global.CurrentScore),str(Global.MaxScore)))

        #---------------
        # Return FAILURE
        #---------------

        
        # Why failure? Why not success?
        #
        # Remember, the Action method returns whatever you want TurnHandler
        # to return. If the TurnHandler fails, the AfterTurnHandler won't
        # run.
        #
        # If we're quitting the game we want to quit RIGHT NOW, we don't want
        # any additional turn handling to occur. This is true of any game
        # controlling verb (quit, save, restore, etc).


        return TURN_CONTINUES


ScoreVerb = ClassScoreVerb("score")


#===========================================================================
#                               Smell Verb
#===========================================================================

# This verb allows actors to sniff things or their location if they don't
# supply a direct object.

class ClassSmellVerb(ClassBasicVerb):

    
    #---------------
    # Set Properties
    #---------------

    # Notice drop (and take!) allow one or more direct objects, but do NOT
    # allow ANY indirect ones.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS + ALLOW_OPTIONAL_DOBJS
        self.OkInDark = TRUE

    
    #--------------
    # Sniff Action
    #--------------

    # This action does a great deal without appearing to. Let's examine
    # the coding tricks used.

    def Action(self):
        """Smell/Sniff action"""

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0:
            P.CA().Where().DescribeSelf("ODOR")
            return TURN_ENDS

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("ODOR")

        return TURN_CONTINUES


SmellVerb = ClassSmellVerb("smell,sniff")


#===========================================================================
#                               Take Verb
#===========================================================================

# This verb allows actors to take things they find. Notice how this verb has synonyms, "take"
# or "pick up". To do this we instantiated a second verb with the ClassDropVerb class to handle
# the "up" preposition.

class ClassTakeVerb(ClassDropVerb):
    """Handles Take/Pick Up command."""
    
    #------------
    # Take Action
    #------------

    # This action does a great deal without appearing to. Let's examine
    # the coding tricks used.

    def Action(self):
        """Take action"""

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        
        # If the player drops a rock the computer will say "Taken". But
        # if the player drops a rock and a coin the computer will say:
        #
        # Rock: Taken.
        # Coin: Taken.
        #
        # The secret lies in the Multiple argument passed to the object's
        # Take method. We use an "implied if" coding trick to make the code
        # 1 line instead of 5!
        #
        # If you examine the expression you see it's the same one you'd
        # put on an if test. The expression evaluates to 1 or 0, in other
        # words, TRUE or FALSE

        Multiple = (len(P.DOL()) > 1)

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            if hasattr(Object,"Take"): Object.Take(Multiple)

        return TURN_CONTINUES


TakeVerb = ClassTakeVerb("take,get,remove,steal")
PickUpVerb = ClassTakeVerb("pick","up")


#=====================================================================
#                               Taste Verb
#=====================================================================

# This verb allows actors to taste things. If they don't supply a
# direct object it will complain.

class ClassTasteVerb(ClassBasicVerb):

    
    #---------------
    # Set Properties
    #---------------

    # Notice drop (and take!) allow one or more direct objects, but do NOT
    # allow ANY indirect ones.

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS

    
    #-------------
    # Taste Action
    #-------------

    # This action does a great deal without appearing to. Let's examine
    # the coding tricks used.

    def Action(self):
        """Taste action"""

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0: return Complain("Taste what?")

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("TASTE")

        return TURN_CONTINUES


TasteVerb = ClassTasteVerb("taste,lick")


#======================================================================~atholbrose
#                                   Terse Verb
#=================================================================================
                
class ClassTerseVerb(ClassSystemVerb):
    """Sets game to play in terse (default) mode."""

    def Action(self):
        Global.Verbose = FALSE
        Say("Show Brief descriptions on return visits.")
        return TURN_CONTINUES

TerseVerb = ClassTerseVerb("terse,brief")


class ClassTranscribeVerb(ClassSystemVerb):
    
    #--------------
    # Debug Action
    #--------------

    # Toggle the debug variable True/False

    def Action(self):
        """Transcribe action"""

        Global.Transcribe = not Global.Transcribe

        if Global.Transcribe:
            Global.LogFile = open(Global.GameModule+".log","a")
            Global.DebugFile = open(Global.GameModule+".dbg","a")
            Say("""
                Logging turned ON. Transcripts appear in %s.log and debugging 
                information appears in %s.dbg.
                """ % (Global.GameModule, Global.GameModule))
        else:
            try:
                Global.DebugFile.close()
                Global.LogFile.close()
            except:
                pass
            Say("Logging turned OFF")

        return TURN_CONTINUES


TranscribeVerb = ClassTranscribeVerb("transcribe")


#=====================================================================~~KR
#                            Unlock Verb
#=====================================================================

class ClassUnlockVerb(ClassBasicVerb):
    """Defines a verb to unlock an object."""

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_ONE_DOBJ + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    
    def Action(self):
        DirectObject = P.DOL()[0]
        IndirectObject = P.IOL()[0]

        DirectObject.MakeCurrent()
        Object.MarkPronoun()

        if not hasattr(DirectObject, "Unlock"):
            return Complain("I don't know how to unlock " + DirectObject.ADesc())

        return DirectObject.Unlock(IndirectObject)


UnlockVerb = ClassUnlockVerb("unlock,unhook,unlatch")


#=====================================================================~~KR
#                            Unlock With Verb
#=====================================================================

class ClassUnlockWithVerb(ClassBasicVerb):
    """Defines a verb to unlock an object."""

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_ONE_DOBJ + ALLOW_ONE_IOBJ
        self.OkInDark = TRUE
        
    
    def Action(self):
        DirectObject = P.DOL()[0]
        IndirectObject = P.IOL()[0]

        DirectObject.MakeCurrent()
        Object.MarkPronoun()

        if not hasattr(DirectObject, "Unlock"):
            return Complain("I don't know how to unlock " + DirectObject.ADesc())

        return DirectObject.Unlock(IndirectObject)


UnlockWithVerb = ClassUnlockWithVerb("unlock","with")



#======================================================================~atholbrose
#                                Verbose Verb
#=================================================================================

# This verb turns on maximum verbosity, it insures that the room's long
# description will be said every time, not just the first time in the room.

class ClassVerboseVerb(ClassSystemVerb):
    """Sets game to play in verbose mode."""

    def Action(self):
        Global.Verbose = TRUE
        Say("Show full descriptions on return visits. ~n")
        P.CA().Where().SmartDescribeSelf()
        return TURN_CONTINUES

VerboseVerb = ClassVerboseVerb("verbose")



#*********************************************************************
#                     U N I V E R S E     O B J E C T S
#*********************************************************************


#===========================================================================
#                                    The Ground
#===========================================================================

# Whenever the player says something like "examine floor" or "examine ground"
# this object will use the current actor's location's GroundDesc() property
# instead. If Take or Taste is used then these descriptions are used, otherwise
# the default descriptions assigned to BasicThing are used.
#
# Note if you want a special Ground object for certain rooms you can set the
# HasGround property to FALSE, then create (another) ground object (maybe
# MyGround or something) with a new Landmark property set to TRUE. That way
# you can implement all the sensory methods for your MyGround object.

Ground = ClassLandmark("ground,floor")
Ground.Landmark = "Ground"

Ground.SetDesc("L","{P.CA().Where().GroundDesc()}")
Ground.SetDesc("Take","You must be joking.")
Ground.SetDesc("Taste","No!")


#===========================================================================
#                                    No Wall
#===========================================================================

# Whenever the player says something like "examine wall" this object will use
# the current actor's location's WallDesc() property instead.
#
# Note if you want a special Wall object for certain rooms you can set the
# HasWall property to FALSE, then create (another) Wall object (maybe
# MyWall or something) with a new Landmark property set to TRUE. That way
# you can implement all the sensory methods for your MySky object.

NoWall = ClassLandmarkMissing("wall")
NoWall.Landmark = "Wall"
NoWall.NamePhrase = "Non-Existent Wall"

NoWall.SetDesc("L","There's no wall here.")
NoWall.SetDesc("Take","You can't take what doesn't exist.")
NoWall.SetDesc("Taste","How exactly do you taste something that doesn't exist?")
NoWall.SetDesc("Sound","The (non-existent) wall makes no (non-existant) noise.")
NoWall.SetDesc("Odor","The (non-existent) wall has no odor. Hardly surprizing, hmm?")

#=============================================================================
#                                Space Time
#=============================================================================

# Because of the way the code works Rooms have to be "somewhere", ie all rooms
# have to be contained in something. That something is SpaceTime, an otherwise
# unused object that is never referred to by the game to the player, and can't
# be referred to by the player. Notice that we DELIBERATELY used propercase
# in defining SpaceTime's noun? That means the parser will always ignore it,
# the parser is looking only for things in lower case.

SpaceTime = ClassBasicThing("SpaceTime")
SpaceTime.IsLit = TRUE


#===========================================================================
#                                    The Sky
#===========================================================================

# Whenever the player says something like "examine sky" or "examine ceiling"
# this object will use the current actor's location's SkyDesc() property
# instead.
#
# Note if you want a special Sky object for certain rooms you can set the
# HasSky property to FALSE, then create (another) sky object (maybe
# MySky or something) with a new Landmark property set to TRUE. That way
# you can implement all the sensory methods for your MySky object.

Sky = ClassLandmark("sky,ceiling,air","thin")
Sky.Landmark = "Sky"

Sky.SetDesc("L","{P.CA().Where().SkyDesc()}")
Sky.SetDesc("Take","You must be joking.")
Sky.SetDesc("Taste","Very poetic, but extremely impractical.")
Sky.SetDesc("Sound","{P.CA().Where().SoundDesc()}")
Sky.SetDesc("Odor","{P.CA().Where().OdorDesc()}")


#===========================================================================
#                                    Wall
#===========================================================================

# Whenever the player says something like "examine wall" this object will use
# the current actor's location's WallDesc() property instead.
#
# Note if you want a special Wall object for certain rooms you can set the
# HasWall property to FALSE, then create (another) Wall object (maybe
# MyWall or something) with a new Landmark property set to TRUE. That way
# you can implement all the sensory methods for your MySky object.

Wall = ClassLandmark("wall")
Wall.Landmark = "Wall"

Wall.SetDesc("L","{P.CA().Where().WallDesc()}")
Wall.SetDesc("Take","You must be joking.")
Wall.SetDesc("Taste","No!")
Wall.SetDesc("Sound","The wall is silent.")
Wall.SetDesc("Odor","The wall has no particular smell.")



#*********************************************************************
#                          End of PAWS Module
#*********************************************************************
