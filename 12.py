import pygetwindow as gw
import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller
import threading

mouse = Controller()
time.sleep(0.5)


def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)


def find_and_click_green_pixels(window_rect):
    end_time = time.time() + 30  # Определяем время окончания через 30 секунд
    while time.time() < end_time:
        if paused:
            continue

        scrn = pyautogui.screenshot(
            region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3])
        )
        width, height = scrn.size

        for x in range(0, width, 10):  # Сокращаем шаг для более точного поиска
            for y in range(0, height, 10):  # Сокращаем шаг для более точного поиска
                r, g, b = scrn.getpixel((x, y))
                if (
                    (b in range(0, 125))
                    and (r in range(102, 220))
                    and (g in range(200, 255))
                ):
                    screen_x = window_rect[0] + x
                    screen_y = window_rect[1] + y
                    click(screen_x, screen_y)
                    time.sleep(0.001)


def click_play_again_button():
    # Пример координат кнопки "Играть снова". Обновите их по необходимости.
    play_again_x = 100  # Убедитесь, что это правильные координаты
    play_again_y = 750  # Убедитесь, что это правильные координаты
    click(play_again_x, play_again_y)
    time.sleep(0.1)


def find_red_pixels(window_rect):
    while True:
        if paused:
            continue

        scrn = pyautogui.screenshot(
            region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3])
        )
        width, height = scrn.size
        red_pixel_found = False

        for x in range(width):
            for y in range(height):
                r, g, b = scrn.getpixel((x, y))
                if (r, g, b) == (252, 118, 132):  # Пиксели в указанном диапазоне цвета
                    click(window_rect[0] + x, window_rect[1] + y)
                    red_pixel_found = True
                    break
            if red_pixel_found:
                break

        if red_pixel_found:
            print("Обнаружены пиксели красного цвета. Отключение поиска на 30 секунд.")
            time.sleep(30)
        else:
            time.sleep(3)


window_name = input("\n[✅] | Введите название окна (1 - TelegramDesktop): ")

if window_name == "1":
    window_name = "TelegramDesktop"

check = gw.getWindowsWithTitle(window_name)
if not check:
    print(f"[❌] | Окно - {window_name} не найдено!")
    exit()
else:
    print(f"[✅] | Окно найдено - {window_name}\n[✅] | Нажмите 'q' для паузы.")

telegram_window = check[0]
paused = False

# Запускаем поток для поиска красных пикселей
thread = threading.Thread(
    target=find_red_pixels,
    args=(
        (
            telegram_window.left,
            telegram_window.top,
            telegram_window.width,
            telegram_window.height,
        ),
    ),
)
thread.daemon = True
thread.start()

while True:
    if keyboard.is_pressed("q"):
        paused = not paused
        if paused:
            print("[✅] | Пауза.")
        else:
            print("[✅] | Продолжение работы.")
        time.sleep(0.2)

    if paused:
        continue

    window_rect = (
        telegram_window.left,
        telegram_window.top,
        telegram_window.width,
        telegram_window.height,
    )

    if telegram_window != []:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    # Кликаем по зеленым пикселям в течение 30 секунд
    find_and_click_green_pixels(window_rect)

    # После 30 секунд кликаем по кнопке "Играть снова"
    click_play_again_button()
    time.sleep(
        1
    )  # Задержка перед следующим циклом для предотвращения многократного клика

print("[✅] | Остановлено.")
