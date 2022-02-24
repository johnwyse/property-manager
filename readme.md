# Property

<a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" alt="Powered by Django." title="Powered by Django." /></a>

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/made-with-javascript.svg)](https://forthebadge.com)

### Overview

Property is a web app that connects property managers and tenants. After registering an account and connecting to a certain property/properties, tenants and managers can message each other (with photos attached), managers can post lease documents, and tenants can report, update, and resolve maintenance issues. Users are alerted of unresolved issues and unread messages upon logging in. 

I was inspired to create this web app because of my real-life frustration with my own property manager and desire for better communication. 

### Models
There are four main models: Users, Units, Messages, and Issues.

All users are classified as either a manager or a tenant. Managers can be joined to multiple units, while tenants can be joined to only one unit. All html views are based on whether a user is a tenant or manager.

Units are joined to one manager and one tenant user. Units are created by managers and later claimed by tenants upon registration. Unit objects also contain image and pdf files related to the unit.

Messages are joined to users only and have a recipient and sender, which must be one tenant and one manager. Messages are also automatically marked as read or unread by an API call.

Issues are connected to units only and are marked as resolved or unresolved. Only tenants may officially change an issue's status to resolved.

##### Diagram
![](readme_files/property_models.png)


### File Tree

```
📦capstone
 ┣ 📂capstone
 ┃ ┣ 📜asgi.py
 ┃ ┣ 📜settings.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜wsgi.py
 ┣ 📂media
 ┣ 📂property
 ┃ ┣ 📂migrations
 ┃ ┣ 📂static
 ┃ ┃ ┣ 📂property
 ┃ ┃ ┃ ┣ 📜favicon.png
 ┃ ┃ ┃ ┣ 📜favicon2.png
 ┃ ┃ ┃ ┣ 📜index.js
 ┃ ┃ ┃ ┣ 📜issues.js
 ┃ ┃ ┃ ┣ 📜messages.js
 ┃ ┃ ┃ ┣ 📜notifications.js
 ┃ ┃ ┃ ┣ 📜personal_styles.css
 ┃ ┃ ┃ ┣ 📜resume.pdf
 ┃ ┃ ┃ ┗ 📜styles.css
 ┃ ┣ 📂templates
 ┃ ┃ ┣ 📂property
 ┃ ┃ ┃ ┣ 📜add_property.html
 ┃ ┃ ┃ ┣ 📜error.html
 ┃ ┃ ┃ ┣ 📜index.html
 ┃ ┃ ┃ ┣ 📜issues.html
 ┃ ┃ ┃ ┣ 📜layout.html
 ┃ ┃ ┃ ┣ 📜login.html
 ┃ ┃ ┃ ┣ 📜messages.html
 ┃ ┃ ┃ ┣ 📜personal_index.html
 ┃ ┃ ┃ ┣ 📜profile.html
 ┃ ┃ ┃ ┣ 📜register.html
 ┃ ┃ ┃ ┣ 📜resume.html
 ┃ ┃ ┃ ┣ 📜unit.html
 ┃ ┃ ┃ ┣ 📜unit_issues.html
 ┃ ┃ ┃ ┗ 📜unit_messages.html
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜personal_urls.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┗ 📜views.py
 ┣ 📜db.sqlite3
 ┣ 📜manage.py
 ┣ 📜readme.md
 ┗ 📜requirements.txt
 ```


### Routes

###### index: /
The index or home route is called after successful login. For managers, all properties are displayed. For tenants, unit info is displayed as well as dropdown forms to report a new issue or send a message to their property manager.

Manager Home
![](readme_files/manager_home.png)


Tenant Home
![](readme_files/tenant_home.png)

###### profile: /profile
The profile route renders a page that shows information about the user and gives an opportunity to upload a profile picture which then appears on messages.

Manager Profile
![](readme_files/profile.png)

###### unit: unit/<int:unit_id>
The unit view is restricted to just property managers and shows a page similar to a tenant's home page, but specific to each unit managed.

###### messages: /messages, /unit_messages/<int:unit_id>
The messages view renders a page for managers that creates links to message threads with each active tenant. It also shows the number of unread messages in each thread. For tenants, the messages thread redirects them to unit_messages for their specific unit.

The unit_messages view renders a page that shows all messages between a property manager and a specific tenant. It has pagination and displays 10 messages (and images if present) in reverse chronological order. It also displays if sent messages are read or unread by the recipient.

Unit Messages
![](readme_files/messages.png)


###### login, logout, register: /login, /logout, /register




### Distinctiveness and Complexity

### Drawbacks / Additional Features
