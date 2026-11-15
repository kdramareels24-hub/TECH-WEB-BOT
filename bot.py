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
  <title>{{BUSINESS_NAME}} | Real Estate & Luxury Properties</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background-color: #ffffff;
      color: #111827;
      padding-bottom: 80px;
      overflow-x: hidden;
    }
    .nexus-red { color: #b91c1c; }
    .nexus-bg-red { background-color: #b91c1c; }
    .nexus-bg-red:hover { background-color: #991b1b; }
    .nexus-icon-box {
      background-color: #fdf2f2;
      color: #b91c1c;
    }

    /* 120FPS GPU Cursor Canvas */
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

    /* 120FPS Hardware-Accelerated Magnetic Cursor Dot & Ring */
    .cursor-dot {
      position: fixed;
      top: 0;
      left: 0;
      width: 10px;
      height: 10px;
      margin-left: -5px;
      margin-top: -5px;
      background: #b91c1c;
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      will-change: transform;
      box-shadow: 0 0 12px #b91c1c, 0 0 24px #f59e0b;
    }
    .cursor-ring {
      position: fixed;
      top: 0;
      left: 0;
      width: 44px;
      height: 44px;
      margin-left: -22px;
      margin-top: -22px;
      border: 2px solid rgba(185, 28, 28, 0.75);
      background: radial-gradient(circle, rgba(185, 28, 28, 0.1) 0%, rgba(245, 158, 11, 0.08) 60%, transparent 75%);
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      will-change: transform, width, height, border-color;
      transition: width 0.2s ease, height 0.2s ease, margin 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
    }
    .cursor-ring.cursor-hover {
      width: 70px;
      height: 70px;
      margin-left: -35px;
      margin-top: -35px;
      border-color: #ec4899;
      background: radial-gradient(circle, rgba(236, 72, 153, 0.16) 0%, rgba(6, 182, 212, 0.12) 60%, transparent 75%);
    }

    /* 120FPS 3D Perspective Tilt & Interactive Spotlight Glare */
    .tilt-3d {
      position: relative;
      transform-style: preserve-3d;
      will-change: transform;
      transition: transform 0.15s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.25s ease;
      overflow: hidden;
    }
    .tilt-3d::after {
      content: "";
      position: absolute;
      inset: 0;
      background: radial-gradient(420px circle at var(--glare-x, 50%) var(--glare-y, 50%), rgba(255, 255, 255, 0.38), rgba(185, 28, 28, 0.08) 40%, transparent 70%);
      opacity: 0;
      transition: opacity 0.25s ease;
      pointer-events: none;
      z-index: 5;
    }
    .tilt-3d:hover::after {
      opacity: 1;
    }
    .tilt-3d:hover {
      box-shadow: 0 24px 48px -12px rgba(185, 28, 28, 0.22), 0 10px 25px -8px rgba(0, 0, 0, 0.1);
    }

    /* Smooth 3D Floating Animation */
    @keyframes float3D {
      0%, 100% { transform: translate3d(0, 0px, 0); }
      50% { transform: translate3d(0, -10px, 0); }
    }
    .animate-float-3d {
      will-change: transform;
      animation: float3D 5.5s ease-in-out infinite;
    }

    /* Smooth Scroll Reveal */
    .reveal-3d {
      opacity: 0;
      transform: perspective(900px) translate3d(0, 35px, 0) rotateX(6deg);
      transition: opacity 0.65s ease-out, transform 0.65s cubic-bezier(0.2, 0.8, 0.2, 1);
      will-change: transform, opacity;
    }
    .reveal-3d.visible {
      opacity: 1;
      transform: perspective(900px) translate3d(0, 0, 0) rotateX(0deg);
    }

    .modal-active { display: flex !important; }
  </style>
</head>
<body class="antialiased selection:bg-red-700 selection:text-white">

  <!-- 120FPS GPU CURSOR TRAIL & MAGNETIC RINGS -->
  <canvas id="cursor-canvas"></canvas>
  <div id="cursor-dot" class="cursor-dot hidden md:block"></div>
  <div id="cursor-ring" class="cursor-ring hidden md:block"></div>

  <!-- 1. EXACT NEXUS PROPERTY STICKY HEADER -->
  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-5 py-3.5 flex justify-between items-center">
      <!-- Left: Exact Dual-Roof House Logo + Name + Tagline -->
      <a href="#home" class="flex flex-col items-start group">
        <div class="flex items-center">
          <svg class="w-24 h-8 -mb-1 transition-transform duration-300 group-hover:scale-105" viewBox="0 0 120 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 32L38 6L66 32H54L38 17L20 32H8Z" fill="#b91c1c"/>
            <rect x="20" y="10" width="6" height="10" fill="#b91c1c"/>
            <rect x="35" y="23" width="3.5" height="3.5" fill="#111827"/>
            <rect x="40" y="23" width="3.5" height="3.5" fill="#111827"/>
            <rect x="35" y="28" width="3.5" height="3.5" fill="#111827"/>
            <rect x="40" y="28" width="3.5" height="3.5" fill="#111827"/>
            <path d="M48 32L74 9L102 32H90L74 18L58 32H48Z" fill="#111827"/>
          </svg>
        </div>
        <div class="text-xl sm:text-2xl tracking-tight leading-none mt-0.5">
          <span class="font-extrabold text-[#b91c1c]">{{FIRST_WORD}}</span>
          <span class="font-normal text-gray-800">{{REST_WORDS}}</span>
        </div>
        <span class="text-[8px] font-semibold uppercase tracking-[0.22em] text-gray-500 mt-1">
          SIMPLE STEPS TO SUCCESS
        </span>
      </a>

      <!-- Desktop Nav Links -->
      <nav class="hidden lg:flex items-center space-x-8 text-sm font-medium text-gray-700">
        <a href="#home" class="text-[#b91c1c] font-semibold">Home</a>
        <a href="#properties" class="hover:text-[#b91c1c] transition">Properties</a>
        <a href="#about" class="hover:text-[#b91c1c] transition">About</a>
        <a href="#gallery" class="hover:text-[#b91c1c] transition">Gallery</a>
        <a href="#contact" class="hover:text-[#b91c1c] transition">Contact</a>
        <button onclick="openModal('loginModal')" class="border border-gray-900 px-4 py-2 rounded-lg text-xs font-semibold hover:bg-gray-900 hover:text-white transition">
          Login / Sign Up
        </button>
      </nav>

      <!-- Right: Exact 3-Line Hamburger Icon -->
      <button onclick="toggleMobileMenu()" class="lg:hidden text-gray-900 focus:outline-none p-1" aria-label="Menu">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 6h18M3 12h18M3 18h18"/>
        </svg>
      </button>
    </div>

    <!-- Mobile Dropdown Drawer -->
    <div id="mobileMenu" class="hidden lg:hidden bg-white border-t border-gray-100 px-6 py-5 space-y-3 shadow-lg">
      <a href="#home" onclick="toggleMobileMenu()" class="block py-2 text-sm font-semibold text-[#b91c1c]">Home</a>
      <a href="#properties" onclick="toggleMobileMenu()" class="block py-2 text-sm font-medium text-gray-800">Properties</a>
      <a href="#about" onclick="toggleMobileMenu()" class="block py-2 text-sm font-medium text-gray-800">About</a>
      <a href="#gallery" onclick="toggleMobileMenu()" class="block py-2 text-sm font-medium text-gray-800">Gallery</a>
      <a href="#contact" onclick="toggleMobileMenu()" class="block py-2 text-sm font-medium text-gray-800">Contact</a>
      <div class="pt-2 flex gap-3">
        <button onclick="toggleMobileMenu(); openModal('loginModal');" class="w-full py-2.5 bg-[#b91c1c] text-white text-xs font-semibold rounded-lg">Login / Register</button>
      </div>
    </div>
  </header>

  <!-- 2. EXACT HERO SECTION + 3D INTERACTIVE SLIDER (SCREENSHOT 1) -->
  <section id="home" class="max-w-7xl mx-auto px-5 pt-10 pb-14">
    <div class="grid lg:grid-cols-12 gap-10 items-center">
      <!-- Left Content Column -->
      <div class="lg:col-span-6 reveal-3d visible">
        <p class="text-[#b91c1c] text-xs sm:text-sm font-semibold uppercase tracking-[0.22em] mb-4">
          WELCOME TO {{BUSINESS_NAME_UPPER}}
        </p>

        <h1 class="text-4xl sm:text-5xl lg:text-[54px] font-bold text-gray-900 leading-[1.18] mb-6">
          Simple Steps,<br>to Your Dream Home
        </h1>

        <p class="text-gray-500 text-base sm:text-[17px] leading-[1.75] mb-8 font-normal">
          {{FIRST_WORD}} is here to help you find the best investment for your future, offering premium homes in prime locations with world-class amenities. Invest with confidence in properties that deliver comfort, quality, long-term value, and growth.
        </p>

        <!-- Exact Two Side-by-Side Buttons -->
        <div class="grid grid-cols-2 gap-4 max-w-md mb-10">
          <a href="#properties" class="tilt-3d nexus-bg-red text-white font-medium text-sm sm:text-base py-4 px-5 rounded-xl text-center shadow-md transition">
            Explore Properties
          </a>
          <a href="#contact" class="tilt-3d bg-white text-gray-900 border-[1.5px] border-gray-900 hover:bg-gray-900 hover:text-white font-medium text-sm sm:text-base py-4 px-5 rounded-xl text-center transition">
            Contact Us
          </a>
        </div>
      </div>

      <!-- Right / Bottom 3D Interactive Image Carousel Slider with < and > Arrows -->
      <div class="lg:col-span-6 animate-float-3d">
        <div class="tilt-3d relative rounded-2xl overflow-hidden shadow-xl bg-gray-100 h-[310px] sm:h-[420px]">
          <!-- Slide 1 -->
          <div class="hero-slide absolute inset-0 transition-opacity duration-700 opacity-100">
            <img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=85" alt="Srishti Greens Plotted Township" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent flex flex-col justify-end p-6 text-white">
              <span class="bg-[#b91c1c] text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded w-max mb-2">Plots For A Brighter Tomorrow</span>
              <h3 class="text-2xl sm:text-3xl font-extrabold tracking-wide">SRISHTI GREENS</h3>
              <p class="text-xs text-gray-200 uppercase tracking-widest">A Modern Living Destination • Gated Plots & Villas</p>
            </div>
          </div>

          <!-- Slide 2 -->
          <div class="hero-slide absolute inset-0 transition-opacity duration-700 opacity-0">
            <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=85" alt="Luxury Villas" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent flex flex-col justify-end p-6 text-white">
              <span class="bg-[#b91c1c] text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded w-max mb-2">Ready To Move In</span>
              <h3 class="text-2xl sm:text-3xl font-extrabold tracking-wide">IMPERIAL COUNTY VILLAS</h3>
              <p class="text-xs text-gray-200 uppercase tracking-widest">Prime Location • World-Class Clubhouse Amenities</p>
            </div>
          </div>

          <!-- Slide 3 -->
          <div class="hero-slide absolute inset-0 transition-opacity duration-700 opacity-0">
            <img src="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=85" alt="Premium Apartments" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent flex flex-col justify-end p-6 text-white">
              <span class="bg-[#b91c1c] text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded w-max mb-2">RERA Approved</span>
              <h3 class="text-2xl sm:text-3xl font-extrabold tracking-wide">ROYAL HEIGHTS RESIDENCY</h3>
              <p class="text-xs text-gray-200 uppercase tracking-widest">2, 3 & 4 BHK Luxury Homes • High ROI Investment</p>
            </div>
          </div>

          <!-- Left & Right Translucent Circle Arrows -->
          <button onclick="changeSlide(-1)" class="absolute left-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/40 hover:bg-[#b91c1c] text-white flex items-center justify-center backdrop-blur-sm transition z-10">
            <i class="fa-solid fa-chevron-left text-sm"></i>
          </button>
          <button onclick="changeSlide(1)" class="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/40 hover:bg-[#b91c1c] text-white flex items-center justify-center backdrop-blur-sm transition z-10">
            <i class="fa-solid fa-chevron-right text-sm"></i>
          </button>
        </div>
      </div>
    </div>
  </section>

  <!-- 3. 3D INTERACTIVE TRUST STATS COUNTER STRIP -->
  <section class="bg-gray-50 border-y border-gray-200 py-12 px-5 reveal-3d">
    <div class="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
      <div class="tilt-3d bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        <div class="text-3xl sm:text-4xl font-extrabold text-[#b91c1c] mb-1">1,200+</div>
        <div class="text-xs font-semibold uppercase tracking-wider text-gray-500">Happy Families</div>
      </div>
      <div class="tilt-3d bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        <div class="text-3xl sm:text-4xl font-extrabold text-[#b91c1c] mb-1">25+</div>
        <div class="text-xs font-semibold uppercase tracking-wider text-gray-500">Prime Projects</div>
      </div>
      <div class="tilt-3d bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        <div class="text-3xl sm:text-4xl font-extrabold text-[#b91c1c] mb-1">100%</div>
        <div class="text-xs font-semibold uppercase tracking-wider text-gray-500">Clear Title & Registry</div>
      </div>
      <div class="tilt-3d bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        <div class="text-3xl sm:text-4xl font-extrabold text-[#b91c1c] mb-1">12+ Yrs</div>
        <div class="text-xs font-semibold uppercase tracking-wider text-gray-500">Real Estate Excellence</div>
      </div>
    </div>
  </section>

  <!-- 4. FEATURED PROPERTIES SECTION WITH 3D TILT CARDS -->
  <section id="properties" class="py-16 px-5 max-w-7xl mx-auto reveal-3d">
    <div class="mb-12">
      <p class="text-[#b91c1c] text-xs sm:text-sm font-semibold uppercase tracking-[0.22em] mb-2">
        OUR PORTFOLIO
      </p>
      <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 leading-tight">
        Featured Properties & Plots
      </h2>
      <p class="text-gray-500 text-sm sm:text-base mt-2 max-w-2xl">
        Explore our handpicked residential plots, independent villas, luxury apartments, and commercial spaces in prime locations.
      </p>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Property Card 1 -->
      <div class="tilt-3d bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div class="relative h-64">
          <img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=85" alt="Srishti Greens Plots" class="w-full h-full object-cover">
          <span class="absolute top-4 left-4 nexus-bg-red text-white text-xs font-semibold px-3 py-1 rounded-md">
            Residential Plots
          </span>
          <span class="absolute bottom-4 right-4 bg-white/95 text-gray-900 text-xs font-bold px-3 py-1.5 rounded-lg shadow">
            Starting ₹ 25 Lakhs*
          </span>
        </div>
        <div class="p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-1">Srishti Greens Township</h3>
          <p class="text-xs text-gray-500 mb-4"><i class="fa-solid fa-location-dot text-[#b91c1c] mr-1"></i> Prime Highway Corridor • Gated Entry</p>
          <div class="grid grid-cols-2 gap-2 py-3 mb-4 border-y border-gray-100 text-xs text-gray-600 font-medium">
            <span><i class="fa-solid fa-vector-square text-[#b91c1c] mr-1.5"></i> 100 - 500 Sq.Yd.</span>
            <span><i class="fa-solid fa-file-contract text-[#b91c1c] mr-1.5"></i> Immediate Registry</span>
          </div>
          <a href="#contact" class="block w-full nexus-bg-red text-white text-center text-sm font-medium py-3 rounded-xl transition">
            Book Site Visit
          </a>
        </div>
      </div>

      <!-- Property Card 2 -->
      <div class="tilt-3d bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div class="relative h-64">
          <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=85" alt="Luxury Villa" class="w-full h-full object-cover">
          <span class="absolute top-4 left-4 nexus-bg-red text-white text-xs font-semibold px-3 py-1 rounded-md">
            Luxury Villas
          </span>
          <span class="absolute bottom-4 right-4 bg-white/95 text-gray-900 text-xs font-bold px-3 py-1.5 rounded-lg shadow">
            ₹ 1.45 Cr Onwards
          </span>
        </div>
        <div class="p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-1">Royal Palm Independent Villas</h3>
          <p class="text-xs text-gray-500 mb-4"><i class="fa-solid fa-location-dot text-[#b91c1c] mr-1"></i> Green Luxury Sector • 24/7 Security</p>
          <div class="grid grid-cols-2 gap-2 py-3 mb-4 border-y border-gray-100 text-xs text-gray-600 font-medium">
            <span><i class="fa-solid fa-bed text-[#b91c1c] mr-1.5"></i> 3 & 4 BHK Duplex</span>
            <span><i class="fa-solid fa-circle-check text-[#b91c1c] mr-1.5"></i> Bank Loan Available</span>
          </div>
          <a href="#contact" class="block w-full nexus-bg-red text-white text-center text-sm font-medium py-3 rounded-xl transition">
            Book Site Visit
          </a>
        </div>
      </div>

      <!-- Property Card 3 -->
      <div class="tilt-3d bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div class="relative h-64">
          <img src="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=85" alt="Luxury Apartments" class="w-full h-full object-cover">
          <span class="absolute top-4 left-4 nexus-bg-red text-white text-xs font-semibold px-3 py-1 rounded-md">
            Premium Flats
          </span>
          <span class="absolute bottom-4 right-4 bg-white/95 text-gray-900 text-xs font-bold px-3 py-1.5 rounded-lg shadow">
            ₹ 68 Lakhs Onwards
          </span>
        </div>
        <div class="p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-1">Skyline Grand Residency</h3>
          <p class="text-xs text-gray-500 mb-4"><i class="fa-solid fa-location-dot text-[#b91c1c] mr-1"></i> Main Metro Connectivity • Clubhouse</p>
          <div class="grid grid-cols-2 gap-2 py-3 mb-4 border-y border-gray-100 text-xs text-gray-600 font-medium">
            <span><i class="fa-solid fa-building text-[#b91c1c] mr-1.5"></i> 2 & 3 BHK Flats</span>
            <span><i class="fa-solid fa-shield-halved text-[#b91c1c] mr-1.5"></i> RERA Registered</span>
          </div>
          <a href="#contact" class="block w-full nexus-bg-red text-white text-center text-sm font-medium py-3 rounded-xl transition">
            Book Site Visit
          </a>
        </div>
      </div>

      <!-- Property Card 4 -->
      <div class="tilt-3d bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div class="relative h-64">
          <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=85" alt="Commercial Hub" class="w-full h-full object-cover">
          <span class="absolute top-4 left-4 nexus-bg-red text-white text-xs font-semibold px-3 py-1 rounded-md">
            Commercial Space
          </span>
          <span class="absolute bottom-4 right-4 bg-white/95 text-gray-900 text-xs font-bold px-3 py-1.5 rounded-lg shadow">
            ₹ 55 Lakhs Onwards
          </span>
        </div>
        <div class="p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-1">Living Style Commercial Mall</h3>
          <p class="text-xs text-gray-500 mb-4"><i class="fa-solid fa-location-dot text-[#b91c1c] mr-1"></i> High-Footfall Business District</p>
          <div class="grid grid-cols-2 gap-2 py-3 mb-4 border-y border-gray-100 text-xs text-gray-600 font-medium">
            <span><i class="fa-solid fa-shop text-[#b91c1c] mr-1.5"></i> Retail & Offices</span>
            <span><i class="fa-solid fa-chart-line text-[#b91c1c] mr-1.5"></i> Assured Rental ROI</span>
          </div>
          <a href="#contact" class="block w-full nexus-bg-red text-white text-center text-sm font-medium py-3 rounded-xl transition">
            Book Site Visit
          </a>
        </div>
      </div>

      <!-- Property Card 5 -->
      <div class="tilt-3d bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div class="relative h-64">
          <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=85" alt="Farmhouse Plots" class="w-full h-full object-cover">
          <span class="absolute top-4 left-4 nexus-bg-red text-white text-xs font-semibold px-3 py-1 rounded-md">
            Green Farmhouses
          </span>
          <span class="absolute bottom-4 right-4 bg-white/95 text-gray-900 text-xs font-bold px-3 py-1.5 rounded-lg shadow">
            ₹ 90 Lakhs Onwards
          </span>
        </div>
        <div class="p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-1">Nature Valley Eco Farms</h3>
          <p class="text-xs text-gray-500 mb-4"><i class="fa-solid fa-location-dot text-[#b91c1c] mr-1"></i> Pollution-Free Expressway Zone</p>
          <div class="grid grid-cols-2 gap-2 py-3 mb-4 border-y border-gray-100 text-xs text-gray-600 font-medium">
            <span><i class="fa-solid fa-tree text-[#b91c1c] mr-1.5"></i> 1000+ Sq.Yd. Farms</span>
            <span><i class="fa-solid fa-lock text-[#b91c1c] mr-1.5"></i> Gated Boundary Wall</span>
          </div>
          <a href="#contact" class="block w-full nexus-bg-red text-white text-center text-sm font-medium py-3 rounded-xl transition">
            Book Site Visit
          </a>
        </div>
      </div>

      <!-- Property Card 6 -->
      <div class="tilt-3d bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div class="relative h-64">
          <img src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=800&q=85" alt="Builder Floors" class="w-full h-full object-cover">
          <span class="absolute top-4 left-4 nexus-bg-red text-white text-xs font-semibold px-3 py-1 rounded-md">
            Builder Floors
          </span>
          <span class="absolute bottom-4 right-4 bg-white/95 text-gray-900 text-xs font-bold px-3 py-1.5 rounded-lg shadow">
            ₹ 75 Lakhs Onwards
          </span>
        </div>
        <div class="p-6">
          <h3 class="text-xl font-bold text-gray-900 mb-1">Prime Luxury Builder Floors</h3>
          <p class="text-xs text-gray-500 mb-4"><i class="fa-solid fa-location-dot text-[#b91c1c] mr-1"></i> Independent Floor with Lift & Parking</p>
          <div class="grid grid-cols-2 gap-2 py-3 mb-4 border-y border-gray-100 text-xs text-gray-600 font-medium">
            <span><i class="fa-solid fa-couch text-[#b91c1c] mr-1.5"></i> Modular Kitchen</span>
            <span><i class="fa-solid fa-key text-[#b91c1c] mr-1.5"></i> Ready Possession</span>
          </div>
          <a href="#contact" class="block w-full nexus-bg-red text-white text-center text-sm font-medium py-3 rounded-xl transition">
            Book Site Visit
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- 5. ABOUT US SECTION WITH 3D TILT FRAMES -->
  <section id="about" class="py-16 bg-gray-50 border-y border-gray-200 px-5 reveal-3d">
    <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 items-center">
      <div class="lg:col-span-6">
        <p class="text-[#b91c1c] text-xs sm:text-sm font-semibold uppercase tracking-[0.22em] mb-3">
          ABOUT {{BUSINESS_NAME_UPPER}}
        </p>
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 leading-tight mb-5">
          Trusted Real Estate Partner For Your Future
        </h2>
        <p class="text-gray-500 text-base leading-relaxed mb-6">
          <strong>{{BUSINESS_NAME}}</strong> is a premier real estate consultancy and property development enterprise headquartered at <strong>{{ADDRESS}}</strong>. We specialize in residential plots, luxury villas, high-rise apartments, and commercial retail investments.
        </p>
        <div class="space-y-4 mb-8">
          <div class="tilt-3d bg-white p-4 rounded-xl border border-gray-200 flex items-start space-x-3.5">
            <div class="w-8 h-8 rounded-lg nexus-icon-box flex items-center justify-center flex-shrink-0 mt-0.5">
              <i class="fa-solid fa-check text-sm"></i>
            </div>
            <div>
              <h4 class="font-bold text-gray-900 text-sm">100% Verified Legal Titles</h4>
              <p class="text-xs text-gray-500 mt-0.5">Every project undergoes complete document verification, CLU/RERA checks, and clear registry assurance.</p>
            </div>
          </div>
          <div class="tilt-3d bg-white p-4 rounded-xl border border-gray-200 flex items-start space-x-3.5">
            <div class="w-8 h-8 rounded-lg nexus-icon-box flex items-center justify-center flex-shrink-0 mt-0.5">
              <i class="fa-solid fa-check text-sm"></i>
            </div>
            <div>
              <h4 class="font-bold text-gray-900 text-sm">Prime High-Growth Locations</h4>
              <p class="text-xs text-gray-500 mt-0.5">Strategically located near highways, metro corridors, schools, and hospitals for maximum appreciation.</p>
            </div>
          </div>
          <div class="tilt-3d bg-white p-4 rounded-xl border border-gray-200 flex items-start space-x-3.5">
            <div class="w-8 h-8 rounded-lg nexus-icon-box flex items-center justify-center flex-shrink-0 mt-0.5">
              <i class="fa-solid fa-check text-sm"></i>
            </div>
            <div>
              <h4 class="font-bold text-gray-900 text-sm">End-to-End Home Loan & Registry</h4>
              <p class="text-xs text-gray-500 mt-0.5">Dedicated assistance from site visit and bank loan sanction to final mutation and possession.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="lg:col-span-6 grid grid-cols-2 gap-4">
        <div class="tilt-3d rounded-2xl overflow-hidden shadow-md h-64">
          <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=700&q=85" alt="Luxury Interior" class="w-full h-full object-cover">
        </div>
        <div class="tilt-3d rounded-2xl overflow-hidden shadow-md h-64 mt-6">
          <img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=700&q=85" alt="Dream Home Key" class="w-full h-full object-cover">
        </div>
      </div>
    </div>
  </section>

  <!-- 6. 3D SITE GALLERY SECTION -->
  <section id="gallery" class="py-16 px-5 max-w-7xl mx-auto reveal-3d">
    <div class="mb-10">
      <p class="text-[#b91c1c] text-xs sm:text-sm font-semibold uppercase tracking-[0.22em] mb-2">
        SITE GALLERY
      </p>
      <h2 class="text-3xl sm:text-4xl font-bold text-gray-900">
        Actual Site Photos & Developments
      </h2>
    </div>

    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="tilt-3d rounded-2xl overflow-hidden h-56 shadow-sm">
        <img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=700&q=85" alt="Project Entrance" class="w-full h-full object-cover">
      </div>
      <div class="tilt-3d rounded-2xl overflow-hidden h-56 shadow-sm">
        <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=700&q=85" alt="Completed Villa" class="w-full h-full object-cover">
      </div>
      <div class="tilt-3d rounded-2xl overflow-hidden h-56 shadow-sm">
        <img src="https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=700&q=85" alt="Clubhouse" class="w-full h-full object-cover">
      </div>
      <div class="tilt-3d rounded-2xl overflow-hidden h-56 shadow-sm">
        <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=700&q=85" alt="Modern Residence" class="w-full h-full object-cover">
      </div>
    </div>
  </section>

  <!-- 7. EXACT "GET IN TOUCH" & "BOOK A FREE CONSULTATION" SECTION (SCREENSHOT 2 & 3) -->
  <section id="contact" class="py-16 px-5 max-w-7xl mx-auto border-t border-gray-100 reveal-3d">
    <div class="grid lg:grid-cols-12 gap-12 items-start">

      <!-- LEFT COLUMN: EXACT SCREENSHOT 2 LAYOUT -->
      <div class="lg:col-span-6">
        <p class="text-[#b91c1c] text-xs sm:text-sm font-semibold uppercase tracking-[0.22em] mb-3">
          GET IN TOUCH
        </p>

        <h2 class="text-4xl sm:text-[44px] font-bold text-gray-900 leading-[1.18] mb-5">
          Let's Find Your<br>Dream Home
        </h2>

        <p class="text-gray-500 text-base sm:text-[17px] leading-[1.75] mb-10">
          Reach out to our team of experts for personalised assistance with finding your perfect luxury property.
        </p>

        <!-- 3 Exact Contact Items: Head Office (Address), Phone, Email -->
        <div class="space-y-8">
          <!-- Item 1: Head Office & Our Branches -->
          <div class="flex items-start space-x-5">
            <div class="tilt-3d w-14 h-14 rounded-2xl nexus-icon-box flex items-center justify-center flex-shrink-0">
              <svg class="w-8 h-8 text-[#b91c1c]" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 21c-4.5-4.5-7-8.2-7-11.5a7 7 0 1114 0c0 3.3-2.5 7-7 11.5z"/>
                <circle cx="12" cy="9.5" r="2.8" stroke="currentColor" stroke-width="2.2"/>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">Head Office</h3>
              <p class="text-gray-500 text-base leading-relaxed mb-3">{{ADDRESS}}</p>
              <h4 class="text-lg font-bold text-gray-900 mb-1">Our Branches</h4>
              <p class="text-gray-500 text-base">Nangloi, Pahladpur, Dwarka</p>
            </div>
          </div>

          <!-- Item 2: Phone -->
          <div class="flex items-start space-x-5">
            <div class="tilt-3d w-14 h-14 rounded-2xl nexus-icon-box flex items-center justify-center flex-shrink-0">
              <i class="fa-solid fa-phone-volume text-2xl text-[#b91c1c]"></i>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">Phone</h3>
              <a href="tel:{{PHONE}}" class="text-gray-500 hover:text-[#b91c1c] text-base transition">{{PHONE}}</a>
            </div>
          </div>

          <!-- Item 3: Email -->
          <div class="flex items-start space-x-5">
            <div class="tilt-3d w-14 h-14 rounded-2xl nexus-icon-box flex items-center justify-center flex-shrink-0">
              <i class="fa-regular fa-envelope text-2xl text-[#b91c1c]"></i>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">Email</h3>
              <a href="mailto:{{EMAIL}}" class="text-gray-500 hover:text-[#b91c1c] text-base break-all transition">{{EMAIL}}</a>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN: EXACT SCREENSHOT 3 "BOOK A FREE CONSULTATION" FORM CARD WITH 3D TILT -->
      <div class="lg:col-span-6">
        <div class="tilt-3d bg-white rounded-3xl shadow-[0_10px_40px_rgba(0,0,0,0.08)] border border-gray-100 p-6 sm:p-10">
          <h3 class="text-2xl sm:text-[26px] font-bold text-gray-900 mb-6">
            Book a Free Consultation
          </h3>

          <form onsubmit="event.preventDefault(); alert('Thank you! Our team at {{BUSINESS_NAME}} will contact you shortly.');" class="space-y-4">
            <div>
              <input type="text" required placeholder="Your Full Name" class="w-full bg-white border border-gray-200 rounded-xl px-4 py-4 text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:border-[#b91c1c]">
            </div>

            <div>
              <input type="email" required placeholder="Email Address" class="w-full bg-white border border-gray-200 rounded-xl px-4 py-4 text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:border-[#b91c1c]">
            </div>

            <div>
              <input type="tel" required placeholder="Phone Number" class="w-full bg-white border border-gray-200 rounded-xl px-4 py-4 text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:border-[#b91c1c]">
            </div>

            <div>
              <select required class="w-full bg-white border border-gray-200 rounded-xl px-4 py-4 text-gray-700 text-sm sm:text-base focus:outline-none focus:border-[#b91c1c]">
                <option value="" disabled selected>Select Property Type</option>
                <option>Residential Plot (Srishti Greens)</option>
                <option>Luxury Villa / Independent House</option>
                <option>2 / 3 / 4 BHK Apartment</option>
                <option>Commercial Shop / Office Space</option>
              </select>
            </div>

            <div>
              <textarea rows="4" placeholder="Your Message" class="w-full bg-white border border-gray-200 rounded-xl px-4 py-4 text-gray-800 placeholder-gray-400 text-sm sm:text-base focus:outline-none focus:border-[#b91c1c]"></textarea>
            </div>

            <button type="submit" class="w-full nexus-bg-red text-white font-semibold text-base py-4 rounded-xl shadow-md transition">
              Send Message
            </button>
          </form>
        </div>
      </div>

    </div>
  </section>

  <!-- 8. FOOTER WITH VERIFIED BUSINESS DETAILS -->
  <footer class="bg-gray-900 text-gray-300 py-12 px-5 mt-10">
    <div class="max-w-7xl mx-auto grid md:grid-cols-3 gap-8 pb-8 border-b border-gray-800">
      <div>
        <h4 class="text-xl font-bold text-white mb-2">{{BUSINESS_NAME}}</h4>
        <p class="text-xs text-gray-400 leading-relaxed">
          {{BUSINESS_NAME}} is here to help you find the best investment for your future, offering premium homes and plots in prime locations.
        </p>
      </div>
      <div class="text-xs space-y-2">
        <div class="font-bold text-white uppercase tracking-wider mb-2">Head Office</div>
        <p>{{ADDRESS}}</p>
      </div>
      <div class="text-xs space-y-2">
        <div class="font-bold text-white uppercase tracking-wider mb-2">Direct Contact</div>
        <p>Phone: <a href="tel:{{PHONE}}" class="text-white font-semibold">{{PHONE}}</a></p>
        <p>Email: <a href="mailto:{{EMAIL}}" class="text-white font-semibold">{{EMAIL}}</a></p>
      </div>
    </div>
    <div class="max-w-7xl mx-auto pt-6 text-center text-xs text-gray-400">
      © 2026 <strong>{{BUSINESS_NAME}}</strong>. All Rights Reserved. | Head Office: {{ADDRESS}} | Phone: {{PHONE}} | Email: {{EMAIL}}
    </div>
  </footer>

  <!-- 9. EXACT FIXED BOTTOM APP BAR (HOME, PROPERTIES, ABOUT, GALLERY, CONTACT - SCREENSHOT 1, 2, 3) -->
  <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-2.5 px-2 z-50 shadow-[0_-4px_20px_rgba(0,0,0,0.05)]">
    <div class="max-w-md mx-auto grid grid-cols-5 text-center">
      <a href="#home" class="bottom-nav-item flex flex-col items-center justify-center text-[#b91c1c]">
        <i class="fa-solid fa-house text-lg mb-1"></i>
        <span class="text-[11px] font-medium">Home</span>
      </a>
      <a href="#properties" class="bottom-nav-item flex flex-col items-center justify-center text-gray-800 hover:text-[#b91c1c] transition">
        <i class="fa-solid fa-building text-lg mb-1"></i>
        <span class="text-[11px] font-medium">Properties</span>
      </a>
      <a href="#about" class="bottom-nav-item flex flex-col items-center justify-center text-gray-800 hover:text-[#b91c1c] transition">
        <i class="fa-solid fa-user text-lg mb-1"></i>
        <span class="text-[11px] font-medium">About</span>
      </a>
      <a href="#gallery" class="bottom-nav-item flex flex-col items-center justify-center text-gray-800 hover:text-[#b91c1c] transition">
        <i class="fa-regular fa-image text-lg mb-1"></i>
        <span class="text-[11px] font-medium">Gallery</span>
      </a>
      <a href="#contact" class="bottom-nav-item flex flex-col items-center justify-center text-gray-800 hover:text-[#b91c1c] transition">
        <i class="fa-solid fa-phone text-lg mb-1"></i>
        <span class="text-[11px] font-medium">Contact</span>
      </a>
    </div>
  </nav>

  <!-- LOGIN / SIGN UP MODAL WITH CONTINUE WITH GOOGLE -->
  <div id="loginModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white text-gray-900 w-full max-w-md p-8 rounded-3xl shadow-2xl relative">
      <button onclick="closeModal('loginModal')" class="absolute top-5 right-5 text-gray-400 hover:text-gray-900 text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-bold mb-1">Welcome to {{BUSINESS_NAME}}</h3>
      <p class="text-xs text-gray-500 mb-6">Sign in or register to view property brochures & booking status</p>

      <button onclick="alert('Redirecting to Google Sign-In...');" class="w-full bg-white hover:bg-gray-50 text-gray-800 font-semibold py-3.5 px-4 rounded-xl border border-gray-300 flex items-center justify-center space-x-3 mb-5 shadow-sm">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span class="text-sm">Continue with Google</span>
      </button>

      <form onsubmit="event.preventDefault(); alert('Logged in successfully!'); closeModal('loginModal');" class="space-y-4 text-sm">
        <input type="email" required placeholder="Email Address" class="w-full border border-gray-200 rounded-xl px-4 py-3.5 focus:outline-none focus:border-[#b91c1c]">
        <input type="password" required placeholder="Password" class="w-full border border-gray-200 rounded-xl px-4 py-3.5 focus:outline-none focus:border-[#b91c1c]">
        <button type="submit" class="w-full nexus-bg-red text-white font-semibold py-3.5 rounded-xl shadow-md">Continue</button>
      </form>
    </div>
  </div>

  <!-- 120FPS 3D PERSPECTIVE TILT, MAGNETIC RING & CONNECTED LASER TRAIL ENGINE -->
  <script>
    function toggleMobileMenu() {
      document.getElementById('mobileMenu').classList.toggle('hidden');
    }
    function openModal(id) { document.getElementById(id).classList.add('modal-active'); }
    function closeModal(id) { document.getElementById(id).classList.remove('modal-active'); }

    // 1. Hero Image Carousel Slider
    let currentSlide = 0;
    const slides = document.querySelectorAll('.hero-slide');
    function showSlide(index) {
      slides.forEach((s, i) => {
        s.style.opacity = (i === index) ? '1' : '0';
      });
    }
    function changeSlide(step) {
      currentSlide = (currentSlide + step + slides.length) % slides.length;
      showSlide(currentSlide);
    }
    setInterval(() => changeSlide(1), 4500);

    // 2. 120FPS 3D Perspective Card Tilt + Specular Glare
    document.querySelectorAll(".tilt-3d").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty("--glare-x", x + "px");
        card.style.setProperty("--glare-y", y + "px");
        const rotateY = ((x / rect.width) - 0.5) * 10;
        const rotateX = ((y / rect.height) - 0.5) * -10;
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
      }, { passive: true });

      card.addEventListener("mouseleave", () => {
        card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)";
      }, { passive: true });
    });

    // 3. 120FPS Scroll Reveal 3D Observer
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add("visible");
      });
    }, { threshold: 0.1 });
    document.querySelectorAll(".reveal-3d").forEach((el) => observer.observe(el));

    // 4. Zero-Lag 120FPS GPU Magnetic Ring + Connected Multi-Color Laser Trail
    const dot = document.getElementById("cursor-dot");
    const ring = document.getElementById("cursor-ring");
    const canvas = document.getElementById("cursor-canvas");
    const ctx = canvas.getContext("2d", { alpha: true });

    let mouseX = window.innerWidth / 2, mouseY = window.innerHeight / 2;
    let ringX = mouseX, ringY = mouseY;
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
      const now = performance.now();
      if (now - lastSpawn > 16) {
        lastSpawn = now;
        hue = (hue + 15) % 360;
        particles.push({
          x: mouseX,
          y: mouseY,
          vx: (Math.random() - 0.5) * 2.5,
          vy: (Math.random() - 0.5) * 2.5,
          size: Math.random() * 4 + 2,
          alpha: 0.95,
          hue: hue
        });
        if (particles.length > 46) particles.shift();
      }
    }, { passive: true });

    document.querySelectorAll("a, button, input, select, textarea, .tilt-3d").forEach((el) => {
      el.addEventListener("mouseenter", () => ring && ring.classList.add("cursor-hover"), { passive: true });
      el.addEventListener("mouseleave", () => ring && ring.classList.remove("cursor-hover"), { passive: true });
    });

    function renderLoop() {
      ringX += (mouseX - ringX) * 0.22;
      ringY += (mouseY - ringY) * 0.22;
      if (ring) ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0)`;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

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
        ctx.fillStyle = `hsla(${p.hue}, 90%, 48%, ${p.alpha})`;
        ctx.fill();

        if (i > 0) {
          const prev = particles[i - 1];
          const dx = p.x - prev.x;
          const dy = p.y - prev.y;
          if (dx * dx + dy * dy < 6400) {
            ctx.beginPath();
            ctx.moveTo(prev.x, prev.y);
            ctx.lineTo(p.x, p.y);
            ctx.strokeStyle = `hsla(${p.hue}, 95%, 45%, ${p.alpha * 0.65})`;
            ctx.lineWidth = 1.8;
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


def split_business_name(name):
    parts = name.strip().split(" ", 1)
    first_word = parts[0]
    rest_words = " " + parts[1] if len(parts) > 1 else ""
    return first_word, rest_words


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = (
        "🏠 *Exact NexusProperty Clone + 120FPS 3D Animation Bot*\n\n"
        "Ye bot bilkul *nexusproperty.in* jaisa exact interface + *120FPS 3D Card Tilt, Magnetic Cursor Ring aur Connected Laser Trail* wali website banayega.\n\n"
        "👇 *Is format me details bhejo:*\n"
        "`Name: Nexus Property`\n"
        "`Phone: +91-98108 90055`\n"
        "`Email: info@nexusproperty.com`\n"
        "`Address: 320 A-B Third floor, Living Style Mall, Jasola, New Delhi - 110025`"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def generate_site(message):
    data = parse_details(message.text)
    if not all(k in data for k in ["name", "phone", "email", "address"]):
        bot.reply_to(
            message,
            "⚠️ *Saari 4 details sahi format me bhejo:*\n\n"
            "`Name: Nexus Property`\n"
            "`Phone: +91-98108 90055`\n"
            "`Email: info@heoo.in`\n"
            "`Address: Full Office Address`",
            parse_mode="Markdown"
        )
        return

    first_word, rest_words = split_business_name(data["name"])

    html = (
        HTML_TEMPLATE
        .replace("{{BUSINESS_NAME}}", data["name"])
        .replace("{{BUSINESS_NAME_UPPER}}", data["name"].upper())
        .replace("{{FIRST_WORD}}", first_word)
        .replace("{{REST_WORDS}}", rest_words)
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
            f"🔥 *Exact NexusProperty + 120FPS 3D Website Ready!*\n\n"
            f"🏠 *Name:* {data['name']}\n"
            f"📞 *Phone:* {data['phone']}\n"
            f"📧 *Email:* {data['email']}\n"
            f"📍 *Head Office:* {data['address']}\n\n"
            f"✨ *Active:* 120FPS 3D Perspective Card Tilt, Magnetic Cursor Ring, Connected Laser Trail & Exact Nexus Layout."
        ),
        parse_mode="Markdown"
    )


app = Flask(__name__)

@app.route('/')
def health():
    return "NexusProperty 120FPS 3D Bot Live 24/7"

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
