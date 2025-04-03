import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    points = []
    eraser_points = []
    mode = 'blue'
    drawing_shape = 'line'
    eraser_mode = False
    drawing_shape_active = False  # For shapes that require start and end positions
    shape_start_pos = None
    shapes = []  # Store all drawn shapes
    
    while True:
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
            
                # Color selection
                if event.key == pygame.K_r:
                    mode = 'red'
                    eraser_mode = False
                elif event.key == pygame.K_g:
                    mode = 'green'
                    eraser_mode = False
                elif event.key == pygame.K_b:
                    mode = 'blue'
                    eraser_mode = False
                elif event.key == pygame.K_e:  # Toggle eraser mode
                    eraser_mode = not eraser_mode
                elif event.key == pygame.K_c:  # Draw circle
                    drawing_shape = 'circle'
                elif event.key == pygame.K_x:  # Draw square
                    drawing_shape = 'square'
                elif event.key == pygame.K_l:  # Draw line
                    drawing_shape = 'line'
                elif event.key == pygame.K_t:  # Draw right triangle
                    drawing_shape = 'triangleR'
                elif event.key == pygame.K_y:  # Draw equilateral triangle
                    drawing_shape = 'triangleEq'
                elif event.key == pygame.K_h:  # Draw rhombus
                    drawing_shape = 'rhombus'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if eraser_mode:
                        eraser_points.append(event.pos)
                    else:
                        if drawing_shape == 'line':
                            points.append(event.pos)
                        elif drawing_shape in ['circle', 'square', 'triangleR', 'triangleEq', 'rhombus']:
                            drawing_shape_active = True
                            shape_start_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing_shape_active:
                    end_pos = event.pos
                    if not eraser_mode:
                        if drawing_shape == 'circle':
                            radius = int(math.hypot(end_pos[0] - shape_start_pos[0], 
                                         end_pos[1] - shape_start_pos[1]))
                            shapes.append(('circle', shape_start_pos, radius, get_color(mode)))
                        elif drawing_shape == 'square':
                            width = end_pos[0] - shape_start_pos[0]
                            height = end_pos[1] - shape_start_pos[1]
                            shapes.append(('square', shape_start_pos, width, height, get_color(mode)))
                        elif drawing_shape == 'triangleR':  # Right triangle
                            shapes.append(('triangleR', shape_start_pos, end_pos, get_color(mode)))
                        elif drawing_shape == 'triangleEq':  # Equilateral triangle
                            shapes.append(('triangleEq', shape_start_pos, end_pos, get_color(mode)))
                        elif drawing_shape == 'rhombus':  # Rhombus
                            shapes.append(('rhombus', shape_start_pos, end_pos, get_color(mode)))
                    drawing_shape_active = False
            
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Left mouse button pressed
                    if eraser_mode:
                        eraser_points.append(event.pos)
                        eraser_points = eraser_points[-256:]
                    else:
                        if drawing_shape == 'line':
                            points.append(event.pos)
                            points = points[-256:]

        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw all persistent shapes
        for shape in shapes:
            if shape[0] == 'circle':
                pygame.draw.circle(screen, shape[3], shape[1], shape[2])
            elif shape[0] == 'square':
                rect = pygame.Rect(shape[1][0], shape[1][1], shape[2], shape[3])
                pygame.draw.rect(screen, shape[4], rect)
            elif shape[0] == 'triangleR':  # Right triangle
                start, end = shape[1], shape[2]
                points = [
                    start,
                    (end[0], start[1]),
                    end
                ]
                pygame.draw.polygon(screen, shape[3], points)
            elif shape[0] == 'triangleEq':  # Equilateral triangle
                start, end = shape[1], shape[2]
                side_length = math.hypot(end[0] - start[0], end[1] - start[1])
                height = (math.sqrt(3)/2) * side_length
                
                # Calculate points for equilateral triangle
                points = [
                    start,
                    (end[0], end[1]),
                    ((start[0] + end[0])/2, start[1] - height)
                ]
                pygame.draw.polygon(screen, shape[3], points)
            elif shape[0] == 'rhombus':  # Rhombus
                start, end = shape[1], shape[2]
                center_x = (start[0] + end[0]) / 2
                center_y = (start[1] + end[1]) / 2
                width = abs(end[0] - start[0])
                height = abs(end[1] - start[1])
                
                points = [
                    (center_x, start[1]),  # Top point
                    (end[0], center_y),    # Right point
                    (center_x, end[1]),    # Bottom point
                    (start[0], center_y)    # Left point
                ]
                pygame.draw.polygon(screen, shape[3], points)
        
        # Draw current line (normal drawing)
        if drawing_shape == 'line':
            i = 0
            while i < len(points) - 1:
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
                i += 1
        
        # Draw eraser lines (black)
        i = 0
        while i < len(eraser_points) - 1:
            drawLineBetween(screen, i, eraser_points[i], eraser_points[i + 1], radius, 'black')
            i += 1
        
        # Draw preview of current shape being drawn
        if drawing_shape_active and shape_start_pos:
            current_pos = pygame.mouse.get_pos()
            color = get_color(mode)
            
            if drawing_shape == 'circle' and not eraser_mode:
                radius_preview = int(math.hypot(current_pos[0] - shape_start_pos[0], 
                                             current_pos[1] - shape_start_pos[1]))
                pygame.draw.circle(screen, color, shape_start_pos, radius_preview)
            elif drawing_shape == 'square' and not eraser_mode:
                width = current_pos[0] - shape_start_pos[0]
                height = current_pos[1] - shape_start_pos[1]
                rect = pygame.Rect(shape_start_pos[0], shape_start_pos[1], width, height)
                pygame.draw.rect(screen, color, rect)
            elif drawing_shape == 'triangleR' and not eraser_mode:  # Right triangle preview
                points = [
                    shape_start_pos,
                    (current_pos[0], shape_start_pos[1]),
                    current_pos
                ]
                pygame.draw.polygon(screen, color, points)
            elif drawing_shape == 'triangleEq' and not eraser_mode:  # Equilateral triangle preview
                side_length = math.hypot(current_pos[0] - shape_start_pos[0], 
                                       current_pos[1] - shape_start_pos[1])
                height = (math.sqrt(3)/2) * side_length
                
                points = [
                    shape_start_pos,
                    (current_pos[0], current_pos[1]),
                    ((shape_start_pos[0] + current_pos[0])/2, shape_start_pos[1] - height)
                ]
                pygame.draw.polygon(screen, color, points)
            elif drawing_shape == 'rhombus' and not eraser_mode:  # Rhombus preview
                center_x = (shape_start_pos[0] + current_pos[0]) / 2
                center_y = (shape_start_pos[1] + current_pos[1]) / 2
                
                points = [
                    (center_x, shape_start_pos[1]),  # Top point
                    (current_pos[0], center_y),      # Right point
                    (center_x, current_pos[1]),      # Bottom point
                    (shape_start_pos[0], center_y)    # Left point
                ]
                pygame.draw.polygon(screen, color, points)

        pygame.display.flip()
        clock.tick(60)

def get_color(color_mode):
    """Returns RGB color tuple based on color mode"""
    if color_mode == 'blue':
        return (0, 0, 255)
    elif color_mode == 'red':
        return (255, 0, 0)
    elif color_mode == 'green':
        return (0, 255, 0)
    elif color_mode == 'black':
        return (0, 0, 0)
    return (255, 255, 255)

def drawLineBetween(screen, index, start, end, width, color_mode):
    """Draws a line between two points with specified width and color"""
    color = get_color(color_mode)
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()