import pygame
from miscFunctions import scale
from miscFunctions import importFolderImages
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,createJumpParticles):
        super().__init__()
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
        self.speed=4
        self.gravity=0.8
        self.jump_speed=-16
        self.onground=True

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
            self.animations["idle"][i]=scale(self.animations["idle"][i],64,64)
        for i in range(len(self.animations["run"])):
            self.animations["run"][i]=scale(self.animations["run"][i],64,64)
        for i in range(len(self.animations["jump"])):
            self.animations["jump"][i] = scale(self.animations["jump"][i], 64, 64)
    def importDustParticles(self):
        spritesPath="../assets/sprites/particles/dust/"
        self.dustParticles={"run":[],"land":[],"jump":[]}
        for animation in self.dustParticles.keys():
            fullPath = spritesPath+animation
            self.dustParticles[animation]=importFolderImages(fullPath)
        for i in range(len(self.dustParticles["run"])):
            self.dustParticles["run"][i]=scale(self.dustParticles["run"][i],16,16)
        for i in range(len(self.dustParticles["land"])):
            self.dustParticles["land"][i]=scale(self.dustParticles["land"][i],16,16)
        for i in range(len(self.dustParticles["jump"])):
            self.dustParticles["jump"][i] = scale(self.dustParticles["jump"][i], 16, 16)

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
        else:
            self.image = pygame.transform.flip(image,True,False)

    def get_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x=1
            self.facingRight=True
        elif keys[pygame.K_a]:
            self.direction.x=-1
            self.facingRight=False
        else:
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
        self.rect.y += self.direction.y
    def jump(self):
        if self.onground:
            self.direction.y = self.jump_speed
            self.onground=False
    def update(self):
        self.get_input()
        self.getStatus()
        self.animate()
        self.animateDust()
