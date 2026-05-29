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
- Swagger/OpenAPI - https://priyamfoods-backend.onrender.com/docs
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

```bash
Add .env file in backend with admin phone number to receive orders
create priyam-foods/backed/.env
ADMIN_WHATSAPP_NUMBER=+4912345678910
ADMIN_TELEGRAM_NUMBER=+4912345678910

Through Docker:
docker-compose up --build
* Make sure Docker Desktop is installed & running.
(normally check the app at http://localhost:4173/ or Docker assigns a random available port)

or

Manually Through Python:

Backend:
   cd backend
   # Delete old venv
   Remove-Item -Recurse -Force venv

   # Create fresh venv using your current Python
   python -m venv venv

   # Activate
   .\venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Run
   uvicorn main:app --reload

Frontend:
   cd frontend
   npm install
   npm run dev
```

### Future Improvements
```
Payment integration
Admin dashboard
Order history storage (DB)
Authentication system
```
### App Screen
<img width="324" height="854" alt="image" src="https://github.com/user-attachments/assets/be629c10-de1b-47b5-a0c0-a4fd827c7ab8" />

### Author
Ravivarma Singaravelu
