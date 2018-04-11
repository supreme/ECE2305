from datetime import datetime
import requests


if __name__ == '__main__':

    data = {
        'room_id': 1,
        'breach_time': datetime.now()
    }

    response = requests.post('http://127.0.0.1:8080/api/', data=data)
    print(response.text)
