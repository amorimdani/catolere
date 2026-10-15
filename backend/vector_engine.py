import os
import math
import random
import hashlib
from PIL import Image, ImageDraw, ImageFilter

def analyze_figure_identity(figure_name: str) -> dict:
    nl = figure_name.lower().strip()
    
    is_michael = any(k in nl for k in ["miguel", "arcanjo são miguel", "sao miguel", "são miguel"])
    is_gabriel = any(k in nl for k in ["gabriel"])
    is_raphael = any(k in nl for k in ["rafael"])
    is_angel = is_michael or is_gabriel or is_raphael or any(k in nl for k in ["arcanjo", "anjo", "querubim", "serafim"])
    
    is_george = any(k in nl for k in ["jorge"])
    is_expedite = any(k in nl for k in ["expedito"])
    is_sebastian = any(k in nl for k in ["sebastião", "sebastiao"])
    is_warrior = is_michael or is_george or is_expedite or is_sebastian or any(k in nl for k in ["soldado", "guerreiro"])
    
    is_francis = any(k in nl for k in ["francisc", "chico", "assis"])
    is_anthony = any(k in nl for k in ["antonio", "antônio"])
    is_benedict = any(k in nl for k in ["bento", "benedito"])
    is_padre_pio = any(k in nl for k in ["pio", "padre pio"])
    is_monk = is_francis or is_anthony or is_benedict or is_padre_pio or any(k in nl for k in ["frade", "monge", "ermitão", "clara"])
    
    is_mary = any(k in nl for k in ["maria", "senhora", "fátima", "fatima", "aparecida", "lourdes", "carmo", "virgem", "guadalupe", "conceição", "madona", "desatadora"])
    is_teresa = any(k in nl for k in ["teresa", "calcutá", "calcuta", "madre"]) and not is_mary
    is_lucy = any(k in nl for k in ["luzia", "lucia"])
    is_female = is_mary or is_teresa or is_lucy or any(k in nl for k in ["santa", "rita", "cecília", "cecilia", "bárbara", "barbara", "irmã", "dulce"])
    
    is_joseph = any(k in nl for k in ["josé", "jose", "carpinteiro"]) and not is_francis
    is_jesus = any(k in nl for k in ["jesus", "cristo", "bom pastor", "messias", "salvador", "coração de jesus", "sagrado coração"]) and not is_joseph
    is_peter = any(k in nl for k in ["pedro", "apóstolo", "apostolo", "pescador"]) and not is_jesus
    is_moses = any(k in nl for k in ["moisés", "moises", "mar vermelho", "sinai", "mandamentos", "profeta", "patriarca", "abraão", "elias", "noé"]) and not is_jesus
    
    return {
        "is_michael": is_michael,
        "is_gabriel": is_gabriel,
        "is_raphael": is_raphael,
        "is_angel": is_angel,
        "is_george": is_george,
        "is_expedite": is_expedite,
        "is_sebastian": is_sebastian,
        "is_warrior": is_warrior,
        "is_francis": is_francis,
        "is_anthony": is_anthony,
        "is_benedict": is_benedict,
        "is_padre_pio": is_padre_pio,
        "is_monk": is_monk,
        "is_mary": is_mary,
        "is_teresa": is_teresa,
        "is_lucy": is_lucy,
        "is_female": is_female,
        "is_joseph": is_joseph,
        "is_jesus": is_jesus,
        "is_peter": is_peter,
        "is_moses": is_moses
    }


def get_bezier_points(p0, p1, p2, p3, steps=40):
    """Calcula pontos suaves de uma curva cúbica de Bézier."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u*u*u * p0[0] + 3*u*u*t * p1[0] + 3*u*t*t * p2[0] + t*t*t * p3[0]
        y = u*u*u * p0[1] + 3*u*u*t * p1[1] + 3*u*t*t * p2[1] + t*t*t * p3[1]
        pts.append((float(x), float(y)))
    return pts

def draw_smooth_curve(draw, p0, p1, p2, p3, width=5, fill="black", steps=40):
    """Renderiza curva de Bézier contínua e suave."""
    pts = get_bezier_points(p0, p1, p2, p3, steps)
    draw.line([(int(x), int(y)) for x, y in pts], fill=fill, width=width, joint="curve")

def draw_star(draw, cx, cy, r_outer, r_inner, points=5, fill="black"):
    """Estrela geométrica proporcional."""
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        ang = i * math.pi / points - math.pi / 2
        pts.append((int(cx + r * math.cos(ang)), int(cy + r * math.sin(ang))))
    draw.polygon(pts, fill=fill)

def draw_rose(draw, cx, cy, radius=16):
    """Flor/rosa detalhada de livro infantil."""
    draw.circle((cx, cy), radius, outline="black", width=4)
    draw.arc([cx - radius + 4, cy - radius + 4, cx + radius - 4, cy + radius - 4], 45, 270, fill="black", width=3)
    draw.arc([cx - radius + 8, cy - radius + 8, cx + radius - 8, cy + radius - 8], 225, 90, fill="black", width=3)
    # Pétalas externas
    for p in range(5):
        ang = p * (math.pi * 2 / 5)
        px = cx + math.cos(ang) * (radius + 6)
        py = cy + math.sin(ang) * (radius + 6)
        draw.arc([int(px - 6), int(py - 6), int(px + 6), int(py + 6)], 0, 360, fill="black", width=3)

def draw_ornate_halo(draw, cx, cy, radius=135, is_mary=False, is_jesus=False, halo_style=0):
    """Auréola sagrada profissional, ornamental e radiante."""
    # Anel externo principal
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline="black", width=6)
    # Anel intermediário decorativo com pontilhado ou friso duplo
    draw.ellipse([cx - radius + 10, cy - radius + 10, cx + radius - 10, cy + radius - 10], outline="black", width=3)
    draw.ellipse([cx - radius + 18, cy - radius + 18, cx + radius - 18, cy + radius - 18], outline="black", width=2)

    if is_jesus:
        # Auréola cruciforme com raios de glória
        for rad in [0, math.pi/2, math.pi, 3*math.pi/2]:
            x1 = cx + math.cos(rad) * (radius - 18)
            y1 = cy + math.sin(rad) * (radius - 18)
            x2 = cx + math.cos(rad) * (radius + 24)
            y2 = cy + math.sin(rad) * (radius + 24)
            draw.line([(x1, y1), (x2, y2)], fill="black", width=7)
            # Travessas da cruz na auréola
            perp = rad + math.pi/2
            for offset in [-8, 8]:
                draw.line([
                    (x2 + math.cos(perp)*offset, y2 + math.sin(perp)*offset),
                    (x1 + math.cos(perp)*offset, y1 + math.sin(perp)*offset)
                ], fill="black", width=3)
    elif is_mary:
        # Coroa celestial de 12 estrelas brilhantes
        for s in range(12):
            ang = s * (math.pi * 2 / 12) - math.pi / 2
            sx = cx + math.cos(ang) * (radius + 24)
            sy = cy + math.sin(ang) * (radius + 24)
            draw_star(draw, sx, sy, 9, 4, points=5, fill="black")
            # Pequeno raio radiante entre estrelas
            ray_ang = ang + (math.pi / 12)
            rx1 = cx + math.cos(ray_ang) * (radius + 4)
            ry1 = cy + math.sin(ray_ang) * (radius + 4)
            rx2 = cx + math.cos(ray_ang) * (radius + 16)
            ry2 = cy + math.sin(ray_ang) * (radius + 16)
            draw.line([(rx1, ry1), (rx2, ry2)], fill="black", width=3)
    else:
        # Raios solares ornamentais com pontas alternadas e contas
        ray_count = 24
        for i in range(ray_count):
            deg = i * (360 / ray_count)
            rad = math.radians(deg)
            is_major = (i % 2 == 0)
            r_start = radius + 6
            r_end = radius + (26 if is_major else 14)
            
            x_start = cx + math.cos(rad) * r_start
            y_start = cy + math.sin(rad) * r_start
            x_end = cx + math.cos(rad) * r_end
            y_end = cy + math.sin(rad) * r_end
            draw.line([(x_start, y_start), (x_end, y_end)], fill="black", width=4 if is_major else 3)
            
            if is_major:
                draw.circle((int(cx + math.cos(rad) * (r_end + 5)), int(cy + math.sin(rad) * (r_end + 5))), 3, fill="black")

def draw_charming_face(draw, cx, cy, is_female=False, is_child=False):
    """Rosto com proporções ilustradas de alta qualidade (storybook cute)."""
    hw, hh = (54, 62) if is_child else (66, 76)
    
    # Contorno suave do rosto com queixo delicado
    draw.ellipse([cx - hw, cy - hh, cx + hw, cy + hh - 4], outline="black", width=6)
    
    # Orelhas delicadas
    draw.arc([cx - hw - 10, cy - 6, cx - hw + 8, cy + 20], 90, 270, fill="black", width=4)
    draw.arc([cx + hw - 8, cy - 6, cx + hw + 10, cy + 20], 270, 450, fill="black", width=4)

    # Olhos expressivos com brilho duplo e profundidade de ilustração
    eye_dx, eye_y = 28, cy - 6
    for ed in [-eye_dx, eye_dx]:
        # Globo ocular
        draw.ellipse([cx + ed - 14, eye_y - 15, cx + ed + 14, eye_y + 15], fill="black")
        # Brilho de luz primário (grande)
        draw.ellipse([cx + ed - 7, eye_y - 10, cx + ed - 1, eye_y - 3], fill="white")
        # Brilho de luz secundário (pequeno)
        draw.ellipse([cx + ed + 3, eye_y + 4, cx + ed + 7, eye_y + 8], fill="white")
        # Arco da pálpebra superior / cílios
        draw.arc([cx + ed - 15, eye_y - 20, cx + ed + 15, eye_y - 6], 190, 350, fill="black", width=5)
        
        if is_female:
            # Cílios charmosos
            side = 1 if ed > 0 else -1
            draw.line([(cx + ed + side*13, eye_y - 11), (cx + ed + side*20, eye_y - 17)], fill="black", width=4)
            draw.line([(cx + ed + side*11, eye_y - 5), (cx + ed + side*18, eye_y - 8)], fill="black", width=3)
        
        # Bochecha corada sutil
        draw.line([(cx + ed - 10, eye_y + 24), (cx + ed + 10, eye_y + 24)], fill="black", width=3)

    # Sobrancelhas suaves e amigáveis
    draw_smooth_curve(draw, (cx - 42, cy - 30), (cx - 30, cy - 38), (cx - 18, cy - 35), (cx - 10, cy - 24), width=4)
    draw_smooth_curve(draw, (cx + 10, cy - 24), (cx + 18, cy - 35), (cx + 30, cy - 38), (cx + 42, cy - 30), width=4)

    # Nariz sutil de botão
    draw.arc([cx - 5, cy + 10, cx + 5, cy + 18], 0, 180, fill="black", width=4)

    # Sorriso iluminado e acolhedor
    draw.arc([cx - 20, cy + 22, cx + 20, cy + 44], 0, 180, fill="black", width=5)
    # Covinhas do sorriso
    draw.line([(cx - 23, cy + 26), (cx - 19, cy + 22)], fill="black", width=3)
    draw.line([(cx + 23, cy + 26), (cx + 19, cy + 22)], fill="black", width=3)

def draw_detailed_wings(draw, cx, cy, wing_span=285):
    """Asas de anjo/arcanjo majestosas e ricas em penas em 3 níveis."""
    for side in [-1, 1]:
        bx = cx + side * 75
        # 1. Envergadura principal superior
        draw_smooth_curve(draw, (bx, cy + 25), (cx + side * (wing_span * 0.7), cy - 165), (cx + side * wing_span, cy - 60), (cx + side * (wing_span + 10), cy + 50), width=6)
        
        # 2. Penas primárias externas longas
        for p in range(5):
            py = cy - 40 + p * 55
            px_out = cx + side * (wing_span + 10 - p * 30)
            draw_smooth_curve(draw, (bx + side * 50, py), (px_out, py + 20), (px_out - side * 20, py + 70), (bx + side * 30, cy + 260), width=4)
            # Frisos internos da pena
            draw.line([(int(bx + side * 45), int(py + 15)), (int(px_out - side * 25), int(py + 30))], fill="black", width=2)
            
        # 3. Penas secundárias e penugem no ombro da asa
        for c in range(4):
            arc_y = cy - 70 + c * 40
            x0 = int(bx + side * 15)
            x1 = int(bx + side * 75)
            draw.arc([min(x0, x1), int(arc_y), max(x0, x1), int(arc_y + 35)], 0, 180, fill="black", width=3)

def generate_professional_coloring_art(figure_name: str, situation_idx: int, seed: int) -> Image.Image:
    """Motor de ilustração 2D de alta fidelidade para livros de colorir católicos."""
    name_hash = int(hashlib.md5(figure_name.lower().strip().encode('utf-8')).hexdigest()[:8], 16)
    random.seed(seed + name_hash + situation_idx * 1000)
    
    # Renderiza em alta resolução 1000x1000
    w, h = 1000, 1000
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    nl = figure_name.lower().strip()
    
    is_michael = any(k in nl for k in ["miguel", "arcanjo são miguel", "sao miguel", "são miguel"])
    is_gabriel = any(k in nl for k in ["gabriel"])
    is_raphael = any(k in nl for k in ["rafael"])
    is_angel = is_michael or is_gabriel or is_raphael or any(k in nl for k in ["arcanjo", "anjo", "querubim", "serafim"])
    
    is_george = any(k in nl for k in ["jorge"])
    is_expedite = any(k in nl for k in ["expedito"])
    is_sebastian = any(k in nl for k in ["sebastião", "sebastiao"])
    is_warrior = is_michael or is_george or is_expedite or is_sebastian or any(k in nl for k in ["soldado", "guerreiro"])
    
    is_francis = any(k in nl for k in ["francisc", "chico", "assis"])
    is_anthony = any(k in nl for k in ["antonio", "antônio"])
    is_benedict = any(k in nl for k in ["bento", "benedito"])
    is_padre_pio = any(k in nl for k in ["pio", "padre pio"])
    is_monk = is_francis or is_anthony or is_benedict or is_padre_pio or any(k in nl for k in ["frade", "monge", "ermitão", "clara"])
    
    is_mary = any(k in nl for k in ["maria", "senhora", "fátima", "fatima", "aparecida", "lourdes", "carmo", "virgem", "guadalupe", "conceição", "madona", "desatadora"])
    is_teresa = any(k in nl for k in ["teresa", "calcutá", "calcuta", "madre"]) and not is_mary
    is_lucy = any(k in nl for k in ["luzia", "lucia"])
    is_female = is_mary or is_teresa or is_lucy or any(k in nl for k in ["santa", "rita", "cecília", "cecilia", "bárbara", "barbara", "irmã", "dulce"])
    
    is_joseph = any(k in nl for k in ["josé", "jose", "carpinteiro"]) and not is_francis
    is_jesus = any(k in nl for k in ["jesus", "cristo", "bom pastor", "messias", "salvador", "coração de jesus", "sagrado coração"]) and not is_joseph
    is_peter = any(k in nl for k in ["pedro", "apóstolo", "apostolo", "pescador"]) and not is_jesus
    is_moses = any(k in nl for k in ["moisés", "moises", "mar vermelho", "sinai", "mandamentos", "profeta", "patriarca", "abraão", "elias", "noé"]) and not is_jesus
    
    has_beard = (is_moses or is_peter or is_joseph or is_jesus or is_benedict or is_padre_pio) and not is_female and not is_angel
    has_wings = is_angel
    has_armor = is_warrior or is_michael

    sit = situation_idx % 5
    cx, cy = 500, 320
    shoulder_y = cy + 76
    bottom_y = 855

    # ================= 1. ELEMENTOS DE FUNDO & ASAS =================
    if has_wings:
        draw_detailed_wings(draw, cx, cy, wing_span=280)

    # Auréola Sacra
    draw_ornate_halo(draw, cx, cy, radius=130, is_mary=is_mary, is_jesus=is_jesus)

    # Nuvens sagradas fofas e estilizadas
    for clx, cly in [(160, 150), (840, 150), (140, 480), (860, 480)]:
        draw.arc([clx - 45, cly - 26, clx + 45, cly + 26], 180, 360, fill="black", width=4)
        draw.arc([clx - 80, cly - 10, clx - 10, cly + 35], 180, 360, fill="black", width=4)
        draw.arc([clx + 10, cly - 10, clx + 80, cly + 35], 180, 360, fill="black", width=4)
        draw.line([(clx - 75, cly + 22), (clx + 75, cly + 22)], fill="black", width=4)

    # ================= 2. CABEÇA, ROSTO E CABELOS RICOS =================
    draw_charming_face(draw, cx, cy, is_female=is_female)

    if is_mary:
        # Manto e Véu Sagrado gracioso
        draw_smooth_curve(draw, (cx, cy - 105), (cx - 120, cy - 65), (cx - 130, cy + 140), (cx - 105, cy + 340), width=6)
        draw_smooth_curve(draw, (cx, cy - 105), (cx + 120, cy - 65), (cx + 130, cy + 140), (cx + 105, cy + 340), width=6)
        # Borda bordada do véu com pequenas estrelas
        draw_smooth_curve(draw, (cx - 60, cy - 60), (cx - 85, cy + 30), (cx - 75, cy + 175), (cx - 65, cy + 320), width=3)
        draw_smooth_curve(draw, (cx + 60, cy - 60), (cx + 85, cy + 30), (cx + 75, cy + 175), (cx + 65, cy + 320), width=3)
        for my in range(cy - 20, cy + 280, 50):
            draw_star(draw, cx - 80, my, 5, 2, points=5, fill="black")
            draw_star(draw, cx + 80, my, 5, 2, points=5, fill="black")
    elif is_teresa:
        # Véu de Santa Teresa com as 3 faixas azuis tradicionais
        draw_smooth_curve(draw, (cx, cy - 100), (cx - 105, cy - 55), (cx - 115, cy + 130), (cx - 90, cy + 310), width=6)
        draw_smooth_curve(draw, (cx, cy - 100), (cx + 105, cy - 55), (cx + 115, cy + 130), (cx + 90, cy + 310), width=6)
        for offset in [10, 20, 30]:
            draw_smooth_curve(draw, (cx - 85 + offset, cy - 45 + offset//2), (cx - 100 + offset, cy + 40), (cx - 85 + offset, cy + 180), (cx - 70 + offset, cy + 300), width=3)
    elif is_monk:
        # Hábito com capuz e tonsura franciscana
        draw_smooth_curve(draw, (cx - 66, cy - 18), (cx - 70, cy - 85), (cx + 70, cy - 85), (cx + 66, cy - 18), width=7)
        draw_smooth_curve(draw, (cx - 38, cy - 75), (cx, cy - 88), (cx + 38, cy - 75), (cx + 28, cy - 65), width=5)
        for bx in range(cx - 30, cx + 36, 11):
            draw.arc([bx, cy + 46, bx + 12, cy + 62], 0, 180, fill="black", width=3)
    elif has_beard:
        # Barba bíblica ondulada e volumosa
        draw_smooth_curve(draw, (cx - 52, cy + 18), (cx - 62, cy + 135), (cx, cy + 175), (cx, cy + 180), width=5)
        draw_smooth_curve(draw, (cx + 52, cy + 18), (cx + 62, cy + 135), (cx, cy + 175), (cx + 62, cy + 180), width=5)
        for by in range(cy + 55, cy + 145, 22):
            draw.arc([cx - 20, by, cx + 20, by + 22], 0, 180, fill="black", width=3)
        # Cabelo ondulado longo
        draw_smooth_curve(draw, (cx - 68, cy - 35), (cx - 85, cy - 88), (cx + 85, cy - 88), (cx + 68, cy - 35), width=6)
        draw_smooth_curve(draw, (cx - 68, cy - 35), (cx - 85, cy + 40), (cx - 75, cy + 120), (cx - 62, cy + 155), width=5)
        draw_smooth_curve(draw, (cx + 68, cy - 35), (cx + 85, cy + 40), (cx + 75, cy + 120), (cx + 62, cy + 155), width=5)
    else:
        # Cabelo com mechas onduladas
        draw_smooth_curve(draw, (cx - 68, cy - 35), (cx - 82, cy - 85), (cx + 82, cy - 85), (cx + 68, cy - 35), width=6)
        draw_smooth_curve(draw, (cx - 68, cy - 35), (cx - 85, cy + 35), (cx - 72, cy + 110), (cx - 62, cy + 150), width=5)
        draw_smooth_curve(draw, (cx + 68, cy - 35), (cx + 85, cy + 35), (cx + 72, cy + 110), (cx + 62, cy + 150), width=5)

    # ================= 3. VESTIMENTAS E DOBRAS REALISTAS =================
    # Gola da túnica com costura dupla
    draw.arc([cx - 38, cy + 48, cx + 38, cy + 90], 0, 180, fill="black", width=5)
    draw.arc([cx - 32, cy + 54, cx + 32, cy + 84], 0, 180, fill="black", width=3)

    # Silhueta exterior do manto com caimento fluído
    draw_smooth_curve(draw, (cx - 75, shoulder_y), (cx - 160, shoulder_y + 115), (cx - 225, bottom_y - 115), (cx - 215, bottom_y), width=6)
    draw_smooth_curve(draw, (cx + 75, shoulder_y), (cx + 160, shoulder_y + 115), (cx + 225, bottom_y - 115), (cx + 215, bottom_y), width=6)

    # Barra ondulada detalhada
    for x in range(cx - 215, cx + 215, 52):
        draw.arc([x, bottom_y - 18, x + 58, bottom_y + 18], 0, 180, fill="black", width=5)

    # Dobras internas de tecido
    draw_smooth_curve(draw, (cx - 35, cy + 185), (cx - 75, cy + 340), (cx - 85, bottom_y - 85), (cx - 75, bottom_y), width=4)
    draw_smooth_curve(draw, (cx + 35, cy + 185), (cx + 75, cy + 340), (cx + 85, bottom_y - 85), (cx + 75, bottom_y), width=4)
    draw.line([(cx, cy + 225), (cx, bottom_y)], fill="black", width=5)

    # Detalhes específicos de cada persona
    if is_monk:
        # Cordão franciscano com 3 nós sagrados
        draw.arc([cx - 105, cy + 240, cx + 105, cy + 285], 0, 180, fill="black", width=6)
        draw.line([(cx + 38, cy + 265), (cx + 38, cy + 450)], fill="black", width=5)
        for ky in [cy + 305, cy + 350, cy + 395]:
            draw.ellipse([cx + 30, ky, cx + 46, ky + 20], fill="black")
            draw.arc([cx + 26, ky - 4, cx + 50, ky + 24], 0, 180, fill="black", width=3)
    elif has_armor:
        # Peitoral de armadura romana com arabescos e cruz
        draw.polygon([(cx - 58, shoulder_y + 15), (cx + 58, shoulder_y + 15), (cx + 45, cy + 255), (cx, cy + 285), (cx - 45, cy + 255)], outline="black", width=5)
        draw.line([(cx, shoulder_y + 35), (cx, cy + 225)], fill="black", width=6)
        draw.line([(cx - 34, shoulder_y + 95), (cx + 34, shoulder_y + 95)], fill="black", width=6)
        # Cruz no peito
        draw.line([(cx, shoulder_y + 65), (cx, shoulder_y + 145)], fill="black", width=5)
        draw.line([(cx - 20, shoulder_y + 90), (cx + 20, shoulder_y + 90)], fill="black", width=5)
        # Pteruges (saiote de placas de couro da armadura romana)
        for ptx in range(cx - 40, cx + 45, 18):
            draw.polygon([(ptx, cy + 255), (ptx + 14, cy + 255), (ptx + 14, cy + 290), (ptx, cy + 290)], outline="black", width=3)
    elif is_teresa:
        cx_s, cy_s = cx - 58, shoulder_y + 25
        draw.line([(cx_s, cy_s - 14), (cx_s, cy_s + 24)], fill="black", width=5)
        draw.line([(cx_s - 10, cy_s - 2), (cx_s + 10, cy_s - 2)], fill="black", width=5)
    elif is_peter:
        ck_x, ck_y = cx - 68, cy + 290
        draw.circle((ck_x, ck_y), 12, outline="black", width=4)
        draw.line([(ck_x, ck_y + 12), (ck_x, ck_y + 45)], fill="black", width=5)
        draw.line([(ck_x, ck_y + 32), (ck_x + 12, ck_y + 32)], fill="black", width=4)
    elif is_jesus:
        heart_x, heart_y = cx, cy + 130
        draw.arc([heart_x - 22, heart_y - 18, heart_x, heart_y + 8], 180, 360, fill="black", width=4)
        draw.arc([heart_x, heart_y - 18, heart_x + 22, heart_y + 8], 180, 360, fill="black", width=4)
        draw.line([(heart_x - 22, heart_y - 5), (heart_x, heart_y + 24), (heart_x + 22, heart_y - 5)], fill="black", width=4)
        draw.line([(heart_x, heart_y - 20), (heart_x, heart_y - 35)], fill="black", width=4)
        # Chamas e coroa de espinhos
        draw.arc([heart_x - 18, heart_y + 2, heart_x + 18, heart_y + 18], 0, 180, fill="black", width=3)

    # ================= 4. AS 5 VARIAÇÕES SITUACIONAIS =================
    if sit == 0:
        # --- CENA 1: EM ORAÇÃO CONTEMPLATIVA ---
        hand_y = cy + 185
        draw_smooth_curve(draw, (cx - 70, shoulder_y), (cx - 115, hand_y - 20), (cx - 65, hand_y + 10), (cx - 24, hand_y), width=5)
        draw_smooth_curve(draw, (cx + 70, shoulder_y), (cx + 115, hand_y - 20), (cx + 65, hand_y + 10), (cx + 24, hand_y), width=5)
        draw.ellipse([cx - 25, hand_y - 24, cx + 25, hand_y + 34], outline="black", width=5)
        draw.line([(cx, hand_y - 22), (cx, hand_y + 30)], fill="black", width=4)
        
        if is_michael:
            # Espada flamejante fincada
            draw.line([(cx, hand_y + 40), (cx, bottom_y - 10)], fill="black", width=6)
            draw.line([(cx - 24, hand_y + 60), (cx + 24, hand_y + 60)], fill="black", width=5)
            draw.circle((cx, hand_y + 38), 6, fill="black")
        elif is_expedite:
            draw.line([(cx + 55, cy + 120), (cx + 55, cy + 220)], fill="black", width=6)
            draw.line([(cx + 38, cy + 150), (cx + 72, cy + 150)], fill="black", width=5)
        elif is_george:
            draw.line([(cx - 75, cy + 140), (cx - 75, bottom_y)], fill="black", width=6)
        elif is_moses:
            for deg in [240, 260, 280, 300]:
                rad = math.radians(deg)
                draw.line([(cx + math.cos(rad)*150, cy + math.sin(rad)*150), (cx + math.cos(rad)*220, cy + math.sin(rad)*220)], fill="black", width=4)
        elif is_peter:
            draw.polygon([(cx - 145, bottom_y - 20), (cx + 145, bottom_y - 20), (cx + 105, bottom_y + 25), (cx - 105, bottom_y + 25)], outline="black", width=5)
        else:
            # Santo Terço com crucifixo
            for b in range(9):
                ang = math.pi * 0.16 + (b / 8) * math.pi * 0.68
                bx = cx + math.cos(ang) * 38
                by = hand_y + 35 + math.sin(ang) * 46
                draw.circle((int(bx), int(by)), 5, fill="black")
            cross_y = hand_y + 92
            draw.line([(cx, cross_y), (cx, cross_y + 36)], fill="black", width=5)
            draw.line([(cx - 13, cross_y + 11), (cx + 13, cross_y + 11)], fill="black", width=5)

    elif sit == 1:
        # --- CENA 2: CAMINHANDO / JORNADA DA FÉ ---
        staff_x = cx + 145
        draw.line([(staff_x, 150), (staff_x, bottom_y)], fill="black", width=8)
        
        if is_joseph:
            # Cajado que floresce lírios
            draw.arc([staff_x - 24, 110, staff_x + 24, 168], 180, 360, fill="black", width=8)
            for ly in [105, 125, 145]:
                draw.ellipse([staff_x - 14, ly - 8, staff_x + 14, ly + 8], outline="black", width=4)
        elif has_armor:
            # Lança do arcanjo/guerreiro com flâmula
            draw.polygon([(staff_x - 16, 110), (staff_x, 70), (staff_x + 16, 110)], fill="black")
            draw.polygon([(staff_x + 6, 95), (staff_x + 75, 125), (staff_x + 6, 155)], outline="black", width=4)
            draw.line([(staff_x + 15, 125), (staff_x + 65, 125)], fill="black", width=3)
        elif is_peter:
            draw.arc([staff_x - 24, 105, staff_x + 24, 165], 180, 360, fill="black", width=8)
            for wx in range(120, 880, 95):
                draw.arc([wx, bottom_y - 40, wx + 75, bottom_y + 10], 0, 180, fill="black", width=4)
        elif is_moses:
            draw.arc([staff_x - 24, 105, staff_x + 24, 165], 180, 360, fill="black", width=8)
            draw_smooth_curve(draw, (120, 180), (160, 400), (140, 600), (120, bottom_y), width=6)
            draw_smooth_curve(draw, (880, 180), (840, 400), (860, 600), (880, bottom_y), width=6)
        else:
            draw.arc([staff_x - 24, 105, staff_x + 24, 165], 180, 360, fill="black", width=8)

        draw_smooth_curve(draw, (cx + 70, shoulder_y), (cx + 125, cy + 115), (staff_x - 24, cy + 155), (staff_x, cy + 165), width=5)
        draw.ellipse([staff_x - 14, cy + 145, staff_x + 14, cy + 185], outline="black", width=5)
        draw_smooth_curve(draw, (cx - 70, shoulder_y), (cx - 130, cy + 155), (cx - 110, cy + 225), (cx - 78, cy + 215), width=5)
        draw.ellipse([cx - 135, cy + 195, cx - 100, cy + 235], outline="black", width=5)

    elif sit == 2:
        # --- CENA 3: SORRINDO / ABENÇOANDO COM A PAZ ---
        bx, by = cx + 120, cy + 110
        draw_smooth_curve(draw, (cx + 70, shoulder_y), (cx + 135, cy + 85), (bx, by + 35), (bx, by), width=5)
        draw.ellipse([bx - 16, by - 16, bx + 16, by + 25], outline="black", width=5)
        draw.line([(bx - 6, by - 16), (bx - 6, by - 46)], fill="black", width=6)
        draw.line([(bx + 5, by - 16), (bx + 5, by - 40)], fill="black", width=6)
        
        draw_smooth_curve(draw, (cx - 70, shoulder_y), (cx - 105, cy + 125), (cx - 65, cy + 185), (cx - 10, cy + 180), width=5)
        draw.ellipse([cx - 34, cy + 165, cx + 8, cy + 205], outline="black", width=5)
        
        if is_mary:
            for lx in [cx - 165, cx - 115]:
                draw.line([(lx, cy - 20), (lx, cy - 70)], fill="black", width=4)
                draw_rose(draw, lx, cy - 75, radius=12)
        elif is_michael:
            # Escudo de defesa celestial abaixado
            sh_x, sh_y = cx - 135, cy + 190
            draw.polygon([(sh_x - 32, sh_y - 45), (sh_x + 32, sh_y - 45), (sh_x + 28, sh_y + 35), (sh_x, sh_y + 65), (sh_x - 28, sh_y + 35)], outline="black", width=5)
            draw.line([(sh_x, sh_y - 35), (sh_x, sh_y + 45)], fill="black", width=4)
            draw.line([(sh_x - 20, sh_y - 10), (sh_x + 20, sh_y - 10)], fill="black", width=4)
        elif is_expedite:
            draw.line([(cx - 135, cy + 150), (cx - 165, cy + 90)], fill="black", width=5)
            for py in range(cy + 100, cy + 150, 10):
                draw.line([(cx - 150, py), (cx - 170, py - 10)], fill="black", width=3)
        elif is_george:
            draw.line([(cx - 135, cy + 80), (cx - 135, bottom_y)], fill="black", width=6)
            draw.polygon([(cx - 135, cy + 90), (cx - 70, cy + 120), (cx - 135, cy + 150)], outline="black", width=4)
        else:
            # Pomba da Paz estilizada
            dove_x, dove_y = cx - 175, cy - 65
            draw.ellipse([dove_x, dove_y, dove_x + 50, dove_y + 32], outline="black", width=4)
            draw.arc([dove_x + 12, dove_y - 32, dove_x + 50, dove_y + 10], 180, 360, fill="black", width=4)
            draw.polygon([(dove_x + 46, dove_y + 12), (dove_x + 62, dove_y + 16), (dove_x + 46, dove_y + 20)], fill="black")

    elif sit == 3:
        # --- CENA 4: AJUDANDO / DEFENDENDO / MILAGRE ---
        if is_joseph or is_mary:
            draw_smooth_curve(draw, (cx - 70, shoulder_y), (cx - 125, cy + 155), (cx - 75, cy + 235), (cx - 16, cy + 225), width=5)
            draw_smooth_curve(draw, (cx + 70, shoulder_y), (cx + 125, cy + 155), (cx + 75, cy + 235), (cx + 16, cy + 225), width=5)
            bj_x, bj_y = cx, cy + 205
            draw.ellipse([bj_x - 30, bj_y - 34, bj_x + 30, bj_y + 28], outline="black", width=5)
            draw_ornate_halo(draw, bj_x, bj_y - 8, radius=46, is_jesus=True)
            draw_charming_face(draw, bj_x, bj_y, is_child=True)
            draw.ellipse([bj_x - 38, bj_y + 22, bj_x + 38, bj_y + 80], outline="black", width=5)
        elif is_michael:
            # Escudo erguido e espada da vitória na mão
            sh_x, sh_y = cx - 105, cy + 205
            draw.polygon([(sh_x - 38, sh_y - 48), (sh_x + 38, sh_y - 48), (sh_x + 32, sh_y + 32), (sh_x, sh_y + 65), (sh_x - 32, sh_y + 32)], outline="black", width=6)
            draw.line([(sh_x, sh_y - 36), (sh_x, sh_y + 48)], fill="black", width=5)
            draw.line([(sh_x - 24, sh_y - 10), (sh_x + 24, sh_y - 10)], fill="black", width=5)
            sw_x, sw_y = cx + 115, cy + 175
            draw.line([(sw_x, sw_y - 68), (sw_x, sw_y + 78)], fill="black", width=6)
            draw.line([(sw_x - 18, sw_y - 30), (sw_x + 18, sw_y - 30)], fill="black", width=5)
            draw.circle((sw_x, sw_y - 72), 8, fill="black")
            # Dragão/serpente vencida
            draw.arc([cx - 145, bottom_y - 42, cx + 145, bottom_y + 22], 0, 180, fill="black", width=5)
        elif is_george:
            draw.line([(cx - 115, cy + 120), (cx + 135, bottom_y - 20)], fill="black", width=6)
            draw.polygon([(cx + 75, bottom_y - 55), (cx + 150, bottom_y - 20), (cx + 75, bottom_y + 20)], outline="black", width=4)
        elif is_expedite:
            draw.ellipse([cx - 95, bottom_y - 38, cx - 20, bottom_y], outline="black", width=4)
            draw.line([(cx + 55, cy + 150), (cx + 55, cy + 250)], fill="black", width=5)
            draw.line([(cx + 38, cy + 180), (cx + 72, cy + 180)], fill="black", width=5)
        elif is_peter:
            net_x, net_y = cx, cy + 230
            draw.ellipse([net_x - 60, net_y - 26, net_x + 60, net_y + 30], outline="black", width=4)
            for fx in [-32, -8, 16, 36]:
                draw.ellipse([net_x + fx - 9, net_y - 7, net_x + fx + 9, net_y + 5], outline="black", width=3)
                draw.polygon([(net_x + fx + 7, net_y - 2), (net_x + fx + 14, net_y - 6), (net_x + fx + 14, net_y + 3)], fill="black")
        elif is_moses:
            rock_x, rock_y = cx, cy + 240
            draw.polygon([(rock_x - 70, rock_y + 28), (rock_x - 42, rock_y - 24), (rock_x + 42, rock_y - 24), (rock_x + 70, rock_y + 28)], outline="black", width=5)
            draw_smooth_curve(draw, (rock_x, rock_y - 24), (rock_x - 32, rock_y - 52), (rock_x - 60, rock_y), (rock_x - 80, rock_y + 24), width=5)
            draw_smooth_curve(draw, (rock_x, rock_y - 24), (rock_x + 32, rock_y - 52), (rock_x + 60, rock_y), (rock_x + 80, rock_y + 24), width=5)
        else:
            # Distribuição de pães e acolhimento
            draw_smooth_curve(draw, (cx - 70, shoulder_y), (cx - 150, cy + 125), (cx - 170, cy + 195), (cx - 115, cy + 230), width=5)
            draw_smooth_curve(draw, (cx + 70, shoulder_y), (cx + 150, cy + 125), (cx + 170, cy + 195), (cx + 115, cy + 230), width=5)
            draw.ellipse([cx - 190, cy + 180, cx - 145, cy + 225], outline="black", width=5)
            draw.ellipse([cx + 145, cy + 180, cx + 190, cy + 225], outline="black", width=5)
            basket_x, basket_y = cx, cy + 225
            draw.arc([basket_x - 46, basket_y - 24, basket_x + 46, basket_y + 34], 0, 180, fill="black", width=5)
            draw.ellipse([basket_x - 46, basket_y - 24, basket_x + 46, basket_y + 8], outline="black", width=4)
            for ox in [-20, 0, 20]:
                draw.ellipse([basket_x + ox - 13, basket_y - 28, basket_x + ox + 13, basket_y - 5], outline="black", width=4)

    elif sit == 4:
        # --- CENA 5: ENSINANDO / SAGRADAS ESCRITURAS ---
        if is_moses:
            tw, th = 65, 105
            t1_x, t1_y = cx - 140, cy + 125
            draw.polygon([(t1_x, t1_y), (t1_x + tw, t1_y), (t1_x + tw, t1_y + th), (t1_x, t1_y + th)], outline="black", width=5)
            draw.arc([t1_x, t1_y - 20, t1_x + tw, t1_y + 20], 180, 360, fill="black", width=5)
            for r in range(5):
                draw.line([(t1_x + 10, t1_y + 16 + r * 17), (t1_x + tw - 10, t1_y + 16 + r * 17)], fill="black", width=4)
            t2_x = t1_x + tw + 10
            draw.polygon([(t2_x, t1_y), (t2_x + tw, t1_y), (t2_x + tw, t1_y + th), (t2_x, t1_y + th)], outline="black", width=5)
            draw.arc([t2_x, t1_y - 20, t2_x + tw, t1_y + 20], 180, 360, fill="black", width=5)
            for r in range(5):
                draw.line([(t2_x + 10, t1_y + 16 + r * 17), (t2_x + tw - 10, t1_y + 16 + r * 17)], fill="black", width=4)
        elif is_peter:
            key_x, key_y = cx + 120, cy + 135
            draw.circle((key_x, key_y), 19, outline="black", width=6)
            draw.circle((key_x, key_y), 8, outline="black", width=4)
            draw.line([(key_x, key_y + 19), (key_x, key_y + 90)], fill="black", width=7)
            draw.line([(key_x, key_y + 60), (key_x + 16, key_y + 60)], fill="black", width=6)
            draw.line([(key_x, key_y + 78), (key_x + 16, key_y + 78)], fill="black", width=6)
            bx, by = cx - 95, cy + 205
            bw, bh = 66, 45
            draw.polygon([(bx - bw, by - bh//2), (bx + bw, by - bh//2), (bx + bw, by + bh//2), (bx - bw, by + bh//2)], outline="black", width=5)
            draw.line([(bx, by - bh//2), (bx, by + bh//2)], fill="black", width=4)
        elif is_michael:
            # Balança da justiça divina e pergaminho da vitória
            sc_x, sc_y = cx - 95, cy + 180
            draw.line([(sc_x - 42, sc_y), (sc_x + 42, sc_y)], fill="black", width=5)
            draw.circle((sc_x, sc_y), 6, fill="black")
            draw.line([(sc_x - 32, sc_y), (sc_x - 32, sc_y + 38)], fill="black", width=3)
            draw.line([(sc_x + 32, sc_y), (sc_x + 32, sc_y + 38)], fill="black", width=3)
            draw.arc([sc_x - 44, sc_y + 28, sc_x - 20, sc_y + 52], 0, 180, fill="black", width=4)
            draw.arc([sc_x + 20, sc_y + 28, sc_x + 44, sc_y + 52], 0, 180, fill="black", width=4)
            bx, by = cx + 105, cy + 210
            bw, bh = 60, 42
            draw.polygon([(bx - bw, by - bh//2), (bx + bw, by - bh//2), (bx + bw, by + bh//2), (bx - bw, by + bh//2)], outline="black", width=5)
        else:
            # Livro Sagrado central com encadernação e fitas
            bx, by = cx, cy + 215
            bw, bh = 88, 60
            draw_smooth_curve(draw, (cx - 70, shoulder_y), (cx - 105, cy + 155), (bx - bw + 16, by), (bx - bw + 16, by + bh//2), width=5)
            draw_smooth_curve(draw, (cx + 70, shoulder_y), (cx + 110, cy + 155), (bx + bw - 16, by), (bx + bw - 16, by + bh//2), width=5)
            draw.polygon([
                (bx - bw, by - bh//2), (bx, by - bh//2 + 12), (bx + bw, by - bh//2),
                (bx + bw, by + bh//2), (bx, by + bh//2 + 12), (bx - bw, by + bh//2)
            ], outline="black", width=5)
            draw.line([(bx, by - bh//2 + 12), (bx, by + bh//2 + 12)], fill="black", width=5)
            for ly in range(by - 10, by + 24, 8):
                draw.line([(bx - bw + 14, ly), (bx - 14, ly + 2)], fill="black", width=3)
                draw.line([(bx + 14, ly + 2), (bx + bw - 14, ly)], fill="black", width=3)
            draw.ellipse([bx - bw + 10, by + bh//2 - 8, bx - bw + 40, by + bh//2 + 20], outline="black", width=4)
            draw.ellipse([bx + bw - 40, by + bh//2 - 8, bx + bw - 10, by + bh//2 + 20], outline="black", width=4)

    # ================= 5. COMPANHEIROS E ATRIBUTOS EXCLUSIVOS =================
    if is_francis:
        # Pássaro no ombro com asinhas
        bird_x, bird_y = cx - 120, cy + 85
        draw.ellipse([bird_x, bird_y, bird_x + 40, bird_y + 25], outline="black", width=4)
        draw.ellipse([bird_x + 25, bird_y - 12, bird_x + 52, bird_y + 10], outline="black", width=4)
        draw.polygon([(bird_x + 50, bird_y - 3), (bird_x + 64, bird_y), (bird_x + 50, bird_y + 4)], fill="black")
        # Lobo amigável com rabo
        wolf_x, wolf_y = cx - 185, bottom_y - 75
        draw.ellipse([wolf_x, wolf_y, wolf_x + 78, wolf_y + 56], outline="black", width=5)
        draw.ellipse([wolf_x + 50, wolf_y - 24, wolf_x + 92, wolf_y + 18], outline="black", width=5)
        draw.polygon([(wolf_x + 54, wolf_y - 20), (wolf_x + 64, wolf_y - 44), (wolf_x + 76, wolf_y - 20)], outline="black", width=4)
        draw.circle((wolf_x + 90, wolf_y - 4), 4, fill="black")
    elif is_anthony:
        # Lírio florescente com folhas
        lily_x = cx - 125
        draw.line([(lily_x, cy + 30), (lily_x, bottom_y)], fill="black", width=5)
        draw.arc([lily_x - 20, cy + 10, lily_x + 20, cy + 42], 0, 180, fill="black", width=4)
        draw.arc([lily_x - 12, cy - 10, lily_x + 12, cy + 22], 0, 180, fill="black", width=4)
    elif is_jesus:
        # Cordeirinho fofo nos campos
        lamb_x, lamb_y = cx + 120, bottom_y - 75
        draw.ellipse([lamb_x, lamb_y, lamb_x + 70, lamb_y + 50], outline="black", width=5)
        # Caracóis de lã
        for sx, sy in [(lamb_x + 15, lamb_y + 15), (lamb_x + 35, lamb_y + 25), (lamb_x + 50, lamb_y + 15)]:
            draw.arc([sx - 8, sy - 8, sx + 8, sy + 8], 0, 270, fill="black", width=3)
        draw.ellipse([lamb_x - 15, lamb_y - 15, lamb_x + 18, lamb_y + 15], outline="black", width=5)
        draw.ellipse([lamb_x - 24, lamb_y - 12, lamb_x - 12, lamb_y - 2], outline="black", width=4)
        draw.circle((lamb_x - 5, lamb_y - 5), 4, fill="black")

    # ================= 6. CHÃO GRAMADO E FLORES DE ENQUADRAMENTO =================
    draw.line([(70, bottom_y), (w - 70, bottom_y)], fill="black", width=6)
    for fx in range(130, w - 130, 90):
        draw_rose(draw, fx, bottom_y + 30, radius=10)
        draw.line([(fx, bottom_y + 38), (fx, bottom_y + 65)], fill="black", width=4)
        # Folhinhas do solo
        draw.arc([fx - 15, bottom_y + 42, fx, bottom_y + 58], 180, 360, fill="black", width=3)
        draw.arc([fx, bottom_y + 42, fx + 15, bottom_y + 58], 180, 360, fill="black", width=3)

    return img

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def render_detailed_coloring_page(figure_name: str, situation_idx: int, seed: int) -> Image.Image:
    """
    Renderiza arte de colorir 1024x1024 profissional, rica em traços pretos expressivos (storybook / 2D lineart),
    fundo 100% transparente (canal alfa limpo) e margem de segurança garantida (zero cortes).
    """
    meta = analyze_figure_identity(figure_name)
    sit = situation_idx % 5
    
    if meta["is_michael"] or meta["is_angel"] or meta["is_warrior"]:
        cat = "arcanjo_guerreiro"
    elif meta["is_mary"]:
        cat = "mariano"
    elif meta["is_teresa"] or meta["is_lucy"] or meta["is_female"]:
        cat = "santa"
    elif meta["is_moses"]:
        cat = "moises"
    elif meta["is_peter"] or meta["is_joseph"] or meta["is_jesus"]:
        cat = "pedro"
    elif meta["is_francis"] or meta["is_monk"]:
        cat = "franciscano"
    else:
        cat = "padrao"
        
    asset_path = os.path.join(ASSETS_DIR, cat, f"{sit}.png")
    if os.path.exists(asset_path):
        base_img = Image.open(asset_path).convert("RGBA")
        bbox = base_img.getbbox()
        if bbox:
            cropped = base_img.crop(bbox)
            
            # Variação determinística única por figura e seed para evitar colisões
            name_hash = int(hashlib.md5(f"{figure_name}_{seed}_{sit}".encode("utf-8")).hexdigest()[:6], 16)
            
            # Escala segura entre 0.94 e 0.98
            scale_var = 0.94 + (name_hash % 40) * 0.001
            safe_target = 850.0 * scale_var
            scale = min(safe_target / cropped.width, safe_target / cropped.height, 1.0)
            
            new_w = max(1, int(cropped.width * scale))
            new_h = max(1, int(cropped.height * scale))
            resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            # Offset determinístico sutil (+/- 6px)
            dx = (name_hash % 13) - 6
            dy = ((name_hash // 13) % 13) - 6
            
            final_canvas = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
            paste_x = (1024 - new_w) // 2 + dx
            paste_y = (1024 - new_h) // 2 + dy
            
            # Respiro estritamente mantido entre 70px e 954px (segurança total contra cortes)
            paste_x = max(70, min(1024 - new_w - 70, paste_x))
            paste_y = max(70, min(1024 - new_h - 70, paste_y))
            
            final_canvas.paste(resized, (paste_x, paste_y), mask=resized)
            return final_canvas
            
    # Fallback procedural
    raw_img = generate_professional_coloring_art(figure_name, situation_idx, seed)
    bbox = raw_img.getbbox()
    if not bbox:
        return raw_img
    
    min_x, min_y, max_x, max_y = bbox
    content_w = max_x - min_x
    content_h = max_y - min_y
    
    target_canvas_size = 1024
    safe_margin = 75
    max_allowed_w = target_canvas_size - (safe_margin * 2)
    max_allowed_h = target_canvas_size - (safe_margin * 2)
    
    scale = min(max_allowed_w / content_w, max_allowed_h / content_h, 1.0)
    
    cropped_content = raw_img.crop(bbox)
    new_w = max(1, int(content_w * scale))
    new_h = max(1, int(content_h * scale))
    
    resized_content = cropped_content.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    final_canvas = Image.new("RGBA", (target_canvas_size, target_canvas_size), (0, 0, 0, 0))
    paste_x = (target_canvas_size - new_w) // 2
    paste_y = (target_canvas_size - new_h) // 2
    final_canvas.paste(resized_content, (paste_x, paste_y), mask=resized_content)
    
    return final_canvas
