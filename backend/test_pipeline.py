import io
import base64
import unittest
from fastapi.testclient import TestClient
from PIL import Image

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import app, generate_dynamic_profile
from vector_engine import render_detailed_coloring_page

class TestPipelineAndProfiles(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_saint_bindings_dynamic(self):
        test_queries = [
            ("São Miguel Arcanjo", "sao_miguel_arcanjo"),
            ("São Francisco de Assis", "sao_francisco_de_assis"),
            ("Nossa Senhora de Fátima", "nossa_senhora_de_fatima"),
            ("Santo Expedito", "santo_expedito"),
            ("São Jorge", "sao_jorge"),
            ("Santa Teresa de Calcutá", "santa_teresa_de_calcuta"),
            ("São José e o Menino Jesus", "sao_jose_e_o_menino_jesus"),
            ("Jesus Bom Pastor", "jesus_bom_pastor"),
            ("Santa Luzia", "santa_luzia")
        ]
        for query, expected_slug in test_queries:
            profile = generate_dynamic_profile(query)
            self.assertEqual(profile["id"], expected_slug, f"Falha no slug de {query}")
            self.assertIn(query, profile["title"], f"O título deve conter o nome exato {query}")

    def test_no_duplicates_and_no_cropping(self):
        saints = [
            "São Miguel Arcanjo",
            "São Francisco de Assis",
            "Nossa Senhora de Fátima",
            "Moisés abrindo o Mar Vermelho",
            "São Pedro Apóstolo",
            "Santo Expedito",
            "São Jorge",
            "Santa Teresa de Calcutá",
            "São José e o Menino Jesus",
            "Jesus Bom Pastor",
        ]
        
        seen_images = set()
        for saint in saints:
            res = self.client.post("/api/generate", json={"name": saint})
            self.assertEqual(res.status_code, 200, f"Erro na requisição para {saint}")
            data = res.json()
            images = data["images"]
            self.assertEqual(len(images), 5)
            self.assertEqual(data["figure"], saint)
            
            for img_info in images:
                self.assertEqual(img_info["figure_name"], saint)
                raw_b64 = img_info["image_base64"].split(",")[1]
                raw_bytes = base64.b64decode(raw_b64)
                
                # Garante que não há repetição
                self.assertNotIn(raw_bytes, seen_images, f"Imagem duplicada encontrada em {saint} #{img_info['id']}")
                seen_images.add(raw_bytes)
                
                # Valida geometria e ausência de cortes
                im = Image.open(io.BytesIO(raw_bytes))
                self.assertEqual(im.mode, "RGBA")
                self.assertEqual(im.size, (1024, 1024))
                
                bbox = im.getbbox()
                self.assertIsNotNone(bbox)
                # Respiro mínimo garantido de 60px em todas as 4 bordas
                self.assertGreaterEqual(bbox[0], 60, f"Corte na margem esquerda em {saint}: {bbox}")
                self.assertGreaterEqual(bbox[1], 60, f"Corte no topo em {saint}: {bbox}")
                self.assertLessEqual(bbox[2], 964, f"Corte na margem direita em {saint}: {bbox}")
                self.assertLessEqual(bbox[3], 964, f"Corte na base em {saint}: {bbox}")

if __name__ == "__main__":
    unittest.main()
