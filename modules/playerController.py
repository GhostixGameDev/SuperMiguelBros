import pygame
from miscFunctions import scale as scaleF
from miscFunctions import importFolderImages
from math import sin
from configLoader import tileSize,scale,tileSizeScaled
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,createJumpParticles,updateLives):
        super().__init__()
        self.updateLives=updateLives
        self.importCharacterAssets()
        self.importDustParticles()
        self.dustState="land"
        self.dustFrameIndex = 0
        self.dustAnimationSpeed = 0.15
        self.frameIndex=0
        self.createJumpParticles=createJumpParticles
        self.animationSpeed=0.15
        self.displaySurface=surface
        self.image=self.animations["idle"][self.frameIndex]
        self.rect=self.image.get_rect(topleft=pos)
        self.direction=pygame.math.Vector2(0,0)
        self.speed=4*scale
        self.gravity=0.8*scale
        self.jumpSpeed= -16 * scale
        self.onground=True
        self.invincible=False
        self.invincibilityDuration=2000
        self.hurtTime=0
        self.forceMove=False
        self.collisionRect = pygame.Rect(self.rect.topleft, (self.rect.width - 5, self.rect.height))
        #audio
        self.jumpSound=pygame.mixer.Sound("../assets/sounds/jump.ogg")
        #Anim States
        self.animationState="idle"
        self.facingRight=True
    def importCharacterAssets(self):
        spritesPath="../assets/sprites/miguel/"
        self.animations={"idle":[],"run":[],"jump":[]}
        for animation in self.animations.keys():
            fullPath = spritesPath+animation
            self.animations[animation]=importFolderImages(fullPath)
        for i in range(len(self.animations["idle"])):
            self.animations["idle"][i]=scaleF(self.animations["idle"][i],tileSizeScaled, tileSizeScaled)
        for i in range(len(self.animations["run"])):
            self.animations["run"][i]=scaleF(self.animations["run"][i],tileSizeScaled, tileSizeScaled)
        for i in range(len(self.animations["jump"])):
            self.animations["jump"][i] = scaleF(self.animations["jump"][i], tileSizeScaled, tileSizeScaled)
    def importDustParticles(self):
        spritesPath="../assets/sprites/particles/dust/"
        self.dustParticles={"run":[],"land":[],"jump":[]}
        for animation in self.dustParticles.keys():
            fullPath = spritesPath+animation
            self.dustParticles[animation]=importFolderImages(fullPath)
        for i in range(len(self.dustParticles["run"])):
            self.dustParticles["run"][i]=scaleF(self.dustParticles["run"][i],tileSizeScaled/4, tileSizeScaled/4)
        for i in range(len(self.dustParticles["land"])):
            self.dustParticles["land"][i]=scaleF(self.dustParticles["land"][i],tileSizeScaled/4, tileSizeScaled/4)
        for i in range(len(self.dustParticles["jump"])):
            self.dustParticles["jump"][i] = scaleF(self.dustParticles["jump"][i], tileSizeScaled/4, tileSizeScaled/4)

    def animateDust(self):
        animation = self.dustParticles[self.dustState]
        if self.dustState=="run":
            self.dustFrameIndex+=self.dustAnimationSpeed
            if self.dustFrameIndex>=len(animation):
                self.dustFrameIndex = 0
            dustParticle = animation[int(self.dustFrameIndex)]
            if self.facingRight:
                pos=self.rect.bottomleft - pygame.math.Vector2(6,20)
                self.displaySurface.blit(dustParticle,pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,20)
                self.displaySurface.blit(dustParticle, pos)
    def animate(self):
        animation = self.animations[self.animationState]
        self.frameIndex+=self.animationSpeed
        if self.frameIndex>=len(animation):
            self.frameIndex = 0
        image = animation[int(self.frameIndex)]
        if self.facingRight:
            self.image = image
            self.rect.bottomleft=self.collisionRect.bottomleft
        else:
            self.image = pygame.transform.flip(image,True,False)
            self.rect.bottomright = self.collisionRect.bottomright
        if self.invincible:
            alpha=self.waveValue()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        self.rect=self.image.get_rect(midbottom=self.rect.midbottom)

    def get_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x=1
            self.facingRight=True
        elif keys[pygame.K_a]:
            self.direction.x=-1
            self.facingRight=False
        elif not self.forceMove:
            self.direction.x=0
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            if self.onground:
                self.createJumpParticles(self.rect.midbottom)
            self.jump()

    def getStatus(self):
        if self.direction.y!=0:
            self.animationState="jump"
            self.dustState="jump"
        elif self.direction.x!=0:
            self.animationState="run"
            self.dustState="run"
        else:
            self.animationState="idle"
            self.dustState="land"

    def apply_gravity(self):
        self.direction.y+=self.gravity
        #print(self.direction.y)
        self.collisionRect.y += self.direction.y
    def jump(self):
        if self.onground:
            self.jumpSound.play()
            self.direction.y = self.jumpSpeed
            self.onground=False
    def getDamage(self):
        if not self.invincible:
            self.updateLives(-1)
            self.invincible=True
            self.hurtTime=pygame.time.get_ticks()

    def invincibilityTimer(self):
        if self.invincible:
            currentTime=pygame.time.get_ticks()
            if currentTime-self.hurtTime>=self.invincibilityDuration:
                self.invincible=False
    def waveValue(self):
        value=sin(pygame.time.get_ticks())
        if value>=0:
            return 255
        else:
            return 0
    def update(self):
        self.get_input()
        self.getStatus()
        self.animate()
        self.animateDust()
        self.waveValue()
        self.invincibilityTimer()