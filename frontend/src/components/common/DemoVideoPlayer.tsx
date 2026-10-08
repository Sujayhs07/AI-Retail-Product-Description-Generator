import React, { useState, useEffect } from 'react';
import {
  Play,
  Pause,
  Volume2,
  VolumeX,
  Sparkles,
  CheckCircle2,
  Cpu,
  Layers,
  Award,
  ArrowRight,
  RefreshCw,
  FileSpreadsheet,
  Zap,
  ShieldCheck,
  Eye,
  Wand2,
  ShoppingBag,
  MousePointer,
  Subtitles,
  Check
} from 'lucide-react';
import { Link } from 'react-router-dom';

interface VideoChapter {
  id: number;
  title: string;
  timestamp: string;
  durationSeconds: number;
  badge: string;
  color: string;
  description: string;
  features: string[];
  subtitles: { time: number; text: string; clicking?: boolean; cursorTarget: { x: number; y: number } }[];
}

export const DemoVideoPlayer: React.FC = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeTab, setActiveTab] = useState<'generate' | 'batch' | 'dual_ai' | 'catalogue'>('generate');
  const [activeChapterId, setActiveChapterId] = useState(1);
  const [progress, setProgress] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const [showSubtitles, setShowSubtitles] = useState(true);
  const [speed, setSpeed] = useState<1 | 1.5 | 2>(1);
  
  // Mouse cursor position & click animation state
  const [cursorPos, setCursorPos] = useState({ x: 45, y: 30 });
  const [isClicking, setIsClicking] = useState(false);
  const [currentSubtitleText, setCurrentSubtitleText] = useState("Welcome to CatalogCraft AI demo! Press Play to start full walkthrough.");

  const [simulatedTypingText, setSimulatedTypingText] = useState("AuraSound Pro Wireless Headphones");
  const [isGenerating, setIsGenerating] = useState(false);

  const chapters: VideoChapter[] = [
    {
      id: 1,
      title: '1. Single Copy Studio Generation',
      timestamp: '00:00 - 00:45',
      durationSeconds: 45,
      badge: 'Single Copy Studio',
      color: 'from-blue-600 to-indigo-600',
      description: 'Demonstrates filling product attributes (Electronics/Fashion presets) and generating structured AI copy with quality scores.',
      features: ['Electronics & Fashion preset loader', 'Instant AI copy & SEO meta tags', '4D Quality Score calculation (0-100)'],
      subtitles: [
        { time: 0, text: "🎙️ [00:02] Step 1: Navigating to Single Copywriting Studio to generate product descriptions.", cursorTarget: { x: 20, y: 20 } },
        { time: 25, text: "🎙️ [00:10] Cursor moves to click '⚡ Load Electronics Preset' button to pre-fill SKU, price ($199.99), and features.", cursorTarget: { x: 82, y: 18 }, clicking: true },
        { time: 50, text: "🎙️ [00:22] Mouse hovers over '✨ Run Live Generation' to initiate real-time dual-AI model execution.", cursorTarget: { x: 85, y: 28 }, clicking: true },
        { time: 75, text: "🎙️ [00:35] Copy is generated! Quality Scorer awards 96/100 (SEO: 98%, Readability: 94%, Brand: 96%).", cursorTarget: { x: 50, y: 65 } }
      ]
    },
    {
      id: 2,
      title: '2. Dual AI Arbiter (Claude vs Gemini)',
      timestamp: '00:45 - 01:30',
      durationSeconds: 45,
      badge: 'Dual AI Engine',
      color: 'from-purple-600 to-cyan-600',
      description: 'Shows side-by-side prompt execution between Anthropic Claude 3.5 Sonnet & Google Gemini to pick the best description.',
      features: ['Side-by-side prompt output benchmarking', 'Transparent winning score rationale', 'Zero-downtime offline mock fallback'],
      subtitles: [
        { time: 0, text: "🎙️ [00:47] Step 2: Opening Dual-AI Model Arena for prompt benchmarking.", cursorTarget: { x: 35, y: 10 } },
        { time: 30, text: "🎙️ [00:58] Mouse highlights Anthropic Claude 3.5 output candidate (Score: 94/100 - Rich Narrative).", cursorTarget: { x: 25, y: 45 } },
        { time: 65, text: "🎙️ [01:15] Mouse moves to Google Gemini candidate (Score: 96/100 WINNER - Superior Spec Density).", cursorTarget: { x: 75, y: 45 }, clicking: true },
        { time: 85, text: "🎙️ [01:25] AI Arbiter logs decision rationale: Gemini selected for higher keyword density.", cursorTarget: { x: 50, y: 78 } }
      ]
    },
    {
      id: 3,
      title: '3. Bulk CSV / JSON Batch Processing',
      timestamp: '01:30 - 02:15',
      durationSeconds: 45,
      badge: 'Batch Processor',
      color: 'from-emerald-600 to-teal-600',
      description: 'Uploads 105-product catalog CSVs, processes batch jobs concurrently, and exports results.',
      features: ['Drag & drop CSV/JSON batch upload', 'Real-time batch progress & status tracking', '1-Click formatted CSV/JSON export'],
      subtitles: [
        { time: 0, text: "🎙️ [01:32] Step 3: Navigating to Bulk Catalog Batch Generator for multi-product uploads.", cursorTarget: { x: 52, y: 10 } },
        { time: 30, text: "🎙️ [01:45] Mouse drags 'demo_upload_products.csv' (105 items in Electronics & Fashion) into upload zone.", cursorTarget: { x: 50, y: 35 }, clicking: true },
        { time: 65, text: "🎙️ [01:58] Batch Job #104 running: 105 / 105 products processed with 100% success rate!", cursorTarget: { x: 50, y: 55 } },
        { time: 85, text: "🎙️ [02:10] Clicking 'Download Demo CSV' button to save exported descriptions to local machine.", cursorTarget: { x: 82, y: 22 }, clicking: true }
      ]
    },
    {
      id: 4,
      title: '4. Catalogue Review & Brand Rules',
      timestamp: '02:15 - 03:00',
      durationSeconds: 45,
      badge: 'Governance & Review',
      color: 'from-amber-600 to-orange-600',
      description: 'Filter catalogue items, side-by-side original vs generated comparison, approval workflow, and prohibited word safety.',
      features: ['Draft -> Needs Review -> Approved pipeline', 'Version history snapshot diffs', 'Prohibited words & brand safety enforcement'],
      subtitles: [
        { time: 0, text: "🎙️ [02:17] Step 4: Opening Product Catalogue Review & Brand Voice Governance.", cursorTarget: { x: 72, y: 10 } },
        { time: 35, text: "🎙️ [02:30] Mouse clicks on product ELEC-001 (AuraSound Headphones) to view side-by-side specs.", cursorTarget: { x: 40, y: 40 }, clicking: true },
        { time: 65, text: "🎙️ [02:45] Reviewer approves product description, updating status to 'Approved' for publication.", cursorTarget: { x: 80, y: 40 }, clicking: true },
        { time: 85, text: "🎙️ [02:55] System verifies zero prohibited words and full compliance with brand voice guidelines.", cursorTarget: { x: 50, y: 70 } }
      ]
    }
  ];

  // Video progress and subtitle/mouse tracker loop
  useEffect(() => {
    let interval: any;
    if (isPlaying) {
      interval = setInterval(() => {
        setProgress((prev) => {
          const nextProg = prev + 2 * speed;
          if (nextProg >= 100) {
            if (activeChapterId < 4) {
              const nextId = activeChapterId + 1;
              setActiveChapterId(nextId);
              switchTabByChapter(nextId);
              return 0;
            } else {
              setIsPlaying(false);
              return 100;
            }
          }

          // Update subtitle & mouse cursor targets based on current progress
          const currentChapter = chapters.find(c => c.id === activeChapterId);
          if (currentChapter) {
            const sub = currentChapter.subtitles.slice().reverse().find(s => nextProg >= s.time);
            if (sub) {
              setCurrentSubtitleText(sub.text);
              setCursorPos(sub.cursorTarget);
              if (sub.clicking) {
                setIsClicking(true);
                setTimeout(() => setIsClicking(false), 400);
              }
            }
          }

          return nextProg;
        });
      }, 200);
    }
    return () => clearInterval(interval);
  }, [isPlaying, activeChapterId, speed]);

  const switchTabByChapter = (chapterId: number) => {
    if (chapterId === 1) setActiveTab('generate');
    else if (chapterId === 2) setActiveTab('dual_ai');
    else if (chapterId === 3) setActiveTab('batch');
    else if (chapterId === 4) setActiveTab('catalogue');
  };

  const handleChapterClick = (id: number) => {
    setActiveChapterId(id);
    switchTabByChapter(id);
    setProgress(0);
    setIsPlaying(true);
  };

  const handleTriggerMockGen = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setIsGenerating(false);
    }, 1000);
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-slate-950 via-indigo-950 to-slate-900 border border-slate-800 text-white shadow-2xl">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-black bg-cyan-500/20 text-cyan-300 border border-cyan-400/30">
            <Eye className="w-3.5 h-3.5 text-cyan-400 animate-pulse" /> Live Video Demonstrator with Mouse Cursor & Subtitles
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
            CatalogCraft AI Real-Time System Walkthrough
          </h2>
          <p className="text-xs text-slate-300">
            Animated video screen demonstrating cursor navigation, button clicks, live AI prompt orchestration, and subtitles explaining every action.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl font-extrabold text-xs text-white bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 shadow-md shadow-blue-500/25 transition-all hover:scale-105 cursor-pointer"
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-current" />}
            <span>{isPlaying ? 'Pause Video' : '▶ Play Animated Video'}</span>
          </button>

          <button
            onClick={() => setShowSubtitles(!showSubtitles)}
            className={`px-3 py-2.5 rounded-xl font-bold text-xs flex items-center gap-1.5 border transition-colors cursor-pointer ${
              showSubtitles ? 'bg-yellow-500/20 text-yellow-300 border-yellow-400/40' : 'bg-slate-800 text-slate-400 border-slate-700'
            }`}
            title="Toggle Live Subtitles (CC)"
          >
            <Subtitles className="w-4 h-4 text-yellow-400" />
            <span>CC Subtitles {showSubtitles ? 'ON' : 'OFF'}</span>
          </button>
        </div>
      </div>

      {/* Main Interactive Screen & Controls */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Video Screen with Animated Cursor & Subtitles (8 Cols) */}
        <div className="lg:col-span-8 space-y-3">
          {/* Top Interactive Screen Navigation Tabs */}
          <div className="flex flex-wrap items-center gap-2 p-1.5 rounded-2xl bg-slate-900 border border-slate-800 text-xs">
            <button
              onClick={() => { setActiveTab('generate'); setActiveChapterId(1); setProgress(0); setCursorPos({ x: 20, y: 20 }); }}
              className={`px-3 py-1.5 rounded-xl font-bold transition-all flex items-center gap-1.5 cursor-pointer ${
                activeTab === 'generate' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Wand2 className="w-3.5 h-3.5" /> 1. Single Studio
            </button>

            <button
              onClick={() => { setActiveTab('dual_ai'); setActiveChapterId(2); setProgress(0); setCursorPos({ x: 35, y: 10 }); }}
              className={`px-3 py-1.5 rounded-xl font-bold transition-all flex items-center gap-1.5 cursor-pointer ${
                activeTab === 'dual_ai' ? 'bg-purple-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Cpu className="w-3.5 h-3.5" /> 2. Dual AI Arbiter
            </button>

            <button
              onClick={() => { setActiveTab('batch'); setActiveChapterId(3); setProgress(0); setCursorPos({ x: 52, y: 10 }); }}
              className={`px-3 py-1.5 rounded-xl font-bold transition-all flex items-center gap-1.5 cursor-pointer ${
                activeTab === 'batch' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Layers className="w-3.5 h-3.5" /> 3. Batch CSV
            </button>

            <button
              onClick={() => { setActiveTab('catalogue'); setActiveChapterId(4); setProgress(0); setCursorPos({ x: 72, y: 10 }); }}
              className={`px-3 py-1.5 rounded-xl font-bold transition-all flex items-center gap-1.5 cursor-pointer ${
                activeTab === 'catalogue' ? 'bg-amber-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              <ShoppingBag className="w-3.5 h-3.5" /> 4. Catalogue Review
            </button>
          </div>

          {/* Simulated Video Display Frame */}
          <div className="relative rounded-2xl bg-slate-950 border border-slate-800 overflow-hidden shadow-2xl p-5 space-y-4 min-h-[380px] flex flex-col justify-between">
            {/* ANIMATED MOUSE CURSOR OVERLAY */}
            <div
              className="absolute pointer-events-none z-30 transition-all duration-700 ease-in-out flex flex-col items-start"
              style={{ left: `${cursorPos.x}%`, top: `${cursorPos.y}%` }}
            >
              <div className="relative">
                <MousePointer className="w-6 h-6 text-cyan-400 fill-cyan-400/30 filter drop-shadow-md transform -rotate-12" />
                {isClicking && (
                  <span className="absolute -top-2 -left-2 w-10 h-10 rounded-full border-2 border-cyan-400 bg-cyan-400/30 animate-ping" />
                )}
              </div>
              <span className="text-[9px] font-mono font-bold bg-slate-950/90 text-cyan-300 px-1.5 py-0.5 rounded border border-cyan-500/40 shadow-xs mt-1">
                Cursor Target
              </span>
            </div>

            {/* Top Video Header bar */}
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-3 text-xs z-10">
              <div className="flex items-center gap-2">
                <span className="flex h-2.5 w-2.5 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500" />
                </span>
                <span className="font-mono text-[11px] uppercase tracking-wider text-slate-300 font-bold">
                  DEMO SIMULATOR • CHAPTER {activeChapterId}/4
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-400/30 font-bold">
                  DATABASE: 105 PRODUCTS (ELECTRONICS & FASHION)
                </span>
              </div>
            </div>

            {/* SCREEN VIEW 1: SINGLE STUDIO */}
            {activeTab === 'generate' && (
              <div className="space-y-4 animate-in fade-in duration-200 z-10">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-base font-black text-white flex items-center gap-2">
                      <Wand2 className="w-4 h-4 text-blue-400" /> Single Product Description Studio
                    </h3>
                    <p className="text-xs text-slate-400">Pre-fills product attributes, triggers AI engine, and outputs quality scores</p>
                  </div>

                  <button
                    onClick={handleTriggerMockGen}
                    disabled={isGenerating}
                    className="px-3 py-1.5 rounded-lg text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white flex items-center gap-1.5 transition-all cursor-pointer shadow-md"
                  >
                    {isGenerating ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
                    <span>{isGenerating ? 'Generating AI Copy...' : '✨ Run Live Generation'}</span>
                  </button>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs p-3.5 rounded-xl bg-slate-900/90 border border-slate-800">
                  <div>
                    <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Product Name</label>
                    <input
                      type="text"
                      readOnly
                      value={simulatedTypingText}
                      className="w-full px-3 py-1.5 rounded bg-slate-800 border border-slate-700 text-slate-200 text-xs font-medium"
                    />
                  </div>

                  <div>
                    <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Brand & Category</label>
                    <div className="px-3 py-1.5 rounded bg-slate-800 border border-slate-700 text-slate-300 text-xs font-medium flex justify-between">
                      <span>AuraSound</span>
                      <span className="text-cyan-400 font-bold">Electronics</span>
                    </div>
                  </div>

                  <div className="sm:col-span-2">
                    <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Key Features</label>
                    <div className="px-3 py-1.5 rounded bg-slate-800 border border-slate-700 text-slate-300 text-xs font-mono">
                      Active Noise Cancellation, 40-hour Battery Life, Spatial Audio, Bluetooth 5.3
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                    <span className="text-xs font-black text-white">Generated E-Commerce Description</span>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 flex items-center gap-1">
                      <Award className="w-3 h-3 text-emerald-400" /> Quality Score: 96/100 (Pass)
                    </span>
                  </div>

                  <p className="text-slate-300 leading-relaxed text-[11px]">
                    Immerse yourself in studio-grade acoustics with the AuraSound Pro. Featuring hybrid active noise cancellation, spatial audio positioning, and a 40-hour battery life engineered for audiophiles and remote workers.
                  </p>

                  <div className="grid grid-cols-4 gap-2 text-center text-[10px] font-bold pt-1">
                    <div className="p-1 rounded bg-emerald-950/60 border border-emerald-800/60 text-emerald-300">SEO: 98%</div>
                    <div className="p-1 rounded bg-blue-950/60 border border-blue-800/60 text-blue-300">Readability: 94%</div>
                    <div className="p-1 rounded bg-purple-950/60 border border-purple-800/60 text-purple-300">Brand: 96%</div>
                    <div className="p-1 rounded bg-cyan-950/60 border border-cyan-800/60 text-cyan-300">Complete: 100%</div>
                  </div>
                </div>
              </div>
            )}

            {/* SCREEN VIEW 2: DUAL AI ARBITER */}
            {activeTab === 'dual_ai' && (
              <div className="space-y-4 animate-in fade-in duration-200 z-10">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-base font-black text-white flex items-center gap-2">
                      <Cpu className="w-4 h-4 text-purple-400" /> Dual-AI Engine Model Arena
                    </h3>
                    <p className="text-xs text-slate-400">Benchmarking Anthropic Claude 3.5 Sonnet vs. Google Gemini</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="p-3.5 rounded-xl bg-purple-950/30 border border-purple-800/50 space-y-2">
                    <div className="flex items-center justify-between border-b border-purple-800/40 pb-2">
                      <span className="font-extrabold text-purple-300">Anthropic Claude 3.5</span>
                      <span className="text-[10px] font-bold text-slate-400">Score: 94 / 100</span>
                    </div>
                    <p className="text-[11px] text-purple-100 font-medium line-clamp-3">
                      "Experience pure audio serenity with AuraSound Pro. Designed with hybrid ANC technology, these headphones deliver deep bass and 40 hours of uninterrupted listening..."
                    </p>
                  </div>

                  <div className="p-3.5 rounded-xl bg-cyan-950/30 border border-cyan-800/50 space-y-2 ring-1 ring-cyan-500/40">
                    <div className="flex items-center justify-between border-b border-cyan-800/40 pb-2">
                      <span className="font-extrabold text-cyan-300">Google Gemini (WINNER)</span>
                      <span className="text-[10px] font-bold text-cyan-300 bg-cyan-500/20 px-2 py-0.5 rounded border border-cyan-400/30">Score: 96 / 100</span>
                    </div>
                    <p className="text-[11px] text-cyan-100 font-medium line-clamp-3">
                      "AuraSound Pro Wireless Headphones combine 40mm drivers, spatial audio, and 40-hour battery capacity. Engineered for crisp calls and audiophile acoustics..."
                    </p>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <span><strong>Arbiter Decision Rationale</strong>: Selected Google Gemini due to higher technical specification density (100%).</span>
                </div>
              </div>
            )}

            {/* SCREEN VIEW 3: BATCH PROCESSOR */}
            {activeTab === 'batch' && (
              <div className="space-y-4 animate-in fade-in duration-200 z-10">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-base font-black text-white flex items-center gap-2">
                      <Layers className="w-4 h-4 text-emerald-400" /> Bulk Catalog Batch Processor
                    </h3>
                    <p className="text-xs text-slate-400">Drag & drop batch upload and progress tracking</p>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-white">Batch Job #104: demo_upload_products.csv</span>
                    <span className="text-emerald-400 font-bold">100% Processed (105 / 105 Items)</span>
                  </div>

                  <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500 w-full" />
                  </div>

                  <div className="grid grid-cols-4 gap-2 text-center text-[10px] pt-1">
                    <div className="p-2 rounded bg-slate-800 text-slate-200"><span className="text-slate-400 block text-[9px]">Total Items</span> 105</div>
                    <div className="p-2 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800/60"><span className="text-emerald-400/70 block text-[9px]">Successful</span> 105</div>
                    <div className="p-2 rounded bg-slate-800 text-slate-200"><span className="text-slate-400 block text-[9px]">Failed</span> 0</div>
                    <div className="p-2 rounded bg-blue-950/60 text-blue-300 border border-blue-800/60"><span className="text-blue-400/70 block text-[9px]">Avg Score</span> 95.2</div>
                  </div>
                </div>
              </div>
            )}

            {/* SCREEN VIEW 4: CATALOGUE REVIEW */}
            {activeTab === 'catalogue' && (
              <div className="space-y-4 animate-in fade-in duration-200 z-10">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-base font-black text-white flex items-center gap-2">
                      <ShoppingBag className="w-4 h-4 text-amber-400" /> Catalogue Review & Brand Safety
                    </h3>
                    <p className="text-xs text-slate-400">Review workflow and brand guardrails</p>
                  </div>
                </div>

                <div className="space-y-2 text-xs">
                  <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-blue-500/20 text-blue-400 font-bold text-xs">ELEC-001</div>
                      <div>
                        <div className="font-bold text-white">AuraSound Pro Wireless Headphones</div>
                        <div className="text-[10px] text-slate-400">Category: Electronics • Tone: Professional</div>
                      </div>
                    </div>
                    <span className="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-[10px] font-bold">Approved</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-purple-500/20 text-purple-400 font-bold text-xs">FASH-026</div>
                      <div>
                        <div className="font-bold text-white">UrbanShield Waterproof Rain Jacket</div>
                        <div className="text-[10px] text-slate-400">Category: Fashion • Tone: Premium</div>
                      </div>
                    </div>
                    <span className="px-2.5 py-1 rounded-full bg-amber-500/20 text-amber-300 border border-amber-400/30 text-[10px] font-bold">Needs Review</span>
                  </div>
                </div>
              </div>
            )}

            {/* LIVE CLOSED CAPTIONS / SUBTITLE OVERLAY */}
            {showSubtitles && (
              <div className="z-20 pt-2">
                <div className="p-3 rounded-xl bg-black/90 border border-yellow-500/40 text-yellow-300 shadow-2xl text-xs sm:text-xs font-semibold leading-relaxed flex items-start gap-2 backdrop-blur-md animate-in slide-in-from-bottom-2 duration-300">
                  <Subtitles className="w-4 h-4 text-yellow-400 flex-shrink-0 mt-0.5 animate-pulse" />
                  <div className="flex-1">
                    <span className="text-[10px] text-slate-400 uppercase tracking-wider block font-mono font-bold mb-0.5">Spoken Commentary Subtitles (CC):</span>
                    <span>{currentSubtitleText}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Video Scrubber & Playbar Controls */}
            <div className="space-y-2 pt-3 border-t border-slate-800 z-10">
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden cursor-pointer">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-cyan-400 transition-all duration-200"
                  style={{ width: `${progress}%` }}
                />
              </div>

              <div className="flex items-center justify-between text-xs text-slate-300">
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => setIsPlaying(!isPlaying)}
                    className="p-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition-colors cursor-pointer shadow-md"
                  >
                    {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-current ml-0.5" />}
                  </button>

                  <button
                    onClick={() => setIsMuted(!isMuted)}
                    className="p-1.5 text-slate-400 hover:text-white transition-colors"
                  >
                    {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                  </button>

                  <span className="text-[11px] font-mono text-slate-400">
                    Chapter {activeChapterId}/4 • {chapters.find(c => c.id === activeChapterId)?.timestamp}
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1 text-[11px] bg-slate-900 px-2 py-1 rounded border border-slate-800">
                    <span className="text-slate-500 font-bold">Speed:</span>
                    {[1, 1.5, 2].map((s) => (
                      <button
                        key={s}
                        onClick={() => setSpeed(s as any)}
                        className={`px-1.5 py-0.5 rounded font-bold transition-colors ${
                          speed === s ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'
                        }`}
                      >
                        {s}x
                      </button>
                    ))}
                  </div>

                  <button
                    onClick={() => handleChapterClick(activeChapterId % 4 + 1)}
                    className="p-1.5 text-slate-400 hover:text-white transition-colors"
                    title="Next Chapter"
                  >
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Video Chapters Navigator (4 Cols) */}
        <div className="lg:col-span-4 space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 px-1">
            Walkthrough Video Chapters ({chapters.length})
          </h3>

          <div className="space-y-2">
            {chapters.map((ch) => {
              const isActive = ch.id === activeChapterId;
              return (
                <button
                  key={ch.id}
                  onClick={() => handleChapterClick(ch.id)}
                  className={`w-full text-left p-3.5 rounded-2xl transition-all duration-200 border cursor-pointer ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-950/60 via-indigo-950/60 to-slate-900 border-blue-500/60 shadow-lg shadow-blue-500/10 text-white'
                      : 'bg-white dark:bg-slate-900/60 hover:bg-slate-50 dark:hover:bg-slate-800/80 border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className={`text-xs font-black ${isActive ? 'text-cyan-400' : 'text-slate-900 dark:text-white'}`}>
                      {ch.title}
                    </span>
                    <span className="text-[10px] font-mono text-slate-400">
                      {ch.timestamp}
                    </span>
                  </div>

                  <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-2 leading-relaxed">
                    {ch.description}
                  </p>

                  {isActive && (
                    <div className="mt-2.5 pt-2 border-t border-blue-500/30 space-y-1">
                      {ch.features.map((f, i) => (
                        <div key={i} className="flex items-center gap-1.5 text-[10px] font-medium text-blue-300">
                          <CheckCircle2 className="w-3 h-3 text-cyan-400 flex-shrink-0" />
                          <span>{f}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Retailer ROI Summary Banner */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xs flex items-center gap-3">
          <div className="p-3 rounded-xl bg-blue-100 dark:bg-blue-950 text-blue-600 dark:text-blue-400">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <div className="text-lg font-black text-slate-900 dark:text-white">95% Faster</div>
            <div className="text-xs text-slate-500 dark:text-slate-400">Time-to-Market for Catalogs</div>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xs flex items-center gap-3">
          <div className="p-3 rounded-xl bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <div className="text-lg font-black text-slate-900 dark:text-white">+40% Organic Traffic</div>
            <div className="text-xs text-slate-500 dark:text-slate-400">SEO Optimized Descriptions</div>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xs flex items-center gap-3">
          <div className="p-3 rounded-xl bg-purple-100 dark:bg-purple-950 text-purple-600 dark:text-purple-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <div className="text-lg font-black text-slate-900 dark:text-white">100% Brand Safe</div>
            <div className="text-xs text-slate-500 dark:text-slate-400">Enforces Tone & Rules</div>
          </div>
        </div>
      </div>
    </div>
  );
};
