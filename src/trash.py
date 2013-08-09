#-------------------------------------------------------------------------------
# Name:        trash.py
# Purpose:     for keeping all the unues code but maybe review for coding idea
#
# Author:      MuychivTaing
#
# Created:     16/02/2012
# Copyright:   (c) MuychivTaing 2012
#-------------------------------------------------------------------------------
#!/usr/bin/env python

class HeroSprite(BaseSprite):
    """
    Sprite()

    a basic sprite class

    Usage: player = Sprite()
           player.loadSpriteSheet(spriteSheet, alpha=False)

    Note : if loadSpriteSheet is not called, the sprite will be
           a box with (100,100,100) color and rect of (25,25)
           and rect.centerx = 320, rect.centery = 240
    """

    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill((100,100,100))
        self.rect = self.image.get_rect()
        self.rect.centerx = 320
        self.rect.centery = 280

        self.imageDict = {}

        # TODO1: be able to load any character sprite size
        self.charDIM = (24,32)
        self.sheetDIM = (96, 128)
        self.maxFrame = 2
        self.addFrame = 1
        self.standFrame = 1
        self.currentFrame = self.standFrame
        self.animationSpeed = 1
        self.delay = 5
        self.temp = self.animationSpeed

        self.direction = "down"
        self.isWalking = False

        self.unWalkable = []
        self.isCollided = False
        self.movementX = 3          # might be change by camera module
        self.movementY = 3          # might be change by camera module
#        self.animationFrame =

#        self.centPos = (0,0)

    def update(self):
        self._check_collision()
        if not self.isWalking:
            self.image = self.imageDict[self.direction][self.standFrame]
        else:
            self.isWalking = False

    def load_sprite_sheet(self, spritesheet, alpha=False):
        """
        sprite.load_sprite_sheet(self, spritesheet, alpha=False)

        Load a sprite sheet
        """
        tempSheet = pygame.image.load(spritesheet).convert()

        ## Subsurface from a the sprite sheet
        tempRect = pygame.Rect((0,0),(self.sheetDIM))
        tempSheet = tempSheet.subsurface(tempRect)

        # TODO2 should tempdirectionlist, tempRow,and tempCollumn be ablt to set?
        tempDirectionList = ["up", "right", "down", "left"]
        tempRow = self.sheetDIM[1]/self.charDIM[1]
        tempCollumn = self.sheetDIM[0]/self.charDIM[0]

        for row in range(tempRow):
            tempList = []
            for collumn in range(tempCollumn):
                tempRect = pygame.Rect((self.charDIM[0]*collumn,
                                        self.charDIM[1]*row),
                                       (self.charDIM))
                tempImage = tempSheet.subsurface(tempRect)
                if alpha:
                    tempImage = tempImage.convert_alpha()
                else:
                    trans_color = tempImage.get_at((0,0))
                    tempImage.set_colorkey(trans_color)
                tempList.append(tempImage)
            self.imageDict[tempDirectionList[row]] = tempList

        self.image = self.imageDict[self.direction][self.standFrame]

        # should this be function. they are use in __init__ and here
        self.rect = self.image.get_rect()
        self.rect.centerx = 320
        self.rect.centery = 240
        self.rect.inflate_ip(-5,0)


    def move(self, direction):
        """
        sprite.move(self, direction)

        To make a sprite move

        Give direction as a string: "up", "down", "left", or "right"
        """
        self.isWalking = True
        self.direction = direction
        self._do_animation()

        if not self.isCollided:
            if self.direction == "up":
                self.rect.centery -= self.movementY
            elif self.direction == "down":
                self.rect.centery += self.movementY
            if self.direction == "left":
                self.rect.centerx -= self.movementX
            elif self.direction == "right":
                self.rect.centerx += self.movementX
        else:
            self.isCollided = False

    def _check_collision(self):
        for sprite in self.unWalkable:
            if self.rect.colliderect(sprite.rect):
                self.isCollided = True
                if self.direction == "up":
                    self.rect.centery += self.movementY
                elif self.direction == "down":
                    self.rect.centery -= self.movementY
                if self.direction == "left":
                    self.rect.centerx += self.movementX
                elif self.direction == "right":
                    self.rect.centerx -= self.movementX

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 3000:
            self.rect.right = 3000
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > 3000:
            self.rect.bottom = 3000


    def add_unwalkable_sprite(self, sprite):
        self.unWalkable.append(sprite)

    def _do_animation(self):
        self.temp += self.animationSpeed
        if self.temp >= self.delay:
            self.temp = self.animationSpeed
            self.image = self.imageDict[self.direction][self.currentFrame]

            # not sure but this animation has to do add and substract frame
            # back and forward
            self.currentFrame += self.addFrame
            if self.currentFrame < 0:
                self.addFrame *= -1
                self.currentFrame += self.addFrame
            elif self.currentFrame > self.maxFrame:
                self.addFrame *= -1
                self.currentFrame += self.addFrame

def main():
    pass

if __name__ == '__main__':
    main()
