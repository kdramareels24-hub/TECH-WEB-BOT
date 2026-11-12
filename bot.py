import os
import re
import io
import json
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN)

STATE_FILE = "tech_template_counter.json"
state_lock = threading.Lock()

def get_next_template_index():
    """Returns 0 to 9 strictly in 1 -> 2 -> 3 ... -> 10 sequence."""
    with state_lock:
        idx = 0
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    data = json.load(f)
                    idx = int(data.get("current_index", 0))
            except Exception:
                idx = 0
        current = idx % 10
        next_idx = (current + 1) % 10
        try:
            with open(STATE_FILE, "w") as f:
                json.dump({"current_index": next_idx}, f)
        except Exception:
            pass
        return current

def set_template_index(num_1_to_10):
    with state_lock:
        idx = (max(1, min(10, num_1_to_10)) - 1) % 10
        try:
            with open(STATE_FILE, "w") as f:
                json.dump({"current_index": idx}, f)
        except Exception:
            pass
        return idx

# ==============================================================================
# 10 DISTINCT TECH & SOFTWARE INTERFACES (WHITE THEME + GIANT HD TECH PHOTOS)
# ==============================================================================
TEMPLATES_DATA = [
    # 1. CYBER BLUE & SLATE
    {
        "id": 1,
        "theme_name": "Enterprise Cyber Blue & Slate",
        "font_name": "Plus Jakarta Sans",
        "font_url": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
        "accent": "blue-600",
        "accent_hover": "blue-700",
        "accent_light": "blue-50",
        "accent_text": "blue-600",
        "badge_bg": "blue-100",
        "badge_text": "blue-800",
        "dark_bg": "slate-900",
        "hero_style": "split",
        "card_radius": "rounded-3xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-connections-41662-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85", "NextGen FinTech Core Banking API", "v2.4 Staging", "78%", "Microservices Architecture & Load Testing Active"),
            ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85", "Multi-Cloud Kubernetes Migration", "AWS + Azure", "86%", "Zero-Downtime Cluster Sync & UAT Verification"),
            ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85", "AI Predictive Supply-Chain ERP", "Enterprise SaaS", "62%", "Neural Model Training & Dashboard Integration")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85", "OmniPay Institutional Gateway", "99.99% Uptime", "Live High-Frequency Payment Processing Platform"),
            ("https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1000&q=85", "MedCore Hospital Cloud ERP", "450+ Hospitals", "End-to-End Patient & Inventory Cloud Suite"),
            ("https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1000&q=85", "Sentinel Zero-Trust Security SOC", "24/7 Active Shield", "Enterprise Threat Detection & Firewall Grid")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85", "Full-Stack Software Engineers", "180+ React, Node.js, Python & Go Developers"),
            ("https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=900&q=85", "Cloud & DevOps Architects", "Kubernetes, Docker & CI/CD Pipeline Specialists"),
            ("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85", "Data Center Hardware Engineers", "Dedicated Bare-Metal Server & Fiber Ops Team"),
            ("https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=85", "Cybersecurity & QA Auditors", "Automated Penetration Testing & ISO Compliance")
        ]
    },

    # 2. QUANTUM INDIGO & OBSIDIAN
    {
        "id": 2,
        "theme_name": "Quantum Indigo & Deep Obsidian",
        "font_name": "Outfit",
        "font_url": "https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap",
        "accent": "indigo-600",
        "accent_hover": "indigo-700",
        "accent_light": "indigo-50",
        "accent_text": "indigo-600",
        "badge_bg": "indigo-100",
        "badge_text": "indigo-800",
        "dark_bg": "slate-950",
        "hero_style": "centered",
        "card_radius": "rounded-2xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-futuristic-hud-scifi-interface-41761-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1000&q=85", "Quantum Guard Encryption Engine", "Beta v3.1", "81%", "End-to-End Enterprise Key Exchange Rollout"),
            ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85", "Nexus Global Logistics CRM", "Multi-Tenant", "69%", "Real-Time Fleet Telemetry API Integration"),
            ("https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85", "HyperScale E-Commerce Core", "High-Concurrency", "74%", "Distributed Redis Caching & Checkout Engine")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1000&q=85", "Vertex Enterprise HRMS Suite", "1.2M+ Active Users", "Automated Payroll & Workforce Analytics Cloud"),
            ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85", "AlphaTrade Algorithmic Terminal", "Sub-ms Latency", "Real-Time Market Analytics & Execution Platform"),
            ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85", "Tier-IV Cloud Storage Grid", "50+ Petabytes", "Redundant Enterprise Backup & Disaster Recovery")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=900&q=85", "AI & Machine Learning Scientists", "Custom LLM & Computer Vision Research Unit"),
            ("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85", "Enterprise Backend Squad", "High-Throughput Java, Rust & Python Systems"),
            ("https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=85", "UI/UX & Product Designers", "Design Systems & Interactive Web Interfaces"),
            ("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85", "24/7 Site Reliability Engineers", "Zero-Downtime Server Monitoring & Incident Desk")
        ]
    },

    # 3. FINTECH EMERALD & ZINC
    {
        "id": 3,
        "theme_name": "FinTech Emerald & Modern Zinc",
        "font_name": "Manrope",
        "font_url": "https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap",
        "accent": "emerald-600",
        "accent_hover": "emerald-700",
        "accent_light": "emerald-50",
        "accent_text": "emerald-600",
        "badge_bg": "emerald-100",
        "badge_text": "emerald-800",
        "dark_bg": "zinc-900",
        "hero_style": "showcase",
        "card_radius": "rounded-3xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-connections-41662-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85", "GreenLedger Automated Tax ERP", "Release Candidate", "88%", "GST/VAT API Reconciliation & Audit Engine"),
            ("https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85", "Cross-Border Settlement Switch", "ISO-20022 Ready", "71%", "Smart Routing & Fraud Scoring Pipeline"),
            ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85", "Hybrid Cloud Data Warehouse", "Snowflake + AWS", "65%", "Real-Time BI Ingestion & Analytics Nodes")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85", "PayPulse Merchant SuperApp", "500K+ Merchants", "Instant QR, POS & Invoicing Ecosystem"),
            ("https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1000&q=85", "VaultX Biometric Identity Cloud", "SOC-2 Type II", "Automated eKYC & Document Verification API"),
            ("https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1000&q=85", "AgriChain Commodity Exchange", "Pan-India Live", "B2B Procurement & Cold-Storage Tracking ERP")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85", "FinTech Systems Engineers", "PCI-DSS Compliant Banking Software Team"),
            ("https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=85", "Mobile App Engineering Unit", "Native iOS, Kotlin & Flutter Specialists"),
            ("https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=900&q=85", "Database & Big Data Architects", "PostgreSQL, MongoDB & Kafka Cluster Leads"),
            ("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85", "Network Infrastructure Crew", "Dedicated Lease-Line & Hardware Security Ops")
        ]
    },

    # 4. AI VIOLET & DARK SLATE
    {
        "id": 4,
        "theme_name": "Neural AI Violet & Dark Slate",
        "font_name": "Space Grotesk",
        "font_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap",
        "accent": "violet-600",
        "accent_hover": "violet-700",
        "accent_light": "violet-50",
        "accent_text": "violet-600",
        "badge_bg": "violet-100",
        "badge_text": "violet-800",
        "dark_bg": "slate-950",
        "hero_style": "split",
        "card_radius": "rounded-2xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-futuristic-hud-scifi-interface-41761-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1000&q=85", "Cortex Conversational AI Agent", "LLM Fine-Tuning", "83%", "Multilingual Voice & Chat Automation Pipeline"),
            ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85", "GPU Compute Cluster Expansion", "H100 Server Nodes", "67%", "High-Density Liquid-Cooled Rack Integration"),
            ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85", "VisionQC Industrial Defect Scanner", "Edge AI", "75%", "Real-Time Assembly Line Camera Integration")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1000&q=85", "Synapse Enterprise BI Cloud", "Fortune-500 Ready", "Automated Executive Reporting & Forecasting"),
            ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85", "OmniDesk Customer Support CRM", "10M+ Tickets/Mo", "AI-Powered Omnichannel Ticketing Platform"),
            ("https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1000&q=85", "CloudFlow DevOps Automation", "Zero-Touch CI/CD", "Automated Container Security & Deployment Hub")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=900&q=85", "Deep Learning & NLP Researchers", "PyTorch, TensorFlow & RAG Pipeline Experts"),
            ("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85", "Core Platform Software Team", "200+ Senior Full-Stack & Cloud Developers"),
            ("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85", "Server Room & Cluster Technicians", "High-Speed InfiniBand & GPU Rack Engineers"),
            ("https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=85", "Enterprise Solutions Architects", "Custom Client Integration & Technical Delivery")
        ]
    },

    # 5. CLOUD CYAN & NAVY
    {
        "id": 5,
        "theme_name": "Cloud Native Cyan & Deep Navy",
        "font_name": "Urbanist",
        "font_url": "https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700;800&display=swap",
        "accent": "cyan-600",
        "accent_hover": "cyan-700",
        "accent_light": "cyan-50",
        "accent_text": "cyan-600",
        "badge_bg": "cyan-100",
        "badge_text": "cyan-900",
        "dark_bg": "slate-900",
        "hero_style": "centered",
        "card_radius": "rounded-3xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-connections-41662-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85", "SkyGrid Edge CDN Deployment", "18 Regional PoPs", "79%", "Low-Latency Fiber Routing & Edge Caching"),
            ("https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85", "AeroERP Aviation Maintenance", "Enterprise Cloud", "64%", "Fleet Spare-Parts & Compliance Tracking Module"),
            ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85", "SmartCity IoT Telemetry Hub", "MQTT + TimeSeries", "85%", "Real-Time Sensor Grid & Command Dashboard")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85", "CloudVault Enterprise Backup", "ISO-27001 Certified", "Automated Immutable Storage & Ransomware Shield"),
            ("https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1000&q=85", "EduSphere University LMS", "300+ Campuses", "Virtual Classrooms, Exam & ERP Management"),
            ("https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1000&q=85", "NetPulse SD-WAN Controller", "99.999% SLA", "Centralized Corporate Branch Network Routing")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85", "Cloud Infrastructure Engineers", "AWS, Google Cloud & Bare-Metal Specialists"),
            ("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85", "Agile Software Development Squad", "Scrum-Certified Full-Stack Engineering Team"),
            ("https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=900&q=85", "API & Microservices Architects", "GraphQL, gRPC & High-Volume Event Streams"),
            ("https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=85", "24/7 Technical Support & NOC", "Dedicated Client SLA & Live Monitoring Team")
        ]
    },

    # 6. ENTERPRISE CRIMSON & CHARCOAL
    {
        "id": 6,
        "theme_name": "RedHat Crimson & Enterprise Charcoal",
        "font_name": "DM Sans",
        "font_url": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap",
        "accent": "rose-600",
        "accent_hover": "rose-700",
        "accent_light": "rose-50",
        "accent_text": "rose-600",
        "badge_bg": "rose-100",
        "badge_text": "rose-800",
        "dark_bg": "neutral-950",
        "hero_style": "showcase",
        "card_radius": "rounded-2xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-futuristic-hud-scifi-interface-41761-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1000&q=85", "RedShield DDoS Mitigation Grid", "v4.0 Core", "82%", "Anycast BGP Scrubbing & AI Traffic Filtering"),
            ("https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85", "AutoManufacture MES Platform", "Industry 4.0", "73%", "PLC Assembly Line Telemetry & ERP Sync"),
            ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85", "RetailX Omni-Channel POS Cloud", "Multi-Store", "68%", "Real-Time Barcode Inventory & GST Billing")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85", "Apex Linux Enterprise Cloud", "10,000+ VMs", "High-Availability Virtualization & Container Grid"),
            ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85", "FinCore NBFC Loan Management", "RBI-Compliant", "Automated Loan Origination, Credit & EMI Suite"),
            ("https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1000&q=85", "FleetTrack GPS Logistics Cloud", "85,000+ Vehicles", "Live Route Optimization & Fuel Analytics Portal")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85", "Enterprise Linux & Kernel Devs", "High-Performance Systems & Security Engineers"),
            ("https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=900&q=85", "Offensive Security & Red Team", " Ethical Hackers & Vulnerability Researchers"),
            ("https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=85", "Frontend & WebGL Engineers", "Next.js, TypeScript & High-Speed Dashboards"),
            ("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85", "Data Center Operations Force", "24/7 Power, Cooling & Fiber Rack Management")
        ]
    },

    # 7. NEURAL TEAL & GRAPHITE
    {
        "id": 7,
        "theme_name": "Neural Teal & Titanium Graphite",
        "font_name": "Lexend",
        "font_url": "https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700;800&display=swap",
        "accent": "teal-600",
        "accent_hover": "teal-700",
        "accent_light": "teal-50",
        "accent_text": "teal-600",
        "badge_bg": "teal-100",
        "badge_text": "teal-800",
        "dark_bg": "slate-900",
        "hero_style": "split",
        "card_radius": "rounded-3xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-connections-41662-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85", "BioMed Diagnostic AI Cloud", "HIPAA Compliant", "77%", "Automated Radiology & Lab Report Analytics"),
            ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85", "Zero-Latency API Gateway v3", "Global Mesh", "84%", "Rust-Based Proxy & Rate-Limiting Cluster"),
            ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85", "PropTech Real-Estate CRM", "Enterprise SaaS", "61%", "3D Virtual Tour & Automated Lead Scoring")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1000&q=85", "LogiCore Warehouse Automation", "320+ Fulfillment Hubs", "Barcode, RFID & Automated Picking Software"),
            ("https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1000&q=85", "TalentSync Enterprise ATS", "Global HR Tech", "AI Resume Parsing & Onboarding Platform"),
            ("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1000&q=85", "CyberHawk SIEM Analytics", "SOC-2 Certified", "Real-Time Log Correlation & Intrusion Alerting")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85", "Senior Software Architects", "Microservices, Event-Driven & Serverless Leads"),
            ("https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=85", "Quality Assurance & SDET Crew", "Automated Selenium, Cypress & Load Testing"),
            ("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85", "Cloud Security & IAM Team", "Zero-Trust Network & Encryption Specialists"),
            ("https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=900&q=85", "Product & Agile Delivery Leads", "On-Time Sprint Execution & Client Success")
        ]
    },

    # 8. SILICON AMBER & SLATE
    {
        "id": 8,
        "theme_name": "Silicon Valley Amber & Dark Slate",
        "font_name": "Montserrat",
        "font_url": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap",
        "accent": "amber-600",
        "accent_hover": "amber-700",
        "accent_light": "amber-50",
        "accent_text": "amber-600",
        "badge_bg": "amber-100",
        "badge_text": "amber-900",
        "dark_bg": "slate-950",
        "hero_style": "centered",
        "card_radius": "rounded-2xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-futuristic-hud-scifi-interface-41761-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85", "Solaris Energy Grid IoT Cloud", "Smart Metering", "76%", "Real-Time Substation Telemetry & Analytics"),
            ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85", "GoldStandard ERP Billing Core", "v5.2 Rollout", "89%", "Multi-Currency Invoicing & Ledger Automation"),
            ("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1000&q=85", "NeuralVoice Call Center AI", "Low-Latency SIP", "63%", "Automated Customer Verification & Routing")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85", "PrimeCommerce B2B Wholesale", "2.5M+ SKUs", "Enterprise Distributor & Dealer Ordering Portal"),
            ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85", "TitanCloud Bare-Metal Hosting", "Tier-III DC", "Dedicated Enterprise Servers & Private VPC"),
            ("https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1000&q=85", "AuthShield Single Sign-On", "Zero-Trust MFA", "Enterprise Identity & Access Management Suite")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85", "Full-Stack Product Engineers", "TypeScript, Python, Go & Cloud-Native Team"),
            ("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85", "Server & Fiber Optics Engineers", "High-Speed Datacenter Switching & Cabling"),
            ("https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=900&q=85", "Data Engineering & BI Team", "Apache Spark, Airflow & Real-Time Dashboards"),
            ("https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=85", "Client Onboarding & Support", "24/7 Dedicated Enterprise Account Engineers")
        ]
    },

    # 9. AZURE SKY & MIDNIGHT
    {
        "id": 9,
        "theme_name": "Azure Cloud & Midnight Steel",
        "font_name": "Inter",
        "font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
        "accent": "sky-600",
        "accent_hover": "sky-700",
        "accent_light": "sky-50",
        "accent_text": "sky-600",
        "badge_bg": "sky-100",
        "badge_text": "sky-900",
        "dark_bg": "slate-950",
        "hero_style": "showcase",
        "card_radius": "rounded-3xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-connections-41662-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85", "AzureMesh Global VPN Core", "WireGuard Enterprise", "80%", "Zero-Trust Remote Workforce Network Rollout"),
            ("https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85", "SmartRetail AI Inventory Engine", "Demand Forecasting", "72%", "Automated Warehouse Replenishment Pipeline"),
            ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85", "InsureTech Claims Portal", "OCR + Workflow", "66%", "Instant Document Scanning & Settlement API")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1000&q=85", "Horizon Enterprise ERP Cloud", "600+ Enterprises", "Unified Finance, Inventory & Supply Chain Suite"),
            ("https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1000&q=85", "ConnectX Unified Comms API", "Voice, Video & SMS", "High-Throughput CPaaS Messaging Infrastructure"),
            ("https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1000&q=85", "Fortress Cloud WAF & Shield", "ISO-27017", "Automated Bot Mitigation & API Security Gateway")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85", "220+ Certified Software Engineers", "Dedicated Enterprise Web, Cloud & Mobile Teams"),
            ("https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=900&q=85", "Cloud Migration & SRE Architects", "99.99% Uptime Guarantee & Auto-Scaling Ops"),
            ("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85", "Datacenter Systems Administrators", "Linux, VMware & SAN Storage Array Experts"),
            ("https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=85", "QA Automation & Security Lab", "Continuous Integration & Compliance Auditing")
        ]
    },

    # 10. MATRIX PURPLE & TITANIUM
    {
        "id": 10,
        "theme_name": "HyperScale Purple & Titanium",
        "font_name": "Plus Jakarta Sans",
        "font_url": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
        "accent": "purple-600",
        "accent_hover": "purple-700",
        "accent_light": "purple-50",
        "accent_text": "purple-600",
        "badge_bg": "purple-100",
        "badge_text": "purple-900",
        "dark_bg": "zinc-950",
        "hero_style": "split",
        "card_radius": "rounded-2xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-futuristic-hud-scifi-interface-41761-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1000&q=85", "Orion Enterprise AI Copilot", "Private LLM", "85%", "On-Premise Corporate Document Search & RAG"),
            ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1000&q=85", "Titanium Core Banking Ledger", "High-TPS Cluster", "74%", "Distributed SQL & Real-Time Audit Logging"),
            ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1000&q=85", "Vanguard Supply-Chain Portal", "B2B Vendor Cloud", "67%", "Automated e-Procurement & Invoice Matching")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=85", "PulseAnalytics Enterprise BI", "10B+ Events/Day", "Real-Time Telemetry & Executive KPI Platform"),
            ("https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1000&q=85", "Aegis Cyber Defense Matrix", "CERT-Aligned", "Automated Endpoint Detection & Cloud Firewall"),
            ("https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1000&q=85", "Nexus Global ERP Ecosystem", "Turnkey SaaS", "Complete HR, Finance, CRM & Inventory Cloud")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=85", "Principal Software Engineers", "High-Scale Distributed Systems & Cloud Team"),
            ("https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=900&q=85", "AI & Data Science Directorate", "Predictive Modeling & Neural Automation Crew"),
            ("https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85", "Datacenter & Cloud Ops Crew", "24/7 Server Rack, Fiber & Kubernetes Management"),
            ("https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=85", "Enterprise QA & Security Desk", "ISO-27001 & SOC-2 Compliance Engineering")
        ]
    }
]


def build_hero_section(t, name, phone, email, address):
    """Generates 3 structurally distinct Tech Hero layouts across the 10 templates."""
    ac = t["accent"]
    ach = t["accent_hover"]
    rad = t["card_radius"]

    if t["hero_style"] == "centered":
        return f"""
  <!-- HERO VARIANT B: CENTERED ENTERPRISE CLOUD & AI HERO -->
  <section class="relative min-h-[92vh] flex items-center justify-center overflow-hidden bg-{t['dark_bg']}">
    <div class="absolute inset-0 z-0">
      <img src="{t['hero_img']}" alt="Tech Infrastructure" class="w-full h-full object-cover animate-live-bg opacity-45">
      <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-60">
        <source src="{t['video_url']}" type="video/mp4">
      </video>
    </div>
    <div class="absolute inset-0 bg-gradient-to-b from-black/85 via-black/70 to-black/90 z-10"></div>

    <div class="relative z-20 max-w-6xl mx-auto px-6 py-24 text-center text-white">
      <div class="inline-flex items-center gap-2.5 bg-{ac} text-white px-5 py-2 rounded-full text-xs font-extrabold uppercase tracking-widest mb-8 shadow-xl">
        <span class="w-2.5 h-2.5 rounded-full bg-white animate-ping"></span>
        <span>ISO/IEC 27001 & SOC-2 Certified IT & Software Company</span>
      </div>
      <h1 class="text-5xl sm:text-7xl lg:text-8xl font-black tracking-tight uppercase leading-none mb-6 drop-shadow-lg">
        {name}
      </h1>
      <div class="text-xl sm:text-3xl font-bold text-gray-200 mb-6 min-h-[42px]">
        <span class="text-{ac} bg-white px-3 py-1 rounded mr-2">SOLUTIONS:</span>
        <span id="typewriter" class="typing-cursor text-white"></span>
      </div>
      <p class="text-base sm:text-xl text-gray-300 max-w-3xl mx-auto mb-10 leading-relaxed">
        Engineering custom enterprise software, scalable cloud infrastructure, AI automation pipelines, and mission-critical web & mobile platforms with 250+ senior software developers at <strong>{address}</strong>.
      </p>
      <div class="flex flex-wrap justify-center gap-5">
        <a href="#ongoing" class="bg-{ac} hover:bg-{ach} text-white font-extrabold px-10 py-5 {rad} text-base shadow-2xl transition transform hover:-translate-y-1">
          <i class="fa-solid fa-code-branch mr-2"></i> View Live Software Deployments
        </a>
        <button onclick="openModal('signupModal')" class="bg-white hover:bg-gray-100 text-slate-950 font-extrabold px-10 py-5 {rad} text-base shadow-2xl transition transform hover:-translate-y-1">
          <i class="fa-solid fa-laptop-code mr-2 text-{ac}"></i> Client Portal & Demo
        </button>
      </div>
    </div>
  </section>"""

    elif t["hero_style"] == "showcase":
        return f"""
  <!-- HERO VARIANT C: DUAL-FRAME SAAS & DATACENTER LIVE SHOWCASE HERO -->
  <section class="relative min-h-[92vh] flex items-center overflow-hidden bg-{t['dark_bg']} py-20 px-6">
    <div class="absolute inset-0 z-0">
      <img src="{t['hero_img']}" alt="Software Engineering" class="w-full h-full object-cover animate-live-bg opacity-35">
      <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-55">
        <source src="{t['video_url']}" type="video/mp4">
      </video>
    </div>
    <div class="absolute inset-0 bg-gradient-to-r from-black/90 via-black/75 to-black/50 z-10"></div>

    <div class="relative z-20 max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7 text-white">
        <span class="inline-block bg-{ac} text-white text-xs font-black uppercase tracking-widest px-4 py-2 rounded-lg mb-6">
          Enterprise Software & Cloud Engineering
        </span>
        <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black uppercase tracking-tight leading-none mb-6">
          {name}
        </h1>
        <div class="text-xl sm:text-2xl font-bold text-gray-200 mb-6">
          <span>Core Stack: </span>
          <span id="typewriter" class="text-white underline decoration-{ac} typing-cursor"></span>
        </div>
        <p class="text-base sm:text-lg text-gray-300 mb-8 leading-relaxed">
          From high-concurrency FinTech APIs and custom ERP software to multi-cloud Kubernetes clusters and AI automation. Built for 99.99% uptime and enterprise security.
        </p>
        <div class="flex flex-wrap gap-4">
          <a href="#completed" class="bg-{ac} hover:bg-{ach} text-white font-extrabold px-8 py-4 {rad} shadow-xl transition">
            <i class="fa-solid fa-server mr-2"></i> Delivered Platforms
          </a>
          <a href="#workforce" class="bg-white text-slate-900 hover:bg-gray-100 font-extrabold px-8 py-4 {rad} shadow-xl transition">
            <i class="fa-solid fa-users-viewfinder mr-2 text-{ac}"></i> Meet Our Engineers
          </a>
        </div>
      </div>

      <div class="lg:col-span-5">
        <div class="bg-white p-3 {rad} shadow-2xl">
          <div class="relative h-[420px] overflow-hidden {rad}">
            <img src="{t['ongoing_imgs'][0][0]}" alt="Live Production Code" class="w-full h-full object-cover animate-live-bg">
            <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-transparent to-transparent flex flex-col justify-end p-6 text-white">
              <span class="bg-{ac} text-white text-xs font-extrabold uppercase px-3 py-1 rounded w-max mb-2">Live Production Cluster</span>
              <h3 class="text-2xl font-black">{name} — Cloud Core</h3>
              <p class="text-xs text-gray-200 mt-1">24/7 DevOps & Automated CI/CD Pipeline Active • {phone}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>"""

    else:
        return f"""
  <!-- HERO VARIANT A: SPLIT TECH HERO + PROJECT CONSULTATION TERMINAL -->
  <section class="relative min-h-[92vh] flex items-center justify-center overflow-hidden bg-{t['dark_bg']}">
    <div class="absolute inset-0 z-0">
      <img src="{t['hero_img']}" alt="Tech Company" class="w-full h-full object-cover animate-live-bg opacity-45">
      <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-60">
        <source src="{t['video_url']}" type="video/mp4">
      </video>
    </div>
    <div class="absolute inset-0 bg-gradient-to-r from-black/90 via-black/75 to-black/40 z-10"></div>

    <div class="relative z-20 max-w-7xl mx-auto px-6 py-20 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-8 text-white">
        <div class="inline-flex items-center gap-2 bg-{ac} text-white px-4 py-1.5 rounded-full text-xs font-extrabold uppercase tracking-wider mb-6 shadow-lg">
          <span class="w-2 h-2 rounded-full bg-white animate-ping"></span>
          <span>Custom Software Development, Cloud & AI Solutions</span>
        </div>
        <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-none mb-6 uppercase">
          {name}
        </h1>
        <div class="text-xl sm:text-2xl md:text-3xl font-bold text-gray-200 mb-6 min-h-[40px]">
          <span>We Engineer: </span>
          <span id="typewriter" class="text-white typing-cursor"></span>
        </div>
        <p class="text-base md:text-lg text-gray-200 max-w-2xl mb-10 leading-relaxed">
          Delivering high-performance enterprise web applications, FinTech APIs, cloud data centers, and AI-driven business automation with 250+ full-stack software engineers and DevOps architects.
        </p>
        <div class="flex flex-wrap gap-4">
          <a href="#ongoing" class="bg-{ac} hover:bg-{ach} text-white font-extrabold px-8 py-4 {rad} shadow-xl transition transform hover:-translate-y-1 flex items-center">
            <i class="fa-solid fa-microchip mr-2.5 text-lg"></i> Active R&D & Cloud Projects
          </a>
          <a href="#contact" class="bg-white hover:bg-gray-100 text-slate-900 font-extrabold px-8 py-4 {rad} shadow-xl transition transform hover:-translate-y-1 flex items-center">
            <i class="fa-solid fa-phone-volume mr-2.5 text-{ac}"></i> {phone}
          </a>
        </div>
      </div>

      <div class="lg:col-span-4 bg-white text-slate-900 p-8 {rad} shadow-2xl border-t-8 border-{ac}">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-extrabold">Request Software Proposal</h3>
          <span class="bg-{t['badge_bg']} text-{t['badge_text']} text-xs font-bold px-2.5 py-1 rounded">Tech Desk</span>
        </div>
        <p class="text-xs text-slate-500 mb-6">Schedule a technical architecture consultation and cost estimate for your software or cloud project.</p>
        <form onsubmit="event.preventDefault(); alert('Thank you! Solutions Architect from {name} will contact you shortly.');" class="space-y-4 text-sm">
          <div>
            <label class="block text-xs font-bold uppercase text-slate-700 mb-1">Your Name / Organization</label>
            <input type="text" required placeholder="Enter full name" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none">
          </div>
          <div>
            <label class="block text-xs font-bold uppercase text-slate-700 mb-1">Work Phone Number</label>
            <input type="tel" required placeholder="+91 XXXXX XXXXX" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none">
          </div>
          <div>
            <label class="block text-xs font-bold uppercase text-slate-700 mb-1">Solution Category</label>
            <select class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 font-semibold">
              <option>Custom Enterprise ERP / SaaS</option>
              <option>Cloud Migration & DevOps Infrastructure</option>
              <option>AI Automation & Data Analytics</option>
              <option>Web & Mobile App Development</option>
            </select>
          </div>
          <button type="submit" class="w-full bg-{ac} hover:bg-{ach} text-white font-extrabold py-4 rounded-xl transition shadow-lg">
            Get Technical Estimate
          </button>
        </form>
      </div>
    </div>
  </section>"""


def generate_html_for_template(t, name, phone, email, address):
    ac = t["accent"]
    ach = t["accent_hover"]
    act = t["accent_text"]
    bbg = t["badge_bg"]
    btxt = t["badge_text"]
    dbg = t["dark_bg"]
    rad = t["card_radius"]

    hero_html = build_hero_section(t, name, phone, email, address)

    # Ongoing / In-Development Tech Projects (EXTRA LARGE h-[420px] IMAGES)
    ongoing_cards = ""
    for img_url, proj_title, stage_tag, pct, desc in t["ongoing_imgs"]:
        ongoing_cards += f"""
        <div class="bg-white {rad} overflow-hidden border border-gray-200 shadow-xl hover-lift">
          <div class="relative h-[420px] overflow-hidden">
            <img src="{img_url}" alt="{proj_title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-700">
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/20"></div>
            <span class="absolute top-5 left-5 bg-amber-400 text-slate-950 text-xs font-black uppercase px-4 py-1.5 rounded-full shadow-lg">
              <i class="fa-solid fa-arrows-rotate fa-spin mr-1.5"></i> In Active Development
            </span>
            <span class="absolute top-5 right-5 bg-white/95 text-slate-900 text-xs font-extrabold px-3.5 py-1.5 rounded-lg shadow">
              {stage_tag}
            </span>
            <div class="absolute bottom-5 left-5 right-5 text-white">
              <h3 class="text-2xl font-black leading-tight">{proj_title}</h3>
              <p class="text-xs text-gray-200 mt-1">{desc}</p>
            </div>
          </div>
          <div class="p-7">
            <div class="mb-2.5 flex justify-between items-center text-sm font-extrabold">
              <span class="text-slate-700">Sprint & Deployment Progress</span>
              <span class="text-{act} text-base">{pct} Completed</span>
            </div>
            <div class="w-full bg-gray-200 h-3.5 rounded-full overflow-hidden">
              <div class="bg-{ac} h-full rounded-full" style="width: {pct}"></div>
            </div>
            <div class="mt-5 pt-4 border-t border-gray-100 flex justify-between text-xs font-bold text-slate-500">
              <span><i class="fa-solid fa-code-commit text-{act} mr-1"></i> CI/CD Active</span>
              <span><i class="fa-solid fa-shield-check text-emerald-600 mr-1"></i> ISO-27001 Audited</span>
            </div>
          </div>
        </div>"""

    # Completed / Delivered Software Platforms (EXTRA LARGE h-[450px] IMAGES)
    completed_cards = ""
    for img_url, proj_title, metric_tag, subtitle in t["completed_imgs"]:
        completed_cards += f"""
        <div class="bg-white {rad} overflow-hidden border border-gray-200 shadow-xl hover-lift group">
          <div class="relative h-[450px] overflow-hidden">
            <img src="{img_url}" alt="{proj_title}" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">
            <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/15 to-transparent"></div>
            <span class="absolute top-5 left-5 bg-emerald-600 text-white text-xs font-black uppercase px-4 py-1.5 rounded-full shadow-lg">
              <i class="fa-solid fa-circle-check mr-1.5"></i> 100% Live In Production
            </span>
            <div class="absolute bottom-6 left-6 right-6 text-white">
              <span class="text-xs font-extrabold uppercase tracking-widest text-emerald-300 block mb-1">{subtitle}</span>
              <h3 class="text-2xl sm:text-3xl font-black">{proj_title}</h3>
            </div>
          </div>
          <div class="p-6 bg-white flex justify-between items-center text-xs font-extrabold text-slate-700">
            <span class="flex items-center"><i class="fa-solid fa-server text-{act} text-base mr-2"></i> Scale: {metric_tag}</span>
            <span class="bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full">Production Verified</span>
          </div>
        </div>"""

    # Software Engineers & Tech Workforce cards (EXTRA LARGE h-[390px] IMAGES)
    worker_cards = ""
    for img_url, role_title, role_desc in t["worker_imgs"]:
        worker_cards += f"""
        <div class="bg-white text-slate-900 {rad} overflow-hidden shadow-xl border border-gray-200 hover-lift group">
          <div class="relative h-[390px] overflow-hidden">
            <img src="{img_url}" alt="{role_title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
            <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-transparent to-transparent"></div>
            <div class="absolute bottom-5 left-5 right-5 text-white">
              <span class="bg-{ac} text-white text-[10px] font-black uppercase px-2.5 py-1 rounded">Verified Engineering Squad</span>
              <h4 class="font-black text-xl mt-2">{role_title}</h4>
              <p class="text-xs text-gray-200 mt-1">{role_desc}</p>
            </div>
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} | Enterprise Software, Cloud & IT Solutions</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="{t['font_url']}">
  <style>
    body {{ font-family: '{t['font_name']}', sans-serif; }}
    .modal-active {{ display: flex !important; }}
    @keyframes slowZoom {{
      0% {{ transform: scale(1); }}
      50% {{ transform: scale(1.12); }}
      100% {{ transform: scale(1); }}
    }}
    .animate-live-bg {{ animation: slowZoom 20s infinite ease-in-out; }}
    .hover-lift {{ transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1); }}
    .hover-lift:hover {{ transform: translateY(-8px); }}
    .typing-cursor::after {{ content: '|'; animation: blink 1s infinite; }}
    @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
  </style>
</head>
<body class="bg-white text-slate-900 antialiased selection:bg-{ac} selection:text-white">

  <!-- 1. TOP CORPORATE BAR -->
  <div class="bg-{dbg} text-slate-200 text-xs py-3 px-6 border-b border-slate-800">
    <div class="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-3">
      <div class="flex flex-wrap items-center gap-6">
        <a href="tel:{phone}" class="hover:text-white font-bold flex items-center">
          <i class="fa-solid fa-phone-volume text-{act} mr-2"></i> {phone}
        </a>
        <a href="mailto:{email}" class="hover:text-white font-bold flex items-center">
          <i class="fa-solid fa-envelope text-{act} mr-2"></i> {email}
        </a>
        <span class="hidden lg:flex items-center text-slate-300">
          <i class="fa-solid fa-location-dot text-{act} mr-2"></i> {address}
        </span>
      </div>
      <div class="flex items-center space-x-4">
        <span class="text-emerald-400 font-bold hidden sm:inline">
          <i class="fa-solid fa-shield-halved mr-1"></i> ISO 27001 & SOC-2 Certified IT Entity
        </span>
        <button onclick="openModal('loginModal')" class="bg-slate-800 hover:bg-slate-700 text-white px-3.5 py-1.5 rounded font-bold transition">Login</button>
        <button onclick="openModal('signupModal')" class="bg-{ac} hover:bg-{ach} text-white px-3.5 py-1.5 rounded font-bold transition">Sign Up</button>
      </div>
    </div>
  </div>

  <!-- 2. STICKY WHITE NAVIGATION -->
  <header class="bg-white/95 backdrop-blur-md sticky top-0 z-40 border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <a href="#" class="flex items-center space-x-3.5">
        <div class="w-12 h-12 {rad} bg-{ac} flex items-center justify-center text-white text-2xl shadow-lg">
          <i class="fa-solid fa-microchip"></i>
        </div>
        <div>
          <span class="text-xl md:text-2xl font-black tracking-tight text-slate-900 block leading-none">{name}</span>
          <span class="text-[11px] font-extrabold uppercase tracking-widest text-{act}">Software, Cloud & AI Technologies</span>
        </div>
      </a>

      <nav class="hidden xl:flex items-center space-x-8 text-sm font-extrabold text-slate-700">
        <a href="#about" class="hover:text-{act} transition">About Tech</a>
        <a href="#ongoing" class="hover:text-{act} transition">Active R&D / Beta</a>
        <a href="#completed" class="hover:text-{act} transition">Live Platforms</a>
        <a href="#workforce" class="hover:text-{act} transition">Our Engineers</a>
        <a href="#infrastructure" class="hover:text-{act} transition">Server Infra</a>
        <a href="#contact" class="hover:text-{act} transition">Contact Desk</a>
      </nav>

      <div class="flex items-center space-x-3">
        <button onclick="openModal('loginModal')" class="hidden sm:inline-flex items-center px-5 py-2.5 border-2 border-slate-900 text-slate-900 hover:bg-slate-900 hover:text-white rounded-xl text-xs font-extrabold uppercase transition">
          Log In
        </button>
        <button onclick="openModal('signupModal')" class="inline-flex items-center px-5 py-2.5 bg-{ac} hover:bg-{ach} text-white rounded-xl text-xs font-extrabold uppercase shadow-lg transition">
          Sign Up
        </button>
      </div>
    </div>
  </header>

  {hero_html}

  <!-- 4. TECH STATS BAR -->
  <section class="bg-{ac} text-white py-14 px-6 shadow-md">
    <div class="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
      <div>
        <div class="text-4xl md:text-6xl font-black mb-1">240+</div>
        <div class="text-xs uppercase font-extrabold tracking-widest opacity-90">Enterprise Platforms Live</div>
      </div>
      <div>
        <div class="text-4xl md:text-6xl font-black mb-1">99.99%</div>
        <div class="text-xs uppercase font-extrabold tracking-widest opacity-90">Cloud Server Uptime SLA</div>
      </div>
      <div>
        <div class="text-4xl md:text-6xl font-black mb-1">260+</div>
        <div class="text-xs uppercase font-extrabold tracking-widest opacity-90">Software & DevOps Engineers</div>
      </div>
      <div>
        <div class="text-4xl md:text-6xl font-black mb-1">100%</div>
        <div class="text-xs uppercase font-extrabold tracking-widest opacity-90">ISO-27001 Data Security</div>
      </div>
    </div>
  </section>

  <!-- 5. ABOUT US WITH EXTRA-LARGE IMAGES (h-[480px]) -->
  <section id="about" class="py-28 px-6 max-w-7xl mx-auto">
    <div class="grid lg:grid-cols-12 gap-14 items-center">
      <div class="lg:col-span-7 grid sm:grid-cols-2 gap-6">
        <div class="relative h-[480px] {rad} overflow-hidden shadow-2xl border border-gray-200">
          <img src="{t['about_imgs'][0]}" alt="Software Engineering Team" class="w-full h-full object-cover">
          <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/85 to-transparent p-6 text-white">
            <span class="bg-{ac} text-white text-xs font-extrabold px-3 py-1 rounded">R&D Engineering Center</span>
            <h4 class="text-xl font-black mt-2">Dedicated Full-Stack & Cloud Developers</h4>
          </div>
        </div>
        <div class="relative h-[480px] {rad} overflow-hidden shadow-2xl border border-gray-200 sm:mt-10">
          <img src="{t['about_imgs'][1]}" alt="Production Code Architecture" class="w-full h-full object-cover">
          <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/85 to-transparent p-6 text-white">
            <span class="bg-emerald-600 text-white text-xs font-extrabold px-3 py-1 rounded">Enterprise Architecture</span>
            <h4 class="text-xl font-black mt-2">High-Throughput Cloud & API Systems</h4>
          </div>
        </div>
      </div>

      <div class="lg:col-span-5">
        <span class="bg-{bbg} text-{btxt} font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          Registered IT & Software Company
        </span>
        <h2 class="text-3xl sm:text-5xl font-black text-slate-900 mt-5 mb-6 leading-tight">
          Architecting Scalable Software & Cloud Ecosystems
        </h2>
        <p class="text-slate-600 text-base leading-relaxed mb-6">
          <strong>{name}</strong> is a premier information technology, custom software development, and cloud engineering company headquartered at <strong>{address}</strong>. We build mission-critical SaaS platforms, enterprise ERP suites, FinTech payment systems, and AI automation pipelines.
        </p>
        <p class="text-slate-600 text-sm leading-relaxed mb-8">
          Our engineering floor operates with agile Scrum squads, DevOps Kubernetes architects, cybersecurity auditors, and 24/7 Network Operations Center (NOC) engineers ensuring zero-downtime digital transformation.
        </p>
        <div class="p-6 bg-gray-50 {rad} border border-gray-200 space-y-3 text-sm">
          <div><strong class="text-slate-900">Legal Tech Entity:</strong> {name}</div>
          <div><strong class="text-slate-900">Support Helpline:</strong> <a href="tel:{phone}" class="text-{act} font-extrabold">{phone}</a></div>
          <div><strong class="text-slate-900">Official Email:</strong> <a href="mailto:{email}" class="text-{act} font-extrabold">{email}</a></div>
          <div><strong class="text-slate-900">Registered Office:</strong> {address}</div>
        </div>
      </div>
    </div>
  </section>

  <!-- 6. GIANT ONGOING TECH PROJECTS (IN-DEVELOPMENT / STAGING - h-[420px] CARDS) -->
  <section id="ongoing" class="py-28 bg-gray-50 border-y border-gray-200 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="bg-amber-100 text-amber-900 font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          Live R&D & Staging Pipelines
        </span>
        <h2 class="text-4xl md:text-6xl font-black text-slate-900 mt-4">Ongoing Software & Cloud Deployments</h2>
        <p class="text-slate-600 text-base mt-3 max-w-3xl mx-auto">
          Real-time sprint progress of enterprise platforms, cloud migrations, and AI systems currently undergoing staging, load testing, and UAT rollout.
        </p>
      </div>

      <div class="grid lg:grid-cols-3 gap-10">
        {ongoing_cards}
      </div>
    </div>
  </section>

  <!-- 7. FULL-WIDTH PANORAMIC DATACENTER BANNER (h-[500px]) -->
  <section class="relative h-[500px] flex items-center justify-center overflow-hidden">
    <img src="{t['panorama_img']}" alt="Panoramic Server Infrastructure" class="absolute inset-0 w-full h-full object-cover animate-live-bg">
    <div class="absolute inset-0 bg-slate-950/80"></div>
    <div class="relative z-10 max-w-5xl mx-auto px-6 text-center text-white">
      <span class="bg-{ac} text-white text-xs font-black uppercase tracking-widest px-4 py-2 rounded-full">
        99.99% High-Availability Cloud Architecture
      </span>
      <h2 class="text-4xl sm:text-6xl font-black mt-6 mb-6 leading-tight">
        From System Architecture Blueprint To Global Cloud Production
      </h2>
      <p class="text-lg text-gray-200 mb-8 max-w-3xl mx-auto">
        Every software platform engineered by <strong>{name}</strong> passes automated penetration testing, multi-region load balancing, and AES-256 encryption compliance.
      </p>
      <a href="#contact" class="inline-block bg-white text-slate-950 hover:bg-gray-100 font-black px-10 py-4 {rad} shadow-2xl transition">
        Connect With Solutions Architect — {phone}
      </a>
    </div>
  </section>

  <!-- 8. GIANT COMPLETED PLATFORMS (LIVE IN PRODUCTION - h-[450px] CARDS) -->
  <section id="completed" class="py-28 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <span class="bg-emerald-100 text-emerald-900 font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
        Production Portfolio
      </span>
      <h2 class="text-4xl md:text-6xl font-black text-slate-900 mt-4">Completed & Live Software Platforms</h2>
      <p class="text-slate-600 text-base mt-3 max-w-3xl mx-auto">
        Explore our successfully deployed enterprise cloud portals, FinTech switches, ERP systems, and cybersecurity grids running 24/7.
      </p>
    </div>

    <div class="grid lg:grid-cols-3 gap-10">
      {completed_cards}
    </div>
  </section>

  <!-- 9. GIANT SOFTWARE ENGINEERS & DEVOPS WORKFORCE GALLERY (h-[390px] PORTRAITS) -->
  <section id="workforce" class="py-28 bg-gray-50 border-y border-gray-200 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="bg-{bbg} text-{btxt} font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          Our Engineering Force
        </span>
        <h2 class="text-4xl md:text-6xl font-black text-slate-900 mt-4">Our Software Developers, Architects & SRE Team</h2>
        <p class="text-slate-600 text-base mt-3 max-w-3xl mx-auto">
          Experienced full-stack developers, cloud DevOps specialists, data scientists, and hardware server engineers powering <strong>{name}</strong>.
        </p>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
        {worker_cards}
      </div>
    </div>
  </section>

  <!-- 10. SERVER INFRASTRUCTURE & AI LABS (LARGE VISUAL CARDS) -->
  <section id="infrastructure" class="py-28 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <span class="bg-{bbg} text-{btxt} font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
        Hardware & Cloud Stack
      </span>
      <h2 class="text-4xl md:text-5xl font-black text-slate-900 mt-4">Dedicated Data Centers, GPU Clusters & SOC Labs</h2>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      <div class="bg-white border border-gray-200 {rad} overflow-hidden shadow-lg hover-lift">
        <img src="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=900&q=85" class="w-full h-80 object-cover" alt="Server Racks">
        <div class="p-6">
          <h4 class="text-xl font-black text-slate-900 mb-2">High-Density Server Clusters</h4>
          <p class="text-sm text-slate-600">Tier-III & Tier-IV bare-metal server racks with redundant 100Gbps fiber uplinks and automated failover.</p>
        </div>
      </div>

      <div class="bg-white border border-gray-200 {rad} overflow-hidden shadow-lg hover-lift">
        <img src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=900&q=85" class="w-full h-80 object-cover" alt="Cybersecurity SOC">
        <div class="p-6">
          <h4 class="text-xl font-black text-slate-900 mb-2">24/7 Cybersecurity SOC Center</h4>
          <p class="text-sm text-slate-600">Real-time threat intelligence, zero-trust firewall monitoring, and automated DDoS scrubbing rooms.</p>
        </div>
      </div>

      <div class="bg-white border border-gray-200 {rad} overflow-hidden shadow-lg hover-lift">
        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=85" class="w-full h-80 object-cover" alt="AI Compute Lab">
        <div class="p-6">
          <h4 class="text-xl font-black text-slate-900 mb-2">AI & Cloud Telemetry Command</h4>
          <p class="text-sm text-slate-600">Dedicated GPU compute nodes for LLM fine-tuning, predictive analytics, and automated CI/CD testing.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 11. LEGAL ENTITY & STATUTORY VERIFICATION BLOCK -->
  <section class="py-20 bg-gray-50 border-t border-gray-200 px-6">
    <div class="max-w-5xl mx-auto bg-white border-2 border-slate-900 {rad} p-10 shadow-2xl">
      <div class="flex flex-wrap justify-between items-center gap-4 pb-6 mb-8 border-b border-gray-200">
        <div>
          <span class="text-xs font-extrabold uppercase tracking-widest text-{act}">Official Corporate IT Registry</span>
          <h3 class="text-3xl font-black text-slate-900">Verified Legal Entity Information</h3>
        </div>
        <span class="bg-emerald-100 text-emerald-800 text-xs font-black px-4 py-2 rounded-full">
          <i class="fa-solid fa-circle-check mr-1.5"></i> Active & Verified Tech Entity
        </span>
      </div>

      <div class="grid md:grid-cols-2 gap-6 text-base">
        <div class="p-5 bg-gray-50 rounded-2xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Registered Company Name</span>
          <span class="font-black text-slate-900 text-lg">{name}</span>
        </div>
        <div class="p-5 bg-gray-50 rounded-2xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Official Phone Number</span>
          <a href="tel:{phone}" class="font-black text-{act} text-lg hover:underline">{phone}</a>
        </div>
        <div class="p-5 bg-gray-50 rounded-2xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Official Corporate Email</span>
          <a href="mailto:{email}" class="font-black text-{act} text-lg hover:underline break-all">{email}</a>
        </div>
        <div class="p-5 bg-gray-50 rounded-2xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Registered Head Office Address</span>
          <span class="font-black text-slate-900">{address}</span>
        </div>
      </div>
    </div>
  </section>

  <!-- 12. FOOTER WITH PROMINENT NAME, ADDRESS, PHONE & EMAIL -->
  <footer id="contact" class="bg-{dbg} text-white pt-20 pb-12 px-6 border-t-8 border-{ac}">
    <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 pb-16 border-b border-slate-800">
      <div class="lg:col-span-5">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-11 h-11 rounded-xl bg-{ac} flex items-center justify-center text-white text-xl font-black">
            <i class="fa-solid fa-microchip"></i>
          </div>
          <span class="text-2xl font-black">{name}</span>
        </div>
        <p class="text-slate-400 text-sm leading-relaxed mb-8">
          Enterprise software development, cloud infrastructure, and AI automation company delivering mission-critical digital platforms and 24/7 managed IT services.
        </p>
        <div class="flex gap-4">
          <button onclick="openModal('loginModal')" class="bg-slate-800 hover:bg-{ac} text-white text-xs font-extrabold px-6 py-3 rounded-xl transition">Client Console Login</button>
          <button onclick="openModal('signupModal')" class="bg-{ac} hover:bg-{ach} text-white text-xs font-extrabold px-6 py-3 rounded-xl transition">Developer Sign Up</button>
        </div>
      </div>

      <div class="lg:col-span-7 grid sm:grid-cols-3 gap-6">
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800">
          <i class="fa-solid fa-location-dot text-2xl text-{act} mb-3"></i>
          <h4 class="text-xs font-bold uppercase text-slate-400 mb-2">Registered Address</h4>
          <p class="text-sm font-bold text-white leading-relaxed">{address}</p>
        </div>
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800">
          <i class="fa-solid fa-phone-volume text-2xl text-{act} mb-3"></i>
          <h4 class="text-xs font-bold uppercase text-slate-400 mb-2">Phone Number</h4>
          <a href="tel:{phone}" class="text-base font-black text-white hover:underline block">{phone}</a>
        </div>
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800">
          <i class="fa-solid fa-envelope text-2xl text-{act} mb-3"></i>
          <h4 class="text-xs font-bold uppercase text-slate-400 mb-2">Official Email</h4>
          <a href="mailto:{email}" class="text-sm font-black text-white hover:underline break-all block">{email}</a>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto pt-8 text-center sm:flex justify-between items-center text-xs text-slate-400">
      <p>© 2026 <strong>{name}</strong>. All Rights Reserved.</p>
      <p class="mt-2 sm:mt-0">Address: {address} | Phone: {phone} | Email: {email}</p>
    </div>
  </footer>

  <!-- LOGIN MODAL WITH CONTINUE WITH GOOGLE -->
  <div id="loginModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white text-slate-900 w-full max-w-md p-8 {rad} shadow-2xl relative">
      <button onclick="closeModal('loginModal')" class="absolute top-5 right-5 text-slate-400 hover:text-slate-900 text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-black mb-1">Client Cloud Console</h3>
      <p class="text-xs text-slate-500 mb-6">Sign in to manage deployments, API keys & billing for {name}</p>

      <button onclick="alert('Redirecting to Google Workspace SSO...');" class="w-full bg-white hover:bg-gray-50 text-slate-800 font-bold py-3.5 px-4 rounded-xl border border-gray-300 flex items-center justify-center space-x-3 mb-5 shadow-sm">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span class="text-sm">Continue with Google</span>
      </button>

      <form onsubmit="event.preventDefault(); alert('Authenticated successfully!');" class="space-y-4 text-sm">
        <input type="email" required placeholder="Work Email Address" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <input type="password" required placeholder="Password / Token" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <button type="submit" class="w-full bg-{ac} hover:bg-{ach} text-white font-extrabold py-3.5 rounded-xl shadow-lg">Sign In to Console</button>
      </form>
    </div>
  </div>

  <!-- SIGN UP MODAL WITH CONTINUE WITH GOOGLE -->
  <div id="signupModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white text-slate-900 w-full max-w-md p-8 {rad} shadow-2xl relative">
      <button onclick="closeModal('signupModal')" class="absolute top-5 right-5 text-slate-400 hover:text-slate-900 text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-black mb-1">Create Enterprise Account</h3>
      <p class="text-xs text-slate-500 mb-6">Onboard your organization with {name}</p>

      <button onclick="alert('Redirecting to Google Workspace Sign-Up...');" class="w-full bg-white hover:bg-gray-50 text-slate-800 font-bold py-3.5 px-4 rounded-xl border border-gray-300 flex items-center justify-center space-x-3 mb-5 shadow-sm">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span class="text-sm">Sign up with Google</span>
      </button>

      <form onsubmit="event.preventDefault(); alert('Enterprise account created!');" class="space-y-3.5 text-sm">
        <input type="text" required placeholder="Full Name / Organization Name" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <input type="tel" required placeholder="Mobile Number" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <input type="email" required placeholder="Corporate Email Address" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <input type="password" required placeholder="Create Password" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <button type="submit" class="w-full bg-slate-900 hover:bg-{ac} text-white font-extrabold py-3.5 rounded-xl shadow-lg transition">Create Account</button>
      </form>
    </div>
  </div>

  <script>
    function openModal(id) {{ document.getElementById(id).classList.add('modal-active'); }}
    function closeModal(id) {{ document.getElementById(id).classList.remove('modal-active'); }}

    const phrases = [
      "Custom Enterprise ERP & SaaS Platforms",
      "Multi-Cloud Kubernetes & Server Infrastructure",
      "AI Automation, LLMs & Predictive Analytics",
      "High-Frequency FinTech APIs & Mobile Apps"
    ];
    let pIdx = 0, cIdx = 0, isDel = false;
    const tw = document.getElementById("typewriter");
    function runType() {{
      const cur = phrases[pIdx];
      tw.innerText = isDel ? cur.substring(0, cIdx--) : cur.substring(0, cIdx++);
      let spd = isDel ? 35 : 65;
      if (!isDel && cIdx > cur.length) {{ spd = 1800; isDel = true; }}
      else if (isDel && cIdx === 0) {{ isDel = false; pIdx = (pIdx + 1) % phrases.length; spd = 350; }}
      setTimeout(runType, spd);
    }}
    document.addEventListener("DOMContentLoaded", runType);
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
        "💻 *1-to-10 Sequential Tech & Software Company Website Generator*\n\n"
        "Is bot me *10 Alag-Alag White-Theme Tech Interfaces* hain (Extra-Large Tech Photos + Alag Live Videos + Alag Design).\n\n"
        "🔄 *Automatic 1-by-1 Sequence:*\n"
        "1st message ➔ *Tech Website #1*\n"
        "2nd message ➔ *Tech Website #2*\n"
        "3rd message ➔ *Tech Website #3* ... (1 se 10 tak line se aayega)\n\n"
        "👇 *Bas ye 4 details bhejo:*\n"
        "`Name: Priyanshu Technology`\n"
        "`Phone: +91 9876543210`\n"
        "`Email: support@heoo.in`\n"
        "`Address: Unit 402, IT Park, Sector 62, Noida, UP 201309`\n\n"
        "⚙️ *Optional:* `/reset` (Wapas #1 se start karne ke liye)"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")


@bot.message_handler(commands=['reset'])
def reset_sequence(message):
    set_template_index(1)
    bot.reply_to(message, "✅ Sequence reset ho gaya! Ab agla website **Tech Template #1 / 10** se start hoga.", parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def generate_site(message):
    data = parse_details(message.text)
    if not all(k in data for k in ["name", "phone", "email", "address"]):
        bot.reply_to(
            message,
            "⚠️ *Saari 4 details sahi format me bhejo:*\n\n"
            "`Name: Tech Company Name`\n"
            "`Phone: +91 9876543210`\n"
            "`Email: contact@heoo.in`\n"
            "`Address: Full Office Address`",
            parse_mode="Markdown"
        )
        return

    idx = get_next_template_index()
    template_cfg = TEMPLATES_DATA[idx]
    template_num = template_cfg["id"]
    next_num = (idx + 1) % 10 + 1

    html = generate_html_for_template(
        template_cfg,
        data["name"],
        data["phone"],
        data["email"],
        data["address"]
    )

    bio = io.BytesIO(html.encode("utf-8"))
    bio.name = "index.html"

    bot.send_document(
        message.chat.id,
        bio,
        caption=(
            f"💻 *Tech Company Website #{template_num} / 10 Ready!*\n"
            f"🎨 *Interface Style:* {template_cfg['theme_name']}\n\n"
            f"🏢 *Name:* {data['name']}\n"
            f"📞 *Phone:* {data['phone']}\n"
            f"📧 *Email:* {data['email']}\n"
            f"📍 *Address:* {data['address']}\n\n"
            f"⏭️ *Agli baar details bhejne par Tech Website #{next_num} aayegi.*"
        ),
        parse_mode="Markdown"
    )


app = Flask(__name__)

@app.route('/')
def health():
    return "10-in-1 Sequential Tech Bot Live 24/7"

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
