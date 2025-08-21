# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).
# EventHub - Student Organisation Event Manager
A Vue-based event management system for student organisations with real-time updates.

## Features
- Role-based authentication (Board/Member)
- Event creation with categories and deadlines
- Yes/No/Maybe response system
- Real-time event chats
- Responsive design
- Real-time updates

## Tech Stack
- Vue 3 (Composition API)
- Vuetify UI Framework
- Firebase (Firestore, Authentication, Hosting)
- Vue Router & Pinia

## Project Setup
```bash
# Install dependencies
npm install

# Compile and hot-reload for development
npm run dev

# Compile and minify for production
npm run build

# Deploy to Firebase
npm run deploy
```

## Firebase Configuration
- Create a new Firebase project
- Enable Authentication (Email/Password)
- Create a Firestore database
- Copy your config to .env.local:

```text
VUE_APP_FIREBASE_API_KEY=your_api_key
VUE_APP_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
VUE_APP_FIREBASE_PROJECT_ID=your_project_id
VUE_APP_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
VUE_APP_FIREBASE_MESSAGING_SENDER_ID=123456789
VUE_APP_FIREBASE_APP_ID=your_app_id
```
## Usage
### For Board Members:
- Log in with board credentials
- Access admin panel from navigation
- Create events with details, categories, and deadlines
- Monitor responses and chat activity

### For Members:
- Log in with member credentials
-View upcoming events on dashboard
- Respond to events (Yes/No/Maybe)
- Participate in event-specific chats

## Firestore Security Rules
```text
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Events collection
    match /events/{eventId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'board';
      
      // Event responses subcollection
      match /responses/{responseId} {
        allow read: if request.auth != null;
        allow create, update: if request.auth != null && 
          request.auth.uid == responseId;
        allow delete: if false;
      }
      
      // Event chat subcollection
      match /chat/{messageId} {
        allow read: if request.auth != null;
        allow write: if request.auth != null;
      }
    }
    
    // Users collection
    match /users/{userId} {
      allow read: if request.auth != null;
      allow write: if request.auth.uid == userId;
    }
  }
}
```