# Racehorse Participation Tracker
A Django-based backend project for managing horse races, jockeys, and participations — built using class-based views without Django REST Framework.

## Project Structure
This project includes models and views for managing:
- Horses
- Jockeys
- Races
- Participations (entries of horses & jockeys in races)

## Features
- CRUD operations via class-based views (View)
- Data exchange through JSON responses (for use in Postman or frontend apps)
- Validation to prevent duplicate participations in the same race
- Auto-detecting winning participant (e.g. if position == 1)
- Detail views return related data (e.g. participations of a horse)

## Setup Instructions
1. Clone the repo:
```bash
git clone https://github.com/yourusername/racehorse-tracker.git
cd racehorse-tracker
```
2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Apply migrations
```bash
python manage.py migrate
```
5. Run the development server
```bash
python manage.py runserver
```

## API Endpoints (for Postman)
| Method | Endpoint               | Description                             |
| ------ | ---------------------- | --------------------------------------- |
| GET    | `/racehorses/`             | List all racehorse                         |
| GET    | `/racehorses/<int:pk>/`        | Get racehorse details (with participations) |
| POST   | `/racehorses/create/`      | Create a new racehorse                      |
| POST    | `/racehorses/<int:pk>/` | Update a racehorse                          |
| DELETE | `/racehorses/<int:pk>/` | Delete a racehorse                          |

**(Same pattern for /jockeys/, /races/, and /participations/)**

## Notes
- Use Postman or any API client to test the endpoints.
- Data is exchanged via JSON.
- No HTML templates are used — backend-only architecture.
- Postman: [Postman Link](https://gold-trinity-657630.postman.co/workspace/My-Workspace~f58b337a-3f8f-4968-84fc-e3dab3d451cf/collection/46171345-8be8ac86-8d6d-4de9-8f24-2cb3c090cd0d?action=share&source=copy-link&creator=46171345)

## Author
David Czar Porras
Github: [davidporras-opswerks](https://github.com/davidporras-opswerks)

