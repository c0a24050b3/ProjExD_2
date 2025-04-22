import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数が：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横、縦）
    画面内ならTrue､外ならFaluse
    """
    yoko,tate = True,True #yokototatehoukounohennsuu
    if rct.left <0 or WIDTH < rct.right: #gamennnaidattara
        yoko = False
    if rct.top <0 or HEIGHT < rct.bottom :
        tate = False
    return yoko,tate



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) 
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    clock = pg.time.Clock()
    vx,vy = +5,+5
    clock = pg.time.Clock()
    tmr = 0
    
    def gameover(screen: pg.Surface) -> None: #ゲームオーバーの条件
        kuro =pg.Surface((WIDTH,HEIGHT))
        kuro.fill((0,0,0))
        kuro.set_alpha(150)
        screen.blit(kuro,(0,0)) 

        kk_cry = pg.image.load("fig/8.png")
        kk_cry1_rect = kk_cry.get_rect(center=(WIDTH//3,HEIGHT//2))
        kk_cry2_rect = kk_cry.get_rect(center=(2*WIDTH//3,HEIGHT//2))
        screen.blit(kk_cry,kk_cry1_rect)
        screen.blit(kk_cry,kk_cry2_rect)

        font = pg.font.Font(None,80)
        txt = font.render("Game Over",True,(255,255,255))
        txt_rect = txt.get_rect(center=(WIDTH//2,HEIGHT//2))

        screen.blit(txt,txt_rect)

        

        pg.display.update()
        time.sleep(5)

    def init_bb_imgs() -> tuple [list[pg.Surface], list[int]]:
        bb_accs = [a for a in range (1, 11)]
        bb_imgs = [b for b in range (1, 10)]
        for r in range(1, 11): 
            bb_img = pg.Surface ((20*r, 20*r))
            pg.draw.circle (bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
            avx = vx*bb_accs [min(tmr//500, 9)]
            bb_img = bb_imgs [min(tmr//500, 9)]
    


    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        bb_imgs, bb_accs = init_bb_imgs() 
        avx = vx*bb_accs[min(tmr//500, 9)] 
        bb_img = bb_imgs[min(tmr//500, 9)]
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct): 
            gameover(screen)

        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #sayuuhoukou 
                sum_mv[1] += mv[1] #jougehoukou

        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True): #壁の爆弾反射
            kk_rct.move_in(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        screen.blit(bb_img, bb_rct)
        yoko,tate=check_bound(bb_rct)
        print(yoko)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr *= 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
