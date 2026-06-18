import math

def normalize(v):
    mag = math.sqrt(sum(x*x for x in v))
    return [x/mag for x in v] if mag > 0 else v

def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def sub(a, b):
    return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]

def get_normal(pts_3d):
    if len(pts_3d) < 3: return [0,0,1]
    v1 = sub(pts_3d[1], pts_3d[0])
    v2 = sub(pts_3d[2], pts_3d[0])
    return normalize(cross(v1, v2))

# Point of view: Top-Right-Forward, looking FROM BELOW, approx 10 degrees up
# Z adjusted from -120 to -60 to flatten the angle
eye = [200, 250, -60]  
target = [0, 0, 0]
up = [0, 0, 1]

z_axis = normalize(sub(eye, target))
x_axis = normalize(cross(up, z_axis))
y_axis = cross(z_axis, x_axis)

def project(p):
    vec = sub(p, eye)
    cx = dot(x_axis, vec)
    cy = dot(y_axis, vec)
    cz = dot(z_axis, vec)
    
    scale = 1.6
    screen_x = 400 + cx * scale
    screen_y = 300 - cy * scale
    return screen_x, screen_y, cz

visible_faces = []

body_h = 40
# Body - Group 2.0 (Height 40)
profile = [
    (-40, -20), # Back-Bottom
    (30, -20),  # Front-Bottom Start
    (40, -12),  # Front-Bottom End (Chamfer)
    (40, 12),   # Front-Top Start
    (30, 20),   # Front-Top End (Chamfer)
    (-40, 20)   # Back-Top
]
body_r = [(40, y, z) for y, z in profile]
body_l = [(-40, y, z) for y, z in profile]

body_faces = []
body_faces.append({'verts': body_r, 'color': '#add8e6'})
body_faces.append({'verts': body_l[::-1], 'color': '#add8e6'})
for i in range(len(profile)):
    next_i = (i + 1) % len(profile)
    face = [body_r[i], body_l[i], body_l[next_i], body_r[next_i]]
    body_faces.append({'verts': face, 'color': '#add8e6'})

for f in body_faces:
    pts = f['verts']
    normal = get_normal(pts)
    c_x = sum(p[0] for p in pts) / len(pts)
    c_y = sum(p[1] for p in pts) / len(pts)
    c_z = sum(p[2] for p in pts) / len(pts)
    view_vec = sub(eye, [c_x, c_y, c_z])
    if dot(normal, view_vec) > -0.01:
        proj_pts = [project(p)[:2] for p in pts]
        depths = [project(p)[2] for p in pts]
        visible_faces.append({
            'pts_2d': proj_pts,
            'depth': sum(depths)/len(depths),
            'group': 2.0,
            'color': f['color'],
            'stroke': 6
        })

# Head - Group 1.0 
# Height is 3/4 of body height = 30
# Raised by 1/6 of body height above body = 40/6 = 6.67
head_h = 30.0
head_z_base = 20.0 + (body_h / 6.0)
head_z_top = head_z_base + head_h
head_profile = [(-20, head_z_base), (40, head_z_base), (40, head_z_top), (-20, head_z_top)]
head_r = [(25, y, z) for y, z in head_profile]
head_l = [(-25, y, z) for y, z in head_profile]

head_faces = []
head_faces.append({'verts': head_r, 'color': '#add8e6'})
head_faces.append({'verts': head_l[::-1], 'color': '#add8e6'})
for i in range(len(head_profile)):
    next_i = (i + 1) % len(head_profile)
    face = [head_r[i], head_l[i], head_l[next_i], head_r[next_i]]
    head_faces.append({'verts': face, 'color': '#add8e6'})

for f in head_faces:
    pts = f['verts']
    normal = get_normal(pts)
    c_x = sum(p[0] for p in pts) / len(pts)
    c_y = sum(p[1] for p in pts) / len(pts)
    c_z = sum(p[2] for p in pts) / len(pts)
    view_vec = sub(eye, [c_x, c_y, c_z])
    if dot(normal, view_vec) > -0.01:
        proj_pts = [project(p)[:2] for p in pts]
        depths = [project(p)[2] for p in pts]
        visible_faces.append({
            'pts_2d': proj_pts,
            'depth': sum(depths)/len(depths),
            'group': 1.0,
            'color': f['color'],
            'stroke': 6
        })

# Eyes - Group 4.0
eye_z_center = (head_z_base + head_z_top) / 2.0
for cx_eye in [-12, 12]:
    eye_verts = []
    for i in range(20):
        theta = 2 * math.pi * i / 20
        vx = cx_eye + 6 * math.cos(theta)
        vz = eye_z_center + 6 * math.sin(theta)
        eye_verts.append((vx, 40.5, vz))
    proj_pts = [project(p)[:2] for p in eye_verts]
    depths = [project(p)[2] for p in eye_verts]
    visible_faces.append({
        'pts_2d': proj_pts,
        'depth': sum(depths)/len(depths),
        'group': 4.0,
        'color': 'white',
        'stroke': 4
    })

# Wheels - 2D Convex Hull
def convex_hull(points):
    points = sorted(list(set(points)))
    if len(points) <= 1: return points
    def cross_2d(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_2d(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_2d(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def add_wheel_2d(cx, cy, cz, radius, thickness, color, group_hull, group_cap):
    N = 40
    pts_inner = []
    pts_outer = []
    for i in range(N):
        theta = 2 * math.pi * i / N
        y = cy + radius * math.cos(theta)
        z = cz + radius * math.sin(theta)
        pts_inner.append((cx, y, z))
        pts_outer.append((cx + thickness, y, z))
        
    proj_inner = [project(p)[:2] for p in pts_inner]
    proj_outer = [project(p)[:2] for p in pts_outer]
    
    hull = convex_hull(proj_inner + proj_outer)
    
    center_3d = (cx + thickness/2, cy, cz)
    vec = sub(center_3d, eye)
    depth = dot(z_axis, vec)
    
    visible_faces.append({
        'pts_2d': hull,
        'depth': depth,
        'group': group_hull,
        'color': color,
        'stroke': 6
    })
    visible_faces.append({
        'pts_2d': proj_outer,
        'depth': depth,
        'group': group_cap,
        'color': color,
        'stroke': 6
    })

# Wheel diameter = 40. Radius = 20.
add_wheel_2d(40.1, 20, -10, 20, 20, '#add8e6', 3.0, 3.1)   # Front Right
add_wheel_2d(40.1, -20, -10, 20, 20, '#add8e6', 3.0, 3.1)  # Back Right
add_wheel_2d(-40.1, 20, -10, 20, -20, '#add8e6', 0.0, 0.1) # Front Left
add_wheel_2d(-40.1, -20, -10, 20, -20, '#add8e6', 0.0, 0.1)# Back Left

visible_faces.sort(key=lambda f: (f['group'], f['depth']))

svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">']
for face in visible_faces:
    pts_str = " ".join([f"{px:.2f},{py:.2f}" for px, py in face['pts_2d']])
    svg.append(f'<polygon points="{pts_str}" fill="{face["color"]}" stroke="black" stroke-width="{face["stroke"]}" stroke-linejoin="round"/>')
svg.append('</svg>')

with open("robot.svg", "w") as f:
    f.write("\n".join(svg))
print("Created robot.svg successfully!")
