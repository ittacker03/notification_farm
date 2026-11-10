import pygame
import blocks
import player
import window
import webbrowser

BLOCK_WIDTH = 48
BLOCK_HEIGHT = 48
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 320

# pygame 초기화
pygame.init()
# 창 크기 설정 (마우스로 크기 조절 가능)
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h - 60
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
# 창 이름 설정
pygame.display.set_caption("Notification Farm")
# 창 tick 객체 생성
clock = pygame.time.Clock()
# 플레이어 설정
player = player.Player(
    SCREEN_WIDTH//2,
    SCREEN_HEIGHT//2,
    50,
    50,
    "pictures/player.png"
)
# 백그라운드 이미지 설정
background_image = pygame.image.load("pictures/sky.jpg")
# 백그라운드 이미지 크기 전체화면에 맞게 조정
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
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
# 윈도우 매니저 생성
window_manager = window.WindowManager()
# 아이템 윈도우, 공지 윈도우 생성
item_window = window.Item_Window(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
notice_window = window.Notice_Window(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

item_window.add_item(blocks.Block(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, "pictures/grass_block.png"))
item_window.add_item(blocks.Block(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, "pictures/stone_block.png"))
item_window.add_item(blocks.Block(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, "pictures/wood_block.png"))
item_window.add_item(blocks.Method_Block(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, "pictures/noti_block.png", method=lambda: window_manager.add_window(notice_window)))

cur_block = blocks.Block(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, "pictures/grass_block.png")


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
            SCREEN_WIDTH, SCREEN_HEIGHT = display.get_size()
            # 백그라운드 이미지 화면크기에 맞게 조정
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Event Type : KEYDOWN
        elif event.type == pygame.KEYDOWN:
            # block : 스페이스바를 누르면 플레이어 위치를 블록 크기의 격자에 맞춘 후, 가장 가까운 블록을 기준으로 새 블록을 생성
            if event.key == pygame.K_SPACE:
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
                    new_block = cur_block.copy()
                    new_block.rect.x = new_blk_x
                    new_block.rect.y = new_blk_y
                    new_block.order = new_blk_order

                    block_manager.add_block(new_block)
                    block_manager.sort_blocks()
            # block : i 누르면 블록 개수 출력
            elif event.key == pygame.K_i:
                print(f"Number of blocks: {len(block_manager.list)}")
            # window : b 누르면 아이템 창 화면에 출력
            elif event.key == pygame.K_b:
                window_manager.add_window(item_window)
            # window : m 누르면 창 모두 화면 중앙에 위치
            elif event.key == pygame.K_m:
                window_manager.center_windows(SCREEN_WIDTH, SCREEN_HEIGHT)
            # window : n 누르면 공지 창 화면에 출력
            elif event.key == pygame.K_n:
                window_manager.add_window(notice_window)
        # Event Type : MOUSEBUTTONDOWN
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # blocks : 블록 클릭 이벤트 처리
                for block in block_manager.list:
                    if block.rect.collidepoint(event.pos):
                        if isinstance(block, blocks.Method_Block):
                            block.execute_method()
                        break
                # window : 클릭한 윈도우를 가장 위로 올리기
                for w in reversed(window_manager.windows):
                    if w.rect.collidepoint(event.pos):
                        window_manager.remove_window(w)
                        window_manager.add_window(w)
                        break
                # window : 종료 버튼 클릭 이벤트 처리
                for w in reversed(window_manager.windows):
                    if w.quit.collidepoint(event.pos):
                        window_manager.remove_window(w)
                        break
                # window : 클릭한 윈도우 안의 아이템 클릭 처리
                for w in reversed(window_manager.windows):
                    if not isinstance(w, window.Item_Window):
                        continue
                    if w.rect.collidepoint(event.pos):
                        for item in w.items:
                            if item.rect.collidepoint(event.pos):
                                # 객체를 복사하기
                                cur_block = item.copy()
                                break
                        break
                # window : 클릭한 윈도우 안의 공지 클릭 처리
                for w in reversed(window_manager.windows):
                    if not isinstance(w, window.Notice_Window):
                        continue
                    if w.rect.collidepoint(event.pos):
                        for notice, notice_rect in zip(w.notices, w.notice_rects):
                            if notice_rect.collidepoint(event.pos):
                                webbrowser.open(notice['url'])
                                break
                        break
        # Event Type : MOUSEMOTION
        elif event.type == pygame.MOUSEMOTION:
            # window : 좌클릭하고 드래그하면 윈도우 이동
            if event.buttons[0]:
                for w in reversed(window_manager.windows):
                    if w.rect.collidepoint(event.pos):
                        for element in w.elements:
                            for sub_element in element:
                                sub_element.x += event.rel[0]
                                sub_element.y += event.rel[1]
                        break

    # 플레이어 이동 키보드 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.rect.top > 0:
        player.rect.y -= 5
    if keys[pygame.K_a] and player.rect.left > 0:
        player.rect.x -= 5
    if keys[pygame.K_s] and player.rect.bottom < SCREEN_HEIGHT:
        player.rect.y += 5
    if keys[pygame.K_d] and player.rect.right < SCREEN_WIDTH:
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
    # 윈도우 매니저에 있는 모든 윈도우 그리기
    window_manager.draw_windows(display)
    # 디스플레이 업데이트
    pygame.display.update()
    # tick 60fps로 설정
    clock.tick(60)
pygame.quit()