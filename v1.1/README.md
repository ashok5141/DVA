# My plan is to build a Secure application with all components involved


## Stages 
- **v1.1** Docker image with Ubuntu having MySQL DB, login, Register, Profile, New post, Logout
- **v1.0** Developed docker image with Ubuntu having MySQL DB, login, Register pages

### Configuration 
- Create a Python virtual environment on this path with the below commands
```bash
python3 -m venv docker #it will create new python virtual environemt name docker
source docker/bin/activate #It will start the environment from docker directory created in above
```
### Installation
```bash
docker images # Check any images
docker rmi <Image ID> # It will delete perticular Image
docker rmi -f $(docker images -aq)  # Carefull it delete all images

# Start the Website
# Rebuild containers with the updated code
docker compose down
docker compose up --build
```
### Credentials DVA
- User:Password - admin:admin123



> Wish to include JWT, OAuth, GraphQL, SOP, and CORS Features possible

#### Key Features Added in the feature
- Secure Password Hashing: Uses pbkdf2_sha256 for password storage.
- MySQL Integration: Dedicated container with persistent storage.
- Docker Networking: Services communicate via Docker’s internal network.
- Health Checks: Ensures MySQL is ready before backend starts.



#### Next Steps
- Add Frontend: Use React/HTML/CSS for a UI.
- JWT Authentication: Return tokens on successful login.
- Input Validation: Sanitize username/password inputs.
- HTTPS: Add SSL/TLS with Nginx reverse proxy.
- Want to expand any specific part (e.g., adding email verification)?


