export function getCsrfToken() {
  const match = document.cookie.match(/csrf_access_token=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : '';
}