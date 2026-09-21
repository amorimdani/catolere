import React from 'react';
import { Sparkles, Layers, ShieldCheck } from 'lucide-react';

export default function Header({ serverStatus }) {
  return (
    <header className="border-b border-amber-100 bg-white/80 backdrop-blur-md sticky top-0 z-30 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-amber-600 to-amber-400 flex items-center justify-center text-white shadow-md shadow-amber-500/20">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              Catolê Colorir
              <span className="text-xs bg-amber-100 text-amber-800 font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider">
                Fundo Transparente
              </span>
            </h1>
            <p className="text-xs text-slate-500 font-medium">
              Livros de colorir de Santos Católicos & Figuras Bíblicas com IA local
            </p>
          </div>
        </div>

        <div className="hidden sm:flex items-center space-x-4 text-xs">
          <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-slate-100 text-slate-600 font-medium border border-slate-200">
            <Layers className="w-3.5 h-3.5 text-amber-600" />
            <span>5 Variações Únicas</span>
          </div>

          <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-full bg-slate-100 font-medium border border-slate-200">
            <span className={`w-2 h-2 rounded-full ${serverStatus?.status === 'online' ? 'bg-emerald-500 animate-pulse' : 'bg-amber-400'}`} />
            <span className="text-slate-600">
              {serverStatus?.status === 'online' 
                ? `Backend: ${serverStatus.device.toUpperCase()}` 
                : 'Conectando Backend...'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
