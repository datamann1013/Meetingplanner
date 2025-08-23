# EventHub - Student Organisation Event Manager

A self-hosted, modern event management system for student organisations. Built with Strapi (backend) and Vue 3 (frontend).

## Features

- **User Roles:** Members and Board members.
- **Event Management:** Board members can create, edit, and delete events.
- **RSVP System:** Users can respond with Yes, No, or Maybe until a set signup deadline.
- **Event Chat:** Live discussion for each event.
- **Transparency:** Everyone can see who has answered what for an event.
- **Moderation:** Board members can delete chat messages and manage users.
- **User Tags:** Assign custom roles (e.g., "Treasurer", "Lead Volunteer") to users.
- **Active/Inactive:** Mark members as active or inactive.

## Tech Stack

### Backend
- **Strapi** (Headless CMS)
- **PostgreSQL** (Production Database)
- **JWT** (Authentication)

### Frontend
- **Vue 3** (Composition API)
- **Vite** (Build Tool)
- **Pinia** (State Management)
- **Vue Router** (Navigation)
- **Vuetify** (UI Component Library)
- **Axios** (HTTP Client)

## Project Setup

### Prerequisites
- Node.js (v18 or higher)
- A PostgreSQL database (for production)
- npm or yarn

### 1. Backend (Strapi) Setup

```bash
# Clone the repository (when available)
# git clone <your-repo>
# cd backend

# Or create a new Strapi project
npx create-strapi-app@latest backend --quickstart
cd backend

# Install dependencies (if cloning)
npm install

# Start the development server
npm run develop
```

Access the Strapi admin panel at http://localhost:1337/admin to create your first admin user.

**Configuration:**

- In the Admin Panel, go to Settings > Content-Type Builder and create the Collections as described in the plan.
- Go to Settings > Users & Permissions Plugin > Roles and configure the permissions for Public, Authenticated, and Board roles.

### 2. Frontend (Vue) Setup
```bash
# Navigate to the frontend directory
cd ../frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Access the application at http://localhost:5173.

#### Environment Variables:
Create a .env file in the frontend directory:

```env
VITE_STRAPI_API_URL=http://localhost:1337/api
```
## Deployment
This setup is designed for deployment on a Linux server (e.g., Ubuntu).

### Backend Deployment (Strapi + PostgreSQL):
1. Server Setup: Install Node.js, PM2, Nginx, and PostgreSQL on your server.
2. Database: Create a new PostgreSQL user and database for Strapi.
3. Configuration: Update the backend's config/database.js and config/server.js files for production settings (use environment variables for secrets!).
4. Process Management: Use PM2 to run npm start in the backend directory to keep Strapi running.
5. Web Server: Configure Nginx as a reverse proxy to forward requests to your Strapi port (e.g., 1337).

### Frontend Deployment (Vue):
1. Build: Run npm run build in the frontend directory. This creates a dist folder with static files.
2. Serve with Nginx: Configure a separate Nginx server block to serve the contents of the dist folder as a static website. Point your domain (e.g., app.yourdomain.com) to this.

## Usage
- Board Members: Log in and access the Admin Panel via the link in the navigation. You can create events and manage users there. You can also delete chat messages directly from the event view in the main app.
- Members: Log in to view events, RSVP, and participate in event chats.
- Signup Deadline: After an event's signup deadline passes, the RSVP buttons will be disabled for everyone.
  
## Delayed features
Customization (Optional but Recommended for deadlines):
We will write custom code in /src/api/rsvp/controllers/rsvp.js to prevent creating/updating an RSVP if the event's signup_deadline has passed.

Proper board member check through Strapi. Go over authenticationwith that in mind later.