import aiohttp
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.requests import Request

app = FastAPI()
VIDEO_URL = "https://cdn.discordapp.com/attachments/821000236788744216/1206034243374022736/17448eddd20dbbc7f875003b23e593c363352d31179d1b39babbd720c836e015_1.mp4?ex=676e9daa&is=676d4c2a&hm=6fe2244d00abdca8ce194f659096dc11b6c917ae8eaa67b8f476d3931c952b76&"

async def fetch_data(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content.iter_chunked(1024):
                yield chunk

async def stream_generator():
    async for chunk in fetch_data(VIDEO_URL):
        yield chunk

@app.get("/")
async def read_root(request: Request):
    return HTMLResponse(
        """
        <video id="videoPlayer" width="640" height="360" controls>
            <source src="/stream" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                var videoPlayer = document.getElementById('videoPlayer');
                videoPlayer.play();
            });
        </script>
        """
    )

@app.get("/stream")
async def stream_video(request: Request):
    return StreamingResponse(stream_generator(), media_type="application/octet-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
