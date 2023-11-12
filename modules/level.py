import pygame

from miscFunctions import importCsvLayout, importCutSpritesheet
from particleHandler import ParticleEffect
from tiles import Tile, staticTile, box, coin, luckyblock, goal
from gameData import *
from enemy import enemy
from playerController import Player
class Level:
    def __init__(self, currentLevel, surface,createOverworld):
        #Level setup
        self.display_surface=surface
        self.world_shift=0
        self.currentLevel=currentLevel
        levelMeta=levels[currentLevel]
        leveldata=levelMeta["content"]
        self.newMaxLevel=levelMeta["unlock"]
        self.createOverworld=createOverworld
        #Player
        playerLayout= importCsvLayout(leveldata["constraints3"])
        self.player=pygame.sprite.GroupSingle()
        self.goal=pygame.sprite.GroupSingle()
        self.playerSetup(playerLayout)

        #Layouts
        boxesLayout=importCsvLayout(leveldata["boxes"])
        backgroundLayout=importCsvLayout(leveldata["background"])
        coinsLayout=importCsvLayout(leveldata["coins"])
        EnemysLayout=importCsvLayout(leveldata["enemys"])
        LuckyBlocksLayout=importCsvLayout(leveldata["luckyblocks"])
        decorationLayout=importCsvLayout(leveldata["decoration"])
        #Background
        self.backgroundSprites=self.createTileGroup(backgroundLayout, "background")
        #boxes
        self.boxesSprites=self.createTileGroup(boxesLayout, "boxes")
        #coins
        self.coinsSprites=self.createTileGroup(coinsLayout, "coins")
        #Enemys
        self.EnemySprites=self.createTileGroup(EnemysLayout, "enemys")
        self.luckyBlocksSprites=self.createTileGroup(LuckyBlocksLayout, "luckyblocks")
        #Decoration
        self.decorationSprites=self.createTileGroup(decorationLayout, "decoration")

        #CONSTRAINTS (They are like checkpoints for different conditions.)
        constraintLayout=importCsvLayout(leveldata["constraints"])
        self.constraintSprites=self.createTileGroup(constraintLayout, "constraints")
        constraintLayout2 = importCsvLayout(leveldata["constraints2"])
        self.constraintSprites2 = self.createTileGroup(constraintLayout2, "constraints2")

        #Dust particles
        self.dustSprite=pygame.sprite.GroupSingle()
        self.playerOnGround = False

    def input(self):
        key=pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            self.createOverworld(self.currentLevel,0)
    def createTileGroup(self,layout,type):
        spriteGroup=pygame.sprite.Group()
        for rowIndex,row in enumerate(layout):
                for colIndex,col in enumerate(row):
                    if col!="-1":
                        x=colIndex*tile_size
                        y=rowIndex*tile_size
                        if type=="boxes":
                            sprite=box(tile_size,x,y)

                        if type=="background":
                            backgroundTileList=importCutSpritesheet("../assets/sprites/background/tiles/backgroundTiles.png")
                            tileSurface=backgroundTileList[int(col)]
                            sprite=staticTile(tile_size,x,y,tileSurface)

                        if type=="coins":
                            coinpath=""
                            if col==0:
                                coinpath="../assets/sprites/objects/coins/gold"
                            else:
                                coinpath="../assets/sprites/objects/coins/silver"
                            sprite=coin(tile_size,x,y,coinpath)
                        if type=="decoration":
                            decoTileList=importCutSpritesheet("../assets/sprites/background/tiles/backgroundTiles.png")
                            tileSurface=decoTileList[int(col)]
                            sprite=staticTile(tile_size,x,y,tileSurface)
                        if type=="enemys":
                            sprite=enemy(tile_size,x,y)
                        if type=="constraints":
                            sprite=Tile(tile_size,x,y)
                        if type=="constraints2":
                            sprite=Tile(tile_size,x,y)
                        if type== "luckyblocks":
                            sprite=luckyblock(tile_size,x,y)



                        spriteGroup.add(sprite)

        return spriteGroup
    def playerSetup(self,layout):
        for rowIndex, row in enumerate(layout):
            for colIndex, col in enumerate(row):
                x = colIndex * tile_size
                y = rowIndex * tile_size
                if col=="2":
                    sprite = Player((x,y),self.display_surface,self.createJumpParticles)
                    self.player.add(sprite)
                if col=="3":
                    sprite=goal(tile_size,x,y)
                    self.goal.add(sprite)
    def checkDeath(self):
        if self.player.sprite.rect.top>screenheight:
            self.createOverworld(self.currentLevel,0)
    def checkWin(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            self.createOverworld(self.currentLevel,self.newMaxLevel)
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

    def enemyCollisionReverse(self):
        for enemy in self.EnemySprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraintSprites,False):
                enemy.reverse()
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        #Select wich things have collisions
        collidableSprites=self.boxesSprites.sprites() + self.luckyBlocksSprites.sprites()
        for sprite in collidableSprites:
            if sprite.rect.colliderect(player):
                if player.direction.x <0:
                    player.rect.left=sprite.rect.right
                elif player.direction.x>0:
                    player.rect.right=sprite.rect.left
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        #Select wich things have collisions
        collidableSprites=self.boxesSprites.sprites() + self.luckyBlocksSprites.sprites()
        for sprite in collidableSprites:
            if sprite.rect.colliderect(player):
                if player.direction.y >0:
                    player.rect.bottom=sprite.rect.top
                    player.direction.y=0
                    player.onground = True
                elif player.direction.y<0:
                    player.rect.top=sprite.rect.bottom
                    player.direction.y=0

    def run(self):
        self.display_surface.fill((0,0,0))
        #Particle loader
        self.dustSprite.update(self.world_shift)
        self.dustSprite.draw(self.display_surface)

        #Level tilemap
        self.backgroundSprites.draw(self.display_surface)
        self.backgroundSprites.update(self.world_shift)
        self.boxesSprites.draw(self.display_surface)
        self.boxesSprites.update(self.world_shift)
        self.coinsSprites.draw(self.display_surface)
        self.coinsSprites.update(self.world_shift)
        self.EnemySprites.draw(self.display_surface)
        self.EnemySprites.update(self.world_shift)
        self.constraintSprites.update(self.world_shift)
        self.enemyCollisionReverse()
        self.decorationSprites.draw(self.display_surface)
        self.decorationSprites.update(self.world_shift)
        self.luckyBlocksSprites.draw(self.display_surface)
        self.luckyBlocksSprites.update(self.world_shift)
        self.scroll_x()

        #dust
        self.dustSprite.update(self.world_shift)
        self.dustSprite.draw(self.display_surface)

        #Player
        self.goal.update(self.world_shift)
        self.player.update()
        self.goal.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.checkDeath()
        self.checkWin()
        self.input()

        self.isPlayerOnGround()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.createLandingDust()




