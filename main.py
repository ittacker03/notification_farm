import pygame

# pygame 초기화
pygame.init()
# 창 크기 설정 (마우스로 크기 조절 가능)
display_size = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
WINDOW_WIDTH, WINDOW_HEIGHT = display_size.get_size()
# 창 이름 설정
pygame.display.set_caption("Notification Farm")
# 창 tick 객체 생성
clock = pygame.time.Clock()
# 플레이어 이미지 설정 및 실제 크기 조정
player_img = pygame.image.load("pictures/player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
player_rect = player_img.get_rect()
player_rect.centerx = (WINDOW_WIDTH//2)
player_rect.bottom = (WINDOW_HEIGHT//2)
# 백그라운드 이미지 설정
background_image = pygame.image.load("pictures/sky.jpg")
# 백그라운드 이미지 크기 전체화면에 맞게 조정
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
# 게임이 동작하는 동안 이벤트
x = 0
y = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # 창 크기 조절 이벤트 처리
            display_size = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            WINDOW_WIDTH, WINDOW_HEIGHT = display_size.get_size()
            # 백그라운드 이미지 화면크기에 맞게 조정
            background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    # 키보드 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_rect.top > 0:
        player_rect.y -= 5
    if keys[pygame.K_a] and player_rect.left > 0:
        player_rect.x -= 5
    if keys[pygame.K_s] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += 5
    if keys[pygame.K_d] and player_rect.right < WINDOW_WIDTH:
        player_rect.x += 5
    # 백그라운드 이미지 붙이기
    display_size.blit(background_image, (0, 0))
    display_size.blit(player_img, player_rect)
    # 디스플레이 업데이트
    pygame.display.update()
    # tick 60fps로 설정
    clock.tick(60)
pygame.quit()