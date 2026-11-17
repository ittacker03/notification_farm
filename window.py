import pygame
import blocks
import web_crawler

# 화면에 띄우는 창을 나타내는 클래스
class Window:
    def __init__(self, x, y, width, height, title="Default Window"):
        self.rect = pygame.Rect(x, y, width, height) # 창 영역
        self.quit = pygame.Rect(x + width - 30, y, 30, 30)  # 종료 버튼 영역
        # 창 안에 텍스트 추가
        self.title = title
        self.font = pygame.font.Font("./font/NanumGothic.ttf", 30)
        self.title_surface = self.font.render(self.title, True, (0, 0, 0))
        self.title_rect = self.title_surface.get_rect()
        self.title_rect.topleft = (self.rect.x + 5, self.rect.y + 5)

        self.basic_rects = [self.rect, self.quit, self.title_rect]
        self.elements = []
        self.elements.append(self.basic_rects)
    
    def draw(self, surface):
        # 기본 창
        pygame.draw.rect(surface, (255, 255, 255), self.rect) # 창 배경색
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)  # 창 외곽선

        # 종료 버튼
        pygame.draw.rect(surface, (255, 0, 0), self.quit) # 종료 버튼 배경색  
        pygame.draw.rect(surface, (0, 0, 0), self.quit, 2) # 종료 버튼 외곽선
        pygame.draw.line(surface, (0, 0, 0), (self.quit.x + 5, self.quit.y + 5), (self.quit.x + 25, self.quit.y + 25), 2) # 종료 버튼 안에 x 표시
        pygame.draw.line(surface, (0, 0, 0), (self.quit.x + 5, self.quit.y + 25), (self.quit.x + 25, self.quit.y + 5), 2) # 종료 버튼 안에 x 표시

        # 텍스트
        surface.blit(self.title_surface, self.title_rect)

class Item_Window(Window):
    def __init__(self, x, y, width, height, title="아이템"):
        super().__init__(x, y, width, height, title)
        self.items = []
        self.item_rects = []
        self.elements.append(self.item_rects)

        self.pages = []
        self.cur_page = 1

        # 페이지 변경 버튼
        self.page_left_button = pygame.Rect(self.rect.x + 10, self.rect.y + self.rect.height - 40, 30, 30)
        self.page_right_button = pygame.Rect(self.page_left_button.x + self.page_left_button.width + 10, self.rect.y + self.rect.height - 40, 30, 30)
        self.elements.append([self.page_left_button, self.page_right_button])
    # 창 크기에 맞게 아이템 위치 조정
    def adjust_item_positions(self):
        self.pages = []

        if not self.items:
            self.cur_page = 1
            self.pages.append([])
            return

        left_space = 30
        top_space = 50
        right_space = 10
        bottom_space = 20

        start_x = self.rect.x + left_space
        start_y = self.rect.y + top_space

        max_x = self.rect.right - right_space
        max_y = self.rect.bottom - bottom_space

        # 아이템 행 단위 배치
        rows = []
        cur_row = []
        x = start_x
        row_height = 0
        for item in self.items:
            item_width, item_height = item.image.get_size()
            # 아이템이 창의 오른쪽 경계를 넘어가면 다음 줄로 이동
            if cur_row and x + item_width > max_x:
                rows.append((cur_row, row_height))
                cur_row = []
                x = start_x
                row_height = 0

            cur_row.append((item, x))
            x += item_width + 10
            row_height = max(row_height, item_height)
        if cur_row:
            rows.append((cur_row, row_height))
        # 페이지 분리
        page = []
        y = start_y
        for row, height in rows:
            if page and y + height > max_y:
                self.pages.append(page)
                page = []
                y = start_y
            for item, item_x in row:
                page.append((item, item_x, y))
            y += height + 20
        if page:
            self.pages.append(page)

        # 페이지 범위 보정
        if self.cur_page > len(self.pages):
            self.cur_page = len(self.pages)
        # 현재 페이지의 아이템 위치 갱신
        self.update_cur_page()
        
    def update_cur_page(self):
        self.item_rects.clear()

        if not self.pages:
            return
        for item, x, y in self.pages[self.cur_page - 1]:
            item.rect.topleft = (x, y)
            self.item_rects.append(item.rect)

    def next_page(self):
        if self.cur_page < len(self.pages):
            self.cur_page += 1
            self.adjust_item_positions() # 아이템 위치 조정

    def prev_page(self):
        if self.cur_page > 1:
            self.cur_page -= 1
            self.adjust_item_positions() # 아이템 위치 조정

    def add_item(self, item):
        self.items.append(item)
        self.adjust_item_positions() # 아이템 위치 조정

    def remove_item(self, item):
        if item is None:
            return
        item_kind = []
        for it in self.items:
            if it.image_path == item.image_path:
                item_kind.append(it)
        if len(item_kind) > 0:
            rm_item = item_kind[len(item_kind) - 1]
            self.items.remove(rm_item)
            self.adjust_item_positions() # 아이템 위치 조정

    def draw(self, surface):
        super().draw(surface)

        # 아이템이 그려질 수 있는 영역 제한
        content_rect = pygame.Rect(
            self.rect.x + 10,
            self.rect.y + 40,
            self.rect.width - 20,
            self.rect.height - 50
        )

        old_clip = surface.get_clip()
        surface.set_clip(content_rect.clip(old_clip))

        if self.pages:
            for item, x, y in self.pages[self.cur_page - 1]:
                surface.blit(item.image, item.rect)

        surface.set_clip(old_clip)

        # 페이지 이동 버튼 그리기
        pygame.draw.rect(surface, (200, 200, 200), self.page_left_button)
        pygame.draw.rect(surface, (200, 200, 200), self.page_right_button)
        pygame.draw.polygon(surface, (0, 0, 0), [(self.page_left_button.x + 20, self.page_left_button.y + 5), (self.page_left_button.x + 10, self.page_left_button.y + 15), (self.page_left_button.x + 20, self.page_left_button.y + 25)])
        pygame.draw.polygon(surface, (0, 0, 0), [(self.page_right_button.x + 10, self.page_right_button.y + 5), (self.page_right_button.x + 20, self.page_right_button.y + 15), (self.page_right_button.x + 10, self.page_right_button.y + 25)])

class User_Item_Window(Item_Window):
    def __init__(self, x, y, width, height, title = "사용자 아이템"):
        super().__init__(x, y, width, height, title)
        self.items_nums = {}
    # 아이템의 image_path를 받아서 해당 아이템이 이미 존재하면 개수만 증가, 없으면 새로 추가
    def add_item(self, item):
        if item.image_path in self.items_nums:
            self.items_nums[item.image_path] += 1
        else:
            self.items_nums[item.image_path] = 1
            super().add_item(item)
        print(self.items_nums)
    def remove_item(self, item):
        if item.image_path in self.items_nums:
            self.items_nums[item.image_path] -= 1
            if self.items_nums[item.image_path] <= 0:
                del self.items_nums[item.image_path]
                super().remove_item(item)
                return "removed"
        print(self.items_nums)
    def draw(self, surface):
        super().draw(surface)
        for item in self.items:
            count = self.items_nums.get(item.image_path, 0)
            if count > 1:
                font = pygame.font.Font("./font/NanumGothic.ttf", 20)
                text_surface = font.render(str(count), True, (0, 0, 0))
                text_rect = text_surface.get_rect()
                text_rect.bottomright = item.rect.bottomright
                surface.blit(text_surface, text_rect)

class STnotice_Window(Window):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, title="학사공지")
        self.page = 1

        self.font_size = 14
        self.font = pygame.font.Font("./font/NanumGothic.ttf", self.font_size)

        self.notices = []
        self.notice_rects = []
        self.page_left_button = pygame.Rect(self.rect.x + 10, self.rect.y + self.rect.height - 40, 30, 30)
        self.page_right_button = pygame.Rect(self.page_left_button.x + self.page_left_button.width + 10, self.rect.y + self.rect.height - 40, 30, 30)
        self.elements.append(self.notice_rects)
        self.elements.append([self.page_left_button, self.page_right_button])

        self.crawler = web_crawler.STnotice_Crawler()
        self.update_notices()
    def update_notices(self):
        rightest_x = 0

        self.notices.clear()
        self.notice_rects.clear()
        for notice in self.crawler.get_notices():
            text_surface = self.font.render(notice['title'], True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.rect.x + 10, self.rect.y + 50 + len(self.notices) * (self.font_size + 1))
            self.notices.append(notice)
            self.notice_rects.append(text_rect)
            rightest_x = max(rightest_x, text_rect.right + 10)

        self.rect.width = rightest_x - self.rect.x
        self.quit.x = self.rect.right - 30
            
    def set_page(self, page):
        self.crawler.set_page(page)
        self.update_notices()
    def page_right(self):
        self.page += 1
        self.set_page(self.page)
    def page_left(self):
        if self.page > 1:
            self.page -= 1
            self.set_page(self.page)
    def draw(self, surface):
        super().draw(surface)
        # 공지사항 리스트 그리기
        for notice, text_rect in zip(self.notices, self.notice_rects):
            text_surface = self.font.render(notice['title'], True, (0, 0, 0))
            surface.blit(text_surface, text_rect)
        # 마우스 오버 시 공지사항 강조 표시
        mouse_pos = pygame.mouse.get_pos()
        for notice, text_rect in zip(self.notices, self.notice_rects):
            if text_rect.collidepoint(mouse_pos):
                text_surface = self.font.render(notice['title'], True, (0, 0, 0))
                pygame.draw.rect(surface, (200, 200, 200), text_rect)
                surface.blit(text_surface, text_rect)
                break
        # 페이지 이동 버튼 그리기
        pygame.draw.rect(surface, (200, 200, 200), self.page_left_button)
        pygame.draw.rect(surface, (200, 200, 200), self.page_right_button)
        pygame.draw.polygon(surface, (0, 0, 0), [(self.page_left_button.x + 20, self.page_left_button.y + 5), (self.page_left_button.x + 10, self.page_left_button.y + 15), (self.page_left_button.x + 20, self.page_left_button.y + 25)])
        pygame.draw.polygon(surface, (0, 0, 0), [(self.page_right_button.x + 10, self.page_right_button.y + 5), (self.page_right_button.x + 20, self.page_right_button.y + 15), (self.page_right_button.x + 10, self.page_right_button.y + 25)])

class WindowManager:
    def __init__(self):
        self.windows = []
    def add_window(self, window):
        # window 안에 클래스가 똑같은 객체가 이미 존재하면 그 객체는 추가 안함
        for existing_window in self.windows:
            if window.__class__ == existing_window.__class__:
                return
        self.windows.append(window)
    def remove_window(self, window):
        if window in self.windows:
            self.windows.remove(window)
    def draw_windows(self, surface):
        for window in self.windows:
            window.draw(surface)
    # window의 모든 element를 이동시키는 함수
    def move_windows(self, window, dx, dy):
        if window in self.windows:
            for element in window.elements:
                for sub_element in element:
                    sub_element.x += dx
                    sub_element.y += dy
    # 모든 window를 화면 중앙에 위치시키는 함수
    def center_windows(self, screen_width, screen_height):
        extra_x = 0
        extra_y = 0
        for window in self.windows:
            dx = (screen_width - window.rect.width) // 2 - window.rect.x
            dy = (screen_height - window.rect.height) // 2 - window.rect.y
            self.move_windows(window, dx + extra_x, dy + extra_y)
            extra_x += 5
            extra_y -= 5

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 320

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    window_manager = WindowManager()
    item_window = Item_Window(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    for i in range(20):
        grass_block = blocks.Block(200, 200, 48, 48, "pictures/grass_block.png")
        stone_block = blocks.Block(200, 200, 48, 48, "pictures/stone_block.png")
        item_window.add_item(grass_block)
        item_window.add_item(stone_block)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 마우스가 눌렸을 때
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 좌클릭
                if event.button == 1:
                    # 클릭한 윈도우를 가장 위로 올리기
                    for window in reversed(window_manager.windows):
                        if window.rect.collidepoint(event.pos):
                            window_manager.remove_window(window)
                            window_manager.add_window(window)
                            break
                    # 종료 버튼 클릭 이벤트 처리
                    for window in reversed(window_manager.windows):
                        if window.quit.collidepoint(event.pos):
                            window_manager.remove_window(window)
                            break
                    # 클릭한 윈도우 안의 아이템 클릭 처리
                    for window in reversed(window_manager.windows):
                        if not isinstance(window, Item_Window):
                            continue
                        if window.rect.collidepoint(event.pos):
                            for item in window.items:
                                if item.rect.collidepoint(event.pos):
                                    print(f"Item clicked: {item.image_path}")
                                    break
                            break
                # 우클릭: 새로운 윈도우 생성
                elif event.button == 3:
                    new_window = Window(event.pos[0] - WINDOW_WIDTH // 2, event.pos[1] - WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT)
                    window_manager.add_window(new_window)
            # 좌클릭하고 드래그하면 윈도우 이동
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                for window in reversed(window_manager.windows):
                    if window.rect.collidepoint(event.pos):
                        for element in window.elements:
                            for sub_element in element:
                                sub_element.x += event.rel[0]
                                sub_element.y += event.rel[1]
                        break
            # m 누르면 창 모두 화면 중앙에 위치
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                window_manager.center_windows(screen.get_width(), screen.get_height())
                break
            # b 누르면 item_window window_manager에 추가
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                window_manager.add_window(item_window)
                # item_window의 items 출력
                print("Current items in item_window:")
                for i, item in enumerate(item_window.items):
                    print(f"Item {i}: {item.image_path}")
                break
            # w 누르면 window_manager의 windows 출력
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                print("Current windows:")
                for i, window in enumerate(window_manager.windows):
                    print(f"Window {i}: {window}")
                break

        # 배경색을 파란색으로 설정
        screen.fill((0, 0, 255))
        # 모든 윈도우 띄우기
        window_manager.draw_windows(screen)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()