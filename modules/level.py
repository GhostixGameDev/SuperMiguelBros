import pygame

from miscFunctions import importCsvLayout, importCutSpritesheet
from particleHandler import ParticleEffect, JoJoLikeText
from tiles import Tile, staticTile, box, coin, luckyblock, goal
from gameData import *
from enemy import enemy
from playerController import Player
class Level:
    def __init__(self, currentLevel, surface,createOverworld,updateCoins,coins,updateLives,createLevel):
        #Level setup
        self.display_surface=surface
        self.world_shift=0
        self.currentLevel=currentLevel
        self.updateCoins=updateCoins
        levelMeta=levels[currentLevel]
        leveldata=levelMeta["content"]
        self.newMaxLevel=levelMeta["unlock"]
        self.createOverworld=createOverworld
        self.createLevel=createLevel
        #Player
        playerLayout= importCsvLayout(leveldata["constraints3"])
        self.player=pygame.sprite.GroupSingle()
        self.goal=pygame.sprite.GroupSingle()
        self.coins=coins
        self.updateLives=updateLives
        self.playerSetup(playerLayout)

        #LOL
        self.JoJoText=JoJoLikeText("../assets/fonts/SF Fedora.ttf", 20, self.display_surface)
        self.JoJoText2 = JoJoLikeText("../assets/fonts/SF Fedora.ttf", 20, self.display_surface)
        self.stopJojo=True

        #Audio
        self.coinSound=pygame.mixer.Sound("../assets/sounds/coin.ogg")

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
                            value=0
                            if col=="0":
                                coinpath="../assets/sprites/objects/coins/gold"
                                value=5
                            else:
                                coinpath="../assets/sprites/objects/coins/silver"
                                value=1
                            sprite=coin(tile_size,x,y,coinpath,value)
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
                            if col=="1":
                                blockpath="../assets/sprites/objects/luckyblock/sliced/luckyBlock02.png"
                                state=0
                            else:
                                blockpath = "../assets/sprites/objects/luckyblock/sliced/luckyBlock01.png"
                                state = 1
                            sprite=luckyblock(tile_size,x,y,blockpath,state)



                        spriteGroup.add(sprite)

        return spriteGroup
    def playerSetup(self,layout):
        for rowIndex, row in enumerate(layout):
            for colIndex, col in enumerate(row):
                x = colIndex * tile_size
                y = rowIndex * tile_size
                if col=="2":
                    sprite = Player((x,y),self.display_surface,self.createJumpParticles,self.updateLives)
                    self.player.add(sprite)
                if col=="3":
                    sprite=goal(tile_size,x,y)
                    self.goal.add(sprite)
    def checkPlayerDownMap(self):
        if self.player.sprite.rect.top>screenheight:
            self.updateLives(-1)
            self.createLevel(self.currentLevel)
    def checkWin(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            self.createOverworld(self.currentLevel,self.newMaxLevel,True)

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
    def scrollX(self):
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
    def horizontalMovementCollision(self):
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
    def verticalMovementCollision(self):
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

    def checkCoinCollision(self):
        collidedCoins=pygame.sprite.spritecollide(self.player.sprite,self.coinsSprites,True)
        if collidedCoins:
            for coin in collidedCoins:
                self.coinSound.play()
                self.coins+=coin.value
                self.updateCoins(self.coins)
    def checkEnemyCollisions(self):
        enemyCollisions=pygame.sprite.spritecollide(self.player.sprite,self.EnemySprites,False)
        if enemyCollisions:
            for enemy in enemyCollisions:
                enemyCenter=enemy.rect.centery
                enemyTop=enemy.rect.top
                self.stopJojo=True
                playerBottom=self.player.sprite.rect.bottom
                if enemyTop<playerBottom<enemyCenter and self.player.sprite.direction.y>=0 and enemy.deadMoving:
                    self.player.sprite.direction.y=-15
                    enemy.kill()
                    self.stopJoJo=True
                    self.JoJoText.pastTime=pygame.time.get_ticks()
                    self.JoJoText2.pastTime=pygame.time.get_ticks()
                elif enemyTop<playerBottom<enemyCenter and self.player.sprite.direction.y>=0:
                    self.player.sprite.direction.y = -15
                    self.stopJojo=False
                    self.JoJoText.pastTime=pygame.time.get_ticks()
                    self.JoJoText2.pastTime=pygame.time.get_ticks()
                    if enemy.dead and not enemy.deadMoving:
                        enemy.deadMoving=True
                    enemy.dead=True

                else:
                    self.player.sprite.getDamage()

    def newLife(self):
        if self.coins>=100:
            self.coins=0
            self.updateLives(1)



    def run(self):
        self.display_surface.fill((0,0,0))
        #Particle loader
        self.dustSprite.update(self.world_shift)
        self.dustSprite.draw(self.display_surface)

        #Level tilemap
        self.backgroundSprites.draw(self.display_surface)
        self.backgroundSprites.update(self.world_shift)
        #dust
        self.dustSprite.update(self.world_shift)
        self.dustSprite.draw(self.display_surface)
        #boxes
        self.boxesSprites.draw(self.display_surface)
        self.boxesSprites.update(self.world_shift)
        #coins
        self.coinsSprites.draw(self.display_surface)
        self.coinsSprites.update(self.world_shift)
        #enemys
        self.EnemySprites.draw(self.display_surface)
        self.EnemySprites.update(self.world_shift)
        #constraints
        self.constraintSprites.update(self.world_shift)
        self.enemyCollisionReverse()
        #decoration
        self.decorationSprites.draw(self.display_surface)
        self.decorationSprites.update(self.world_shift)
        #LuckyBlocks
        self.luckyBlocksSprites.draw(self.display_surface)
        self.luckyBlocksSprites.update(self.world_shift)
        #Camera
        self.scrollX()



        #Player
        self.goal.update(self.world_shift)
        self.player.update()
        self.goal.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.checkPlayerDownMap()
        self.checkWin()
        self.checkCoinCollision()
        self.newLife()
        self.checkEnemyCollisions()
        self.JoJoText.update(self.world_shift)
        self.JoJoText2.update(self.world_shift)

        if not self.stopJojo:
            self.stopJojo = self.JoJoText.textTimer()
            self.JoJoText.draw("Gracias por no",(0,0,0),self.player.sprite.rect.x+40,self.player.sprite.rect.y+20)
            self.JoJoText2.draw("Usar los celulares...",(0,0,0),self.player.sprite.rect.x+60,self.player.sprite.rect.y+30)
        self.input()

        self.isPlayerOnGround()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.createLandingDust()



