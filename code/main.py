import pygame, sys
from settings import *
from level import Level
from ui import Button


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('NinjaAd')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.death_music = pygame.mixer.Sound('../audio/playerdeath.wav')
        self.death_music.set_volume(1)
        self.intro_backgound = pygame.image.load('../graphics/bg/2background3.jpg')
        self.go_backgound = pygame.image.load('../graphics/bg/goground.jpg')
        self.guide_pic = pygame.image.load('../graphics/bg/guide2.jpg')
        # sound
        self.main_sound = pygame.mixer.Sound('../audio/main.wav')
        self.play_sound = pygame.mixer.Sound('../audio/playing.wav')
        self.go_sound = pygame.mixer.Sound('../audio/gameover.wav')
        self.main_sound.set_volume(0.5)
        self.go_sound.set_volume(0.5)
        self.play_sound.set_volume(0.5)
        self.running = True
        self.playing = True
        self.intro = True
        self.font = pygame.font.Font('../graphics/font/Aria.ttf', 72)
        self.restart = False

    def intro_screen(self):
        title = self.font.render('Ninja Adventure', True, BLACK)
        self.main_sound.play(loops=-1)
        title_rect = title.get_rect(x=400, y=200)
        play_button = Button(600, 300, 100, 50, WHITE, BLACK, 'Play', 32)
        guide_button = Button(600, 400, 100, 50, WHITE, BLACK, 'Guide', 32)
        exit_button = Button(600, 500, 100, 50, WHITE, BLACK, 'Exit', 32)
        while self.intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.intro = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro = False
                self.main_sound.stop()
            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False
                pygame.quit()
                sys.exit()
            if guide_button.is_pressed(mouse_pos, mouse_pressed):
                self.guide()

            self.screen.blit(self.intro_backgound, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(guide_button.image, guide_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def guide(self):
        check = True

        while check:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            back_button = Button(10, 720 - 60, 120, 50, WHITE, BLACK, 'Back', 32)
            self.screen.blit(self.guide_pic, (0, 0))
            self.screen.blit(back_button.image, back_button.rect)
            self.clock.tick(FPS)
            if back_button.is_pressed(mouse_pos, mouse_pressed):
                check = False
                self.main_sound.stop()
                self.intro_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

    def game_over(self):
        text = self.font.render('You Die', True, BLACK)
        self.go_sound.play(loops=-1)
        text_rect = text.get_rect(center=(1280 / 2, 720 / 2))
        restart_button = Button(10, 720 - 60, 120, 50, WHITE, BLACK, 'Again?', 32)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            self.screen.blit(self.go_backgound, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.go_sound.stop()
                self.main()
            pygame.display.update()

    def run(self):
        self.play_sound.play(loops=-1)
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
            if self.level.game_over:
                self.play_sound.stop()
                self.death_music.play(loops=0)
                self.playing = False
                self.game_over()
            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

    def main(self):
        self.__init__()
        self.intro_screen()
        while self.running:
            self.run()


if __name__ == '__main__':
    game = Game()
    game.main()
