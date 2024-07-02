import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
import requests
import json

MODEL_INPUT_SIZE = 28 
CANVAS_SIZE = MODEL_INPUT_SIZE * 8

st.write("Draw something here")
canvas_res = st_canvas(
    fill_color="black",
    stroke_width=15,
    stroke_color="white",
    width=CANVAS_SIZE,
    height=CANVAS_SIZE,
    drawing_mode="freedraw",
    key="canvas",
    display_toolbar=True,
)

# Get image
if canvas_res.image_data is not None:
    # Scale down image to the model input size
    img = cv2.resize(canvas_res.image_data.astype("uint8"), (MODEL_INPUT_SIZE, MODEL_INPUT_SIZE))

    # Rescaled image upwards to show
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rescaled = cv2.resize(img, (CANVAS_SIZE, CANVAS_SIZE), interpolation=cv2.INTER_NEAREST)
    st.write("Model input")
    st.image(img_rescaled)

    # Predict on the press of a button
    if canvas_res.image_data is not None:
        # Scale down image to the model input size
        img = cv2.resize(canvas_res.image_data.astype("uint8"), (MODEL_INPUT_SIZE, MODEL_INPUT_SIZE))

        # Convert image to grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Normalize image (if necessary)
        img_normalized = img_gray.astype(np.float32) / 255.0

        img_list = img_normalized.tolist()
        # img_json = json.dumps(img_list)

        # # Reshape image for model input (if necessary)
        # img_input = np.expand_dims(img_normalized, axis=0)

        # # Convertir en bytes pour l'envoi à l'API
        # img_bytes = img_input.tobytes()
        
        if st.button('Predict'):
            # Envoyer l'image à l'API FastAPI
            response = requests.post('http://backend:8000/api/v1/predict', json={'file': img_list})

            # Vérifier la réponse de l'API
            if response.status_code == 200:
                prediction = response.json()['prediction'][0]
                st.write(f'Prédiction : {prediction}')
            else:
                st.write(f'Erreur lors de la requête : {response.status_code}')

        
        # if st.button("Predict"):
        #     try:
        #         response_predict = requests.post(url=PREDICT_URL,
        #                                         data=json.dumps({"input_image": img.tolist()}))
        #         if response_predict.ok:
        #             res = response_predict.json()
        #             st.markdown(f"**Prediction**: {res['results']['pred']}")

        #         else:
        #             st.write("Some error occured")
        #     except ConnectionError as e:
        #         st.write("Couldn't reach backend")
