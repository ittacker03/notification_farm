import pygame

# 화면에 띄우는 창을 나타내는 클래스
class Window:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.quit = pygame.Rect(x + width - 30, y, 30, 30)  # 종료 버튼 영역
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.quit)  # 종료 버튼을 빨간색으로 표시

class WindowManager:
    def __init__(self):
        self.windows = []

    def add_window(self, window):
        self.windows.append(window)
    def remove_window(self, window):
        if window in self.windows:
            self.windows.remove(window)
    def draw_windows(self, surface):
        for window in self.windows:
            window.draw(surface)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    window_manager = WindowManager()
    window1 = Window(100, 100, 200, 150)
    window2 = Window(300, 200, 200, 150)
    window_manager.add_window(window1)
    window_manager.add_window(window2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 마우스 우클릭시 윈도우 생성
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                new_window = Window(event.pos[0] - 100, event.pos[1] - 75, 200, 150)
                window_manager.add_window(new_window)
            # 윈도우 좌클릭 하면 windows 리스트에서 가장 위로 올리기
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for window in reversed(window_manager.windows):
                    if window.rect.collidepoint(event.pos):
                        window_manager.remove_window(window)
                        window_manager.add_window(window)
                        print(window_manager.windows)
                        break
            # 종료 버튼 클릭 이벤트 처리
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for window in window_manager.windows:
                    if window.quit.collidepoint(event.pos):
                        window_manager.remove_window(window)

            # 좌클릭하고 드래그하면 윈도우 이동
            # 가장 위에 있는 윈도우만 이동
            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                for window in reversed(window_manager.windows):
                    if window.rect.collidepoint(event.pos):
                        window.rect.x += event.rel[0]
                        window.rect.y += event.rel[1]
                        window.quit.x += event.rel[0]
                        window.quit.y += event.rel[1]
                        break



        screen.fill((0, 0, 0))
        window_manager.draw_windows(screen)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()