# monstrosity
A turn-based dungeon crawler written in Python and Pygame

    Created By:  Darron Vanaria
    Email:  dvanaria@gmail.com
    Game Website:  monstrosity.fireheadfred.com

    Programming Language:  Python 3.4.3
    Game Library:  Pygame 1.9.2a0            
    Codebase Size:  3615 LOC

    Resolution:  800 x 600 pixels
    Colors:  216
    Text Grid:  80 x 30 characters

    Font:  TerminusBold.ttf, 20 pt
    Sound:  16-bit (made with SFXR)
    Music:  Tom Murphy (www.cs.cmu.edu/~tom7)

Background Story:

    When I was a kid I read a lot of those "Choose Your Own Adventure"-style
    gamebooks, with the more advanced ones being more like mini-RPGs with
    character stats, hit points, and combat with monsters.

    I could never figure out as a kid why combat in those books was so
    unsatisfying, so ultimately boring and pointless. As an adult, its 
    easier for me to see why (those books relied heavily on chance and left
    little strategic choice to the player). Games like chess are engaging 
    because they are pure strategic games. Games like poker are interesting
    becuase they have a little bit if chance and a little bit of strategy
    together in one game.

    This game (Monstrosity) started as a prototype to flesh out a new
    combat mechanic I thought would be great for a new type of gamebook, one
    that gave the player more strategic power. The system I ended up with is
    very effective in my opinion, but ultimately would be too cumbersome to
    do with pen and paper. It works relatively well as a computer game, where
    the computer can do most of the (mathematical) heavy-lifting.

    This game was a lot of fun to make. I wrote it in Python, a language I
    feel is a pleasure to work with. It always amazes me how much can be done
    with python that would take five to ten times as much code in a language
    like C or Java.

    The Pygame library (a python wrapper for the SDL library) was employed for
    graphics and sound implementation, but the engine and program architecture
    was all done from the ground up by myself. All the source is crammed into
    one monolithic source code file, a practice that makes me cringe now as a
    more experienced programmer.

The New Combat Mechanic:

    I always imagined that if a highly trained sword fighter gained more and
    more experience, it must seem like his or her opponents almost move in 
    slow motion, their attacks and defenses so obviously telegraphed (the
    other name I was going to use for this game was Telegraph).

    This new mechanic employs that idea with a combat skill rating (I believe
    it is in a large range of 0 to 999 points). If you come across an 
    apponent that has a lower combat rating than you, you will "see" his
    intended next move (in the game, it is marked with a yellow or grey 
    symbol: yellow arrows to indicate the monster is about to move in a 
    given direction, a yellow circle-out symbol to show the monster is not
    intending on making any action, and a grey sword to telegraph that this
    monster is about to swing his weapon at you.

    You, as a higher-ranked fighter, can act appropriately, moving out of
    the way if the monster is about to strike, or attack if the monster is
    clearly going to move away from you.

    As a higher ranked combat rating, you get to act first, before your 
    lower ranked opponent moves. This is the key to the whole system working.

    If you come across a higher ranked combatter than yourself, you will NOT
    see their moves telegraphed, and they WILL GET TO ACT FIRST.

    Have fun!