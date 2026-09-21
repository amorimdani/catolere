import JSZip from 'jszip';
import { saveAs } from 'file-saver';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/health`, { method: 'GET' });
    if (!res.ok) throw new Error('Falha no status do servidor');
    return await res.json();
  } catch (err) {
    return { status: 'offline', error: err.message };
  }
}

export async function generatePages(figureName) {
  const response = await fetch(`${API_BASE_URL}/api/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name: figureName }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Erro do servidor (${response.status})`);
  }

  return await response.json();
}

export async function downloadAllZip(figureName, images) {
  try {
    // 1. Tenta baixar diretamente pelo endpoint do Backend
    const response = await fetch(`${API_BASE_URL}/api/download-zip`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        figure_name: figureName,
        images: images.map((img, idx) => ({
          filename: `${figureName.toLowerCase().replace(/\s+/g, '_')}_${idx + 1}.png`,
          image_base64: img.image_base64
        }))
      })
    });

    if (response.ok) {
      const blob = await response.blob();
      saveAs(blob, `paginas_colorir_${figureName.toLowerCase().replace(/\s+/g, '_')}.zip`);
      return;
    }
  } catch (e) {
    console.warn('Fallback para empacotamento ZIP local no navegador:', e);
  }

  // 2. Fallback resiliente no navegador usando JSZip
  const zip = new JSZip();
  const folder = zip.folder(`paginas_colorir_${figureName.toLowerCase().replace(/\s+/g, '_')}`);

  images.forEach((img, index) => {
    const base64Data = img.image_base64.split(',')[1];
    folder.file(`${figureName.toLowerCase().replace(/\s+/g, '_')}_variacao_${index + 1}.png`, base64Data, { base64: true });
  });

  const zipContent = await zip.generateAsync({ type: 'blob' });
  saveAs(zipContent, `paginas_colorir_${figureName.toLowerCase().replace(/\s+/g, '_')}.zip`);
}

export function downloadSinglePng(imageBase64, filename) {
  saveAs(imageBase64, filename);
}
