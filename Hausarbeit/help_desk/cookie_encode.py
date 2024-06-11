from itsdangerous import URLSafeSerializer
from itsdangerous import base64_decode


#s = URLSafeSerializer(SECRET_KEY)

encrypted_cookie = 'eyJ1c2VybmFtZSI6Ik1hcnZpbiJ9.Zj55jg.bGtHVtItOddNY7nrtcg9ehzAUL0'

print(base64_decode(encrypted_cookie.split(".")[0]))

#print(s.loads(encrypted_cookie))