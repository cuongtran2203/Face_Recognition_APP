import uvicorn

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Camera.camera_multi import Camera_extract
# from camera_single import Camera
from Camera.camera_multi import Camera as CameraRECOG

from coreAI.create_db import *

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
   return templates.TemplateResponse('index.html', {"request": request})

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        encode_frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encode_frame + b'\r\n')

@app.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return  StreamingResponse(gen(CameraRECOG()),
                    media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/add_user",response_class=HTMLResponse)
async def add_user(request: Request):
    return templates.TemplateResponse('add_user.html', {"request": request})

cam_ext = None
@app.get("/streaming",response_class=HTMLResponse)
async def streaming():
    global cam_ext
    cam_ext = Camera_extract()
    return  StreamingResponse(gen(cam_ext),
                    media_type='multipart/x-mixed-replace; boundary=frame')

@app.post("/add_user", response_class=HTMLResponse)
async def handle_form(request: Request, fname: str = Form(...)):
    global cam_ext
    if cam_ext:
        _, frame = cam_ext.get_frame()
        print(frame)
        print(f'{fname}')
        if len((f'{fname}'))>0 :
            create_user(frame,f'{fname}')
        return templates.TemplateResponse("add_user.html", context= {"request": request, "fname": fname})

if __name__ == "__main__":
    print('stop: ctrl+c')
    uvicorn.run(app, host="localhost", port=8000)
