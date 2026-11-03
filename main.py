import pygame
import blocks
import player

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
# 플레이어 설정
player = player.Player(
    WINDOW_WIDTH//2,
    WINDOW_HEIGHT//2,
    50,
    50,
    "pictures/player.png"
)
# 백그라운드 이미지 설정
background_image = pygame.image.load("pictures/sky.jpg")
# 백그라운드 이미지 크기 전체화면에 맞게 조정
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
# 블록 매니저 생성
block_manager = blocks.BlockManager()
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
        block_manager.list.append(block)
# 현재 선택된 블럭
cur_block = "pictures/grass_block.png"


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
        # 스페이스바를 누르면 플레이어 위치를 블록 크기의 격자에 맞춘 후, 가장 가까운 블록을 기준으로 새 블록을 생성
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # 플레이어 위치를 블록 크기의 격자에 맞춘다.
            grid_x = round(player.rect.x / BLOCK_WIDTH) * BLOCK_WIDTH
            grid_y = round(player.rect.y / BLOCK_HEIGHT) * BLOCK_HEIGHT

            # 같은 열에 있는 가장 가까운 위/아래 블록을 찾는다.
            grid_rect = pygame.Rect(grid_x, grid_y, BLOCK_WIDTH, BLOCK_HEIGHT)
            blocks_above = [
                block for block in block_manager.list
                if block.rect.right > grid_rect.left
                and block.rect.left < grid_rect.right
                and block.rect.bottom <= grid_rect.top
            ]
            blocks_below = [
                block for block in block_manager.list
                if block.rect.right > grid_rect.left
                and block.rect.left < grid_rect.right
                and block.rect.top >= grid_rect.bottom
            ]
            blocks_left = [
                block for block in block_manager.list
                if block.rect.bottom > grid_rect.top
                and block.rect.top < grid_rect.bottom
                and block.rect.right <= grid_rect.left
            ]
            blocks_right = [
                block for block in block_manager.list
                if block.rect.bottom > grid_rect.top
                and block.rect.top < grid_rect.bottom
                and block.rect.left >= grid_rect.right
            ]
            
            # blocks_left, blocks_right, blocks_above, blocks_below 안에 블럭이 없으면 블럭을 만들지 않는다.
            if not (blocks_left or blocks_right or blocks_above or blocks_below):
                continue

            left_block = None
            right_block = None
            upper_block = None
            lower_block = None
            candidates = []
            if blocks_left:
                left_block = max(blocks_left, key=lambda block: block.rect.right)
                distance = grid_rect.left - left_block.rect.right
                candidates.append(("left", distance, left_block))

            if blocks_right:
                right_block = min(blocks_right, key=lambda block: block.rect.left)
                distance = right_block.rect.left - grid_rect.right
                candidates.append(("right", distance, right_block))

            if blocks_above:
                upper_block = max(blocks_above, key=lambda block: block.rect.bottom)
                distance = grid_rect.top - upper_block.rect.bottom
                candidates.append(("above", distance, upper_block))

            if blocks_below:
                lower_block = min(blocks_below, key=lambda block: block.rect.top)
                distance = lower_block.rect.top - grid_rect.bottom
                candidates.append(("below", distance, lower_block))

            # 방향과 가장 가까운 블록을 함께 기억한다.
            direction, _, nearest_block = min(candidates, key=lambda candidate: candidate[1])

            new_blk_x = grid_x
            new_blk_y = grid_y
            new_blk_order = nearest_block.order

            if direction == "left":
                new_blk_x = nearest_block.rect.right

            elif direction == "right":
                new_blk_x = nearest_block.rect.left - BLOCK_WIDTH

            elif direction == "above":
                new_blk_y = nearest_block.rect.bottom
                new_blk_order = nearest_block.order - 1

            elif direction == "below":
                new_blk_y = nearest_block.rect.top - BLOCK_HEIGHT
                new_blk_order = nearest_block.order + 1
            
            # 같은 격자 칸에 블록이 있을 때는 새 블록을 만들지 않는다. and 플레이어 격자 칸과 새 블록 격자가 겹칠 때만 새 블록을 만든다.
            block_rect = pygame.Rect(new_blk_x, new_blk_y, BLOCK_WIDTH, BLOCK_HEIGHT)
            if not any(block.rect == block_rect for block in block_manager.list) and grid_rect.colliderect(block_rect):
                new_block = blocks.Block(
                    new_blk_x,
                    new_blk_y,
                    BLOCK_WIDTH,
                    BLOCK_HEIGHT,
                    cur_block,
                    order=new_blk_order
                )
                block_manager.add_block(new_block)
                block_manager.sort_blocks()
        # 겹친 블록 중 화면에서 가장 앞에 있는 블록 확인
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for block in block_manager.list:
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
            print(f"Number of blocks: {len(block_manager.list)}")
        # 키보드 r 누르면 블록 바꾸기
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if cur_block == "pictures/grass_block.png":
                cur_block = "pictures/stone_block.png"
            else:
                cur_block = "pictures/grass_block.png"

    # 플레이어 이동 키보드 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.rect.top > 0:
        player.rect.y -= 5
    if keys[pygame.K_a] and player.rect.left > 0:
        player.rect.x -= 5
    if keys[pygame.K_s] and player.rect.bottom < WINDOW_HEIGHT:
        player.rect.y += 5
    if keys[pygame.K_d] and player.rect.right < WINDOW_WIDTH:
        player.rect.x += 5
    # display에 백그라운드 이미지 그리기
    display.blit(background_image, (0, 0))
    # 블록 리스트를 순회하며 블록 그리기
    block_manager.draw_blocks(display)
    # 플레이어 이미지 그리기
    display.blit(player.image, player.rect)
    # 플레이어의 위치를 블록 크기의 격자에 맞춘 사각형 그리기
    grid_rect = pygame.Rect(
        round(player.rect.x / BLOCK_WIDTH) * BLOCK_WIDTH,
        round(player.rect.y / BLOCK_HEIGHT) * BLOCK_HEIGHT,
        BLOCK_WIDTH,
        BLOCK_HEIGHT
    )
    pygame.draw.rect(display, (255, 0, 0), grid_rect, 2)
    # 디스플레이 업데이트
    pygame.display.update()
    # tick 60fps로 설정
    clock.tick(60)
pygame.quit()