import axios from "axios";
import API_URL from "@/config/api";
class StatsService {
    async getStats() {
        try {
            const response = await axios.get(`${API_URL}/stats/monthly`);
            return response.data;
        } catch (error) {
            console.error("Stats error:", error);
            throw error;
        }
    }
}
export default new StatsService();