เอกสารนี้รวบรวม "ข้อสังเกตอีเมลหลอกลวง" (red flags) แบบต่างๆ เพื่อ

- นำมาสร้างเป็นแผนการโจมตี (attack scheme)
- นำมาสร้างเป็นบทเรียนให้กับผู้เข้าร่วมการฝึก

# Look alike URL links

For example, `drive--google.com` instead of `drive.google.com`.
This can channel victims to attacker controlled website instead of legitimate ones the victim though they were accessing.

Or you could use subdomains to imitate real domain. Like:
`http://myaccount.google.com-securitysettingpage.ml-security.org/signonoptions/`

# Mismatched sender address and sender name

Scammer will try to assume the identity of some party trusted by victim in order to exploit that trust.
Some will try to set sender name to the trusted party, which can be done easily.
However, using the email address of the trusted party is not as easily done, leading to the mismatch.

They can also try to register an email address similar to the trusted party.

# Use of image to avoid scam filter

Content inside images can be [harder][1] to process by scam filter.
Some filter will skip trying to parse information inside image.

# Suspicious content

Receiver of emails should be vary of scam tactics used in email content such as:
- Using urgency to reduce thinking time
- Unrealistic offer
- Language use unfit to the sender assumed identity

# Hide payload in URL fragment

URL fragment is usually not logged by server.
Therefore, client JavaScript can read URL fragment and activate malicious behaviour
while log scanner did not see the URL that would trigger malicious behaviour.

- [ ] TODO: double check validity

# Use legitimate website to send malicious message

For example, add seller's note to an invoice on a trusted platform instructing victim to contact back via alternative channel.

# Use legitimate platform to redirect

google.com/amp allows creating arbitrary site?
https://google.com/amp/tinyurl.com/y7u8ewlr

# Asking for verification code

Attacker can try to send a message asking for verification code
that you got from a real verification code email.

# Mismatched display text and href

For example,

```html
<a href="https://malicious-site.com">https://trusted-site.com</a>
```

# References

[1]: https://phishingquiz.withgoogle.com/
[2]: https://portswigger.net/research/concealing-payloads-in-url-credentials
