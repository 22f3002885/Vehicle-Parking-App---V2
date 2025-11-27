import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000', // your Flask backend
})

// Attach auth token if present
api.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers['Authentication-Token'] = token
  }
  return config
})

export default api
