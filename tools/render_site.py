#!/usr/bin/env python3
"""Write the static pages. GitHub Pages serves the HTML directly; this script
is only for regenerating them after a copy or layout change."""

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

FEATURED = ["keeper", "gotlr", "fantasy-funduhmentals", "ebher"]


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
      <a class="wordmark" href="/">Haseeb&nbsp;Asim</a>
      <nav class="nav-links" aria-label="Primary">
        <a data-nav-link href="/work/">Work</a>
        <a data-nav-link href="/concepts/">Concepts</a>
        <a data-nav-link href="/about/">About</a>
      </nav>
      <button class="theme-btn" type="button" data-theme-toggle aria-pressed="false">Dark</button>
    </div>
  </header>
"""


def footer():
    return """  <footer class="footer">
    <div class="wrap">
      <p class="footer-label">Have something that needs to work? Write to me.</p>
      <a class="footer-mail" href="mailto:haseebasim95@gmail.com">haseebasim95@gmail.com</a>
      <p class="sign">With care, Haseeb</p>
      <p class="stamp">Last updated Nov&nbsp;12,&nbsp;2026 · <span class="clock" data-clock>—:—</span> CT · Dallas</p>
      <nav aria-label="Footer">
        <a href="/work/">Work</a>
        <a href="/concepts/">Concepts</a>
        <a href="/about/">About</a>
        <a href="https://github.com/haseeb-asim" rel="me noopener noreferrer">GitHub</a>
      </nav>
    </div>
  </footer>
  <script src="/js/site.js" defer></script>
</body>
</html>
"""


def write(path, html):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    print(path)


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

DETAILS = {
    "keeper": [
        ("keeper-1.webp", 240, 320, "Portfolio", "Keeper portfolio chart with net worth and account totals."),
        ("keeper-2.webp", 216, 288, "Market table", "Keeper market table with prices and daily change."),
    ],
    "fantasy-funduhmentals": [
        ("fantasy-1.webp", 240, 320, "Player page", "Fantasy FunDUHmentals player stats and a mint button."),
        ("fantasy-2.webp", 232, 310, "Home", "Fantasy FunDUHmentals home, with the navigation and hero."),
    ],
    "blob-dao": [
        ("blob-1.webp", 240, 320, "Treasury", "Blob DAO treasury balance and a claim button."),
        ("blob-2.webp", 232, 310, "Charts", "Blob DAO price charts."),
    ],
    "blockrock": [
        ("block-1.webp", 180, 240, "Token launch", "Blockrock steps to register and create a token."),
        ("block-2.webp", 232, 310, "Landing page", "Blockrock form for setting up a landing page."),
    ],
    "gotlr": [
        ("gotlr-1.webp", 384, 512, "Delivery", "GOTLR delivery tracking with a map and a route."),
        ("gotlr-2.webp", 384, 512, "Chat", "GOTLR chat between a customer and a rider."),
    ],
    "liible": [
        ("liible-1.webp", 384, 512, "A listing", "A Liible job listing with the rate and the schedule."),
        ("liible-2.webp", 372, 496, "Business profile", "A Liible business profile with contact details."),
    ],
    "md-foods": [
        ("md-1.webp", 372, 496, "Shop", "MD Foods product grid with prices."),
        ("md-2.webp", 348, 464, "Best sellers", "MD Foods best sellers."),
    ],
    "vitalvet": [
        ("vital-1.webp", 384, 512, "Cart", "VitalVet cart with a consult and the total."),
        ("vital-2.webp", 384, 512, "Shop", "VitalVet shop list."),
    ],
    "tadalal": [
        ("talal-1.webp", 384, 512, "Home", "Tadalal home, with categories and a delivery banner."),
        ("talal-2.webp", 372, 496, "Cart", "Tadalal cart with prices in QAR."),
    ],
    "ebher": [
        ("ebhar-1.webp", 384, 512, "Pick a date", "Ebher date picker for a booking."),
        ("ebhar-2.webp", 372, 496, "A listing", "An Ebher yacht listing with the rate and guest count."),
    ],
}

HERO = (
    "I've spent eight years shipping apps people actually use: marketplaces, "
    "fintech dashboards, and apps on the App Store and Google Play. Lately I build "
    "the AI and backend systems behind products like these."
)


def feature(project, eager=False):
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return f"""<a class="feature" data-vt="{project['slug']}" href="/work/{project['slug']}/">
        <span class="feature-media"><img src="/assets/projects/{project['file']}-sm.webp" srcset="/assets/projects/{project['file']}-sm.webp 960w, /assets/projects/{project['file']}.webp 1600w" sizes="(min-width: 960px) 34vw, 92vw" width="1600" height="1200" alt="{e(project['alt'])}" loading="{loading}" decoding="async"{priority}></span>
        <span class="feature-meta"><span class="vt-title">{e(project['name'])}</span></span>
        <span class="feature-line">{e(project['summary'])}</span>
      </a>"""


def row(project):
    stack = " · ".join(project["tech"])
    return f"""<li><a data-vt="{project['slug']}" href="/work/{project['slug']}/">
        <span class="name vt-title">{e(project['name'])}</span>
        <span class="meta"><span class="desc">{e(project['summary'])}</span><span class="stack">{e(stack)}</span></span>
      </a></li>"""


def detail_block(project):
    shots = DETAILS.get(project["slug"], [])
    if not shots:
        return ""
    figs = []
    for file, w, h, caption, alt in shots:
        figs.append(
            f"""<figure>
        <div class="frame"><img src="/assets/projects/details/{file}" width="{w}" height="{h}" alt="{e(alt)}" decoding="async"></div>
        <figcaption>{e(caption)}</figcaption>
      </figure>"""
        )
    return f'<div class="details">\n        {"".join(figs)}\n      </div>'


def next_block(project):
    index = next(i for i, item in enumerate(PROJECTS) if item["slug"] == project["slug"])
    nxt = PROJECTS[(index + 1) % len(PROJECTS)]
    if nxt["file"]:
        media = f'<span class="next-media"><img src="/assets/projects/{nxt["file"]}-sm.webp" width="960" height="720" alt=""></span>'
    else:
        media = '<span class="next-media"></span>'
    return f"""<a class="next" data-vt="{nxt['slug']}" href="/work/{nxt['slug']}/">
        {media}
        <span><span class="next-kicker">Next project</span><span class="vt-title">{e(nxt['name'])}</span></span>
        <span class="go" aria-hidden="true">→</span>
      </a>"""


def page_home():
    by = {p["slug"]: p for p in PROJECTS}
    cards = "\n      ".join(feature(by[slug], eager=(i == 0)) for i, slug in enumerate(FEATURED))
    rest = [p for p in PROJECTS if p["slug"] not in FEATURED]
    web = [p for p in rest if p["group"] == "web"]
    mobile = [p for p in rest if p["group"] == "mobile"]
    html = head(
        "Haseeb Asim",
        HERO,
        "/",
    )
    html += nav()
    html += f"""  <main id="main">
    <div class="wrap index">
      <div class="index-grid">
        <header class="identity">
          <p class="who">Haseeb Asim</p>
          <h1 class="hero-line">{e(HERO)}</h1>
          <p class="status"><span class="dot" aria-hidden="true"></span><span>Available for new work</span><span class="clock" data-clock>—:—</span><span>Dallas · CT</span></p>
          <p class="reach"><a href="mailto:haseebasim95@gmail.com">haseebasim95@gmail.com</a></p>
        </header>
        <div>
          <div class="featured">
            {cards}
          </div>
          <section class="catalog" aria-labelledby="all-work">
            <p class="catalog-note" id="all-work">Everything else</p>
            <p class="group-label">Web and Web3</p>
            <ul class="catalog">{''.join(row(p) for p in web)}</ul>
            <p class="group-label">Mobile</p>
            <ul class="catalog">{''.join(row(p) for p in mobile)}</ul>
          </section>
        </div>
      </div>
    </div>
  </main>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Person","name":"Haseeb Asim","jobTitle":"Senior full-stack engineer","email":"mailto:haseebasim95@gmail.com","url":"https://haseeb-asim.github.io/","address":{{"@type":"PostalAddress","addressLocality":"Dallas","addressRegion":"TX","addressCountry":"US"}},"alumniOf":[{{"@type":"CollegeOrUniversity","name":"Columbia University"}},{{"@type":"CollegeOrUniversity","name":"LUMS"}}],"sameAs":["https://github.com/haseeb-asim"]}}
  </script>
"""
    html += footer()
    write("index.html", html)


def page_work_index():
    # The homepage is the index. /work/ still lists everything for a clean URL.
    page_home_list = True
    html = head("Work · Haseeb Asim", "Shipped products. Each one is client work, and the public link is private.", "/work/")
    html += nav()
    web = [p for p in PROJECTS if p["group"] == "web"]
    mobile = [p for p in PROJECTS if p["group"] == "mobile"]
    html += f"""  <main id="main" class="page">
    <div class="wrap">
      <p class="kicker">Work</p>
      <h1 class="page-title">Shipped</h1>
      <p class="lede">Client products I have shipped.</p>
      <p class="group-label">Web and Web3</p>
      <ul class="catalog">{''.join(row(p) for p in web)}</ul>
      <p class="group-label">Mobile</p>
      <ul class="catalog">{''.join(row(p) for p in mobile)}</ul>
    </div>
  </main>
"""
    html += footer()
    write("work/index.html", html)
    return page_home_list


def page_project(project):
    path = f"/work/{project['slug']}/"
    overview = OVERVIEW.get(project["slug"], project["summary"])
    narrative = f"<p>{e(overview)}</p>"
    tech = " · ".join(e(t) for t in project["tech"])
    platform = "Web" if project["group"] == "web" else "Mobile"
    role = ROLE.get(project["slug"])
    role_row = f"<div><dt>Role</dt><dd>{e(role)}</dd></div>" if role else ""
    if project["file"]:
        stage = f"""<figure class="stage" data-vt-hero><img src="/assets/projects/{project['file']}.webp" width="1600" height="1200" alt="{e(project['alt'])}" decoding="async" fetchpriority="high"></figure>"""
        og = f"/assets/projects/{project['file']}.webp"
    else:
        stage = '<div class="stage" data-vt-hero><p class="feature-line" style="position:absolute;inset:0;display:grid;place-items:center">No mockup on file.</p></div>'
        og = "/assets/og.png"
    html = head(f"{project['name']} · Haseeb Asim", project["summary"], path, og)
    html = html.replace("<body>", '<body class="has-progress">\n  <div class="progress" aria-hidden="true"></div>', 1)
    html += nav()
    html += f"""  <main id="main" class="page">
    <article class="wrap">
      <p class="kicker"><a href="/work/">Work</a></p>
      <h1 class="page-title vt-title">{e(project['name'])}</h1>
      <p class="lede">{e(project['summary'])}</p>
      {stage}
      <div class="study">
        <dl class="rail">
          {role_row}
          <div><dt>Platform</dt><dd>{platform}</dd></div>
          <div><dt>Stack</dt><dd>{tech}</dd></div>
          <div><dt>Link</dt><dd>Private codebase</dd></div>
        </dl>
        <div class="narrative">
          {narrative}
        </div>
      </div>
      {detail_block(project)}
      {next_block(project)}
    </article>
  </main>
"""
    html += footer()
    write(f"work/{project['slug']}/index.html", html)


def page_concepts_index():
    cards = []
    for concept in CONCEPTS:
        d = concept["dir"]
        cards.append(f"""<a data-vt="{concept['slug']}" href="/concepts/{concept['slug']}/">
          <span class="feature-media"><img src="/assets/concepts/{d}/cover-sm.webp" srcset="/assets/concepts/{d}/cover-sm.webp 720w, /assets/concepts/{d}/cover.webp 1200w" sizes="(min-width: 960px) 18vw, 46vw" width="1200" height="900" alt="{e(concept['name'])} concept cover." loading="lazy" decoding="async"></span>
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
      <h1 class="page-title">Concept designs</h1>
      <p class="lede">Self-initiated concept designs with fictional sample data, not client work.</p>
      <div class="wall" aria-label="Concept covers">
        <div class="wall-plane">
          {''.join(cards)}
        </div>
      </div>
    </div>
  </main>
"""
    html += footer()
    write("concepts/index.html", html)


def page_concept(concept):
    d = concept["dir"]
    shots = []
    cover = f"""<figure class="shot">
        <img src="/assets/concepts/{d}/cover.webp" width="1200" height="900" alt="{e(concept['name'])} concept cover." decoding="async">
        <figcaption>Cover</figcaption>
      </figure>"""
    shots.append(cover)
    for shot in concept["screens"]:
        shots.append(f"""<figure class="shot">
        <img src="/assets/concepts/{d}/{shot['file']}" width="{shot['w']}" height="{shot['h']}" alt="{e(shot['alt'])}" loading="lazy" decoding="async">
        <figcaption>{e(shot['caption'])}</figcaption>
      </figure>""")
    html = head(
        f"{concept['name']} · Concept · Haseeb Asim",
        concept["summary"] + " Self-initiated concept with fictional sample data, not client work.",
        f"/concepts/{concept['slug']}/",
        f"/assets/concepts/{d}/cover.webp",
    )
    html = html.replace("<body>", '<body class="has-progress">\n  <div class="progress" aria-hidden="true"></div>', 1)
    html += nav()
    html += f"""  <main id="main" class="page">
    <article class="wrap">
      <p class="kicker"><a href="/concepts/">Concepts</a> · Concept</p>
      <h1 class="page-title vt-title">{e(concept['name'])}</h1>
      <p class="lede">{e(concept['summary'])}</p>
      <p class="notice">Self-initiated concept design. Names, brands, and figures are fictional sample data, not client work.</p>
      <div class="stack" data-vt-hero>
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
        <h2>How I work</h2>
        <ol class="plain">
          <li>A short call to understand the workflow and what success looks like.</li>
          <li>A working prototype early, so you see results before the big spend.</li>
          <li>Daily or every-other-day updates.</li>
          <li>Clean handoff docs and a walkthrough video.</li>
        </ol>
      </section>
      <section class="block" id="services">
        <h2>What I build</h2>
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
        <h2>Tools</h2>
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
