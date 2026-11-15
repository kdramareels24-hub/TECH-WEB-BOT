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
      padding-bottom: 76px;
      overflow-x: hidden;
    }
    .nexus-red { color: #b91c1c; }
    .nexus-bg-red { background-color: #b91c1c; }
    .nexus-bg-red:hover { background-color: #991b1b; }
    .nexus-icon-box {
      background-color: #fdf2f2;
      color: #b91c1c;
    }
    .prop-card {
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .prop-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 15px 30px -10px rgba(185, 28, 28, 0.12);
    }
    .modal-active { display: flex !important; }
  </style>
</head>
<body class="antialiased selection:bg-red-700 selection:text-white">

  <!-- EXACT NEXUS PROPERTY STICKY HEADER -->
  <header class="sticky top-0 z-40 bg-white border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-5 py-3.5 flex justify-between items-center">
      <!-- Left: Dual-Roof House Logo + Name + Tagline -->
      <a href="#home" class="flex flex-col items-start">
        <div class="flex items-center">
          <svg class="w-24 h-8 -mb-1" viewBox="0 0 120 40" fill="none" xmlns="http://www.w3.org/2000/svg">
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

      <!-- Hamburger Menu Button -->
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

  <!-- HERO SECTION + IMAGE SLIDER (SCREENSHOT 1) -->
  <section id="home" class="max-w-7xl mx-auto px-5 pt-10 pb-14">
    <div class="grid lg:grid-cols-12 gap-10 items-center">
      <div class="lg:col-span-6">
        <p class="text-[#b91c1c] text-xs sm:text-sm font-semibold uppercase tracking-[0.22em] mb-4">
          WELCOME TO {{BUSINESS_NAME_UPPER}}
        </p>

        <h1 class="text-4xl sm:text-5xl lg:text-[54px] font-bold text-gray-900 leading-[1.18] mb-6">
          Simple Steps,<br>to Your Dream Home
        </h1>

        <p class="text-gray-500 text-base sm:text-[17px] leading-[1.75] mb-8 font-normal">
          {{FIRST_WORD}} is here to help you find the best investment for your future, offering premium homes in prime locations with world-class amenities. Invest with confidence in properties that deliver comfort, quality, long-term value, and growth.
        </p>

        <div class="grid grid-cols-2 gap-4 max-w-md mb-10">
          <a href="#properties" class="nexus-bg-red text-white font-medium text-sm sm:text-base py-4 px-5 rounded-xl text-center shadow-sm transition">
            Explore Properties
          </a>
          <a href="#contact" class="bg-white text-gray-900 border-[1.5px] border-gray-900 hover:bg-gray-900 hover:text-white font-medium text-sm sm:text-base py-4 px-5 rounded-xl text-center transition">
            Contact Us
          </a>
        </div>
      </div>

      <!-- Image Carousel Slider with < and > Arrows -->
      <div class="lg:col-span-6">
        <div class="relative rounded-2xl overflow-hidden shadow-lg group bg-gray-100 h-[300px] sm:h-[400px]">
          <div class="hero-slide absolute inset-0 transition-opacity duration-700 opacity-100">
            <img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=85" alt="Srishti Greens" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent flex flex-col justify-end p-6 text-white">
              <span class="bg-[#b91c1c] text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded w-max mb-2">Plots For A Brighter Tomorrow</span>
              <h3 class="text-2xl sm:text-3xl font-extrabold tracking-wide">SRISHTI GREENS</h3>
              <p class="text-xs text-gray-200 uppercase tracking-widest">A Modern Living Destination • Gated Plots & Villas</p>
            </div>
          </div>

          <div class="hero-slide absolute inset-0 transition-opacity duration-700 opacity-0">
            <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=85" alt="Luxury Villas" class="w-full h-full object-cover">
            <div class="absolute inset-0 bg-gradient-to-t from-black/75 via-black/20 to-transparent flex flex-col justify-end p-6 text-white">
              <span class="bg-[#b91c1c] text-white text-[10px] font-bold uppercase tracking-widest px-3 py-1 rounded w-max mb-2">Ready To Move In</span>
              <h3 class="text-2xl sm:text-3xl font-extrabold tracking-wide">IMPERIAL COUNTY VILLAS</h3>
              <p class="text-xs text-gray-200 uppercase tracking-widest">Prime Location • World-Class Clubhouse Amenities</p>
            </div>
          </div>

          <button onclick="changeSlide(-1)" class="absolute left-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/35 hover:bg-black/60 text-white flex items-center justify-center backdrop-blur-sm transition z-10">
            <i class="fa-solid fa-chevron-left text-sm"></i>
          </button>
          <button onclick="changeSlide(1)" class="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/35 hover:bg-black/60 text-white flex items-center justify-center backdrop-blur-sm transition z-10">
            <i class="fa-solid fa-chevron-right text-sm"></i>
          </button>
        </div>
      </div>
    </div>
  </section>

  <!-- TRUST STATS -->
  <section class="bg-gray-50 border-y border-gray-200 py-12 px-5">
    <div class="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
      <div>
        <div class="text-3xl sm:text-4xl font-extrabold text-[#b91c1c] mb-1">1,200+</div>
        <div class="text-xs font-semibold uppercase tracking-wider text-gray-500">Happy Families</div>
      </div>
      <div>
        <div class="text-3xl sm:text-4xl font-extrabold text-[#b91c1c] mb-1">25+</div>
        <div class="text-xs font-semibold uppercase tracking-wider text-gray-500">Prime Projects</div>
      </div>
      <div>
        <div class="text-3xl sm:text-4xl font-extrabold text-[#b91c1c] mb-1">100%</div>
        <div class="text-xs font-semibold uppercase tracking-wider text-gray-500">Clear Title & Registry</div>
      </div>
      <div>
        <div class="text-3xl sm:text-4xl font-extrabold text-[#b91c1c] mb-1">12+ Yrs</div>
        <div class="text-xs font-semibold uppercase tracking-wider text-gray-500">Real Estate Excellence</div>
      </div>
    </div>
  </section>

  <!-- PROPERTIES SECTION -->
  <section id="properties" class="py-16 px-5 max-w-7xl mx-auto">
    <div class="mb-12">
      <p class="text-[#b91c1c] text-xs sm:text-sm font-semibold uppercase tracking-[0.22em] mb-2">OUR PORTFOLIO</p>
      <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 leading-tight">Featured Properties & Plots</h2>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div class="prop-card bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div class="relative h-64"><img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=85" class="w-full h-full object-cover"></div>
        <div class="p-6"><h3 class="text-xl font-bold text-gray-900 mb-1">Srishti Greens Township</h3><p class="text-xs text-gray-500 mb-4"><i class="fa-solid fa-location-dot text-[#b91c1c] mr-1"></i> Prime Highway Corridor</p></div>
      </div>
      <div class="prop-card bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div class="relative h-64"><img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=85" class="w-full h-full object-cover"></div>
        <div class="p-6"><h3 class="text-xl font-bold text-gray-900 mb-1">Royal Palm Independent Villas</h3><p class="text-xs text-gray-500 mb-4"><i class="fa-solid fa-location-dot text-[#b91c1c] mr-1"></i> Green Luxury Sector</p></div>
      </div>
      <div class="prop-card bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
        <div class="relative h-64"><img src="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=85" class="w-full h-full object-cover"></div>
        <div class="p-6"><h3 class="text-xl font-bold text-gray-900 mb-1">Skyline Grand Residency</h3><p class="text-xs text-gray-500 mb-4"><i class="fa-solid fa-location-dot text-[#b91c1c] mr-1"></i> Main Metro Connectivity</p></div>
      </div>
    </div>
  </section>

  <!-- ABOUT SECTION -->
  <section id="about" class="py-16 bg-gray-50 border-y border-gray-200 px-5">
    <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 items-center">
      <div class="lg:col-span-6">
        <p class="text-[#b91c1c] text-xs sm:text-sm font-semibold uppercase tracking-[0.22em] mb-3">ABOUT {{BUSINESS_NAME_UPPER}}</p>
        <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 leading-tight mb-5">Trusted Real Estate Partner For Your Future</h2>
        <p class="text-gray-500 text-base leading-relaxed mb-6"><strong>{{BUSINESS_NAME}}</strong> is a premier real estate consultancy headquartered at <strong>{{ADDRESS}}</strong>.</p>
      </div>
      <div class="lg:col-span-6 grid grid-cols-2 gap-4">
        <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=700&q=85" class="rounded-2xl shadow-md h-64 w-full object-cover">
        <img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=700&q=85" class="rounded-2xl shadow-md h-64 w-full object-cover mt-6">
      </div>
    </div>
  </section>

  <!-- GALLERY SECTION -->
  <section id="gallery" class="py-16 px-5 max-w-7xl mx-auto">
    <div class="mb-10"><p class="text-[#b91c1c] text-xs font-semibold uppercase tracking-[0.22em] mb-2">SITE GALLERY</p><h2 class="text-3xl font-bold text-gray-900">Actual Site Photos</h2></div>
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=700&q=85" class="rounded-2xl h-56 w-full object-cover">
      <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=700&q=85" class="rounded-2xl h-56 w-full object-cover">
      <img src="https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=700&q=85" class="rounded-2xl h-56 w-full object-cover">
      <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=700&q=85" class="rounded-2xl h-56 w-full object-cover">
    </div>
  </section>

  <!-- GET IN TOUCH & CONSULTATION FORM (SCREENSHOT 2 & 3) -->
  <section id="contact" class="py-16 px-5 max-w-7xl mx-auto border-t border-gray-100">
    <div class="grid lg:grid-cols-12 gap-12 items-start">
      <div class="lg:col-span-6">
        <p class="text-[#b91c1c] text-xs sm:text-sm font-semibold uppercase tracking-[0.22em] mb-3">GET IN TOUCH</p>
        <h2 class="text-4xl sm:text-[44px] font-bold text-gray-900 leading-[1.18] mb-5">Let's Find Your<br>Dream Home</h2>
        <p class="text-gray-500 text-base sm:text-[17px] leading-[1.75] mb-10">Reach out to our team of experts for personalised assistance with finding your perfect luxury property.</p>

        <div class="space-y-8">
          <div class="flex items-start space-x-5">
            <div class="w-14 h-14 rounded-2xl nexus-icon-box flex items-center justify-center flex-shrink-0">
              <svg class="w-8 h-8 text-[#b91c1c]" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 21c-4.5-4.5-7-8.2-7-11.5a7 7 0 1114 0c0 3.3-2.5 7-7 11.5z"/><circle cx="12" cy="9.5" r="2.8" stroke="currentColor" stroke-width="2.2"/></svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">Head Office</h3>
              <p class="text-gray-500 text-base leading-relaxed mb-3">{{ADDRESS}}</p>
              <h4 class="text-lg font-bold text-gray-900 mb-1">Our Branches</h4>
              <p class="text-gray-500 text-base">Nangloi, Pahladpur, Dwarka</p>
            </div>
          </div>

          <div class="flex items-start space-x-5">
            <div class="w-14 h-14 rounded-2xl nexus-icon-box flex items-center justify-center flex-shrink-0">
              <i class="fa-solid fa-phone-volume text-2xl text-[#b91c1c]"></i>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">Phone</h3>
              <a href="tel:{{PHONE}}" class="text-gray-500 hover:text-[#b91c1c] text-base transition">{{PHONE}}</a>
            </div>
          </div>

          <div class="flex items-start space-x-5">
            <div class="w-14 h-14 rounded-2xl nexus-icon-box flex items-center justify-center flex-shrink-0">
              <i class="fa-regular fa-envelope text-2xl text-[#b91c1c]"></i>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">Email</h3>
              <a href="mailto:{{EMAIL}}" class="text-gray-500 hover:text-[#b91c1c] text-base break-all transition">{{EMAIL}}</a>
            </div>
          </div>
        </div>
      </div>

      <!-- CONSULTATION FORM -->
      <div class="lg:col-span-6">
        <div class="bg-white rounded-3xl shadow-[0_10px_40px_rgba(0,0,0,0.08)] border border-gray-100 p-6 sm:p-10">
          <h3 class="text-2xl sm:text-[26px] font-bold text-gray-900 mb-6">Book a Free Consultation</h3>
          <form onsubmit="event.preventDefault(); alert('Thank you! Our team at {{BUSINESS_NAME}} will contact you shortly.');" class="space-y-4">
            <input type="text" required placeholder="Your Full Name" class="w-full bg-white border border-gray-200 rounded-xl px-4 py-4 text-gray-800 text-sm focus:outline-none focus:border-[#b91c1c]">
            <input type="email" required placeholder="Email Address" class="w-full bg-white border border-gray-200 rounded-xl px-4 py-4 text-gray-800 text-sm focus:outline-none focus:border-[#b91c1c]">
            <input type="tel" required placeholder="Phone Number" class="w-full bg-white border border-gray-200 rounded-xl px-4 py-4 text-gray-800 text-sm focus:outline-none focus:border-[#b91c1c]">
            <select required class="w-full bg-white border border-gray-200 rounded-xl px-4 py-4 text-gray-700 text-sm focus:outline-none focus:border-[#b91c1c]">
              <option value="" disabled selected>Select Property Type</option>
              <option>Residential Plot (Srishti Greens)</option>
              <option>Luxury Villa / Independent House</option>
              <option>2 / 3 / 4 BHK Apartment</option>
              <option>Commercial Shop / Office Space</option>
            </select>
            <textarea rows="4" placeholder="Your Message" class="w-full bg-white border border-gray-200 rounded-xl px-4 py-4 text-gray-800 text-sm focus:outline-none focus:border-[#b91c1c]"></textarea>
            <button type="submit" class="w-full nexus-bg-red text-white font-semibold text-base py-4 rounded-xl shadow-md transition">Send Message</button>
          </form>
        </div>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="bg-gray-900 text-gray-300 py-12 px-5 mt-10">
    <div class="max-w-7xl mx-auto grid md:grid-cols-3 gap-8 pb-8 border-b border-gray-800">
      <div>
        <h4 class="text-xl font-bold text-white mb-2">{{BUSINESS_NAME}}</h4>
        <p class="text-xs text-gray-400 leading-relaxed">{{BUSINESS_NAME}} helps you find prime properties.</p>
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
      © 2026 <strong>{{BUSINESS_NAME}}</strong>. All Rights Reserved. | Address: {{ADDRESS}} | Phone: {{PHONE}} | Email: {{EMAIL}}
    </div>
  </footer>

  <!-- FIXED BOTTOM APP BAR -->
  <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-2.5 px-2 z-50 shadow-[0_-4px_20px_rgba(0,0,0,0.05)]">
    <div class="max-w-md mx-auto grid grid-cols-5 text-center">
      <a href="#home" class="flex flex-col items-center justify-center text-[#b91c1c]"><i class="fa-solid fa-house text-lg mb-1"></i><span class="text-[11px] font-medium">Home</span></a>
      <a href="#properties" class="flex flex-col items-center justify-center text-gray-800 hover:text-[#b91c1c] transition"><i class="fa-solid fa-building text-lg mb-1"></i><span class="text-[11px] font-medium">Properties</span></a>
      <a href="#about" class="flex flex-col items-center justify-center text-gray-800 hover:text-[#b91c1c] transition"><i class="fa-solid fa-user text-lg mb-1"></i><span class="text-[11px] font-medium">About</span></a>
      <a href="#gallery" class="flex flex-col items-center justify-center text-gray-800 hover:text-[#b91c1c] transition"><i class="fa-regular fa-image text-lg mb-1"></i><span class="text-[11px] font-medium">Gallery</span></a>
      <a href="#contact" class="flex flex-col items-center justify-center text-gray-800 hover:text-[#b91c1c] transition"><i class="fa-solid fa-phone text-lg mb-1"></i><span class="text-[11px] font-medium">Contact</span></a>
    </div>
  </nav>

  <!-- LOGIN MODAL -->
  <div id="loginModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white text-gray-900 w-full max-w-md p-8 rounded-3xl shadow-2xl relative">
      <button onclick="closeModal('loginModal')" class="absolute top-5 right-5 text-gray-400 hover:text-gray-900 text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-bold mb-1">Welcome to {{BUSINESS_NAME}}</h3>
      <p class="text-xs text-gray-500 mb-6">Sign in or register to view property brochures</p>
      <form onsubmit="event.preventDefault(); alert('Logged in successfully!'); closeModal('loginModal');" class="space-y-4 text-sm">
        <input type="email" required placeholder="Email Address" class="w-full border border-gray-200 rounded-xl px-4 py-3.5 focus:outline-none focus:border-[#b91c1c]">
        <input type="password" required placeholder="Password" class="w-full border border-gray-200 rounded-xl px-4 py-3.5 focus:outline-none focus:border-[#b91c1c]">
        <button type="submit" class="w-full nexus-bg-red text-white font-semibold py-3.5 rounded-xl shadow-md">Continue</button>
      </form>
    </div>
  </div>

  <script>
    function toggleMobileMenu() { document.getElementById('mobileMenu').classList.toggle('hidden'); }
    function openModal(id) { document.getElementById(id).classList.add('modal-active'); }
    function closeModal(id) { document.getElementById(id).classList.remove('modal-active'); }

    let currentSlide = 0;
    const slides = document.querySelectorAll('.hero-slide');
    function changeSlide(step) {
      slides[currentSlide].style.opacity = '0';
      currentSlide = (currentSlide + step + slides.length) % slides.length;
      slides[currentSlide].style.opacity = '1';
    }
    setInterval(() => changeSlide(1), 4500);
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
        "🏠 *Clean NexusProperty Clone Bot*\n\n"
        "Ye bilkul asli `nexusproperty.in` jaisi clean white website banayega bina kisi cursor circle ke.\n\n"
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
            "`Name: Business Name`\n"
            "`Phone: +91 9876543210`\n"
            "`Email: contact@heoo.in`\n"
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
            f"✅ *Clean NexusProperty Clone Ready (No Cursor Circle)*\n\n"
            f"🏠 *Name:* {data['name']}\n"
            f"📞 *Phone:* {data['phone']}\n"
            f"📧 *Email:* {data['email']}\n"
            f"📍 *Head Office:* {data['address']}"
        ),
        parse_mode="Markdown"
    )


app = Flask(__name__)

@app.route('/')
def health():
    return "Clean NexusProperty Clone Bot Live 24/7"

if __name__ == "__main__":
    threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    ).start()
    try:
        bot.remove_webhook()
    except Exception:
        pass
    bot.infinity_polling(timeout=20, long_polling_timeout=20)
