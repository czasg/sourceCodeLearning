from itsdangerous import URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer
import hashlib

if __name__ == '__main__':
    s = URLSafeTimedSerializer('cza', salt='cookie-session', serializer=TaggedJSONSerializer(), signer_kwargs={
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1,
    })

    # {'username2': 'are you ok'}
    # eyJ1c2VybmFtZTIiOiJhcmUgeW91IG9rIn0.XeDGEw.WgJXqS1A3B6UigZ23umuQf-QKdE
    # eyJ1c2VybmFtZTIiOiJhcmUgeW91IG9rIn0.XeDIQw.PSqxZeT5L8uQ4RGbt0UQC-WvN7Y
    result = s.loads('eyJ1c2VybmFtZTIiOiJhcmUgeW91IG9rIn0.XeDIQw.PSqxZeT5L8uQ4RGbt0UQC-WvN7Y')
    print(result)
