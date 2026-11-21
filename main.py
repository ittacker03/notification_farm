import pygame
import blocks
import player
import window
import webbrowser
import json

PLAYER_SPEED = 5
BLOCK_WIDTH = 48
BLOCK_HEIGHT = 48
DEF_WINDOW_WIDTH = 400
DEF_WINDOW_HEIGHT = 350
NOTI_WINDOW_WIDTH = 400
NOTI_WINDOW_HEIGHT = 400

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
try:
    player__ = player.load_player("./data/player_data.json")
except (FileNotFoundError, json.JSONDecodeError):
    player__ = player.User(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 48, 48, "./pictures/char_down.png", noti_seed=0)
# 백그라운드 이미지 설정
background_image = pygame.image.load("./pictures/sky.jpg")
# 백그라운드 이미지 크기 전체화면에 맞게 조정
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
# 윈도우 매니저 생성
window_manager = window.WindowManager()
# 각 윈도우 생성
storeitem_window = window.Store_Item_Window(100, 100, DEF_WINDOW_WIDTH, DEF_WINDOW_HEIGHT)
stnotice_window = window.STnotice_Window(100, 100, NOTI_WINDOW_WIDTH, NOTI_WINDOW_HEIGHT)
storeitem_window.add_item(blocks.Block(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, "pictures/grass_block.png"), 1)
storeitem_window.add_item(blocks.Block(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, "pictures/stone_block.png"), 1)
storeitem_window.add_item(blocks.Block(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, "pictures/wood_block.png"), 1)
storeitem_window.add_item(blocks.Method_Block(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT, "pictures/noti_block.png", method=lambda: window_manager.add_window(stnotice_window)), 0)
useritem_window = window.load_useritem_windows("./data/useritem_window_data.json", 100, 100, DEF_WINDOW_WIDTH, DEF_WINDOW_HEIGHT, window_manager, stnotice_window, storeitem_window)

# 블록 매니저 생성
block_manager = blocks.load_blocks("./data/block_data.json", window_manager, stnotice_window, storeitem_window)
# 플레이어가 들고 있는 블록
cur_block = None

# Running the main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player.save_player("./data/player_data.json", player__)
            blocks.save_blocks("./data/block_data.json", block_manager)
            window.save_useritem_windows("./data/useritem_window_data.json", useritem_window)
            running = False

        elif event.type == pygame.VIDEORESIZE:
            # 창 크기 조절 이벤트 처리
            display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            SCREEN_WIDTH, SCREEN_HEIGHT = display.get_size()
            # 백그라운드 이미지 화면크기에 맞게 조정
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        elif event.type == pygame.KEYDOWN:
            # block : 스페이스바를 누르면 플레이어 위치를 블록 크기의 격자에 맞춘 후, 가장 가까운 블록을 기준으로 새 블록을 생성
            if event.key == pygame.K_SPACE:
                if cur_block is None:
                    continue
                # 플레이어 위치를 블록 크기의 격자에 맞춘다.
                grid_x = round(player__.rect.x / BLOCK_WIDTH) * BLOCK_WIDTH
                grid_y = round(player__.rect.y / BLOCK_HEIGHT) * BLOCK_HEIGHT

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

                    block_state = useritem_window.remove_item(cur_block)
                    if block_state == "removed":
                        cur_block = None
            # block : r 누르면 플레이어 위치에 있는 블록 제거
            elif event.key == pygame.K_r:
                for block in block_manager.list:
                    if block.rect.colliderect(player__.rect):
                        block_manager.remove_block(block)
                        break
            # user item window : i 누르면 사용자 아이템 창 화면에 출력
            elif event.key == pygame.K_i:
                window_manager.add_window(useritem_window)
            # window : m 누르면 창 모두 화면 중앙에 위치
            elif event.key == pygame.K_m:
                window_manager.center_windows(SCREEN_WIDTH, SCREEN_HEIGHT)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                event_happend = False
                # method block : 클릭 이벤트 처리
                for block in block_manager.list:
                    # 클릭한 블록이 윈도우 위에 있는지 확인
                    is_window_above = False
                    for w in window_manager.windows:
                        if w.rect.collidepoint(event.pos):
                            is_window_above = True
                            break
                    if is_window_above:
                        continue
                    if block.rect.collidepoint(event.pos):
                        if isinstance(block, blocks.Method_Block):
                            block.execute_method()
                            event_happend = True
                        break
                if event_happend:
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
                # item window : 아이템 윈도우의 페이지 변경 버튼 클릭 처리
                for w in reversed(window_manager.windows):
                    if not isinstance(w, window.Item_Window):
                        continue
                    if w.page_left_button.collidepoint(event.pos):
                        w.prev_page()
                        break
                    if w.page_right_button.collidepoint(event.pos):
                        w.next_page()
                        break
                # user item window : 클릭한 윈도우 안의 아이템 클릭 처리
                for w in reversed(window_manager.windows):
                    if not isinstance(w, window.User_Item_Window):
                        continue
                    if w.rect.collidepoint(event.pos):
                        for item in w.items:
                            if item.rect.collidepoint(event.pos):
                                # 객체를 복사하기
                                cur_block = item.copy()
                                break
                        break
                # store item window : 클릭한 윈도우 안의 아이템 클릭 처리
                for w in reversed(window_manager.windows):
                    if not isinstance(w, window.Store_Item_Window) or not isinstance(player__, player.User):
                        continue
                    if w.rect.collidepoint(event.pos):
                        for item in w.items:
                            if item.rect.collidepoint(event.pos):
                                if w.get_price(item) <= player__.get_noti_seed():
                                    player__.subtract_noti_seed(w.get_price(item))
                                    useritem_window.add_item(item.copy())
                                break
                        break
                
                # stnotice window : 학사공지 클릭 처리
                for w in reversed(window_manager.windows):
                    if not isinstance(w, window.STnotice_Window):
                        break
                    if w.rect.collidepoint(event.pos):
                        for notice, notice_rect in zip(w.notices, w.notice_rects):
                            if notice_rect.collidepoint(event.pos):
                                webbrowser.open(notice['url'])
                                if isinstance(player__, player.User):
                                    player__.add_noti_seed(5)
                                break
                        break
                # stnotice window : 페이지 변경 버튼 클릭 처리
                for w in reversed(window_manager.windows):
                    if not isinstance(w, window.STnotice_Window):
                        break
                    if w.page_left_button.collidepoint(event.pos):
                        w.page_left()
                        break
                    if w.page_right_button.collidepoint(event.pos):
                        w.page_right()
                        break

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
    if isinstance(player__, player.User):
        keys = pygame.key.get_pressed()

        # 이동 후 플레이어의 발밑 검사
        def can_move(dx, dy):
            next_rect = player__.rect.copy()
            next_rect.x += dx
            next_rect.y += dy

            # 플레이어 발밑 전체 영역
            foot_rect = pygame.Rect(
                next_rect.left + next_rect.width // 4,
                next_rect.top + next_rect.height // 4,
                next_rect.width // 2,
                next_rect.height // 2,
            )

            return any(
                foot_rect.colliderect(block.rect)
                for block in block_manager.list
            )

        if keys[pygame.K_w] and player__.rect.top > 0 and can_move(0, -PLAYER_SPEED):
            player__.direction = "up"
            player__.rect.y -= PLAYER_SPEED

        if keys[pygame.K_a] and player__.rect.left > 0 and can_move(-PLAYER_SPEED, 0):
            player__.direction = "left"
            player__.rect.x -= PLAYER_SPEED

        if keys[pygame.K_s] and player__.rect.bottom < SCREEN_HEIGHT and can_move(0, PLAYER_SPEED):
            player__.direction = "down"
            player__.rect.y += PLAYER_SPEED

        if keys[pygame.K_d] and player__.rect.right < SCREEN_WIDTH and can_move(PLAYER_SPEED, 0):
            player__.direction = "right"
            player__.rect.x += PLAYER_SPEED

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player__.rect.top > 0:
            player__.direction = "up"
            player__.rect.y -= PLAYER_SPEED
        if keys[pygame.K_a] and player__.rect.left > 0:
            player__.direction = "left"
            player__.rect.x -= PLAYER_SPEED
        if keys[pygame.K_s] and player__.rect.bottom < SCREEN_HEIGHT:
            player__.direction = "down"
            player__.rect.y += PLAYER_SPEED
        if keys[pygame.K_d] and player__.rect.right < SCREEN_WIDTH:
            player__.direction = "right"
            player__.rect.x += PLAYER_SPEED
    

    # display에 백그라운드 이미지 그리기
    display.blit(background_image, (0, 0))
    # 블록 리스트를 순회하며 블록 그리기
    block_manager.draw_blocks(display)
    # 플레이어 이미지 그리기
    player__.draw(display)
    # 플레이어의 위치를 블록 크기의 격자에 맞춘 사각형 그리기
    grid_rect = pygame.Rect(round(player__.rect.x / BLOCK_WIDTH) * BLOCK_WIDTH, round(player__.rect.y / BLOCK_HEIGHT) * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT)
    pygame.draw.rect(display, (255, 0, 0), grid_rect, 2)
    # User의 noti_seed 표시
    if isinstance(player__, player.User):
        font = pygame.font.Font("./font/NanumGothic.ttf", 20)
        noti_seed_text = f"Noti Seed: {player__.get_noti_seed()}"
        text_surface = font.render(noti_seed_text, True, (0, 0, 0))
        display.blit(text_surface, (10, 10))

    # 윈도우 매니저에 있는 모든 윈도우 그리기
    window_manager.draw_windows(display)
    # 디스플레이 업데이트
    pygame.display.update()
    # tick 60fps로 설정
    clock.tick(60)
pygame.quit()