import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'X-API-KEY': 'ioxnsaunxa',
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
