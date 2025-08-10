import axios from 'axios';
import API_URL from '@/config/api';

class LoginService {
    
    async login(username, password) {
        try {
            const response = await axios.post(`${API_URL}/users/login`,
                {
                    username,
                    password
                }
            );

            if(response.status === 200) {
                const access_token = response.data.token;
      
                localStorage.setItem('token', access_token);  
                return access_token;
            }
        } catch (error) {
            console.error("Login error:", error);
            throw error;
        }
    };

    logout() {
        localStorage.removeItem('token');
    };
}

export default new LoginService();