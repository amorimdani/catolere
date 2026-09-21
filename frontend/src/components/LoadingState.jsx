import React, { useState, useEffect } from 'react';
import { Loader2, Wand2, Scissors, Image as ImageIcon } from 'lucide-react';

const STEPS = [
  { icon: Wand2, title: 'Invocando Difusão Latente', desc: 'Gerando 5 composições com seeds diferentes no SDXL-Turbo...' },
  { icon: Scissors, title: 'Extração de Fundo com Rembg', desc: 'Removendo o fundo branco e isolando linhas pretas...' },
  { icon: ImageIcon, title: 'Renderizando Canal Alfa', desc: 'Convertendo para PNG com 100% de transparência...' },
];

export default function LoadingState({ figureName }) {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev + 1) % STEPS.length);
    }, 2800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white rounded-3xl border border-amber-200/80 shadow-lg p-8 sm:p-12 text-center max-w-2xl mx-auto my-8 animate-pulse-subtle">
      <div className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-amber-100 flex items-center justify-center text-amber-600 shadow-inner">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>

      <h3 className="text-2xl font-bold text-slate-800">
        Criando ilustrações para "{figureName}"
      </h3>
      <p className="text-sm text-slate-500 mt-2">
        Estamos gerando simultaneamente 5 variações situacionais exclusivas sem fundo.
      </p>

      {/* Etapas Visuais */}
      <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-4">
        {STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isActive = idx === currentStep;
          return (
            <div
              key={idx}
              className={`p-4 rounded-xl border text-left transition-all duration-300 ${
                isActive
                  ? 'bg-amber-50/80 border-amber-300 shadow-sm scale-102'
                  : 'bg-slate-50/60 border-slate-200 opacity-60'
              }`}
            >
              <Icon className={`w-5 h-5 mb-2 ${isActive ? 'text-amber-600' : 'text-slate-400'}`} />
              <h4 className="text-xs font-bold text-slate-800">{step.title}</h4>
              <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">{step.desc}</p>
            </div>
          );
        })}
      </div>

      <div className="mt-6 text-xs text-amber-700 bg-amber-50 px-4 py-2 rounded-lg inline-block font-medium">
        ⚡ A velocidade depende da GPU/CPU disponível no seu ambiente local.
      </div>
    </div>
  );
}
