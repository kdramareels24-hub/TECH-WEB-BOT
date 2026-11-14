import os
import re
import io
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{BUSINESS_NAME}} | Next-Gen Digital, Cloud & Enterprise Solutions</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #05050f;
      color: #ffffff;
      overflow-x: hidden;
    }
    h1, h2, h3, .font-display {
      font-family: 'Space Grotesk', sans-serif;
    }

    /* GPU-Accelerated Interactive Cursor Canvas (Zero Lag) */
    #cursor-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 9998;
      will-change: contents;
    }

    /* GPU-Accelerated Multi-Color Aurora Follower */
    #cursor-glow {
      position: fixed;
      top: 0;
      left: 0;
      width: 520px;
      height: 520px;
      margin-left: -260px;
      margin-top: -260px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(236,72,153,0.16) 0%, rgba(6,182,212,0.14) 35%, rgba(168,85,247,0.08) 60%, transparent 75%);
      pointer-events: none;
      z-index: 1;
      will-change: transform;
      transform: translate3d(-1000px, -1000px, 0);
    }

    /* Hardware-Accelerated Magnetic Cursor Dot & Rainbow Ring */
    .cursor-dot {
      position: fixed;
      top: 0;
      left: 0;
      width: 10px;
      height: 10px;
      margin-left: -5px;
      margin-top: -5px;
      background: #00f5d4;
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      will-change: transform;
      box-shadow: 0 0 12px #00f5d4, 0 0 24px #ff2a85;
    }
    .cursor-ring {
      position: fixed;
      top: 0;
      left: 0;
      width: 44px;
      height: 44px;
      margin-left: -22px;
      margin-top: -22px;
      border: 2px solid #ff2a85;
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      will-change: transform, width, height, border-color;
      transition: width 0.2s ease, height 0.2s ease, margin 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
    }
    .cursor-ring.cursor-hover {
      width: 68px;
      height: 68px;
      margin-left: -34px;
      margin-top: -34px;
      border-color: #00f5d4;
      background-color: rgba(255, 42, 133, 0.12);
    }

    /* Animated Colorful Rainbow Gradient Text */
    @keyframes gradientFlow {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    .rainbow-text {
      background: linear-gradient(90deg, #00f5d4, #38bdf8, #a855f7, #ec4899, #f59e0b, #00f5d4);
      background-size: 300% 300%;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: gradientFlow 7s ease infinite;
    }
    .rainbow-border {
      background: linear-gradient(90deg, #06b6d4, #8b5cf6, #ec4899, #f59e0b, #10b981, #06b6d4);
      background-size: 300% 300%;
      animation: gradientFlow 6s linear infinite;
    }

    /* Ultra-Smooth 60FPS Interactive Cards */
    .interactive-card {
      position: relative;
      will-change: transform;
      transition: transform 0.18s cubic-bezier(0.2, 0.8, 0.2, 1), border-color 0.25s ease;
      transform: translate3d(0, 0, 0);
    }
    .interactive-card:hover {
      transform: translate3d(0, -8px, 0) scale(1.015);
    }

    /* Smooth Infinite Marquee */
    @keyframes marquee {
      0% { transform: translate3d(0%, 0, 0); }
      100% { transform: translate3d(-50%, 0, 0); }
    }
    .animate-marquee {
      display: flex;
      width: max-content;
      will-change: transform;
      animation: marquee 26s linear infinite;
    }

    /* Smooth Floating Element */
    @keyframes floatSmooth {
      0%, 100% { transform: translate3d(0, 0px, 0); }
      50% { transform: translate3d(0, -12px, 0); }
    }
    .animate-float {
      will-change: transform;
      animation: floatSmooth 5s ease-in-out infinite;
    }

    .modal-active { display: flex !important; }
    .typing-cursor::after { content: '|'; animation: blink 1s infinite; color: #ff2a85; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
  </style>
</head>
<body class="selection:bg-pink-500 selection:text-white">

  <!-- GPU CURSOR AURORA, CANVAS & MAGNETIC RINGS -->
  <div id="cursor-glow" class="hidden md:block"></div>
  <canvas id="cursor-canvas"></canvas>
  <div id="cursor-dot" class="cursor-dot hidden md:block"></div>
  <div id="cursor-ring" class="cursor-ring hidden md:block"></div>

  <!-- 1. VIBRANT MULTI-COLOR TOP BAR -->
  <div class="rainbow-border h-1 w-full"></div>
  <div class="bg-[#090919] border-b border-indigo-500/30 text-xs py-2.5 px-6 relative z-40">
    <div class="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-3">
      <div class="flex flex-wrap items-center gap-6 text-slate-200">
        <a href="tel:{{PHONE}}" class="hover:text-pink-400 transition flex items-center font-bold">
          <span class="w-6 h-6 rounded-full bg-pink-500/20 text-pink-400 flex items-center justify-center mr-2">
            <i class="fa-solid fa-phone-volume text-[11px]"></i>
          </span>
          {{PHONE}}
        </a>
        <a href="mailto:{{EMAIL}}" class="hover:text-cyan-400 transition flex items-center font-bold">
          <span class="w-6 h-6 rounded-full bg-cyan-500/20 text-cyan-400 flex items-center justify-center mr-2">
            <i class="fa-solid fa-envelope text-[11px]"></i>
          </span>
          {{EMAIL}}
        </a>
        <span class="hidden lg:flex items-center text-slate-300 font-medium">
          <span class="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center mr-2">
            <i class="fa-solid fa-location-dot text-[11px]"></i>
          </span>
          {{ADDRESS}}
        </span>
      </div>
      <div class="flex items-center space-x-4">
        <span class="inline-flex items-center bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 px-3 py-1 rounded-full font-bold">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-2"></span> ISO 27001 Verified Enterprise
        </span>
        <button onclick="openModal('loginModal')" class="text-cyan-300 hover:text-white font-bold transition">Login</button>
        <button onclick="openModal('signupModal')" class="bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 hover:opacity-90 text-white font-extrabold px-4 py-1.5 rounded-full transition shadow-lg shadow-pink-500/30">Sign Up</button>
      </div>
    </div>
  </div>

  <!-- 2. STICKY NAVBAR -->
  <header class="sticky top-0 z-40 bg-[#070714]/90 backdrop-blur-md border-b border-purple-500/25">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <a href="#" class="flex items-center space-x-3.5 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-pink-500 via-purple-600 to-cyan-400 flex items-center justify-center text-white text-2xl shadow-lg shadow-purple-500/30 group-hover:scale-105 transition">
          <i class="fa-solid fa-wand-magic-sparkles"></i>
        </div>
        <div>
          <span class="text-xl md:text-2xl font-black tracking-tight text-white block leading-none">{{BUSINESS_NAME}}</span>
          <span class="text-[10px] font-extrabold uppercase tracking-widest rainbow-text">Digital, Cloud & AI Innovation</span>
        </div>
      </a>

      <nav class="hidden xl:flex items-center space-x-7 text-sm font-bold text-slate-200">
        <a href="#about" class="hover:text-pink-400 transition">About Us</a>
        <a href="#services" class="hover:text-cyan-400 transition">Services</a>
        <a href="#ongoing" class="hover:text-amber-400 transition">Live Projects</a>
        <a href="#portfolio" class="hover:text-emerald-400 transition">Portfolio</a>
        <a href="#process" class="hover:text-purple-400 transition">Workflow</a>
        <a href="#team" class="hover:text-pink-400 transition">Team</a>
        <a href="#verification" class="hover:text-cyan-400 transition">Verification</a>
        <a href="#contact" class="hover:text-amber-400 transition">Contact</a>
      </nav>

      <div class="flex items-center space-x-3">
        <button onclick="openModal('loginModal')" class="hidden sm:inline-flex items-center px-4 py-2.5 border border-purple-500/50 hover:border-pink-500 bg-purple-500/10 text-white rounded-xl text-xs font-extrabold uppercase tracking-wider transition">
          <i class="fa-regular fa-user mr-2 text-pink-400"></i> Log In
        </button>
        <a href="#contact" class="inline-flex items-center px-5 py-2.5 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 hover:opacity-95 text-white rounded-xl text-xs font-black uppercase tracking-wider shadow-lg shadow-cyan-500/25 transition">
          Start Project <i class="fa-solid fa-bolt ml-2 text-amber-300"></i>
        </a>
      </div>
    </div>
  </header>

  <!-- 3. COLORFUL HERO SECTION WITH LIVE VIDEO -->
  <section class="relative min-h-[92vh] flex items-center justify-center overflow-hidden px-6 py-20">
    <!-- Live Video Background -->
    <div class="absolute inset-0 z-0">
      <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1920&q=80" alt="Digital Background" class="w-full h-full object-cover opacity-30">
      <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-40">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-connections-41662-large.mp4" type="video/mp4">
      </video>
    </div>

    <!-- Vibrant Multi-Color Ambient Glows (Static GPU Layers - Zero Lag) -->
    <div class="absolute inset-0 bg-gradient-to-b from-[#05050f]/80 via-[#08081a]/75 to-[#05050f] z-10"></div>
    <div class="absolute top-10 left-10 w-80 h-80 bg-pink-600/20 rounded-full blur-3xl pointer-events-none z-10"></div>
    <div class="absolute bottom-10 right-10 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl pointer-events-none z-10"></div>
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-purple-600/15 rounded-full blur-3xl pointer-events-none z-10"></div>

    <div class="relative z-20 max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7">
        <div class="inline-flex items-center gap-2.5 bg-gradient-to-r from-pink-500/20 via-purple-500/20 to-cyan-500/20 border border-pink-500/40 px-4 py-2 rounded-full text-xs font-extrabold uppercase tracking-widest text-pink-300 mb-6 shadow-xl">
          <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping"></span>
          <span>360° Digital Transformation, Cloud & AI Studio</span>
        </div>

        <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-none mb-6 uppercase rainbow-text">
          {{BUSINESS_NAME}}
        </h1>

        <div class="text-xl sm:text-2xl md:text-3xl font-bold text-slate-200 mb-6 min-h-[42px]">
          <span class="text-amber-400">We Build: </span>
          <span id="typewriter" class="text-white typing-cursor font-extrabold"></span>
        </div>

        <p class="text-base md:text-lg text-slate-300 max-w-2xl mb-10 leading-relaxed">
          Transforming ambitious brands with ultra-fast web & mobile apps, custom cloud ERP software, AI business automation, and ROI-driven digital marketing from our head office at <strong class="text-cyan-300">{{ADDRESS}}</strong>.
        </p>

        <div class="flex flex-wrap gap-4 mb-10">
          <a href="#services" class="bg-gradient-to-r from-pink-500 via-purple-600 to-indigo-600 hover:opacity-95 text-white font-black px-8 py-4 rounded-2xl shadow-xl shadow-pink-500/25 transition transform hover:-translate-y-1 flex items-center">
            <i class="fa-solid fa-rocket mr-2.5 text-amber-300"></i> Explore Colorful Solutions
          </a>
          <a href="#contact" class="bg-gradient-to-r from-cyan-500 to-emerald-500 hover:opacity-95 text-slate-950 font-black px-8 py-4 rounded-2xl shadow-xl shadow-cyan-500/25 transition transform hover:-translate-y-1 flex items-center">
            <i class="fa-solid fa-phone-volume mr-2.5"></i> {{PHONE}}
          </a>
        </div>

        <!-- Colorful Mini Stat Pills -->
        <div class="grid grid-cols-3 gap-4 max-w-xl">
          <div class="bg-pink-500/10 border border-pink-500/30 p-3.5 rounded-2xl text-center">
            <div class="text-2xl sm:text-3xl font-black text-pink-400">380+</div>
            <div class="text-[11px] text-slate-300 font-bold uppercase">Projects Live</div>
          </div>
          <div class="bg-cyan-500/10 border border-cyan-500/30 p-3.5 rounded-2xl text-center">
            <div class="text-2xl sm:text-3xl font-black text-cyan-400">99.9%</div>
            <div class="text-[11px] text-slate-300 font-bold uppercase">Uptime SLA</div>
          </div>
          <div class="bg-amber-500/10 border border-amber-500/30 p-3.5 rounded-2xl text-center">
            <div class="text-2xl sm:text-3xl font-black text-amber-400">24/7</div>
            <div class="text-[11px] text-slate-300 font-bold uppercase">Expert Support</div>
          </div>
        </div>
      </div>

      <!-- Hero Right Colorful Floating Card -->
      <div class="lg:col-span-5">
        <div class="p-[2px] rounded-3xl rainbow-border shadow-2xl animate-float">
          <div class="bg-[#0b0b1e] rounded-3xl p-6">
            <div class="relative h-72 rounded-2xl overflow-hidden mb-5">
              <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=80" alt="Analytics Hub" class="w-full h-full object-cover">
              <div class="absolute inset-0 bg-gradient-to-t from-[#0b0b1e] via-transparent to-transparent flex flex-col justify-end p-5">
                <span class="bg-gradient-to-r from-pink-500 to-amber-500 text-white text-[10px] font-black uppercase px-3 py-1 rounded-full w-max mb-2">Live Cloud Engine</span>
                <h3 class="text-xl font-black text-white">Real-Time Performance & Growth</h3>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4 mb-4">
              <div class="bg-gradient-to-br from-purple-900/50 to-pink-900/30 p-4 rounded-2xl border border-pink-500/30">
                <div class="text-xs text-pink-200 font-semibold">Client ROI Growth</div>
                <div class="text-2xl font-black text-amber-300">+340% Avg</div>
              </div>
              <div class="bg-gradient-to-br from-cyan-900/50 to-blue-900/30 p-4 rounded-2xl border border-cyan-500/30">
                <div class="text-xs text-cyan-200 font-semibold">Cloud Speed Score</div>
                <div class="text-2xl font-black text-emerald-400">99 / 100</div>
              </div>
            </div>

            <div class="flex items-center justify-between text-xs bg-white/5 px-4 py-3 rounded-xl border border-white/10">
              <span class="text-emerald-300 font-bold"><i class="fa-solid fa-circle-check mr-2"></i>Verified Legal Entity</span>
              <a href="#verification" class="text-amber-400 font-extrabold hover:underline">Check Registry →</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 4. VIBRANT RAINBOW MARQUEE TICKER -->
  <div class="bg-gradient-to-r from-pink-600 via-purple-600 to-cyan-600 py-4 overflow-hidden shadow-lg">
    <div class="animate-marquee space-x-12 text-sm font-black uppercase tracking-wider text-white">
      <span><i class="fa-solid fa-star text-amber-300 mr-2"></i>Custom Web & Mobile App Development</span>
      <span><i class="fa-solid fa-fire text-amber-300 mr-2"></i>AI Chatbots & WhatsApp Automation</span>
      <span><i class="fa-solid fa-bolt text-amber-300 mr-2"></i>Cloud Server & DevOps Engineering</span>
      <span><i class="fa-solid fa-chart-pie text-amber-300 mr-2"></i>Performance Google & Meta Ads</span>
      <span><i class="fa-solid fa-cubes text-amber-300 mr-2"></i>Enterprise ERP, CRM & Billing Software</span>
      <span><i class="fa-solid fa-shield-halved text-amber-300 mr-2"></i>Cybersecurity & ISO Compliance</span>
      <span><i class="fa-solid fa-star text-amber-300 mr-2"></i>Custom Web & Mobile App Development</span>
      <span><i class="fa-solid fa-fire text-amber-300 mr-2"></i>AI Chatbots & WhatsApp Automation</span>
      <span><i class="fa-solid fa-bolt text-amber-300 mr-2"></i>Cloud Server & DevOps Engineering</span>
      <span><i class="fa-solid fa-chart-pie text-amber-300 mr-2"></i>Performance Google & Meta Ads</span>
    </div>
  </div>

  <!-- 5. 4 MULTI-COLOR METRIC CARDS -->
  <section class="py-20 px-6 max-w-7xl mx-auto">
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="interactive-card bg-gradient-to-br from-pink-600/20 to-rose-900/20 border-2 border-pink-500/40 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-pink-500 text-white flex items-center justify-center text-2xl shadow-lg shadow-pink-500/40">
          <i class="fa-solid fa-laptop-code"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-1">380+</div>
        <div class="text-xs font-extrabold uppercase tracking-widest text-pink-400">Platforms Delivered</div>
      </div>

      <div class="interactive-card bg-gradient-to-br from-cyan-600/20 to-blue-900/20 border-2 border-cyan-500/40 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-cyan-500 text-slate-950 flex items-center justify-center text-2xl shadow-lg shadow-cyan-500/40">
          <i class="fa-solid fa-users-gear"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-1">150+</div>
        <div class="text-xs font-extrabold uppercase tracking-widest text-cyan-400">Tech Specialists</div>
      </div>

      <div class="interactive-card bg-gradient-to-br from-amber-500/20 to-orange-900/20 border-2 border-amber-500/40 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-amber-500 text-slate-950 flex items-center justify-center text-2xl shadow-lg shadow-amber-500/40">
          <i class="fa-solid fa-trophy"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-1">99.9%</div>
        <div class="text-xs font-extrabold uppercase tracking-widest text-amber-400">Client Retention</div>
      </div>

      <div class="interactive-card bg-gradient-to-br from-emerald-500/20 to-teal-900/20 border-2 border-emerald-500/40 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-emerald-500 text-slate-950 flex items-center justify-center text-2xl shadow-lg shadow-emerald-500/40">
          <i class="fa-solid fa-shield-check"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-1">100%</div>
        <div class="text-xs font-extrabold uppercase tracking-widest text-emerald-400">Verified Security</div>
      </div>
    </div>
  </section>

  <!-- 6. ABOUT US WITH COLORFUL FRAMES -->
  <section id="about" class="py-24 px-6 max-w-7xl mx-auto">
    <div class="grid lg:grid-cols-12 gap-14 items-center">
      <div class="lg:col-span-6 grid sm:grid-cols-2 gap-6">
        <div class="interactive-card h-[440px] rounded-3xl overflow-hidden border-2 border-pink-500/50 shadow-2xl">
          <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=80" alt="Engineering Team" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent flex flex-col justify-end p-6">
            <span class="bg-pink-500 text-white text-xs font-black px-3 py-1 rounded-full w-max mb-2">Creative & Code</span>
            <h4 class="text-xl font-bold text-white">Senior Full-Stack & UI/UX Squad</h4>
          </div>
        </div>
        <div class="interactive-card h-[440px] rounded-3xl overflow-hidden border-2 border-cyan-500/50 shadow-2xl sm:mt-10">
          <img src="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=900&q=80" alt="Cloud Servers" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent flex flex-col justify-end p-6">
            <span class="bg-cyan-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full w-max mb-2">Cloud Infrastructure</span>
            <h4 class="text-xl font-bold text-white">High-Speed Server & AI Clusters</h4>
          </div>
        </div>
      </div>

      <div class="lg:col-span-6">
        <span class="bg-gradient-to-r from-pink-500 to-purple-600 text-white font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          About {{BUSINESS_NAME}}
        </span>
        <h2 class="text-3xl sm:text-5xl font-black text-white mt-5 mb-6 leading-tight">
          Where Colorful Creativity Meets <span class="rainbow-text">Enterprise Engineering</span>
        </h2>
        <p class="text-slate-300 text-base leading-relaxed mb-6">
          <strong>{{BUSINESS_NAME}}</strong> is a full-service digital transformation and software engineering powerhouse operating from <strong>{{ADDRESS}}</strong>. We help ambitious businesses scale through custom cloud software, mobile apps, and automated marketing funnels.
        </p>
        <div class="grid sm:grid-cols-2 gap-4 mb-8">
          <div class="bg-gradient-to-r from-pink-500/10 to-purple-500/10 p-5 rounded-2xl border border-pink-500/30">
            <i class="fa-solid fa-wand-magic-sparkles text-pink-400 text-xl mb-2"></i>
            <h4 class="font-bold text-white text-sm">Ultra-Modern UI/UX</h4>
            <p class="text-xs text-slate-300 mt-1">Interactive, colorful, and butter-smooth interfaces that convert visitors.</p>
          </div>
          <div class="bg-gradient-to-r from-cyan-500/10 to-emerald-500/10 p-5 rounded-2xl border border-cyan-500/30">
            <i class="fa-solid fa-server text-cyan-400 text-xl mb-2"></i>
            <h4 class="font-bold text-white text-sm">99.99% Cloud Reliability</h4>
            <p class="text-xs text-slate-300 mt-1">Auto-scaling AWS & cloud clusters with 24/7 security monitoring.</p>
          </div>
        </div>

        <div class="p-5 rounded-2xl bg-white/5 border border-white/10 flex flex-wrap justify-between items-center gap-4">
          <div>
            <span class="text-xs text-amber-400 uppercase font-bold block">Direct Helpline</span>
            <a href="tel:{{PHONE}}" class="text-lg font-black text-white hover:text-pink-400">{{PHONE}}</a>
          </div>
          <div>
            <span class="text-xs text-cyan-400 uppercase font-bold block">Official Email</span>
            <a href="mailto:{{EMAIL}}" class="text-lg font-black text-white hover:text-cyan-400">{{EMAIL}}</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 7. 8 COLORFUL DIGITAL SERVICES (EACH CARD HAS ITS OWN NEON THEME) -->
  <section id="services" class="py-28 bg-[#080818] border-y border-indigo-500/20 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-20">
        <span class="bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          Our Services Spectrum
        </span>
        <h2 class="text-4xl md:text-6xl font-black text-white mt-4">Full-Spectrum <span class="rainbow-text">Digital Solutions</span></h2>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
        <!-- Card 1: Pink -->
        <div class="interactive-card bg-gradient-to-b from-pink-500/15 to-[#0b0b1e] border-2 border-pink-500/40 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-pink-500 to-rose-600 text-white flex items-center justify-center text-2xl mb-6 shadow-lg shadow-pink-500/30">
            <i class="fa-solid fa-code"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Custom Web Portals</h3>
          <p class="text-slate-300 text-xs leading-relaxed">High-speed React, Next.js, and Node.js web platforms with interactive animations and SEO architecture.</p>
        </div>

        <!-- Card 2: Cyan -->
        <div class="interactive-card bg-gradient-to-b from-cyan-500/15 to-[#0b0b1e] border-2 border-cyan-500/40 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-400 to-blue-600 text-white flex items-center justify-center text-2xl mb-6 shadow-lg shadow-cyan-500/30">
            <i class="fa-solid fa-mobile-screen-button"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">iOS & Android Apps</h3>
          <p class="text-slate-300 text-xs leading-relaxed">Sleek Flutter & React Native mobile applications with instant push notifications and payment gateways.</p>
        </div>

        <!-- Card 3: Purple -->
        <div class="interactive-card bg-gradient-to-b from-purple-500/15 to-[#0b0b1e] border-2 border-purple-500/40 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-indigo-600 text-white flex items-center justify-center text-2xl mb-6 shadow-lg shadow-purple-500/30">
            <i class="fa-solid fa-robot"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">AI & Chat Automation</h3>
          <p class="text-slate-300 text-xs leading-relaxed">Custom AI agents, official WhatsApp Business API bots, and automated CRM lead qualification.</p>
        </div>

        <!-- Card 4: Amber -->
        <div class="interactive-card bg-gradient-to-b from-amber-500/15 to-[#0b0b1e] border-2 border-amber-500/40 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-amber-400 to-orange-600 text-slate-950 flex items-center justify-center text-2xl mb-6 shadow-lg shadow-amber-500/30">
            <i class="fa-solid fa-bullhorn"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Digital Marketing & Ads</h3>
          <p class="text-slate-300 text-xs leading-relaxed">High-converting Meta Ads, Google Search/Display campaigns, and viral social media growth strategies.</p>
        </div>

        <!-- Card 5: Emerald -->
        <div class="interactive-card bg-gradient-to-b from-emerald-500/15 to-[#0b0b1e] border-2 border-emerald-500/40 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-400 to-teal-600 text-slate-950 flex items-center justify-center text-2xl mb-6 shadow-lg shadow-emerald-500/30">
            <i class="fa-solid fa-cloud-arrow-up"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Cloud & DevOps Infra</h3>
          <p class="text-slate-300 text-xs leading-relaxed">AWS, Google Cloud, and Azure cluster management, Docker CI/CD pipelines, and 24/7 server scaling.</p>
        </div>

        <!-- Card 6: Rose/Fuchsia -->
        <div class="interactive-card bg-gradient-to-b from-fuchsia-500/15 to-[#0b0b1e] border-2 border-fuchsia-500/40 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-fuchsia-500 to-pink-600 text-white flex items-center justify-center text-2xl mb-6 shadow-lg shadow-fuchsia-500/30">
            <i class="fa-solid fa-network-wired"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Enterprise ERP & Billing</h3>
          <p class="text-slate-300 text-xs leading-relaxed">Custom inventory, GST invoicing, payroll, and multi-branch supply chain management software.</p>
        </div>

        <!-- Card 7: Sky Blue -->
        <div class="interactive-card bg-gradient-to-b from-sky-500/15 to-[#0b0b1e] border-2 border-sky-500/40 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-sky-400 to-indigo-500 text-white flex items-center justify-center text-2xl mb-6 shadow-lg shadow-sky-500/30">
            <i class="fa-solid fa-palette"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">UI/UX & Brand Design</h3>
          <p class="text-slate-300 text-xs leading-relaxed">Vibrant Figma design systems, 3D web graphics, brand identity kits, and video motion graphics.</p>
        </div>

        <!-- Card 8: Lime/Green -->
        <div class="interactive-card bg-gradient-to-b from-lime-500/15 to-[#0b0b1e] border-2 border-lime-500/40 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-lime-400 to-emerald-600 text-slate-950 flex items-center justify-center text-2xl mb-6 shadow-lg shadow-lime-500/30">
            <i class="fa-solid fa-shield-halved"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Cybersecurity & SSL</h3>
          <p class="text-slate-300 text-xs leading-relaxed">Enterprise DDoS protection, penetration testing, zero-trust firewalls, and data compliance audits.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 8. ONGOING LIVE PROJECTS (COLORFUL PROGRESS CARDS) -->
  <section id="ongoing" class="py-28 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <span class="bg-gradient-to-r from-amber-400 to-orange-500 text-slate-950 font-black uppercase tracking-widest text-xs px-4 py-2 rounded-full">
        Active R&D & Staging
      </span>
      <h2 class="text-4xl md:text-6xl font-black text-white mt-4">Ongoing <span class="rainbow-text">Live Deployments</span></h2>
    </div>

    <div class="grid lg:grid-cols-3 gap-8">
      <div class="interactive-card bg-[#0c0c20] border-2 border-pink-500/40 rounded-3xl overflow-hidden shadow-xl">
        <div class="relative h-[380px]">
          <img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=900&q=80" alt="FinTech API" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-black/30 to-transparent"></div>
          <span class="absolute top-4 left-4 bg-gradient-to-r from-pink-500 to-rose-500 text-white text-xs font-black uppercase px-4 py-1.5 rounded-full">
            <i class="fa-solid fa-spinner fa-spin mr-1"></i> Sprint Active
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <h3 class="text-2xl font-black text-white">OmniPay FinTech Core Switch</h3>
            <p class="text-xs text-pink-200 mt-1">High-frequency UPI/Card payment gateway & instant settlement dashboard.</p>
          </div>
        </div>
        <div class="p-6">
          <div class="flex justify-between text-xs font-extrabold mb-2">
            <span class="text-pink-300">Load Testing & UAT</span>
            <span class="text-amber-400">84% Done</span>
          </div>
          <div class="w-full bg-slate-800 h-3.5 rounded-full overflow-hidden">
            <div class="bg-gradient-to-r from-pink-500 via-purple-500 to-amber-400 h-full rounded-full" style="width: 84%"></div>
          </div>
        </div>
      </div>

      <div class="interactive-card bg-[#0c0c20] border-2 border-cyan-500/40 rounded-3xl overflow-hidden shadow-xl">
        <div class="relative h-[380px]">
          <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80" alt="AI ERP" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-black/30 to-transparent"></div>
          <span class="absolute top-4 left-4 bg-gradient-to-r from-cyan-400 to-blue-500 text-slate-950 text-xs font-black uppercase px-4 py-1.5 rounded-full">
            <i class="fa-solid fa-spinner fa-spin mr-1"></i> Cloud Sync
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <h3 class="text-2xl font-black text-white">Nexus AI Supply-Chain ERP</h3>
            <p class="text-xs text-cyan-200 mt-1">Automated multi-warehouse inventory & predictive dispatch engine.</p>
          </div>
        </div>
        <div class="p-6">
          <div class="flex justify-between text-xs font-extrabold mb-2">
            <span class="text-cyan-300">API Cluster Deployment</span>
            <span class="text-emerald-400">76% Done</span>
          </div>
          <div class="w-full bg-slate-800 h-3.5 rounded-full overflow-hidden">
            <div class="bg-gradient-to-r from-cyan-400 via-blue-500 to-emerald-400 h-full rounded-full" style="width: 76%"></div>
          </div>
        </div>
      </div>

      <div class="interactive-card bg-[#0c0c20] border-2 border-amber-500/40 rounded-3xl overflow-hidden shadow-xl">
        <div class="relative h-[380px]">
          <img src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=900&q=80" alt="Security Cloud" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-black/30 to-transparent"></div>
          <span class="absolute top-4 left-4 bg-gradient-to-r from-amber-400 to-orange-500 text-slate-950 text-xs font-black uppercase px-4 py-1.5 rounded-full">
            <i class="fa-solid fa-spinner fa-spin mr-1"></i> Beta Rollout
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <h3 class="text-2xl font-black text-white">Cortex Omnichannel AI CRM</h3>
            <p class="text-xs text-amber-200 mt-1">Voice bot, WhatsApp automation & real-time sales analytics cloud.</p>
          </div>
        </div>
        <div class="p-6">
          <div class="flex justify-between text-xs font-extrabold mb-2">
            <span class="text-amber-300">Production Server Ready</span>
            <span class="text-pink-400">91% Done</span>
          </div>
          <div class="w-full bg-slate-800 h-3.5 rounded-full overflow-hidden">
            <div class="bg-gradient-to-r from-amber-400 via-orange-500 to-pink-500 h-full rounded-full" style="width: 91%"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 9. COMPLETED PLATFORMS PORTFOLIO -->
  <section id="portfolio" class="py-28 bg-[#080818] border-y border-purple-500/20 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="bg-gradient-to-r from-emerald-400 to-teal-500 text-slate-950 font-black uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          100% Delivered Portfolio
        </span>
        <h2 class="text-4xl md:text-6xl font-black text-white mt-4">Completed <span class="rainbow-text">Flagship Platforms</span></h2>
      </div>

      <div class="grid lg:grid-cols-3 gap-8">
        <div class="interactive-card bg-[#0c0c20] border-2 border-emerald-500/40 rounded-3xl overflow-hidden">
          <div class="relative h-[420px]">
            <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=900&q=80" alt="B2B Cloud" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-black/30 to-transparent"></div>
            <span class="absolute top-4 left-4 bg-emerald-400 text-slate-950 text-xs font-black uppercase px-4 py-1.5 rounded-full">
              <i class="fa-solid fa-circle-check mr-1"></i> Live In Production
            </span>
            <div class="absolute bottom-5 left-5 right-5">
              <span class="text-emerald-400 text-xs font-extrabold uppercase">E-Commerce & ERP</span>
              <h3 class="text-2xl font-black text-white mt-1">PrimeTrade B2B Wholesale Cloud</h3>
              <p class="text-xs text-slate-300 mt-1">2.5L+ daily transactions with automated GST billing & dealer app.</p>
            </div>
          </div>
        </div>

        <div class="interactive-card bg-[#0c0c20] border-2 border-purple-500/40 rounded-3xl overflow-hidden">
          <div class="relative h-[420px]">
            <img src="https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=900&q=80" alt="Hospital Cloud" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-black/30 to-transparent"></div>
            <span class="absolute top-4 left-4 bg-emerald-400 text-slate-950 text-xs font-black uppercase px-4 py-1.5 rounded-full">
              <i class="fa-solid fa-circle-check mr-1"></i> Live In Production
            </span>
            <div class="absolute bottom-5 left-5 right-5">
              <span class="text-purple-400 text-xs font-extrabold uppercase">HealthTech SaaS</span>
              <h3 class="text-2xl font-black text-white mt-1">MedCore Hospital ERP Suite</h3>
              <p class="text-xs text-slate-300 mt-1">Running across 200+ hospitals with cloud lab & pharmacy modules.</p>
            </div>
          </div>
        </div>

        <div class="interactive-card bg-[#0c0c20] border-2 border-cyan-500/40 rounded-3xl overflow-hidden">
          <div class="relative h-[420px]">
            <img src="https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=900&q=80" alt="Security Gateway" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-black/30 to-transparent"></div>
            <span class="absolute top-4 left-4 bg-emerald-400 text-slate-950 text-xs font-black uppercase px-4 py-1.5 rounded-full">
              <i class="fa-solid fa-circle-check mr-1"></i> Live In Production
            </span>
            <div class="absolute bottom-5 left-5 right-5">
              <span class="text-cyan-400 text-xs font-extrabold uppercase">FinTech Security</span>
              <h3 class="text-2xl font-black text-white mt-1">VaultX Biometric eKYC Engine</h3>
              <p class="text-xs text-slate-300 mt-1">AI document verification & fraud detection gateway with 99.99% SLA.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 10. 6-STAGE COLORFUL WORKFLOW -->
  <section id="process" class="py-28 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <h2 class="text-4xl md:text-5xl font-black text-white">6-Step <span class="rainbow-text">Execution Roadmap</span></h2>
    </div>
    <div class="grid sm:grid-cols-2 lg:grid-cols-6 gap-6">
      <div class="interactive-card bg-pink-500/10 border border-pink-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-pink-400 mb-2">01</div>
        <h4 class="font-bold text-white text-sm mb-1">Strategy & SRS</h4>
        <p class="text-xs text-slate-300">Complete project blueprint & architecture planning.</p>
      </div>
      <div class="interactive-card bg-purple-500/10 border border-purple-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-purple-400 mb-2">02</div>
        <h4 class="font-bold text-white text-sm mb-1">UI/UX Prototype</h4>
        <p class="text-xs text-slate-300">Colorful Figma design & interactive wireframes.</p>
      </div>
      <div class="interactive-card bg-cyan-500/10 border border-cyan-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-cyan-400 mb-2">03</div>
        <h4 class="font-bold text-white text-sm mb-1">Agile Coding</h4>
        <p class="text-xs text-slate-300">Clean frontend, backend API & database sprints.</p>
      </div>
      <div class="interactive-card bg-amber-500/10 border border-amber-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-amber-400 mb-2">04</div>
        <h4 class="font-bold text-white text-sm mb-1">QA & Speed Test</h4>
        <p class="text-xs text-slate-300">120FPS performance optimization & security audit.</p>
      </div>
      <div class="interactive-card bg-emerald-500/10 border border-emerald-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-emerald-400 mb-2">05</div>
        <h4 class="font-bold text-white text-sm mb-1">Cloud Launch</h4>
        <p class="text-xs text-slate-300">Zero-downtime deployment on global cloud servers.</p>
      </div>
      <div class="interactive-card bg-rose-500/10 border border-rose-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-rose-400 mb-2">06</div>
        <h4 class="font-bold text-white text-sm mb-1">24/7 Growth</h4>
        <p class="text-xs text-slate-300">Dedicated SLA support, scaling & live monitoring.</p>
      </div>
    </div>
  </section>

  <!-- 11. OUR ENGINEERS & WORKFORCE -->
  <section id="team" class="py-28 bg-[#080818] border-y border-pink-500/20 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-black text-white">Our <span class="rainbow-text">Engineers & Digital Force</span></h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
        <div class="interactive-card bg-[#0c0c20] border-2 border-pink-500/40 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80" alt="Developers" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-pink-400 text-xs font-extrabold uppercase">Full-Stack Squad</span>
            <h4 class="text-xl font-bold text-white mt-1">Web & Mobile App Engineers</h4>
          </div>
        </div>
        <div class="interactive-card bg-[#0c0c20] border-2 border-cyan-500/40 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=800&q=80" alt="AI Team" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-cyan-400 text-xs font-extrabold uppercase">Cloud & AI Lab</span>
            <h4 class="text-xl font-bold text-white mt-1">DevOps & AI Architects</h4>
          </div>
        </div>
        <div class="interactive-card bg-[#0c0c20] border-2 border-amber-500/40 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80" alt="Server Crew" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-amber-400 text-xs font-extrabold uppercase">24/7 Server NOC</span>
            <h4 class="text-xl font-bold text-white mt-1">Infrastructure & Security</h4>
          </div>
        </div>
        <div class="interactive-card bg-[#0c0c20] border-2 border-emerald-500/40 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80" alt="Growth Team" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-emerald-400 text-xs font-extrabold uppercase">UI/UX & Growth</span>
            <h4 class="text-xl font-bold text-white mt-1">Product & Digital Strategists</h4>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 12. VERIFIED LEGAL ENTITY DISCLOSURE TABLE (RAINBOW BORDER) -->
  <section id="verification" class="py-24 px-6 max-w-5xl mx-auto">
    <div class="p-[3px] rounded-3xl rainbow-border shadow-2xl">
      <div class="bg-[#090919] rounded-3xl p-8 sm:p-12">
        <div class="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-white/10">
          <div>
            <span class="text-xs font-extrabold uppercase tracking-widest text-pink-400">Statutory Corporate Disclosure</span>
            <h3 class="text-2xl sm:text-3xl font-black text-white mt-1">Verified Legal Entity Information</h3>
          </div>
          <span class="bg-emerald-500/20 border border-emerald-400 text-emerald-300 text-xs font-extrabold px-4 py-2 rounded-full flex items-center">
            <i class="fa-solid fa-circle-check mr-2"></i> Active Registered Business
          </span>
        </div>

        <div class="grid md:grid-cols-2 gap-6 text-sm">
          <div class="p-5 bg-white/5 rounded-2xl border border-pink-500/30">
            <span class="text-xs font-bold uppercase text-pink-400 block mb-1">Registered Company Name</span>
            <span class="text-lg font-black text-white">{{BUSINESS_NAME}}</span>
          </div>
          <div class="p-5 bg-white/5 rounded-2xl border border-cyan-500/30">
            <span class="text-xs font-bold uppercase text-cyan-400 block mb-1">Business Category</span>
            <span class="text-lg font-black text-white">Digital Services, Software & IT Solutions</span>
          </div>
          <div class="p-5 bg-white/5 rounded-2xl border border-amber-500/30">
            <span class="text-xs font-bold uppercase text-amber-400 block mb-1">Registered Telephone Number</span>
            <a href="tel:{{PHONE}}" class="text-lg font-black text-white hover:text-amber-300">{{PHONE}}</a>
          </div>
          <div class="p-5 bg-white/5 rounded-2xl border border-emerald-500/30">
            <span class="text-xs font-bold uppercase text-emerald-400 block mb-1">Official Corporate Email</span>
            <a href="mailto:{{EMAIL}}" class="text-lg font-black text-white hover:text-emerald-300 break-all">{{EMAIL}}</a>
          </div>
          <div class="md:col-span-2 p-5 bg-white/5 rounded-2xl border border-purple-500/30">
            <span class="text-xs font-bold uppercase text-purple-400 block mb-1">Registered Head Office Address</span>
            <span class="text-base sm:text-lg font-black text-white leading-relaxed">{{ADDRESS}}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 13. COLORFUL FOOTER WITH MANDATORY NAME, ADDRESS, PHONE & EMAIL -->
  <div class="rainbow-border h-1.5 w-full"></div>
  <footer id="contact" class="bg-[#05050f] text-white pt-20 pb-12 px-6 relative z-20">
    <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 pb-16 border-b border-white/10">
      <div class="lg:col-span-5">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-pink-500 via-purple-500 to-cyan-400 flex items-center justify-center text-white text-xl font-black">
            <i class="fa-solid fa-wand-magic-sparkles"></i>
          </div>
          <span class="text-2xl font-black tracking-tight text-white">{{BUSINESS_NAME}}</span>
        </div>
        <p class="text-slate-300 text-sm leading-relaxed mb-8">
          Next-generation digital transformation, custom enterprise software, cloud infrastructure, and AI automation solutions engineered for speed and scale.
        </p>
        <div class="flex flex-wrap gap-4">
          <button onclick="openModal('loginModal')" class="bg-white/10 hover:bg-white/20 text-white text-xs font-extrabold px-6 py-3 rounded-xl transition">Client Login</button>
          <button onclick="openModal('signupModal')" class="bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 text-white text-xs font-black px-6 py-3 rounded-xl transition">Create Account</button>
        </div>
      </div>

      <div class="lg:col-span-7 grid sm:grid-cols-3 gap-6">
        <div class="interactive-card bg-gradient-to-b from-pink-500/10 to-[#0b0b1e] p-6 rounded-2xl border border-pink-500/40">
          <div class="w-10 h-10 rounded-xl bg-pink-500 text-white flex items-center justify-center text-lg mb-4">
            <i class="fa-solid fa-location-dot"></i>
          </div>
          <h4 class="text-xs font-extrabold uppercase tracking-wider text-pink-400 mb-2">Office Address</h4>
          <p class="text-sm font-bold text-white leading-relaxed">{{ADDRESS}}</p>
        </div>

        <div class="interactive-card bg-gradient-to-b from-cyan-500/10 to-[#0b0b1e] p-6 rounded-2xl border border-cyan-500/40">
          <div class="w-10 h-10 rounded-xl bg-cyan-400 text-slate-950 flex items-center justify-center text-lg mb-4">
            <i class="fa-solid fa-phone-volume"></i>
          </div>
          <h4 class="text-xs font-extrabold uppercase tracking-wider text-cyan-400 mb-2">Phone Number</h4>
          <a href="tel:{{PHONE}}" class="text-base font-black text-white hover:text-cyan-300 block">{{PHONE}}</a>
          <span class="text-[11px] text-slate-400 mt-1 block">Mon-Sat (9 AM - 8 PM)</span>
        </div>

        <div class="interactive-card bg-gradient-to-b from-amber-500/10 to-[#0b0b1e] p-6 rounded-2xl border border-amber-500/40">
          <div class="w-10 h-10 rounded-xl bg-amber-400 text-slate-950 flex items-center justify-center text-lg mb-4">
            <i class="fa-solid fa-envelope"></i>
          </div>
          <h4 class="text-xs font-extrabold uppercase tracking-wider text-amber-400 mb-2">Official Email</h4>
          <a href="mailto:{{EMAIL}}" class="text-sm font-black text-white hover:text-amber-300 break-all block">{{EMAIL}}</a>
          <span class="text-[11px] text-slate-400 mt-1 block">24/7 Official Desk</span>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto pt-8 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-400 gap-4">
      <p>© 2026 <strong>{{BUSINESS_NAME}}</strong>. All Rights Reserved. | Address: {{ADDRESS}} | Phone: {{PHONE}} | Email: {{EMAIL}}</p>
      <div class="flex space-x-6">
        <a href="#verification" class="hover:text-pink-400">Privacy Policy</a>
        <a href="#verification" class="hover:text-cyan-400">Terms & Conditions</a>
      </div>
    </div>
  </footer>

  <!-- LOGIN MODAL -->
  <div id="loginModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden items-center justify-center p-4">
    <div class="bg-[#0d0d24] border-2 border-pink-500/50 text-white w-full max-w-md p-8 rounded-3xl shadow-2xl relative">
      <button onclick="closeModal('loginModal')" class="absolute top-5 right-5 text-slate-400 hover:text-white text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-black mb-1 rainbow-text">Client Portal Login</h3>
      <p class="text-xs text-slate-400 mb-6">Sign in to manage projects at {{BUSINESS_NAME}}</p>

      <button onclick="alert('Redirecting to Google SSO...');" class="w-full bg-white hover:bg-gray-100 text-slate-900 font-bold py-3.5 px-4 rounded-xl flex items-center justify-center space-x-3 mb-5 shadow">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span class="text-sm">Continue with Google</span>
      </button>

      <form onsubmit="event.preventDefault(); alert('Logged in successfully!');" class="space-y-4 text-sm">
        <input type="email" required placeholder="Email Address" class="w-full bg-black/50 border border-purple-500/40 rounded-xl px-4 py-3 text-white">
        <input type="password" required placeholder="Password" class="w-full bg-black/50 border border-purple-500/40 rounded-xl px-4 py-3 text-white">
        <button type="submit" class="w-full bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 text-white font-black py-3.5 rounded-xl shadow-lg">Sign In</button>
      </form>
    </div>
  </div>

  <!-- SIGN UP MODAL -->
  <div id="signupModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden items-center justify-center p-4">
    <div class="bg-[#0d0d24] border-2 border-cyan-500/50 text-white w-full max-w-md p-8 rounded-3xl shadow-2xl relative">
      <button onclick="closeModal('signupModal')" class="absolute top-5 right-5 text-slate-400 hover:text-white text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-black mb-1 rainbow-text">Create Client Account</h3>
      <p class="text-xs text-slate-400 mb-6">Partner with {{BUSINESS_NAME}}</p>

      <button onclick="alert('Redirecting to Google Sign-Up...');" class="w-full bg-white hover:bg-gray-100 text-slate-900 font-bold py-3.5 px-4 rounded-xl flex items-center justify-center space-x-3 mb-5 shadow">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span class="text-sm">Sign up with Google</span>
      </button>

      <form onsubmit="event.preventDefault(); alert('Account created successfully!');" class="space-y-3.5 text-sm">
        <input type="text" required placeholder="Full Name / Company Name" class="w-full bg-black/50 border border-cyan-500/40 rounded-xl px-4 py-3 text-white">
        <input type="tel" required placeholder="Mobile Number" class="w-full bg-black/50 border border-cyan-500/40 rounded-xl px-4 py-3 text-white">
        <input type="email" required placeholder="Email Address" class="w-full bg-black/50 border border-cyan-500/40 rounded-xl px-4 py-3 text-white">
        <input type="password" required placeholder="Create Password" class="w-full bg-black/50 border border-cyan-500/40 rounded-xl px-4 py-3 text-white">
        <button type="submit" class="w-full bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 text-white font-black py-3.5 rounded-xl shadow-lg">Create Free Account</button>
      </form>
    </div>
  </div>

  <!-- 120FPS BUTTER-SMOOTH GPU CURSOR & RAINBOW PARTICLE ENGINE -->
  <script>
    function openModal(id) { document.getElementById(id).classList.add('modal-active'); }
    function closeModal(id) { document.getElementById(id).classList.remove('modal-active'); }

    // 1. Typewriter Effect
    const phrases = [
      "Colorful Web, App & Cloud Ecosystems",
      "AI Chatbots & WhatsApp Business Automation",
      "Custom Enterprise ERP & Billing Portals",
      "High-ROI Digital Marketing Campaigns"
    ];
    let pIdx = 0, cIdx = 0, isDel = false;
    const tw = document.getElementById("typewriter");
    function runType() {
      const cur = phrases[pIdx];
      tw.innerText = isDel ? cur.substring(0, cIdx--) : cur.substring(0, cIdx++);
      let spd = isDel ? 30 : 60;
      if (!isDel && cIdx > cur.length) { spd = 1800; isDel = true; }
      else if (isDel && cIdx === 0) { isDel = false; pIdx = (pIdx + 1) % phrases.length; spd = 300; }
      setTimeout(runType, spd);
    }
    document.addEventListener("DOMContentLoaded", runType);

    // 2. Zero-Lag GPU Cursor Ring, Dot & Aurora Glow (Uses translate3d only)
    const dot = document.getElementById("cursor-dot");
    const ring = document.getElementById("cursor-ring");
    const glow = document.getElementById("cursor-glow");
    const canvas = document.getElementById("cursor-canvas");
    const ctx = canvas.getContext("2d", { alpha: true });

    let mouseX = window.innerWidth / 2, mouseY = window.innerHeight / 2;
    let ringX = mouseX, ringY = mouseY;
    let glowX = mouseX, glowY = mouseY;
    let hue = 0;
    let particles = [];
    let lastSpawn = 0;

    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resizeCanvas, { passive: true });
    resizeCanvas();

    window.addEventListener("mousemove", (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;

      if (dot) {
        dot.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0)`;
      }

      // Throttle particle creation to keep 120FPS smooth
      const now = performance.now();
      if (now - lastSpawn > 16) {
        lastSpawn = now;
        hue = (hue + 14) % 360;
        particles.push({
          x: mouseX,
          y: mouseY,
          vx: (Math.random() - 0.5) * 2.8,
          vy: (Math.random() - 0.5) * 2.8,
          size: Math.random() * 4 + 2,
          alpha: 1,
          hue: hue
        });
        if (particles.length > 48) particles.shift();
      }
    }, { passive: true });

    document.querySelectorAll("a, button, .interactive-card").forEach((el) => {
      el.addEventListener("mouseenter", () => ring && ring.classList.add("cursor-hover"), { passive: true });
      el.addEventListener("mouseleave", () => ring && ring.classList.remove("cursor-hover"), { passive: true });
    });

    // Single Unified 120FPS Animation Loop (No shadowBlur = Zero Lag)
    function renderLoop() {
      ringX += (mouseX - ringX) * 0.22;
      ringY += (mouseY - ringY) * 0.22;
      glowX += (mouseX - glowX) * 0.08;
      glowY += (mouseY - glowY) * 0.08;

      if (ring) ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0)`;
      if (glow) glow.style.transform = `translate3d(${glowX}px, ${glowY}px, 0)`;

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.globalCompositeOperation = "lighter";

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.alpha -= 0.024;

        if (p.alpha <= 0) {
          particles.splice(i, 1);
          i--;
          continue;
        }

        // Draw vibrant rainbow particle (Fast GPU circle)
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${p.hue}, 100%, 60%, ${p.alpha})`;
        ctx.fill();

        // Connect sequential trail points with smooth rainbow ribbon line
        if (i > 0) {
          const prev = particles[i - 1];
          const dx = p.x - prev.x;
          const dy = p.y - prev.y;
          if (dx * dx + dy * dy < 6500) {
            ctx.beginPath();
            ctx.moveTo(prev.x, prev.y);
            ctx.lineTo(p.x, p.y);
            ctx.strokeStyle = `hsla(${p.hue}, 100%, 65%, ${p.alpha * 0.55})`;
            ctx.lineWidth = 1.6;
            ctx.stroke();
          }
        }
      }

      requestAnimationFrame(renderLoop);
    }
    requestAnimationFrame(renderLoop);
  </script>
</body>
</html>"""


def parse_details(text):
    data = {}
    for line in text.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip().lower(), v.strip()
            if "name" in k:
                data["name"] = v
            elif "phone" in k or "mobile" in k or "number" in k:
                data["phone"] = v
            elif "email" in k or "gmail" in k or "mail" in k:
                data["email"] = v
            elif "address" in k or "location" in k:
                data["address"] = v
    return data


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = (
        "🌈 *Ultra-Smooth Colorful Interactive Website Bot*\n\n"
        "Ye bot *120FPS Makhan-Smooth Rainbow Cursor Trail + Multi-Color Neon Theme* wali website generate karega.\n\n"
        "👇 *Is format me details bhejo:*\n"
        "`Name: Uday Enterprise`\n"
        "`Phone: +91 9288374176`\n"
        "`Email: udayenterprise@heoo.in`\n"
        "`Address: Bypass Road, 2nd Floor, Shantinagar Phase 3, Rewa, Madhya Pradesh 474922`"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def generate_site(message):
    data = parse_details(message.text)
    if not all(k in data for k in ["name", "phone", "email", "address"]):
        bot.reply_to(
            message,
            "⚠️ *Saari 4 details sahi format me bhejo:*\n\n"
            "`Name: Business Name`\n"
            "`Phone: +91 9876543210`\n"
            "`Email: contact@heoo.in`\n"
            "`Address: Full Address with exact Pincode`",
            parse_mode="Markdown"
        )
        return

    html = (
        HTML_TEMPLATE
        .replace("{{BUSINESS_NAME}}", data["name"])
        .replace("{{PHONE}}", data["phone"])
        .replace("{{EMAIL}}", data["email"])
        .replace("{{ADDRESS}}", data["address"])
    )

    bio = io.BytesIO(html.encode("utf-8"))
    bio.name = "index.html"

    bot.send_document(
        message.chat.id,
        bio,
        caption=(
            f"🌈 *Colorful & 120FPS Smooth Website Ready!*\n\n"
            f"🏢 *Name:* {data['name']}\n"
            f"📞 *Phone:* {data['phone']}\n"
            f"📧 *Email:* {data['email']}\n"
            f"📍 *Address:* {data['address']}\n\n"
            f"🚀 *Upgrades:* Zero-Lag GPU Cursor Trail, Rainbow Neon Gradients, Live Video & Verified Entity Box."
        ),
        parse_mode="Markdown"
    )


app = Flask(__name__)

@app.route('/')
def health():
    return "Colorful Smooth Bot Live 24/7"

if __name__ == "__main__":
    threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))),
        daemon=True
    ).start()
    try:
        bot.remove_webhook()
    except Exception:
        pass
    bot.infinity_polling(timeout=20, long_polling_timeout=20)
