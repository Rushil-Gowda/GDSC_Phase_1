import pygame
import math

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Classroom")


boxes = []
y = 50
while y < 765:
    x = 50
    while x < 800:
        box = pygame.Rect(x, y, 50, 15)
        boxes.append(box)
        x += 150
    y += 50

cols = 5
rows = len(boxes) // cols


circles = []
lights = []


fan_centers = [6, 8, 21, 23, 36, 38, 51, 53, 66, 68]

for seat_id in fan_centers:

    box = boxes[seat_id]

    # exact center of blue rectangle
    cx = box.centerx
    cy = box.centery

    circles.append((cx, cy, 12))


for (cx, cy, r) in circles:
    lights.append((cx, cy - 50, 8)) 
    if cy > 600:
        lights.append((cx, cy + 50, 8)) 

    


 

selected_boxes = set()
selected_circles = set()
selected_lights = set()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

 
            for i, (cx, cy, r) in enumerate(circles):
                if math.hypot(event.pos[0] - cx, event.pos[1] - cy) <= r:
                    if i in selected_circles:
                        selected_circles.remove(i)
                    else:
                        selected_circles.add(i)

                    print("Fan clicked:", i)
                    break

            for i, box in enumerate(boxes):
                if box.collidepoint(event.pos):
                    if i in selected_boxes:
                        selected_boxes.remove(i)
                    else:
                        selected_boxes.add(i)

                    print("Seat clicked:", i)
                    break
            
  
            for i, (cx, cy, r) in enumerate(lights):
                if math.hypot(event.pos[0] - cx, event.pos[1] - cy) <= r:
                    if i in selected_lights:
                        selected_lights.remove(i)
                    else:
                        selected_lights.add(i)

                    print("Light clicked:", i)
                    break

    screen.fill((0, 0, 0))


    for i, box in enumerate(boxes):
        color = (0, 255, 0) if i in selected_boxes else (0, 150, 255)
        pygame.draw.rect(screen, color, box)


    for i, (cx, cy, r) in enumerate(circles):
        color = (255, 0, 0) if i in selected_circles else (255, 255, 255)
        pygame.draw.circle(screen, color, (cx, cy), r)


    for i, (cx, cy, r) in enumerate(lights):
        color = (255, 0, 200) if i in selected_lights else (200, 200, 0)
        pygame.draw.circle(screen, color, (cx, cy), r)

    pygame.display.flip()

pygame.quit()

print("Selected seats:", selected_boxes)
print("Selected fans:", selected_circles)
print("Selected lights:", selected_lights)


cols = 5
rows = len(boxes) // cols

# stores final clusters
fan_clusters = {}

# LOOP THROUGH ALL FANS to find the center of the coverage of the fan.


for fan_id, (fx, fy, r) in enumerate(circles):

    # FIND NEAREST SEAT TO THIS FAN, which is nothing but the seat directly below the fan

    nearest_seat = -1
    min_distance = float("inf")

    for seat_id, box in enumerate(boxes):

        sx, sy = box.center

        # distance between fan and seat
        distance = math.sqrt((fx - sx)**2 + (fy - sy)**2)

        # update nearest seat
        if distance < min_distance:
            min_distance = distance
            nearest_seat = seat_id

    # CONVERT SEAT NUMBER → ROW,COL, this for making the clusters in 3x3 manner as we are taking 3x3 as the range of the fan

    row = nearest_seat // cols
    col = nearest_seat % cols


    # BUILD 3x3 CLUSTER
    cluster = []

    # one row above to one row below
    for r in range(row - 1, row + 2):

        # one col left to one col right
        for c in range(col - 1, col + 2):

            # check classroom boundaries
            if 0 <= r < rows and 0 <= c < cols:

                seat_number = r * cols + c
                cluster.append(seat_number)

    # store cluster
    fan_clusters[fan_id] = cluster


# After making the clusters we are going to check each seat in the selected seats and map them to the corresponding fan.

active_fans = set()

for fanid,cluster in fan_clusters.items():
    
    for seat in selected_boxes:

        if seat in cluster:
            active_fans.add(fanid)
            break

print("Active fans: " + str(active_fans))





