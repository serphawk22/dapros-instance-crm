let baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
if (baseUrl && !baseUrl.startsWith('http://') && !baseUrl.startsWith('https://')) {
  baseUrl = 'https://' + baseUrl;
}
baseUrl = baseUrl.replace(/\/+$/, '');

// In browser production on Vercel, route via same-origin rewrite (/api/backend) to eliminate CORS entirely
export const API_BASE_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
  ? '/api/backend'
  : baseUrl;

// WhatsApp destination (digits only, no "+"). Configure via NEXT_PUBLIC_WHATSAPP_NUMBER.
export const WHATSAPP_NUMBER = (process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || "919502901416").replace(/\D/g, "");
export const WHATSAPP_DISPLAY = (process.env.NEXT_PUBLIC_WHATSAPP_DISPLAY || "+91 9502901416");
export const WHATSAPP_LINK = `https://wa.me/${WHATSAPP_NUMBER}`;
