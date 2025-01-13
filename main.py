from pg_extensions import *
from threading import Thread


class TickSystem:
    def __init__(self):
        self.tick = 0
        self.running = False

    def tick_updater(self, delay):
        """
        Starts a thread that increments the tick count every `delay` seconds.
        """

        def update_ticks():
            while self.running:
                time.sleep(delay)
                self.tick += 1

        self.running = True
        updater_thread = Thread(target=update_ticks, daemon=True)
        updater_thread.start()

    def stop(self):
        """
        Stops the tick updater.
        """
        self.running = False


def start():
    global position, tick_system
    position = 0

    tick_system = TickSystem()
    tick_system.tick_updater(1 / 20)


def update():
    global window, position
    window = get_window()
    window.SURFACE.fill(BLACK.tup())

    if input_manager.get_key_down(pygame.K_ESCAPE):
        window.running = False

    set_window(window)


if __name__ == "__main__":
    run(start, update, 2560, 1440, True, "TENS - Testing Evolution and Natural Selection", 999)
    tick_system.stop()
