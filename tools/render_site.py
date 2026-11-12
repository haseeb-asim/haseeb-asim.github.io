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
]


def screen(file, w, h, caption, alt):
    return {"file": file, "w": w, "h": h, "caption": caption, "alt": alt}


def web(file, caption, alt, w=2000, h=1347):
    return screen(file, w, h, caption, alt)


def phone(file, caption, alt):
    return screen(file, 790, 1516, caption, alt)


CONCEPTS = [
    {
        "slug": "fernly", "dir": "01-fernly", "name": "Fernly",
        "kind": "AI customer-support inbox",
        "summary": "An AI-assisted support inbox. Drafts come from the company's help-center articles, with citations, so an agent can check, edit, and approve a reply before it is sent.",
        "screens": [
            web("web-1-agent-console.webp", "Agent console · Web", "Fernly web screen: the agent console, with an AI draft and the articles it cites."),
            web("web-2-insights-knowledge.webp", "Insights · Web", "Fernly web screen: insights on drafts, and questions the help center cannot answer yet."),
            phone("mobile-1-inbox.webp", "Inbox · iOS", "Fernly iOS screen: the support inbox."),
            phone("mobile-2-ticket-ai-reply.webp", "AI reply · iOS", "Fernly iOS screen: a ticket with an AI draft."),
            phone("mobile-3-edit-review.webp", "Edit and review · iOS", "Fernly iOS screen: editing a draft before it is sent."),
        ],
    },
    {
        "slug": "crewline", "dir": "02-crewline", "name": "Crewline",
        "kind": "Field-service booking and dispatch",
        "summary": "Booking and dispatch for home-service companies. Customers book a window and follow their technician. Dispatchers assign jobs from a timeline beside a map.",
        "screens": [
            web("web-1-dispatch-board.webp", "Dispatch board · Web", "Crewline web screen: a dispatch board with a timeline and a live map."),
            web("web-2-job-detail.webp", "Job detail · Web", "Crewline web screen: a job detail page."),
            phone("mobile-1-customer-booking.webp", "Customer booking · iOS", "Crewline iOS screen: a customer booking an arrival window."),
            phone("mobile-2-customer-tracking.webp", "Live tracking · iOS", "Crewline iOS screen: a customer following their technician."),
            phone("mobile-3-technician-job.webp", "Technician job · iOS", "Crewline iOS screen: a technician job with a checklist, photos, and sign-off."),
        ],
    },
    {
        "slug": "mendwell", "dir": "03-mendwell", "name": "Mendwell",
        "kind": "Clinic and telehealth",
        "summary": "A clinic and telehealth product. Patients book a video or in-person visit and check in. Clinicians work from the day's schedule and the visit note.",
        "screens": [
            web("web-1-provider-schedule.webp", "Provider schedule · Web", "Mendwell web screen: a clinician schedule beside a waiting room."),
            web("web-2-patient-chart.webp", "Patient chart · Web", "Mendwell web screen: a visit note with intake answers."),
            phone("mobile-1-book-visit.webp", "Book a visit · iOS", "Mendwell iOS screen: booking a visit."),
            phone("mobile-2-intake.webp", "Intake · iOS", "Mendwell iOS screen: a short check-in form."),
            phone("mobile-3-video-visit.webp", "Video visit · iOS", "Mendwell iOS screen: a video visit with live captions."),
        ],
    },
    {
        "slug": "repharbor", "dir": "04-repharbor", "name": "Repharbor",
        "kind": "Strength coaching",
        "summary": "A subscription coaching product. Clients log workouts and send form-check videos. Coaches see every client and build each week of the program.",
        "screens": [
            web("web-1-clients.webp", "Client roster · Web", "Repharbor web screen: a coach's client roster."),
            web("web-2-plan-builder.webp", "Plan builder · Web", "Repharbor web screen: a week-by-week plan builder."),
            phone("mobile-1-workout.webp", "Active workout · iOS", "Repharbor iOS screen: logging a workout set by set."),
            phone("mobile-2-progress.webp", "Progress · iOS", "Repharbor iOS screen: strength and consistency trends."),
            phone("mobile-3-coach-chat.webp", "Coach chat · iOS", "Repharbor iOS screen: coach chat with a form-check video."),
        ],
    },
    {
        "slug": "quillmere", "dir": "05-quillmere", "name": "Quillmere",
        "kind": "Small-business CRM",
        "summary": "A CRM for small trade and service businesses that sell through calls and site visits. Each point in the lead summary cites its source.",
        "screens": [
            web("web-1-pipeline.webp", "Pipeline · Web", "Quillmere web screen: a pipeline of open, weighted, and won deals."),
            web("web-2-deal.webp", "Deal · Web", "Quillmere web screen: a deal with an AI lead summary that cites its sources."),
            phone("mobile-1-log-call.webp", "Log a call · iOS", "Quillmere iOS screen: logging a call from the field."),
            phone("mobile-2-contact.webp", "Contact · iOS", "Quillmere iOS screen: a contact with the same lead summary."),
            phone("mobile-3-today.webp", "Today · iOS", "Quillmere iOS screen: today's visits and calls."),
        ],
    },
    {
        "slug": "haverlet", "dir": "06-haverlet", "name": "Haverlet",
        "kind": "Property management",
        "summary": "For small property managers and their tenants. Managers see rent and repairs. Tenants pay rent, request repairs, and read building notices.",
        "screens": [
            web("web-1-payments.webp", "Payments · Web", "Haverlet web screen: rent payments for the manager."),
            web("web-2-repairs.webp", "Repairs · Web", "Haverlet web screen: a repairs queue."),
            phone("mobile-1-pay-rent.webp", "Pay rent · iOS", "Haverlet iOS screen: a tenant paying rent."),
            phone("mobile-2-repair-request.webp", "Repair request · iOS", "Haverlet iOS screen: a new repair request."),
            phone("mobile-3-home.webp", "Home · iOS", "Haverlet iOS screen: the tenant home screen."),
        ],
    },
    {
        "slug": "ibidwell", "dir": "07-ibidwell", "name": "Ibidwell",
        "kind": "AI document assistant",
        "summary": "Answers from a team's own contracts. Ask in plain English, and every statement points to the page and clause it came from.",
        "screens": [
            web("web-1-ask.webp", "Ask · Web", "Ibidwell web screen: an answer with citations back to the page and clause."),
            web("web-2-library.webp", "Library · Web", "Ibidwell web screen: a document library with processing status."),
            phone("mobile-1-answer.webp", "Answer · iOS", "Ibidwell iOS screen: an answer with citations."),
            phone("mobile-2-viewer.webp", "Citation viewer · iOS", "Ibidwell iOS screen: the cited page with the passage highlighted."),
            phone("mobile-3-not-found.webp", "Not found · iOS", "Ibidwell iOS screen: a not-found state limited to the documents that were searched."),
        ],
    },
    {
        "slug": "toquelane", "dir": "08-toquelane", "name": "Toquelane",
        "kind": "Restaurant ordering",
        "summary": "Ordering, rewards, and the kitchen for fast-casual restaurants. Guests order and track food in the restaurant's app. The kitchen runs the display.",
        "screens": [
            web("web-1-kds.webp", "Kitchen display · Web", "Toquelane web screen: a kitchen display sorted by time left.", 2000, 1193),
            web("web-2-menu.webp", "Menu manager · Web", "Toquelane web screen: a menu manager synced with the kitchen."),
            phone("mobile-1-customize.webp", "Customize · iOS", "Toquelane iOS screen: customizing an order."),
            phone("mobile-2-checkout.webp", "Checkout · iOS", "Toquelane iOS screen: checkout with the total broken out."),
            phone("mobile-3-tracking.webp", "Order tracking · iOS", "Toquelane iOS screen: order tracking tied to the kitchen ticket."),
        ],
    },
    {
        "slug": "holdlark", "dir": "09-holdlark", "name": "Holdlark",
        "kind": "Cash and crypto wallet",
        "summary": "Cash and a few crypto assets in one balance. Extra checks appear before a send that cannot be undone.",
        "screens": [
            web("web-1-overview.webp", "Overview · Web", "Holdlark web screen: balance, allocation, and card spending."),
            web("web-2-activity.webp", "Activity · Web", "Holdlark web screen: one activity ledger across accounts."),
            phone("mobile-1-home.webp", "Home · iOS", "Holdlark iOS screen: one balance and each asset."),
            phone("mobile-2-send-review.webp", "Review send · iOS", "Holdlark iOS screen: fees and an address check before a send."),
            phone("mobile-3-receive.webp", "Receive · iOS", "Holdlark iOS screen: a receive address and QR code."),
        ],
    },
    {
        "slug": "musterwick", "dir": "10-musterwick", "name": "Musterwick",
        "kind": "Events, tickets, and chat",
        "summary": "Community events. People find something nearby, carry a ticket that scans at the door, and talk with everyone going. Organizers see sales and check-in.",
        "screens": [
            web("web-1-overview.webp", "Sales and overview · Web", "Musterwick web screen: sales, payout, and live check-in."),
            web("web-2-attendees.webp", "Attendees · Web", "Musterwick web screen: attendees and check-in status."),
            phone("mobile-1-discover.webp", "Discover · iOS", "Musterwick iOS screen: events nearby."),
            phone("mobile-2-ticket.webp", "Ticket · iOS", "Musterwick iOS screen: a ticket with a rotating QR code."),
            phone("mobile-3-chat.webp", "Community chat · iOS", "Musterwick iOS screen: moderated attendee chat."),
        ],
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

CONCEPT_HARD = {
    "fernly": "The hard part of the design is keeping the cited help-center article next to the draft, so a person can approve it before it is sent.",
    "crewline": "The hard part of the design is one picture of the day: a timeline, a live map, and the job the technician is actually on.",
    "mendwell": "The hard part of the design is the same visit existing as a booking, a check-in, and a note the clinician can finish.",
    "repharbor": "The hard part of the design is a workout log and a coach's week plan staying on the same program.",
    "quillmere": "The hard part of the design is a lead summary where every point shows the call, email, or visit it came from.",
    "haverlet": "The hard part of the design is rent and repairs adding up the same way for the manager and the tenant.",
    "ibidwell": "The hard part of the design is an answer that points at the page and clause, instead of a score.",
    "toquelane": "The hard part of the design is the guest's ticket and the kitchen display counting the same order.",
    "holdlark": "The hard part of the design is showing the fee and the address check before a send that cannot be undone.",
    "musterwick": "The hard part of the design is one ticket that scans at the door and still matches the organizer's check-in count.",
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
}

HERO = (
    "I've spent eight years shipping apps people actually use: marketplaces, "
    "fintech dashboards, and apps on the App Store and Google Play. Lately I build "
    "the AI and backend systems behind products like these."
)

FEATURED = ["keeper", "gotlr", "fantasy-funduhmentals", "ebher"]

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
        <a data-nav-link data-magnetic href="/concepts/">Concepts</a>
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
        {"label": "Concepts", "href": "/concepts/", "hint": "Page"},
        {"label": "About", "href": "/about/", "hint": "Page"},
        {"label": "Let’s talk", "href": "mailto:haseebasim95@gmail.com", "hint": "Email"},
    ]
    for project in PROJECTS:
        items.append({"label": project["name"], "href": f"/work/{project['slug']}/", "hint": project["summary"]})
    for concept in CONCEPTS:
        items.append({"label": concept["name"], "href": f"/concepts/{concept['slug']}/", "hint": "Concept"})
    return json.dumps(items)


def footer():
    return f"""  <footer class="footer">
    <div class="wrap">
      <p class="footer-label">Have something that needs to work? Write to me.</p>
      <a class="footer-mail" href="mailto:haseebasim95@gmail.com">haseebasim95@gmail.com</a>
      <p class="sign">With care, Haseeb</p>
      <p class="stamp">Last updated Nov&nbsp;12,&nbsp;2026 · <span class="clock" data-clock>—:—</span> CT · Dallas</p>
      <p class="colophon">Colophon. Static HTML, CSS, and JavaScript, generated in the repo and served by GitHub Pages. Display type is Newsreader. Scroll sequences use GSAP ScrollTrigger. Large screens use Lenis for smooth scrolling. The hero field is a small WebGL shader, paused when it leaves the screen, and left out when motion is reduced or WebGL is unavailable. Page changes use the View Transitions API. No analytics.</p>
      <nav aria-label="Footer">
        <a href="/work/">Work</a>
        <a href="/concepts/">Concepts</a>
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


def row(project):
    stack = " · ".join(project["tech"])
    preview = ""
    if project.get("file"):
        preview = f' data-preview="/assets/projects/{project["file"]}-sm.webp"'
    return f"""<li><a data-vt="{project['slug']}" data-cursor="view"{preview} href="/work/{project['slug']}/">
        <span class="name vt-title">{e(project['name'])}</span>
        <span class="meta"><span class="desc">{e(project['summary'])}</span><span class="stack">{e(stack)}</span></span>
      </a></li>"""


def slide(project, index, total):
    if project.get("file"):
        file = project["file"]
        media = (
            f'<img src="/assets/projects/{file}.webp" '
            f'srcset="/assets/projects/{file}-sm.webp 960w, /assets/projects/{file}.webp 1600w" '
            f'sizes="(min-width: 900px) 62vw, 88vw" width="1600" height="1200" alt="{e(project["alt"])}" '
            f'loading="eager" decoding="sync" fetchpriority="high">'
        )
    else:
        media = '<span class="no-shot">No mockup on file.</span>'
    live = '<span class="live-tag">Live site</span>' if project.get("live") else ""
    on = " is-on" if index == 1 else ""
    return f"""<a class="reel-item{on}" data-vt="{project['slug']}" data-cursor="view" href="/work/{project['slug']}/">
        <span class="reel-fig">{media}</span>
        <span class="reel-copy">
          <span class="reel-idx">{index:02d} / {total:02d}</span>
          <span class="vt-title">{e(project['name'])}</span>
          <span class="reel-sum">{e(project['summary'])}</span>
          {live}
        </span>
      </a>"""


def catalog(projects):
    web = [project for project in projects if project["group"] == "web"]
    mobile = [project for project in projects if project["group"] == "mobile"]
    return f"""<p class="group-label">Web and Web3</p>
      <ul class="catalog">{''.join(row(project) for project in web)}</ul>
      <p class="group-label">Mobile</p>
      <ul class="catalog">{''.join(row(project) for project in mobile)}</ul>"""


def link_html(project):
    url = project.get("live")
    if not url:
        return "Private codebase"
    return f'<a href="{e(url)}" rel="noopener noreferrer" target="_blank">Live site ↗</a>'


def pipe_block(project):
    pipe = PIPES.get(project["slug"])
    if not pipe:
        return ""
    items = "".join(f"<li><span>{i:02d}</span>{e(step)}</li>" for i, step in enumerate(pipe["steps"], 1))
    note = f'<p class="pipe-note">{e(pipe["note"])}</p>' if pipe.get("note") else ""
    return f"""<section class="wrap system">
      <p class="num">02 — The system</p>
      <h2>How the pieces connect.</h2>
      <ol class="pipe" data-pipe>{items}</ol>
      {note}
    </section>"""


def next_block(project):
    index = next(i for i, item in enumerate(PROJECTS) if item["slug"] == project["slug"])
    nxt = PROJECTS[(index + 1) % len(PROJECTS)]
    if nxt.get("file"):
        media = f'<span class="next-media"><img src="/assets/projects/{nxt["file"]}-sm.webp" width="960" height="720" alt=""></span>'
    else:
        media = '<span class="next-media"><span class="no-shot">No mockup on file.</span></span>'
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
    by = {project["slug"]: project for project in PROJECTS}
    featured = [by[slug] for slug in FEATURED]
    slides = "".join(slide(project, i, len(featured)) for i, project in enumerate(featured, 1))
    rest = [project for project in PROJECTS if project["slug"] not in FEATURED]
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
    <section class="band" aria-labelledby="selected">
      <div class="wrap band-head">
        <p class="num">01 — Selected work</p>
        <h2 id="selected">Four products,<br>on the record.</h2>
      </div>
      <div class="reel wrap" data-reel>
        <div class="reel-sticky">
          <div class="reel-track">
            {slides}
          </div>
          <div class="reel-progress" role="progressbar" aria-valuemin="1" aria-valuemax="{len(featured)}" aria-valuenow="1" aria-label="Selected work">
            <span class="reel-count">01 / {len(featured):02d}</span>
            <span class="reel-bar"><span></span></span>
          </div>
        </div>
      </div>
    </section>
    <section class="band" aria-labelledby="index-work">
      <div class="wrap">
        <p class="num">02 — The index</p>
        <h2 id="index-work">Everything else,<br>still shipped.</h2>
        {catalog(rest)}
      </div>
    </section>
    <section class="band" data-loop aria-labelledby="agent">
      <div class="wrap">
        <p class="num">03 — An agent</p>
        <h2 id="agent">Plan, retrieve,<br>cite, answer.</h2>
        <p class="notice">Illustrative demo. Not a client project. The question and the policy are made up, to show the loop I build: plan, call a tool, retrieve a passage, cite it, then answer.</p>
        <div class="loop">
          <ol class="loop-steps">
            <span class="loop-fill" aria-hidden="true"></span>
            <li data-step="1"><span>01</span>Plan</li>
            <li data-step="2"><span>02</span>Call a tool</li>
            <li data-step="3"><span>03</span>Retrieve</li>
            <li data-step="4"><span>04</span>Cite the source</li>
            <li data-step="5"><span>05</span>Answer</li>
          </ol>
          <div class="loop-run" aria-live="polite">
            <p class="loop-q"><span class="loop-k">Question</span>What’s the refund window for a damaged shipment?</p>
            <p class="loop-line" data-out="1"><span class="loop-k">Plan</span>Search the shipping policy for the refund window.</p>
            <p class="loop-line" data-out="2"><span class="loop-k">Tool</span>search_docs, “refund damaged shipment”.</p>
            <p class="loop-line" data-out="3"><span class="loop-k">Retrieved</span>Shipping policy, page 4. Damaged items can be refunded within 14 days if you send a photo.</p>
            <p class="loop-line" data-out="4"><span class="loop-k">Source</span><span class="chip">Shipping policy · page 4</span></p>
            <p class="loop-answer" data-out="5"><span class="sr">You have 14 days. Send a photo of the damage, and the shipment is refunded.</span><span class="typed" data-typed="You have 14 days. Send a photo of the damage, and the shipment is refunded." aria-hidden="true">You have 14 days. Send a photo of the damage, and the shipment is refunded.</span></p>
          </div>
        </div>
        <button class="replay" type="button" data-replay>Play it again</button>
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
    html = head("Work · Haseeb Asim", "Shipped products. Each one is client work, and the public link is private unless a live site is listed.", "/work/")
    html += nav()
    html += f"""  <main id="main" class="page">
    <div class="wrap">
      <p class="kicker">Work</p>
      <p class="num">01 — Shipped</p>
      <h1 class="page-title">Client products.</h1>
      <p class="lede">Each one is real work. Where a product is on the public web, the case study links to it. The codebase stays private.</p>
      {catalog(PROJECTS)}
    </div>
  </main>
"""
    html += footer()
    write("work/index.html", html)


def page_project(project):
    path = f"/work/{project['slug']}/"
    overview = OVERVIEW.get(project["slug"], project["summary"])
    steps = "".join(f"<li>{e(part)}</li>" for part in sentences(overview))
    tech = " · ".join(e(item) for item in project["tech"])
    platform = "Web" if project["group"] == "web" else "Mobile"
    role = ROLE.get(project["slug"])
    role_row = f"<div><dt>Role</dt><dd>{e(role)}</dd></div>" if role else ""
    if project.get("file"):
        stage = f"""<figure class="stage" data-vt-hero><img src="/assets/projects/{project['file']}.webp" width="1600" height="1200" alt="{e(project['alt'])}" decoding="async" fetchpriority="high"></figure>"""
        og = f"/assets/projects/{project['file']}.webp"
    else:
        stage = '<div class="stage" data-vt-hero><p class="no-shot">No mockup on file.</p></div>'
        og = "/assets/og.png"
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
        <div class="story-pin">{stage}</div>
        <ol class="story-steps">{steps}</ol>
      </div>
      {pipe_block(project)}
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


def page_concepts_index():
    cards = []
    for concept in CONCEPTS:
        directory = concept["dir"]
        cards.append(f"""<a class="g-card" data-vt="{concept['slug']}" data-cursor="view" href="/concepts/{concept['slug']}/">
          <img src="/assets/concepts/{directory}/cover-sm.webp" width="1200" height="900" alt="{e(concept['name'])} concept cover." loading="lazy" decoding="async">
          <span class="concept-cap"><span class="vt-title">{e(concept['name'])}</span> — {e(concept['kind'])}</span>
        </a>""")
    html = head(
        "Concepts · Haseeb Asim",
        "Self-initiated concept designs with fictional sample data, not client work.",
        "/concepts/",
    )
    html += nav()
    html += f"""  <main id="main" class="page">
    <div class="wrap">
      <p class="kicker">Concepts</p>
      <p class="num">01 — Studies</p>
      <h1 class="page-title">Concept designs.</h1>
      <p class="lede">Self-initiated concept designs with fictional sample data, not client work.</p>
      <p class="gallery-hint">Drag to move through them. Arrow keys work too.</p>
    </div>
    <div class="gallery" data-gallery tabindex="0" aria-label="Concept studies">
      <div class="gallery-track">
        {''.join(cards)}
      </div>
    </div>
  </main>
"""
    html += footer()
    write("concepts/index.html", html)


def page_concept(concept):
    directory = concept["dir"]
    shots = [f"""<figure class="shot" data-vt-hero>
        <img src="/assets/concepts/{directory}/cover.webp" width="1200" height="900" alt="{e(concept['name'])} concept cover." decoding="async">
        <figcaption>Cover</figcaption>
      </figure>"""]
    for shot in concept["screens"]:
        shots.append(f"""<figure class="shot">
        <img src="/assets/concepts/{directory}/{shot['file']}" width="{shot['w']}" height="{shot['h']}" alt="{e(shot['alt'])}" loading="lazy" decoding="async">
        <figcaption>{e(shot['caption'])}</figcaption>
      </figure>""")
    html = head(
        f"{concept['name']} · Concept · Haseeb Asim",
        concept["summary"] + " Self-initiated concept with fictional sample data, not client work.",
        f"/concepts/{concept['slug']}/",
        f"/assets/concepts/{directory}/cover.webp",
    )
    html = html.replace("<body>", '<body class="has-progress">\n  <div class="progress" aria-hidden="true"></div>', 1)
    html += nav()
    html += f"""  <main id="main" class="page">
    <article class="wrap">
      <p class="kicker"><a href="/concepts/">Concepts</a> · Concept</p>
      <h1 class="page-title vt-title">{e(concept['name'])}</h1>
      <p class="lede">{e(concept['summary'])}</p>
      <p class="notice">Self-initiated concept design. Names, brands, and figures are fictional sample data, not client work.</p>
      <div class="stack">
        {''.join(shots)}
      </div>
    </article>
  </main>
"""
    html += footer()
    write(f"concepts/{concept['slug']}/index.html", html)


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
      <div class="about-grid">
        <div>
          <h1 class="page-title">About</h1>
          <p class="narrative">I like shipping production systems, with clean code you can own and extend.</p>
          <p class="lede">For eight years that has meant full-stack products across SaaS, fintech, and blockchain, including apps I've published to the App Store and Google Play. Lately I build the backend systems, data, and applied agentic AI behind them. I have an MS from Columbia University and a BS from LUMS, and I'm based in Dallas, Texas.</p>
        </div>
        <dl class="facts">
          <div><dt>Based</dt><dd>Dallas, Texas<br>US Central Time</dd></div>
          <div><dt>Hours</dt><dd>US Eastern business hours</dd></div>
          <div><dt>Education</dt><dd>MS, Columbia University, 2021<br>BS, LUMS, 2018</dd></div>
          <div><dt>Now</dt><dd>Available for new work</dd></div>
        </dl>
      </div>
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
    paths = ["/", "/work/", "/concepts/", "/about/"]
    paths += [f"/work/{p['slug']}/" for p in PROJECTS]
    paths += [f"/concepts/{c['slug']}/" for c in CONCEPTS]
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
    page_concepts_index()
    for concept in CONCEPTS:
        page_concept(concept)
    page_about()
    page_404()
    sitemap()


if __name__ == "__main__":
    main()
