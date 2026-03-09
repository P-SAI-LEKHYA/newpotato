from fastapi import FastAPI,File,UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware

MODEL= tf.keras.models.load_model("models/1.keras")
CLASS_NAMES=["Potato__Early_blight","Potato__Late_blight","Potato__healthy"]

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return "hey!!i am alive"

def read_file_as_image(data):
    image=np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
async def predict(
    file: UploadFile=File(...)
):
    image=read_file_as_image(await file.read())
    image_batch=np.expand_dims(image,0)
    prediction=MODEL.predict(image_batch)
    predicted_class=CLASS_NAMES[np.argmax(prediction[0])]
    confidence = float(np.max(prediction[0]))
    return{
        'class':predicted_class,
        'confidence':confidence
    }
   
    


if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)
