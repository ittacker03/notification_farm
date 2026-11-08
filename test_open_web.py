import pygame
import webbrowser
import web_crawler

TEXT_SIZE = 20

pygame.init()

screen = pygame.display.set_mode((800, 600))

stnotice_crawler = web_crawler.STnotice_Crawler()
stnotice_list = stnotice_crawler.get_notices()
page = 1

left_page = pygame.Rect(50, 500, 100, 50)
right_page = pygame.Rect(650, 500, 100, 50)

texts = []
font = pygame.font.Font("font/malgun.ttf", TEXT_SIZE)
for notice in stnotice_list:
    text_surface = font.render(notice['title'], True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (0, 50 + len(texts) * TEXT_SIZE)
    texts.append((text_surface, text_rect, notice['url']))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if left_page.collidepoint(event.pos):
                    page -= 1
                elif right_page.collidepoint(event.pos):
                    page += 1
                if page < 1:
                    page = 1
                stnotice_crawler.set_page(page)
                stnotice_list = stnotice_crawler.get_notices()
                texts = []
                for notice in stnotice_list:
                    text_surface = font.render(notice['title'], True, (0, 0, 0))
                    text_rect = text_surface.get_rect()
                    text_rect.topleft = (0, 50 + len(texts) * TEXT_SIZE)
                    texts.append((text_surface, text_rect, notice['url']))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for text_surface, text_rect, url in texts:
                    if text_rect.collidepoint(event.pos):
                        webbrowser.open(url)

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), left_page)
    pygame.draw.rect(screen, (0, 0, 0), right_page)

    for text_surface, text_rect, url in texts:
        screen.blit(text_surface, text_rect)
        # You can add a click event to open the URL in a web browser


    pygame.display.flip()

pygame.quit()