import pygame

from modules.particleHandler import ParticleEffect
from tiles import Tile
from levelEditor import *
from playerController import Player
class Level:
    def __init__(self,leveldata,surface):
        #Level setup
        self.display_surface=surface
        self.setup_level(leveldata)
        self.world_shift=0

        #Dust particles
        self.dustSprite=pygame.sprite.GroupSingle()
        self.playerOnGround = False
    def setup_level(self,layout):
        self.tiles=pygame.sprite.Group()
        self.player=pygame.sprite.GroupSingle()
        for row_index,row in enumerate(layout):
            for col_index,col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col=="X":
                    tile=Tile((x,y),tile_size)
                    self.tiles.add(tile)
                elif col=="P":
                    player_sprite=Player((x,y),self.display_surface,self.createJumpParticles)
                    self.player.add(player_sprite)

    def createJumpParticles(self,pos):
        if self.player.sprite.facingRight:
            pos-=pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jumpParticleSprite=ParticleEffect(pos,"jump")
        self.dustSprite.add(jumpParticleSprite)
    def isPlayerOnGround(self):
        if self.player.sprite.onground:
            self.playerOnGround=True
        else:
            self.playerOnGround = False
    def createLandingDust(self):
        if not self.playerOnGround and self.player.sprite.onground and not self.dustSprite.sprites():
            if self.player.sprite.facingRight:
                offset=pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            landDustParticle=ParticleEffect(self.player.sprite.rect.midbottom-offset,"land")
            self.dustSprite.add(landDustParticle)
    def scroll_x(self):
        player = self.player.sprite
        player_x=player.rect.centerx
        direction_x=player.direction.x

        if player_x<screenWidth / 4 and direction_x<0:
            self.world_shift=4
            player.speed=0
        elif player_x>screenWidth - (screenWidth/4) and direction_x>0:
            self.world_shift=-4
            player.speed=0
        else:
            self.world_shift=0
            player.speed=4

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player):
                if player.direction.x <0:
                    player.rect.left=sprite.rect.right
                elif player.direction.x>0:
                    player.rect.right=sprite.rect.left
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player):
                if player.direction.y >0:
                    player.rect.bottom=sprite.rect.top
                    player.direction.y=0
                    player.onground = True
                elif player.direction.y<0:
                    player.rect.top=sprite.rect.bottom
                    player.direction.y=0

    def run(self):
        #Particle loader
        self.dustSprite.update(self.world_shift)
        self.dustSprite.draw(self.display_surface)

        #Level tilemap
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        #Player
        self.player.update()
        self.horizontal_movement_collision()
        self.isPlayerOnGround()
        self.vertical_movement_collision()
        self.createLandingDust()
        self.player.draw(self.display_surface)



