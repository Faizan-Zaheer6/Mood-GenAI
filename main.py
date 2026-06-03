from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from schemas import MoodRequest, MoodResponse
from ai_logic import generate_mood_content

app = FastAPI(title="AI Mood Booster API")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.post("/generate-quote", response_model=MoodResponse)
async def get_quote(request: MoodRequest):
    # AI logic ko call kar ke result wapis bheja ja raha hai
    result = await generate_mood_content(request)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)