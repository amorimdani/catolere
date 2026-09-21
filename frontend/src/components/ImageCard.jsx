import React, { useState } from 'react';
import { Download, Eye, Check } from 'lucide-react';
import { downloadSinglePng } from '../services/api';

export default function ImageCard({ image, figureName, index }) {
  const [downloaded, setDownloaded] = useState(false);

  const handleDownload = () => {
    const filename = `${figureName.toLowerCase().replace(/\s+/g, '_')}_variacao_${index + 1}.png`;
    downloadSinglePng(image.image_base64, filename);
    setDownloaded(true);
    setTimeout(() => setDownloaded(false), 2000);
  };

  return (
    <div className="group bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between">
      {/* Imagem com fundo xadrez demonstrando transparência */}
      <div className="relative aspect-square w-full checkerboard-pattern overflow-hidden p-6 flex items-center justify-center border-b border-slate-100">
        <img
          src={image.image_base64}
          alt={`Variação ${index + 1} de ${figureName}`}
          className="w-full h-full object-contain filter drop-shadow-md group-hover:scale-105 transition-transform duration-300 pointer-events-none select-none"
          loading="lazy"
        />
        
        {/* Badge Variação e Código */}
        <div className="absolute top-3 left-3 flex flex-col gap-1">
          <span className="bg-white/95 backdrop-blur-sm text-slate-800 text-[11px] font-bold px-2 py-0.5 rounded-md border border-slate-200 shadow-xs">
            {image.saint_code || `VAR-${index + 1}`}
          </span>
          <span className="bg-amber-100/90 text-amber-900 text-[10px] font-semibold px-2 py-0.5 rounded-md border border-amber-200/80 shadow-xs truncate max-w-[130px]">
            {image.figure_name || figureName}
          </span>
        </div>
        
        {/* Badge Fundo Alfa */}
        <span className="absolute top-3 right-3 bg-emerald-50 text-emerald-700 text-[11px] font-bold px-2 py-0.5 rounded-full border border-emerald-200 shadow-xs">
          Alfa 100%
        </span>
      </div>

      {/* Informações da variação e ação de download */}
      <div className="p-4 bg-slate-50/50 flex flex-col justify-between flex-grow">
        <div className="mb-3">
          <div className="flex items-center justify-between mb-1">
            <p className="text-[11px] font-bold text-amber-800 uppercase tracking-wide">
              Cena #{index + 1}
            </p>
            <span className="text-[10px] font-mono text-slate-400">
              Seed: {image.seed}
            </span>
          </div>
          <p className="text-xs text-slate-700 font-medium line-clamp-2" title={image.situation}>
            {image.situation}
          </p>
        </div>

        <button
          onClick={handleDownload}
          className={`w-full py-2.5 px-4 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 transition-all duration-200 shadow-sm ${
            downloaded
              ? 'bg-emerald-600 text-white'
              : 'bg-white hover:bg-amber-600 text-slate-700 hover:text-white border border-slate-300 hover:border-amber-600'
          }`}
        >
          {downloaded ? (
            <>
              <Check className="w-4 h-4" />
              <span>Baixado!</span>
            </>
          ) : (
            <>
              <Download className="w-4 h-4" />
              <span>Baixar PNG</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
