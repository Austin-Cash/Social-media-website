git clone https://github.com/your-username/social-media-website.git  #clone the repo
cd social-media-website

#start back end
pip install -r requirements.txt  # OR: pip install fastapi sqlalchemy uvicorn passlib[bcrypt] python-jose
uvicorn main:app --reload

#start front end, open another terminal
cd frontend
npm install
npm run dev