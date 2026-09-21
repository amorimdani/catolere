import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ImageCard from './components/ImageCard';
import LoadingState from './components/LoadingState';
import { generatePages, downloadAllZip, checkBackendHealth } from './services/api';
import { Search, Sparkles, Archive, RefreshCw, AlertCircle, BookOpen } from 'lucide-react';

const SUGGESTIONS = [
  'São Francisco de Assis',
  'Nossa Senhora de Fátima',
  'Moisés abrindo o Mar Vermelho',
  'São Pedro Apóstolo',
  'Arcanjo São Miguel',
  'Santa Teresa de Calcutá',
  'São José e o Menino Jesus'
];

export default function App() {
  const [figureName, setFigureName] = useState('');
  const [loading, setLoading] = useState(false);
  const [serverStatus, setServerStatus] = useState(null);
  const [error, setError] = useState(null);
  const [generatedData, setGeneratedData] = useState(null);
  const [downloadingZip, setDownloadingZip] = useState(false);

  useEffect(() => {
    // Verificar conectividade com o backend FastAPI
    checkBackendHealth().then((status) => setServerStatus(status));
  }, []);

  const handleGenerate = async (nameToUse) => {
    const query = (typeof nameToUse === 'string' ? nameToUse : figureName).trim();
    if (!query) return;

    setLoading(true);
    setError(null);

    try {
      const data = await generatePages(query);
      setGeneratedData(data);
    } catch (err) {
      console.error(err);
      setError(
        err.message || 'Erro ao gerar imagens. Certifique-se de que o backend FastAPI está em execução na porta 8000.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleZipDownload = async () => {
    if (!generatedData?.images || generatedData.images.length === 0) return;
    setDownloadingZip(true);
    try {
      await downloadAllZip(generatedData.figure, generatedData.images);
    } catch (err) {
      alert('Erro ao baixar arquivo ZIP.');
    } finally {
      setDownloadingZip(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
      <Header serverStatus={serverStatus} />

      <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Bloco Hero com Formulário de Busca */}
        <section className="text-center max-w-3xl mx-auto mb-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-semibold uppercase tracking-wider mb-4">
            <Sparkles className="w-3.5 h-3.5 text-amber-700" />
            Gerador de Desenhos Infantis
          </div>

          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Páginas de Colorir Católicas & Bíblicas
          </h2>
          <p className="mt-3 text-base text-slate-600">
            Digite o nome de um Santo ou Figura Bíblica. A IA gerará 5 ilustrações vetoriais 2D com traços pretos e fundo 100% transparente para impressão ou pintura digital.
          </p>

          {/* Campo de Input e Botão Gerar */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleGenerate();
            }}
            className="mt-8 flex flex-col sm:flex-row gap-3 shadow-md rounded-2xl bg-white p-2 border border-amber-200"
          >
            <div className="relative flex-grow flex items-center">
              <Search className="w-5 h-5 text-slate-400 absolute left-4 pointer-events-none" />
              <input
                type="text"
                value={figureName}
                onChange={(e) => setFigureName(e.target.value)}
                placeholder="Ex: São Francisco de Assis, Moisés, Virgem Maria..."
                disabled={loading}
                className="w-full pl-12 pr-4 py-3.5 bg-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-500 text-slate-800 placeholder-slate-400 font-medium"
              />
            </div>
            <button
              type="submit"
              disabled={loading || !figureName.trim()}
              className="px-8 py-3.5 bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-700 hover:to-amber-800 disabled:opacity-50 text-white font-bold rounded-xl shadow-md transition-all duration-200 flex items-center justify-center gap-2"
            >
              <Sparkles className="w-5 h-5" />
              <span>{loading ? 'Processando...' : 'Gerar Ilustrações'}</span>
            </button>
          </form>

          {/* Sugestões Rápidas */}
          <div className="mt-4 flex flex-wrap items-center justify-center gap-2">
            <span className="text-xs text-slate-400 font-medium flex items-center gap-1">
              <BookOpen className="w-3.5 h-3.5" /> Sugestões:
            </span>
            {SUGGESTIONS.map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => {
                  setFigureName(item);
                  handleGenerate(item);
                }}
                disabled={loading}
                className="text-xs bg-white hover:bg-amber-50 text-slate-600 hover:text-amber-800 px-3 py-1 rounded-full border border-slate-200 hover:border-amber-300 transition-colors duration-150 shadow-2xs font-medium"
              >
                {item}
              </button>
            ))}
          </div>
        </section>

        {/* Mensagem de Erro */}
        {error && (
          <div className="max-w-2xl mx-auto mb-8 p-4 bg-rose-50 border border-rose-200 rounded-2xl flex items-start gap-3 text-rose-800 shadow-sm">
            <AlertCircle className="w-5 h-5 mt-0.5 text-rose-600 flex-shrink-0" />
            <div className="text-sm">
              <p className="font-bold">Ocorreu um problema:</p>
              <p className="mt-0.5">{error}</p>
            </div>
          </div>
        )}

        {/* Estado de Loading */}
        {loading && <LoadingState figureName={figureName} />}

        {/* Grid de Resultados */}
        {!loading && generatedData?.images && (
          <section className="mt-6">
            <div className="flex flex-col sm:flex-row items-center justify-between pb-6 border-b border-slate-200 gap-4">
              <div>
                <div className="flex items-center gap-2 flex-wrap mb-1">
                  <h3 className="text-2xl font-bold text-slate-900">
                    Ilustrações para <span className="text-amber-700 underline decoration-amber-300">{generatedData.figure}</span>
                  </h3>
                  {generatedData.figure_id && (
                    <span className="text-xs bg-amber-100 text-amber-900 font-bold px-2.5 py-0.5 rounded-full border border-amber-300 shadow-2xs">
                      Identificador: #{generatedData.figure_id}
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-600 font-medium">
                  {generatedData.figure_title} • 5 variações situacionais autênticas com fundo transparente (PNG com canal alfa).
                </p>
              </div>

              {/* Botão Baixar Todas (ZIP) */}
              <button
                onClick={handleZipDownload}
                disabled={downloadingZip}
                className="w-full sm:w-auto px-6 py-3 bg-slate-900 hover:bg-slate-800 text-white rounded-xl font-bold shadow-md hover:shadow-lg transition-all duration-200 flex items-center justify-center gap-2.5"
              >
                {downloadingZip ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Criando ZIP...</span>
                  </>
                ) : (
                  <>
                    <Archive className="w-4 h-4 text-amber-400" />
                    <span>Baixar Todas (ZIP)</span>
                  </>
                )}
              </button>
            </div>

            {/* Grid com as 5 Imagens Simultâneas */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6 mt-8">
              {generatedData.images.map((img, idx) => (
                <ImageCard
                  key={img.id || idx}
                  image={img}
                  figureName={generatedData.figure}
                  index={idx}
                />
              ))}
            </div>
          </section>
        )}
      </main>

      {/* Rodapé */}
      <footer className="border-t border-slate-200 bg-white py-6 mt-16 text-center text-xs text-slate-400">
        <p>Catolê Colorir — Gerador autônomo com Diffusers & Rembg. Código 100% open-source.</p>
      </footer>
    </div>
  );
}
