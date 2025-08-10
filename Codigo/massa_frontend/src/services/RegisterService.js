import axios from "axios";
import API_URL from "@/config/api";

class RegisterService {

    async register(userData) {
        try {
            const response = await axios.post(`${API_URL}/users/register`, userData);

            if(response.status === 201) {
                const access_token = response.data.token;

                localStorage.setItem('token', access_token);
                return access_token;
            }
        } catch (error) {
            console.log("Register error:", error);
            throw error;
        }
    }
}

export default new RegisterService();