from pg_extensions import *
from threading import Thread


def tick_updater(delay):
    """
    Increment tick variable every x milliseconds

    Args:
        delay: in milliseconds, how much time between each tick
    """
    global tick

    while window.running:
        time.sleep(delay * 1000)
        tick += 1


def start():
    global position, tick
    position = 0
    tick = 0

    tick_updater_thread = Thread(target=tick_updater, args=[50])
    tick_updater_thread.start()


def update():
    global window, position
    window = get_window()
    window.SURFACE.fill(BLACK.tup())

    if input_manager.get_key_down(pygame.K_ESCAPE):
        window.running = False

    print(tick)
    position += 5
    draw_circle(window.SURFACE, WHITE, Vector2(position, 0), 50)

    set_window(window)


if __name__ == "__main__":
    run(start, update, 2560, 1440, True, "TENS - Testing Evolution and Natural Selection", 999)
