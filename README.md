# Priyam Foods – WhatsApp Food Ordering App

## Live Demo
Frontend: https://priyamfoods.vercel.app  
Backend API: https://priyamfoods-backend.onrender.com  

---

## Overview
A simple fullstack food ordering web application where users can:
- Browse menu
- Select items and quantity
- Enter delivery details
- Send order via WhatsApp to admin

This project demonstrates integration of frontend, backend, and third-party communication (WhatsApp).

---

## Tech Stack
- Frontend: Vue 3 (Vite), TypeScript, Tailwind CSS
- Backend: FastAPI (Python)
- Deployment: Render (Backend), Vercel (Frontend)
- Tools: Docker, Git, GitHub

---

## Features
- Dynamic menu loading from API
- Order calculation with total price
- WhatsApp message generation with order details
- Contact download via vCard
- Responsive UI (mobile-friendly)

---

## Architecture
Frontend (Vercel)
   ↓ API call
Backend (Render)
   ↓
Generates WhatsApp message → opens wa.me link

---

## Challenges & Solutions
- CORS issues → solved via FastAPI middleware
- Environment config → handled via dynamic config.js
- Mobile UI issues → fixed using Tailwind responsive design
- Docker networking → debugged API connection inside container

---

## How to Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
Frontend
cd frontend
npm install
npm run dev

### Future Improvements
Payment integration
Admin dashboard
Order history storage (DB)
Authentication system

Author
Ravivarma Singaravelu
