import os
import pygame as pg

if not pg.font:
    print("fonts are disabled!")
if not pg.mixer:
    print("sounds are disabled!")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass
    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound


class Fist(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)   # call sprite initializer
        self.image, self.rect = load_image("fist.png", -1)
        self.fist_offset = (-135, -80)
        self.punching = False

    def update(self):
        pos = pg.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move_ip(self.fist_offset)
        if self.punching:
            self.rect.move_ip(15, 25)

    def punch(self, target):
        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        self.punching = False


class Chimp(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("chimp.png", -1, 1)
        screeen = pg.display.get_surface()
        self.area = screeen.get_rect()
        self.rect.topleft = 10, 90
        self.move = 20
        self.dizzy = False

    def update(self):
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, True, False)
        self.rect = newpos

    def _spin(self):
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = False
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        if not self.dizzy:
            self.dizzy = True
            self.original = self.image

# RUN THE PROGRAM

pg.init()

screen = pg.display.set_mode((2280, 1400), pg.SCALED)
pg.display.set_caption("Monkey Fever")
pg.mouse.set_visible(False)

background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((170, 28, 187))

if pg.font:
    font = pg.font.Font(None, 64)
    heading = font.render("Smack the munkey,ern dollar's $$$$", True, (10, 10, 10))
    textpos = heading.get_rect(centerx=background.get_width() / 2, y=10)
    background.blit(heading, textpos)

    jk_message = font.render("juste kidding, noo meney for you!", True, (20, 20, 20))
    textposition = jk_message.get_rect(centerx=background.get_width() / 2, y=1000)
    background.blit(jk_message, textposition)

screen.blit(background, (0, 0))
pg.display.flip()

whiff_sound = load_sound("SmackPunch.mp3")
punch_sound = load_sound("SmackPunch.mp3")
chimp = Chimp()
fist = Fist()
allsprites = pg.sprite.RenderPlain((chimp, fist))
clock = pg.time.Clock()

going = True
while going:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            going = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            going = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if fist.punch(chimp):
                punch_sound.play()
                chimp.punched()
            else:
                whiff_sound.play()
        elif event.type == pg.MOUSEBUTTONUP:
            fist.unpunch()

    allsprites.update()
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pg.display.flip()
