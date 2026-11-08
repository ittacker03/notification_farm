import pygame
import webbrowser

pygame.init()

screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font("font/malgun.ttf", 30)

page = 5
title = "맑은 고딕"
url = f'https://www.seoultech.ac.kr/service/info/matters/?bidx=6112&bnum=6112&allboard=true&page={page}&size=12&searchtype=1&searchtext='
text = font.render(title, True, (0, 0, 255))
text_rect = text.get_rect(topleft=(100, 100))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if text_rect.collidepoint(event.pos):
                    webbrowser.open(url)

    screen.fill((255, 255, 255))
    screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()