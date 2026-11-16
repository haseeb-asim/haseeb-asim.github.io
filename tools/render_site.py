#!/usr/bin/env python3
"""Write the static pages. GitHub Pages serves the HTML directly; this script
is only for regenerating them after a copy or layout change."""

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://haseeb-asim.github.io"

PROJECTS = [
    {
        "slug": "keeper",
        "name": "Keeper",
        "group": "web",
        "group_label": "Web",
        "file": "keeper",
        "w": 1800, "h": 1350, "sw": 960, "sh": 720,
        "summary": "Multi-chain crypto portfolio management.",
        "alt": "Keeper on a laptop, desktop monitor, and tablet, showing a portfolio dashboard and a marketing page.",
        "selected": True,
        "tech": ["Web3", "Next.js", "Tailwind CSS", "Solana", "Ethereum"],
        "role": [
            "Designed dashboards aggregating data from wallet addresses, exchange APIs, and CSV files.",
            "Implemented PnL and US/Canada tax reporting with exports to platforms like TaxBit.",
            "Integrated Zerion, Vezgo, and Crypto API for data visualization.",
        ],
    },
    {
        "slug": "fantasy-funduhmentals",
        "name": "Fantasy FunDUHmentals",
        "group": "web",
        "group_label": "Web",
        "file": "fantasy",
        "w": 1800, "h": 1350, "sw": 960, "sh": 720,
        "summary": "Fantasy sports linked to real athletic performance, with a media hub.",
        "alt": "Fantasy FunDUHmentals on a laptop, desktop monitor, and tablet, showing a player page and a players list.",
        "selected": True,
        "tech": ["Web3", "Next.js", "Tailwind CSS", "Cardano"],
        "live": "https://theduh.com/",
        "role": [
            "Built the web interface for a platform merging real-world athletic performance with blockchain technology.",
            "Developed dashboards for minting, burning, and trading dynamic player NFTs tied to live sports data.",
            "Integrated a media hub with independent sports commentary and video.",
        ],
    },
    {
        "slug": "blob-dao",
        "name": "Blob DAO",
        "group": "web",
        "group_label": "Web",
        "file": "blob",
        "w": 1800, "h": 1350, "sw": 960, "sh": 720,
        "summary": "A DAO interface joining meme culture with DeFi.",
        "alt": "Blob DAO on a laptop, desktop monitor, and tablet, showing a dashboard and a marketing page.",
        "tech": ["Web3", "Ethers.js", "Next.js", "Tailwind CSS", "Crypto wallet"],
        "role": [
            "Developed the user-facing interface for Blob DAO, a decentralized organization integrating meme culture with DeFi protocols.",
            "Engineered a platform designed to capture liquidity from volatile meme-coin assets and redirect value back into the ecosystem.",
            "Turned on-chain liquidity redirection into community-driven mechanics.",
        ],
    },
    {
        "slug": "blockrock",
        "name": "Blockrock",
        "group": "web",
        "group_label": "Web",
        "file": "block",
        "w": 1800, "h": 1350, "sw": 960, "sh": 720,
        "summary": "A token launcher web app.",
        "alt": "Blockrock on a laptop, desktop monitor, and tablet, showing a token launcher.",
        "tech": ["Next.js", "Tailwind CSS", "Web3"],
        "role": [],
    },
    {
        "slug": "gotlr",
        "name": "GOTLR",
        "group": "mobile",
        "group_label": "Mobile",
        "file": "gotlr",
        "w": 1800, "h": 1444, "sw": 960, "sh": 770,
        "summary": "Multi-vendor delivery with live maps and chat.",
        "alt": "Three phones showing GOTLR: a map, delivery tracking, and chat.",
        "selected": True,
        "tech": ["React Native", "Geolocation", "Chat"],
        "role": [
            "Built the frontend for a multi-vendor commerce and delivery app.",
            "Implemented live, map-based tracking for delivery riders.",
            "Developed real-time messaging between users and riders.",
        ],
    },
    {
        "slug": "liible",
        "name": "Liible",
        "group": "mobile",
        "group_label": "Mobile",
        "file": "liible",
        "w": 1800, "h": 1444, "sw": 960, "sh": 770,
        "summary": "A multi-vendor marketplace with rider tracking and chat.",
        "alt": "Three phones showing the Liible app.",
        "tech": ["React Native"],
        "role": [
            "Developed the frontend for a multi-vendor commerce and delivery marketplace.",
            "Implemented live geolocation tracking for delivery riders.",
            "Built in-app chat and multi-store checkout.",
        ],
    },
    {
        "slug": "md-foods",
        "name": "MD Foods",
        "group": "mobile",
        "group_label": "Mobile",
        "file": "md",
        "w": 1800, "h": 1444, "sw": 960, "sh": 770,
        "summary": "A mobile store on a WooCommerce backend.",
        "alt": "Three phones showing the MD Foods grocery app: home, a product list, and a product page.",
        "tech": ["React Native"],
        "role": [
            "Developed the cross-platform app in React Native.",
            "Connected the storefront to WooCommerce through headless REST APIs.",
            "Implemented authentication, real-time sync, and native checkout.",
        ],
    },
    {
        "slug": "vitalvet",
        "name": "VitalVet",
        "group": "mobile",
        "group_label": "Mobile",
        "file": "vital",
        "w": 1800, "h": 1444, "sw": 960, "sh": 770,
        "summary": "Vet booking, video visits, and a pet shop.",
        "alt": "Three phones showing VitalVet: specialist booking, products, and a cart.",
        "tech": ["React Native"],
        "role": [
            "Developed the React Native app for veterinary services and pet commerce.",
            "Built booking for clinic visits and in-app video visits.",
            "Engineered checkout for pet products and accessories.",
        ],
    },
    {
        "slug": "tadalal",
        "name": "Tadalal",
        "group": "mobile",
        "group_label": "Mobile",
        "file": "talal",
        "w": 1800, "h": 1444, "sw": 960, "sh": 770,
        "summary": "E-commerce for the Qatari market, on Laravel.",
        "alt": "Three phones showing the Tadalal shopping app, including home, categories, and a cart in QAR.",
        "tech": ["React Native"],
        "role": [
            "Developed the React Native app for the Qatari e-commerce market.",
            "Implemented localized address checks and checkout for regional delivery.",
            "Integrated REST APIs backed by Laravel.",
        ],
    },
    {
        "slug": "ebher",
        "name": "Ebher",
        "group": "mobile",
        "group_label": "Mobile",
        "file": "ebhar",
        "w": 1800, "h": 1444, "sw": 960, "sh": 770,
        "summary": "Boat and yacht booking, with scheduling and add-ons.",
        "alt": "Three phones showing the Ebher boat booking app: listings, a yacht, and a date picker.",
        "selected": True,
        "tech": ["React Native"],
        "role": [
            "Developed the frontend for a boat and yacht reservation marketplace.",
            "Built scheduling for live slot selection and availability.",
            "Created checkout for optional gear, and an admin panel for listings.",
        ],
    },
    {
        "slug": "tastee",
        "name": "Tastee",
        "group": "mobile",
        "group_label": "Mobile",
        "file": None,
        "summary": "Food delivery, with merchant menus and consumer ordering.",
        "tech": ["React Native"],
        "role": [
            "Built the frontend for a food delivery platform connecting people with local restaurants.",
            "Developed a merchant portal for pricing, items, and details.",
            "Created location-based browsing, checkout, and order flow.",
        ],
    },
    {
        "slug": "fernly",
        "name": "Fernly",
        "prototype": True,
        "screen_dir": "/assets/concepts/01-fernly",
        "cover": "/assets/concepts/composites/fernly.webp",
        "thumb": "/assets/concepts/composites/fernly-sm.webp",
        "composite": True,
        "w": 1600, "h": 1200, "sw": 960, "sh": 720,
        "summary": "A support inbox with each draft cited to the help center.",
        "alt": "Fernly on a desktop and a phone, showing a support draft beside the articles it cites.",
        "tech": ["Web", "iOS"],
        "role": [],
    },
    {
        "slug": "crewline",
        "name": "Crewline",
        "prototype": True,
        "screen_dir": "/assets/concepts/02-crewline",
        "cover": "/assets/concepts/composites/crewline.webp",
        "thumb": "/assets/concepts/composites/crewline-sm.webp",
        "composite": True,
        "w": 1600, "h": 1200, "sw": 960, "sh": 720,
        "summary": "Booking and dispatch with a timeline, a map, and the job.",
        "alt": "Crewline on a desktop and a phone, showing a dispatch board and a booked job.",
        "tech": ["Web", "iOS"],
        "role": [],
    },
    {
        "slug": "mendwell",
        "name": "Mendwell",
        "prototype": True,
        "screen_dir": "/assets/concepts/03-mendwell",
        "cover": "/assets/concepts/composites/mendwell.webp",
        "thumb": "/assets/concepts/composites/mendwell-sm.webp",
        "composite": True,
        "w": 1600, "h": 1200, "sw": 960, "sh": 720,
        "summary": "Clinic and video visits, from the booking to the note.",
        "alt": "Mendwell on a desktop and a phone, showing a schedule and a visit booking.",
        "tech": ["Web", "iOS"],
        "role": [],
    },
    {
        "slug": "repharbor",
        "name": "Repharbor",
        "prototype": True,
        "screen_dir": "/assets/concepts/04-repharbor",
        "cover": "/assets/concepts/composites/repharbor.webp",
        "thumb": "/assets/concepts/composites/repharbor-sm.webp",
        "composite": True,
        "w": 1600, "h": 1200, "sw": 960, "sh": 720,
        "summary": "Strength coaching with a workout log and a week plan.",
        "alt": "Repharbor on a desktop and a phone, showing a coaching roster and a workout.",
        "tech": ["Web", "iOS"],
        "role": [],
    },
    {
        "slug": "quillmere",
        "name": "Quillmere",
        "prototype": True,
        "screen_dir": "/assets/concepts/05-quillmere",
        "cover": "/assets/concepts/composites/quillmere.webp",
        "thumb": "/assets/concepts/composites/quillmere-sm.webp",
        "composite": True,
        "w": 1600, "h": 1200, "sw": 960, "sh": 720,
        "summary": "A CRM where each line of a lead summary cites its source.",
        "alt": "Quillmere on a desktop and a phone, showing a pipeline and a lead summary.",
        "tech": ["Web", "iOS"],
        "role": [],
    },
    {
        "slug": "haverlet",
        "name": "Haverlet",
        "prototype": True,
        "screen_dir": "/assets/concepts/06-haverlet",
        "cover": "/assets/concepts/composites/haverlet.webp",
        "thumb": "/assets/concepts/composites/haverlet-sm.webp",
        "composite": True,
        "w": 1600, "h": 1200, "sw": 960, "sh": 720,
        "summary": "Rent and repairs, for the manager and the tenant.",
        "alt": "Haverlet on a desktop and a phone, showing rent and a repair request.",
        "tech": ["Web", "iOS"],
        "role": [],
    },
    {
        "slug": "ibidwell",
        "name": "Ibidwell",
        "prototype": True,
        "screen_dir": "/assets/concepts/07-ibidwell",
        "cover": "/assets/concepts/composites/ibidwell.webp",
        "thumb": "/assets/concepts/composites/ibidwell-sm.webp",
        "composite": True,
        "w": 1600, "h": 1200, "sw": 960, "sh": 720,
        "summary": "Contract answers, each one pointing at the page and clause.",
        "alt": "Ibidwell on a desktop and a phone, showing an answer with a citation.",
        "tech": ["Web", "iOS"],
        "role": [],
    },
    {
        "slug": "toquelane",
        "name": "Toquelane",
        "prototype": True,
        "screen_dir": "/assets/concepts/08-toquelane",
        "cover": "/assets/concepts/composites/toquelane.webp",
        "thumb": "/assets/concepts/composites/toquelane-sm.webp",
        "composite": True,
        "w": 1600, "h": 1200, "sw": 960, "sh": 720,
        "summary": "Restaurant ordering, from the guest's ticket to the kitchen.",
        "alt": "Toquelane on a desktop and a phone, showing a kitchen display and an order.",
        "tech": ["Web", "iOS"],
        "role": [],
    },
    {
        "slug": "holdlark",
        "name": "Holdlark",
        "prototype": True,
        "screen_dir": "/assets/concepts/09-holdlark",
        "cover": "/assets/concepts/composites/holdlark.webp",
        "thumb": "/assets/concepts/composites/holdlark-sm.webp",
        "composite": True,
        "w": 1600, "h": 1200, "sw": 960, "sh": 720,
        "summary": "Cash and crypto in one balance, checked before a send.",
        "alt": "Holdlark on a desktop and a phone, showing one balance and a send review.",
        "tech": ["Web", "iOS"],
        "role": [],
    },
    {
        "slug": "musterwick",
        "name": "Musterwick",
        "prototype": True,
        "screen_dir": "/assets/concepts/10-musterwick",
        "cover": "/assets/concepts/composites/musterwick.webp",
        "thumb": "/assets/concepts/composites/musterwick-sm.webp",
        "composite": True,
        "w": 1600, "h": 1200, "sw": 960, "sh": 720,
        "summary": "Event tickets that scan at the door and match check-in.",
        "alt": "Musterwick on a desktop and a phone, showing an event ticket and check-in.",
        "tech": ["Web", "iOS"],
        "role": [],
    },
]


def e(value):
    return escape(str(value), quote=True)


HARD = {
    "keeper": "The hard part was one dashboard that had to agree across wallet addresses, exchange APIs, and CSV files, including the tax export.",
    "fantasy-funduhmentals": "The hard part was dashboards for minting, burning, and trading player NFTs that follow live sports data, beside a media hub.",
    "blob-dao": "The hard part was turning on-chain liquidity redirection into a community interface.",
    "blockrock": "The hard part was a short web flow for launching a token contract.",
    "gotlr": "The hard part was keeping the live map, the rider, and the chat together during a delivery.",
    "liible": "The hard part was live rider tracking, in-app chat, and checkout across more than one store.",
    "md-foods": "The hard part was a React Native storefront that stays in sync with WooCommerce through native checkout.",
    "vitalvet": "The hard part was moving between a clinic booking, a video visit, and the shop without the app losing its place.",
    "tadalal": "The hard part was address checks and checkout for delivery in Qatar, on a Laravel API.",
    "ebher": "The hard part was live boat availability, optional add-ons, and an admin side for the listings.",
    "tastee": "The hard part was a merchant menu builder and a customer ordering flow in the same app.",
}

ROLE = {
    "keeper": "Design and engineering",
    "fantasy-funduhmentals": "Engineering",
    "blob-dao": "Engineering",
    "blockrock": "Engineering",
    "gotlr": "Engineering",
    "liible": "Engineering",
    "md-foods": "Engineering",
    "vitalvet": "Engineering",
    "tadalal": "Engineering",
    "ebher": "Engineering",
    "tastee": "Engineering",
    "fernly": "Design",
    "crewline": "Design",
    "mendwell": "Design",
    "repharbor": "Design",
    "quillmere": "Design",
    "haverlet": "Design",
    "ibidwell": "Design",
    "toquelane": "Design",
    "holdlark": "Design",
    "musterwick": "Design",
}

OVERVIEW = {
    "keeper": "Keeper needed one place to see a crypto portfolio across wallets, exchanges, and CSV files. I designed the dashboards, then built profit-and-loss and US and Canada tax reporting, with exports to TaxBit. The numbers come in through Zerion, Vezgo, and Crypto API.",
    "fantasy-funduhmentals": "Fantasy FunDUHmentals needed a web app that links fantasy sports to real athletic performance, plus a media hub. I built dashboards for minting, burning, and trading player NFTs tied to live sports data, and the hub for independent sports commentary and video.",
    "blob-dao": "Blob DAO needed an interface that puts meme culture next to DeFi. I built the user-facing side of a platform meant to capture liquidity from volatile meme-coin assets and send that value back into the ecosystem, as community-driven mechanics.",
    "blockrock": "Blockrock is a token launcher web app. I built the web app.",
    "gotlr": "GOTLR needed multi-vendor delivery with a live map and chat. I built the frontend, including map-based tracking for riders and real-time messaging between users and riders.",
    "liible": "Liible needed a multi-vendor marketplace with rider tracking and chat. I built the frontend, with live geolocation, in-app chat, and checkout across more than one store.",
    "md-foods": "MD Foods needed a mobile store on a WooCommerce backend. I built the React Native app, connected it through headless REST APIs, and implemented authentication, real-time sync, and native checkout.",
    "vitalvet": "VitalVet needed vet booking, video visits, and a pet shop in one app. I built the React Native app, including clinic and video-visit booking, and checkout for pet products and accessories.",
    "tadalal": "Tadalal needed an e-commerce app for the Qatari market. I built the React Native app, with localized address checks and checkout for regional delivery, on REST APIs backed by Laravel.",
    "ebher": "Ebher needed boat and yacht booking, with scheduling and add-ons. I built the frontend for live slot selection and availability, checkout for optional gear, and an admin panel for the listings.",
    "tastee": "Tastee needed food delivery, with merchant menus and consumer ordering. I built the frontend, including a merchant portal for pricing, items, and details, and location-based browsing and checkout.",
    "fernly": "A draft is hard to trust when the help-center passage it came from is not on the screen. I designed and prototyped Fernly so the draft and the cited article sit together. The decision was that a person checks, edits, and approves the reply before it is sent.",
    "crewline": "A home-service day is hard to run when the booking, the map, and the job are separate. I designed and prototyped Crewline so a person books a window and follows the technician, while dispatch works from a timeline beside a map. The decision was to keep the checklist, photos, and sign-off on that same job.",
    "mendwell": "A visit breaks when the booking, the check-in, and the note are different records. I designed and prototyped Mendwell so a person books a clinic or video visit and checks in, and the clinician finishes the note from the day's schedule. The decision was to treat those three as one visit.",
    "repharbor": "A coaching program drifts when the workout log and the week's plan are not the same program. I designed and prototyped Repharbor so a person logs sets and can send a form-check video, and the coach builds the week from that. The decision was to keep the log and the plan together.",
    "quillmere": "A lead summary is hard to trust when it does not show the call, email, or visit behind it. I designed and prototyped Quillmere for small businesses that sell through calls and site visits. The decision was that the pipeline, the deal, and the phone log share that cited summary.",
    "haverlet": "Rent and repairs get disputed when the manager and the tenant are not looking at the same numbers. I designed and prototyped Haverlet so the manager sees rent and the repair queue, and a tenant pays rent, requests a repair, and reads notices. The decision was that both sides add up the same way.",
    "ibidwell": "An answer from a contract is hard to use when it does not point at the page and clause. I designed and prototyped Ibidwell for questions against a team's own contracts. The decision was to say so when the searched documents do not contain the answer.",
    "toquelane": "An order goes wrong when the guest's ticket and the kitchen display are not the same order. I designed and prototyped Toquelane so a guest customizes an order, checks out, and follows the ticket. The decision was that the kitchen display and the menu stay on that ticket.",
    "holdlark": "A send of cash or crypto is hard to undo, so the fee and the address have to be visible first. I designed and prototyped Holdlark so those assets sit in one balance. The decision was to show the fee and an address check before the send, with one ledger for activity.",
    "musterwick": "A ticket fails when the scan at the door does not match the organizer's list. I designed and prototyped Musterwick so a person finds an event, holds a ticket, and can talk with the people going. The decision was that the door scan and check-in use that same ticket.",
}

HERO = (
    "I've spent eight years shipping apps people actually use: marketplaces, "
    "fintech dashboards, and apps on the App Store and Google Play. Lately I build "
    "the AI and backend systems behind products like these."
)

PIPES = {
    "keeper": {
        "steps": [
            "Wallets, exchanges, and CSV files",
            "Dashboards for profit and loss",
            "US and Canada tax reporting",
            "Export to TaxBit",
        ],
        "note": "The numbers come in through Zerion, Vezgo, and Crypto API.",
    },
    "fantasy-funduhmentals": {
        "steps": [
            "Live sports data",
            "Mint, burn, and trade player NFTs",
            "A media hub for commentary and video",
        ],
    },
    "blob-dao": {
        "steps": [
            "Volatile meme-coin assets",
            "Liquidity captured for the ecosystem",
            "Community-driven mechanics",
        ],
    },
    "blockrock": {
        "steps": [
            "A short web flow",
            "Launch a token",
        ],
    },
    "gotlr": {
        "steps": [
            "Multi-vendor delivery",
            "A live map of the rider",
            "Chat between the customer and the rider",
        ],
    },
    "liible": {
        "steps": [
            "More than one store",
            "Live rider tracking",
            "In-app chat and checkout",
        ],
    },
    "md-foods": {
        "steps": [
            "WooCommerce, through headless REST",
            "Authentication and real-time sync",
            "Native checkout",
        ],
    },
    "vitalvet": {
        "steps": [
            "Clinic booking and video visits",
            "A pet shop",
            "Checkout for products and accessories",
        ],
    },
    "tadalal": {
        "steps": [
            "A catalog for the Qatari market",
            "Localized address checks",
            "Checkout on a Laravel API",
        ],
    },
    "ebher": {
        "steps": [
            "Boat and yacht listings",
            "Live slot selection",
            "Optional gear at checkout",
            "An admin panel for the listings",
        ],
    },
    "tastee": {
        "steps": [
            "Merchant menus, prices, and items",
            "Location-based browsing",
            "Checkout and the order",
        ],
    },
    "fernly": {
        "steps": [
            "Help-center articles",
            "A draft with the cited passage",
            "A person approves it before it is sent",
        ],
    },
    "crewline": {
        "steps": [
            "A booked arrival window",
            "A timeline beside a map",
            "The technician's checklist",
        ],
    },
    "mendwell": {
        "steps": [
            "Book a visit",
            "Check in",
            "The visit note",
        ],
    },
    "repharbor": {
        "steps": [
            "A logged workout",
            "A week of the program",
            "A form-check in the chat",
        ],
    },
    "quillmere": {
        "steps": [
            "Calls, emails, and visits",
            "A lead summary that cites them",
            "The pipeline",
        ],
    },
    "haverlet": {
        "steps": [
            "Rent and repairs",
            "The manager's view",
            "The tenant's view",
        ],
    },
    "ibidwell": {
        "steps": [
            "The team's contracts",
            "An answer with the page and clause",
            "A not-found state when it is not there",
        ],
    },
    "toquelane": {
        "steps": [
            "The guest's order",
            "Checkout",
            "The kitchen display",
        ],
    },
    "holdlark": {
        "steps": [
            "One balance",
            "A fee and an address check",
            "The send",
        ],
    },
    "musterwick": {
        "steps": [
            "An event nearby",
            "A ticket at the door",
            "Check-in for the organizer",
        ],
    },
}


def sentences(text):
    parts = re.split(r"(?<=[.])\s+", text.strip())
    return [part for part in parts if part]


def head(title, description, path, image=None):
    url = SITE + path
    image = image or "/assets/og.png"
    full_image = image if image.startswith("http") else SITE + image
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>
    (function () {{
      try {{
        var t = localStorage.getItem("theme");
        if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
        var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        if (!reduce) document.documentElement.classList.add("motion");
        if (!reduce && window.matchMedia("(min-width: 900px)").matches) document.documentElement.classList.add("rich");
      }} catch (e) {{}}
    }})();
  </script>
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{e(url)}">
  <meta name="author" content="Haseeb Asim">
  <meta name="theme-color" content="#f4f4f2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0b0b0c" media="(prefers-color-scheme: dark)">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{e(url)}">
  <meta property="og:image" content="{e(full_image)}">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(description)}">
  <meta name="twitter:image" content="{e(full_image)}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/newsreader.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/css/site.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
"""


def nav():
    return """  <header class="nav" data-nav>
    <div class="wrap nav-inner">
      <a class="wordmark" data-magnetic href="/">Haseeb&nbsp;Asim</a>
      <nav class="nav-links" aria-label="Primary">
        <a data-nav-link data-magnetic href="/work/">Work</a>
        <a data-nav-link data-magnetic href="/about/">About</a>
      </nav>
      <div class="nav-tools">
        <button class="cmd-btn" type="button" data-command aria-haspopup="dialog">Search <kbd>⌘K</kbd></button>
        <a class="talk" data-magnetic href="mailto:haseebasim95@gmail.com">Let’s talk</a>
        <button class="theme" type="button" data-theme-toggle data-magnetic aria-pressed="false">
          <span class="theme-track" aria-hidden="true"><span class="theme-disk"></span></span>
          <span class="theme-label">Dark</span>
        </button>
      </div>
    </div>
  </header>
"""


def command_json():
    items = [
        {"label": "Home", "href": "/", "hint": "Page"},
        {"label": "Work", "href": "/work/", "hint": "Page"},
        {"label": "About", "href": "/about/", "hint": "Page"},
        {"label": "Let’s talk", "href": "mailto:haseebasim95@gmail.com", "hint": "Email"},
    ]
    for project in PROJECTS:
        items.append({"label": project["name"], "href": f"/work/{project['slug']}/", "hint": project["summary"]})
    return json.dumps(items)


def footer():
    return f"""  <footer class="footer">
    <div class="wrap">
      <p class="footer-label">Have something that needs to work? Write to me.</p>
      <a class="footer-mail" href="mailto:haseebasim95@gmail.com">haseebasim95@gmail.com</a>
      <p class="sign">With care, Haseeb</p>
      <nav aria-label="Footer">
        <a href="/work/">Work</a>
        <a href="/about/">About</a>
        <a href="https://github.com/haseeb-asim" rel="me noopener noreferrer">GitHub</a>
      </nav>
    </div>
  </footer>
  <div class="cmd" data-cmd hidden>
    <div class="cmd-panel" role="dialog" aria-modal="true" aria-label="Search the site">
      <input data-cmd-input type="search" placeholder="Search projects and pages" aria-label="Search projects and pages">
      <ul data-cmd-list></ul>
    </div>
  </div>
  <script type="application/json" id="cmd-index">{command_json()}</script>
  <script src="/js/site.js" defer></script>
</body>
</html>
"""


def write(path, html):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    print(path)


def thumb(project):
    if project.get("thumb"):
        return project["thumb"]
    if project.get("cover"):
        return project["cover"]
    if project.get("file"):
        return f"/assets/projects/{project['file']}-sm.webp"
    return ""


CHEVRON_PREV = (
    '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true">'
    '<path d="M10 3.5 5.5 8 10 12.5" fill="none" stroke="currentColor" '
    'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)
CHEVRON_NEXT = (
    '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true">'
    '<path d="M6 3.5 10.5 8 6 12.5" fill="none" stroke="currentColor" '
    'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


def group_id(label):
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def card(project):
    plate = ""
    if project.get("file"):
        file = project["file"]
        shot = f"/assets/projects/{file}-sm.webp"
        width = project.get("sw", 960)
        height = project.get("sh", 720)
        plate = " is-plate"
    elif project.get("thumb") or project.get("cover"):
        if project.get("thumb"):
            shot = project["thumb"]
            width = project.get("sw", project.get("w", 1600))
            height = project.get("sh", project.get("h", 1200))
        else:
            shot = project["cover"]
            width = project.get("w", 1600)
            height = project.get("h", 1200)
        if project.get("composite"):
            plate = " is-plate"
    else:
        shot = ""
        plate = " type-plate"
    if shot:
        media = (
            f'<img src="{shot}" width="{width}" height="{height}" alt="" '
            f'loading="lazy" decoding="async">'
        )
    else:
        media = f'<span class="type-mark">{e(project["name"])}</span>'
    stack = " · ".join(project.get("tech") or [])
    stack_html = f'<span class="card-stack">{e(stack)}</span>' if stack else ""
    return f"""<a class="card" data-vt="{project['slug']}" data-cursor="view" href="/work/{project['slug']}/">
        <span class="card-media{plate}">{media}</span>
        <span class="card-copy">
          <span class="card-name">{e(project['name'])}</span>
          <span class="card-line">{e(project['summary'])}</span>
          {stack_html}
        </span>
      </a>"""


def card_items(projects):
    return "".join(f"<li>{card(project)}</li>" for project in projects)


PROTO_ORDER = [
    "holdlark", "fernly", "ibidwell", "quillmere", "crewline",
    "toquelane", "mendwell", "haverlet", "repharbor", "musterwick",
]


def work_order():
    shipped = [project for project in PROJECTS if not project.get("prototype")]
    by_slug = {project["slug"]: project for project in PROJECTS}
    return shipped + [by_slug[slug] for slug in PROTO_ORDER]


# Shown as text, not image cards. Blockrock's case study is two short
# sentences, and Tastee has no screenshots. Nothing else is that thin
# or missing an image.
ALSO_BUILT = ["blockrock", "tastee"]


# Work index buckets. Shipped projects come first inside each one.
# Tadalal, Ebher, and VitalVet were not in the requested lists:
# Tadalal is Qatari e-commerce, Ebher is boat and yacht booking,
# and VitalVet is vet care plus a pet shop.
WORK_GROUPS = [
    ("Crypto and fintech", [
        "keeper", "fantasy-funduhmentals", "blob-dao", "blockrock", "holdlark",
    ]),
    ("Delivery and marketplaces", [
        "gotlr", "liible", "md-foods", "tastee", "tadalal", "toquelane", "crewline",
    ]),
    ("AI-powered tools", [
        "fernly", "ibidwell", "quillmere",
    ]),
    ("Business and booking software", [
        "ebher", "haverlet", "musterwick",
    ]),
    ("Health and fitness", [
        "vitalvet", "mendwell", "repharbor",
    ]),
]


def grouped_projects():
    by_slug = {project["slug"]: project for project in PROJECTS}
    seen = []
    groups = []
    for label, slugs in WORK_GROUPS:
        items = [by_slug[slug] for slug in slugs if slug not in ALSO_BUILT]
        seen.extend(slugs)
        if items:
            groups.append((label, items))
    missing = [project["slug"] for project in PROJECTS if project["slug"] not in seen]
    if missing or len(seen) != len(PROJECTS):
        raise SystemExit(f"Work groups do not cover every project: {missing}")
    return groups


def grid_class(count):
    names = ["card-grid"]
    # A lone last card reads as a leftover. Widen the first card so the
    # last row holds two, on both the 3-column and 2-column layouts.
    if count > 1 and count % 3 == 1:
        names.append("span-lead")
    if count > 1 and count % 2 == 1:
        names.append("span-lead-2")
    return " ".join(names)


def work_groups():
    parts = []
    for label, items in grouped_projects():
        parts.append(
            f'<section class="bucket" id="{group_id(label)}">\n'
            f'        <h2 class="group-label">{e(label)}</h2>\n'
            f'        <ul class="{grid_class(len(items))}">{card_items(items)}</ul>\n'
            f'      </section>'
        )
    return "\n      ".join(parts)


def shelves():
    parts = []
    for label, items in grouped_projects():
        gid = group_id(label)
        parts.append(
            f"""<div class="shelf">
        <div class="shelf-head">
          <h2 class="group-label">{e(label)}</h2>
          <div class="shelf-tools">
            <button class="shelf-btn shelf-prev" type="button" aria-label="Previous projects in {e(label)}" disabled>{CHEVRON_PREV}</button>
            <button class="shelf-btn shelf-next" type="button" aria-label="Next projects in {e(label)}">{CHEVRON_NEXT}</button>
            <a class="see-all" href="/work/#{gid}">See all<span class="sr"> {e(label)}</span></a>
          </div>
        </div>
        <div class="shelf-row">
          <ul class="shelf-track" data-shelf>{card_items(items)}</ul>
        </div>
      </div>"""
        )
    return "\n      ".join(parts)


def also_projects():
    by_slug = {project["slug"]: project for project in PROJECTS}
    return [by_slug[slug] for slug in ALSO_BUILT]


def also_block():
    rows = []
    for project in also_projects():
        stack = " · ".join(project.get("tech") or [])
        stack_html = f'<span class="stack">{e(stack)}</span>' if stack else ""
        rows.append(
            f"""<li><a data-vt="{project['slug']}" data-cursor="view" href="/work/{project['slug']}/">
        <span class="name">{e(project['name'])}</span>
        <span class="meta"><span class="desc">{e(project['summary'])}</span>{stack_html}</span>
      </a></li>"""
        )
    return f"""<section class="also" aria-labelledby="also-built">
        <h2 id="also-built" class="group-label">Also built</h2>
        <ul class="catalog">{''.join(rows)}</ul>
      </section>"""


def also_line():
    links = [
        f'<a href="/work/{project["slug"]}/">{e(project["name"])}</a>'
        for project in also_projects()
    ]
    if len(links) == 1:
        listed = links[0]
    elif len(links) == 2:
        listed = f"{links[0]} and {links[1]}"
    else:
        listed = ", ".join(links[:-1]) + f", and {links[-1]}"
    return f'<p class="also-line">Also built {listed}.</p>'


def webp_size(path):
    data = path.read_bytes()
    if data[12:16] == b"VP8X" and len(data) >= 30:
        return 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
    if data[12:16] == b"VP8 " and len(data) >= 30:
        return int.from_bytes(data[26:28], "little") & 0x3FFF, int.from_bytes(data[28:30], "little") & 0x3FFF
    if data[12:16] == b"VP8L" and len(data) >= 25:
        b0, b1, b2, b3 = data[21:25]
        width = 1 + (((b1 & 0x3F) << 8) | b0)
        height = 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
        return width, height
    return 1600, 1200


def screen_caption(filename):
    parts = Path(filename).stem.split("-")
    if parts and parts[0] in {"web", "mobile"}:
        parts = parts[1:]
    if parts and parts[0].isdigit():
        parts = parts[1:]
    acronyms = {"ai": "AI", "kds": "KDS"}
    words = [acronyms.get(part.lower(), part.lower()) for part in parts]
    if words and words[0] not in acronyms.values():
        words[0] = words[0][:1].upper() + words[0][1:]
    return " ".join(words)


def extra_screens(project):
    directory = project.get("screen_dir")
    if not directory:
        return []
    folder = ROOT / directory.lstrip("/")
    paths = [
        path for path in folder.glob("*.webp")
        if not path.name.startswith("cover") and not path.name.startswith("web-1")
    ]
    paths.sort(key=lambda path: (0 if path.name.startswith("web") else 1, path.name))
    screens = []
    for path in paths:
        width, height = webp_size(path)
        src = "/" + path.relative_to(ROOT).as_posix()
        screens.append((src, width, height, screen_caption(path.name)))
    return screens


def screens_block(project):
    shots = extra_screens(project)
    if not shots:
        return ""
    items = []
    for src, width, height, caption in shots:
        items.append(
            f'<li><figure class="shot"><img src="{src}" width="{width}" height="{height}" alt="" loading="lazy" decoding="async"><figcaption>{e(caption)}</figcaption></figure></li>'
        )
    return f"""<section class="wrap screen-set" aria-label="More screens">
      <p class="num">More screens</p>
      <ul class="screen-grid">{''.join(items)}</ul>
    </section>"""


def link_html(project):
    if project.get("link_text"):
        return e(project["link_text"])
    url = project.get("live")
    if not url:
        return "Private codebase"
    return f'<a href="{e(url)}" rel="noopener noreferrer" target="_blank">Live site ↗</a>'


def pipe_block(project):
    pipe = PIPES.get(project["slug"])
    if not pipe:
        return ""
    parts = []
    steps = pipe["steps"]
    for i, step in enumerate(steps, 1):
        source = f'<p class="pipe-source">{e(pipe["note"])}</p>' if i == 1 and pipe.get("note") else ""
        dot = '<span class="pipe-dot" aria-hidden="true"></span>' if i < len(steps) else ""
        parts.append(f"<li><span class=\"pipe-n\">{i:02d}</span>{e(step)}{source}{dot}</li>")
    return f"""<section class="wrap system">
      <p class="num">02 — How it's built</p>
      <h2>How the pieces connect.</h2>
      <ol class="pipe" data-pipe>{''.join(parts)}</ol>
    </section>"""


def next_block(project):
    items = work_order()
    index = next(i for i, item in enumerate(items) if item["slug"] == project["slug"])
    nxt = items[(index + 1) % len(items)]
    shot = thumb(nxt)
    if shot:
        media = f'<span class="next-media"><img src="{shot}" width="960" height="720" alt=""></span>'
    else:
        media = f'<span class="next-media type-plate"><span class="type-mark">{e(nxt["name"])}</span></span>'
    return f"""<a class="next wrap" data-vt="{nxt['slug']}" data-cursor="view" href="/work/{nxt['slug']}/">
        {media}
        <span><span class="next-kicker">Next project</span><span class="vt-title">{e(nxt['name'])}</span><span class="go">View</span></span>
      </a>"""


def hero_block():
    return """<h1 class="hero-line">
          <span class="ln"><span>I’ve spent eight years shipping apps people actually use:</span></span>
          <span class="ln"><span>marketplaces, fintech dashboards, and apps on the App Store and Google Play.</span></span>
          <span class="ln"><span>Lately I build the <em class="kinetic">AI and backend systems</em> behind products like these.</span></span>
        </h1>"""


def page_home():
    html = head("Haseeb Asim", HERO, "/")
    html += nav()
    html += f"""  <main id="main">
    <section class="hero" data-hero>
      <canvas class="field" data-field aria-hidden="true"></canvas>
      <div class="wrap hero-inner">
        <p class="eyebrow"><span class="dot" aria-hidden="true"></span> Available for new work</p>
        {hero_block()}
        <p class="status"><span class="clock" data-clock>—:—</span><span>Dallas · Central Time</span><a href="mailto:haseebasim95@gmail.com">haseebasim95@gmail.com</a></p>
      </div>
    </section>
    <section class="band shelves" aria-label="Work">
      <div class="wrap">
        {shelves()}
        {also_line()}
      </div>
    </section>
  </main>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Person","name":"Haseeb Asim","jobTitle":"Senior full-stack engineer","email":"mailto:haseebasim95@gmail.com","url":"https://haseeb-asim.github.io/","address":{{"@type":"PostalAddress","addressLocality":"Dallas","addressRegion":"TX","addressCountry":"US"}},"alumniOf":[{{"@type":"CollegeOrUniversity","name":"Columbia University"}},{{"@type":"CollegeOrUniversity","name":"LUMS"}}],"sameAs":["https://github.com/haseeb-asim"]}}
  </script>
"""
    html += footer()
    write("index.html", html)


def page_work_index():
    html = head("Work · Haseeb Asim", "A mix of live products and work still in development or at the prototype stage. Where a product is public, the case study links to it.", "/work/")
    html += nav()
    html += f"""  <main id="main" class="page">
    <div class="wrap">
      <p class="kicker">Work</p>
      <h1 class="page-title">The work.</h1>
      <p class="lede">A mix of live products and work still in development or at the prototype stage. Where a product is public, the case study links to it.</p>
      {work_groups()}
      {also_block()}
    </div>
  </main>
"""
    html += footer()
    write("work/index.html", html)


def page_project(project):
    path = f"/work/{project['slug']}/"
    overview = OVERVIEW.get(project["slug"], project["summary"])
    parts = sentences(overview)
    problem = parts[0] if parts else project["summary"]
    later = parts[1:]
    if project.get("prototype") and later and later[-1].startswith("The decision"):
        decision = later[-1]
        approach = " ".join(later[:-1])
    else:
        decision = ""
        approach = " ".join(later)
    decision_html = f"<h2>Key decisions</h2><p>{e(decision)}</p>" if decision else ""
    tech = " · ".join(e(item) for item in project["tech"])
    if project.get("prototype"):
        platform = "Web and iOS"
    elif project["group"] == "web":
        platform = "Web"
    else:
        platform = "Mobile"
    role = ROLE.get(project["slug"])
    role_row = f"<div><dt>Role</dt><dd>{e(role)}</dd></div>" if role else ""
    if project.get("cover"):
        stage = f"""<figure class="stage" data-vt-hero><img src="{project['cover']}" width="{project.get('w', 1200)}" height="{project.get('h', 900)}" alt="{e(project['alt'])}" decoding="async" fetchpriority="high"></figure>"""
        og = project["cover"]
    elif project.get("file"):
        stage = f"""<figure class="stage" data-vt-hero><img src="/assets/projects/{project['file']}.webp" width="1600" height="1200" alt="{e(project['alt'])}" decoding="async" fetchpriority="high"></figure>"""
        og = f"/assets/projects/{project['file']}.webp"
    else:
        stage = f'<div class="stage type-plate" data-vt-hero><p class="type-mark">{e(project["name"])}</p></div>'
        og = "/assets/og.png"
    screens = screens_block(project)
    screens_html = f"\n      {screens}" if screens else ""
    html = head(f"{project['name']} · Haseeb Asim", project["summary"], path, og)
    html = html.replace("<body>", '<body class="has-progress">\n  <div class="progress" aria-hidden="true"></div>', 1)
    html += nav()
    html += f"""  <main id="main" class="page">
    <article>
      <header class="wrap study-top">
        <p class="kicker"><a href="/work/">Work</a></p>
        <p class="num">01 — The product</p>
        <h1 class="page-title vt-title">{e(project['name'])}</h1>
        <p class="lede">{e(project['summary'])}</p>
      </header>
      <div class="story wrap" data-story>
        <div class="story-pin"><p class="num">Screens</p>{stage}</div>
        <div class="story-copy">
          <h2>Problem</h2>
          <p>{e(problem)}</p>
          <h2>Approach</h2>
          <p>{e(approach)}</p>
          {decision_html}
        </div>
      </div>{screens_html}
      {pipe_block(project)}
      <p class="num wrap stack-num">03 — Stack</p>
      <dl class="study-facts wrap">
        {role_row}
        <div><dt>Platform</dt><dd>{platform}</dd></div>
        <div><dt>Stack</dt><dd>{tech}</dd></div>
        <div><dt>Link</dt><dd>{link_html(project)}</dd></div>
      </dl>
      {next_block(project)}
    </article>
  </main>
"""
    html += footer()
    write(f"work/{project['slug']}/index.html", html)


def page_redirect(path, target):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Moved</title>
  <link rel="canonical" href="{SITE}{target}">
  <meta http-equiv="refresh" content="0; url={target}">
  <script>location.replace("{target}")</script>
</head>
<body>
  <p><a href="{target}">This page has moved.</a></p>
</body>
</html>
"""
    write(path, html)


def page_about():
    html = head(
        "About · Haseeb Asim",
        "Senior full-stack engineer in Dallas. Eight-plus years, MS Columbia 2021, BS LUMS 2018.",
        "/about/",
    )
    html += nav()
    html += """  <main id="main" class="page">
    <div class="wrap">
      <p class="kicker">About</p>
      <div class="about-top">
        <div>
          <h1 class="page-title">About</h1>
          <p class="narrative">I like shipping production systems, with clean code you can own and extend.</p>
          <p class="lede">For eight years that has meant full-stack products across SaaS, fintech, and blockchain, including apps I've published to the App Store and Google Play. Lately I build the backend systems, data, and applied agentic AI behind them. I have an MS from Columbia University and a BS from LUMS, and I'm based in Dallas, Texas.</p>
        </div>
        <figure class="portrait">
          <picture>
            <source srcset="/assets/portrait.avif" type="image/avif">
            <img src="/assets/portrait.webp" width="460" height="460" alt="Haseeb Asim" decoding="async">
          </picture>
        </figure>
      </div>
      <dl class="about-facts">
        <div><dt>Based</dt><dd>Dallas, Texas</dd></div>
        <div><dt>Hours</dt><dd>US Central Time business hours</dd></div>
        <div><dt>Education</dt><dd>MS, Columbia University, 2021<br>BS, LUMS, 2018</dd></div>
        <div><dt>Now</dt><dd>Available for new work</dd></div>
      </dl>
      <section class="block" id="process">
        <p class="num">01 — How I work</p>
        <h2>A short path from the first call to the handoff.</h2>
        <ol class="plain">
          <li>A short call to understand the workflow and what success looks like.</li>
          <li>A working prototype early, so you see results before the big spend.</li>
          <li>Daily or every-other-day updates.</li>
          <li>Clean handoff docs and a walkthrough video.</li>
        </ol>
      </section>
      <section class="block" id="services">
        <p class="num">02 — What I build</p>
        <h2>AI agents, RAG, and the stack around them.</h2>
        <p class="lede">AI agents, RAG, CRM automation, and the full stack around them.</p>
        <div class="services">
          <div>
            <h3>AI agents and workflows</h3>
            <p>LangGraph, LangChain, or CrewAI agents that plan, call tools, and keep state across steps.</p>
          </div>
          <div>
            <h3>RAG and search</h3>
            <p>Answers grounded in your docs, tickets, or knowledge base, using Pinecone, pgvector, or Chroma, so you can check the source.</p>
          </div>
          <div>
            <h3>CRM and sales automation</h3>
            <p>HubSpot integrations, lead enrichment, AI email drafting, and pipeline updates.</p>
          </div>
          <div>
            <h3>The full stack around it</h3>
            <p>Next.js and React, NestJS and Node, React Native, Stripe, and AWS or Supabase. Voice and multimodal work with Whisper, Deepgram, and ElevenLabs when the product needs it.</p>
          </div>
        </div>
      </section>
      <section class="block" id="tools">
        <p class="num">03 — Tools</p>
        <h2>What the work is built with.</h2>
        <dl class="facts">
          <div><dt>Engineering</dt><dd>JavaScript, TypeScript, Python, React, Next.js, React Native, Node.js, Express, NestJS, FastAPI, Tailwind CSS</dd></div>
          <div><dt>Data and infra</dt><dd>MongoDB, PostgreSQL, Redis, pgvector, Docker, AWS, Supabase, Git</dd></div>
          <div><dt>Applied AI</dt><dd>OpenAI, LangGraph, LangChain, CrewAI, Pinecone, Chroma</dd></div>
        </dl>
      </section>
    </div>
  </main>
"""
    html += footer()
    write("about/index.html", html)


def page_404():
    html = head("Page not found · Haseeb Asim", "This page is not on the site.", "/404.html")
    html += nav()
    html += """  <main id="main" class="missing">
    <div class="wrap">
      <h1 class="page-title">This page is not on the site.</h1>
      <p class="lede">The address may have changed.</p>
      <a href="/">Back home</a>
    </div>
  </main>
"""
    html += footer()
    write("404.html", html)


def sitemap():
    paths = ["/", "/work/", "/about/"]
    paths += [f"/work/{p['slug']}/" for p in PROJECTS]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in paths:
        lines.append(f"  <url><loc>{SITE}{path}</loc></url>")
    lines.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(lines))
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")


def main():
    page_home()
    page_work_index()
    for project in PROJECTS:
        page_project(project)
    page_redirect("concepts/index.html", "/work/")
    for project in PROJECTS:
        if project.get("prototype"):
            page_redirect(f"concepts/{project['slug']}/index.html", f"/work/{project['slug']}/")
    page_about()
    page_404()
    sitemap()


if __name__ == "__main__":
    main()
