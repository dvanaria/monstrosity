# Programmer: Darron Vanaria
# Last Modified: Sun Sep 20, 2020  10:53PM
# Filename: monstrosity.py
# Language Version: Python 3.4.3
# Library Version: Pygame 1.9.2a0
# LOC: 2496

import pygame
import random
import sys
import time
from pygame.locals import *

x = 50
y = 70
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

class TextComponent:

    # This object is an extension to the GraphicsComponent - it handles all 
    # font-related drawing on a surface which is then blitted to the main
    # surface. Boxes are also drawn around certain areas to direct the user.
    #
    # Other parts of the program can set text in the "text box" area by
    # calling tc.lines (an array of 2-item tuples: text, color) and can also
    # clear this area by setting tc.lines = []

    global ic
    global gc
    global sc

    COL_X = 52
    COL_Y = 2

    BOX_X = 3
    BOX_Y = 26
    
    BLINK_ON = 30
    BLINK_OFF = 5 

    def __init__(self):

        # Constants
        self.CHARACTER_GRID_WIDTH = 80
        self.CHARACTER_GRID_HEIGHT = 30

        # Initialize Font 
        self.FONT_NAME    = "fonts/TerminusBold.ttf"
        self.FONT_SIZE    = 20 
        self.FONT         = pygame.font.Font(self.FONT_NAME, self.FONT_SIZE)
        self.FONT_WIDTH   = self.FONT.size(" ")[0]
        self.FONT_HEIGHT  = self.FONT.size(" ")[1]

        # the surface all text is written on, then blitted to mainSurface later
        self.text_surface = gc.mainSurface.convert()

        # this is the "text box" area under the dungeon map
        self.lines = []
       
        # this is to blink certain visual indicators on the screen, to help
        # guide the novice player
        self.blink = TextComponent.BLINK_ON + TextComponent.BLINK_OFF
        self.blink_feature_on = True


    def update(self):

        if self.blink_feature_on == True: 
            self.blink -= 1

            if self.blink < 0:
                self.blink = TextComponent.BLINK_ON + TextComponent.BLINK_OFF
               
            blink_color = BLACK 

            if self.blink > TextComponent.BLINK_OFF:
                blink_color = YELLOW
        else:
            blink_color = YELLOW

        
        self.text_surface.fill((0,0,0))


        if wc.exit_unlocked == True:
            self.add_text('EXIT: Unlocked!', RED, 1, 0)
        else:
            self.add_text('EXIT: Locked', YELLOW, 1, 0)

        if wc.monsters_killed >= WorldComponent.MONSTERS_NEEDED_FOR_EXIT:
            self.add_text('Monsters: ' + str(wc.monsters_killed), RED, 20, 0)
        else:
            self.add_text('Monsters: ' + str(wc.monsters_killed), YELLOW, 20, 0)
        
        if wc.keys_collected >= WorldComponent.KEYS_NEEDED_FOR_EXIT:
            self.add_text('Keys: ' + str(wc.keys_collected), RED, 37, 0)
        else:
            self.add_text('Keys: ' + str(wc.keys_collected), YELLOW, 37, 0)


        self.add_text('(Press F for FAQ, ESC to quit)', GREEN, 49,0)
        
        self.add_text("Player: ", WHITE, \
                TextComponent.COL_X, TextComponent.COL_Y) 
        self.add_text(wc.player.name, wc.player.color, \
                TextComponent.COL_X + 8, TextComponent.COL_Y)
        
        self.add_text("COMBAT: " + str(wc.player.COMBAT), WHITE, \
                TextComponent.COL_X, TextComponent.COL_Y + 1) 

        if wc.player.FATIGUE == Character.MAX_FATIGUE:
            self.add_text("FATIGUE: " + str(wc.player.FATIGUE), RED, \
                    TextComponent.COL_X, TextComponent.COL_Y + 2) 
        elif wc.player.FATIGUE > (Character.MAX_FATIGUE / 2):
            if wc.player.status == Character.ACTIVE:
                self.add_text("FATIGUE: " + str(wc.player.FATIGUE), blink_color, \
                    TextComponent.COL_X, TextComponent.COL_Y + 2) 
            else:
                self.add_text("FATIGUE: " + str(wc.player.FATIGUE), YELLOW, \
                    TextComponent.COL_X, TextComponent.COL_Y + 2) 
        else:
            self.add_text("FATIGUE: " + str(wc.player.FATIGUE), WHITE, \
                    TextComponent.COL_X, TextComponent.COL_Y + 2) 
        self.add_text(' (' + str(Character.MAX_FATIGUE) + ' = COLLAPSE)', WHITE, \
                TextComponent.COL_X + 11, TextComponent.COL_Y + 2) 

        if wc.player.INJURIES == Character.MAX_INJURY: 
            self.add_text("INJURIES: " + str(wc.player.INJURIES), RED, \
                    TextComponent.COL_X, TextComponent.COL_Y + 3) 
        elif wc.player.INJURIES > (Character.MAX_INJURY / 2): 
            self.add_text("INJURIES: " + str(wc.player.INJURIES), blink_color, \
                    TextComponent.COL_X, TextComponent.COL_Y + 3) 
        else: 
            self.add_text("INJURIES: " + str(wc.player.INJURIES), WHITE, \
                    TextComponent.COL_X, TextComponent.COL_Y + 3) 
        self.add_text(' (' + str(Character.MAX_INJURY) + ' = DEATH)', WHITE, \
                TextComponent.COL_X + 12, TextComponent.COL_Y + 3) 

        if ic.mode != InputComponent.SPELL_SELECTION:
            self.add_text("SPELLS: (name and cost)", WHITE, \
                    TextComponent.COL_X, TextComponent.COL_Y + 5) 
        else:
            self.add_text("SPELLS: ", WHITE, \
                    TextComponent.COL_X, TextComponent.COL_Y + 5) 
        
        for s in wc.player.spellbook:
            self.add_text(str(s.number) + '. ' + s.name + \
                    ' (' + str(s.cost) + ')', WHITE, \
                TextComponent.COL_X, TextComponent.COL_Y + 5 + s.number) 


        controls = 14 
        self.add_text("CONTROLS:", WHITE, \
                TextComponent.COL_X, TextComponent.COL_Y + controls) 
        self.add_text("[Arrow Keys] to Move", WHITE, \
                TextComponent.COL_X, TextComponent.COL_Y + controls+1)
        self.add_text("[S] Sword Attack", WHITE, \
                TextComponent.COL_X, TextComponent.COL_Y + controls+2)
        self.add_text("[W] Wait (Do Nothing)", WHITE, \
                TextComponent.COL_X, TextComponent.COL_Y + controls+3)
        self.add_text("[C] Cast Spell", WHITE, \
                TextComponent.COL_X, TextComponent.COL_Y + controls+4)

        players = 20
        self.add_text("PLAYER PARTY:", WHITE, \
                TextComponent.COL_X, TextComponent.COL_Y + players) 
        for c in wc.player_list:
            self.add_text(str(c.number) + '. ' + c.name, WHITE, \
                TextComponent.COL_X, TextComponent.COL_Y + players + c.number ) 
            if c in wc.winners_circle:
                self.add_text('(ESCAPED)', BLUE, \
                    TextComponent.COL_X + 11, TextComponent.COL_Y + players + c.number ) 
            elif c.status == Character.DEAD:
                self.add_text('(DEAD)', RED, \
                    TextComponent.COL_X + 11, TextComponent.COL_Y + players + c.number ) 
            elif c.status == Character.STONED:
                if ic.mode == InputComponent.CHOOSE_PLAYER and \
                        c == wc.player:
                    self.add_text('(STONE)', BLACK, \
                        TextComponent.COL_X + 11, TextComponent.COL_Y + players + c.number ) 
                else:
                    self.add_text('(STONE)', GREY, \
                        TextComponent.COL_X + 11, TextComponent.COL_Y + players + c.number ) 
            elif c.number == wc.player.number:
                self.add_text('(PLAYER CONTROL)', YELLOW, \
                    TextComponent.COL_X + 11, TextComponent.COL_Y + players + c.number ) 

        # this is the box area underneath the dungeon map
        line_index = 0
        for line in self.lines:
            self.add_text(line[0], line[1], \
                TextComponent.BOX_X - 1, TextComponent.BOX_Y + line_index ) 
            line_index += 1

        adj = 18 

        # highlight spell list, if mode is enabled
        if ic.mode == InputComponent.SPELL_SELECTION:
            box_x = 510
            box_y = 113 + adj
            box_w = 279 
            box_h = 194 - adj
            pygame.draw.rect(self.text_surface, YELLOW, 
                    (box_x, box_y, box_w, box_h), 2)
            self.add_text("(select number)", blink_color, \
                TextComponent.COL_X + 8, TextComponent.COL_Y + 5) 

        # highlight controls box, if mode is enabled
        if ic.mode == InputComponent.MAIN_CONTROLS:
            box_x = 510
            box_y = 311  
            box_w = 279 
            box_h = 116
            pygame.draw.rect(self.text_surface, YELLOW, 
                    (box_x, box_y, box_w, box_h), 2)
            self.add_text("(select action)", blink_color, \
                TextComponent.COL_X + 10, TextComponent.COL_Y + 14) 

        # highlight player list, if mode is enabled
        if ic.mode == InputComponent.CHOOSE_PLAYER:
            box_x = 510
            box_y = 433
            box_w = 279 
            box_h = 156
            pygame.draw.rect(self.text_surface, YELLOW, 
                    (box_x, box_y, box_w, box_h), 2)
            self.add_text("(select)", blink_color, \
                TextComponent.COL_X + 14, TextComponent.COL_Y + 20) 

            if wc.player.FATIGUE == Character.MAX_FATIGUE:
                text = wc.player.name + ' becomes exhausted and turns to stone.'
                self.add_text(\
                      text, \
                      blink_color, \
                      TextComponent.COL_X - 50, TextComponent.COL_Y + 26) 
                
        if ic.mode == InputComponent.TARGETING:        
            self.add_text(\
                  "Use arrow keys to aim, ENTER to select target.", \
                  blink_color, \
                  TextComponent.COL_X - 50, TextComponent.COL_Y + 25) 
        

        if ic.mode == InputComponent.WITHIN_SPELL:        
            self.add_text(\
                  "Press ESC to end this spell.", \
                  blink_color, \
                  TextComponent.COL_X - 50, TextComponent.COL_Y + 26) 

        if ic.mode == InputComponent.SPELL_SELECTION:
            tc.lines = []
            self.add_text( \
                'Select a spell by number, ESC to abort.', \
                blink_color, \
                TextComponent.COL_X - 50, TextComponent.COL_Y + 24)

        if ic.mode == InputComponent.CONFIRM_QUIT:
            tc.lines = []
            self.add_text( \
                "Please confirm: Close program? (y/n)", \
                blink_color, \
                TextComponent.COL_X - 50, TextComponent.COL_Y + 24)

        if ic.mode == InputComponent.CONFIRM_SUICIDE:
            tc.lines = []
            self.add_text( \
                "Please confirm: Kill player? (y/n)", \
                blink_color, \
                TextComponent.COL_X - 50, TextComponent.COL_Y + 24)
        
        # blit this surface to the main surface!
        gc.mainSurface.blit(self.text_surface, (0,0))
       

    
    def add_text(self, t, color, cx, cy):

        line = self.FONT.render(t, False, color)
        
        self.text_surface.blit(line, (cx * self.FONT_WIDTH, cy * self.FONT_HEIGHT))
        


class WorldComponent:

    # needs access to InputComponent and GraphicsComponent
    global ic
    global gc
    global sc

    # initial values are only to show "level 9" approximation
    WORLD_WIDTH  = 97
    WORLD_HEIGHT = 97

    NUM_KEYS              = 18
    KEYS_NEEDED_FOR_EXIT  = 6

    NUM_MONSTERS             = 70 
    MONSTERS_NEEDED_FOR_EXIT = 46

    NUM_PLAYERS  = 6

    # enums for board array
    TILE             = 0
    WALL             = 1
    TILE_DEAD_BODY   = 2
    DOOR_OPEN        = 3
    DOOR_STUCK       = 4
    DOOR_HELD        = 5
    EXIT             = 6
    TRAP             = 7
    KEY              = 8

    # level information
    START_LEVEL = 2
    END_LEVEL = 9

    def __init__(self):

        # "level" feature: go through EXIT = go to next level.
        # Each level is bigger, has more monsters, and requires more keys to 
        # unlock the next EXIT.
        self.level = WorldComponent.START_LEVEL 
        WorldComponent.WORLD_WIDTH  = self.level * 11
        WorldComponent.WORLD_HEIGHT = self.level * 11
        WorldComponent.NUM_KEYS     = self.level * 3 
        WorldComponent.NUM_MONSTERS = self.level * 7
        WorldComponent.KEYS_NEEDED_FOR_EXIT  = self.level * 2 
        WorldComponent.MONSTERS_NEEDED_FOR_EXIT = self.level * 4

        # these get set in generateRandomCharacters()
        self.player = None 
        self.character_list = []  # list of all Characters (MONSTERS and PLAYERS) 
        self.rooms = []   # a list of x,y pairs, used to place EXIT and monsters
        self.exit_x = 0
        self.exit_y = 0
        self.player_list = []
        self.num_guardians = 0

        # a 2D array of INT (example: WorldComponent.WALL)
        self.board = self.generateRandomBoard() 

        # a 2D array of Character objects (includes Player and Monsters)
        self.characters = self.generateRandomCharacters() 

        # a 2D array of Boolean
        self.light = self.generateLightArray()

        # a 2D array of INT (1,2,3,4,5,6 -> Character.number) 0 = no paint
        self.tile_color = self.generateTileColorArray()

        # this gets set to True if a monster is within the visible 9x9 area
        self.encounter = False

        # this is where all players end up if they successfully escape!
        self.winners_circle = [] 

        # The big 3 items that are needed to unlock each EXIT, as well as 
        # serve as the player's score.
        self.keys_collected = 0
        self.monsters_killed = 0
        self.tiles_explored = 0

        self.score = 0
        
        self.exit_unlocked = False

        self.nextLevel = False
        
        self.turn = 0


    def newWorld(self):

        global gc

        old_player_list = self.player_list
        old_player = self.player

        self.level += 1

        WorldComponent.WORLD_WIDTH  = self.level * 11
        WorldComponent.WORLD_HEIGHT = self.level * 11
        WorldComponent.NUM_KEYS     = self.level * 3 
        WorldComponent.NUM_MONSTERS = self.level * 7

        WorldComponent.KEYS_NEEDED_FOR_EXIT  = (self.level * 2) + \
                WorldComponent.KEYS_NEEDED_FOR_EXIT
        
        WorldComponent.MONSTERS_NEEDED_FOR_EXIT  = (self.level * 4) + \
                WorldComponent.MONSTERS_NEEDED_FOR_EXIT

        # these get set in generateRandomCharacters()
        self.player = None 
        self.character_list = []  # list of all Characters (MONSTERS and PLAYERS) 
        self.rooms = []   # a list of x,y pairs, used to place EXIT and monsters
        self.exit_x = 0
        self.exit_y = 0
        self.player_list = []
        self.num_guardians = 0

        # a 2D array of INT (example: WorldComponent.WALL)
        self.board = self.generateRandomBoard() 

        # a 2D array of Character objects (includes Player and Monsters)
        self.characters = self.generateRandomCharacters() 


        # a 2D array of INT (1,2,3,4,5,6 -> Character.number) 0 = no paint
        self.tile_color = self.generateTileColorArray()

        # this gets set to True if a monster is within the visible 9x9 area
        self.encounter = False

        # this is where all players end up if they successfully escape!
        self.winners_circle = [] 

        # keep new locations of the Players, but substitute in old data 
        for op in old_player_list:
            for np in self.player_list:
                if np.number == op.number:
                    np.COMBAT = op.COMBAT
                    np.FATIGUE = op.FATIGUE
                    np.INJURIES = op.INJURIES
                    if op.status == Character.DEAD:
                        np.status = Character.DEAD
                        np.plan = None
                        np.action = None
                        self.characters[np.y][np.x] = None
                        self.board[np.y][np.x] = WorldComponent.TILE_DEAD_BODY
                    #elif np.status != Character.ACTIVE:
                        #np.status = Character.STONED
                    else:
                        np.status = Character.STONED
                    np.spellbook = op.spellbook

        # Choose ACTIVE player
        selected = False
        rec = 1000
        while selected == False: 
            rp = random.choice(self.player_list)
            rec -= 1
            if rec <= 0:
                print('ERROR: Could not find next player.')
                pygame.quit()
                sys.exit()
            if rp.status == Character.STONED:
                rp.status = Character.ACTIVE
                wc.player = rp
                selected = True


        # a 2D array of Boolean
        self.light = self.generateLightArray()


        self.exit_unlocked = False

        sc.stop_music()

        gc = GraphicsComponent()
        
        gc.orientCameraOnPlayer(wc.player.x, wc.player.y)
        gc.calculateLight()
        gc.update() 

 
    def attemptToUnlockExit(self):

        requirements = 2

        if self.monsters_killed >= WorldComponent.MONSTERS_NEEDED_FOR_EXIT:

            requirements -= 1

        if self.keys_collected >= WorldComponent.KEYS_NEEDED_FOR_EXIT:

            requirements -= 1
            
        if requirements == 0:

            if wc.exit_unlocked == False:
                tc.lines.append(('EXIT is now unlocked!', RED))
                wc.exit_unlocked = True
                sc.exit_unlocked.play()

    def generateTileColorArray(self):
        
        b = []

        row = []
        for r in range(WorldComponent.WORLD_HEIGHT):
            for c in range(WorldComponent.WORLD_WIDTH):

                row.append(0)

            b.append(row)
            row = []

        return b


    def generateLightArray(self):

        b = []

        row = []
        for r in range(WorldComponent.WORLD_HEIGHT):
            for c in range(WorldComponent.WORLD_WIDTH):

                if self.characters[r][c] != None:
                    i = self.characters[r][c]
                    if i.character_type == Character.PLAYER and \
                            i.status == Character.ACTIVE:
                        row.append(True)
                    else:
                        row.append(False)
                else:
                    row.append(False)

            b.append(row)
            row = []

        return b

    def generateRandomBoard(self):

        b = []


        # first fill entire board with tiles and random walls
        row = []
        for r in range(WorldComponent.WORLD_HEIGHT):
            for c in range(WorldComponent.WORLD_WIDTH):
                row.append( random.choice(
                    [WorldComponent.TILE, WorldComponent.TILE,
                        WorldComponent.WALL]) )
            b.append(row)
            row = []

        
        # next add some solid areas of the dungeon that will form islands of
        # rooms/passages. Use the PAINT_FLOOR algorithm.
        NUMBER_SOLID_AREAS = self.level * 5 
        SIZE_OF_SOLID_AREAS = self.level * 52 
        for z in range(NUMBER_SOLID_AREAS):

            x = random.randint(0,WorldComponent.WORLD_WIDTH-1)
            y = random.randint(0,WorldComponent.WORLD_HEIGHT-1)

            b[y][x] = WorldComponent.WALL
            dx = 0
            dy = 0

            # make the voids big enough to cut off players from one another
            for i in range(SIZE_OF_SOLID_AREAS):

                dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                x += dx
                y += dy

                if x < 0:
                   x = 0
                if x > WorldComponent.WORLD_WIDTH - 1:
                   x = WorldComponent.WORLD_WIDTH - 1
                if y < 0:
                   y = 0
                if y > WorldComponent.WORLD_HEIGHT - 1:
                   y = WorldComponent.WORLD_HEIGHT - 1

                b[y][x] = WorldComponent.WALL
                        
        
        # make sure a player doesn't get trapped on a single tile 
        for r in range(WorldComponent.WORLD_HEIGHT):
            for c in range(WorldComponent.WORLD_WIDTH):

                space_tiles = 0

                if b[r][c] == WorldComponent.TILE:

                    if r-1 != -1:
                        if b[r-1][c] == WorldComponent.TILE:
                            space_tiles += 1
                    if r+1 != WorldComponent.WORLD_HEIGHT:
                        if b[r+1][c] == WorldComponent.TILE:
                            space_tiles += 1
                    if c-1 != -1:
                        if b[r][c-1] == WorldComponent.TILE:
                            space_tiles += 1
                    if c+1 != WorldComponent.WORLD_WIDTH:
                        if b[r][c+1] == WorldComponent.TILE:
                            space_tiles += 1
                            
                    if space_tiles == 0:

                        if r-1 != -1:
                            b[r-1][c] = WorldComponent.TILE
                        if r+1 != WorldComponent.WORLD_HEIGHT:
                            b[r+1][c] = WorldComponent.TILE
                        if c-1 != -1:
                            b[r][c-1] = WorldComponent.TILE
                        if c+1 != WorldComponent.WORLD_WIDTH:
                            b[r][c+1] = WorldComponent.TILE


        # build rooms
        NUMBER_OF_ROOMS = self.level * 4 
        MIN_ROOM_SIZE = 6
        MAX_ROOM_SIZE = 12 
        NUMBER_OF_DOORS = 2
        for room in range(NUMBER_OF_ROOMS):

            size = random.randint(MIN_ROOM_SIZE,MAX_ROOM_SIZE)
            start_x = random.randint(1,WorldComponent.WORLD_WIDTH-size-1)
            start_y = random.randint(1,WorldComponent.WORLD_HEIGHT-size-1)

            # horizontal room sides
            for c in range(size):
                    
                b[start_y][start_x+c] = WorldComponent.WALL
                    
                b[start_y+size-1][start_x+c] = WorldComponent.WALL

            # vertical room sides
            for r in range(size-2):

                b[start_y+1+r][start_x] = WorldComponent.WALL

                b[start_y+1+r][start_x+size-1] = WorldComponent.WALL

            # clear space inside
            for r in range(size-2):
                for c in range(size-2):
                    b[start_y+r+1][start_x+c+1] = WorldComponent.TILE
                    self.rooms.append((start_y+r+1, start_x+c+1))

            # doors 
            MIN_LENGTH_HALLWAY = self.level 
            MAX_LENGTH_HALLWAY = WorldComponent.WORLD_WIDTH - (self.level * 3) 
            for d in range(NUMBER_OF_DOORS): 
           
                # horizontal or vertical wall? (0 = horizontal)
                if random.randint(0,1) == 0:

                    # place door
                    random_c = random.randint(1,size-2) + start_x
                    random_r = random.choice([start_y,start_y+size-1])
                    if random.randint(0,1) == 0:
                        b[random_r][random_c] = WorldComponent.DOOR_STUCK
                    else:
                        b[random_r][random_c] = WorldComponent.DOOR_HELD

                    # now extend N-S hallway from this door
                    within_room = 0
                    random_dy = random.choice([-1,1])
                    length = random.randint(MIN_LENGTH_HALLWAY,
                            MAX_LENGTH_HALLWAY)
                    random_r += random_dy
                    for zz in range(length):

                        # if you picked the "within room" direction, kill it
                        if random_r != 0 and \
                                random_r != WorldComponent.WORLD_HEIGHT:
                            if b[random_r][random_c] == WorldComponent.TILE:
                                within_room += 1
                                if within_room == MIN_ROOM_SIZE:
                                    zz = length - 1
                        
                        # blast through!
                        if random_r != 0 and \
                                random_r != WorldComponent.WORLD_HEIGHT:
                            b[random_r][random_c] = WorldComponent.TILE
                            random_r += random_dy



                else:

                    # place door
                    random_c = random.choice([start_x,start_x+size-1]) 
                    random_r = random.randint(1,size-2) + start_y
                    if random.randint(0,1) == 0:
                        b[random_r][random_c] = WorldComponent.DOOR_STUCK
                    else:
                        b[random_r][random_c] = WorldComponent.DOOR_HELD

                    # now extend E-W hallway from this door
                    within_room = 0
                    random_dx = random.choice([-1,1])
                    length = random.randint(MIN_LENGTH_HALLWAY,
                            MAX_LENGTH_HALLWAY)
                    random_c += random_dx
                    for zz in range(length):
                       
                        # if you picked the "within room" direction, kill it
                        if random_c != 0 and \
                                random_c != WorldComponent.WORLD_WIDTH:
                            if b[random_r][random_c] == WorldComponent.TILE:
                                within_room += 1
                                if within_room == MIN_ROOM_SIZE:
                                    zz = length - 1

                        # blast through!
                        if random_c != 0 and \
                                random_c != WorldComponent.WORLD_WIDTH:
                            b[random_r][random_c] = WorldComponent.TILE
                            random_c += random_dx

        # another round of solid areas to create islands
        NUMBER_SOLID_AREAS = self.level * 2 
        SIZE_OF_SOLID_AREAS = self.level * 19 
        for z in range(NUMBER_SOLID_AREAS):

            x = random.randint(0,WorldComponent.WORLD_WIDTH-1)
            y = random.randint(0,WorldComponent.WORLD_HEIGHT-1)

            b[y][x] = WorldComponent.WALL
            dx = 0
            dy = 0

            # make the voids big enough to cut off players from one another
            for i in range(SIZE_OF_SOLID_AREAS):

                dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                x += dx
                y += dy

                if x < 0:
                   x = 0
                if x > WorldComponent.WORLD_WIDTH - 1:
                   x = WorldComponent.WORLD_WIDTH - 1
                if y < 0:
                   y = 0
                if y > WorldComponent.WORLD_HEIGHT - 1:
                   y = WorldComponent.WORLD_HEIGHT - 1

                b[y][x] = WorldComponent.WALL

                    
                    
        # a round of solid wall "runs" to section off areas
        NUMBER_WALLS = self.level 
        MIN_SIZE_OF_WALLS = 3
        MAX_SIZE_OF_WALLS = int(WorldComponent.WORLD_WIDTH / 2) 
        for z in range(NUMBER_WALLS):

            random_c = random.randint(0,WorldComponent.WORLD_WIDTH-1)
            random_r = random.randint(0,WorldComponent.WORLD_HEIGHT-1)

            # horizontal or vertical wall? (0 = vertical)
            if random.randint(0,1) == 0:

                # extend N-S (vertical) wall from here 
                random_dy = random.choice([-1,1])
                length = random.randint(MIN_SIZE_OF_WALLS, MAX_SIZE_OF_WALLS)
                random_r += random_dy
                for zz in range(length):

                    # build wall!
                    if random_r != 0 and \
                            random_r != WorldComponent.WORLD_HEIGHT:
                        b[random_r][random_c] = WorldComponent.WALL
                        random_r += random_dy

            else:

                # extend E_W (horizontal) wall from here 

                random_dx = random.choice([-1,1])
                length = random.randint(MIN_SIZE_OF_WALLS, MAX_SIZE_OF_WALLS)
                random_c += random_dx
                for zz in range(length):

                    # build wall!
                    if random_c != 0 and \
                            random_c != WorldComponent.WORLD_WIDTH:
                        b[random_r][random_c] = WorldComponent.WALL
                        random_c += random_dx


        # cleanup any isolated TILE (one that is surrounded by WALL)
        for r in range(WorldComponent.WORLD_HEIGHT):
            for c in range(WorldComponent.WORLD_WIDTH):

                num_checks = 0
                num_walls = 0

                if r-1 != 0:
                    num_checks += 1
                    if b[c][r-1] == WorldComponent.WALL:
                        num_walls += 1
                if r+1 != WorldComponent.WORLD_HEIGHT:
                    num_checks += 1
                    if b[c][r+1] == WorldComponent.WALL:
                        num_walls += 1
                if c-1 != 0:
                    num_checks += 1
                    if b[c-1][r] == WorldComponent.WALL:
                        num_walls += 1
                if c+1 != WorldComponent.WORLD_WIDTH:
                    num_checks += 1
                    if b[c+1][r] == WorldComponent.WALL:
                        num_walls += 1
                if r-1 != 0 and c-1 != 0:
                    num_checks += 1
                    if b[c-1][r-1] == WorldComponent.WALL:
                        num_walls += 1
                if r+1 != WorldComponent.WORLD_HEIGHT and \
                   c+1 != WorldComponent.WORLD_WIDTH:
                    num_checks += 1
                    if b[c+1][r+1] == WorldComponent.WALL:
                        num_walls += 1
                if c-1 != 0 and r+1 != WorldComponent.WORLD_HEIGHT: 
                    num_checks += 1
                    if b[c-1][r+1] == WorldComponent.WALL:
                        num_walls += 1
                if c+1 != WorldComponent.WORLD_WIDTH and r-1 != 0:
                    num_checks += 1
                    if b[c+1][r-1] == WorldComponent.WALL:
                        num_walls += 1

                if num_walls == num_checks:
                    b[c][r] = WorldComponent.WALL



        # generate and place keys 
        keys = WorldComponent.NUM_KEYS 
        while keys > 0:
            c = random.randint(0, WorldComponent.WORLD_WIDTH - 1)
            r = random.randint(0, WorldComponent.WORLD_HEIGHT - 1)
            if b[r][c] == WorldComponent.TILE:
                b[r][c] = WorldComponent.KEY
                keys -= 1

        # last: place the EXIT
        exit_placed = False
        while exit_placed == False:
            c = random.randint(0, WorldComponent.WORLD_WIDTH - 1)
            r = random.randint(0, WorldComponent.WORLD_HEIGHT - 1)
            if (c,r) in self.rooms:
                b[r][c] = WorldComponent.EXIT
                exit_placed = True
                self.exit_y = r
                self.exit_x = c
       
        return b
    
    def generateRandomCharacters(self):

        b = []

        row = []
        for r in range(WorldComponent.WORLD_HEIGHT):
            for c in range(WorldComponent.WORLD_WIDTH):
                row.append( None )
            b.append(row)
            row = []

        for m in range(WorldComponent.NUM_MONSTERS):
            locationFound = False
            while locationFound == False:
                x = random.randint(0, WorldComponent.WORLD_WIDTH-1)
                y = random.randint(0, WorldComponent.WORLD_HEIGHT-1)
                if b[y][x] == None and self.board[y][x] == WorldComponent.TILE:
                    i = Character(Character.MONSTER, m) 
                    i.status = Character.ACTIVE
                    self.character_list.append(i)
                    i.x = x
                    i.y = y
                    b[y][x] = i 
                    locationFound = True

        for nc in range(WorldComponent.NUM_PLAYERS):

            locationFound = False

            while locationFound == False:

                x = random.randint(0, WorldComponent.WORLD_WIDTH-1)
                y = random.randint(0, WorldComponent.WORLD_HEIGHT-1)

                num_walls = 0

                if y-1 > 0:
                    if self.board[y-1][x] == WorldComponent.WALL:
                        num_walls += 1
                if y+1 < WorldComponent.WORLD_HEIGHT - 1:
                    if self.board[y+1][x] == WorldComponent.WALL:
                        num_walls += 1
                if x-1 > 0:
                    if self.board[y][x-1] == WorldComponent.WALL:
                        num_walls += 1
                if x+1 < WorldComponent.WORLD_WIDTH - 1:
                    if self.board[y][x+1] == WorldComponent.WALL:
                        num_walls += 1

                if b[y][x] == None and \
                        self.board[y][x] == WorldComponent.TILE and \
                        num_walls < 4:
                    
                    self.player = Character(Character.PLAYER, nc + 1) 
                    self.character_list.append(self.player)
                    self.player.x = x
                    self.player.y = y
                    b[y][x] = self.player 
                    locationFound = True
                    if (nc+1) == 1:
                        self.player.name = 'Rodina'
                        self.player.color = RED 
                        self.player.number = 1
                    elif (nc+1) == 2:
                        self.player.name = 'Greedo'
                        self.player.color = GREEN 
                        self.player.number = 2
                    elif (nc+1) == 3:
                        self.player.name = 'Bluth'
                        self.player.color = BLUE 
                        self.player.number = 3
                    elif (nc+1) == 4:
                        self.player.name = 'Yorrik'
                        self.player.color = YELLOW 
                        self.player.number = 4
                    elif (nc+1) == 5:
                        self.player.name = 'Cyrano'
                        self.player.color = CYAN 
                        self.player.number = 5
                    elif (nc+1) == 6:
                        self.player.name = 'Magenta'
                        self.player.color = MAGENTA 
                        self.player.number = 6

                    self.player_list.append(self.player)
    
        # choose starting character
        start = random.randint(1,6)
        for i in self.player_list:
            if i.number == start:
                self.player = i
                self.player.status = Character.ACTIVE

        # surround EXIT with lots of powerful monsters
        for r in range(WorldComponent.WORLD_HEIGHT):
            for c in range(WorldComponent.WORLD_WIDTH):
                if self.board[r][c] == WorldComponent.EXIT:
                    tries = self.level
                    while tries > 0:
                        x = random.randint(c-9,c+9)
                        y = random.randint(r-9,r+9)
                        if x < 0:
                            x = 0
                        if x > WorldComponent.WORLD_WIDTH - 1:
                            x = WorldComponent.WORLD_WIDTH - 1
                        if y < 0:
                            y = 0
                        if y > WorldComponent.WORLD_HEIGHT - 1:
                            y = WorldComponent.WORLD_HEIGHT - 1
                        if self.board[y][x] == WorldComponent.TILE and \
                                b[y][x] == None:
                            i = Character(Character.MONSTER, m) 
                            self.num_guardians += 1
                            i.status = Character.ACTIVE
                            i.COMBAT = random.randint(800,999) 
                            self.character_list.append(i)
                            i.x = x
                            i.y = y 
                            b[y][x] = i 
                            tries -= 1

        return b

    def isValidMove(self, x, y, c):

        result = True 

        if x < 0 or y < 0:

            result = False

        elif x > WorldComponent.WORLD_WIDTH - 1 \
            or y > WorldComponent.WORLD_HEIGHT - 1:

            result = False

        else: # at least we know its in-bounds

            # master list: all valid spaces must show up here
            if self.board[y][x] != WorldComponent.TILE and \
                    self.board[y][x] != WorldComponent.TILE_DEAD_BODY and \
                    self.board[y][x] != WorldComponent.DOOR_OPEN and \
                    self.board[y][x] != WorldComponent.DOOR_HELD and \
                    self.board[y][x] != WorldComponent.DOOR_STUCK and \
                    self.board[y][x] != WorldComponent.TRAP and \
                    self.board[y][x] != WorldComponent.KEY and \
                    self.board[y][x] != WorldComponent.EXIT:

                result = False

            if self.characters[y][x] != None: 

                result = False

            if self.board[y][x] == WorldComponent.DOOR_STUCK and \
                    c.character_type != Character.PLAYER:

                result = False
            
            if self.board[y][x] == WorldComponent.DOOR_HELD and \
                    c.character_type != Character.PLAYER:

                result = False
            
            if self.board[y][x] == WorldComponent.EXIT and \
                    c.character_type != Character.PLAYER:

                result = False
            
            if self.board[y][x] == WorldComponent.KEY and \
                    c.character_type != Character.PLAYER:

                result = False

        return result


    def calculateScore(self):

        wc.score = (wc.keys_collected + wc.monsters_killed) * (wc.level - 1)

    
    def foundKey(self):
        
        self.keys_collected += 1
        sc.key.play()
        tc.lines = []
        tc.lines.append(('Total keys now collected: ' + \
            str(wc.keys_collected) + '.', BLUE))


        if self.keys_collected >= WorldComponent.KEYS_NEEDED_FOR_EXIT:

            tc.lines.append(('Key requirement satisfied.', BLUE))
            #sc.exit_unlocked.play()
            wc.attemptToUnlockExit()

        
        self.calculateScore()

        



    # planning stage, helper functions (only needed for MOVE and SPELL)

    def playerPlanMove(self, dx, dy):

        wc.player.plan = Character.MOVE
        wc.player.dx = dx 
        wc.player.dy = dy

    def playerPlanSpell(self, tx, ty, spell):

        wc.player.plan = Character.SPELL
        wc.player.tx = tx 
        wc.player.ty = ty
        wc.player.selected_spell = spell


    def adjacentToPlayer(self, c):

        # returns True if c (a Character object) is adjacent to Player

        x = c.x
        y = c.y

        result = False

        if y > 0:
            i = self.characters[y-1][x]
            if i != None and i.character_type == Character.PLAYER and \
                    i.status != Character.STONED:
                result = True

        if y < WorldComponent.WORLD_HEIGHT - 1:
            i = self.characters[y+1][x]
            if i != None and  i.character_type == Character.PLAYER and \
                    i.status != Character.STONED:
                result = True

        if x > 0:
            i = self.characters[y][x-1]
            if i != None and  i.character_type == Character.PLAYER and \
                    i.status != Character.STONED:
                result = True

        if x < WorldComponent.WORLD_WIDTH - 1:
            i = self.characters[y][x+1]
            if i != None and  i.character_type == Character.PLAYER and \
                    i.status != Character.STONED:
                result = True

        return result


    def executeMove(self, c):

        if self.board[c.y+c.dy][c.x+c.dx] == WorldComponent.DOOR_HELD:

            if c.character_type == Character.PLAYER:

                tc.lines.append(('This door is being magically held.', GREEN))
                sc.denied_entry.play()

        elif self.board[c.y+c.dy][c.x+c.dx] == WorldComponent.EXIT and \
            wc.exit_unlocked == False:

            tc.lines.append(('The EXIT is locked.', YELLOW))

            if wc.keys_collected < WorldComponent.KEYS_NEEDED_FOR_EXIT and \
               wc.monsters_killed < WorldComponent.MONSTERS_NEEDED_FOR_EXIT:
                tc.lines.append(('Your party must collect a total of ' + \
                    str(WorldComponent.KEYS_NEEDED_FOR_EXIT) + ' keys', \
                    YELLOW))
                tc.lines.append(('and slay ' + \
                    str(WorldComponent.MONSTERS_NEEDED_FOR_EXIT) + \
                    ' monsters to unlock the EXIT.', \
                    YELLOW))
            elif wc.keys_collected < WorldComponent.KEYS_NEEDED_FOR_EXIT:
                tc.lines.append(('Your party must collect ' + \
                    str(WorldComponent.KEYS_NEEDED_FOR_EXIT) + \
                    ' keys to unlock EXIT.', \
                    YELLOW))
            elif wc.monsters_killed < WorldComponent.MONSTERS_NEEDED_FOR_EXIT:
                tc.lines.append(('Your party must slay ' + \
                    str(WorldComponent.MONSTERS_NEEDED_FOR_EXIT) + \
                    ' monsters to unlock EXIT.', \
                    YELLOW))

        else:

            self.characters[c.y][c.x] = None

            c.x += c.dx
            c.y += c.dy

            self.characters[c.y][c.x] = c 

            c.dx = 0
            c.dy = 0

            c.plan = None

            if gc.isCharacterVisible(c) == True:

                if c.character_type == Character.PLAYER:

                    sc.player_move.play()

                else:

                    sc.enemy_move.play()


            if self.board[c.y][c.x] == WorldComponent.DOOR_STUCK:

                self.board[c.y][c.x] = WorldComponent.DOOR_OPEN

                sc.stuck_door.play()

                if c.character_type == Character.PLAYER:

                    c.causeFatigue(3)

                    gc.calculateLight()

            if self.board[c.y][c.x] == WorldComponent.EXIT:

                if c.character_type == Character.PLAYER:
                    
                    self.escapeDungeon(c) 


            if self.board[c.y][c.x] == WorldComponent.TRAP:

                c.causeInjury(10)

                self.board[c.y][c.x] = WorldComponent.TILE

        
            if self.board[c.y][c.x] == WorldComponent.KEY:

                if c.character_type == Character.PLAYER:
                    
                    self.board[c.y][c.x] = WorldComponent.TILE

                    wc.foundKey()



            # check: did player just move next to a statue?
            if c.character_type == Character.PLAYER:

                x = c.x
                y = c.y

                adjacent = False
                name = None

                if y > 0:
                    i = self.characters[y-1][x]
                    if i != None and i.character_type == Character.PLAYER and \
                            i.status == Character.STONED:
                        i.INJURIES = 0
                        wc.player.INJURIES = 0
                        adjacent = True
                        name = i.name

                if y < WorldComponent.WORLD_HEIGHT - 1:
                    i = self.characters[y+1][x]
                    if i != None and  i.character_type == Character.PLAYER and \
                            i.status == Character.STONED:
                        i.INJURIES = 0
                        wc.player.INJURIES = 0
                        adjacent = True
                        name = i.name

                if x > 0:
                    i = self.characters[y][x-1]
                    if i != None and  i.character_type == Character.PLAYER and \
                            i.status == Character.STONED:
                        i.INJURIES = 0
                        wc.player.INJURIES = 0
                        adjacent = True
                        name = i.name

                if x < WorldComponent.WORLD_WIDTH - 1:
                    i = self.characters[y][x+1]
                    if i != None and  i.character_type == Character.PLAYER and \
                            i.status == Character.STONED:
                        i.INJURIES = 0
                        wc.player.INJURIES = 0
                        adjacent = True
                        name = i.name

                if adjacent == True:

                    text = 'This is a statue of ' + name + '.'
                    tc.lines.append((text,YELLOW))
                    tc.lines.append( \
                      ('You have both been healed (INJURIES = 0)', BLUE))
                    sc.restore_health.play()


    def executeSpell(self, s, x, y):

        sound_effect = None

        if s.code == Character.OPEN_DOOR:

            if self.board[y][x] == WorldComponent.DOOR_HELD or \
                    self.board[y][x] == WorldComponent.DOOR_STUCK:

                self.board[y][x] = WorldComponent.DOOR_OPEN

                wc.player.action = Character.GOOD_SPELL
                sound_effect = sc.open_held_door

            else:

                wc.player.action = Character.BAD_SPELL

            
        elif s.code == Character.WEAKEN_MONSTER:

            # this spell effects 5 squares: center + 4 cardinal directions
            # the center square does NOT have to hit in order for the remaining
            # squares to be tested - why? because the spell was proving too
            # weak - stronger monsters would usually move out of the way before
            # the spell took effect.

            num_hits = 0

            c = self.characters[y][x]
            if c != None:
                if c.character_type == Character.MONSTER:
                    c.COMBAT = wc.player.COMBAT - 1
                    num_hits += 1
           
            if y > 0:
                c = self.characters[y-1][x]
                if c != None:
                    if c.character_type == Character.MONSTER:
                        c.COMBAT = wc.player.COMBAT - 1
                        num_hits += 1

            if y < WorldComponent.WORLD_HEIGHT - 1:
                c = self.characters[y+1][x]
                if c != None:
                    if c.character_type == Character.MONSTER:
                        c.COMBAT = wc.player.COMBAT - 1
                        num_hits += 1

            if x > 0:
                c = self.characters[y][x-1]
                if c != None:
                    if c.character_type == Character.MONSTER:
                        c.COMBAT = wc.player.COMBAT - 1
                        num_hits += 1

            if x < WorldComponent.WORLD_WIDTH - 1:
                c = self.characters[y][x+1]
                if c != None:
                    if c.character_type == Character.MONSTER:
                        c.COMBAT = wc.player.COMBAT - 1
                        num_hits += 1

           
            if num_hits > 0:
                    
                wc.player.action = Character.GOOD_SPELL
                sound_effect = sc.weaken_monster

            else:
                
                wc.player.action = Character.BAD_SPELL


            if num_hits == 1:

                tc.lines.append(('1 monster weakened.', BLUE))

            elif num_hits > 1:

                tc.lines.append((str(num_hits) + ' monsters weakened.', BLUE))




        elif s.code == Character.SET_TRAP:

            b = self.board[y][x]
            c = self.characters[y][x]

            if b == WorldComponent.TILE and c == None:

                self.board[y][x] = WorldComponent.TRAP

                wc.player.action = Character.GOOD_SPELL
                
                sound_effect = sc.set_trap

            else:
                
                wc.player.action = Character.BAD_SPELL


        
        elif s.code == Character.THE_KNOWN_WORLD:

            show_over = False

            tc.lines = []
            tc.lines.append(('You see the places you have been.', GREEN))

            sc.the_known_world.play()

            ic.mode = InputComponent.WITHIN_SPELL

            while show_over == False:

                gc.showKnownWorld()

                for e in pygame.event.get():

                    if e.type == QUIT:

                        pygame.quit()
                        sys.exit()

                    if e.type == KEYDOWN:

                        if e.key == K_ESCAPE:
                            show_over = True
            
            tc.lines = []  # ok to clear dialog box for this spell
            wc.player.action = None 
            
            ic.mode = None

        elif s.code == Character.INSIGHT:

            show_over = False

            tc.lines = []
            tc.lines.append(('You can see the numbers that lie underneath.', GREEN))

            sc.info.play()
            
            ic.mode = InputComponent.WITHIN_SPELL

            while show_over == False:

                gc.showInsight()

                for e in pygame.event.get():

                    if e.type == QUIT:

                        pygame.quit()
                        sys.exit()

                    if e.type == KEYDOWN:

                        if e.key == K_ESCAPE:
                            show_over = True

            tc.lines = []  # ok to clear dialog box for this spell
            wc.player.action = None 
            
            ic.mode = None


        elif s.code == Character.STATUE_LOCATOR:

            show_over = False

            tc.lines = []
            tc.lines.append(('You see the statues, your party.', GREEN))
            
            sc.locate_statues.play()
            
            ic.mode = InputComponent.WITHIN_SPELL

            while show_over == False:

                gc.showStatueLocator()

                for e in pygame.event.get():

                    if e.type == QUIT:
                        show_over = True

                    if e.type == KEYDOWN:

                        if e.key == K_ESCAPE:
                            show_over = True

            tc.lines = []  # ok to clear dialog box for this spell

            wc.player.action = None 

            ic.mode = None

        elif s.code == Character.PAINT_FLOOR:

            b = self.board[y][x]

            if b == WorldComponent.TILE:
               
                self.tile_color[y][x] = wc.player.number
                dx = 0
                dy = 0

                for i in range(35):

                    dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
                    x += dx
                    y += dy

                    if x < 0:
                       x = 0
                    if x > WorldComponent.WORLD_WIDTH - 1:
                       x = WorldComponent.WORLD_WIDTH - 1
                    if y < 0:
                       y = 0
                    if y > WorldComponent.WORLD_HEIGHT - 1:
                       y = WorldComponent.WORLD_HEIGHT - 1

                    if self.board[y][x] == WorldComponent.TILE:
                       self.tile_color[y][x] = wc.player.number
                                
                wc.player.action = Character.GOOD_SPELL

                sound_effect = sc.paint_floor

            else:
                
                wc.player.action = Character.BAD_SPELL

       

        elif s.code == Character.CRUMBLE_WALL:

            b = self.board[y][x]

            if b == WorldComponent.WALL:

                self.board[y][x] = WorldComponent.TILE

                wc.player.action = Character.GOOD_SPELL

                if y > 0:
                    if self.board[y-1][x] == WorldComponent.WALL:
                        self.board[y-1][x] = WorldComponent.TILE
                if y < WorldComponent.WORLD_HEIGHT - 1:
                    if self.board[y+1][x] == WorldComponent.WALL:
                        self.board[y+1][x] = WorldComponent.TILE
                if x > 0:
                    if self.board[y][x-1] == WorldComponent.WALL:
                        self.board[y][x-1] = WorldComponent.TILE
                if x < WorldComponent.WORLD_WIDTH - 1:
                    if self.board[y][x+1] == WorldComponent.WALL:
                        self.board[y][x+1] = WorldComponent.TILE

                sound_effect = sc.crumble
                        
            else:
                
                wc.player.action = Character.BAD_SPELL



        elif s.code == Character.POINT_TO_EXIT:
        
            
            ic.mode = InputComponent.MAIN_CONTROLS

            north = 0
            south = 0
            east = 0
            west = 0
          
            tc.lines = []
            text = 'The EXIT is:'


            dir_string = ''

            if self.exit_y < wc.player.y:
                north = wc.player.y - self.exit_y
                dir_string = ' ' + str(north) + ' spaces north,'
            else:
                south = self.exit_y - wc.player.y
                dir_string = ' ' + str(south) + ' spaces south,'
            text += dir_string

            if self.exit_x < wc.player.x:
                west = wc.player.x - self.exit_x
                dir_string = ' ' + str(west) + ' spaces west.'
            else:
                east = self.exit_x - wc.player.x
                dir_string = ' ' + str(east) + ' spaces east.'
            text += dir_string

            tc.lines.append((text, GREEN))
            gc.update()

            sc.find_exit.play()

            ic.mode = InputComponent.WITHIN_SPELL

            show_over = False

            while show_over == False:

                for e in pygame.event.get():

                    if e.type == QUIT:
                        show_over = True

                    if e.type == KEYDOWN:

                        if e.key == K_ESCAPE:
                            show_over = True

                gc.update()

            tc.lines = []  # ok to clear dialog box for this spell

            wc.player.action = None 

            ic.mode = None


        elif s.code == Character.TURN_TO_STONE:


            wc.player.status = Character.STONED

            tc.lines.append( \
                    ('This character turns to stone (impervious to', YELLOW))
            tc.lines.append( \
                    ('monster attacks). You can now select another', YELLOW))
            tc.lines.append( \
                    ('character to control.', YELLOW))

            sc.turn_to_stone.play()

            wc.player.causeFatigue(s.cost) # must call before selecting another
            ic.selectAnotherPlayer()



        # after ALL spells:
        gc.calculateLight()
        gc.update()
        
        if wc.player.action == Character.BAD_SPELL:
            sound_effect = sc.misfire

        if sound_effect != None:
            sound_effect.play()

        time.sleep(GraphicsComponent.ANIMATION_SPEED)
        wc.player.action = None
        wc.player.selected_spell = None
        wc.player.tx = 0 
        wc.player.ty = 0
        if s.code != Character.TURN_TO_STONE: 
            wc.player.causeFatigue(s.cost)
        ic.mode = InputComponent.MAIN_CONTROLS



    def update_plan(self):

        # sort by ascending COMBAT order: 56, 128, 556...
        self.character_list.sort(key=lambda c: c.COMBAT, reverse=False)

        counter = 0

        for c in self.character_list:

            if c.character_type == Character.MONSTER and \
               c.status != Character.DEAD:

                planned = False
                max_tries = 30
                failsafe = max_tries

                while planned == False and failsafe > 0:

                    roll = random.randint(1,6)

                    if wc.adjacentToPlayer(c) == True and roll > 4:

                        c.plan = Character.SWORD
                        planned = True

                    elif roll > 3:

                        c.plan = Character.WAIT
                        planned = True

                    else:

                        dx = 0
                        dy = 0

                        # plan to move monster in a random direction
                        if random.choice([0,1]) == 0:
                            dx = random.choice([-1,1])
                        else:
                            dy = random.choice([-1,1])

                        x = c.x + dx
                        y = c.y + dy

                        if self.isValidMove(x,y,c):
                            c.plan = Character.MOVE
                            c.dx = dx
                            c.dy = dy
                            planned = True
                        else:
                            failsafe -= 1

                if failsafe == 0:
                    c.plan = Character.WAIT

                # must update display after each on-screen monster has set plan 
                if gc.isCharacterVisible(c) == True:
                    gc.update() 
                    time.sleep(GraphicsComponent.ANIMATION_SPEED)

            elif c.character_type == Character.PLAYER and \
                    c.status == Character.ACTIVE:

                ic.mode = InputComponent.MAIN_CONTROLS
                ic.planning_stage_input()

                # this is the main place the dialog box should be cleared
                tc.lines = []

                gc.update() 
                time.sleep(GraphicsComponent.ANIMATION_SPEED)

            counter += 1



    def update_action(self):

        self.character_list.sort(key=lambda x: x.COMBAT, reverse=True)

        counter = 0

        for c in self.character_list:

            if c.plan == Character.MOVE:

                if self.isValidMove( c.x+c.dx, c.y+c.dy, c ):

                    self.executeMove(c)

                    if c.character_type == Character.PLAYER:

                        gc.possibleCameraMove(self.player)

            elif c.plan == Character.SWORD:

                self.swingSword(c)

            elif c.plan == Character.SPELL:

                wc.executeSpell(wc.player.selected_spell, \
                        wc.player.tx, wc.player.ty)
                wc.player.selected_spell = None

            elif c.plan == Character.WAIT:

                if gc.isCharacterVisible(c) == True:
                    sc.wait.play()

            elif c.plan == Character.SUICIDE:

                c.causeInjury(Character.MAX_INJURY) 
                

            c.plan = None
            
            if gc.isCharacterVisible(c) == True:
                # must update display after each on-screen character has acted 
                gc.update() 
                time.sleep(GraphicsComponent.ANIMATION_SPEED)
        
            counter += 1


    def swingSword(self, c):

        # inflict sword strike damage on any Character within range

        sc.swing_sword.play()

        x = c.x
        y = c.y

        if y > 0:
            i = self.characters[y-1][x]
            if i != None and i.status != Character.STONED:
                self.swordHit(c,i)

        if y < WorldComponent.WORLD_HEIGHT - 1:
            i = self.characters[y+1][x]
            if i != None and i.status != Character.STONED:
                self.swordHit(c,i)

        if x > 0:
            i = self.characters[y][x-1]
            if i != None and i.status != Character.STONED:
                self.swordHit(c,i)

        if x < WorldComponent.WORLD_WIDTH - 1:
            i = self.characters[y][x+1]
            if i != None and i.status != Character.STONED:
                self.swordHit(c,i)

    def swordHit(self, c, i):

        i.causeInjury(Character.SWORD_DAMAGE) 

        if c.character_type == Character.PLAYER:
            c.earnXP()
            if i.status == Character.DEAD:
                if i.COMBAT > c.COMBAT:
                    c.earnXP()
                    c.earnXP()
                else:
                    c.earnXP()

    def countRemainingPlayers(self):

        num_alive = 0
        for a in wc.player_list:
            if a.status != Character.DEAD and a.status != Character.ESCAPED:
                num_alive += 1

        return num_alive

    def isGameOver(self):
    
        # This function will count the number of remaining players still
        # alive and in the dungeon. 

        result = True 

        num_alive = self.countRemainingPlayers()

        if num_alive > 0:

            if num_alive > 1:
                tc.lines.append(('There are still ' + str(num_alive) + \
                        ' party members alive in the', BLUE))
                tc.lines.append(('dungeon.', BLUE))
            else:
                tc.lines.append(('There is still ' + str(num_alive) + \
                        ' party member alive in the', BLUE))
                tc.lines.append(('dungeon.', BLUE))

            result = False 

        return result


    def escapeDungeon(self, c):

        c.status = Character.ESCAPED
        c.plan = None
        c.action = None

        sc.exit.play()

        self.winners_circle.append(c)

        self.calculateScore()

        self.characters[c.y][c.x] = None

        if c.character_type == Character.PLAYER:

            if self.isGameOver() == False:

                ic.selectAnotherPlayer()

            else:

                self.gameOver()

        gc.update()


    def characterDeath(self, c):

        c.status = Character.DEAD
        c.plan = None
        c.action = None

        self.characters[c.y][c.x] = None

        self.board[c.y][c.x] = WorldComponent.TILE_DEAD_BODY
        gc.update()
        time.sleep(GraphicsComponent.ANIMATION_SPEED)

        if c.character_type == Character.PLAYER:
            if self.isGameOver() == False:
                ic.selectAnotherPlayer()
            else:
                self.gameOver()

        # recalculate score if monster death
        if c.character_type == Character.MONSTER:
            
            self.monsters_killed += 1

            tc.lines = []
            tc.lines.append(('Total monsters now slain: ' + \
                str(wc.monsters_killed) + '.', BLUE))


            if self.monsters_killed >= WorldComponent.MONSTERS_NEEDED_FOR_EXIT:

                tc.lines.append((\
                    'Monster requirement satisfied.', BLUE))
                #sc.exit_unlocked.play()
                wc.attemptToUnlockExit()

            self.calculateScore()



    def gameOver(self):

        # if you reached this, there are no other adventurers alive in the
        # dungeon.
        # if any have escaped and you aren't on the last level, you can go to 
        # the next level!

        sc.game_over.play()

        sc.play_exit_music()
            
        gc.mainSurface.fill(BLACK)
        x = 18 
        y = 5 

        num_escaped = len(self.winners_circle)

        if num_escaped > 0 and wc.level != WorldComponent.END_LEVEL:

            wc.nextLevel = True

        else:

            tp.add_text('Game Over', ORANGE, x, y)
            tp.add_text('There are no other members of your party', ORANGE, x, y+2)
            tp.add_text('left alive in the dungeon.', ORANGE, x, y+3)

            if num_escaped > 0 and wc.level == WorldComponent.END_LEVEL:

                tp.add_text('*** You have won the game! ***', GREEN, x+4, y+5)
                tp.add_text('*** You have won the game! ***', GREEN, x+4, y+6)
                tp.add_text('*** You have won the game! ***', GREEN, x+4, y+7)
            
            tp.add_text('c = Current level: ' + str(wc.level - 1), \
                    BLUE, x+4, y+9)

            tp.add_text('m = Monsters slain: ' + str(wc.monsters_killed), \
                    BLUE, x+4, y+11)
            
            tp.add_text('k = Keys collected: ' + str(wc.keys_collected), \
                    BLUE, x+4, y+13)


            tp.add_text('FINAL SCORE (m + k) * c = ' + str(wc.score), ORANGE, x+4, y+16)

            tp.add_text('Hit [ESC] to Quit Program.', RED, x, y+19)

            pygame.display.update()

            done = False

            while done == False:

                for e in pygame.event.get():

                    if e.type == QUIT:

                        pygame.quit()
                        sys.exit()

                    elif e.type == KEYDOWN:

                        if e.key == K_ESCAPE:
                            
                            pygame.quit()
                            sys.exit()
            
                gc.clock.tick(gc.FPS)

            pygame.quit()
            sys.exit()

    def levelTitlePage(self):

        sc.play_exit_music()
            
        gc.mainSurface.fill(BLACK)
        x = 10 
        y = 5 

        if wc.level != WorldComponent.END_LEVEL + 1:
         
            tp.add_text('* Level ' + str(wc.level - 1) + ' *', ORANGE, x+25, y)

            if wc.level == WorldComponent.END_LEVEL:
                tp.add_text('(last level!)', RED, x+24, y+2)

            tp.add_text( \
                    'Get as many party members through the EXIT as possible', \
                    ORANGE, x+3, y+4)
          
            tp.add_text('Need ' + \
                    str(WorldComponent.KEYS_NEEDED_FOR_EXIT) + \
                    ' keys to unlock next EXIT', GREEN, x+14, y+8)
            tp.add_text('Need ' + \
                    str(WorldComponent.MONSTERS_NEEDED_FOR_EXIT) + \
                    ' monsters dead to unlock next EXIT', GREEN, x+11, y+10)

            tp.add_text('Hit any key to continue.', RED, x, y+20)
            pygame.display.update()

            pygame.key.set_repeat()
           
            done = False

            while done == False:

                for e in pygame.event.get():

                    if e.type == QUIT:

                        pygame.quit()
                        sys.exit()

                    elif e.type == KEYDOWN:

                        done = True
                        sc.stop_music()
                        pygame.key.set_repeat(1,100)
            
                gc.clock.tick(gc.FPS)

        else:

            self.gameOver()
    

class GraphicsComponent:

    # needs access to WorldComponent
    global wc
    global sc
    
    # animation speed
    ANIMATION_SPEED  = 0.1


    def __init__(self):

        self.CAMERA_WIDTH = 9
        self.CAMERA_HEIGHT = 9
        self.CAMERA_MOVE_UP = 1
        self.CAMERA_MOVE_DOWN = 7
        self.CAMERA_MOVE_LEFT = 1
        self.CAMERA_MOVE_RIGHT = 7
        self.CAMERA_MAX_X = wc.WORLD_WIDTH - self.CAMERA_WIDTH
        self.CAMERA_MAX_Y = wc.WORLD_HEIGHT - self.CAMERA_HEIGHT
        self.mainSurface = pygame.display.set_mode((800,600))
        pygame.display.set_caption('Monstrosity')
        self.clock = pygame.time.Clock()

        self.sprite_player = \
                pygame.image.load(resource_path('images\\player.png'))
        self.sprite_monster = \
        pygame.image.load(resource_path('images\\monster.png'))
        self.sprite_statue = \
        pygame.image.load(resource_path('images\\statue.png'))
        
        self.sprite_tile = pygame.image.load(resource_path('images\\tile.png'))
        self.sprite_tile_dead_body = \
        pygame.image.load(resource_path('images\\tile_dead_body.png'))
        self.sprite_wall = pygame.image.load(resource_path('images\\wall.png'))
        self.sprite_door_closed = \
        pygame.image.load(resource_path('images\\door_closed.png'))
        self.sprite_door_open = \
        pygame.image.load(resource_path('images\\door_open.png'))
        self.sprite_exit = pygame.image.load(resource_path('images\\exit.png'))
       
        self.sprite_move = pygame.image.load(resource_path('images\\move.png'))
        self.sprite_move_n =  pygame.transform.rotate(self.sprite_move,0)
        self.sprite_move_w =  pygame.transform.rotate(self.sprite_move,90)
        self.sprite_move_e =  pygame.transform.rotate(self.sprite_move,270)
        self.sprite_move_s =  pygame.transform.rotate(self.sprite_move,180)
        self.sprite_sword = pygame.image.load(resource_path('images\\sword.png'))
        self.sprite_cast = pygame.image.load(resource_path('images\\cast.png'))
        self.sprite_wait = pygame.image.load(resource_path('images\\wait.png'))
        self.sprite_trap = pygame.image.load(resource_path('images\\trap.png'))
        self.sprite_key = pygame.image.load(resource_path('images\\key.png'))
        
        self.sprite_hit = pygame.image.load(resource_path('images\\hit.png'))
        self.sprite_poof = pygame.image.load(resource_path('images\\poof.png'))

        self.rects = self.constructRectsArray() 
        self.camera_x = 0
        self.camera_y = 0
        self.FPS = 30

        self.orientCameraOnPlayer(wc.player.x, wc.player.y)

        self.animation_speed = 1
        GraphicsComponent.ANIMATION_SPEED = (0.1 * self.animation_speed) - 0.1 


    def calculateLight(self):

        total = self.CAMERA_HEIGHT * self.CAMERA_WIDTH
        
        for t in range(10): # this seems to be good enough, not 81 times

            for r in range(self.CAMERA_HEIGHT):
                for c in range(self.CAMERA_WIDTH):

                    u = wc.light[r+self.camera_y][c+self.camera_x] 
                    b = wc.board[r+self.camera_y][c+self.camera_x]

                    if u == True and b != WorldComponent.WALL and \
                            b != WorldComponent.DOOR_STUCK and \
                            b != WorldComponent.DOOR_HELD:

                        if r > 0:
                            wc.light[r-1+self.camera_y][c+self.camera_x] = True

                        if r < self.CAMERA_HEIGHT - 1:
                            wc.light[r+1+self.camera_y][c+self.camera_x] = True

                        if c > 0:
                            wc.light[r+self.camera_y][c-1+self.camera_x] = True

                        if c < self.CAMERA_WIDTH - 1:
                            wc.light[r+self.camera_y][c+1+self.camera_x] = True

         
    def toggleAnimationSpeed(self):

        self.animation_speed -= 1

        if self.animation_speed == 0:

            self.animation_speed = 3

        GraphicsComponent.ANIMATION_SPEED = (0.1 * self.animation_speed) - 0.1 

        if self.animation_speed == 1:

            text = 'Fast animation speed (for expert players)'

        elif self.animation_speed == 2:

            text = 'Medium animation speed (for advanced players)'

        else:

            text = 'Slow animation speed (for beginner players)'



    def orientCameraOnPlayer(self, player_x, player_y): 
    
        self.camera_x = player_x - int(self.CAMERA_WIDTH / 2.0)
        self.camera_y = player_y - int(self.CAMERA_HEIGHT / 2.0)

        if self.camera_x < 0:
            self.camera_x = 0
        elif self.camera_x > self.CAMERA_MAX_X:
            self.camera_x = self.CAMERA_MAX_X
        if self.camera_y < 0:
            self.camera_y = 0
        elif self.camera_y > self.CAMERA_MAX_Y:
            self.camera_y = self.CAMERA_MAX_Y


   
    def constructRectsArray(self):
        rects = [] 
        row = []
        insert_x = 16 
        insert_y = 30 
        for r in range(9):
            for c in range(9):
                temp = pygame.Rect(insert_x, insert_y, 51, 51)
                row.append(temp)
                insert_x += 51 + 3 
            rects.append(row)
            row = []
            insert_y += 51 + 3 
            insert_x = 16 

        return rects

    def possibleCameraMove(self, c):

        x = c.x
        y = c.y

        if y == (self.camera_y + self.CAMERA_MOVE_UP) and \
            self.camera_y > 0:
                self.camera_y -= 1
                self.calculateLight()

        elif y == (self.camera_y + self.CAMERA_MOVE_DOWN) and \
            self.camera_y < self.CAMERA_MAX_Y:
                self.camera_y += 1
                self.calculateLight()
                
        elif x == (self.camera_x + self.CAMERA_MOVE_RIGHT) and \
            self.camera_x < self.CAMERA_MAX_X:
                self.camera_x += 1
                self.calculateLight()
                    
        elif x == (self.camera_x + self.CAMERA_MOVE_LEFT) and \
            self.camera_x > 0: 
                self.camera_x -= 1
                self.calculateLight()



    def isCharacterVisible(self, c):

        x = c.x
        y = c.y

        if y >= (self.camera_y) and y < (self.camera_y + self.CAMERA_HEIGHT):
            
            if x >= (self.camera_x) and x < (self.camera_x + self.CAMERA_WIDTH):

                if wc.light[y][x] == True:

                    return True

    def isGlobalCoordinateVisible(self, x, y):

        if y >= (self.camera_y) and y < (self.camera_y + self.CAMERA_HEIGHT):
            
            if x >= (self.camera_x) and x < (self.camera_x + self.CAMERA_WIDTH):

                return True


    
    def monstersAreVisible(self):

        # used to detect if an encounter is occurring

        result = False

        for r in range(self.CAMERA_HEIGHT):

            for c in range(self.CAMERA_WIDTH):

                i = wc.characters[r+self.camera_y][c+self.camera_x] 

                if i != None:

                    if i.character_type == Character.MONSTER and \
                        wc.light[r+self.camera_y][c+self.camera_x] == True:

                        result = True

        return result



    def showInsight(self):

        # call tc.update() to draw everything but the graphics area
        self.mainSurface.fill( (0,0,0) )
        tc.mode_player_select = False
        tc.mode_spell_select = False
        tc.mode_controls_select = False
        tc.update()    
        
        # calling tc.add_text draws on tc.text_surface only
        TEXT_X = 6
        TEXT_Y = 3
        tc.add_text('Level: ' + str(wc.level-1),
                GREEN, TEXT_X, TEXT_Y)
        
        tc.add_text('Number of keys to unlock EXIT: ' + \
                str(WorldComponent.KEYS_NEEDED_FOR_EXIT),
                GREEN, TEXT_X, TEXT_Y+3)
        tc.add_text('Monster kills to unlock EXIT: ' + \
                str(WorldComponent.MONSTERS_NEEDED_FOR_EXIT),
                GREEN, TEXT_X, TEXT_Y+2)


        tc.add_text('Dungeon width (blocks): ' + str(WorldComponent.WORLD_WIDTH),
                GREEN, TEXT_X, TEXT_Y+5)
        tc.add_text('Dungeon height (blocks): ' + str(WorldComponent.WORLD_HEIGHT),
                GREEN, TEXT_X, TEXT_Y+6)
        tc.add_text('Total area of dungeon: ' + \
                str(WorldComponent.WORLD_WIDTH * WorldComponent.WORLD_HEIGHT),
                GREEN, TEXT_X, TEXT_Y+7)
       
        n_keys = 0
        for r in range(WorldComponent.WORLD_HEIGHT):
            for c in range(WorldComponent.WORLD_WIDTH):
                if wc.board[r][c] == WorldComponent.KEY:
                    n_keys += 1

        n_monsters = 0
        for m in wc.character_list:
            if m != None and m.character_type == Character.MONSTER and \
                    m.status != Character.DEAD:
                n_monsters += 1

        tc.add_text('Keys remaining on this level: ' + str(n_keys),
                GREEN, TEXT_X, TEXT_Y+10)
        tc.add_text('Monsters remaining on this level: ' + \
                str(n_monsters),
                GREEN, TEXT_X, TEXT_Y+9)

        tc.add_text('Score: ' + str(wc.score),
                GREEN, TEXT_X, TEXT_Y+12)

        # must manually blit text_surface again to mainSurface
        gc.mainSurface.blit(tc.text_surface, (0,0))

        # draw a box around the graphics area
        start_x = 50
        start_y = 50
        cell_w = 3
        cell_h = 3
        gap = 1
        space = cell_w + gap
        pygame.draw.rect(self.mainSurface, GREEN,
                (start_x-space-space, start_y-space-space, 
                    (space*97 + (space*4)),
                    (space*97 + (space*4))), 2)

        # show mainSurface
        pygame.display.update()
    
        self.clock.tick(self.FPS)
        

    def showKnownWorld(self):

        self.mainSurface.fill( (0,0,0) )

        tc.mode_player_select = False
        tc.mode_spell_select = False
        tc.mode_controls_select = False
        
        tc.update()    

        start_x = 50
        start_y = 50

        cell_w = 3
        cell_h = 3

        gap = 1

        space = cell_w + gap

        pygame.draw.rect(self.mainSurface, GREEN,
                (start_x-space-space, start_y-space-space, 
                    (space*wc.WORLD_WIDTH + (space*4)),
                    (space*wc.WORLD_HEIGHT + (space*4))), 2)

        for r in range(wc.WORLD_HEIGHT):
            for c in range(wc.WORLD_WIDTH):

                if wc.light[r][c] == True and wc.characters[r][c] == None:

                    if wc.board[r][c] == WorldComponent.TILE:
                        pygame.draw.rect(self.mainSurface, (102,102,102), 
                                (start_x, start_y, cell_w, cell_h))
                    
                    if wc.tile_color[r][c] != 0:
                        for p in wc.player_list:
                            if p.number == wc.tile_color[r][c]:
                                pygame.draw.rect(self.mainSurface, p.color, 
                                    (start_x, start_y, cell_w, cell_h))

                # draw current player white
                if wc.player.x == c and wc.player.y == r:
                    pygame.draw.rect(self.mainSurface, WHITE, 
                            (start_x, start_y, cell_w, cell_h))
                    pygame.draw.rect(self.mainSurface, WHITE, 
                        (start_x-space, start_y, cell_w, cell_h))
                    pygame.draw.rect(self.mainSurface, WHITE, 
                        (start_x+space, start_y, cell_w, cell_h))
                    pygame.draw.rect(self.mainSurface, WHITE,
                        (start_x, start_y-space, cell_w, cell_h))
                    pygame.draw.rect(self.mainSurface, WHITE, 
                        (start_x, start_y+space, cell_w, cell_h))

                start_x += (cell_w+gap)

            start_y += (cell_h+gap)
            start_x = 50
            
        pygame.display.update()
    
        self.clock.tick(self.FPS)


    def showStatueLocator(self):

        self.mainSurface.fill( (0,0,0) )
       
        tc.mode_player_select = False
        tc.mode_spell_select = False
        tc.mode_controls_select = False
        
        tc.update()    

        start_x = 50
        start_y = 50

        cell_w = 3
        cell_h = 3

        gap = 1

        space = cell_w + gap

        pygame.draw.rect(self.mainSurface, GREEN,
                (start_x-space-space, start_y-space-space, 
                    (space*wc.WORLD_WIDTH + (space*4)),
                    (space*wc.WORLD_HEIGHT + (space*4))), 2)

        for r in range(wc.WORLD_HEIGHT):
            for c in range(wc.WORLD_WIDTH):

                # draw statues
                for s in wc.player_list:
                    if s.x == c and s.y == r and s.status != Character.DEAD:
                        pygame.draw.rect(self.mainSurface, s.color, 
                            (start_x, start_y, cell_w, cell_h))
                        pygame.draw.rect(self.mainSurface, s.color, 
                            (start_x-space, start_y, cell_w, cell_h))
                        pygame.draw.rect(self.mainSurface, s.color, 
                            (start_x+space, start_y, cell_w, cell_h))
                        pygame.draw.rect(self.mainSurface, s.color, 
                            (start_x, start_y-space, cell_w, cell_h))
                        pygame.draw.rect(self.mainSurface, s.color, 
                            (start_x, start_y+space, cell_w, cell_h))

                        if s == wc.player:
                            pygame.draw.rect(self.mainSurface, s.color, 
                                (start_x, start_y - (space*3), cell_w, cell_h))
                            pygame.draw.rect(self.mainSurface, s.color, 
                                (start_x, start_y + (space*3), cell_w, cell_h))
                            pygame.draw.rect(self.mainSurface, s.color, 
                                (start_x - (space*3), start_y, cell_w, cell_h))
                            pygame.draw.rect(self.mainSurface, s.color, 
                                (start_x + (space*3), start_y, cell_w, cell_h))


                start_x += (cell_w+gap)

            start_y += (cell_h+gap)
            start_x = 50
        
        pygame.display.update()
    
        self.clock.tick(self.FPS)
  

    def update(self):

        self.mainSurface.fill( (0,0,0) )

        tc.update()    

        for r in range(self.CAMERA_HEIGHT):
            for c in range(self.CAMERA_WIDTH):

                if wc.light[r+self.camera_y][c+self.camera_x] == True: 
    
                    x,y = self.rects[r][c].topleft
                   
                    # draw first-layer, the gameboard
                    if wc.board[r+self.camera_y][c+self.camera_x] == WorldComponent.TILE:
                        self.mainSurface.blit(self.sprite_tile, (x,y))
                    elif wc.board[r+self.camera_y][c+self.camera_x] == WorldComponent.WALL:
                        self.mainSurface.blit(self.sprite_wall, (x,y))
                    elif wc.board[r+self.camera_y][c+self.camera_x] == \
                        WorldComponent.DOOR_STUCK:
                        self.mainSurface.blit(self.sprite_door_closed, (x,y))
                    elif wc.board[r+self.camera_y][c+self.camera_x] == \
                        WorldComponent.DOOR_OPEN:
                        self.mainSurface.blit(self.sprite_door_open, (x,y))
                    elif wc.board[r+self.camera_y][c+self.camera_x] == \
                        WorldComponent.DOOR_HELD:
                        self.mainSurface.blit(self.sprite_door_closed, (x,y))
                    elif wc.board[r+self.camera_y][c+self.camera_x] == \
                        WorldComponent.EXIT:
                        self.mainSurface.blit(self.sprite_exit, (x,y))
                    elif wc.board[r+self.camera_y][c+self.camera_x] == \
                        WorldComponent.TILE_DEAD_BODY:
                        self.mainSurface.blit(self.sprite_tile_dead_body, (x,y))
                    elif wc.board[r+self.camera_y][c+self.camera_x] == \
                        WorldComponent.TRAP:
                        self.mainSurface.blit(self.sprite_trap, (x,y))
                    elif wc.board[r+self.camera_y][c+self.camera_x] == \
                        WorldComponent.KEY:
                        self.mainSurface.blit(self.sprite_key, (x,y))

                    # draw magically painted flooring
                    cc = wc.tile_color[r+self.camera_y][c+self.camera_x]  
                    if cc != 0:
                        for p in wc.player_list:
                            if p.number == cc:
                                pygame.draw.rect(self.mainSurface, p.color, \
                                    self.rects[r][c], 0)

                    # for each on-screen character, draw their image, plus any
                    # current plan (such as "swing sword", "wait", "cast spell")
                    i = wc.characters[r+self.camera_y][c+self.camera_x] 
                    if i != None:

                        # draw character image
                        if i.character_type == Character.MONSTER:
                            self.mainSurface.blit(self.sprite_monster, (x,y))
                        else:
                            if i.status == Character.ACTIVE:
                                self.mainSurface.blit(self.sprite_player, (x,y))
                                pygame.draw.rect(self.mainSurface, wc.player.color, \
                                    self.rects[r][c], 2)
                            elif i.status == Character.STONED:
                                self.mainSurface.blit(self.sprite_statue, (x,y))


                        # draw their planned next move
                        if i.plan == Character.MOVE:
                            if i.dy == -1:
                                self.mainSurface.blit(self.sprite_move_n, (x,y))
                            elif i.dy == 1:
                                self.mainSurface.blit(self.sprite_move_s, (x,y))
                            elif i.dx == -1:
                                self.mainSurface.blit(self.sprite_move_w, (x,y))
                            elif i.dx == 1:
                                self.mainSurface.blit(self.sprite_move_e, (x,y))
                        elif i.plan == Character.SWORD:
                            self.mainSurface.blit(self.sprite_sword, (x,y))
                        elif i.plan == Character.WAIT:
                            self.mainSurface.blit(self.sprite_wait, (x,y))
                        elif i.plan == Character.SPELL:
                            self.mainSurface.blit(self.sprite_cast, (x,y))
                      

                        # draw any current action occurring:
                        if i.action == Character.BLOODBURST:
                            self.mainSurface.blit(self.sprite_hit, (x,y))
                        elif i.action == Character.GOOD_SPELL:
                            x,y = \
                 self.rects[wc.player.ty-self.camera_y][wc.player.tx-self.camera_x].topleft
                            self.mainSurface.blit(self.sprite_cast, (x,y))
                        elif i.action == Character.BAD_SPELL:
                            x,y = \
                 self.rects[wc.player.ty-self.camera_y][wc.player.tx-self.camera_x].topleft
                            self.mainSurface.blit(self.sprite_poof, (x,y))


                # draw targeting square if it is currently enabled
                spell = wc.player.selected_spell
                if spell != None and spell.target_needed == True and \
                        ic.mode == InputComponent.TARGETING:

                    if wc.player.tx == c + self.camera_x and \
                        wc.player.ty == r + self.camera_y:

                        pygame.draw.rect(self.mainSurface, GREEN, \
                            self.rects[r][c], 4)

        
        pygame.display.update()

        self.clock.tick(self.FPS)



class InputComponent:

    # needs access to WorldComponent and GraphicsComponent
    global wc
    global gc
    global tc
    global sc

    #enums for modes
    MAIN_CONTROLS      = 0
    SPELL_SELECTION    = 1
    TARGETING          = 2
    CONFIRM_QUIT       = 3
    CHOOSE_PLAYER      = 4
    HELP_SYSTEM        = 5
    WITHIN_SPELL       = 6
    CONFIRM_SUICIDE    = 7

    def __init__(self):

        self.mode = InputComponent.MAIN_CONTROLS


    def getAnyKey(self):

        done = False

        while done == False:

            for e in pygame.event.get():

                if e.type == QUIT:

                    pygame.quit()
                    sys.exit()

                elif e.type == KEYDOWN:

                    done = True

            gc.clock.tick(gc.FPS)

        return done


    def planning_stage_input(self):

        plan_made = False

        while plan_made == False:

            
            if self.mode == InputComponent.MAIN_CONTROLS:

                mode_complete = False

                while mode_complete == False:

                    for e in pygame.event.get():

                        if e.type == QUIT:

                            pygame.quit()
                            sys.exit()

                        elif e.type == KEYDOWN:

                            if e.key == K_UP:
                                if wc.isValidMove(wc.player.x, wc.player.y - 1,
                                        wc.player):
                                    wc.playerPlanMove(0,-1)
                                    plan_made = True
                                    mode_complete = True

                            elif e.key == K_DOWN:
                                if wc.isValidMove(wc.player.x, wc.player.y + 1,
                                        wc.player):
                                    wc.playerPlanMove(0,1)
                                    plan_made = True
                                    mode_complete = True
                                
                            elif e.key == K_RIGHT:
                                if wc.isValidMove(wc.player.x + 1, wc.player.y,
                                        wc.player):
                                    wc.playerPlanMove(1,0)
                                    plan_made = True
                                    mode_complete = True
                                    
                            elif e.key == K_LEFT:
                                if wc.isValidMove(wc.player.x - 1, wc.player.y,
                                        wc.player):
                                    wc.playerPlanMove(-1,0)
                                    plan_made = True
                                    mode_complete = True
                            
                            elif e.key == K_s:
                
                                wc.player.plan = Character.SWORD
                                plan_made = True
                                mode_complete = True
                                
                            elif e.key == K_w:
                
                                wc.player.plan = Character.WAIT
                                plan_made = True
                                mode_complete = True

                            elif e.key == K_i:
                                
                                self.mode = InputComponent.CONFIRM_SUICIDE  
                                #plan_made = True
                                mode_complete = True

                            elif e.key == K_c:
                                
                                self.mode = InputComponent.SPELL_SELECTION
                                mode_complete = True

                            elif e.key == K_f:
                                
                                self.mode = InputComponent.HELP_SYSTEM
                                mode_complete = True

                            elif e.key == K_b:
                                
                                if tc.blink_feature_on == True:
                                    tc.blink_feature_on = False
                                    tc.lines.append( \
                             ('Blinking Lights feature is now off.', YELLOW))
                                else:
                                    tc.blink_feature_on = True
                                    tc.lines.append( \
                             ('Blinking Lights feature is now on.', YELLOW))

                                mode_complete = True
                            
                            elif e.key == K_ESCAPE:

                                self.mode = InputComponent.CONFIRM_QUIT  
                                mode_complete = True

                    gc.update() 


   
            elif self.mode == InputComponent.HELP_SYSTEM:

                mode_complete = False

                sc.play_help_music()
               
                while mode_complete == False:

                    hs.showPage()

                    for e in pygame.event.get():

                        if e.type == QUIT:

                            pygame.quit()
                            sys.exit()

                        elif e.type == KEYDOWN:

                            if e.key == K_SPACE:

                                hs.nextPage()

                            elif e.key == K_ESCAPE:

                                self.mode = InputComponent.MAIN_CONTROLS
                                mode_complete = True
                                sc.stop_music()


            
            
            elif self.mode == InputComponent.SPELL_SELECTION:

                gc.update()

                wc.player.selected_spell = None
                
                mode_complete = False

                while mode_complete == False:

                    for e in pygame.event.get():

                        if e.type == QUIT:

                            pygame.quit()
                            sys.exit()

                        elif e.type == KEYDOWN:

                            if (e.key == K_1 or e.key == K_2 or e.key == K_3 or
                                    e.key == K_4 or e.key == K_5 or e.key == K_6 or
                                    e.key == K_7 or e.key == K_8) \
                                            and wc.player.selected_spell == None:

                                num = 0

                                if e.key == K_1:
                                    num = 1
                                elif e.key == K_2:
                                    num = 2
                                elif e.key == K_3:
                                    num = 3
                                elif e.key == K_4:
                                    num = 4
                                elif e.key == K_5:
                                    num = 5
                                elif e.key == K_6:
                                    num = 6
                                elif e.key == K_7:
                                    num = 7
                                elif e.key == K_8:
                                    num = 8
                                
                                if num <= len(wc.player.spellbook) and num > 0:
                                   
                                    wc.player.selected_spell = wc.player.spellbook[num-1]
                                         
                                    if wc.player.selected_spell.target_needed == True:
                            
                                        self.mode = InputComponent.TARGETING  
                                        mode_complete = True

                                    else:
                                            
                                        mode_complete = True
                                        plan_made = True
                                        wc.player.plan = Character.SPELL

                            if e.key == K_ESCAPE:

                                self.mode = InputComponent.MAIN_CONTROLS
                                mode_complete = True

                    gc.update()  # don't want to rev CPU


            elif self.mode == InputComponent.CONFIRM_SUICIDE:

                gc.update()
                
                result = False
           
                mode_complete = False

                while mode_complete == False:

                    for e in pygame.event.get():

                        if e.type == QUIT:

                            pygame.quit()
                            sys.exit()

                        elif e.type == KEYDOWN:

                            if e.key == K_y:

                                result = True
                                mode_complete = True
                                plan_made = True

                            elif e.key == K_n:

                                result = False 
                                mode_complete = True

                    gc.update()


                if result == True:

                    wc.player.plan = Character.SUICIDE

                else:
                    
                    self.mode = InputComponent.MAIN_CONTROLS
                    mode_complete = True
           

            elif self.mode == InputComponent.CONFIRM_QUIT:

                gc.update()
                
                result = False
           
                mode_complete = False

                while mode_complete == False:

                    for e in pygame.event.get():

                        if e.type == QUIT:

                            pygame.quit()
                            sys.exit()

                        elif e.type == KEYDOWN:

                            if e.key == K_y:

                                result = True
                                mode_complete = True

                            elif e.key == K_n:

                                result = False 
                                mode_complete = True

                    gc.update()


                if result == True:

                    wc.calculateScore()

                    tc.lines.append(('', BLACK))
                    tc.lines.append(('FINAL SCORE: ' + str(wc.score), VIOLET))
                    tc.lines.append(('<hit any key to exit>', VIOLET))
                    gc.update()

                    ic.getAnyKey()
                    pygame.quit()
                    sys.exit()

                else:
                    
                    self.mode = InputComponent.MAIN_CONTROLS
                    mode_complete = True


            elif self.mode == InputComponent.TARGETING:

                tc.lines = []
                tc.lines.append( \
                ('Casting ' + wc.player.selected_spell.name + '.', \
                  GREEN))
                gc.update()

                wc.player.tx = wc.player.x
                wc.player.ty = wc.player.y

                mode_complete = False

                while mode_complete == False:

                    for e in pygame.event.get():

                        if e.type == QUIT:

                            pygame.quit()
                            sys.exit()

                        if e.type == KEYDOWN:
                
                            if (e.key == K_UP):

                                if gc.isGlobalCoordinateVisible( \
                                        wc.player.tx,
                                        wc.player.ty - 1):
                                    wc.player.ty -= 1

                            elif (e.key == K_DOWN):

                                if gc.isGlobalCoordinateVisible( \
                                        wc.player.tx,
                                        wc.player.ty + 1):
                                    wc.player.ty += 1

                            elif (e.key == K_RIGHT):
                                
                                if gc.isGlobalCoordinateVisible( \
                                        wc.player.tx + 1,
                                        wc.player.ty):
                                    wc.player.tx += 1

                            elif (e.key == K_LEFT):

                                if gc.isGlobalCoordinateVisible( \
                                        wc.player.tx - 1,
                                        wc.player.ty):
                                    wc.player.tx -= 1

                            elif e.key == K_RETURN:

                                mode_complete = True
                                wc.player.plan = Character.SPELL
                                plan_made = True

                            elif e.key == K_ESCAPE:

                                ic.mode = InputComponent.SPELL_SELECTION
                                mode_complete = True

                    gc.update()   # don't want to rev cpu    



    def selectAnotherPlayer(self):

        # This function assumes there IS another player to choose, one that
        # is: 1. in the dungeon still and 2. not dead

        # Once a player is selected, wc.player will be updated, as well as
        # the camera centered on this new player. Function returns True

        # The user may decide to abort choosing another player, by hitting
        # the window-close button, or hitting ESC during the selection
        # process. This function sets game_over and returns a False value.
        
        ic.mode = InputComponent.CHOOSE_PLAYER
            
        gc.update()

        player_selected = None 

        while player_selected == None:

            for e in pygame.event.get():

                if e.type == QUIT:

                    pygame.quit()
                    sys.exit()

                elif e.type == KEYDOWN:

                    if (e.key == K_1 or e.key == K_2 or e.key == K_3 or
                            e.key == K_4 or e.key == K_5 or e.key == K_6):

                        num = 0

                        if e.key == K_1:
                            num = 1
                        elif e.key == K_2:
                            num = 2
                        elif e.key == K_3:
                            num = 3
                        elif e.key == K_4:
                            num = 4
                        elif e.key == K_5:
                            num = 5
                        elif e.key == K_6:
                            num = 6
                        
                        for c in wc.player_list:
                            if num == c.number:
                                if c.status == Character.DEAD:
                                    tc.lines = []
                                    tc.lines.append( \
                          ('Select a character that is still alive.', RED))
                                    gc.update()
                                elif c.status == Character.ESCAPED:
                                    tc.lines = []
                                    tc.lines.append( \
                          ('Select a character that is still in dungeon.', GREEN))
                                    gc.update()
                                elif c.number == wc.player.number:
                                    num_left = wc.countRemainingPlayers()
                                    if num_left > 1:
                                        tc.lines = []
                                        tc.lines.append( \
                          ('You cannot switch control to the same player.', GREEN))
                                        gc.update()
                                    else:
                                        player_selected = c
                                else:
                                    player_selected = c
                            
            gc.update() # don't want to rev CPU 


        # lots of work to do!
        wc.player = player_selected
        if wc.player.FATIGUE >= Character.MAX_FATIGUE:
            wc.player.FATIGUE = 0
        wc.player.status = Character.ACTIVE
        tc.lines = []
        tc.lines.append( \
        ('Control switched to ' + wc.player.name + '.', YELLOW))
        sc.transfer.play()
        ic.mode = InputComponent.MAIN_CONTROLS
        wc.light[wc.player.y][wc.player.x] = True
        
        gc.orientCameraOnPlayer(wc.player.x, wc.player.y)
        gc.calculateLight()
        gc.update()
        return True
                        

class Character:

    # enums for character_type
    MONSTER    = 0
    PLAYER     = 1

    # enums for status
    STONED     = 0
    ESCAPED    = 1
    ACTIVE     = 2
    DEAD       = 3

    # enums for plan
    MOVE       = 0
    SWORD      = 1
    WAIT       = 2
    SPELL      = 3
    SUICIDE    = 4

    # enums for action
    BLOODBURST = 0
    GOOD_SPELL = 1
    BAD_SPELL  = 2

    # enums for variable weapon damage
    SWORD_DAMAGE = 4

    # enums for spell list ('code')
    TURN_TO_STONE   = 0 
    OPEN_DOOR       = 1
    WEAKEN_MONSTER  = 2
    CRUMBLE_WALL    = 3
    PAINT_FLOOR     = 4
    POINT_TO_EXIT   = 5
    STATUE_LOCATOR  = 6
    THE_KNOWN_WORLD = 7 
    INSIGHT         = 8
    SET_TRAP        = 9

    MAX_FATIGUE = 50
    MAX_INJURY  = 20

    MAX_INJURY_MONSTER = 10

    def __init__(self, t, n):

        self.character_type = t  # (example: Character.MONSTER)

        self.x = 0
        self.y = 0
        self.COMBAT   = random.randint(1,999)
        self.FATIGUE  = 0
        self.INJURIES = 0

        self.status = Character.STONED
        
        self.color = WHITE 
        self.number = n
        self.name = 'Blank'

        # the following are set during the Planning Stage 
        self.plan = None
        self.dx = 0
        self.dy = 0
        self.selected_spell = None
        self.tx = 0
        self.ty = 0
       
        # the following are set during the Action Stage 
        self.action = None

        # fill spellbook with all spells
        self.spellbook = []
        self.spellbook.append(
                Spell('Open Door', Character.OPEN_DOOR, 3, True))
        self.spellbook.append(
                Spell('Weaken Monster', Character.WEAKEN_MONSTER, 3, True))
        self.spellbook.append(
                Spell('Crumble Wall', Character.CRUMBLE_WALL, 6, True))
        self.spellbook.append(
                Spell('Paint Floor', Character.PAINT_FLOOR, 2, True))
        self.spellbook.append(
                Spell('Find Exit', Character.POINT_TO_EXIT, 7, False))
        self.spellbook.append(
                Spell('The Known World', Character.THE_KNOWN_WORLD, 3, False))
        self.spellbook.append(
                Spell('Statue Locator', Character.STATUE_LOCATOR, 3, False))
        self.spellbook.append(
                Spell('Insight', Character.INSIGHT, 2, False))
        self.spellbook.append(
                Spell('Set Trap', Character.SET_TRAP, 4, True))

        # select a subset of spells from the master spellbook
        num_spells = random.randint(2,6)
        temp_book = []
        for i in range(num_spells):
            random.shuffle(self.spellbook)
            temp_book.append( self.spellbook.pop() )

        self.spellbook = temp_book

        # always have Turn to Stone spell available
        self.spellbook.append(
                Spell('Turn to Stone', Character.TURN_TO_STONE, 0, False))

        # number these babies
        n = 1
        for s in self.spellbook:
            s.number = n
            n += 1



    def causeInjury(self, d):

        # This function may be called by MONSTERS

        self.INJURIES += d

        # graphic violence here
        if self.character_type == Character.PLAYER:

            if d > 1:
                text = self.name + ' INJURIES increase: ' + str(d) + ' points.'
                tc.lines.append((text,YELLOW))
            elif d == 1:
                text = self.name + ' INJURIES increase: ' + str(d) + ' point.'
                tc.lines.append((text,YELLOW))

        self.action = Character.BLOODBURST 
        gc.update()     
        if gc.isCharacterVisible(self) == True:
            sc.hit.play()
        time.sleep(GraphicsComponent.ANIMATION_SPEED)
        self.action = None

        # handle death
        max_injury = 0
        if self.character_type == Character.PLAYER:
            max_injury = Character.MAX_INJURY
        else:
            max_injury = Character.MAX_INJURY_MONSTER
        if self.INJURIES >= max_injury:

            self.INJURIES = max_injury 
            
            if self.character_type == Character.PLAYER:

                tc.lines = []
                text =  self.name + ' has died.'
                sc.player_death.play()
                tc.lines.append((text,RED))
                ic.mode = None

            else:
        
                if gc.isCharacterVisible(self) == True:
                    text =  'Monster has been slain.'
                    tc.lines.append((text,BLUE))
                    sc.monster_death.play()
            
            wc.characterDeath(self)


    def causeFatigue(self, f):

        self.FATIGUE += f

        if f > 1:
            text = self.name + ' FATIGUE increase: ' + str(f) + ' points.'
            tc.lines.append((text,YELLOW))
        elif f == 1:
            text = self.name + ' FATIGUE increase: ' + str(f) + ' point.'
            tc.lines.append((text,YELLOW))

        if self.FATIGUE >= Character.MAX_FATIGUE:

            self.FATIGUE = Character.MAX_FATIGUE 
            self.status = Character.STONED
            sc.turn_to_stone.play()
            ic.selectAnotherPlayer()
    
    
    
    def earnXP(self):

        xp = self.roll3d6()

        self.COMBAT += xp 

        if self.COMBAT > 999:

            self.COMBAT = 999

            tc.lines.append(('You have earned a maximum COMBAT rating.', BLUE))

        else:

            text = 'Earned ' + str(xp) + ' experience points. (COMBAT = ' + \
                str(self.COMBAT) + ')'
            tc.lines.append((text, BLUE))



    def roll3d6(self):

        # 3d6 returns a bell-shaped curve probability distribution

        result = 0

        for i in range(3):

            result += random.randint(1,6)

        return result





class Spell:

    def __init__(self, name, code, cost, target_needed):

        self.name = name
        self.code = code
        self.cost = cost
        self.target_needed = target_needed

        self.number = 0

    def setNumber(self, n):

        self.number = n


class SoundComponent:

    # enums for music
    TITLE_SCREEN             = 0

    def __init__(self):

        self.paint_floor         = pygame.mixer.Sound( \
                resource_path('sounds\\paint_floor.wav'))
        self.set_trap            = pygame.mixer.Sound( \
                resource_path('sounds\\set_trap.wav'))
        self.open_held_door      = pygame.mixer.Sound( \
                resource_path('sounds\\open_held_door.wav'))
        self.hit                 = pygame.mixer.Sound( \
                resource_path('sounds\\hit.wav'))
        self.the_known_world     = pygame.mixer.Sound( \
                resource_path('sounds\\the_known_world.wav'))
        self.transfer            = pygame.mixer.Sound( \
                resource_path('sounds\\transfer.wav'))
        self.locate_statues      = pygame.mixer.Sound( \
                resource_path('sounds\\locate_statues.wav'))
        self.enemy_move          = pygame.mixer.Sound( \
                resource_path('sounds\\enemy_move.wav'))
        self.player_move         = pygame.mixer.Sound( \
                resource_path('sounds\\player_move.wav'))
        self.info                = pygame.mixer.Sound( \
                resource_path('sounds\\info.wav'))
        self.swing_sword         = pygame.mixer.Sound( \
                resource_path('sounds\\swing_sword.wav'))
        self.exit                = pygame.mixer.Sound( \
                resource_path('sounds\\exit.wav'))
        self.denied_entry        = pygame.mixer.Sound( \
                resource_path('sounds\\denied_entry.wav'))
        self.misfire             = pygame.mixer.Sound( \
                resource_path('sounds\\misfire.wav'))
        self.weaken_monster      = pygame.mixer.Sound( \
                resource_path('sounds\\weaken_monster.wav'))
        self.stuck_door          = pygame.mixer.Sound( \
                resource_path('sounds\\stuck_door.wav'))
        self.crumble             = pygame.mixer.Sound( \
                resource_path('sounds\\crumble.wav'))
        self.game_over           = pygame.mixer.Sound( \
                resource_path('sounds\\game_over.wav'))
        self.monster_death       = pygame.mixer.Sound( \
                resource_path('sounds\\monster_death.wav'))
        self.player_death        = pygame.mixer.Sound( \
                resource_path('sounds\\player_death.wav'))
        self.wait                = pygame.mixer.Sound( \
                resource_path('sounds\\wait.wav'))
        self.restore_health      = pygame.mixer.Sound( \
                resource_path('sounds\\restore_health.wav'))
        self.key                 = pygame.mixer.Sound( \
                resource_path('sounds\\key.wav'))
        self.exit_unlocked       = pygame.mixer.Sound( \
                resource_path('sounds\\exit_unlocked.wav'))
        self.find_exit           = pygame.mixer.Sound( \
                resource_path('sounds\\find_exit.wav'))
        self.turn_to_stone       = pygame.mixer.Sound( \
                resource_path('sounds\\turn_to_stone.wav'))
    
    def play_intro_music(self):

        pygame.mixer.music.load(resource_path('music\\unauthorized.mp3'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)
        
    def play_exit_music(self):
  
        pygame.mixer.music.load(resource_path('music\\agoode.mp3'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)
    
    def play_help_music(self):
  
        pygame.mixer.music.load(resource_path('music\\lowdown.mp3'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)
 
    def stop_music(self):

        pygame.mixer.music.stop()

        

class TitlePage:

    def __init__(self):

        self.title_file = open(resource_path('files\\title_page.txt'), 'r')

        self.lines = []

        line = self.title_file.readline() 
        line = line.rstrip()

        while line != 'FINAL_END':

            self.lines.append(line)

            line = self.title_file.readline()
            line = line.rstrip()

        self.title_file.close()


    def showPage(self):

        # show current page

        gc.mainSurface.fill((0,0,0))

        y = 1
        for p in self.lines:
            if y < 6:
                self.add_text(p, YELLOW, 0, y)
            elif y > 23:
                self.add_text(p, YELLOW, 0, y)
            else:
                self.add_text(p, GRAPH_PAPER, 0, y)
            y += 1
        
        pygame.display.update()
        gc.clock.tick(gc.FPS)

    
    def add_text(self, t, color, cx, cy):

        n = tc.FONT.render(t, False, color)
        
        gc.mainSurface.blit(n, (cx * tc.FONT_WIDTH, cy * tc.FONT_HEIGHT))




class HelpSystem:

    def __init__(self):

        self.current_page = 1

        self.help_file = open(resource_path('files\\help_system.txt'), 'r')

        self.lines = []

        line = self.help_file.readline() 
        line = line.rstrip()
        line_num = 1

        while line != 'FINAL_END':

            if line != 'END':

                self.lines.append( (line_num, line) )

                line = self.help_file.readline()
                line = line.rstrip()

            else:

                line_num += 1

                line = self.help_file.readline()
                line = line.rstrip()

        self.help_file.close()

        self.total_num_pages = 0
        for p in self.lines:
            if p[0] > self.total_num_pages:
                self.total_num_pages = p[0]



    def nextPage(self):

        self.current_page += 1
        if self.current_page > self.total_num_pages:
            self.current_page = 1


    def showPage(self):

        # show current page

        gc.mainSurface.fill((0,0,0))

        self.add_text('FAQ page ' + str(self.current_page), GREEN, 67, 1)

        y = 3
        for p in self.lines:
            if p[0] == self.current_page:
                self.add_text(p[1], GRAPH_PAPER, 0, y)
                y += 1
        
        self.add_text('Press SPACE for next FAQ page, or ESC to return to game.', \
                GREEN, 2, 28)

        pygame.display.update()
        gc.clock.tick(gc.FPS)

    
    def add_text(self, t, color, cx, cy):

        n = tc.FONT.render(t, False, color)
        
        gc.mainSurface.blit(n, (cx * tc.FONT_WIDTH, cy * tc.FONT_HEIGHT))


def game_loop():

    global wc
    global gc
    global ic
    global tc
    global sc
    global hs
    global tp

    wc.levelTitlePage()

    # make sure initial screen is visible
    gc.calculateLight()
    gc.update() 

    while True:

        wc.update_plan()

        wc.update_action()
        
        wc.turn += 1

        if wc.nextLevel == True:
            wc.newWorld()
            wc.levelTitlePage()
            wc.nextLevel = False



def resource_path(relative):

    t = ''

    if hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
        t = os.path.join(sys._MEIPASS, relative)
    elif '_MEIPASS2' in os.environ:
        os.chdir(os.environ['_MEIPASS2'])
        t = os.path.join(os.environ['_MEIPASS2'], relative)
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        t = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative)

    return t



# program begins running here

pygame.mixer.pre_init(44100, -16, 2, 2048) # to avoid lag in sound effects
pygame.init()


# 216 Color System (RGB values, 0 to 255 each, step 51)
# Incremental Values are: 0, 51, 102, 153, 204, 255
COLOR = []
for r in range(0,256,51):
    for g in range(0,256,51):
        for b in range(0,256,51):
            COLOR.append((r,g,b))
WHITE        = COLOR[215]   # 255, 255, 255
BLACK        = COLOR[0]     # 000, 000, 000
RED          = COLOR[180]   # 255, 000, 000
DARK_RED     = COLOR[144]   # 204, 000, 000 
ORANGE       = COLOR[198]   # 255, 153, 000
YELLOW       = COLOR[210]   # 255, 255, 000 
LIGHT_YELLOW = COLOR[211]   # 255, 255, 051
DARK_YELLOW  = COLOR[168]   # 204, 204, 000
GREEN        = COLOR[30]    # 000, 255, 000
DARK_GREEN   = COLOR[24]    # 000, 204, 000
BLUE         = COLOR[5]     # 000, 000, 255
LIGHT_BLUE   = COLOR[47]    # 051, 051, 255
INDIGO       = COLOR[39]    # 051, 000, 153
VIOLET       = COLOR[203]   # 255, 153, 255
CYAN         = COLOR[35]    # 000, 255, 255
GRAPH_PAPER  = COLOR[137]   # 153, 204, 255
MAGENTA      = COLOR[185]   # 255, 000, 255
GREY         = COLOR[172]   # 204, 204, 204

wc = WorldComponent()
gc = GraphicsComponent()
ic = InputComponent()
tc = TextComponent()
sc = SoundComponent()
hs = HelpSystem()
tp = TitlePage()

sc.play_intro_music()

pygame.key.set_repeat(1,100)

while True:

    tp.showPage()

    for e in pygame.event.get():

        if e.type == QUIT:

            pygame.quit()
            sys.exit()

        elif e.type == KEYDOWN:

            if e.key == K_n:

                sc.stop_music()
                game_loop()

            elif e.key == K_q:

                pygame.quit()
                sys.exit()

    pygame.display.update()
    gc.clock.tick(gc.FPS)
