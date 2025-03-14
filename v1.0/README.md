# My plan is to build a Secure application with all components involved

> Wish to include JWT, OAuth, GraphQL, SOP, CORS Features possiable

## Key Features
- Secure Password Hashing: Uses pbkdf2_sha256 for password storage.
- MySQL Integration: Dedicated container with persistent storage.
- Docker Networking: Services communicate via Docker’s internal network.
- Health Checks: Ensures MySQL is ready before backend starts.



## Next Steps
- Add Frontend: Use React/HTML/CSS for a UI.
- JWT Authentication: Return tokens on successful login.
- Input Validation: Sanitize username/password inputs.
- HTTPS: Add SSL/TLS with Nginx reverse proxy.
- Want to expand any specific part (e.g., adding email verification)?



## Stages
- **v1.0** Developed docker image with Ubuntu having MySQL DB, Login, Register pages
