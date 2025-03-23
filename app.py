from flask import Flask, render_template, request, redirect, url_for, send_file
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Riemann Sum and Integral
def riemann_sum(f, a, b, n, method='left'):
    dx = (b - a) / n
    x = np.linspace(a, b, n+1)
    if method == 'left':
        x_samples = x[:-1]
    elif method == 'right':
        x_samples = x[1:]
    elif method == 'midpoint':
        x_samples = (x[:-1] + x[1:]) / 2
    else:
        raise ValueError("Method must be 'left', 'right', or 'midpoint'.")
    return np.sum(f(x_samples) * dx)

# Home Page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        calculation_type = request.form.get("calculation_type")
        a = float(request.form.get("a"))
        b = float(request.form.get("b"))
        n = int(request.form.get("n"))
        method = request.form.get("method")
        f = lambda x: x**2  # Example function: f(x) = x^2

        # Calculate Riemann sum
        result = riemann_sum(f, a, b, n, method)

        # Handle image upload
        if "image" in request.files:
            image = request.files["image"]
            if image.filename != "":
                img = Image.open(image)
                img.thumbnail((200, 200))  # Resize image
                img_path = "static/uploaded_image.png"
                img.save(img_path)
                return render_template("index.html", result=result, calculation_type=calculation_type, image_uploaded=True)

        return render_template("index.html", result=result, calculation_type=calculation_type)
    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
