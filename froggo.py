import pygame
from settings import *
from math import sin
import datetime

class Froggo(pygame.sprite.Sprite):
    def __init__(self,position,label,obstacle_sprites,create_attack,destroy_attack,create_spells):
        super().__init__(label)
        self.graphic = pygame.image.load('../img/froggo/down/down_0.png')
        self.rect = self.graphic.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-8,-26)



        self.import_froggo()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.direction = pygame.math.Vector2()

        self.attacking = False
        self.cooldown_attack = 550
        self.time_attack = None
        self.create_attack = create_attack
        self.obstacle_sprites = obstacle_sprites

        #bronie
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(INFO_WEAPONS.keys())[self.weapon_index] #potrzebujemy listy by móc zdobywac index broni
        self.switch_weapon = True
        self.time_switch_weapon = None


        #magia
        self.create_spells = create_spells
        self.spells_index = 0
        self.spells = list(INFO_SPELLS.keys())[self.spells_index]
        self.switch_spells = True
        self.time_switch_spells = None

        #statystyki
        self.stats = {'hp':80,'mana':80,'attack':8,'spells':5,"speed":5}
        self.max_stats = FROGGO_MAX_LEVEL
        self.upgrade_cost = {'hp':125,'mana':125,'attack':200,'spells':200,"speed": 150}
        self.hp = self.stats['hp']
        self.mana = self.stats['mana']
        self.xp = 3500
        self.score = 0
        self.speed = self.stats['speed']

        #timer zapisywania wyniku
        self.switch_score = True
        self.time_score = None


        #timer obrażeń
        self.vulnerable = True
        self.hurt_time = None


        #importujemy dźwieki
        self.weapon_sound = pygame.mixer.Sound('../sound/attack.wav')
        self.weapon_sound.set_volume(0.3)


        #czcionka GameOver Screen
        self.fontBig = pygame.font.Font(FONT,90)
        self.font = pygame.font.Font(FONT,60)


    def import_froggo(self):
        froggo_folder = '../img/froggo/'
        self.animation_status = {'up': [],'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animation_status.keys():
            complete_path = froggo_folder + animation
            self.animation_status[animation] = folder_import(complete_path)



    def move(self,speed):
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #idziemy w prawo
                        self.hitbox.right = sprite.rect.left #skoro idziemy w prawo to ewentualna kolizja na 100% będzie po prawej stronie
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #idziemy w dół, w pygame center point (0,0) jest w gornym lewym rogu
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

    def wave_value(self):
        if sin(pygame.time.get_ticks()) >= 0: 
            return 255 #pelna przezroczystosc
        else: 
            return 0




    def froggo_input(self):
        if not self.attacking: #by nie mozna bylo zmienic kierunku w trakcie ataku
            keys = pygame.key.get_pressed()

            #input gracza do poruszania się
            if keys[pygame.K_UP]:
                self.direction.y =-1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0


            if keys[pygame.K_RIGHT]:
                self.direction.x =1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

        #input do atakowania
            if keys[pygame.K_SPACE]: #and not self.attacking: #po to by gracz nie atakował trzymając przycisk ORAZ by nie mógł atakować i uzywac magii jednoczesnie ORAZ by nie mogl ich uzywac w bardzooo krotkich odstepach czasu
                self.attacking = True
                self.time_attack = pygame.time.get_ticks() #zapisuje czas tylko ostatniego ataku
                self.create_attack()
                self.weapon_sound.play()

        #input - magia
            if keys[pygame.K_w]:
                self.attacking = True
                self.time_attack = pygame.time.get_ticks()
                style = list(INFO_SPELLS.keys())[self.spells_index]
                strength = list(INFO_SPELLS.values())[self.spells_index]['strength'] +self.stats['spells']
                mana_cost = list(INFO_SPELLS.values())[self.spells_index]['mana_cost']


                self.create_spells(style,strength,mana_cost)

            if keys[pygame.K_a] and self.switch_weapon:
                self.switch_weapon = False
                self.time_switch_weapon = pygame.time.get_ticks()

                if self.weapon_index < len(list(INFO_WEAPONS.keys())) - 1: #-1 bo indeksy liczymy od 0, więc bronie
                    #mają 0,1,2; natomiast ilość broni to 3
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(INFO_WEAPONS.keys())[self.weapon_index]


            if keys[pygame.K_d] and self.switch_spells:
                self.switch_spells = False
                self.time_switch_spells = pygame.time.get_ticks()

                if self.spells_index < len(list(INFO_SPELLS.keys())) - 1:
                    self.spells_index += 1
                else:
                    self.spells_index = 0
                self.spells = list(INFO_SPELLS.keys())[self.spells_index]


#Game Over screen
            if self.hp <= 0:
                surface = pygame.display.get_surface()
                Loserect = pygame.Rect(0,0,surface.get_size()[0],surface.get_size()[1])
                pygame.draw.rect(surface,'black',Loserect,500)

                dead_surf = self.fontBig.render("Game Over",False,'white')

                scoreText = "Wynik : "+str(int(self.score))
                score_surf = self.font.render(scoreText,False,'white')

                restart_text = "Restart - wcisnij R"
                restart_surface = self.font.render(restart_text,False,'white')

                save_text = "Zapisz wynik - wcisnij F"
                save_surface = self.font.render(save_text,False,'white')

                surface.blit(dead_surf,(370,90))
                surface.blit(score_surf,(425,250))
                surface.blit(restart_surface,(358,530))
                surface.blit(save_surface,(320,620))


                self.hitbox.x = 10000000#Teleportujemy gracza żeby wrogowie nie mogli go dalej atakować w tle.
                self.hitbox.y = 10000000
                if keys[pygame.K_f] and self.switch_score:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.switch_score = False
                    self.time_score = pygame.time.get_ticks()
                    with open("../list_of_scores.txt", "a") as file: 
                        file.write("Date: "+ str(now)+'\n' + "score: "+str(int(self.score))+'\n\n')



    def get_status(self):
        #status bezruchu
        if self.direction.x == 0 and self.direction.y == 0: #gracz się nie rusza
            if not 'idle' in self.status and not 'attack' in self.status: #sprawdzamy czy status nie posiada już idle w tytule bo inaczej ciągle będzie dodawać koncowke _idle do statusu wiec otrzymamy up_idle_idle_idle_idle
                self.status = self.status + '_idle'

        #status atakowania
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status: #inaczej beda tworzone kombosy rigt_idle_attack
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status: #po to by _attack zniknelo z statusu gdy zaatakujemy i przejdziemy w tryb idle
                self.status = self.status.replace('_attack','')


    def cooldowns(self):
        #cooldowns są po to by 
        #podczas pojedynczego wcisniecia przycisku zmiany broni nie doszlo do wielu 
        #zmian broni jako ze fizycznie wcisniecie przyciska to np okolo 0,2s 
        #co dla komputera oznacza wiele klatek a wiec powtorzenie kodu zmiany broni 
        #wiele razy
        current_time = pygame.time.get_ticks() #cały czas liczy czas

        if self.attacking:
            if current_time - self.time_attack >= self.cooldown_attack + INFO_WEAPONS[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.switch_weapon:
            if current_time - self.time_switch_weapon >= 200:
                self.switch_weapon = True


        if not self.switch_spells:
            if current_time - self.time_switch_spells >= 200:
                self.switch_spells = True

        if not self.switch_score:
            if current_time - self.time_score >= 500:
                self.switch_weapon = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= 500:
                self.vulnerable = True

    def create_animation(self):
        animation = self.animation_status[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.graphic = animation[int(self.frame_index)] #int bo animation speed to float a python oczekuje intów
        self.rect = self.graphic.get_rect(center = self.hitbox.center)


        #miganie po obrazeniach
        if not self.vulnerable:
            self.graphic.set_alpha(self.wave_value())
        else:
            self.graphic.set_alpha(255)

    def damage(self):
        attack_level = self.stats['attack'] #full obrazenia to staty bohatera + staty broni
        damage_of_weapon = INFO_WEAPONS[self.weapon]['damage']
        combined_weapon_damage = attack_level + damage_of_weapon

        spells_level = self.stats['spells']
        damage_of_spells = INFO_SPELLS[self.spells]['strength']
        combined_spells_damage = spells_level + damage_of_spells

        return (combined_weapon_damage,combined_spells_damage)

    def update(self):
        self.froggo_input()
        self.cooldowns()
        self.get_status()
        self.create_animation()
        self.move(self.stats['speed'])
        #przywracanie many jeśli nie jest pełna
        if self.mana < self.stats['mana']:
            self.mana += 0.03 * self.stats['spells']
        else:
            self.mana = self.stats['mana']