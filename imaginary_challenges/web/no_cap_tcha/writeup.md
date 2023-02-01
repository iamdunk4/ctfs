# Looking at the source code

## Brute force

Since the https://nocapcaptcha.fly.dev/captcha get request gave us the image and the captcha answer, my first approach was trying to brute force like 3000 captchas and save them in a file. Then using the file that contain the image it was only analysing the image and look at the file if we had the answer to the captcha.

In a scenario where the server has 1 million captchas saved to be served it would not be possible in a time fashion way.

I looked at the code and I notice two things:

## Session

It seems that the cookie is a dictionary that has some attributes, one of them is the captcha answer and another is the count. If we have 3 or more counts or right captchas answers we get the flag. But this cookie is signed using the followed lines of code:

```
session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)
session_cookie = session_serializer.dumps(dict(session))
response = make_response()
headers = {
    "cookie": f"{app.session_cookie_name}={session_cookie}; Path=/; HttpOnly"
}
```

It seems that is signed by the app, but it can be default signing and maybe we can deserialize it. With the help of a board member of imaginary ctf i found the right sources and was able to decode it using a tool called flask-unsign. 

```
cd /home/dunk4/.local/lib/python3.10/site-packages/flask_unsign
python3 __main__.py -d -c <cookie_here>
```

So my process was the following, I enter some answer like "test" and then capture the request with burp, copy the cookie to flask-unsign, ge the right answer continue with the request. After 3 right captchas i got the flag(`ictf{what_do_you_mean_this_isn't_realistic?_11452}`).

I tried to use the following(https://gist.github.com/aescalana/7e0bc39b95baa334074707f73bc64bfe):

```
#!/usr/bin/env python
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer

class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
	# Override method
	# Take secret_key instead of an instance of a Flask app
	def get_signing_serializer(self, secret_key):
		if not secret_key:
			return None
		signer_kwargs = dict(
			key_derivation=self.key_derivation,
			digest_method=self.digest_method
		)
		return URLSafeTimedSerializer(secret_key, salt=self.salt,
		                              serializer=self.serializer,
		                              signer_kwargs=signer_kwargs)

def decodeFlaskCookie(secret_key, cookieValue):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer(secret_key)
	return signingSerializer.loads(cookieValue)

# Keep in mind that flask uses unicode strings for the
# dictionary keys
def encodeFlaskCookie(secret_key, cookieDict):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer(secret_key)
	return signingSerializer.dumps(cookieDict)

if __name__=='__main__':
	sk = 'youWillNeverGuess'
	sessionDict = {u'Hello':'World'}
	cookie = encodeFlaskCookie(sk, sessionDict)
	decodedDict = decodeFlaskCookie(sk, cookie)
	assert sessionDict==decodedDict
```

I tried as well making a script using the flask-unsign but did not find the documentation to do it.

## References

https://blog.paradoxis.nl/defeating-flasks-session-management-65706ba9d3ce
https://pypi.org/project/flask-unsign/
https://github.com/Paradoxis/Flask-Unsign