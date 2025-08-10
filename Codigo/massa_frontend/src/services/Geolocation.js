import { ref } from 'vue';
import axios from 'axios';
import { countries } from 'countries-list';
import API_URL from '@/config/api';

export function getCountryName(code) {
    return countries[code]?.name || 'Unknown country';
}

async function getIpLocation() {
    const url = 'https://checkip.amazonaws.com';
    try {
        const response = await axios.get(url);
        return response.data.trim();
    } catch (error) {
        console.error("Error retrieving IP:", error);
        return null;
    }
}

export async function getIpInfos() {
    const ipInfo = ref(null);
    const ipError = ref(null);
    const ip = await getIpLocation();
    if (!ip) {
        ipError.value = "Unable to retrieve IP";
        return;
    }

    const token = 'cb2eeb132673ac'; // Replace with your ipinfo.io token
    const url = `https://ipinfo.io/${ip}?token=${token}`;

    try {
        const response = await fetch(url, {
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
            method: 'GET'
        });
        const data = await response.json();
        ipInfo.value = {
            country: getCountryName(data.country),
            city: data.city,
        };

        return ipInfo.value;

    } catch (error) {
        console.error("Error retrieving IP info:", error);
        console.error("Error details:", error.toJSON());
        ipError.value = "Unable to retrieve IP info";
    }
}

export async function getAllUsersIpInfos() {
    try {
        const response = await axios.get(`${API_URL}/users/all/addresses`);
        return response.data;
    } catch (error) {
        console.error("IPs error:", error);
        throw error;
    }
}

