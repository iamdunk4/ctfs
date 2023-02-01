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

def decodeFlaskCookie(cookieValue):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer("")
	return signingSerializer.loads(cookieValue)

if __name__=='__main__':
	cookie = '.eJwNy7sKAjEQBdB_mdrAbMzTXtAVLNaIpcxOcmERVNRO_HfTn_MllSdtaHspI5-mcToezrvCYV9ypBXp-4Xr53Fr927aIJjX3qXkICEwC3NsSMm6zBpsBHy1QftbavdqgTZXNRGRjWtWzczemYyhqkCEE9PvD3wyJLw.Y9qHLA.06Vo7hZiZGQWHnGP2_bGykIZC-A'
	decodedDict = decodeFlaskCookie(cookie)
	print(decodedDict)
