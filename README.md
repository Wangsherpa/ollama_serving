# Ollama Gateway

Ollama Gateway is a FastAPI-based project that aims to provide a gateway for interacting with Ollama's backend services. 
It supports all the essential endpoints from Ollama's server, with plans to add extra features like authentication and rate limiting.

## Features (In Progress)

1. **Full Endpoint Support**
   - Replicates the core endpoints provided by Ollama's backend server.

2. **Authentication** 
   - Implements secure user authentication with JWT tokens.

3. **Role-Based Access Control (RBAC)**
   - Controls access to different endpoints based on user roles (e.g., admin, user, etc).

4. **Rate Limiting**
   - Limits the number of requests users can make within a certain period to prevent abuse.
