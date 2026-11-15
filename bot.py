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
  <title>{{BUSINESS_NAME}} | Luxury Real Estate, Commercial Properties & RERA Projects</title>
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

    /* GPU-Accelerated Interactive Cursor Canvas (Zero Lag 120FPS) */
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

    /* Animated Colorful Rainbow Gradient Text & Borders */
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

    /* Ultra-Smooth 120FPS Interactive Cards */
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
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-2"></span> RERA Certified & Verified Real Estate
        </span>
        <button onclick="openModal('loginModal')" class="text-cyan-300 hover:text-white font-bold transition">Buyer Login</button>
        <button onclick="openModal('signupModal')" class="bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 hover:opacity-90 text-white font-extrabold px-4 py-1.5 rounded-full transition shadow-lg shadow-pink-500/30">List Property</button>
      </div>
    </div>
  </div>

  <!-- 2. STICKY GLASSMORPHISM NAVBAR -->
  <header class="sticky top-0 z-40 bg-[#070714]/90 backdrop-blur-md border-b border-purple-500/25">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <a href="#" class="flex items-center space-x-3.5 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-pink-500 via-purple-600 to-cyan-400 flex items-center justify-center text-white text-2xl shadow-lg shadow-purple-500/30 group-hover:scale-105 transition">
          <i class="fa-solid fa-building-wheat"></i>
        </div>
        <div>
          <span class="text-xl md:text-2xl font-black tracking-tight text-white block leading-none">{{BUSINESS_NAME}}</span>
          <span class="text-[10px] font-extrabold uppercase tracking-widest rainbow-text">Luxury Properties & Real Estate Advisory</span>
        </div>
      </a>

      <nav class="hidden xl:flex items-center space-x-7 text-sm font-bold text-slate-200">
        <a href="#featured" class="hover:text-pink-400 transition">Featured Properties</a>
        <a href="#new-launches" class="hover:text-cyan-400 transition">New Launches</a>
        <a href="#services" class="hover:text-amber-400 transition">Real Estate Services</a>
        <a href="#about" class="hover:text-emerald-400 transition">About Agency</a>
        <a href="#process" class="hover:text-purple-400 transition">Buying Guide</a>
        <a href="#advisors" class="hover:text-pink-400 transition">Advisors</a>
        <a href="#verification" class="hover:text-cyan-400 transition">Legal Info</a>
        <a href="#contact" class="hover:text-amber-400 transition">Contact</a>
      </nav>

      <div class="flex items-center space-x-3">
        <button onclick="openModal('loginModal')" class="hidden sm:inline-flex items-center px-4 py-2.5 border border-purple-500/50 hover:border-pink-500 bg-purple-500/10 text-white rounded-xl text-xs font-extrabold uppercase tracking-wider transition">
          <i class="fa-regular fa-user mr-2 text-pink-400"></i> Log In
        </button>
        <a href="#contact" class="inline-flex items-center px-5 py-2.5 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 hover:opacity-95 text-white rounded-xl text-xs font-black uppercase tracking-wider shadow-lg shadow-cyan-500/25 transition">
          Book Site Visit <i class="fa-solid fa-key ml-2 text-amber-300"></i>
        </a>
      </div>
    </div>
  </header>

  <!-- 3. COLORFUL REAL ESTATE HERO SECTION WITH LIVE ARCHITECTURAL VIDEO -->
  <section class="relative min-h-[92vh] flex items-center justify-center overflow-hidden px-6 py-16">
    <!-- Live Luxury Real Estate / Skyline Video Background -->
    <div class="absolute inset-0 z-0">
      <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1920&q=85" alt="Luxury Mansion" class="w-full h-full object-cover opacity-35">
      <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-45">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-buildings-on-a-sunny-day-41465-large.mp4" type="video/mp4">
      </video>
    </div>

    <!-- Vibrant Multi-Color Ambient Glows (Static GPU Layers - Zero Lag) -->
    <div class="absolute inset-0 bg-gradient-to-b from-[#05050f]/80 via-[#08081a]/75 to-[#05050f] z-10"></div>
    <div class="absolute top-10 left-10 w-80 h-80 bg-pink-600/20 rounded-full blur-3xl pointer-events-none z-10"></div>
    <div class="absolute bottom-10 right-10 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl pointer-events-none z-10"></div>
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-purple-600/15 rounded-full blur-3xl pointer-events-none z-10"></div>

    <div class="relative z-20 max-w-7xl mx-auto w-full">
      <div class="grid lg:grid-cols-12 gap-12 items-center">
        <div class="lg:col-span-7">
          <div class="inline-flex items-center gap-2.5 bg-gradient-to-r from-pink-500/20 via-purple-500/20 to-cyan-500/20 border border-pink-500/40 px-4 py-2 rounded-full text-xs font-extrabold uppercase tracking-widest text-pink-300 mb-6 shadow-xl">
            <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping"></span>
            <span>Premier Real Estate, Commercial & Luxury Property Portal</span>
          </div>

          <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-none mb-6 uppercase rainbow-text">
            {{BUSINESS_NAME}}
          </h1>

          <div class="text-xl sm:text-2xl md:text-3xl font-bold text-slate-200 mb-6 min-h-[42px]">
            <span class="text-amber-400">Discover: </span>
            <span id="typewriter" class="text-white typing-cursor font-extrabold"></span>
          </div>

          <p class="text-base md:text-lg text-slate-300 max-w-2xl mb-8 leading-relaxed">
            Your trusted destination for buying, selling, and leasing RERA-approved residential apartments, signature villas, high-ROI commercial retail spaces, and prime plots across India. Headquartered at <strong class="text-cyan-300">{{ADDRESS}}</strong>.
          </p>

          <div class="flex flex-wrap gap-4 mb-10">
            <a href="#featured" class="bg-gradient-to-r from-pink-500 via-purple-600 to-indigo-600 hover:opacity-95 text-white font-black px-8 py-4 rounded-2xl shadow-xl shadow-pink-500/25 transition transform hover:-translate-y-1 flex items-center">
              <i class="fa-solid fa-house-chimney-window mr-2.5 text-amber-300"></i> Explore Luxury Properties
            </a>
            <a href="#contact" class="bg-gradient-to-r from-cyan-500 to-emerald-500 hover:opacity-95 text-slate-950 font-black px-8 py-4 rounded-2xl shadow-xl shadow-cyan-500/25 transition transform hover:-translate-y-1 flex items-center">
              <i class="fa-solid fa-phone-volume mr-2.5"></i> {{PHONE}}
            </a>
          </div>

          <!-- Colorful Mini Stat Pills -->
          <div class="grid grid-cols-3 gap-4 max-w-xl">
            <div class="bg-pink-500/10 border border-pink-500/30 p-3.5 rounded-2xl text-center">
              <div class="text-2xl sm:text-3xl font-black text-pink-400">1,450+</div>
              <div class="text-[11px] text-slate-300 font-bold uppercase">Properties Sold</div>
            </div>
            <div class="bg-cyan-500/10 border border-cyan-500/30 p-3.5 rounded-2xl text-center">
              <div class="text-2xl sm:text-3xl font-black text-cyan-400">100%</div>
              <div class="text-[11px] text-slate-300 font-bold uppercase">Clear Title & RERA</div>
            </div>
            <div class="bg-amber-500/10 border border-amber-500/30 p-3.5 rounded-2xl text-center">
              <div class="text-2xl sm:text-3xl font-black text-amber-400">0%</div>
              <div class="text-[11px] text-slate-300 font-bold uppercase">Hidden Charges</div>
            </div>
          </div>
        </div>

        <!-- Hero Right Colorful Floating Penthouse Showcase Card -->
        <div class="lg:col-span-5">
          <div class="p-[2px] rounded-3xl rainbow-border shadow-2xl animate-float">
            <div class="bg-[#0b0b1e] rounded-3xl p-6">
              <div class="relative h-72 rounded-2xl overflow-hidden mb-5">
                <img src="https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1000&q=85" alt="Signature Villa" class="w-full h-full object-cover">
                <span class="absolute top-4 left-4 bg-gradient-to-r from-pink-500 to-amber-500 text-white text-[11px] font-black uppercase px-3.5 py-1 rounded-full shadow-lg">
                  <i class="fa-solid fa-crown mr-1"></i> Spotlight Property
                </span>
                <span class="absolute top-4 right-4 bg-emerald-500 text-slate-950 text-xs font-black px-3 py-1 rounded-lg">
                  ₹ 3.25 Cr*
                </span>
                <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-[#0b0b1e] via-[#0b0b1e]/60 to-transparent p-5">
                  <h3 class="text-xl font-black text-white">The Imperial Sky-Villa & Penthouse</h3>
                  <p class="text-xs text-cyan-300 mt-0.5"><i class="fa-solid fa-location-dot mr-1"></i> Prime Luxury Sector • 4,200 Sq.Ft. • 5 BHK</p>
                </div>
              </div>

              <div class="grid grid-cols-3 gap-3 mb-4 text-center">
                <div class="bg-purple-900/40 p-3 rounded-xl border border-pink-500/30">
                  <div class="text-[10px] text-pink-200 uppercase font-bold">Configuration</div>
                  <div class="text-sm font-black text-white mt-0.5">4 & 5 BHK</div>
                </div>
                <div class="bg-cyan-900/40 p-3 rounded-xl border border-cyan-500/30">
                  <div class="text-[10px] text-cyan-200 uppercase font-bold">Possession</div>
                  <div class="text-sm font-black text-emerald-400 mt-0.5">Ready To Move</div>
                </div>
                <div class="bg-amber-900/40 p-3 rounded-xl border border-amber-500/30">
                  <div class="text-[10px] text-amber-200 uppercase font-bold">Rental Yield</div>
                  <div class="text-sm font-black text-amber-300 mt-0.5">8.5% ROI</div>
                </div>
              </div>

              <button onclick="openModal('visitModal')" class="w-full bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 hover:opacity-95 text-white font-black py-3.5 rounded-xl transition shadow-lg">
                <i class="fa-solid fa-calendar-check mr-2"></i> Schedule Private Site Visit
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- INTERACTIVE PROPERTY SEARCH & FILTER BAR (NEXUSPROPERTY STYLE) -->
      <div class="mt-14 p-[2px] rounded-3xl rainbow-border shadow-2xl">
        <div class="bg-[#0a0a1c]/95 backdrop-blur-xl rounded-3xl p-6 sm:p-8">
          <form onsubmit="event.preventDefault(); document.getElementById('featured').scrollIntoView({behavior: 'smooth'});" class="grid sm:grid-cols-2 lg:grid-cols-5 gap-4 items-end">
            <div>
              <label class="block text-xs font-extrabold uppercase text-pink-400 mb-2"><i class="fa-solid fa-tags mr-1.5"></i> Looking To</label>
              <select class="w-full bg-[#12122b] border border-purple-500/40 rounded-xl px-4 py-3.5 text-sm font-bold text-white focus:outline-none focus:border-pink-500">
                <option>Buy Property</option>
                <option>Commercial Lease</option>
                <option>New Launch Investment</option>
                <option>Plot / Land Purchase</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-extrabold uppercase text-cyan-400 mb-2"><i class="fa-solid fa-building mr-1.5"></i> Property Category</label>
              <select class="w-full bg-[#12122b] border border-cyan-500/40 rounded-xl px-4 py-3.5 text-sm font-bold text-white focus:outline-none focus:border-cyan-400">
                <option>Luxury Apartment / Penthouse</option>
                <option>Independent Villa / Bungalow</option>
                <option>Commercial Office / Retail Shop</option>
                <option>Residential / Industrial Plot</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-extrabold uppercase text-amber-400 mb-2"><i class="fa-solid fa-indian-rupee-sign mr-1.5"></i> Budget Range</label>
              <select class="w-full bg-[#12122b] border border-amber-500/40 rounded-xl px-4 py-3.5 text-sm font-bold text-white focus:outline-none focus:border-amber-400">
                <option>₹ 50 Lakhs - ₹ 1.50 Cr</option>
                <option>₹ 1.50 Cr - ₹ 3.00 Cr</option>
                <option>₹ 3.00 Cr - ₹ 7.50 Cr</option>
                <option>Above ₹ 7.50 Cr (Ultra Luxury)</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-extrabold uppercase text-emerald-400 mb-2"><i class="fa-solid fa-certificate mr-1.5"></i> Project Status</label>
              <select class="w-full bg-[#12122b] border border-emerald-500/40 rounded-xl px-4 py-3.5 text-sm font-bold text-white focus:outline-none focus:border-emerald-400">
                <option>Ready to Move In</option>
                <option>Under Construction (RERA)</option>
                <option>Pre-Launch Offer</option>
              </select>
            </div>
            <div>
              <button type="submit" class="w-full bg-gradient-to-r from-pink-500 via-purple-600 to-cyan-500 hover:opacity-95 text-white font-black py-3.5 px-6 rounded-xl shadow-lg shadow-pink-500/30 transition flex items-center justify-center">
                <i class="fa-solid fa-magnifying-glass mr-2"></i> Search Properties
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>

  <!-- 4. VIBRANT RAINBOW REAL ESTATE MARQUEE TICKER -->
  <div class="bg-gradient-to-r from-pink-600 via-purple-600 to-cyan-600 py-4 overflow-hidden shadow-lg">
    <div class="animate-marquee space-x-12 text-sm font-black uppercase tracking-wider text-white">
      <span><i class="fa-solid fa-building-circle-check text-amber-300 mr-2"></i>100% RERA Registered Luxury Apartments</span>
      <span><i class="fa-solid fa-gem text-amber-300 mr-2"></i>Signature Gated Villas & Penthouses</span>
      <span><i class="fa-solid fa-shop text-amber-300 mr-2"></i>High-Footfall Commercial Retail & Offices</span>
      <span><i class="fa-solid fa-map-location-dot text-amber-300 mr-2"></i>Clear-Title Residential & Industrial Plots</span>
      <span><i class="fa-solid fa-handshake text-amber-300 mr-2"></i>Instant Home Loan & Registry Assistance</span>
      <span><i class="fa-solid fa-chart-line text-amber-300 mr-2"></i>Assured High Rental Yield Investments</span>
      <span><i class="fa-solid fa-building-circle-check text-amber-300 mr-2"></i>100% RERA Registered Luxury Apartments</span>
      <span><i class="fa-solid fa-gem text-amber-300 mr-2"></i>Signature Gated Villas & Penthouses</span>
      <span><i class="fa-solid fa-shop text-amber-300 mr-2"></i>High-Footfall Commercial Retail & Offices</span>
      <span><i class="fa-solid fa-map-location-dot text-amber-300 mr-2"></i>Clear-Title Residential & Industrial Plots</span>
    </div>
  </div>

  <!-- 5. 4 MULTI-COLOR REAL ESTATE METRIC CARDS -->
  <section class="py-20 px-6 max-w-7xl mx-auto">
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="interactive-card bg-gradient-to-br from-pink-600/20 to-rose-900/20 border-2 border-pink-500/40 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-pink-500 text-white flex items-center justify-center text-2xl shadow-lg shadow-pink-500/40">
          <i class="fa-solid fa-key"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-1">1,450+</div>
        <div class="text-xs font-extrabold uppercase tracking-widest text-pink-400">Properties Handed Over</div>
      </div>

      <div class="interactive-card bg-gradient-to-br from-cyan-600/20 to-blue-900/20 border-2 border-cyan-500/40 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-cyan-400 text-slate-950 flex items-center justify-center text-2xl shadow-lg shadow-cyan-400/40">
          <i class="fa-solid fa-city"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-1">12.5M+</div>
        <div class="text-xs font-extrabold uppercase tracking-widest text-cyan-400">Sq.Ft. Area Transacted</div>
      </div>

      <div class="interactive-card bg-gradient-to-br from-amber-500/20 to-orange-900/20 border-2 border-amber-500/40 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-amber-400 text-slate-950 flex items-center justify-center text-2xl shadow-lg shadow-amber-400/40">
          <i class="fa-solid fa-face-smile-beam"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-1">4,800+</div>
        <div class="text-xs font-extrabold uppercase tracking-widest text-amber-400">Happy Property Owners</div>
      </div>

      <div class="interactive-card bg-gradient-to-br from-emerald-500/20 to-teal-900/20 border-2 border-emerald-500/40 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-emerald-400 text-slate-950 flex items-center justify-center text-2xl shadow-lg shadow-emerald-400/40">
          <i class="fa-solid fa-shield-halved"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-1">100%</div>
        <div class="text-xs font-extrabold uppercase tracking-widest text-emerald-400">Legal Title Verified</div>
      </div>
    </div>
  </section>

  <!-- 6. FEATURED LUXURY PROPERTIES (6 GIANT HD REAL ESTATE CARDS) -->
  <section id="featured" class="py-24 px-6 max-w-7xl mx-auto">
    <div class="flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
      <div>
        <span class="bg-gradient-to-r from-pink-500 to-purple-600 text-white font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          Exclusive Inventory
        </span>
        <h2 class="text-4xl md:text-6xl font-black text-white mt-4">Featured <span class="rainbow-text">Luxury Properties</span></h2>
        <p class="text-slate-300 text-sm mt-2 max-w-2xl">Handpicked residential villas, penthouses, and commercial properties with 100% clear legal titles.</p>
      </div>
      <button onclick="openModal('visitModal')" class="bg-gradient-to-r from-cyan-400 to-blue-600 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-4 rounded-xl shadow-lg transition">
        Request Complete Brochure <i class="fa-solid fa-download ml-2"></i>
      </button>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Property 1: Pink Theme -->
      <div class="interactive-card bg-[#0c0c20] border-2 border-pink-500/40 rounded-3xl overflow-hidden shadow-2xl">
        <div class="relative h-[340px]">
          <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=900&q=85" alt="Luxury Villa" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-transparent to-black/30"></div>
          <span class="absolute top-4 left-4 bg-pink-500 text-white text-xs font-black uppercase px-3.5 py-1.5 rounded-full shadow">
            Ready To Move
          </span>
          <span class="absolute top-4 right-4 bg-slate-950/90 border border-pink-400 text-pink-300 text-sm font-black px-3.5 py-1.5 rounded-xl">
            ₹ 2.85 Cr
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <span class="text-amber-300 text-xs font-extrabold uppercase"><i class="fa-solid fa-crown mr-1"></i> Signature Gated Villa</span>
            <h3 class="text-2xl font-black text-white">The Palm Royale Villa</h3>
          </div>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-3 gap-2 py-3 mb-4 border-y border-white/10 text-xs font-bold text-slate-300 text-center">
            <span><i class="fa-solid fa-bed text-pink-400 mr-1"></i> 4 BHK + Pool</span>
            <span><i class="fa-solid fa-ruler-combined text-cyan-400 mr-1"></i> 3,650 Sq.Ft.</span>
            <span><i class="fa-solid fa-compass text-amber-400 mr-1"></i> East Facing</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-xs text-emerald-400 font-bold"><i class="fa-solid fa-circle-check mr-1"></i> RERA Approved</span>
            <button onclick="openModal('visitModal')" class="bg-pink-500 hover:bg-pink-600 text-white text-xs font-black px-4 py-2.5 rounded-xl transition">Book Visit →</button>
          </div>
        </div>
      </div>

      <!-- Property 2: Cyan Theme -->
      <div class="interactive-card bg-[#0c0c20] border-2 border-cyan-500/40 rounded-3xl overflow-hidden shadow-2xl">
        <div class="relative h-[340px]">
          <img src="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=900&q=85" alt="High Rise Apartment" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-transparent to-black/30"></div>
          <span class="absolute top-4 left-4 bg-cyan-400 text-slate-950 text-xs font-black uppercase px-3.5 py-1.5 rounded-full shadow">
            Luxury High-Rise
          </span>
          <span class="absolute top-4 right-4 bg-slate-950/90 border border-cyan-400 text-cyan-300 text-sm font-black px-3.5 py-1.5 rounded-xl">
            ₹ 1.45 Cr
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <span class="text-cyan-300 text-xs font-extrabold uppercase"><i class="fa-solid fa-building mr-1"></i> Sky-Deck Residences</span>
            <h3 class="text-2xl font-black text-white">Celestia Heights 3BHK</h3>
          </div>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-3 gap-2 py-3 mb-4 border-y border-white/10 text-xs font-bold text-slate-300 text-center">
            <span><i class="fa-solid fa-bed text-cyan-400 mr-1"></i> 3 BHK Luxury</span>
            <span><i class="fa-solid fa-ruler-combined text-pink-400 mr-1"></i> 2,150 Sq.Ft.</span>
            <span><i class="fa-solid fa-car text-amber-400 mr-1"></i> 2 Covered Park</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-xs text-emerald-400 font-bold"><i class="fa-solid fa-circle-check mr-1"></i> OC Received</span>
            <button onclick="openModal('visitModal')" class="bg-cyan-400 hover:bg-cyan-300 text-slate-950 text-xs font-black px-4 py-2.5 rounded-xl transition">Book Visit →</button>
          </div>
        </div>
      </div>

      <!-- Property 3: Amber Theme -->
      <div class="interactive-card bg-[#0c0c20] border-2 border-amber-500/40 rounded-3xl overflow-hidden shadow-2xl">
        <div class="relative h-[340px]">
          <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=900&q=85" alt="Commercial Tower" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-transparent to-black/30"></div>
          <span class="absolute top-4 left-4 bg-amber-400 text-slate-950 text-xs font-black uppercase px-3.5 py-1.5 rounded-full shadow">
            Assured 9% ROI
          </span>
          <span class="absolute top-4 right-4 bg-slate-950/90 border border-amber-400 text-amber-300 text-sm font-black px-3.5 py-1.5 rounded-xl">
            ₹ 1.90 Cr
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <span class="text-amber-300 text-xs font-extrabold uppercase"><i class="fa-solid fa-briefcase mr-1"></i> Grade-A Commercial</span>
            <h3 class="text-2xl font-black text-white">Nexus Corporate Square</h3>
          </div>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-3 gap-2 py-3 mb-4 border-y border-white/10 text-xs font-bold text-slate-300 text-center">
            <span><i class="fa-solid fa-chair text-amber-400 mr-1"></i> Furnished Office</span>
            <span><i class="fa-solid fa-ruler-combined text-cyan-400 mr-1"></i> 1,800 Sq.Ft.</span>
            <span><i class="fa-solid fa-bolt text-pink-400 mr-1"></i> 100% Power Back</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-xs text-emerald-400 font-bold"><i class="fa-solid fa-circle-check mr-1"></i> Pre-Leased Option</span>
            <button onclick="openModal('visitModal')" class="bg-amber-400 hover:bg-amber-300 text-slate-950 text-xs font-black px-4 py-2.5 rounded-xl transition">Book Visit →</button>
          </div>
        </div>
      </div>

      <!-- Property 4: Purple Theme -->
      <div class="interactive-card bg-[#0c0c20] border-2 border-purple-500/40 rounded-3xl overflow-hidden shadow-2xl">
        <div class="relative h-[340px]">
          <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=900&q=85" alt="Modern Bungalow" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-transparent to-black/30"></div>
          <span class="absolute top-4 left-4 bg-purple-500 text-white text-xs font-black uppercase px-3.5 py-1.5 rounded-full shadow">
            Gated Township
          </span>
          <span class="absolute top-4 right-4 bg-slate-950/90 border border-purple-400 text-purple-300 text-sm font-black px-3.5 py-1.5 rounded-xl">
            ₹ 4.20 Cr
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <span class="text-purple-300 text-xs font-extrabold uppercase"><i class="fa-solid fa-gem mr-1"></i> Ultra-Luxury Duplex</span>
            <h3 class="text-2xl font-black text-white">Aura Golf-View Mansion</h3>
          </div>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-3 gap-2 py-3 mb-4 border-y border-white/10 text-xs font-bold text-slate-300 text-center">
            <span><i class="fa-solid fa-bed text-purple-400 mr-1"></i> 5 BHK Duplex</span>
            <span><i class="fa-solid fa-ruler-combined text-cyan-400 mr-1"></i> 4,800 Sq.Ft.</span>
            <span><i class="fa-solid fa-tree text-emerald-400 mr-1"></i> Private Lawn</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-xs text-emerald-400 font-bold"><i class="fa-solid fa-circle-check mr-1"></i> Freehold Registry</span>
            <button onclick="openModal('visitModal')" class="bg-purple-500 hover:bg-purple-600 text-white text-xs font-black px-4 py-2.5 rounded-xl transition">Book Visit →</button>
          </div>
        </div>
      </div>

      <!-- Property 5: Emerald Theme -->
      <div class="interactive-card bg-[#0c0c20] border-2 border-emerald-500/40 rounded-3xl overflow-hidden shadow-2xl">
        <div class="relative h-[340px]">
          <img src="https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=900&q=85" alt="Retail Showroom" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-transparent to-black/30"></div>
          <span class="absolute top-4 left-4 bg-emerald-400 text-slate-950 text-xs font-black uppercase px-3.5 py-1.5 rounded-full shadow">
            High-Street Retail
          </span>
          <span class="absolute top-4 right-4 bg-slate-950/90 border border-emerald-400 text-emerald-300 text-sm font-black px-3.5 py-1.5 rounded-xl">
            ₹ 95 Lakhs
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <span class="text-emerald-300 text-xs font-extrabold uppercase"><i class="fa-solid fa-shop mr-1"></i> Double-Height Shop</span>
            <h3 class="text-2xl font-black text-white">Galleria Boulevard Retail</h3>
          </div>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-3 gap-2 py-3 mb-4 border-y border-white/10 text-xs font-bold text-slate-300 text-center">
            <span><i class="fa-solid fa-store text-emerald-400 mr-1"></i> Ground Floor</span>
            <span><i class="fa-solid fa-ruler-combined text-cyan-400 mr-1"></i> 850 Sq.Ft.</span>
            <span><i class="fa-solid fa-road text-amber-400 mr-1"></i> 60m Main Road</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-xs text-emerald-400 font-bold"><i class="fa-solid fa-circle-check mr-1"></i> Bank Loan Approved</span>
            <button onclick="openModal('visitModal')" class="bg-emerald-400 hover:bg-emerald-300 text-slate-950 text-xs font-black px-4 py-2.5 rounded-xl transition">Book Visit →</button>
          </div>
        </div>
      </div>

      <!-- Property 6: Rose Theme -->
      <div class="interactive-card bg-[#0c0c20] border-2 border-rose-500/40 rounded-3xl overflow-hidden shadow-2xl">
        <div class="relative h-[340px]">
          <img src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=900&q=85" alt="Luxury Interior" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-transparent to-black/30"></div>
          <span class="absolute top-4 left-4 bg-rose-500 text-white text-xs font-black uppercase px-3.5 py-1.5 rounded-full shadow">
            Fully Furnished
          </span>
          <span class="absolute top-4 right-4 bg-slate-950/90 border border-rose-400 text-rose-300 text-sm font-black px-3.5 py-1.5 rounded-xl">
            ₹ 1.75 Cr
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <span class="text-rose-300 text-xs font-extrabold uppercase"><i class="fa-solid fa-star mr-1"></i> Smart Home Residences</span>
            <h3 class="text-2xl font-black text-white">Sovereign Smart 4BHK</h3>
          </div>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-3 gap-2 py-3 mb-4 border-y border-white/10 text-xs font-bold text-slate-300 text-center">
            <span><i class="fa-solid fa-bed text-rose-400 mr-1"></i> 4 BHK + Servant</span>
            <span><i class="fa-solid fa-ruler-combined text-cyan-400 mr-1"></i> 2,680 Sq.Ft.</span>
            <span><i class="fa-solid fa-water-ladder text-amber-400 mr-1"></i> Club & Pool</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-xs text-emerald-400 font-bold"><i class="fa-solid fa-circle-check mr-1"></i> Immediate Registry</span>
            <button onclick="openModal('visitModal')" class="bg-rose-500 hover:bg-rose-600 text-white text-xs font-black px-4 py-2.5 rounded-xl transition">Book Visit →</button>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 7. NEW LAUNCH & UNDER-CONSTRUCTION RERA PROJECTS -->
  <section id="new-launches" class="py-28 bg-[#080818] border-y border-indigo-500/20 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="bg-gradient-to-r from-amber-400 to-orange-500 text-slate-950 font-black uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          Pre-Launch & Ongoing Developments
        </span>
        <h2 class="text-4xl md:text-6xl font-black text-white mt-4">New Launch <span class="rainbow-text">RERA Projects</span></h2>
        <p class="text-slate-300 text-sm mt-2 max-w-2xl mx-auto">Invest early in our high-appreciation upcoming residential townships and commercial hubs.</p>
      </div>

      <div class="grid lg:grid-cols-3 gap-8">
        <div class="interactive-card bg-[#0c0c20] border-2 border-pink-500/40 rounded-3xl overflow-hidden shadow-xl">
          <div class="relative h-[360px]">
            <img src="https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=900&q=85" alt="Under Construction Tower" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-black/30 to-transparent"></div>
            <span class="absolute top-4 left-4 bg-gradient-to-r from-pink-500 to-rose-500 text-white text-xs font-black uppercase px-4 py-1.5 rounded-full">
              <i class="fa-solid fa-fire mr-1"></i> Booking Open
            </span>
            <div class="absolute bottom-4 left-5 right-5">
              <h3 class="text-2xl font-black text-white">Pinnacle World Towers</h3>
              <p class="text-xs text-pink-200 mt-1">G+24 Luxury Residential Towers • Starting ₹ 88 Lakhs*</p>
            </div>
          </div>
          <div class="p-6">
            <div class="flex justify-between text-xs font-extrabold mb-2">
              <span class="text-pink-300">RCC Structure & Tower Crane Stage</span>
              <span class="text-amber-400">78% Completed</span>
            </div>
            <div class="w-full bg-slate-800 h-3.5 rounded-full overflow-hidden">
              <div class="bg-gradient-to-r from-pink-500 via-purple-500 to-amber-400 h-full rounded-full" style="width: 78%"></div>
            </div>
          </div>
        </div>

        <div class="interactive-card bg-[#0c0c20] border-2 border-cyan-500/40 rounded-3xl overflow-hidden shadow-xl">
          <div class="relative h-[360px]">
            <img src="https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=900&q=85" alt="Commercial IT Park" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-black/30 to-transparent"></div>
            <span class="absolute top-4 left-4 bg-gradient-to-r from-cyan-400 to-blue-500 text-slate-950 text-xs font-black uppercase px-4 py-1.5 rounded-full">
              <i class="fa-solid fa-bolt mr-1"></i> Nearing Possession
            </span>
            <div class="absolute bottom-4 left-5 right-5">
              <h3 class="text-2xl font-black text-white">CyberOne Commercial Plaza</h3>
              <p class="text-xs text-cyan-200 mt-1">Lockable Office Spaces & Food Court • Starting ₹ 65 Lakhs*</p>
            </div>
          </div>
          <div class="p-6">
            <div class="flex justify-between text-xs font-extrabold mb-2">
              <span class="text-cyan-300">Glass Facade & Interior Finishing</span>
              <span class="text-emerald-400">91% Completed</span>
            </div>
            <div class="w-full bg-slate-800 h-3.5 rounded-full overflow-hidden">
              <div class="bg-gradient-to-r from-cyan-400 via-blue-500 to-emerald-400 h-full rounded-full" style="width: 91%"></div>
            </div>
          </div>
        </div>

        <div class="interactive-card bg-[#0c0c20] border-2 border-amber-500/40 rounded-3xl overflow-hidden shadow-xl">
          <div class="relative h-[360px]">
            <img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=900&q=85" alt="Plotted Township" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-[#0c0c20] via-black/30 to-transparent"></div>
            <span class="absolute top-4 left-4 bg-gradient-to-r from-amber-400 to-orange-500 text-slate-950 text-xs font-black uppercase px-4 py-1.5 rounded-full">
              <i class="fa-solid fa-map-pin mr-1"></i> Freehold Plots
            </span>
            <div class="absolute bottom-4 left-5 right-5">
              <h3 class="text-2xl font-black text-white">Emerald Green Plotted City</h3>
              <p class="text-xs text-amber-200 mt-1">1000 to 4500 Sq.Ft. Gated Villa Plots • Starting ₹ 42 Lakhs*</p>
            </div>
          </div>
          <div class="p-6">
            <div class="flex justify-between text-xs font-extrabold mb-2">
              <span class="text-amber-300">Wide Roads, Park & Underground Electrification</span>
              <span class="text-pink-400">85% Completed</span>
            </div>
            <div class="w-full bg-slate-800 h-3.5 rounded-full overflow-hidden">
              <div class="bg-gradient-to-r from-amber-400 via-orange-500 to-pink-500 h-full rounded-full" style="width: 85%"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 8. 8 COLORFUL REAL ESTATE SERVICES -->
  <section id="services" class="py-28 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-20">
      <span class="bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
        End-To-End Property Solutions
      </span>
      <h2 class="text-4xl md:text-6xl font-black text-white mt-4">360° Real Estate <span class="rainbow-text">Advisory Services</span></h2>
    </div>

    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
      <div class="interactive-card bg-gradient-to-b from-pink-500/15 to-[#0b0b1e] border-2 border-pink-500/40 p-8 rounded-3xl">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-pink-500 to-rose-600 text-white flex items-center justify-center text-2xl mb-6 shadow-lg">
          <i class="fa-solid fa-house-chimney"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-3">Residential Buying & Selling</h3>
        <p class="text-slate-300 text-xs leading-relaxed">Verified luxury apartments, builder floors, penthouses, and independent villas across prime residential sectors.</p>
      </div>

      <div class="interactive-card bg-gradient-to-b from-cyan-500/15 to-[#0b0b1e] border-2 border-cyan-500/40 p-8 rounded-3xl">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-400 to-blue-600 text-white flex items-center justify-center text-2xl mb-6 shadow-lg">
          <i class="fa-solid fa-building"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-3">Commercial Office & Retail</h3>
        <p class="text-slate-300 text-xs leading-relaxed">Pre-leased corporate offices, high-street retail showrooms, food courts, and institutional commercial buildings.</p>
      </div>

      <div class="interactive-card bg-gradient-to-b from-purple-500/15 to-[#0b0b1e] border-2 border-purple-500/40 p-8 rounded-3xl">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-indigo-600 text-white flex items-center justify-center text-2xl mb-6 shadow-lg">
          <i class="fa-solid fa-map-location-dot"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-3">Plots & Land Acquisition</h3>
        <p class="text-slate-300 text-xs leading-relaxed">CLU-cleared residential plots, industrial land parcels, warehouse zones, and agricultural farmhouses.</p>
      </div>

      <div class="interactive-card bg-gradient-to-b from-amber-500/15 to-[#0b0b1e] border-2 border-amber-500/40 p-8 rounded-3xl">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-amber-400 to-orange-600 text-slate-950 flex items-center justify-center text-2xl mb-6 shadow-lg">
          <i class="fa-solid fa-building-columns"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-3">Home Loan & Mortgage Desk</h3>
        <p class="text-slate-300 text-xs leading-relaxed">Instant home loan sanction from SBI, HDFC, ICICI & Axis Bank at lowest interest rates with doorstep documentation.</p>
      </div>

      <div class="interactive-card bg-gradient-to-b from-emerald-500/15 to-[#0b0b1e] border-2 border-emerald-500/40 p-8 rounded-3xl">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-400 to-teal-600 text-slate-950 flex items-center justify-center text-2xl mb-6 shadow-lg">
          <i class="fa-solid fa-scale-balanced"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-3">Legal Title & Registry Audit</h3>
        <p class="text-slate-300 text-xs leading-relaxed">30-year chain document verification, RERA compliance check, stamp duty calculation, and sub-registrar sale deed execution.</p>
      </div>

      <div class="interactive-card bg-gradient-to-b from-fuchsia-500/15 to-[#0b0b1e] border-2 border-fuchsia-500/40 p-8 rounded-3xl">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-fuchsia-500 to-pink-600 text-white flex items-center justify-center text-2xl mb-6 shadow-lg">
          <i class="fa-solid fa-earth-americas"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-3">NRI Property Management</h3>
        <p class="text-slate-300 text-xs leading-relaxed">Dedicated portfolio management, tenant verification, rent collection, and virtual video site tours for NRI investors.</p>
      </div>

      <div class="interactive-card bg-gradient-to-b from-sky-500/15 to-[#0b0b1e] border-2 border-sky-500/40 p-8 rounded-3xl">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-sky-400 to-indigo-500 text-white flex items-center justify-center text-2xl mb-6 shadow-lg">
          <i class="fa-solid fa-couch"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-3">Luxury Interior & Turnkey</h3>
        <p class="text-slate-300 text-xs leading-relaxed">Complete modular kitchens, false ceiling, smart home automation, and luxury furnishing before you move in.</p>
      </div>

      <div class="interactive-card bg-gradient-to-b from-lime-500/15 to-[#0b0b1e] border-2 border-lime-500/40 p-8 rounded-3xl">
        <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-lime-400 to-emerald-600 text-slate-950 flex items-center justify-center text-2xl mb-6 shadow-lg">
          <i class="fa-solid fa-chart-pie"></i>
        </div>
        <h3 class="text-xl font-bold text-white mb-3">High-ROI Investment Advisory</h3>
        <p class="text-slate-300 text-xs leading-relaxed">Data-backed real estate wealth planning focused on capital appreciation and assured corporate lease returns.</p>
      </div>
    </div>
  </section>

  <!-- 9. ABOUT REAL ESTATE AGENCY SECTION -->
  <section id="about" class="py-24 bg-[#080818] border-y border-pink-500/20 px-6">
    <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-14 items-center">
      <div class="lg:col-span-6 grid sm:grid-cols-2 gap-6">
        <div class="interactive-card h-[440px] rounded-3xl overflow-hidden border-2 border-pink-500/50 shadow-2xl">
          <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=900&q=85" alt="Luxury Villa Interior" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent flex flex-col justify-end p-6">
            <span class="bg-pink-500 text-white text-xs font-black px-3 py-1 rounded-full w-max mb-2">100% Verified</span>
            <h4 class="text-xl font-bold text-white">Premium Residential & Villa Portfolio</h4>
          </div>
        </div>
        <div class="interactive-card h-[440px] rounded-3xl overflow-hidden border-2 border-cyan-500/50 shadow-2xl sm:mt-10">
          <img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=900&q=85" alt="Property Key Handover" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent flex flex-col justify-end p-6">
            <span class="bg-cyan-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full w-max mb-2">Transparent Deals</span>
            <h4 class="text-xl font-bold text-white">Direct Builder Price & Instant Registry</h4>
          </div>
        </div>
      </div>

      <div class="lg:col-span-6">
        <span class="bg-gradient-to-r from-pink-500 to-purple-600 text-white font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          About {{BUSINESS_NAME}}
        </span>
        <h2 class="text-3xl sm:text-5xl font-black text-white mt-5 mb-6 leading-tight">
          Setting The Gold Standard In <span class="rainbow-text">Real Estate Excellence</span>
        </h2>
        <p class="text-slate-300 text-base leading-relaxed mb-6">
          <strong>{{BUSINESS_NAME}}</strong> is a premier real estate consultancy, property development, and asset management company headquartered at <strong>{{ADDRESS}}</strong>. We connect homebuyers, corporate tenants, and institutional investors with RERA-verified properties.
        </p>
        <p class="text-slate-300 text-sm leading-relaxed mb-8">
          Every property listed with us passes a strict 40-point legal and structural inspection covering title deed history, municipal approvals, occupancy certificates, and builder track record.
        </p>

        <div class="p-5 rounded-2xl bg-white/5 border border-white/10 flex flex-wrap justify-between items-center gap-4">
          <div>
            <span class="text-xs text-amber-400 uppercase font-bold block">Property Helpline</span>
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

  <!-- 10. 6-STEP PROPERTY BUYING & REGISTRY WORKFLOW -->
  <section id="process" class="py-28 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <h2 class="text-4xl md:text-5xl font-black text-white">6-Step <span class="rainbow-text">Property Buying Journey</span></h2>
    </div>
    <div class="grid sm:grid-cols-2 lg:grid-cols-6 gap-6">
      <div class="interactive-card bg-pink-500/10 border border-pink-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-pink-400 mb-2">01</div>
        <h4 class="font-bold text-white text-sm mb-1">Requirement Call</h4>
        <p class="text-xs text-slate-300">Share your budget, preferred location, and BHK/office size.</p>
      </div>
      <div class="interactive-card bg-purple-500/10 border border-purple-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-purple-400 mb-2">02</div>
        <h4 class="font-bold text-white text-sm mb-1">VIP Site Visits</h4>
        <p class="text-xs text-slate-300">Chauffeur-driven guided visits to shortlisted RERA projects.</p>
      </div>
      <div class="interactive-card bg-cyan-500/10 border border-cyan-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-cyan-400 mb-2">03</div>
        <h4 class="font-bold text-white text-sm mb-1">Best Price Deal</h4>
        <p class="text-xs text-slate-300">Direct table negotiation for lowest builder/owner rate.</p>
      </div>
      <div class="interactive-card bg-amber-500/10 border border-amber-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-amber-400 mb-2">04</div>
        <h4 class="font-bold text-white text-sm mb-1">Legal Verification</h4>
        <p class="text-xs text-slate-300">Complete title deed, RERA & encumbrance certificate check.</p>
      </div>
      <div class="interactive-card bg-emerald-500/10 border border-emerald-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-emerald-400 mb-2">05</div>
        <h4 class="font-bold text-white text-sm mb-1">Home Loan Sanction</h4>
        <p class="text-xs text-slate-300">Fast-track bank loan processing within 5 working days.</p>
      </div>
      <div class="interactive-card bg-rose-500/10 border border-rose-500/40 p-6 rounded-2xl">
        <div class="text-3xl font-black text-rose-400 mb-2">06</div>
        <h4 class="font-bold text-white text-sm mb-1">Registry & Keys</h4>
        <p class="text-xs text-slate-300">Sale deed registration and ceremonial key handover.</p>
      </div>
    </div>
  </section>

  <!-- 11. SENIOR PROPERTY CONSULTANTS & LEGAL ADVISORS -->
  <section id="advisors" class="py-28 bg-[#080818] border-y border-purple-500/20 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-black text-white">Our <span class="rainbow-text">Property Advisors & Legal Desk</span></h2>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
        <div class="interactive-card bg-[#0c0c20] border-2 border-pink-500/40 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=800&q=80" alt="Luxury Property Head" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-pink-400 text-xs font-extrabold uppercase">Residential Desk</span>
            <h4 class="text-xl font-bold text-white mt-1">Luxury Villa & Penthouse Team</h4>
          </div>
        </div>
        <div class="interactive-card bg-[#0c0c20] border-2 border-cyan-500/40 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=800&q=80" alt="Commercial Leasing" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-cyan-400 text-xs font-extrabold uppercase">Commercial & Retail</span>
            <h4 class="text-xl font-bold text-white mt-1">Corporate Leasing Specialists</h4>
          </div>
        </div>
        <div class="interactive-card bg-[#0c0c20] border-2 border-amber-500/40 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=800&q=80" alt="Legal Advocates" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-amber-400 text-xs font-extrabold uppercase">RERA & Registry</span>
            <h4 class="text-xl font-bold text-white mt-1">Property Legal & Documentation</h4>
          </div>
        </div>
        <div class="interactive-card bg-[#0c0c20] border-2 border-emerald-500/40 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1556157382-97eda2d62296?auto=format&fit=crop&w=800&q=80" alt="Home Loan Desk" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-emerald-400 text-xs font-extrabold uppercase">Banking & Finance</span>
            <h4 class="text-xl font-bold text-white mt-1">Home Loan & NRI Portfolio Desk</h4>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 12. VERIFIED LEGAL ENTITY DISCLOSURE TABLE (RAINBOW BORDER FOR META VERIFICATION) -->
  <section id="verification" class="py-24 px-6 max-w-5xl mx-auto">
    <div class="p-[3px] rounded-3xl rainbow-border shadow-2xl">
      <div class="bg-[#090919] rounded-3xl p-8 sm:p-12">
        <div class="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-white/10">
          <div>
            <span class="text-xs font-extrabold uppercase tracking-widest text-pink-400">Statutory Real Estate Disclosure</span>
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
            <span class="text-lg font-black text-white">Real Estate Advisory, Property Development & Housing</span>
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
            <i class="fa-solid fa-building-wheat"></i>
          </div>
          <span class="text-2xl font-black tracking-tight text-white">{{BUSINESS_NAME}}</span>
        </div>
        <p class="text-slate-300 text-sm leading-relaxed mb-8">
          Trusted real estate advisory, RERA-registered residential & commercial property consultancy, and turnkey asset management company.
        </p>
        <div class="flex flex-wrap gap-4">
          <button onclick="openModal('loginModal')" class="bg-white/10 hover:bg-white/20 text-white text-xs font-extrabold px-6 py-3 rounded-xl transition">Buyer Login</button>
          <button onclick="openModal('visitModal')" class="bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 text-white text-xs font-black px-6 py-3 rounded-xl transition">Book Site Visit</button>
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
          <span class="text-[11px] text-slate-400 mt-1 block">Mon-Sun (9 AM - 8 PM)</span>
        </div>

        <div class="interactive-card bg-gradient-to-b from-amber-500/10 to-[#0b0b1e] p-6 rounded-2xl border border-amber-500/40">
          <div class="w-10 h-10 rounded-xl bg-amber-400 text-slate-950 flex items-center justify-center text-lg mb-4">
            <i class="fa-solid fa-envelope"></i>
          </div>
          <h4 class="text-xs font-extrabold uppercase tracking-wider text-amber-400 mb-2">Official Email</h4>
          <a href="mailto:{{EMAIL}}" class="text-sm font-black text-white hover:text-amber-300 break-all block">{{EMAIL}}</a>
          <span class="text-[11px] text-slate-400 mt-1 block">24/7 Property Desk</span>
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

  <!-- SITE VISIT MODAL -->
  <div id="visitModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden items-center justify-center p-4">
    <div class="bg-[#0d0d24] border-2 border-amber-400/50 text-white w-full max-w-md p-8 rounded-3xl shadow-2xl relative">
      <button onclick="closeModal('visitModal')" class="absolute top-5 right-5 text-slate-400 hover:text-white text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-black mb-1 rainbow-text">Schedule VIP Site Visit</h3>
      <p class="text-xs text-slate-300 mb-6">Get free pickup & drop with a senior property advisor from {{BUSINESS_NAME}}</p>

      <form onsubmit="event.preventDefault(); alert('Your Site Visit is confirmed! Our advisor from {{BUSINESS_NAME}} will call you shortly.'); closeModal('visitModal');" class="space-y-4 text-sm">
        <input type="text" required placeholder="Your Full Name" class="w-full bg-black/50 border border-purple-500/40 rounded-xl px-4 py-3 text-white">
        <input type="tel" required placeholder="Mobile Number (+91)" class="w-full bg-black/50 border border-purple-500/40 rounded-xl px-4 py-3 text-white">
        <select class="w-full bg-black/50 border border-purple-500/40 rounded-xl px-4 py-3 text-white">
          <option>Luxury 3/4/5 BHK Apartment</option>
          <option>Independent Villa / Bungalow</option>
          <option>Commercial Office / Retail Shop</option>
          <option>Residential / Industrial Plot</option>
        </select>
        <button type="submit" class="w-full bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 text-white font-black py-3.5 rounded-xl shadow-lg">Confirm Site Visit</button>
      </form>
    </div>
  </div>

  <!-- LOGIN MODAL -->
  <div id="loginModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden items-center justify-center p-4">
    <div class="bg-[#0d0d24] border-2 border-pink-500/50 text-white w-full max-w-md p-8 rounded-3xl shadow-2xl relative">
      <button onclick="closeModal('loginModal')" class="absolute top-5 right-5 text-slate-400 hover:text-white text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-black mb-1 rainbow-text">Buyer & Investor Login</h3>
      <p class="text-xs text-slate-400 mb-6">Access saved properties & allotment documents at {{BUSINESS_NAME}}</p>

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
      <h3 class="text-2xl font-black mb-1 rainbow-text">Register / List Property</h3>
      <p class="text-xs text-slate-400 mb-6">Create an account with {{BUSINESS_NAME}}</p>

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
        <input type="text" required placeholder="Full Name" class="w-full bg-black/50 border border-cyan-500/40 rounded-xl px-4 py-3 text-white">
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

    // 1. Typewriter Effect (Real Estate Focus)
    const phrases = [
      "Luxury Penthouses & Signature Villas",
      "RERA-Approved Residential Townships",
      "High-ROI Commercial Offices & Retail",
      "Clear-Title Plots & Investment Land"
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

    document.querySelectorAll("a, button, select, .interactive-card").forEach((el) => {
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

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${p.hue}, 100%, 60%, ${p.alpha})`;
        ctx.fill();

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
        "🏡 *120FPS Colorful Real Estate & Property Website Bot*\n\n"
        "Ye bot *NexusProperty Style Real Estate Content + 120FPS Rainbow Cursor & 3D Colorful Theme* wali website generate karega.\n\n"
        "👇 *Is format me details bhejo:*\n"
        "`Name: Nexus Property Solutions`\n"
        "`Phone: +91 9876543210`\n"
        "`Email: info@heoo.in`\n"
        "`Address: Plot 18, 2nd Floor, Civil Lines, Rewa, Madhya Pradesh 474922`"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def generate_site(message):
    data = parse_details(message.text)
    if not all(k in data for k in ["name", "phone", "email", "address"]):
        bot.reply_to(
            message,
            "⚠️ *Saari 4 details sahi format me bhejo:*\n\n"
            "`Name: Real Estate Company Name`\n"
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
            f"🏡 *120FPS Colorful Real Estate Website Ready!*\n\n"
            f"🏢 *Name:* {data['name']}\n"
            f"📞 *Phone:* {data['phone']}\n"
            f"📧 *Email:* {data['email']}\n"
            f"📍 *Address:* {data['address']}\n\n"
            f"✨ *Includes:* Property Search Bar, 6 Featured Luxury Properties, 3 RERA New Launches, 120FPS Rainbow Cursor Trail & Verified Legal Entity Box."
        ),
        parse_mode="Markdown"
    )


app = Flask(__name__)

@app.route('/')
def health():
    return "120FPS Real Estate Bot Live 24/7"

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
