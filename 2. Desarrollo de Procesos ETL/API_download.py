import requests
import json



url = "https://api-nba-v1.p.rapidapi.com/standings"

querystring = {"league":"standard","season":"2021","division":"southeast"}

headers = {
	"X-RapidAPI-Key": "",
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
print(response.json())

if response.status_code == 200:
    data = response.json()

    with open("divisions.json", "w") as file:
        json.dump(data, file)

    print("JSON descargado y guardado correctamente")
else:
    print(f"Error en la solicitud. Código de respuesta: {response.status_code}")
    print(response.text)
