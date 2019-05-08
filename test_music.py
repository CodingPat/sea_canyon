import pygame,os


def main():
    screen=pygame.display.set_mode((800,600))
    main_dir=os.path.split(os.path.abspath(__file__))[0]
    
    if pygame.get_sdl_version()[0] == 2:
        print("mixer pre_init")
        pygame.mixer.pre_init(44100, 16, 2, 1024)
    pygame.init()
    #pygame.mixer.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    if pygame.mixer:
        #music = os.path.join(main_dir, 'music', '276557__tyops__arcade-intro_16bit.wav')
        
        music = os.path.join(main_dir, 'music', '276557__tyops__arcade-intro.ogg')
        
        #music = os.path.join(main_dir, 'music', '255597__akemov__underwater-ambience.ogg')
        
        print('play music {}'.format(music))
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    pygame.display.update()
    
    while True:
        pass
    
if __name__=='__main__':main()
