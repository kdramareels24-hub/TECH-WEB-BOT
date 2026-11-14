import os
import re
import io
import random
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
  <title>{{BUSINESS_NAME}} | Digital Transformation, Cloud & Enterprise Solutions</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --mouse-x: 50%;
      --mouse-y: 50%;
    }
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #030712;
      color: #f8fafc;
      overflow-x: hidden;
    }
    h1, h2, h3, .font-display {
      font-family: 'Space Grotesk', sans-serif;
    }

    /* Interactive Cursor Canvas Overlay */
    #cursor-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 9998;
    }

    /* Custom Magnetic Cursor Ring & Dot */
    .cursor-dot {
      position: fixed;
      top: 0;
      left: 0;
      width: 8px;
      height: 8px;
      background: #06b6d4;
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      transform: translate(-50%, -50%);
      box-shadow: 0 0 15px #06b6d4, 0 0 30px #3b82f6;
      transition: width 0.2s, height 0.2s, background-color 0.2s;
    }
    .cursor-ring {
      position: fixed;
      top: 0;
      left: 0;
      width: 42px;
      height: 42px;
      border: 1.5px solid rgba(6, 182, 212, 0.65);
      background: radial-gradient(circle, rgba(6,182,212,0.12) 0%, transparent 70%);
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      transform: translate(-50%, -50%);
      transition: width 0.25s ease-out, height 0.25s ease-out, border-color 0.25s, background-color 0.25s;
    }
    .cursor-ring.cursor-hover {
      width: 72px;
      height: 72px;
      border-color: #a855f7;
      background: radial-gradient(circle, rgba(168,85,247,0.22) 0%, transparent 70%);
    }

    /* Global Mouse Spotlight Effect */
    .spotlight-bg {
      background: radial-gradient(700px circle at var(--mouse-x) var(--mouse-y), rgba(6, 182, 212, 0.12), transparent 40%);
    }

    /* 3D Interactive Tilt & Glow Cards */
    .interactive-card {
      position: relative;
      transition: transform 0.2s ease-out, box-shadow 0.3s ease, border-color 0.3s ease;
      transform-style: preserve-3d;
      overflow: hidden;
    }
    .interactive-card::before {
      content: "";
      position: absolute;
      inset: 0;
      background: radial-gradient(450px circle at var(--card-x, 50%) var(--card-y, 50%), rgba(6, 182, 212, 0.18), transparent 45%);
      opacity: 0;
      transition: opacity 0.3s;
      pointer-events: none;
      z-index: 1;
    }
    .interactive-card:hover::before {
      opacity: 1;
    }
    .interactive-card:hover {
      border-color: rgba(6, 182, 212, 0.6) !important;
      box-shadow: 0 20px 50px -15px rgba(6, 182, 212, 0.28);
    }

    /* Infinite Marquee Animation */
    @keyframes marquee {
      0% { transform: translateX(0%); }
      100% { transform: translateX(-50%); }
    }
    .animate-marquee {
      display: flex;
      width: max-content;
      animation: marquee 28s linear infinite;
    }
    .animate-marquee:hover {
      animation-play-state: paused;
    }

    /* Floating & Pulse Animations */
    @keyframes floatSlow {
      0%, 100% { transform: translateY(0px) rotate(0deg); }
      50% { transform: translateY(-14px) rotate(1.5deg); }
    }
    .animate-float {
      animation: floatSlow 6s ease-in-out infinite;
    }
    @keyframes slowZoom {
      0% { transform: scale(1); }
      50% { transform: scale(1.12); }
      100% { transform: scale(1); }
    }
    .animate-zoom {
      animation: slowZoom 22s ease-in-out infinite;
    }

    /* Scroll Reveal Utility */
    .reveal {
      opacity: 0;
      transform: translateY(36px);
      transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .reveal.active {
      opacity: 1;
      transform: translateY(0);
    }

    .modal-active { display: flex !important; }
    .typing-cursor::after { content: '|'; animation: blink 1s infinite; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
  </style>
</head>
<body class="selection:bg-cyan-500 selection:text-slate-950 spotlight-bg">

  <!-- LIVE INTERACTIVE CURSOR CANVAS & RINGS -->
  <canvas id="cursor-canvas"></canvas>
  <div id="cursor-dot" class="cursor-dot hidden md:block"></div>
  <div id="cursor-ring" class="cursor-ring hidden md:block"></div>

  <!-- 1. TOP ANNOUNCEMENT & DIRECT CONTACT BAR -->
  <div class="bg-slate-950/90 border-b border-slate-800/80 text-xs py-2.5 px-6 relative z-40">
    <div class="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-3">
      <div class="flex flex-wrap items-center gap-6 text-slate-300">
        <a href="tel:{{PHONE}}" class="hover:text-cyan-400 transition flex items-center font-semibold">
          <i class="fa-solid fa-phone-volume text-cyan-400 mr-2 animate-pulse"></i> {{PHONE}}
        </a>
        <a href="mailto:{{EMAIL}}" class="hover:text-cyan-400 transition flex items-center font-semibold">
          <i class="fa-solid fa-envelope text-cyan-400 mr-2"></i> {{EMAIL}}
        </a>
        <span class="hidden lg:flex items-center text-slate-400">
          <i class="fa-solid fa-location-dot text-cyan-400 mr-2"></i> {{ADDRESS}}
        </span>
      </div>
      <div class="flex items-center space-x-4">
        <span class="inline-flex items-center text-emerald-400 font-bold">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-2"></span> ISO 27001 & Digital Verified Entity
        </span>
        <span class="text-slate-700">|</span>
        <button onclick="openModal('loginModal')" class="text-slate-200 hover:text-cyan-400 font-bold transition">Client Login</button>
        <button onclick="openModal('signupModal')" class="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-extrabold px-3.5 py-1 rounded-full transition shadow-lg shadow-cyan-500/20">Sign Up</button>
      </div>
    </div>
  </div>

  <!-- 2. STICKY GLASSMORPHISM NAVBAR -->
  <header class="sticky top-0 z-40 bg-slate-950/80 backdrop-blur-xl border-b border-slate-800/80">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <a href="#" class="flex items-center space-x-3.5 group">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-cyan-500 via-blue-600 to-purple-600 flex items-center justify-center text-white text-2xl shadow-lg shadow-cyan-500/30 group-hover:rotate-6 transition">
          <i class="fa-solid fa-bolt-lightning"></i>
        </div>
        <div>
          <span class="text-xl md:text-2xl font-extrabold tracking-tight text-white block leading-none">{{BUSINESS_NAME}}</span>
          <span class="text-[10px] font-bold uppercase tracking-widest text-cyan-400">Digital Services & Enterprise Tech</span>
        </div>
      </a>

      <nav class="hidden xl:flex items-center space-x-7 text-sm font-bold text-slate-300">
        <a href="#about" class="hover:text-cyan-400 transition">About Us</a>
        <a href="#services" class="hover:text-cyan-400 transition">Digital Services</a>
        <a href="#ongoing" class="hover:text-cyan-400 transition">Live Projects</a>
        <a href="#portfolio" class="hover:text-cyan-400 transition">Case Studies</a>
        <a href="#process" class="hover:text-cyan-400 transition">Workflow</a>
        <a href="#team" class="hover:text-cyan-400 transition">Engineers</a>
        <a href="#verification" class="hover:text-cyan-400 transition">Legal Registry</a>
        <a href="#contact" class="hover:text-cyan-400 transition">Contact</a>
      </nav>

      <div class="flex items-center space-x-3">
        <button onclick="openModal('loginModal')" class="hidden sm:inline-flex items-center px-4 py-2.5 border border-slate-700 hover:border-cyan-400 text-slate-200 hover:text-white rounded-xl text-xs font-extrabold uppercase tracking-wider transition">
          <i class="fa-regular fa-user mr-2 text-cyan-400"></i> Log In
        </button>
        <a href="#contact" class="inline-flex items-center px-5 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 rounded-xl text-xs font-black uppercase tracking-wider shadow-lg shadow-cyan-500/25 transition">
          Get Free Quote <i class="fa-solid fa-arrow-right ml-2"></i>
        </a>
      </div>
    </div>
  </header>

  <!-- 3. HERO SECTION WITH LIVE VIDEO + INTERACTIVE 3D CARDS -->
  <section class="relative min-h-[94vh] flex items-center justify-center overflow-hidden px-6 py-20">
    <!-- Background Live Video + Fallback High-Res Tech Grid -->
    <div class="absolute inset-0 z-0">
      <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=85" alt="Digital Network" class="w-full h-full object-cover animate-zoom opacity-35">
      <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-45">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-connections-41662-large.mp4" type="video/mp4">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-futuristic-hud-scifi-interface-41761-large.mp4" type="video/mp4">
      </video>
    </div>

    <!-- Glowing Radial Orbs -->
    <div class="absolute top-1/4 -left-20 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute bottom-1/4 -right-20 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute inset-0 bg-gradient-to-b from-slate-950/85 via-slate-950/70 to-[#030712] z-10"></div>

    <div class="relative z-20 max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7">
        <div class="inline-flex items-center gap-2.5 bg-slate-900/90 border border-cyan-500/40 px-4 py-2 rounded-full text-xs font-extrabold uppercase tracking-widest text-cyan-400 mb-6 shadow-xl">
          <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping"></span>
          <span>Next-Gen Digital Transformation & IT Solutions</span>
        </div>

        <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-none mb-6 uppercase text-transparent bg-clip-text bg-gradient-to-r from-white via-cyan-100 to-blue-400">
          {{BUSINESS_NAME}}
        </h1>

        <div class="text-xl sm:text-2xl md:text-3xl font-bold text-slate-300 mb-6 min-h-[42px]">
          <span class="text-cyan-400">Powering: </span>
          <span id="typewriter" class="text-white typing-cursor font-extrabold"></span>
        </div>

        <p class="text-base md:text-lg text-slate-300 max-w-2xl mb-10 leading-relaxed">
          We engineer high-converting digital ecosystems, custom cloud software, AI business automation, full-stack web & mobile applications, and performance digital marketing from our headquarters at <strong>{{ADDRESS}}</strong>.
        </p>

        <div class="flex flex-wrap gap-4 mb-10">
          <a href="#services" class="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-black px-8 py-4 rounded-2xl shadow-xl shadow-cyan-500/25 transition transform hover:-translate-y-1 flex items-center">
            <i class="fa-solid fa-rocket mr-2.5"></i> Explore Digital Services
          </a>
          <a href="#contact" class="bg-slate-900/90 hover:bg-slate-800 border border-slate-700 hover:border-cyan-400 text-white font-bold px-8 py-4 rounded-2xl transition flex items-center">
            <i class="fa-solid fa-phone-volume mr-2.5 text-cyan-400"></i> {{PHONE}}
          </a>
        </div>

        <div class="grid grid-cols-3 gap-4 pt-6 border-t border-slate-800/80 max-w-lg">
          <div>
            <div class="text-2xl sm:text-3xl font-black text-white">320+</div>
            <div class="text-xs text-slate-400 font-semibold">Projects Delivered</div>
          </div>
          <div>
            <div class="text-2xl sm:text-3xl font-black text-cyan-400">99.9%</div>
            <div class="text-xs text-slate-400 font-semibold">Client Satisfaction</div>
          </div>
          <div>
            <div class="text-2xl sm:text-3xl font-black text-purple-400">24/7</div>
            <div class="text-xs text-slate-400 font-semibold">Live Support Desk</div>
          </div>
        </div>
      </div>

      <!-- Hero Right Interactive Floating Dashboard Showcase -->
      <div class="lg:col-span-5 relative">
        <div class="interactive-card bg-slate-900/90 backdrop-blur-xl border border-slate-700/80 rounded-3xl p-6 shadow-2xl animate-float">
          <div class="relative h-72 rounded-2xl overflow-hidden mb-6 border border-slate-800">
            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85" alt="Digital Analytics" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/30 to-transparent flex flex-col justify-end p-5">
              <span class="bg-cyan-500 text-slate-950 text-[10px] font-black uppercase px-3 py-1 rounded-full w-max mb-2">Live Telemetry Active</span>
              <h3 class="text-xl font-black text-white">Real-Time Cloud & Digital Command</h3>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-5">
            <div class="bg-slate-950/90 p-4 rounded-2xl border border-slate-800">
              <div class="text-xs text-slate-400 mb-1">Server Uptime SLA</div>
              <div class="text-2xl font-black text-emerald-400">99.998%</div>
            </div>
            <div class="bg-slate-950/90 p-4 rounded-2xl border border-slate-800">
              <div class="text-xs text-slate-400 mb-1">Active Deployments</div>
              <div class="text-2xl font-black text-cyan-400">140+ Live</div>
            </div>
          </div>

          <div class="flex items-center justify-between text-xs text-slate-300 bg-slate-950/70 px-4 py-3 rounded-xl border border-slate-800">
            <span><i class="fa-solid fa-shield-check text-emerald-400 mr-2"></i>Verified Enterprise Portal</span>
            <a href="#verification" class="text-cyan-400 font-bold hover:underline">View Credentials →</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 4. INFINITE TECH & DIGITAL SOLUTIONS MARQUEE TICKER -->
  <div class="bg-slate-900/90 border-y border-slate-800 py-4 overflow-hidden">
    <div class="animate-marquee space-x-12 text-sm font-extrabold uppercase tracking-widest text-slate-300">
      <span><i class="fa-solid fa-code text-cyan-400 mr-2"></i>Custom Web & App Development</span>
      <span><i class="fa-solid fa-cloud text-blue-400 mr-2"></i>Cloud Architecture & DevOps</span>
      <span><i class="fa-solid fa-robot text-purple-400 mr-2"></i>AI Chatbots & Workflow Automation</span>
      <span><i class="fa-solid fa-chart-line text-emerald-400 mr-2"></i>Performance Digital Marketing & SEO</span>
      <span><i class="fa-solid fa-shield-halved text-amber-400 mr-2"></i>Enterprise Cybersecurity & Audits</span>
      <span><i class="fa-solid fa-database text-pink-400 mr-2"></i>Custom ERP, CRM & SaaS Portals</span>
      <span><i class="fa-solid fa-code text-cyan-400 mr-2"></i>Custom Web & App Development</span>
      <span><i class="fa-solid fa-cloud text-blue-400 mr-2"></i>Cloud Architecture & DevOps</span>
      <span><i class="fa-solid fa-robot text-purple-400 mr-2"></i>AI Chatbots & Workflow Automation</span>
      <span><i class="fa-solid fa-chart-line text-emerald-400 mr-2"></i>Performance Digital Marketing & SEO</span>
    </div>
  </div>

  <!-- 5. INTERACTIVE STATS MATRIX -->
  <section class="py-20 px-6 max-w-7xl mx-auto reveal">
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="interactive-card bg-slate-900/70 border border-slate-800 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 text-2xl">
          <i class="fa-solid fa-laptop-code"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-2">350+</div>
        <div class="text-xs font-bold uppercase tracking-widest text-cyan-400">Digital Platforms Built</div>
      </div>

      <div class="interactive-card bg-slate-900/70 border border-slate-800 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-400 text-2xl">
          <i class="fa-solid fa-users-gear"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-2">120+</div>
        <div class="text-xs font-bold uppercase tracking-widest text-blue-400">Certified IT Specialists</div>
      </div>

      <div class="interactive-card bg-slate-900/70 border border-slate-800 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 text-2xl">
          <i class="fa-solid fa-globe"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-2">99.9%</div>
        <div class="text-xs font-bold uppercase tracking-widest text-purple-400">Cloud Uptime Guarantee</div>
      </div>

      <div class="interactive-card bg-slate-900/70 border border-slate-800 p-8 rounded-3xl text-center">
        <div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-2xl">
          <i class="fa-solid fa-award"></i>
        </div>
        <div class="text-4xl md:text-5xl font-black text-white mb-2">100%</div>
        <div class="text-xs font-bold uppercase tracking-widest text-emerald-400">On-Time SLA Delivery</div>
      </div>
    </div>
  </section>

  <!-- 6. ABOUT THE COMPANY (EXTRA LARGE VISUALS + 3D TILT) -->
  <section id="about" class="py-24 px-6 max-w-7xl mx-auto reveal">
    <div class="grid lg:grid-cols-12 gap-14 items-center">
      <div class="lg:col-span-6 grid sm:grid-cols-2 gap-6">
        <div class="interactive-card h-[440px] rounded-3xl overflow-hidden border border-slate-800 shadow-2xl">
          <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85" alt="Digital Team" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent flex flex-col justify-end p-6">
            <span class="bg-cyan-500 text-slate-950 text-xs font-black px-3 py-1 rounded w-max mb-2">Agile Squads</span>
            <h4 class="text-xl font-bold text-white">Full-Stack Developers & Designers</h4>
          </div>
        </div>
        <div class="interactive-card h-[440px] rounded-3xl overflow-hidden border border-slate-800 shadow-2xl sm:mt-10">
          <img src="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=900&q=85" alt="Server Infrastructure" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent flex flex-col justify-end p-6">
            <span class="bg-purple-500 text-white text-xs font-black px-3 py-1 rounded w-max mb-2">Cloud Core</span>
            <h4 class="text-xl font-bold text-white">24/7 Server & Security Operations</h4>
          </div>
        </div>
      </div>

      <div class="lg:col-span-6">
        <span class="text-cyan-400 font-extrabold uppercase tracking-widest text-xs bg-cyan-500/10 border border-cyan-500/30 px-4 py-2 rounded-full">
          About {{BUSINESS_NAME}}
        </span>
        <h2 class="text-3xl sm:text-5xl font-black text-white mt-5 mb-6 leading-tight">
          Accelerating Businesses Through Smart Digital Engineering
        </h2>
        <p class="text-slate-300 text-base leading-relaxed mb-6">
          <strong>{{BUSINESS_NAME}}</strong> is a premier digital transformation, software engineering, and enterprise IT services company located at <strong>{{ADDRESS}}</strong>. We partner with startups, SMEs, and large enterprises to build scalable digital products and automated cloud workflows.
        </p>
        <p class="text-slate-400 text-sm leading-relaxed mb-8">
          From custom ERP/CRM architecture and high-speed web applications to performance marketing and WhatsApp/API business automation, every solution is engineered for security, speed, and measurable ROI.
        </p>

        <div class="grid sm:grid-cols-2 gap-4 mb-8">
          <div class="interactive-card bg-slate-900/80 p-5 rounded-2xl border border-slate-800">
            <i class="fa-solid fa-bolt text-cyan-400 text-xl mb-2"></i>
            <h4 class="font-bold text-white text-sm">High-Velocity Execution</h4>
            <p class="text-xs text-slate-400 mt-1">Agile sprint cycles with live staging links and transparent milestone tracking.</p>
          </div>
          <div class="interactive-card bg-slate-900/80 p-5 rounded-2xl border border-slate-800">
            <i class="fa-solid fa-lock text-purple-400 text-xl mb-2"></i>
            <h4 class="font-bold text-white text-sm">Enterprise-Grade Security</h4>
            <p class="text-xs text-slate-400 mt-1">End-to-end SSL encryption, cloud firewall protection, and ISO-compliant audits.</p>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-6 pt-4 border-t border-slate-800">
          <div>
            <span class="text-xs text-slate-400 uppercase font-bold block">Direct Desk</span>
            <a href="tel:{{PHONE}}" class="text-lg font-extrabold text-cyan-400 hover:underline">{{PHONE}}</a>
          </div>
          <div class="h-8 w-px bg-slate-800 hidden sm:block"></div>
          <div>
            <span class="text-xs text-slate-400 uppercase font-bold block">Official Email</span>
            <a href="mailto:{{EMAIL}}" class="text-lg font-extrabold text-white hover:text-cyan-400">{{EMAIL}}</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 7. 8 CORE DIGITAL & TECH SERVICES (INTERACTIVE SPOTLIGHT CARDS) -->
  <section id="services" class="py-28 bg-slate-900/40 border-y border-slate-800/80 px-6 reveal">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-20">
        <span class="text-cyan-400 font-extrabold uppercase tracking-widest text-xs bg-cyan-500/10 border border-cyan-500/30 px-4 py-2 rounded-full">
          Our Digital Capabilities
        </span>
        <h2 class="text-4xl md:text-6xl font-black text-white mt-4">360° Digital & IT Services</h2>
        <p class="text-slate-400 text-base mt-3 max-w-2xl mx-auto">
          Move your cursor over any service card below to experience our interactive architecture.
        </p>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
        <div class="interactive-card bg-slate-900/90 border border-slate-800 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center text-2xl mb-6">
            <i class="fa-solid fa-code"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Custom Web & Portal Dev</h3>
          <p class="text-slate-400 text-xs leading-relaxed">Ultra-fast React, Next.js, Node.js, and Python web applications engineered for enterprise scale and SEO dominance.</p>
        </div>

        <div class="interactive-card bg-slate-900/90 border border-slate-800 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/30 text-blue-400 flex items-center justify-center text-2xl mb-6">
            <i class="fa-solid fa-mobile-screen-button"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">iOS & Android Mobile Apps</h3>
          <p class="text-slate-400 text-xs leading-relaxed">Native and cross-platform Flutter & React Native mobile applications with seamless payment and real-time sync.</p>
        </div>

        <div class="interactive-card bg-slate-900/90 border border-slate-800 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-purple-500/10 border border-purple-500/30 text-purple-400 flex items-center justify-center text-2xl mb-6">
            <i class="fa-solid fa-robot"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">AI & Business Automation</h3>
          <p class="text-slate-400 text-xs leading-relaxed">Custom AI chatbots, CRM workflows, WhatsApp API integrations, and automated billing systems that run 24/7.</p>
        </div>

        <div class="interactive-card bg-slate-900/90 border border-slate-800 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-2xl mb-6">
            <i class="fa-solid fa-bullhorn"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Performance Digital Marketing</h3>
          <p class="text-slate-400 text-xs leading-relaxed">ROI-focused Google Ads, Meta Ad campaigns, technical SEO, and conversion rate optimization for rapid growth.</p>
        </div>

        <div class="interactive-card bg-slate-900/90 border border-slate-800 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center text-2xl mb-6">
            <i class="fa-solid fa-cloud-arrow-up"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Cloud & DevOps Infra</h3>
          <p class="text-slate-400 text-xs leading-relaxed">AWS, Google Cloud, and Azure server deployment, Kubernetes auto-scaling, Docker CI/CD, and 24/7 monitoring.</p>
        </div>

        <div class="interactive-card bg-slate-900/90 border border-slate-800 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-pink-500/10 border border-pink-500/30 text-pink-400 flex items-center justify-center text-2xl mb-6">
            <i class="fa-solid fa-network-wired"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Enterprise ERP & CRM</h3>
          <p class="text-slate-400 text-xs leading-relaxed">Centralized inventory, invoicing, HR payroll, and supply-chain management software tailored to your workflow.</p>
        </div>

        <div class="interactive-card bg-slate-900/90 border border-slate-800 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 flex items-center justify-center text-2xl mb-6">
            <i class="fa-solid fa-pen-ruler"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">UI/UX & Brand Identity</h3>
          <p class="text-slate-400 text-xs leading-relaxed">Interactive Figma prototypes, design systems, 3D motion graphics, and high-converting user journeys.</p>
        </div>

        <div class="interactive-card bg-slate-900/90 border border-slate-800 p-8 rounded-3xl">
          <div class="w-14 h-14 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-400 flex items-center justify-center text-2xl mb-6">
            <i class="fa-solid fa-shield-virus"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Cybersecurity & Audits</h3>
          <p class="text-slate-400 text-xs leading-relaxed">Vulnerability penetration testing, DDoS protection, SSL security hardening, and compliance auditing.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 8. ONGOING LIVE PROJECTS (IN-DEVELOPMENT / STAGING - GIANT CARDS) -->
  <section id="ongoing" class="py-28 px-6 max-w-7xl mx-auto reveal">
    <div class="flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
      <div>
        <span class="text-amber-400 font-extrabold uppercase tracking-widest text-xs bg-amber-500/10 border border-amber-500/30 px-4 py-2 rounded-full">
          Live Staging & R&D Pipeline
        </span>
        <h2 class="text-4xl md:text-5xl font-black text-white mt-4">Ongoing Digital Deployments</h2>
        <p class="text-slate-400 text-sm mt-2 max-w-2xl">Real-time progress of enterprise cloud platforms, mobile apps, and AI systems currently in active sprint execution.</p>
      </div>
      <a href="#contact" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-black text-xs uppercase tracking-wider px-6 py-3.5 rounded-xl transition">
        Start Your Project <i class="fa-solid fa-arrow-right ml-2"></i>
      </a>
    </div>

    <div class="grid lg:grid-cols-3 gap-8">
      <div class="interactive-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden">
        <div class="relative h-[380px] overflow-hidden">
          <img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=900&q=85" alt="FinTech Cloud" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent"></div>
          <span class="absolute top-4 left-4 bg-amber-400 text-slate-950 text-xs font-black uppercase px-3.5 py-1.5 rounded-full">
            <i class="fa-solid fa-spinner fa-spin mr-1"></i> Active Sprint
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <h3 class="text-2xl font-black text-white">OmniPay FinTech Core API</h3>
            <p class="text-xs text-slate-300 mt-1">Microservices payment switch & automated reconciliation dashboard.</p>
          </div>
        </div>
        <div class="p-6">
          <div class="flex justify-between text-xs font-bold mb-2">
            <span class="text-slate-300">UAT & Load Testing Stage</span>
            <span class="text-cyan-400">82% Completed</span>
          </div>
          <div class="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
            <div class="bg-gradient-to-r from-cyan-500 to-blue-500 h-full rounded-full" style="width: 82%"></div>
          </div>
        </div>
      </div>

      <div class="interactive-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden">
        <div class="relative h-[380px] overflow-hidden">
          <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=85" alt="AI ERP" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent"></div>
          <span class="absolute top-4 left-4 bg-amber-400 text-slate-950 text-xs font-black uppercase px-3.5 py-1.5 rounded-full">
            <i class="fa-solid fa-spinner fa-spin mr-1"></i> Cloud Migration
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <h3 class="text-2xl font-black text-white">Nexus Supply-Chain AI ERP</h3>
            <p class="text-xs text-slate-300 mt-1">Multi-warehouse inventory tracking & predictive demand forecasting.</p>
          </div>
        </div>
        <div class="p-6">
          <div class="flex justify-between text-xs font-bold mb-2">
            <span class="text-slate-300">Database Sync & API Rollout</span>
            <span class="text-cyan-400">74% Completed</span>
          </div>
          <div class="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
            <div class="bg-gradient-to-r from-cyan-500 to-purple-500 h-full rounded-full" style="width: 74%"></div>
          </div>
        </div>
      </div>

      <div class="interactive-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden">
        <div class="relative h-[380px] overflow-hidden">
          <img src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=900&q=85" alt="Cyber Matrix" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent"></div>
          <span class="absolute top-4 left-4 bg-amber-400 text-slate-950 text-xs font-black uppercase px-3.5 py-1.5 rounded-full">
            <i class="fa-solid fa-spinner fa-spin mr-1"></i> Beta Deployment
          </span>
          <div class="absolute bottom-4 left-5 right-5">
            <h3 class="text-2xl font-black text-white">Cortex Enterprise CRM Suite</h3>
            <p class="text-xs text-slate-300 mt-1">Omnichannel customer support, voice bot & automated lead routing.</p>
          </div>
        </div>
        <div class="p-6">
          <div class="flex justify-between text-xs font-bold mb-2">
            <span class="text-slate-300">Production Cluster Setup</span>
            <span class="text-cyan-400">89% Completed</span>
          </div>
          <div class="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
            <div class="bg-gradient-to-r from-emerald-400 to-cyan-500 h-full rounded-full" style="width: 89%"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 9. COMPLETED PLATFORMS & CASE STUDIES (GIANT HD PORTFOLIO) -->
  <section id="portfolio" class="py-28 bg-slate-900/40 border-y border-slate-800/80 px-6 reveal">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="text-emerald-400 font-extrabold uppercase tracking-widest text-xs bg-emerald-500/10 border border-emerald-500/30 px-4 py-2 rounded-full">
          Delivered Success Stories
        </span>
        <h2 class="text-4xl md:text-6xl font-black text-white mt-4">Completed & Live Digital Platforms</h2>
        <p class="text-slate-400 text-base mt-3 max-w-2xl mx-auto">Enterprise software systems, e-commerce engines, and cloud portals running live in production.</p>
      </div>

      <div class="grid lg:grid-cols-3 gap-8">
        <div class="interactive-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden group">
          <div class="relative h-[420px] overflow-hidden">
            <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=900&q=85" alt="Enterprise Portal" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/30 to-transparent"></div>
            <span class="absolute top-4 left-4 bg-emerald-500 text-slate-950 text-xs font-black uppercase px-3.5 py-1.5 rounded-full">
              <i class="fa-solid fa-check-circle mr-1"></i> 100% Live In Production
            </span>
            <div class="absolute bottom-5 left-5 right-5">
              <span class="text-cyan-400 text-xs font-bold uppercase">Enterprise SaaS</span>
              <h3 class="text-2xl font-black text-white mt-1">PrimeCommerce B2B Trade Cloud</h3>
              <p class="text-xs text-slate-300 mt-1">Handling 250,000+ daily orders with real-time GST billing & logistics sync.</p>
            </div>
          </div>
        </div>

        <div class="interactive-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden group">
          <div class="relative h-[420px] overflow-hidden">
            <img src="https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=900&q=85" alt="Data Analytics" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/30 to-transparent"></div>
            <span class="absolute top-4 left-4 bg-emerald-500 text-slate-950 text-xs font-black uppercase px-3.5 py-1.5 rounded-full">
              <i class="fa-solid fa-check-circle mr-1"></i> 100% Live In Production
            </span>
            <div class="absolute bottom-5 left-5 right-5">
              <span class="text-cyan-400 text-xs font-bold uppercase">Healthcare Cloud</span>
              <h3 class="text-2xl font-black text-white mt-1">MedCore Hospital Management ERP</h3>
              <p class="text-xs text-slate-300 mt-1">Deployed across 180+ clinics with automated lab reports & patient portal.</p>
            </div>
          </div>
        </div>

        <div class="interactive-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden group">
          <div class="relative h-[420px] overflow-hidden">
            <img src="https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=900&q=85" alt="Security Grid" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/30 to-transparent"></div>
            <span class="absolute top-4 left-4 bg-emerald-500 text-slate-950 text-xs font-black uppercase px-3.5 py-1.5 rounded-full">
              <i class="fa-solid fa-check-circle mr-1"></i> 100% Live In Production
            </span>
            <div class="absolute bottom-5 left-5 right-5">
              <span class="text-cyan-400 text-xs font-bold uppercase">FinTech & Security</span>
              <h3 class="text-2xl font-black text-white mt-1">VaultX Identity & eKYC Gateway</h3>
              <p class="text-xs text-slate-300 mt-1">Sub-second document OCR verification and biometric authentication engine.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 10. 6-STAGE DIGITAL EXECUTION ROADMAP -->
  <section id="process" class="py-28 px-6 max-w-7xl mx-auto reveal">
    <div class="text-center mb-16">
      <span class="text-cyan-400 font-extrabold uppercase tracking-widest text-xs bg-cyan-500/10 border border-cyan-500/30 px-4 py-2 rounded-full">
        How We Deliver
      </span>
      <h2 class="text-4xl md:text-5xl font-black text-white mt-4">6-Step Digital Engineering Workflow</h2>
    </div>

    <div class="grid sm:grid-cols-2 lg:grid-cols-6 gap-6">
      <div class="interactive-card bg-slate-900/90 p-6 rounded-2xl border border-slate-800">
        <div class="text-3xl font-black text-cyan-400 mb-3">01</div>
        <h4 class="font-bold text-white text-sm mb-2">Discovery & SRS</h4>
        <p class="text-xs text-slate-400">Requirement gathering, technical feasibility, and architecture blueprint.</p>
      </div>
      <div class="interactive-card bg-slate-900/90 p-6 rounded-2xl border border-slate-800">
        <div class="text-3xl font-black text-blue-400 mb-3">02</div>
        <h4 class="font-bold text-white text-sm mb-2">UI/UX Wireframing</h4>
        <p class="text-xs text-slate-400">Interactive Figma mockups and high-conversion user journey design.</p>
      </div>
      <div class="interactive-card bg-slate-900/90 p-6 rounded-2xl border border-slate-800">
        <div class="text-3xl font-black text-purple-400 mb-3">03</div>
        <h4 class="font-bold text-white text-sm mb-2">Agile Coding</h4>
        <p class="text-xs text-slate-400">Clean frontend, backend API, and database engineering in 2-week sprints.</p>
      </div>
      <div class="interactive-card bg-slate-900/90 p-6 rounded-2xl border border-slate-800">
        <div class="text-3xl font-black text-pink-400 mb-3">04</div>
        <h4 class="font-bold text-white text-sm mb-2">QA & Security</h4>
        <p class="text-xs text-slate-400">Automated load testing, bug squashing, and SSL/OWASP security audits.</p>
      </div>
      <div class="interactive-card bg-slate-900/90 p-6 rounded-2xl border border-slate-800">
        <div class="text-3xl font-black text-amber-400 mb-3">05</div>
        <h4 class="font-bold text-white text-sm mb-2">Cloud Deployment</h4>
        <p class="text-xs text-slate-400">Zero-downtime CI/CD rollout on AWS, Vercel, or dedicated cloud clusters.</p>
      </div>
      <div class="interactive-card bg-slate-900/90 p-6 rounded-2xl border border-slate-800">
        <div class="text-3xl font-black text-emerald-400 mb-3">06</div>
        <h4 class="font-bold text-white text-sm mb-2">24/7 SLA Support</h4>
        <p class="text-xs text-slate-400">Continuous server monitoring, backups, and feature scaling.</p>
      </div>
    </div>
  </section>

  <!-- 11. OUR ENGINEERS & DIGITAL WORKFORCE SHOWCASE -->
  <section id="team" class="py-28 bg-slate-900/40 border-y border-slate-800/80 px-6 reveal">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="text-cyan-400 font-extrabold uppercase tracking-widest text-xs bg-cyan-500/10 border border-cyan-500/30 px-4 py-2 rounded-full">
          Our Human Capital
        </span>
        <h2 class="text-4xl md:text-5xl font-black text-white mt-4">Engineers, Architects & Digital Specialists</h2>
        <p class="text-slate-400 text-sm mt-2 max-w-2xl mx-auto">Dedicated teams working from our operations center at <strong>{{BUSINESS_NAME}}</strong>.</p>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
        <div class="interactive-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=85" alt="Full Stack Team" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-cyan-400 text-xs font-bold uppercase">Core Engineering</span>
            <h4 class="text-xl font-bold text-white mt-1">Full-Stack Web & App Squad</h4>
            <p class="text-xs text-slate-400 mt-1">React, Next.js, Node.js, Python & Flutter specialists.</p>
          </div>
        </div>

        <div class="interactive-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=800&q=85" alt="Cloud DevOps" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-purple-400 text-xs font-bold uppercase">Cloud & AI Lab</span>
            <h4 class="text-xl font-bold text-white mt-1">DevOps & AI Architects</h4>
            <p class="text-xs text-slate-400 mt-1">AWS, Kubernetes, LLM Automation & Data Pipelines.</p>
          </div>
        </div>

        <div class="interactive-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=85" alt="Server Ops" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-emerald-400 text-xs font-bold uppercase">24/7 NOC Desk</span>
            <h4 class="text-xl font-bold text-white mt-1">Server & Security Engineers</h4>
            <p class="text-xs text-slate-400 mt-1">Real-time uptime monitoring, firewall & data protection.</p>
          </div>
        </div>

        <div class="interactive-card bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden">
          <img src="https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=85" alt="Digital Growth" class="w-full h-80 object-cover">
          <div class="p-6">
            <span class="text-amber-400 text-xs font-bold uppercase">Growth & UI/UX</span>
            <h4 class="text-xl font-bold text-white mt-1">Digital Marketing & Product Crew</h4>
            <p class="text-xs text-slate-400 mt-1">Performance ads, SEO, conversion UI/UX & client onboarding.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 12. VERIFIED LEGAL ENTITY DISCLOSURE TABLE (FOR META VERIFICATION CRAWLERS) -->
  <section id="verification" class="py-24 px-6 max-w-5xl mx-auto reveal">
    <div class="interactive-card bg-slate-900/95 border-2 border-cyan-500/50 rounded-3xl p-8 sm:p-12 shadow-2xl">
      <div class="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-slate-800">
        <div>
          <span class="text-xs font-extrabold uppercase tracking-widest text-cyan-400">Statutory Corporate Disclosure</span>
          <h3 class="text-2xl sm:text-3xl font-black text-white mt-1">Verified Legal Entity Information</h3>
        </div>
        <span class="bg-emerald-500/10 border border-emerald-500/40 text-emerald-400 text-xs font-extrabold px-4 py-2 rounded-full flex items-center">
          <i class="fa-solid fa-circle-check mr-2"></i> Active Registered Business
        </span>
      </div>

      <div class="grid md:grid-cols-2 gap-6 text-sm">
        <div class="p-5 bg-slate-950 rounded-2xl border border-slate-800">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Registered Company Name</span>
          <span class="text-lg font-black text-white">{{BUSINESS_NAME}}</span>
        </div>
        <div class="p-5 bg-slate-950 rounded-2xl border border-slate-800">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Business Category</span>
          <span class="text-lg font-black text-cyan-400">Digital Services, Software & IT Solutions</span>
        </div>
        <div class="p-5 bg-slate-950 rounded-2xl border border-slate-800">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Registered Telephone Number</span>
          <a href="tel:{{PHONE}}" class="text-lg font-black text-white hover:text-cyan-400">{{PHONE}}</a>
        </div>
        <div class="p-5 bg-slate-950 rounded-2xl border border-slate-800">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Official Corporate Email</span>
          <a href="mailto:{{EMAIL}}" class="text-lg font-black text-cyan-400 hover:underline break-all">{{EMAIL}}</a>
        </div>
        <div class="md:col-span-2 p-5 bg-slate-950 rounded-2xl border border-slate-800">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Registered Head Office Address</span>
          <span class="text-base sm:text-lg font-black text-white leading-relaxed">{{ADDRESS}}</span>
        </div>
      </div>
    </div>
  </section>

  <!-- 13. INTERACTIVE FAQ ACCORDION -->
  <section class="py-16 px-6 max-w-4xl mx-auto reveal">
    <div class="text-center mb-12">
      <h2 class="text-3xl font-black text-white">Frequently Asked Questions</h2>
    </div>
    <div class="space-y-4">
      <details class="interactive-card bg-slate-900 border border-slate-800 rounded-2xl p-6 cursor-pointer group">
        <summary class="font-bold text-white flex justify-between items-center">
          <span>What services does {{BUSINESS_NAME}} provide?</span>
          <i class="fa-solid fa-chevron-down text-cyan-400 group-open:rotate-180 transition"></i>
        </summary>
        <p class="text-xs text-slate-400 mt-3 leading-relaxed">We provide end-to-end web and mobile app development, custom ERP/CRM software, cloud server management, AI business automation, and performance digital marketing.</p>
      </details>
      <details class="interactive-card bg-slate-900 border border-slate-800 rounded-2xl p-6 cursor-pointer group">
        <summary class="font-bold text-white flex justify-between items-center">
          <span>How can we contact the official desk of {{BUSINESS_NAME}}?</span>
          <i class="fa-solid fa-chevron-down text-cyan-400 group-open:rotate-180 transition"></i>
        </summary>
        <p class="text-xs text-slate-400 mt-3 leading-relaxed">You can reach our registered office directly at {{ADDRESS}}, call us on {{PHONE}}, or email our support desk at {{EMAIL}}.</p>
      </details>
    </div>
  </section>

  <!-- 14. CONTACT & FOOTER WITH MANDATORY NAME, ADDRESS, PHONE & EMAIL -->
  <footer id="contact" class="bg-slate-950 text-white pt-24 pb-12 px-6 border-t-4 border-cyan-500 relative z-20">
    <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 pb-16 border-b border-slate-800">
      <div class="lg:col-span-5">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-11 h-11 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white text-xl font-black">
            <i class="fa-solid fa-bolt-lightning"></i>
          </div>
          <span class="text-2xl font-black tracking-tight text-white">{{BUSINESS_NAME}}</span>
        </div>
        <p class="text-slate-400 text-sm leading-relaxed mb-8">
          Full-stack digital services, custom enterprise software, cloud infrastructure, and performance automation solutions built for modern businesses.
        </p>
        <div class="flex flex-wrap gap-4">
          <button onclick="openModal('loginModal')" class="bg-slate-900 hover:bg-slate-800 border border-slate-700 text-white text-xs font-extrabold px-6 py-3 rounded-xl transition">Client Portal Login</button>
          <button onclick="openModal('signupModal')" class="bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 text-xs font-black px-6 py-3 rounded-xl transition">Partner Sign Up</button>
        </div>
      </div>

      <!-- Highlighted Address, Phone, Email Cards -->
      <div class="lg:col-span-7 grid sm:grid-cols-3 gap-6">
        <div class="interactive-card bg-slate-900 p-6 rounded-2xl border border-slate-800">
          <div class="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center text-lg mb-4">
            <i class="fa-solid fa-location-dot"></i>
          </div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Office Address</h4>
          <p class="text-sm font-bold text-white leading-relaxed">{{ADDRESS}}</p>
        </div>

        <div class="interactive-card bg-slate-900 p-6 rounded-2xl border border-slate-800">
          <div class="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center text-lg mb-4">
            <i class="fa-solid fa-phone-volume"></i>
          </div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Phone Number</h4>
          <a href="tel:{{PHONE}}" class="text-base font-extrabold text-cyan-400 hover:underline block">{{PHONE}}</a>
          <span class="text-[11px] text-slate-400 mt-1 block">Mon-Sat (9 AM - 8 PM)</span>
        </div>

        <div class="interactive-card bg-slate-900 p-6 rounded-2xl border border-slate-800">
          <div class="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center text-lg mb-4">
            <i class="fa-solid fa-envelope"></i>
          </div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Official Email</h4>
          <a href="mailto:{{EMAIL}}" class="text-sm font-extrabold text-cyan-400 hover:underline break-all block">{{EMAIL}}</a>
          <span class="text-[11px] text-slate-400 mt-1 block">24/7 Support Desk</span>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto pt-8 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-400 gap-4">
      <p>© 2026 <strong>{{BUSINESS_NAME}}</strong>. All Rights Reserved. | Address: {{ADDRESS}} | Phone: {{PHONE}} | Email: {{EMAIL}}</p>
      <div class="flex space-x-6">
        <a href="#verification" class="hover:text-cyan-400">Privacy Policy</a>
        <a href="#verification" class="hover:text-cyan-400">Terms & Conditions</a>
      </div>
    </div>
  </footer>

  <!-- LOGIN MODAL WITH CONTINUE WITH GOOGLE -->
  <div id="loginModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 text-white w-full max-w-md p-8 rounded-3xl shadow-2xl relative">
      <button onclick="closeModal('loginModal')" class="absolute top-5 right-5 text-slate-400 hover:text-white text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-black mb-1">Client Portal Login</h3>
      <p class="text-xs text-slate-400 mb-6">Sign in to manage projects & invoices at {{BUSINESS_NAME}}</p>

      <button onclick="alert('Redirecting to Google Workspace SSO...');" class="w-full bg-white hover:bg-gray-100 text-slate-900 font-bold py-3.5 px-4 rounded-xl flex items-center justify-center space-x-3 mb-5 shadow">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span class="text-sm">Continue with Google</span>
      </button>

      <form onsubmit="event.preventDefault(); alert('Authenticated successfully!');" class="space-y-4 text-sm">
        <input type="email" required placeholder="Corporate Email Address" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white">
        <input type="password" required placeholder="Password" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white">
        <button type="submit" class="w-full bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-black py-3.5 rounded-xl shadow-lg">Sign In</button>
      </form>
    </div>
  </div>

  <!-- SIGN UP MODAL WITH CONTINUE WITH GOOGLE -->
  <div id="signupModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 text-white w-full max-w-md p-8 rounded-3xl shadow-2xl relative">
      <button onclick="closeModal('signupModal')" class="absolute top-5 right-5 text-slate-400 hover:text-white text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-black mb-1">Create Client Account</h3>
      <p class="text-xs text-slate-400 mb-6">Onboard your business with {{BUSINESS_NAME}}</p>

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
        <input type="text" required placeholder="Full Name / Company Name" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white">
        <input type="tel" required placeholder="Mobile Number" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white">
        <input type="email" required placeholder="Email Address" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white">
        <input type="password" required placeholder="Create Password" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white">
        <button type="submit" class="w-full bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-black py-3.5 rounded-xl shadow-lg">Create Free Account</button>
      </form>
    </div>
  </div>

  <!-- INTERACTIVE CURSOR ENGINE, PARTICLE TRAIL & 3D TILT SCRIPT -->
  <script>
    function openModal(id) { document.getElementById(id).classList.add('modal-active'); }
    function closeModal(id) { document.getElementById(id).classList.remove('modal-active'); }

    // 1. Typewriter Effect
    const phrases = [
      "Custom Web, App & Cloud Ecosystems",
      "AI Chatbots & Business Workflow Automation",
      "Enterprise ERP, CRM & FinTech Portals",
      "ROI-Driven Performance Digital Marketing"
    ];
    let pIdx = 0, cIdx = 0, isDel = false;
    const tw = document.getElementById("typewriter");
    function runType() {
      const cur = phrases[pIdx];
      tw.innerText = isDel ? cur.substring(0, cIdx--) : cur.substring(0, cIdx++);
      let spd = isDel ? 35 : 65;
      if (!isDel && cIdx > cur.length) { spd = 1800; isDel = true; }
      else if (isDel && cIdx === 0) { isDel = false; pIdx = (pIdx + 1) % phrases.length; spd = 350; }
      setTimeout(runType, spd);
    }
    document.addEventListener("DOMContentLoaded", runType);

    // 2. Magnetic Dual-Ring Cursor & Global Spotlight
    const dot = document.getElementById("cursor-dot");
    const ring = document.getElementById("cursor-ring");
    let mouseX = window.innerWidth / 2, mouseY = window.innerHeight / 2;
    let ringX = mouseX, ringY = mouseY;

    window.addEventListener("mousemove", (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      document.documentElement.style.setProperty("--mouse-x", mouseX + "px");
      document.documentElement.style.setProperty("--mouse-y", mouseY + "px");
      if (dot) {
        dot.style.left = mouseX + "px";
        dot.style.top = mouseY + "px";
      }
      spawnTrailParticles(mouseX, mouseY);
    });

    function animateCursorRing() {
      ringX += (mouseX - ringX) * 0.18;
      ringY += (mouseY - ringY) * 0.18;
      if (ring) {
        ring.style.left = ringX + "px";
        ring.style.top = ringY + "px";
      }
      requestAnimationFrame(animateCursorRing);
    }
    animateCursorRing();

    document.querySelectorAll("a, button, .interactive-card, details").forEach((el) => {
      el.addEventListener("mouseenter", () => ring && ring.classList.add("cursor-hover"));
      el.addEventListener("mouseleave", () => ring && ring.classList.remove("cursor-hover"));
    });

    // 3. 3D Tilt & Local Card Glow on Mouse Move
    document.querySelectorAll(".interactive-card").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty("--card-x", x + "px");
        card.style.setProperty("--card-y", y + "px");
        const rotateY = ((x / rect.width) - 0.5) * 8;
        const rotateX = ((y / rect.height) - 0.5) * -8;
        card.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "perspective(900px) rotateX(0deg) rotateY(0deg) translateY(0px)";
      });
    });

    // 4. Interactive HTML5 Canvas Cursor Particle Trail + Constellation Network
    const canvas = document.getElementById("cursor-canvas");
    const ctx = canvas.getContext("2d");
    let particles = [];
    const colors = ["#06b6d4", "#3b82f6", "#a855f7", "#10b981"];

    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    function spawnTrailParticles(x, y) {
      for (let i = 0; i < 2; i++) {
        particles.push({
          x: x + (Math.random() - 0.5) * 10,
          y: y + (Math.random() - 0.5) * 10,
          vx: (Math.random() - 0.5) * 2.2,
          vy: (Math.random() - 0.5) * 2.2,
          size: Math.random() * 3 + 1.5,
          alpha: 1,
          color: colors[Math.floor(Math.random() * colors.length)]
        });
      }
      if (particles.length > 110) particles.splice(0, particles.length - 110);
    }

    function renderCanvas() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.alpha -= 0.018;

        if (p.alpha <= 0) {
          particles.splice(i, 1);
          i--;
          continue;
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.shadowBlur = 12;
        ctx.shadowColor = p.color;
        ctx.fill();

        // Connect nearby trail particles with glowing laser lines
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 75) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = p.color;
            ctx.globalAlpha = p.alpha * 0.35;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(renderCanvas);
    }
    renderCanvas();

    // 5. Scroll Reveal Observer
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add("active");
      });
    }, { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));
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
        "⚡ *TechnoServicesDigital Style Live Interactive Website Bot*\n\n"
        "Ye bot *Live Cursor Particle Effect + 3D Tilt + Deep Scrolling* wali Digital & Tech website generate karega.\n\n"
        "👇 *Is format me details bhejo:*\n"
        "`Name: Techno Services Digital`\n"
        "`Phone: +91 9876543210`\n"
        "`Email: support@heoo.in`\n"
        "`Address: Bypass Road, 2nd Floor, Rewa, Madhya Pradesh 474922`"
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
            f"⚡ *Live Interactive Digital Website Ready!*\n\n"
            f"🏢 *Name:* {data['name']}\n"
            f"📞 *Phone:* {data['phone']}\n"
            f"📧 *Email:* {data['email']}\n"
            f"📍 *Address:* {data['address']}\n\n"
            f"✨ *Features:* Live Mouse Particle Trail, Magnetic Cursor Ring, 3D Card Tilt, Live Video & 14-Section Deep Scroll."
        ),
        parse_mode="Markdown"
    )


app = Flask(__name__)

@app.route('/')
def health():
    return "TechnoServicesDigital Interactive Bot Live 24/7"

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
