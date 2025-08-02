import axios from 'axios'

const apiClient = axios.create({
<<<<<<< Updated upstream
  baseURL: import.meta.env.VITE_API_URL || 'backend:8000/api/v1',
  headers: {
=======
  baseURL: import.meta.env.VITE_API_URL || 'http://backend:8000/api/v1/',
  headers: {
    Accept: "application/json",
>>>>>>> Stashed changes
    'Content-Type': 'application/json',
  },
})

export default apiClient
