import pygame
import blocks
BLOCK_WIDTH = 48
BLOCK_HEIGHT = 48


# pygame 초기화
pygame.init()
# 창 크기 설정 (마우스로 크기 조절 가능)
info = pygame.display.Info()
WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h - 60

display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
# 창 이름 설정
pygame.display.set_caption("Notification Farm")
# 창 tick 객체 생성
clock = pygame.time.Clock()
# 플레이어 이미지 설정 및 실제 크기 조정
player_img = pygame.image.load("pictures/player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
player_rect = player_img.get_rect()
# 플레이어 위치 설정
player_rect.centerx = WINDOW_WIDTH//2
player_rect.bottom = WINDOW_HEIGHT//2
# 백그라운드 이미지 설정
background_image = pygame.image.load("pictures/sky.jpg")
# 백그라운드 이미지 크기 전체화면에 맞게 조정
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
# 블록 리스트 생성
block_list = []
for i in range(3):
    for j in range(3):
        block = blocks.Block(
            48 * 10 + i * BLOCK_WIDTH,
            48 * 10 + j * BLOCK_HEIGHT,
            BLOCK_WIDTH,
            BLOCK_HEIGHT,
            "pictures/grass_block.png",
            order=2-j
        )
        block_list.append(block)


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
            display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            WINDOW_WIDTH, WINDOW_HEIGHT = display.get_size()
            # 백그라운드 이미지 화면크기에 맞게 조정
            background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # 플레이어 위치를 블록 크기의 격자에 맞춘다.
            grid_x = round(player_rect.x / BLOCK_WIDTH) * BLOCK_WIDTH
            grid_y = round(player_rect.y / BLOCK_HEIGHT) * BLOCK_HEIGHT

            # 같은 열에 있는 가장 가까운 위/아래 블록을 찾는다.
            grid_rect = pygame.Rect(grid_x, grid_y, BLOCK_WIDTH, BLOCK_HEIGHT)
            blocks_above = [
                block for block in block_list
                if block.rect.right > grid_rect.left
                and block.rect.left < grid_rect.right
                and block.rect.bottom <= grid_rect.top
            ]
            blocks_below = [
                block for block in block_list
                if block.rect.right > grid_rect.left
                and block.rect.left < grid_rect.right
                and block.rect.top >= grid_rect.bottom
            ]
            blocks_left = [
                block for block in block_list
                if block.rect.bottom > grid_rect.top
                and block.rect.top < grid_rect.bottom
                and block.rect.right <= grid_rect.left
            ]
            blocks_right = [
                block for block in block_list
                if block.rect.bottom > grid_rect.top
                and block.rect.top < grid_rect.bottom
                and block.rect.left >= grid_rect.right
            ]

            new_blk_x = grid_x
            new_blk_y = grid_y
            new_blk_order = 0
            if blocks_left:
                left_block = max(blocks_left, key=lambda block: block.rect.right)
                new_blk_x = left_block.rect.right
                new_blk_order = left_block.order
            elif blocks_right:
                right_block = min(blocks_right, key=lambda block: block.rect.left)
                new_blk_x = right_block.rect.left - BLOCK_WIDTH
                new_blk_order = right_block.order
            elif blocks_above:
                upper_block = max(blocks_above, key=lambda block: block.rect.bottom)
                new_blk_y = upper_block.rect.bottom
                new_blk_order = upper_block.order - 1
            elif blocks_below:
                lower_block = min(blocks_below, key=lambda block: block.rect.top)
                new_blk_y = lower_block.rect.top - BLOCK_HEIGHT
                new_blk_order = lower_block.order + 1

            block_rect = pygame.Rect(new_blk_x, new_blk_y, BLOCK_WIDTH, BLOCK_HEIGHT)

            # blocks_left, blocks_right, blocks_above, blocks_below 안에 블럭이 없으면 블럭을 만들지 않는다.
            if not (blocks_left or blocks_right or blocks_above or blocks_below):
                continue
            # 같은 격자 칸에 블록이 있을 때는 새 블록을 만들지 않는다.
            if not any(block.rect == block_rect for block in block_list):
                new_block = blocks.Block(
                    new_blk_x,
                    new_blk_y,
                    BLOCK_WIDTH,
                    BLOCK_HEIGHT,
                    "pictures/grass_block.png",
                )
                new_block.order = new_blk_order
                block_list.append(new_block)
                block_list.sort(key=lambda block: (block.layer, block.order), reverse=True)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 겹친 블록 중 화면에서 가장 앞에 있는 블록 확인
            for block in block_list:
                if block.rect.collidepoint(event.pos):
                    print(
                        f"Block at ({block.rect.x}, {block.rect.y}) - "
                        f"Size: ({block.rect.width}, {block.rect.height}) - "
                        # 블럭의 이미지 크기 출력
                        f"Image Size: {block.image.get_size()} - "
                        f"Layer: {block.layer}, Order: {block.order}"
                        
                    )
                    break
        # 키보드 i 누르면 블록 리스트의 원소 수 출력
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            print(f"Number of blocks: {len(block_list)}")

    # 플레이어 이동 키보드 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_rect.top > 0:
        player_rect.y -= 5
    if keys[pygame.K_a] and player_rect.left > 0:
        player_rect.x -= 5
    if keys[pygame.K_s] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += 5
    if keys[pygame.K_d] and player_rect.right < WINDOW_WIDTH:
        player_rect.x += 5
    # display에 이미지 그리고
    
    display.blit(background_image, (0, 0))

    # 블록 리스트를 순회하며 블록 그리기
    for block in block_list:
        block.draw(display)
    display.blit(player_img, player_rect)
    
    # 디스플레이 업데이트
    pygame.display.update()
    # tick 60fps로 설정
    clock.tick(60)
pygame.quit()