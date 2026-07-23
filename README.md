<div align="center">

<img src="assets/logo.png" alt="Khouloud Fekih Psychology Platform logo" width="230">

# Khouloud Fekih Psychology Platform

### Multilingual Appointment Booking & Patient Management Web Application

**Flask · Python · SQLite · Jinja2 · HTML · CSS · JavaScript · Responsive Web Design**

<br>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](#technology-stack)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?logo=flask&logoColor=white)](#technology-stack)
[![SQLite](https://img.shields.io/badge/SQLite-Relational%20Database-003B57?logo=sqlite&logoColor=white)](#database-design)
[![Jinja](https://img.shields.io/badge/Jinja2-Template%20Engine-B41717?logo=jinja&logoColor=white)](#technology-stack)
[![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?logo=html5&logoColor=white)](#technology-stack)
[![CSS3](https://img.shields.io/badge/CSS3-Premium%20UI-1572B6?logo=css3&logoColor=white)](#technology-stack)
[![JavaScript](https://img.shields.io/badge/JavaScript-Interactions-F7DF1E?logo=javascript&logoColor=black)](#technology-stack)
[![Multilingual](https://img.shields.io/badge/Multilingual-FR%20%7C%20AR%20%7C%20EN-CB846A)](#multilingual-experience)
[![Responsive](https://img.shields.io/badge/Design-Responsive-51384F)](#responsive-design)
[![Project](https://img.shields.io/badge/Project-Full--Stack%20Web%20Application-7B506F)](#project-context)

<br>

**A complete multilingual web platform connecting a clinical psychologist with patients through online appointment requests, dedicated dashboards, notifications and private messaging.**

<br>

[Platform Overview](#overview) ·
[Features](#core-features) ·
[Screenshots](#platform-showcase) ·
[Installation](#installation) ·
[Architecture](#system-architecture)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Project Context](#project-context)
- [Business Need](#business-need)
- [Project Objectives](#project-objectives)
- [Core Features](#core-features)
- [Platform Showcase](#platform-showcase)
  - [Public Homepage](#public-homepage)
  - [Appointment Request Form](#appointment-request-form)
  - [Patient Appointment Space](#patient-appointment-space)
  - [Patient Messaging](#patient-messaging)
  - [Administrator Dashboard](#administrator-dashboard)
  - [Appointment Request Management](#appointment-request-management)
- [Multilingual Experience](#multilingual-experience)
- [Patient Journey](#patient-journey)
- [Administrator Workflow](#administrator-workflow)
- [Appointment Management](#appointment-management)
- [Messaging System](#messaging-system)
- [Notification System](#notification-system)
- [Authentication and Access Control](#authentication-and-access-control)
- [System Architecture](#system-architecture)
- [Application Workflow](#application-workflow)
- [Database Design](#database-design)
- [Security Design](#security-design)
- [Technology Stack](#technology-stack)
- [Frontend Design](#frontend-design)
- [Responsive Design](#responsive-design)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Application Routes](#application-routes)
- [Testing the Platform](#testing-the-platform)
- [Deployment Considerations](#deployment-considerations)
- [Privacy and Data Protection](#privacy-and-data-protection)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Author](#author)
- [Acknowledgements](#acknowledgements)

---

## Overview

**Khouloud Fekih Psychology Platform** is a multilingual full-stack web application developed for a clinical psychologist based in Monastir, Tunisia.

The platform provides a unified digital environment where visitors and registered patients can:

- discover the psychologist and her approach;
- explore available psychological support services;
- create a patient account;
- request an appointment online;
- choose a consultation type;
- select a preferred date and time;
- follow the status of each request;
- receive notifications;
- communicate through a dedicated messaging space.

The psychologist accesses a separate professional area where appointment requests, patients, statuses and conversations can be managed.

```text
Public Website
      │
      ├── Psychologist Presentation
      ├── Services
      ├── Contact Information
      ├── Multilingual Content
      └── Appointment Call-to-Action
                 │
                 ▼
          Patient Authentication
                 │
                 ▼
       Appointment Request System
                 │
                 ▼
          Patient Dashboard
                 │
          ┌──────┴──────┐
          ▼             ▼
   Notifications     Messaging
          │             │
          └──────┬──────┘
                 ▼
        Professional Dashboard
                 │
          Appointment Management
```

The project demonstrates the implementation of a practical web product rather than an isolated technical prototype.

---

## Project Context

This platform was developed as a real-world website for **Khouloud Fekih**, a clinical psychologist.

It combines:

- a professional public website;
- a multilingual content system;
- patient account management;
- an appointment-request workflow;
- an administrator dashboard;
- appointment status management;
- a patient–psychologist conversation system;
- notifications;
- persistent database storage.

The project focuses on both technical implementation and user experience.

### Main development areas

- backend development with Flask;
- relational data management with SQLite;
- dynamic server-side rendering with Jinja2;
- user and administrator sessions;
- form handling and validation;
- appointment lifecycle management;
- multilingual interface design;
- right-to-left Arabic layout;
- responsive frontend development;
- dashboard design;
- private messaging;
- content management.

---

## Business Need

Independent healthcare and well-being professionals often rely on fragmented communication channels such as:

- telephone calls;
- social-media messages;
- informal messaging applications;
- manually managed calendars;
- paper appointment records.

These methods can create several difficulties.

### Appointment requests

Patients may not know:

- which consultation type to select;
- which dates are available;
- whether the request has been accepted;
- whether a response has been sent.

### Administrative organisation

The professional needs to:

- view all incoming requests;
- identify pending requests;
- confirm appointments;
- cancel appointments;
- search for a patient;
- sort requests by date;
- monitor daily activity.

### Communication

Patients may need a dedicated channel to ask practical questions related to their requests.

### Accessibility

The audience may prefer French, Arabic or English.

The platform centralises these interactions in one coherent application.

---

## Project Objectives

| Objective | Implemented Capability | Value |
|---|---|---|
| Present the professional activity | Public multilingual website | Improve digital presence |
| Simplify appointment requests | Online booking form | Reduce manual coordination |
| Track patient requests | Patient dashboard | Improve transparency |
| Manage appointment statuses | Admin dashboard | Centralise operations |
| Facilitate communication | Private messaging | Create a dedicated exchange channel |
| Inform users | Notifications | Improve follow-up |
| Serve a multilingual audience | French, Arabic and English | Increase accessibility |
| Persist application data | SQLite database | Maintain appointments and messages |
| Separate user roles | Patient and admin areas | Protect administrative functions |
| Improve usability | Responsive premium interface | Deliver a professional experience |

---

## Core Features

### Public website

- modern landing page;
- psychologist profile;
- presentation of the clinical approach;
- services and accompaniment categories;
- contact page;
- office images;
- location information;
- call-to-action buttons;
- multilingual navigation.

### Patient authentication

- account registration;
- patient login;
- session-based access;
- logout;
- protected patient pages.

### Appointment requests

- patient information;
- consultation type selection;
- preferred date;
- preferred time;
- general reason field;
- request creation;
- request confirmation page;
- controlled appointment statuses.

### Patient dashboard

- appointment history;
- request details;
- status indicators;
- cancellation of eligible pending requests;
- personal data display;
- notification access.

### Administrator dashboard

- global appointment statistics;
- total request count;
- pending request count;
- confirmed request count;
- cancelled request count;
- daily agenda;
- recent appointment requests;
- search;
- filters;
- sorting;
- status changes.

### Messaging

- patient–psychologist conversation;
- separate message styles by sender;
- message timestamps;
- persistent conversation history;
- administrator conversation management.

### Multilingual system

- French;
- Arabic;
- English;
- language selector;
- translated interface content;
- right-to-left Arabic layout.

---

# Platform Showcase

The following screenshots present the real platform experience and its principal workflows.

---

## Public Homepage

<p align="center">
  <img
    src="assets/accueil.png"
    alt="Khouloud Fekih psychologist website homepage"
    width="100%"
  >
</p>

The homepage introduces the psychologist through a refined editorial interface.

### Homepage elements

- professional identity;
- clinical psychologist title;
- location in Monastir;
- appointment availability;
- audience categories;
- primary appointment action;
- approach discovery;
- language selector;
- authenticated-user navigation;
- notification indicator.

### Main message

```text
Comprendre.
Apaiser.
Avancer.
```

The interface communicates a calm, professional and reassuring identity through:

- warm neutral colours;
- dark plum typography;
- peach accents;
- generous spacing;
- rounded visual components;
- elegant serif headings.

---

## Appointment Request Form

<p align="center">
  <img
    src="assets/formulaire.png"
    alt="Online psychology appointment request form"
    width="100%"
  >
</p>

The appointment page guides the patient through a simple request process.

### Request steps

```text
1. Enter contact information
2. Choose a consultation type
3. Select a preferred date and time
4. Provide an optional general reason
5. Submit the request
6. Wait for confirmation
```

### Form fields

- full name;
- phone number;
- email address;
- consultation type;
- preferred date;
- preferred time;
- general reason.

### Privacy-oriented wording

The form encourages patients to provide only a general reason and avoid transmitting unnecessary sensitive medical information.

### Appointment confirmation model

Submitting the form creates a request.

The appointment becomes definitive only after confirmation by the office.

---

## Patient Appointment Space

<p align="center">
  <img
    src="assets/espacepatientrendezvous.png"
    alt="Patient appointment dashboard"
    width="100%"
  >
</p>

The patient dashboard centralises all submitted appointment requests.

### Information displayed

- request number;
- consultation type;
- preferred date;
- preferred time;
- phone number;
- email;
- current status.

### Supported statuses

| Status | Meaning |
|---|---|
| Pending | The request is waiting for administrative review |
| Confirmed | The appointment has been approved |
| Cancelled | The request or appointment has been cancelled |

### Patient actions

Patients may review appointment information and cancel eligible pending requests.

### Visual status system

- green for confirmed requests;
- yellow for pending requests;
- red or soft pink for cancellation actions.

---

## Patient Messaging

<p align="center">
  <img
    src="assets/conversation.png"
    alt="Patient and psychologist messaging conversation"
    width="100%"
  >
</p>

The messaging space provides a dedicated conversation between the patient and the office.

### Messaging characteristics

- authenticated access;
- persistent message history;
- message timestamps;
- distinct visual styles by sender;
- message composition field;
- direct send action;
- conversation-specific display.

### Conversation design

```text
Patient message
      │
      ▼
Stored in database
      │
      ▼
Visible in admin messaging area
      │
      ▼
Administrator response
      │
      ▼
Visible in patient conversation
```

The system is intended for practical communication and appointment follow-up.

It should not be treated as an emergency service or as a replacement for a clinical consultation.

---

## Administrator Dashboard

<p align="center">
  <img
    src="assets/tableaudebord.png"
    alt="Psychologist administrator dashboard"
    width="100%"
  >
</p>

The professional dashboard provides an overview of appointment activity.

### Dashboard metrics

- total requests;
- pending requests;
- confirmed appointments;
- cancelled appointments.

### Operational views

- today's agenda;
- recent requests;
- appointment statuses;
- patient identification;
- consultation type;
- scheduled date and time.

### Administrator navigation

- dashboard;
- messaging;
- account identity;
- secure logout.

---

## Appointment Request Management

<p align="center">
  <img
    src="assets/gestiondemandes.png"
    alt="Administrator appointment request management"
    width="100%"
  >
</p>

The request-management interface enables the administrator to review and update appointment requests.

### Search and filtering

The administrator can search using:

- patient name;
- email;
- telephone number.

Requests can be filtered by:

- all statuses;
- pending;
- confirmed;
- cancelled.

Requests can also be sorted by appointment date.

### Administrative actions

- confirm;
- cancel;
- return to pending status;
- inspect contact information;
- review the request creation date.

### Appointment lifecycle

```text
New Request
     │
     ▼
Pending
  ┌──┴─────────────┐
  ▼                ▼
Confirmed       Cancelled
  │
  └──────► Pending again
           when authorised
```

---

## Multilingual Experience

The platform supports three interface languages.

| Language | Code | Direction |
|---|---|---|
| French | FR | Left to right |
| Arabic | AR | Right to left |
| English | EN | Left to right |

### French interface

French is used as the principal interface language.

### Arabic interface

The Arabic experience includes:

- translated navigation;
- translated homepage content;
- translated actions;
- right-to-left alignment;
- reversed interface flow where appropriate.

### English interface

The English version makes the public website accessible to a broader audience.

### Language-switching concept

```text
User selects language
        │
        ▼
Language saved for the session
        │
        ▼
Translation dictionary loaded
        │
        ▼
Templates render translated content
        │
        ▼
Arabic activates RTL presentation
```

---

## Patient Journey

The patient journey begins on the public website and continues inside a protected personal space.

```text
Visit Homepage
      │
      ▼
Explore Services
      │
      ▼
Create Account / Sign In
      │
      ▼
Request Appointment
      │
      ▼
Request Stored as Pending
      │
      ▼
View Request in Dashboard
      │
      ▼
Receive Status Update
      │
      ├── Confirmed
      ├── Pending
      └── Cancelled
      │
      ▼
Communicate through Messaging
```

### Journey goals

- minimise confusion;
- avoid unnecessary steps;
- provide visibility on appointment status;
- maintain a coherent visual experience;
- give the patient direct access to relevant information.

---

## Administrator Workflow

```text
Administrator Login
        │
        ▼
Professional Dashboard
        │
        ├── Review KPIs
        ├── View Today's Agenda
        ├── Inspect Recent Requests
        └── Open Messaging
                    │
                    ▼
          Appointment Management
                    │
             ┌──────┼──────┐
             ▼      ▼      ▼
          Confirm  Cancel  Pending
                    │
                    ▼
          Patient Status Updated
                    │
                    ▼
              Notification
```

### Professional objectives

- centralise requests;
- prioritise pending appointments;
- reduce manual tracking;
- simplify patient follow-up;
- maintain appointment traceability.

---

## Appointment Management

The appointment system represents the central business workflow of the application.

### Appointment data

Each request may contain:

```json
{
  "patient": "Patient name",
  "email": "patient@example.com",
  "phone": "00000000",
  "consultation_type": "First consultation",
  "desired_date": "2026-07-24",
  "desired_time": "10:00",
  "reason": "General reason",
  "status": "pending",
  "created_at": "2026-07-20 09:15:36"
}
```

### Consultation types

The available options can be configured according to the professional activity, for example:

- first consultation;
- psychological follow-up;
- child consultation;
- adolescent consultation;
- adult consultation;
- family consultation.

### Time-slot principles

The appointment form allows the patient to indicate a preferred moment.

The final appointment remains subject to confirmation by the office.

### Status transitions

| Current status | Available transition |
|---|---|
| Pending | Confirmed |
| Pending | Cancelled |
| Confirmed | Pending |
| Confirmed | Cancelled |
| Cancelled | Pending, if authorised |

---

## Messaging System

The platform provides separate patient and administrator messaging views.

### Patient side

The patient can:

- open the conversation;
- view previous messages;
- send a new message;
- identify message timestamps.

### Administrator side

The administrator can:

- view patient conversations;
- access conversation history;
- respond to a patient;
- monitor unread exchanges.

### Message data model

A message generally contains:

```json
{
  "id": 1,
  "sender_type": "user",
  "sender_id": 5,
  "recipient_type": "admin",
  "recipient_id": 1,
  "content": "Message content",
  "is_read": false,
  "created_at": "2026-07-23 15:53:57"
}
```

### Appropriate use

The messaging system is designed for:

- appointment questions;
- schedule clarification;
- practical follow-up;
- administrative communication.

It is not designed for:

- medical emergencies;
- immediate crisis intervention;
- sharing highly sensitive clinical records;
- replacing a consultation.

---

## Notification System

The notification indicator informs the patient about important platform updates.

### Potential notification events

- appointment request created;
- appointment confirmed;
- appointment cancelled;
- request returned to pending;
- new message received;
- administrative response available.

### Notification lifecycle

```text
System Event
     │
     ▼
Notification Created
     │
     ▼
Unread Counter Updated
     │
     ▼
User Opens Notification
     │
     ▼
Notification Marked as Read
```

---

## Authentication and Access Control

The platform separates patient and administrator access.

### Patient authentication

Patients access:

- their own appointment requests;
- their own notifications;
- their own conversation;
- their personal account.

### Administrator authentication

The administrator accesses:

- global appointment data;
- all relevant requests;
- professional statistics;
- patient conversations;
- administrative actions.

### Access separation

```text
Unauthenticated Visitor
        │
        ├── Public Pages
        ├── Login
        └── Registration

Authenticated Patient
        │
        ├── Personal Dashboard
        ├── Appointment Requests
        ├── Notifications
        └── Messaging

Authenticated Administrator
        │
        ├── Admin Dashboard
        ├── Request Management
        ├── Status Actions
        └── Admin Messaging
```

---

## System Architecture

<p align="center">
  <img
    src="assets/architecture.png"
    alt="Khouloud Fekih platform system architecture"
    width="100%"
  >
</p>

The application follows a server-rendered Flask architecture.

```mermaid
flowchart TB
    V[Public Visitor] --> WEB[Public Website]
    P[Patient] --> PORTAL[Patient Portal]
    A[Administrator] --> ADMIN[Admin Dashboard]

    WEB --> FRONT[Frontend Layer]
    PORTAL --> FRONT
    ADMIN --> FRONT

    FRONT --> HTML[HTML]
    FRONT --> CSS[CSS]
    FRONT --> JS[JavaScript]
    FRONT --> JINJA[Jinja2 Templates]

    HTML --> FLASK[Flask Application]
    CSS --> FLASK
    JS --> FLASK
    JINJA --> FLASK

    FLASK --> ROUTES[Routing]
    FLASK --> AUTH[Authentication]
    FLASK --> APPT[Appointment Logic]
    FLASK --> MSG[Messaging]
    FLASK --> NOTIF[Notifications]
    FLASK --> LANG[Localisation]
    FLASK --> CONTENT[Content Management]

    ROUTES --> DB[(SQLite Database)]
    AUTH --> DB
    APPT --> DB
    MSG --> DB
    NOTIF --> DB

    DB --> USERS[Users]
    DB --> APPOINTMENTS[Appointments]
    DB --> MESSAGES[Messages]
    DB --> NOTIFICATIONS[Notifications]
    DB --> ADMINS[Administrators]
```

### Presentation layer

Implemented with:

- HTML;
- CSS;
- JavaScript;
- Jinja2.

### Application layer

Implemented with Flask and responsible for:

- routing;
- sessions;
- form processing;
- appointment logic;
- status updates;
- messaging;
- translations.

### Data layer

Implemented using SQLite.

---

## Application Workflow

<p align="center">
  <img
    src="assets/workflow.png"
    alt="Khouloud Fekih application workflow"
    width="100%"
  >
</p>

The workflow connects patient activity with administrator validation.

### Patient workflow

```text
Browse Website
      │
      ▼
Register / Login
      │
      ▼
Submit Appointment Request
      │
      ▼
Pending Status
      │
      ▼
View Dashboard
      │
      ▼
Receive Updated Status
      │
      ▼
Use Messaging
```

### Administrator workflow

```text
Receive Appointment Request
      │
      ▼
Review Patient Information
      │
      ▼
Confirm / Cancel / Return to Pending
      │
      ▼
Update Patient Dashboard
      │
      ▼
Send Notification
```

---

## Database Design

<p align="center">
  <img
    src="assets/database.png"
    alt="Khouloud Fekih platform database schema"
    width="100%"
  >
</p>

The application uses a relational SQLite database.

### Main entities

- users;
- appointments;
- messages;
- notifications;
- administrators.

### Conceptual relationships

```text
USER
  │
  ├── has many APPOINTMENTS
  ├── has many NOTIFICATIONS
  └── participates in MESSAGES

ADMIN
  │
  └── participates in MESSAGES
```

### Users

Potential fields include:

- ID;
- name;
- email;
- phone;
- password data;
- preferred language;
- creation date.

### Appointments

Potential fields include:

- ID;
- user ID;
- consultation type;
- desired date;
- desired time;
- reason;
- status;
- creation date.

### Messages

Potential fields include:

- ID;
- sender;
- recipient;
- content;
- reading status;
- creation date.

### Notifications

Potential fields include:

- ID;
- user ID;
- title;
- content;
- reading status;
- creation date.

### Administrators

Potential fields include:

- ID;
- username;
- email;
- authentication data;
- creation date.

> The diagram presents the functional database model. Refer to the actual SQLite schema in the application for the definitive field definitions.

---

## Security Design

<p align="center">
  <img
    src="assets/security.png"
    alt="Khouloud Fekih platform security and access control"
    width="100%"
  >
</p>

Security is based on controlled access and separation between public, patient and administrative functions.

### Security principles

- protected patient routes;
- protected administrator routes;
- role separation;
- authenticated sessions;
- server-side validation;
- controlled status actions;
- database parameterisation;
- minimal exposure of user information;
- logout support.

### Input validation

Forms should validate:

- required fields;
- email format;
- phone format;
- date format;
- selected consultation type;
- selected time;
- text length.

### Access checks

Before displaying protected resources, the application verifies the appropriate session.

```text
Request to Protected Page
          │
          ▼
Session Available?
     ┌────┴────┐
     │         │
    Yes        No
     │         │
     ▼         ▼
Role Check   Redirect to Login
     │
     ▼
Authorised Resource
```

### Important security notice

This repository must never contain:

- real patient data;
- production credentials;
- private database backups;
- secret keys;
- sensitive clinical information.

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python | Application logic |
| Framework | Flask | Routing, sessions and request handling |
| Template engine | Jinja2 | Dynamic HTML rendering |
| Database | SQLite | Persistent relational storage |
| Frontend | HTML5 | Page structure |
| Styling | CSS3 | Responsive premium interface |
| Interactions | JavaScript | Dynamic frontend behaviour |
| Content | Python dictionaries / content module | Multilingual content management |
| Authentication | Flask sessions | Protected patient and admin areas |
| Version control | Git and GitHub | Source-code management |

### Main technical keywords

```text
Python
Flask
SQLite
Jinja2
HTML5
CSS3
JavaScript
Session Authentication
Responsive Design
Multilingual Web Development
RTL Support
Appointment Management
Admin Dashboard
Patient Portal
Private Messaging
Notifications
```

---

## Frontend Design

The interface follows a consistent visual design system.

### Colour direction

- dark plum;
- warm peach;
- cream and off-white;
- soft green for confirmation;
- soft yellow for pending states;
- soft red for cancellations.

### Typography

The design combines:

- an elegant serif typeface for editorial headings;
- a clean sans-serif typeface for navigation, labels and body content.

### Components

- rounded cards;
- pill buttons;
- status badges;
- navigation controls;
- language selector;
- notification counter;
- appointment cards;
- dashboard metrics;
- message bubbles;
- responsive forms.

### User-experience principles

- clear visual hierarchy;
- limited cognitive load;
- explicit appointment statuses;
- prominent primary actions;
- consistent spacing;
- accessible labels;
- calm visual identity.

---

## Responsive Design

The platform is designed to adapt across:

- desktop computers;
- tablets;
- mobile devices.

### Responsive considerations

- flexible containers;
- stacked form fields;
- adaptive navigation;
- scalable typography;
- touch-friendly buttons;
- responsive cards;
- RTL layout support;
- image resizing.

### Desktop experience

The desktop layout uses:

- wide multi-column sections;
- large editorial headings;
- side-by-side forms and instructions;
- dashboard metric grids.

### Mobile evolution

A production-ready mobile version should include:

- collapsible navigation;
- single-column forms;
- simplified dashboard cards;
- optimised conversation layout;
- reduced decorative content.

---

## Repository Structure

```text
psychologist-appointment-platform/
│
├── assets/
│   ├── accueil.png
│   ├── architecture.png
│   ├── conversation.png
│   ├── database.png
│   ├── espacepatientrendezvous.png
│   ├── formulaire.png
│   ├── gestiondemandes.png
│   ├── logo.png
│   ├── security.png
│   ├── tableaudebord.png
│   └── workflow.png
│
├── database/
│   └── psychologue.db
│
├── static/
│   ├── css/
│   │   ├── premium-theme.css
│   │   └── style.css
│   │
│   ├── images/
│   │   ├── cabinet-khouloud-fekih-psychologie-enfants.jpg
│   │   ├── centre-education-enfants-monastir.jpg
│   │   ├── difficultes-scolaires-apprentissages-enfants-a-monastir.jpg
│   │   ├── imm-el-makateb-monastir.jpg
│   │   ├── khouloud.jpeg
│   │   ├── Psychological-Montessori-Solutions-monastir.jpg
│   │   ├── psychologie-enfants-education-monastir.jpg
│   │   └── troubles-enfants-psychologie-monastir.jpg
│   │
│   └── js/
│       └── main.js
│
├── templates/
│   ├── about.html
│   ├── admin_conversation.html
│   ├── admin_dashboard.html
│   ├── admin_login.html
│   ├── admin_messages.html
│   ├── appointment.html
│   ├── appointment_success.html
│   ├── base.html
│   ├── contact.html
│   ├── index.html
│   ├── login.html
│   ├── patient_dashboard.html
│   ├── patient_messages.html
│   ├── services.html
│   └── signup.html
│
├── .gitignore
├── app.py
├── content.py
├── requirements.txt
└── README.md
```

### Main application files

#### `app.py`

Contains the Flask application and principal backend logic.

#### `content.py`

Contains centralised content used by the multilingual interface.

#### `premium-theme.css`

Defines the premium visual system.

#### `main.js`

Contains client-side interactions.

#### `templates/`

Contains the Jinja2 interface pages.

---

## Installation

### Prerequisites

Install:

- Python 3.10 or later;
- Git;
- pip.

### Clone the repository

```bash
git clone https://github.com/sarah-falehh/psychologist-appointment-platform.git
cd psychologist-appointment-platform
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate on Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Activate on Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

### Activate on Linux or macOS

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuration

Create an environment file for local configuration if the application uses environment variables.

```text
.env
```

Example:

```env
FLASK_SECRET_KEY=replace_with_a_secure_random_value
FLASK_ENV=development
DATABASE_PATH=database/psychologue.db
```

Do not publish the real `.env` file.

Add it to `.gitignore`:

```gitignore
.env
*.env
!.env.example
```

### Secret key

A production secret key should:

- be long;
- be random;
- never appear directly in the public repository;
- differ between development and production.

---

## Running the Application

From the project root:

```bash
python app.py
```

The development server should start locally.

Open:

```text
http://127.0.0.1:5000
```

### Flask development notice

The built-in Flask server is suitable for development.

It should not be used directly as the production server.

---

## Application Routes

Based on the application pages, the platform includes routes corresponding to the following areas.

### Public routes

```text
/
/about
/services
/contact
```

### Authentication

```text
/signup
/login
/logout
```

### Patient area

```text
/mon-espace
/mon-espace/messages
/rendez-vous
```

### Administrator area

```text
/admin/login
/admin
/admin/messages
/admin/conversation
```

> Exact route names should be confirmed in `app.py`, as URL structures may evolve.

---

## Testing the Platform

### Public website

Verify:

- homepage rendering;
- language switching;
- navigation;
- links;
- images;
- contact page.

### Registration and login

Test:

- valid account registration;
- duplicate email handling;
- incorrect credentials;
- logout;
- protected route redirection.

### Appointment requests

Test:

- missing fields;
- invalid dates;
- invalid phone numbers;
- available consultation types;
- request creation;
- patient dashboard display.

### Administrator actions

Test:

- administrator login;
- dashboard statistics;
- request search;
- filtering;
- confirmation;
- cancellation;
- pending-status restoration.

### Messaging

Test:

- patient message creation;
- administrator reply;
- message ordering;
- timestamp display;
- conversation isolation.

### Multilingual interface

Verify:

- French content;
- Arabic translation;
- Arabic RTL layout;
- English content;
- language persistence.

---

## Deployment Considerations

The current application uses Flask and SQLite.

### Development architecture

```text
Browser
   │
   ▼
Flask Development Server
   │
   ▼
SQLite
```

### Production architecture

```text
Browser
   │
   ▼
HTTPS Reverse Proxy
   │
   ▼
Production WSGI Server
   │
   ▼
Flask Application
   │
   ▼
Production Database
```

### Recommended production components

- Gunicorn or Waitress;
- Nginx or Apache;
- HTTPS;
- environment-based secrets;
- database backups;
- application logging;
- access monitoring;
- secure hosting;
- production database migration where required.

### SQLite considerations

SQLite is appropriate for:

- development;
- demonstrations;
- low-traffic prototypes;
- local applications.

For higher traffic or concurrent production use, consider:

- MySQL;
- PostgreSQL;
- a managed relational database.

---

## Privacy and Data Protection

The platform concerns a psychology practice, which requires particular caution.

### Public repository policy

The repository must include only:

- fictional test accounts;
- synthetic appointment data;
- demonstration messages;
- non-sensitive content.

The repository must not include:

- real patient names;
- real telephone numbers;
- real patient email addresses;
- medical information;
- consultation notes;
- private conversations;
- real production database files.

### Database exclusion

The production database should remain excluded from Git:

```gitignore
database/*.db
database/*.sqlite
database/*.sqlite3
```

### Demonstration data

Screenshots and sample records should use:

- invented identities;
- generic email addresses;
- fictional telephone numbers;
- neutral message content.

---

## Limitations

- The platform is a custom web application and not certified medical software.
- The messaging area is not an emergency communication service.
- SQLite may not be appropriate for high-concurrency production usage.
- The application requires a secure production deployment configuration.
- Real patient data must never be committed to the repository.
- Appointment availability depends on the scheduling logic configured in the application.
- Automated email or SMS delivery may require external services.
- Accessibility should be validated with dedicated auditing tools.
- Production use requires legal, privacy and security review.
- The screenshots show demonstration records and should contain no real patient data.

---

## Future Improvements

### Appointment scheduling

- real-time availability calendar;
- automatic prevention of double booking;
- configurable working hours;
- vacation and absence management;
- appointment rescheduling;
- recurring appointments.

### Notifications

- email confirmation;
- SMS reminders;
- WhatsApp reminders;
- appointment reminder scheduling;
- unread-notification filtering.

### Messaging

- attachment support;
- message search;
- read receipts;
- archived conversations;
- conversation categories.

### Patient portal

- profile editing;
- password reset;
- appointment calendar;
- downloadable confirmations;
- communication preferences.

### Administrator portal

- calendar view;
- weekly agenda;
- monthly statistics;
- patient directory;
- appointment export;
- CSV and PDF reporting;
- activity logs.

### Security

- CSRF protection;
- login-rate limiting;
- secure password-reset workflow;
- stricter audit logging;
- database encryption strategy;
- automated dependency scanning.

### Engineering

- Flask Blueprints;
- application factory pattern;
- automated tests;
- Docker;
- continuous integration;
- structured logging;
- production configuration profiles;
- database migrations.

### Accessibility

- keyboard-navigation audit;
- screen-reader testing;
- colour-contrast validation;
- accessible form-error reporting;
- improved Arabic accessibility.

### Deployment

- production WSGI configuration;
- HTTPS;
- managed database;
- automated backups;
- monitoring;
- uptime alerts.

---

## Author

## Sarah Faleh

Final-Year Software Engineering Student  
Specialisation in Data Science and Artificial Intelligence

### Contribution

- full-stack web development;
- Flask backend;
- SQLite data model;
- appointment workflow;
- patient portal;
- administrator dashboard;
- messaging system;
- multilingual interface;
- premium UI design;
- frontend integration;
- project documentation.

### GitHub

[github.com/sarah-falehh](https://github.com/sarah-falehh)

### LinkedIn

[linkedin.com/in/sarah-faleh](https://www.linkedin.com/in/sarah-faleh)

---

## Acknowledgements

This platform was designed and developed for the professional activity of clinical psychologist **Khouloud Fekih** in Monastir, Tunisia.

The project demonstrates the application of software-engineering principles to a real professional need through:

- requirements analysis;
- interface design;
- multilingual content;
- role-based workflows;
- appointment management;
- persistent data storage;
- patient–professional communication.

---

<div align="center">

<img src="assets/logo.png" alt="Khouloud Fekih platform logo" width="250">

<br>

### Comprendre. Apaiser. Avancer.

**A thoughtful digital experience for appointment management, communication and patient support.**

</div>