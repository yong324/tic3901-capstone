first time starting front end:
  cd frontend
  npm install

to start front end
  npm run dev

first time starting back end
  cd app
  .\venv\Scripts\Activate.ps1
  source venv/script/activate
  pip install -r requirements.txt
  
to start backend
  .\venv\Scripts\Activate.ps1
  flask run

docker commands
open docker desktop application
- docker compose commands
  - open git bash and run following command:
    - docker-compose up --build

run tests
  frontend:
    npm run test -- --coverage
  backend:
    cd backend
    pytest

to pytest backend w coverage
  pytest --cov=app app/tests
  
to pytest backend w full html report
  pytest --cov=app --cov-report=html
