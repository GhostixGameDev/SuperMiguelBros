import pygame

from miscFunctions import importCsvLayout, importCutSpritesheet
from particleHandler import ParticleEffect, JoJoLikeText
from tiles import Tile, staticTile, box, coin, luckyblock, goal
from configLoader import height
from gameData import *
from enemy import enemy
from playerController import Player
class Level:
    def __init__(self, currentLevel, surface,createOverworld,updateCoins,coins,updateLives,createLevel):
        #Level setup
        self.display_surface=surface
        self.worldShiftX=0
        self.worldShiftY=0
        self.currentLevel=currentLevel
        self.updateCoins=updateCoins
        levelMeta=levels[currentLevel]
        leveldata=levelMeta["content"]
        self.newMaxLevel=levelMeta["unlock"]
        self.createOverworld=createOverworld
        self.createLevel=createLevel
        self.initScrolled=0
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
                        x= colIndex * tileSizeScaled
                        y= rowIndex * tileSizeScaled
                        if type=="boxes":
                            sprite=box(tileSizeScaled, x, y)

                        if type=="background":
                            backgroundTileList=importCutSpritesheet("../assets/sprites/background/tiles/backgroundTiles.png")
                            tileSurface=backgroundTileList[int(col)]
                            sprite=staticTile(tileSizeScaled, x, y, tileSurface)

                        if type=="coins":
                            coinpath=""
                            value=0
                            if col=="0":
                                coinpath="../assets/sprites/objects/coins/gold"
                                value=5
                            else:
                                coinpath="../assets/sprites/objects/coins/silver"
                                value=1
                            sprite=coin(tileSizeScaled, x, y, coinpath, value)
                        if type=="decoration":
                            decoTileList=importCutSpritesheet("../assets/sprites/background/tiles/backgroundTiles.png")
                            tileSurface=decoTileList[int(col)]
                            sprite=staticTile(tileSizeScaled, x, y, tileSurface)
                        if type=="enemys":
                            sprite=enemy(tileSizeScaled, x, y)
                        if type=="constraints":
                            sprite=Tile(tileSizeScaled, x, y)
                        if type=="constraints2":
                            sprite=Tile(tileSizeScaled, x, y)
                        if type== "luckyblocks":
                            if col=="1":
                                blockpath="../assets/sprites/objects/luckyblock/sliced/luckyBlock02.png"
                                state=0
                            else:
                                blockpath = "../assets/sprites/objects/luckyblock/sliced/luckyBlock01.png"
                                state = 1
                            sprite=luckyblock(tileSizeScaled, x, y, blockpath, state)



                        spriteGroup.add(sprite)

        return spriteGroup
    def playerSetup(self,layout):
        for rowIndex, row in enumerate(layout):
            for colIndex, col in enumerate(row):
                x = colIndex * tileSize
                y = rowIndex * tileSize
                if col=="2":
                    sprite = Player((x,y),self.display_surface,self.createJumpParticles,self.updateLives)
                    self.player.add(sprite)
                if col=="3":
                    sprite=goal(tileSize, x, y)
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
        playerX=player.rect.centerx
        directionX=player.direction.x

        if playerX<screenWidth /4 and directionX<0:
            self.worldShiftX=4
            player.rect.centerx=player.rect.centerx+scale#*2
            player.speed=1
        elif playerX>screenWidth - (screenWidth/4) and directionX>0:
            self.worldShiftX=-4
            player.rect.centerx = player.rect.centerx - scale
            player.speed=1
        elif self.initScrolled==1:
            self.worldShiftX=0
            player.speed=4
    def scrollY(self):
        player = self.player.sprite
        playerY=player.rect.centery
        playerGravity=player.gravity
        originalGravity=0.8*scale
        directionY=player.direction.y

        if playerY<height /5 and directionY>playerGravity:
            print("Im up")
            self.worldShiftY=4
            playerGravity=0
            player.rect.centery=player.rect.centery+scale#*2
        elif playerY>height - (height/2): #and directionY<playerJumpSpeed:
            print("im down")
            self.worldShiftY=-4
            player.rect.centery = player.rect.centery - scale
            playerGravity=0
        else:
            playerGravity=originalGravity
            self.worldShiftY=0

    def initialScroll(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        originalSpeed=player.speed

        if playerX > screenWidth-500*scale:
            #print("moving left")
            self.worldShiftX = -64
            player.rect.centerx = player.rect.centerx - scale
            player.direction.x=-1
            player.gravity=0
            player.forceMove=True
            player.invincible=True
            player.speed = 63*scale
            #print(player.rect.x)
        else:
            #print("im not init moving")
            self.initScrolled=1
            player.forceMove=False
            player.invincible=False
            self.worldShiftX = 0
            player.speed = originalSpeed
            player.gravity= 0.8*scale
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
    def moveAll(self):
        #PUT ALL THINGS YOU WANT THE CAMERA TO MOVE HERE
        self.dustSprite.update(self.worldShiftX, self.worldShiftY)
        self.backgroundSprites.update(self.worldShiftX, self.worldShiftY)
        self.boxesSprites.update(self.worldShiftX, self.worldShiftY)
        self.dustSprite.update(self.worldShiftX, self.worldShiftY)
        self.coinsSprites.update(self.worldShiftX, self.worldShiftY)
        self.EnemySprites.update(self.worldShiftX, self.worldShiftY)
        self.constraintSprites.update(self.worldShiftX, self.worldShiftY)
        self.decorationSprites.update(self.worldShiftX, self.worldShiftY)
        self.luckyBlocksSprites.update(self.worldShiftX, self.worldShiftY)
        self.goal.update(self.worldShiftX, self.worldShiftY)
        self.JoJoText.update(self.worldShiftX, self.worldShiftY)
        self.JoJoText2.update(self.worldShiftX, self.worldShiftY)
        print("Moving things at this speed: " + str(self.worldShiftX) + ", " + str(self.worldShiftY))
    def newLife(self):
        if self.coins>=100:
            self.coins=0
            self.updateLives(1)



    def run(self):
        self.display_surface.fill((0,0,0))
        #Particle loader
        self.dustSprite.draw(self.display_surface)

        #Level tilemap
        self.backgroundSprites.draw(self.display_surface)

        #dust
        self.dustSprite.draw(self.display_surface)

        #boxes
        self.boxesSprites.draw(self.display_surface)

        #coins
        self.coinsSprites.draw(self.display_surface)

        #enemys
        self.EnemySprites.draw(self.display_surface)

        #constraints
        self.enemyCollisionReverse()
        #decoration
        self.decorationSprites.draw(self.display_surface)

        #LuckyBlocks
        self.luckyBlocksSprites.draw(self.display_surface)

        #Camera
        self.moveAll()
        if not self.initScrolled:
            self.initialScroll()
        self.scrollX()
        self.scrollY()



        #Player
        self.player.update()
        self.goal.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.checkPlayerDownMap()
        self.checkWin()
        self.checkCoinCollision()
        self.newLife()
        self.checkEnemyCollisions()


        if not self.stopJojo:
            self.stopJojo = self.JoJoText.textTimer()
            self.JoJoText.draw("Gracias por no",(0,0,0),self.player.sprite.rect.x+40,self.player.sprite.rect.y+20)
            self.JoJoText2.draw("Usar los celulares...",(0,0,0),self.player.sprite.rect.x+60,self.player.sprite.rect.y+30)
        self.input()

        self.isPlayerOnGround()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.createLandingDust()



