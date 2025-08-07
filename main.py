import pygame
import math
import sys

# ---------- parameters ----------
WIDTH, HEIGHT = 800, 800
FPS                = 60

OCT_RADIUS         = 300          # distance from centre to any vertex
OCT_ROT_SPEED      = math.radians(10) / FPS   # ~10° per second

BALL_RADIUS        = 15
BALL_SPEED         = 350          # pixels per second, initial speed

# ---------- helpers ----------
def regular_octagon(radius):
    """Return the 8 points of a unit regular octagon centred at the origin."""
    return [
        pygame.math.Vector2(
            radius * math.cos(math.pi/4 + i * math.pi/4),
            radius * math.sin(math.pi/4 + i * math.pi/4)
        ) for i in range(8)
    ]

def outward_normal(p1, p2):
    """Clockwise ordering → outward normal = (dy, −dx) normalised."""
    edge = p2 - p1
    normal = pygame.math.Vector2(edge.y, -edge.x)
    return normal.normalize()

# ---------- init ----------
pygame.init()
screen  = pygame.display.set_mode((WIDTH, HEIGHT))
clock   = pygame.time.Clock()

centre  = pygame.math.Vector2(WIDTH/2, HEIGHT/2)
base_oct= regular_octagon(OCT_RADIUS)

ball_pos   = centre + pygame.math.Vector2(0, -OCT_RADIUS/2)
ball_vel   = pygame.math.Vector2(BALL_SPEED, 0).rotate(37)  # any direction

angle = 0.0  # current rotation of the octagon (radians)

# ---------- main loop ----------
while True:
    dt = clock.tick(FPS) / 1000  # seconds since last frame

    # --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- update octagon rotation ---
    angle += OCT_ROT_SPEED * dt * FPS
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    octagon = [centre + pygame.math.Vector2(
                    v.x * cos_a - v.y * sin_a,
                    v.x * sin_a + v.y * cos_a) for v in base_oct]

    # --- move ball ---
    ball_pos += ball_vel * dt

    # --- collision detection & response ---
    for i in range(8):
        p1 = octagon[i]
        p2 = octagon[(i + 1) % 8]
        n  = outward_normal(p1 - centre, p2 - centre)  # outward normal
        dist = n.dot(ball_pos - p1)                   # signed distance
        if dist > -BALL_RADIUS:                       # penetration or contact
            # push ball just inside
            ball_pos -= (dist + BALL_RADIUS) * n
            # reflect velocity
            ball_vel -= 2 * ball_vel.dot(n) * n

    # --- draw ---
    screen.fill((30, 30, 30))
    pygame.draw.polygon(screen, (80, 80, 200), octagon, width=3)
    pygame.draw.circle(screen, (255, 230, 0), ball_pos, BALL_RADIUS)
    pygame.display.flip()
