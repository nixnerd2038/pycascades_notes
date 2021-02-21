# Notes
## What is urllib3?
- HTTP Client lib
- Extends the stdlib with things like SSL verification
## Why release breaking changes
- Keep up with new innovations, like QUIC
- HTTP/2 and HTTP/3 compliance
- TLS 1.0/1.1 Deprecated, should be removed
- CommonName deprecated, should be removed
## What features are coming in urllib3 v2
- Drop 2.7 and 3.5 support
- Deprecate CommonName in favor of SAN
- Type Hints
- Modern security by default
## What are we doing to not break the Python-verse
- Opt-in when ready
- Backporting security changes to 1.2
- Most major changes are outside the GET functionality
## Best mitigations for breaking changes
- Talk to users
- Be aware that not all breaking changes are in code
- Documentation
- Good error messages with URLs
- Test your own code
- Funding and time to spend on development
- Bring in test suites of your largest stakeholders and dependants
  - In urllib3's case this would be the requests lib
