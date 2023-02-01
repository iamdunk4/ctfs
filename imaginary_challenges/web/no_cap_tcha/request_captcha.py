import requests

headers = {
        "cookie": "session=.eJwNy70KAjEMAOB3yWwhl0t_zlFcigpOek6Spg0cgoq6ie9u9-_7gsoT1jBuTn53zDnl_WFLOPPlPMMK9P2y6-dxa_du2iBWRs8psUkIiIIYm6VEPKEGima-UtD-ltq9klkrVV20iI4bqSvo2U02VBUTwYTw-wNnbySV.Y9mdCA.9D5vCMHZ2if6tkjpSAdyAG3_P9c"
    }

f = open("cap", "w+")

caps = []
for i in range(2000):
	res = requests.get("https://nocapcaptcha.fly.dev/captcha", headers=headers).json()
	cap = res["cap"]
	image = res["image"]
	f.write(cap + ":" + image[-40:] + "\n")
f.close()


