from pg_extensions import *
from threading import Thread
from enum import Enum, auto


class State(Enum):
    SPRINTING = auto()
    DRINKING = auto()
    EATING = auto()
    ATTACKING = auto()


class Entity:
    def __init__(self, position, start_health, start_energy, move_speed, sprint_speed, color):
        self.position = position
        self.size = 0.5

        self.health = start_health
        self.start_energy = start_energy
        self.energy = start_energy

        self.move_speed = move_speed
        self.sprint_speed = sprint_speed
        self.target_speed = move_speed

        self.color = color

        self.state = State()

        self.is_prey = False
        self.is_alive = True

        self.move_direction = Vector2(0, 0)

    def drink(self):
        self.energy += 1

    def eat(self):
        self.energy += 50

    def kill(self, other):
        other.is_alive = False

    def update(self, closest_entity):
        if not self.is_alive:
            return

        if self.state == State.SPRINTING:
            self.target_speed = self.sprint_speed
            if self.move_direction.magnitude() != 0:
                self.energy -= 0.1

        elif self.state == State.DRINKING or self.state == State.EATING or self.state == State.ATTACKING:
            self.target_speed = 0

        else:
            self.target_speed = self.move_speed
            if self.move_direction.magnitude() != 0:
                self.energy -= 0.05

        if self.state == State.DRINKING:
            self.drink()
        if self.state == State.EATING:
            self.drink()
        if self.state == State.ATTACKING and closest_entity.is_prey:
            self.kill(closest_entity)

        self.energy = clamp(self.energy, 0, self.start_energy)

        self.position += self.move_direction * self.target_speed

    def render(self):
        draw_circle(window.SURFACE, self.color, self.position, self.size)


class Predator(Entity):
    def __init__(self, position, start_health, start_energy, move_speed, sprint_speed, color):
        super().__init__(position, start_health, start_energy, move_speed, sprint_speed, color)
        self.is_prey = False


class Prey(Entity):
    def __init__(self, position, start_health, start_energy, move_speed, sprint_speed, color):
        super().__init__(position, start_health, start_energy, move_speed, sprint_speed, color)
        self.is_prey = True


# Prolly wont use but i made it so not deleting
# class TickSystem:
#     def __init__(self):
#         self.tick = 0
#         self.running = False

#     def tick_updater(self, delay):
#         """
#         Starts a thread that increments the tick count every `delay` seconds.
#         """

#         def update_ticks():
#             while self.running:
#                 time.sleep(delay)
#                 self.tick += 1

#         self.running = True
#         updater_thread = Thread(target=update_ticks, daemon=True)
#         updater_thread.start()

#     def stop(self):
#         """
#         Stops the tick updater.
#         """
#         self.running = False


def start():
    global position, tick_system
    position = 0


def update():
    global window, position
    window = get_window()
    window.SURFACE.fill(WHITE.tup())

    if input_manager.get_key_down(pygame.K_ESCAPE):
        window.running = False

    set_window(window)


if __name__ == "__main__":
    run(start, update, 2560, 1440, True, "TENS - Testing Evolution and Natural Selection", 999)
