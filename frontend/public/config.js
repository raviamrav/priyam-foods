const hostname = window?.location?.hostname || "localhost";

let API_URL;

if (hostname === 'localhost' || hostname === '127.0.0.1') {
  API_URL = 'http://localhost:8000';
} else if (hostname.includes('vercel.app') || hostname.includes('priyam-foods')) {
  API_URL = 'https://priyamfoods-backend.onrender.com';
} else {
  API_URL = `${window.location.protocol}//${hostname}:8000`;
}

window.APP_CONFIG = { API_URL }