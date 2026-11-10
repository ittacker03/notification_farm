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
        self.font = pygame.font.Font("font/malgun.ttf", 30)
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
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, title="아이템")
        self.items = []
        self.item_rects = []
        self.elements.append(self.item_rects)
        # 창 크기에 맞게 아이템 위치 조정
    def adjust_item_positions(self):
        if not self.items:
            return

        left_space = 30
        top_space = 50
        x = self.rect.x + left_space
        y = self.rect.y + top_space
        row_height = 0

        for item in self.items:
            item_width, item_height = item.image.get_size()

            # 아이템이 창의 오른쪽 경계를 넘어가면 다음 줄로 이동
            if x != self.rect.x + left_space and x + item_width > self.rect.right - 10:
                x = self.rect.x + left_space
                y += row_height + 20
                # 왜 row_height = 0을 여기서 해주지 않으면 row_height가 계속 누적되어서 아이템이 겹쳐서 나오는 문제가 발생함
                row_height = 0

            item.rect.topleft = (x, y)
            x += item_width + 10
            row_height = max(row_height, item_height)
    def add_item(self, item):
        self.items.append(item)
        self.item_rects.append(item.rect)
        self.adjust_item_positions() # 아이템 위치 조정
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            self.item_rects.remove(item.rect)
            self.adjust_item_positions() # 아이템 위치 조정
    def draw(self, surface):
        super().draw(surface)
        for item in self.items:
            surface.blit(item.image, item.rect)

# web_crawler.py에서 가져온 공지사항 크롤러를 이용한 공지사항 창
class Notice_Window(Window):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, title="Notice")
        self.notices = []
        self.notice_rects = []
        self.elements.append(self.notice_rects)
        self.crawler = web_crawler.STnotice_Crawler()
        self.update_notices()
    def update_notices(self):
        self.notices.clear()
        self.notice_rects.clear()
        font = pygame.font.Font("font/malgun.ttf", 20)
        for notice in self.crawler.get_notices():
            text_surface = font.render(notice['title'], True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.rect.x + 10, self.rect.y + 50 + len(self.notices) * 30)
            self.notices.append(notice)
            self.notice_rects.append(text_rect)
    def draw(self, surface):
        super().draw(surface)
        for notice, text_rect in zip(self.notices, self.notice_rects):
            # why text_surface is needed to be created here? because if it is created in update_notices, the text_surface will be created only once, and when the notice title changes, the text_surface will not change. So it needs to be created here to reflect the current notice title.
            text_surface = pygame.font.Font("font/malgun.ttf", 20).render(notice['title'], True, (0, 0, 0))
            surface.blit(text_surface, text_rect)

class WindowManager:
    def __init__(self):
        self.windows = []
    def add_window(self, window):
        # window 안에 클래스가 똑같은 객체가 이미 존재하면 그 객체는 추가 안함
        for existing_window in self.windows:
            if isinstance(existing_window, type(window)):
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