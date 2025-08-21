# Implementation Plan
## Phase 1: Backend Setup & Data Modeling (Strapi)
Goal: A fully configured Strapi backend with data structures and user permissions.

### Create Strapi Project:

```bash
npx create-strapi-app@latest backend --quickstart
cd backend
```
(This uses SQLite for development. We'll change to PostgreSQL for production later).

### Create Content-Types in Admin Panel (Settings > Content-Type Builder):

- Collection: category
    - name (Text, Short text)

- Collection: event
    - title (Text, Short text)
    - description (Text, Long text)
    - date (Date, DateTime)
    - location (Text, Short text)
    - capacity (Number, Integer)
    - signup_deadline (Date, DateTime)
    - contact_info (Text, Long text) // Info provided by event creator

- Relations:
    - event has many categories (Categories will be freeform, created on the fly)
    - event belongs to one user (as the responsible_person) // This is a critical relation
    - event has many chat_messages
    - event has many rsvps

- Collection: chat-message
    - message (Text, Long text)
    - Relations:
        - chat-message belongs to one event
        - chat-message belongs to one user (author)

- Collection: rsvp
    - status (Enumeration: yes, no, maybe)
    - Relations:
        - rsvp belongs to one event
        - rsvp belongs to one user

- Configure User Roles & Permissions (Settings > Users & Permissions Plugin > Roles):
    - Public:
        - auth - local callback: Open (for login)
        - user - find, findone: Open (for viewing user profiles/tags)
        - event - find, findone: Open
        - category - find, findone: Open
    - Authenticated:
        - Inherits all Public permissions.
        - chat-message: create (Users can only create messages. find and findone are public).
        - rsvp: create, update (Users can set and change their own RSVP until the deadline). We will write custom logic to enforce the "own RSVP" and deadline rules.

    - Board:
        - Inherits all Authenticated permissions.
        - event: create, update, delete
        - chat-message: delete (Can delete any message)
        - user: find (Can access the list of users)

- Customization (Optional but Recommended for deadlines):

We will write custom code in /src/api/rsvp/controllers/rsvp.js to prevent creating/updating an RSVP if the event's signup_deadline has passed.

## Phase 2: Frontend Foundation (Vue 3 + Vite)
Goal: A working Vue app with routing, state management, and UI library.

- Scaffold Vue Project:

```bash
npm create vite@latest frontend -- --template vue
cd frontend
npm install
```
- Install Dependencies:

```bash
npm install vue-router@4 pinia axios
npm install vuetify@^3.3.0 @mdi/font
```
- Configure Vuetify & Router: Create the necessary plugins and initialization files as discussed in previous plans.

- Set up API Client: Create a src/services/strapi.js file that uses axios to connect to http://localhost:1337/api, including automatic JWT token attachment to requests.

## Phase 3: Authentication & Core Views
Goal: Users can log in and see a list of events.

- Build Login View: A form that sends a request to POST /api/auth/local and stores the received JWT in Pinia and localStorage.
- Create Authentication Store (Pinia): A store to hold the user object, jwt token, and methods for login, logout, and checkAuth.
- Implement Route Guards: Protect routes like /admin and /event/create to require authentication and the board role.
- Build Event List View (/): Fetches data from GET /api/events?populate=* and displays events in cards.

## Phase 4: Event Interaction Features
Goal: Implement all user stories for events, RSVP, and chat.

- Event Detail View (/event/:id):
    - Fetches a single event with all populated data (responsible_person, categories, chat_messages, rsvps).
    - Displays all event information.

- RSVP Component:
    - Checks if the current user has an existing RSVP for this event.
    - Displays Yes/No/Maybe buttons.
    - Logic: Before sending POST /api/rsvps (or PUT /api/rsvps/:id), the frontend checks if the current time is past the event's signup_deadline. If it is, it disables the buttons. The backend also performs this check for security.

- RSVP List Component: Fetches GET /api/rsvps?filters[event][$eq]=X&populate=user to show who answered what.

- Chat Component:
    - Fetches existing messages (GET /api/chat-messages?filters[event][$eq]=X&populate=user).
    - Has a form to submit a new message (POST /api/chat-messages with data: { message: "text", event: id, user: id }).
    - Displays messages with username and timestamp.
    - For Board Users: Adds a delete button next to each message.

## Phase 5: Admin Features & Final Polish
Goal: Implement board-specific features and polish the UI.

- Event Create/Edit Form: Forms for board members to manage events. The "Responsible Person" field will be a dropdown fetched from GET /api/users.
- User List View (/admin/users): A simple table showing users, their roles, and active status (fetched from GET /api/users). Only accessible to board members.
- Add User "Tag" (Role): In the Strapi admin panel, you can add a custom field like role_tag (Text) to the User collection. This can be filled manually for now (e.g., "Project Manager", "First-Year Rep").
- Active/Inactive: Add a boolean is_active field to the User collection in Strapi. Filter the user list based on this.
- Error Handling & Loading States: Add these throughout the application for a better user experience.
- Responsive Design: Use Vuetify's grid system to ensure it works on mobile.

## Phase 6: Deployment Preparation
Goal: Prepare the application for deployment on your server.

- Backend:
    - Change config/database.js to use PostgreSQL instead of SQLite for production.
    - Set environment variables for database connection string, JWT secret, etc.
    - Run npm run build to create a production build.

- Frontend:
    - Set the VITE_STRAPI_API_URL environment variable to your production server URL (e.g., https://api.yourdomain.com).
    - Run npm run build to create static files in the dist folder.
- Deployment: You will need:
    - A server (Ubuntu VPS is common).
    - PM2 process manager to run the Strapi backend.
    - A web server (Nginx) to serve the Strapi backend and the Vue frontend static files (or host the frontend on Netlify/Vercel).