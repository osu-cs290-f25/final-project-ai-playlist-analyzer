from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# how to run the code
# python -m uvicorn run:app --reload --host 0.0.0.0 --port 7222

# then look at it with flip2.engr.oregonstate.edu:7222 or whatever port you set it as above
# http://flip2.engr.oregonstate.edu:7222

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    # return HTMLResponse(content="<h1>Hello World</h1>")


